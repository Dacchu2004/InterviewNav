import os
import openai
import PyPDF2
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from extensions import db, jwt
from model import User, CV, PerformanceReport
from docx import Document
from flask_migrate import Migrate
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import logging
import uuid
import json

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object('config.Config')

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize extensions
db.init_app(app)
jwt.init_app(app)
migrate = Migrate(app, db)

# JWT error handlers for better error messages
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    logging.error("JWT token expired")
    return jsonify({"error": "Token has expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    logging.error(f"JWT invalid token error: {error_string}")
    return jsonify({"error": f"Invalid token: {error_string}"}), 422

@jwt.unauthorized_loader
def missing_token_callback(error_string):
    logging.error(f"JWT missing token error: {error_string}")
    return jsonify({"error": "Authorization token is missing"}), 401

# Enable CORS
CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize OpenAI client with timeout and retry configuration
client = openai.OpenAI(
    api_key=app.config['OPENAI_API_KEY'],
    timeout=60.0,  # 60 second timeout
    max_retries=3  # Retry up to 3 times
)

# In-memory storage for interview sessions (in production, use Redis or database)
interview_sessions = {}

# Helper Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_cv(file_path):
    text = ""
    ext = file_path.split('.')[-1].lower()
    try:
        if ext == 'pdf':
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text()
        elif ext == 'docx':
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text
    except Exception as e:
        logging.error(f"Error extracting text from CV: {e}")
    return text

def generate_interview_questions(cv_text, company_name, job_role, interview_level):
    """Generate interview questions based on CV text, company, role, and level - FIXED to include CV text"""
    
    # FIXED: Now includes CV text in the prompt
    base_prompt = (
        f"Based on the following CV/resume text, generate a list of 6 to 10 personalized interview questions "
        f"for a {job_role} position at {company_name}. "
        f"The questions should be tailored to the candidate's specific skills, experience, and background mentioned in their CV.\n\n"
        f"CV/RESUME TEXT:\n{cv_text}\n\n"
        f"Generate interview questions that focus on the candidate's skills, experience, and industry knowledge mentioned in the CV above."
    )

    if interview_level == 'Beginner':
        level_prompt = "The questions should focus on basic knowledge, entry-level skills, and general understanding of the field."
    elif interview_level == 'Intermediate':
        level_prompt = "The questions should focus on practical experience, challenges faced in the role, and problem-solving skills."
    elif interview_level == 'Advanced':
        level_prompt = "The questions should focus on advanced technical knowledge, leadership skills, and strategic thinking."
    else:
        level_prompt = "Please provide a balanced set of questions."

    prompt = f"{base_prompt}\n\n{level_prompt}\n\nFormat the questions as a numbered list, one question per line."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            timeout=60.0
        )
        return response.choices[0].message.content.strip()
    except openai.APIError as e:
        logging.error(f"OpenAI API error generating interview questions: {e}")
        return "Unable to generate interview questions at this time. Please check your OpenAI API key and try again later."
    except openai.APIConnectionError as e:
        logging.error(f"OpenAI connection error: {e}")
        return "Unable to connect to OpenAI service. Please check your internet connection and try again."
    except Exception as e:
        logging.error(f"Error generating interview questions: {type(e).__name__}: {e}")
        return "Unable to generate interview questions at this time. Please try again later."

def generate_personalized_feedback(responses, questions):
    """Generate personalized feedback based on user responses"""
    try:
        # Include questions in feedback generation for better context
        feedback_prompt = (
            "Based on the following interview questions and the candidate's responses, provide personalized and detailed feedback for improvement. "
            "Analyze the responses and give detailed suggestions on how the candidate can improve their interview skills, including communication skills, "
            "confidence, areas where they went wrong, and general advice for success.\n\n"
        )
        
        for idx, (question, response) in enumerate(zip(questions, responses), 1):
            feedback_prompt += f"Question {idx}: {question}\nCandidate's Answer: {response}\n\n"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": feedback_prompt}],
            max_tokens=800,
            timeout=60.0
        )
        feedback = response.choices[0].message.content.strip()
        return feedback
    except openai.APIError as e:
        logging.error(f"OpenAI API error generating feedback: {e}")
        return "Unable to generate feedback at this time. Please check your OpenAI API key and try again later."
    except openai.APIConnectionError as e:
        logging.error(f"OpenAI connection error generating feedback: {e}")
        return "Unable to connect to OpenAI service. Please check your internet connection and try again."
    except Exception as e:
        logging.error(f"Error generating feedback: {type(e).__name__}: {e}")
        return "Unable to generate personalized feedback at this time. Please try again later."

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "API is running"}), 200

