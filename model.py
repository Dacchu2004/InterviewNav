from flask_login import UserMixin
from extensions import db  # Import the db extension from your extensions.py file

# Updated User model
class User(UserMixin, db.Model):  # Add UserMixin here
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)  # Ensure 255 length
    is_active = db.Column(db.Boolean, default=True)

    # Relationship with CV model: Each user can have multiple CVs
    cvs = db.relationship('CV', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    job_role = db.Column(db.String(255), nullable=False)
    interview_level = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User model

    # Relationship with PerformanceReport model: One CV can have many performance reports
    performance_reports = db.relationship('PerformanceReport', backref='cv', lazy=True)

    def __repr__(self):
        return f'<CV {self.company_name} - {self.job_role}>'

class PerformanceReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accuracy_level = db.Column(db.String(50), nullable=False)
    confidence_level = db.Column(db.String(50), nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text, nullable=True)  # New field to store personalized feedback
    cv_id = db.Column(db.Integer, db.ForeignKey('cv.id'), nullable=False)  # Foreign key to CV model

    def __repr__(self):
        return f'<PerformanceReport {self.accuracy_level} - {self.confidence_level}>'
