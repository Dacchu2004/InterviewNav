import os
import openai
import PyPDF2
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from extensions import db, jwt
from extensions import db, jwt
from model import User, CV, PerformanceReport, InterviewSession
from docx import Document
from flask_migrate import Migrate
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import logging
import uuid
import json
from prompts import get_interview_questions_prompt, get_feedback_prompt

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
import httpx
# Create a custom HTTP client that disables SSL verification
http_client = httpx.Client(verify=False)

client = openai.OpenAI(
    api_key=app.config['OPENAI_API_KEY'],
    http_client=http_client, # Bypass SSL verification
    timeout=60.0,  # 60 second timeout
    max_retries=3  # Retry up to 3 times
)

# In-memory storage for interview sessions (in production, use Redis or database)
# Database storage for interview sessions is now used instead of in-memory dictionary

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

def generate_interview_questions(cv_text, company_name, job_role, interview_level, job_description=None):
    """Generate interview questions based on CV text, company, role, level and optional JD"""
    
    if interview_level == 'Beginner':
        level_prompt = "The questions should focus on basic knowledge, entry-level skills, and general understanding of the field."
    elif interview_level == 'Intermediate':
        level_prompt = "The questions should focus on practical experience, challenges faced in the role, and problem-solving skills."
    elif interview_level == 'Advanced':
        level_prompt = "The questions should focus on advanced technical knowledge, leadership skills, and strategic thinking."
    else:
        level_prompt = "Please provide a balanced set of questions."

    # FIXED: Now includes CV text in the prompt
    prompt = get_interview_questions_prompt(cv_text, job_role, company_name, level_prompt, job_description)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            timeout=60.0
        )
        return response.choices[0].message.content.strip()
    except openai.APIConnectionError as e:
        logging.error(f"OpenAI connection error: {e}")
        return "Unable to connect to OpenAI service. Please check your internet connection and try again."
    except openai.APIError as e:
        logging.error(f"OpenAI API error generating interview questions: {e}")
        return "Unable to generate interview questions at this time. Please check your OpenAI API key and try again later."
    except Exception as e:
        logging.error(f"Error generating interview questions: {type(e).__name__}: {e}")
        return "Unable to generate interview questions at this time. Please try again later."

