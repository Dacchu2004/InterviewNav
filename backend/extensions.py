from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Initialize database and JWT manager
db = SQLAlchemy()
jwt = JWTManager()

