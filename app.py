import os
import openai
import PyPDF2
import speech_recognition as sr
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from forms import CVUploadForm, RegistrationForm, LoginForm
from dotenv import load_dotenv
from extensions import db, login_manager
from model import User, CV, PerformanceReport
from docx import Document
from flask_migrate import Migrate
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/interview_navigator')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db)

# OpenAI API Key setup
openai.api_key = os.getenv("OPENAI_API_KEY", "").strip()
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already exists. Try logging in.', 'danger')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/upload_cv', methods=['GET', 'POST'])
@login_required
def upload_cv():
    form = CVUploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        file = form.cv_file.data
        company_name = form.company_name.data
        job_role = form.job_role.data
        interview_level = form.interview_level.data

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Extract text and generate questions
            cv_text = extract_text_from_cv(file_path)
            if not cv_text.strip():
                flash("Could not extract text from CV. Please upload a valid file.", "danger")
                return redirect(url_for('upload_cv'))

            questions = generate_interview_questions(cv_text, company_name, job_role, interview_level)
            if questions.startswith("Unable"):
                flash("Failed to generate interview questions. Please try again later.", 'danger')
                return redirect(url_for('upload_cv'))

            # Save CV info to the database
            new_cv = CV(
                file_path=file_path,
                company_name=company_name,
                job_role=job_role,
                interview_level=interview_level,
                user_id=current_user.id
            )
            db.session.add(new_cv)
            db.session.commit()

            session['questions'] = questions.split("\n")
            session['current_question'] = 0
            session['responses'] = []

            flash('CV uploaded successfully. Interview session ready.', 'success')
            return redirect(url_for('interview'))
        else:
            flash('Invalid file type. Please upload a PDF or DOCX file.', 'danger')
    return render_template('upload_cv.html', form=form)

@app.route('/interview', methods=['GET', 'POST'])
@login_required
def interview():
    if 'questions' not in session:
        flash('No interview session found. Please upload your CV first.', 'danger')
        return redirect(url_for('upload_cv'))

    questions = session['questions']
    current_question_index = session.get('current_question', 0)

    if current_question_index >= len(questions):
        flash('Interview completed! Generating your performance report.', 'success')
        return redirect(url_for('report'))

    current_question = questions[current_question_index]

    if request.method == 'POST':
        response = request.form.get('transcribed_response')  # Get transcribed response
        if response:
            session['responses'].append(response)
            session['current_question'] += 1
        else:
            flash("Please provide an answer before clicking Done.", 'danger')
        return redirect(url_for('interview'))

    return render_template(
        'interview.html', 
        question=current_question, 
        progress=current_question_index + 1, 
        total=len(questions)
    )

@app.route('/report')
@login_required
def report():
    questions = session.get('questions', [])
    responses = session.get('responses', [])

    report = {
        "total_questions": len(questions),
        "answers_received": len(responses),
        "accuracy_level": f"{min(100, (len(responses) / len(questions)) * 100):.2f}%",
        "confidence_level": "High" if len(responses) == len(questions) else "Moderate",
        "detailed_responses": list(zip(questions, responses))
    }

    feedback = generate_personalized_feedback(responses)

    # Retrieve the CV object associated with the current user
    cv = CV.query.filter_by(user_id=current_user.id).order_by(CV.id.desc()).first()

    # If a CV exists for the user, create a performance report for that CV
    if cv:
        new_report = PerformanceReport(
            accuracy_level=report["accuracy_level"],
            confidence_level=report["confidence_level"],
            total_questions=report["total_questions"],
            correct_answers=report["answers_received"],
            cv_id=cv.id
        )
        db.session.add(new_report)
        db.session.commit()

    return render_template('report.html', report=report, feedback=feedback)

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
    base_prompt = (
        f"Based on the CV text, generate a list of 6 to 10 interview questions for a {job_role} position at {company_name}. "
        f"Focus on skills, experience, and industry knowledge."
    )

    if interview_level == 'Beginner':
        level_prompt = "The questions should focus on basic knowledge, entry-level skills, and general understanding of the field."
    elif interview_level == 'Intermediate':
        level_prompt = "The questions should focus on practical experience, challenges faced in the role, and problem-solving skills."
    elif interview_level == 'Advanced':
        level_prompt = "The questions should focus on advanced technical knowledge, leadership skills, and strategic thinking."
    else:
        level_prompt = "Please provide a balanced set of questions."

    prompt = f"{base_prompt} {level_prompt}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.OpenAIError as e:
        logging.error(f"Error generating interview questions: {e}")
        return "Unable to generate interview questions at this time. Please try again later."

def generate_personalized_feedback(responses):
    try:
        feedback_prompt = "Based on the following responses to interview questions, provide personalized and detailed feedback for improvement. Analyze the responses and give detailed suggestions on how the user can improve their interview skills, including communication skills, confidence, areas where they went wrong, and general advice for success.\n\n"
        for idx, response in enumerate(responses):
            feedback_prompt += f"Question {idx + 1}: {response}\n"

        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": feedback_prompt}],
            max_tokens=500
        )
        feedback = openai_response['choices'][0]['message']['content'].strip()
        return feedback

    except openai.OpenAIError as e:
        logging.error(f"Error generating feedback: {e}")
        return "Unable to generate personalized feedback at this time. Please try again later."

if __name__ == '__main__':
    app.run(debug=True)
