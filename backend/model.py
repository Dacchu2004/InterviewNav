from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Relationship with CV model: Each user can have multiple CVs
    cvs = db.relationship('CV', backref='owner', lazy=True, cascade='all, delete-orphan')

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
    interview_level = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship with PerformanceReport model: One CV can have many performance reports
    performance_reports = db.relationship('PerformanceReport', backref='cv', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<CV {self.company_name} - {self.job_role}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'job_role': self.job_role,
            'interview_level': self.interview_level,
            'user_id': self.user_id
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

