from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize database and login manager
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
