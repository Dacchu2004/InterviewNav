"""
Script to initialize the database with tables.
Use this if migrations are causing issues with a fresh database.
"""
from app import app, db
from model import User, CV, PerformanceReport

def init_database():
    """Create all database tables"""
    with app.app_context():
        # Drop all tables (use with caution - only for fresh database!)
        # db.drop_all()
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        print("📊 Tables created: user, cv, performance_report")

if __name__ == '__main__':
    init_database()