@app.route('/api/debug/token', methods=['GET'])
@jwt_required()
def debug_token():
    """Debug endpoint to test JWT token"""
    try:
        user_id = get_jwt_identity()
        return jsonify({
            "status": "Token is valid",
            "user_id": user_id,
            "message": "JWT authentication working correctly"
        }), 200
    except Exception as e:
        logging.error(f"Token debug error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({"error": "Username, email, and password are required"}), 400

        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "Email already exists"}), 400

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return jsonify({"error": "Username already exists"}), 400

        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()

        # Generate JWT token (identity must be a string)
        access_token = create_access_token(identity=str(new_user.id))

        return jsonify({
            "message": "Account created successfully",
            "user": new_user.to_dict(),
            "access_token": access_token
        }), 201

    except Exception as e:
        logging.error(f"Registration error: {e}")
        db.session.rollback()
        return jsonify({"error": "Registration failed"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            if not user.is_active:
                return jsonify({"error": "Account is inactive"}), 403

            # Generate JWT token (identity must be a string)
            access_token = create_access_token(identity=str(user.id))
            return jsonify({
                "message": "Login successful",
                "user": user.to_dict(),
                "access_token": access_token
            }), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    except Exception as e:
        logging.error(f"Login error: {e}")
        return jsonify({"error": "Login failed"}), 500

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        # Convert to int since JWT stores as string but DB uses int
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Get user's CVs
        cvs = [cv.to_dict() for cv in user.cvs]
        
        return jsonify({
            "user": user.to_dict(),
            "cvs": cvs
        }), 200

    except Exception as e:
        logging.error(f"Profile error: {e}")
        return jsonify({"error": "Failed to fetch profile"}), 500

@app.route('/api/upload-cv', methods=['POST'])
@jwt_required()
def upload_cv():
    try:
        user_id = get_jwt_identity()
        
        if 'cv_file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['cv_file']
        company_name = request.form.get('company_name')
        job_role = request.form.get('job_role')
        interview_level = request.form.get('interview_level')

        if not company_name or not job_role or not interview_level:
            return jsonify({"error": "Company name, job role, and interview level are required"}), 400

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Please upload PDF or DOCX"}), 400

        # Save file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text from CV
        cv_text = extract_text_from_cv(file_path)
        if not cv_text.strip():
            return jsonify({"error": "Could not extract text from CV. Please upload a valid file."}), 400

        # Generate interview questions (FIXED: CV text now included)
        questions_text = generate_interview_questions(cv_text, company_name, job_role, interview_level)
        if questions_text.startswith("Unable"):
            return jsonify({"error": questions_text}), 500

        # Parse questions (split by newlines and filter empty lines)
        questions = [q.strip() for q in questions_text.split('\n') if q.strip() and not q.strip().startswith('#')]
        # Remove numbering if present
        questions = [q.split('.', 1)[-1].strip() if '.' in q[:3] else q for q in questions]

        # Save CV to database (convert user_id to int)
        new_cv = CV(
            file_path=file_path,
            company_name=company_name,
            job_role=job_role,
            interview_level=interview_level,
            user_id=int(user_id)
        )
        db.session.add(new_cv)
        db.session.commit()

        # Create interview session (store user_id as string for consistency with JWT)
        session_id = str(uuid.uuid4())
        interview_sessions[session_id] = {
            'user_id': str(user_id),  # Store as string to match JWT format
            'cv_id': new_cv.id,
            'questions': questions,
            'responses': [],
            'current_question': 0
        }

        return jsonify({
            "message": "CV uploaded successfully",
            "session_id": session_id,
            "questions": questions,
            "cv": new_cv.to_dict()
        }), 200

    except Exception as e:
        logging.error(f"CV upload error: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to upload CV"}), 500

@app.route('/api/interview/question', methods=['GET'])
@jwt_required()
def get_current_question():
    try:
        user_id = get_jwt_identity()
        session_id = request.args.get('session_id')

        if not session_id or session_id not in interview_sessions:
            return jsonify({"error": "Invalid or expired session"}), 404

        session_data = interview_sessions[session_id]
        # Compare as strings since both are stored as strings
        if str(session_data['user_id']) != str(user_id):
            return jsonify({"error": "Unauthorized access to session"}), 403

        questions = session_data['questions']
        current_index = session_data['current_question']

        if current_index >= len(questions):
            return jsonify({
                "completed": True,
                "message": "Interview completed"
            }), 200

        return jsonify({
            "question": questions[current_index],
            "progress": current_index + 1,
            "total": len(questions),
            "session_id": session_id
        }), 200

    except Exception as e:
        logging.error(f"Get question error: {e}")
        return jsonify({"error": "Failed to get question"}), 500

@app.route('/api/interview/answer', methods=['POST'])
@jwt_required()
def submit_answer():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        session_id = data.get('session_id')
        answer = data.get('answer')

        if not session_id or session_id not in interview_sessions:
            return jsonify({"error": "Invalid or expired session"}), 404

        session_data = interview_sessions[session_id]
        # Compare as strings since both are stored as strings
        if str(session_data['user_id']) != str(user_id):
            return jsonify({"error": "Unauthorized access to session"}), 403

        if not answer or not answer.strip():
            return jsonify({"error": "Answer is required"}), 400

        # Store answer
        session_data['responses'].append(answer.strip())
        session_data['current_question'] += 1

        questions = session_data['questions']
        current_index = session_data['current_question']

        if current_index >= len(questions):
            return jsonify({
                "completed": True,
                "message": "All questions answered"
            }), 200

        return jsonify({
            "message": "Answer submitted successfully",
            "next_question": questions[current_index],
            "progress": current_index + 1,
            "total": len(questions)
        }), 200

    except Exception as e:
        logging.error(f"Submit answer error: {e}")
        return jsonify({"error": "Failed to submit answer"}), 500

@app.route('/api/report/generate', methods=['POST'])
@jwt_required()
def generate_report():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        session_id = data.get('session_id')

        if not session_id or session_id not in interview_sessions:
            return jsonify({"error": "Invalid or expired session"}), 404

        session_data = interview_sessions[session_id]
        # Compare as strings since both are stored as strings
        if str(session_data['user_id']) != str(user_id):
            return jsonify({"error": "Unauthorized access to session"}), 403

        questions = session_data['questions']
        responses = session_data['responses']
        cv_id = session_data['cv_id']

        if len(responses) != len(questions):
            return jsonify({"error": "Not all questions have been answered"}), 400

        # Calculate metrics
        accuracy_level = f"{min(100, (len(responses) / len(questions)) * 100):.2f}%"
        confidence_level = "High" if len(responses) == len(questions) else "Moderate"

        # Generate feedback (FIXED: Now saves to database)
        feedback = generate_personalized_feedback(responses, questions)

        # Create performance report
        new_report = PerformanceReport(
            accuracy_level=accuracy_level,
            confidence_level=confidence_level,
            total_questions=len(questions),
            correct_answers=len(responses),
            feedback=feedback,  # FIXED: Now saving feedback to database
            cv_id=cv_id
        )
        db.session.add(new_report)
        db.session.commit()

        # Prepare report data
        detailed_responses = [{"question": q, "answer": r} for q, r in zip(questions, responses)]
        
        report_data = {
            "total_questions": len(questions),
            "answers_received": len(responses),
            "accuracy_level": accuracy_level,
            "confidence_level": confidence_level,
            "detailed_responses": detailed_responses,
            "feedback": feedback
        }

        # Clean up session
        del interview_sessions[session_id]

        return jsonify({
            "message": "Report generated successfully",
            "report": report_data,
            "report_id": new_report.id
        }), 200

    except Exception as e:
        logging.error(f"Generate report error: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to generate report"}), 500

@app.route('/api/reports', methods=['GET'])
@jwt_required()
def get_reports():
    try:
        user_id = get_jwt_identity()
        # Convert to int since JWT stores as string but DB uses int
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Get all CVs and their reports
        reports_data = []
        for cv in user.cvs:
            for report in cv.performance_reports:
                reports_data.append({
                    "report": report.to_dict(),
                    "cv": cv.to_dict()
                })

        return jsonify({"reports": reports_data}), 200

    except Exception as e:
        logging.error(f"Get reports error: {e}")
        return jsonify({"error": "Failed to fetch reports"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

