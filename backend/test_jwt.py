"""
Quick test script to verify JWT_SECRET_KEY is being read correctly
Run this: python test_jwt.py
"""
from app import app

with app.app_context():
    print("JWT_SECRET_KEY from config:", app.config.get('JWT_SECRET_KEY'))
    print("SECRET_KEY from config:", app.config.get('SECRET_KEY'))
    print("\nIf JWT_SECRET_KEY shows the default value, your .env file isn't being loaded correctly!")