def generate_personalized_feedback(responses, questions):
    """Generate personalized feedback based on user responses"""
    try:
        # Include questions in feedback generation for better context
        feedback_prompt = get_feedback_prompt(questions, responses)

        # Request JSON format explicitly
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": feedback_prompt}],
            response_format={ "type": "json_object" }, # Enforce JSON mode
            max_tokens=2500,
            timeout=60.0
        )
        content = response.choices[0].message.content.strip()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logging.error(f"Failed to decode AI JSON feedback: {content}")
            return {
                "overall_feedback": "Error parsing detailed feedback. " + content,
                "questions_analysis": []
            }
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
        job_description = request.form.get('job_description') # Optional
        interview_level = request.form.get('interview_level')

        if not company_name or not job_role or not interview_level:
            return jsonify({"error": "Company name, job role, and interview level are required"}), 400

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Please upload PDF or DOCX"}), 400

        # Save file with unique name to prevent collisions
        filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text from CV
        cv_text = extract_text_from_cv(file_path)
        if not cv_text.strip():
            # Try to cleanup before returning error
            try:
                os.remove(file_path)
            except: 
                pass
            return jsonify({"error": "Could not extract text from CV. Please upload a valid file."}), 400

        # Generate interview questions (includes CV text and optional JD)
        questions_text = generate_interview_questions(cv_text, company_name, job_role, interview_level, job_description)
        if questions_text.startswith("Unable"):
             # Try to cleanup on error
            try:
                os.remove(file_path)
            except: 
                pass
            return jsonify({"error": questions_text}), 500

        # Parse questions (split by newlines and filter empty lines)
        questions = [q.strip() for q in questions_text.split('\n') if q.strip() and not q.strip().startswith('#')]
        # Remove numbering if present
        questions = [q.split('.', 1)[-1].strip() if '.' in q[:3] else q for q in questions]

        # Save CV to database (convert user_id to int)
        new_cv = CV(
            file_path=file_path, # Note: We keep the path in DB even if file is deleted, or we could mark it as processed
            company_name=company_name,
            job_role=job_role,
            job_description=job_description,
            interview_level=interview_level,
            user_id=int(user_id)
        )
        db.session.add(new_cv)
        db.session.commit()

        # Create interview session in Database
        session_id = str(uuid.uuid4())
        new_session = InterviewSession(
            id=session_id,
            user_id=int(user_id),
            cv_id=new_cv.id,
            questions=questions,
            responses=[],
            current_question_index=0
        )
        db.session.add(new_session)
        db.session.commit()
        
        # Cleanup: Delete the file after processing to save space
        try:
             # Force garbage collection if needed or just wait. 
             # sometimes PyPDF2 keeps file open.
             import gc
             gc.collect()
             if os.path.exists(file_path):
                 os.remove(file_path)
        except Exception as e:
            # Log but don't fail the request
            logging.error(f"Warning: Could not delete file {file_path}: {e}")

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

        session = InterviewSession.query.get(session_id)
        
        if not session:
            return jsonify({"error": "Invalid or expired session"}), 404

        # Compare user_ids
        if session.user_id != int(user_id):
            return jsonify({"error": "Unauthorized access to session"}), 403

        questions = session.questions
        current_index = session.current_question_index

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

        session = InterviewSession.query.get(session_id)
        
        if not session:
            return jsonify({"error": "Invalid or expired session"}), 404

        # Compare user_ids
        if session.user_id != int(user_id):
            return jsonify({"error": "Unauthorized access to session"}), 403

        if not answer or not answer.strip():
            return jsonify({"error": "Answer is required"}), 400

        # Store answer in DB
        current_responses = session.responses
        current_responses.append(answer.strip())
        session.responses = current_responses # Trigger setter
        session.current_question_index += 1
        
        db.session.commit()

        questions = session.questions
        current_index = session.current_question_index

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

        session = db.session.get(InterviewSession, session_id)
        
        if not session:
            return jsonify({"error": "Invalid or expired session"}), 404

        # Compare user_ids
        if session.user_id != int(user_id):
            return jsonify({"error": "Unauthorized access to session"}), 403

        questions = session.questions
        responses = session.responses
        cv_id = session.cv_id

        if len(responses) != len(questions):
            return jsonify({"error": "Not all questions have been answered"}), 400

        # Generate feedback (Returns structured dict)
        ai_analysis = generate_personalized_feedback(responses, questions)

        # Handle potential error in AI response
        if "questions_analysis" not in ai_analysis:
            # Fallback if AI failed to return valid JSON
            questions_analysis = []
            overall_feedback = ai_analysis.get("overall_feedback", "Feedback generation unavailable.")
        else:
            questions_analysis = ai_analysis["questions_analysis"]
            overall_feedback = ai_analysis["overall_feedback"]

        # Calculate metrics based on AI scores
        total_score = sum(q.get("score", 0) for q in questions_analysis)
        accuracy_level = f"{(total_score / len(questions)) * 100:.2f}%"
        confidence_level = "High" if total_score > (len(questions) * 0.7) else "Moderate"

        # Update Session with results
        # Store the FULL JSON analysis in the feedback column for retrieval
        session.feedback = json.dumps(ai_analysis)
        session.status = 'completed'
        session.completed_at = datetime.utcnow()
        
        # Create performance report
        new_report = PerformanceReport(
            accuracy_level=accuracy_level,
            confidence_level=confidence_level,
            total_questions=len(questions),
            correct_answers=int(total_score), # Approximate integer score
            feedback=json.dumps(ai_analysis), # Store full JSON
            cv_id=cv_id
        )
        db.session.add(new_report)
        
        # REMOVED: db.session.delete(session) - We keep it for history!
        
        db.session.commit()

        # Prepare report data using the rich analysis
        # Merge questions info with AI analysis if needed, but AI analysis has it.
        # However, to be safe, we map by index or trust AI order.
        # AI prompt iterates indices, so order maintains.
        
        detailed_responses = questions_analysis if questions_analysis else \
            [{"question": q, "answer": r, "status": "Unknown", "score": 0, "feedback": "No detailed analysis."} for q, r in zip(questions, responses)]
        
        report_data = {
            "total_questions": len(questions),
            "answers_received": len(responses),
            "accuracy_level": accuracy_level,
            "confidence_level": confidence_level,
            "detailed_responses": detailed_responses,
            "feedback": overall_feedback
        }

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
        user = db.session.get(User, int(user_id))
        
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
@app.route('/api/profile/reports', methods=['GET'])
@jwt_required()
def get_past_reports():
    try:
        user_id = get_jwt_identity()
        # Fetch completed sessions (reports)
        # Ordered by completed_at desc
        sessions = InterviewSession.query.filter_by(
            user_id=int(user_id), 
            status='completed'
        ).order_by(InterviewSession.completed_at.desc()).all()
        
        reports_list = []
        for s in sessions:
            cv = CV.query.get(s.cv_id)
            # Calculate actual score from AI analysis if available
            score_display = f"{len(s.responses)}/{len(s.questions)}" # Default
            try:
                if s.feedback and (s.feedback.startswith('{') or s.feedback.startswith('[')):
                    analysis = json.loads(s.feedback)
                    if isinstance(analysis, dict) and "questions_analysis" in analysis:
                        total_score = sum(q.get("score", 0) for q in analysis["questions_analysis"])
                        # Format score to 2 decimal places if float, or int if whole number
                        formatted_score = f"{total_score:.2f}".rstrip('0').rstrip('.')
                        score_display = f"{formatted_score}/{len(s.questions)}"
            except Exception:
                pass # Fallback to count

            reports_list.append({
                'session_id': s.id,
                'cv_company': cv.company_name if cv else "Unknown",
                'cv_role': cv.job_role if cv else "Unknown",
                'interview_level': cv.interview_level if cv else "",
                'completed_at': s.completed_at.strftime('%Y-%m-%d %H:%M') if s.completed_at else "",
                'score': score_display
            })
            
        return jsonify(reports_list), 200
    except Exception as e:
        logging.error(f"Get reports error: {e}")
        return jsonify({"error": "Failed to load reports"}), 500

