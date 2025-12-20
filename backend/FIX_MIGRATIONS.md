# Fix Database Migrations

## Problem

The old migration files are trying to ALTER existing tables, but this is a fresh database with no tables yet.

## Solution

We need to create fresh migrations for the new database. Follow these steps:

### Step 1: Delete old migration version files
Already done - old migration files have been removed.

### Step 2: Initialize fresh migrations

Run these commands in the backend directory:

```powershell
# Make sure you're in backend directory and venv is activated
flask db stamp head
flask db revision --autogenerate -m "Initial migration"
flask db upgrade
```

If that doesn't work, try:

```powershell
# Delete alembic_version table if it exists (optional, only if needed)
# Then:
flask db init  # Only if migrations folder needs reinitialization
flask db migrate -m "Initial migration"
flask db upgrade
```

### Alternative: Use db.create_all() for fresh database

If migrations are still problematic, you can create tables directly:

```python
# In Python shell or create init_db.py
from app import app, db
from model import User, CV, PerformanceReport

with app.app_context():
    db.create_all()
    print("Tables created successfully!")
```

Then mark migrations as current:
```powershell
flask db stamp head
```

