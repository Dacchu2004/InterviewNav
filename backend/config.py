import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET', 'your_jwt_secret_key')
    # Note: Remove ?schema=public from DATABASE_URL - it's not a valid PostgreSQL connection parameter
    # PostgreSQL defaults to 'public' schema automatically
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/InterviewNavigator')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}
    JWT_ACCESS_TOKEN_EXPIRES = False  # Tokens don't expire (or set to timedelta(hours=24))
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')