@app.route('/api/report/<session_id>', methods=['GET'])
@jwt_required()
def get_report_detail(session_id):
    try:
        user_id = get_jwt_identity()
        session = db.session.get(InterviewSession, session_id)
        
        if not session:
            return jsonify({"error": "Report not found"}), 404
            
        if session.user_id != int(user_id):
            return jsonify({"error": "Unauthorized"}), 403
            
        if session.status != 'completed':
            return jsonify({"error": "Interview not completed yet"}), 400

        # Reconstruct report structure
        questions = session.questions
        responses = session.responses
        
        # Parse feedback
        feedback_raw = session.feedback
        overall_feedback = ""
        questions_analysis = []
        
        try:
            if feedback_raw and (feedback_raw.startswith('{') or feedback_raw.startswith('[')):
                 ai_analysis = json.loads(feedback_raw)
                 if isinstance(ai_analysis, dict):
                    overall_feedback = ai_analysis.get("overall_feedback", "")
                    questions_analysis = ai_analysis.get("questions_analysis", [])
                 else:
                     overall_feedback = str(feedback_raw) # Fallback
            else:
                 overall_feedback = feedback_raw or "No feedback available."
        except Exception as e:
            logging.warning(f"Failed to parse feedback JSON: {e}")
            overall_feedback = feedback_raw

        # If we have structured analysis, use it. Otherwise fallback to simple pairing
        if questions_analysis:
             detailed_responses = questions_analysis
             # Recalculate score from analysis data for consistency
             total_score = sum(q.get("score", 0) for q in questions_analysis)
             accuracy_level = f"{(total_score / len(questions)) * 100:.2f}%"
             confidence_level = "High" if total_score > (len(questions) * 0.7) else "Moderate"
        else:
             detailed_responses = [{"question": q, "answer": r, "status": "Unknown", "score": 0, "feedback": "Detailed analysis unavailable for this old session."} for q, r in zip(questions, responses)]
             accuracy_level = f"{min(100, (len(responses) / len(questions)) * 100):.2f}%"
             confidence_level = "High" if len(responses) == len(questions) else "Moderate"

        report_data = {
            "total_questions": len(questions),
            "answers_received": len(responses),
            "accuracy_level": accuracy_level,
            "confidence_level": confidence_level,
            "detailed_responses": detailed_responses,
            "feedback": overall_feedback
        }
        
        return jsonify({"report": report_data}), 200
    except Exception as e:
        logging.error(f"Get report detail error: {e}")
        return jsonify({"error": "Failed to load report"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

