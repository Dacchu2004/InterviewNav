# Database Connection Fix

## The Problem

You're getting this error:
```
psycopg2.ProgrammingError: invalid dsn: invalid connection option "schema"
```

## The Solution

Remove `?schema=public` from your DATABASE_URL in the `.env` file.

### ❌ Wrong (causes error):
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/InterviewNavigator?schema=public
```

### ✅ Correct:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/InterviewNavigator
```

## Why?

PostgreSQL connection strings don't support a `schema` parameter. The `public` schema is the default schema in PostgreSQL, so you don't need to specify it in the connection string.

If you need to use a different schema, you can set it in your SQL queries or SQLAlchemy models, but not in the connection string.

## Steps to Fix

1. Open `backend/.env` file
2. Find the line with `DATABASE_URL`
3. Remove `?schema=public` from the end
4. Save the file
5. Try `flask db upgrade` again

---

**After fixing, your DATABASE_URL should look like:**
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/InterviewNavigator
```

