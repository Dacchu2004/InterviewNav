# Database Setup Fix

## The Problem

The old migration files are trying to ALTER existing tables, but this is a fresh database with no tables. This causes the error:
```
relation "cv" does not exist
```

## Solution: Create Tables Directly

Since this is a fresh database, we'll create tables directly and then fix migrations.

### Step 1: Create Tables Using init_db.py

In your **activated virtual environment** (make sure you're in the backend directory with venv activated):

```powershell
# Make sure venv is activated first!
python init_db.py
```

This will create all the tables directly from your models.

### Step 2: Mark Migrations as Current

After tables are created, tell Flask-Migrate that the database is up to date:

```powershell
flask db stamp head
```

### Step 3: Verify

You should now be able to run the Flask app:

```powershell
python app.py
```

---

## Alternative: Fresh Migration (If Step 1 doesn't work)

If you prefer to use migrations properly:

1. **Delete old migration versions** (already done)
2. **Create fresh migration:**
   ```powershell
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

---

## Quick Check

After running `init_db.py`, verify tables exist in PostgreSQL:

```sql
\dt
```

You should see: `user`, `cv`, `performance_report`

