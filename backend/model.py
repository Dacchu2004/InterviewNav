from extensions import db
from datetime import datetime
import json

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Relationship with CV model: Each user can have multiple CVs
    cvs = db.relationship('CV', backref='owner', lazy=True, cascade='all, delete-orphan')
    # Relationship with InterviewSession
    sessions = db.relationship('InterviewSession', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active
        }

class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    job_role = db.Column(db.String(255), nullable=False)
    job_description = db.Column(db.Text, nullable=True) # Optional Job Description
    interview_level = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship with PerformanceReport model: One CV can have many performance reports
    performance_reports = db.relationship('PerformanceReport', backref='cv', lazy=True, cascade='all, delete-orphan')
    # Relationship with InterviewSession
    sessions = db.relationship('InterviewSession', backref='cv', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<CV {self.company_name} - {self.job_role}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'job_role': self.job_role,
            'job_description': self.job_description,
            'interview_level': self.interview_level,
            'user_id': self.user_id
        }

class InterviewSession(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # UUID string
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cv_id = db.Column(db.Integer, db.ForeignKey('cv.id'), nullable=False)
    questions_json = db.Column(db.Text, nullable=False) # Stored as JSON string
    responses_json = db.Column(db.Text, default='[]')   # Stored as JSON string
    feedback = db.Column(db.Text, nullable=True)        # AI Feedback
    status = db.Column(db.String(20), default='active') # active, completed
    current_question_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Helper to get/set questions as list
    @property
    def questions(self):
        return json.loads(self.questions_json)
    
    @questions.setter
    def questions(self, value):
        self.questions_json = json.dumps(value)

    # Helper to get/set responses as list
    @property
    def responses(self):
        return json.loads(self.responses_json)
    
    @responses.setter
    def responses(self, value):
        self.responses_json = json.dumps(value)

    def to_dict(self):
        return {
            'session_id': self.id,
            'user_id': self.user_id,
            'cv_id': self.cv_id,
            'current_question': self.current_question_index,
            'total_questions': len(self.questions),
            'completed': self.current_question_index >= len(self.questions) or self.status == 'completed',
            'status': self.status,
            'feedback': self.feedback,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class PerformanceReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accuracy_level = db.Column(db.String(50), nullable=False)
    confidence_level = db.Column(db.String(50), nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text, nullable=True)
    cv_id = db.Column(db.Integer, db.ForeignKey('cv.id'), nullable=False)

    def __repr__(self):
        return f'<PerformanceReport {self.accuracy_level} - {self.confidence_level}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'accuracy_level': self.accuracy_level,
            'confidence_level': self.confidence_level,
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers,
            'feedback': self.feedback,
            'cv_id': self.cv_id
        }
