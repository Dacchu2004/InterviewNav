# JWT Fix - "Subject must be a string" Error

## The Problem
Error: `Invalid token: Subject must be a string`

Flask-JWT-Extended's `create_access_token()` requires the `identity` parameter to be a **string**, but we were passing an integer (`user.id`).

## The Fix

### 1. Token Creation (Login/Register)
Changed from:
```python
access_token = create_access_token(identity=user.id)  # ❌ Wrong - integer
```

To:
```python
access_token = create_access_token(identity=str(user.id))  # ✅ Correct - string
```

### 2. Token Retrieval (All protected routes)
Changed from:
```python
user_id = get_jwt_identity()  # Returns string
user = User.query.get(user_id)  # ❌ Wrong - DB expects int
```

To:
```python
user_id = get_jwt_identity()  # Returns string
user = User.query.get(int(user_id))  # ✅ Correct - convert to int
```

## Files Changed
- `backend/app.py`:
  - `register()` - Fixed token creation
  - `login()` - Fixed token creation  
  - `get_profile()` - Fixed user_id conversion
  - `upload_cv()` - Fixed user_id conversion
  - `get_reports()` - Fixed user_id conversion
  - All session comparisons - Handle string comparison

## Testing

1. **Restart backend server**
2. **Clear browser localStorage**: 
   ```javascript
   localStorage.clear()
   ```
3. **Login again** - Should work now!
4. **Try accessing protected routes** - Should work!

---

**The issue is now fixed! Restart your server and login again.** ✅

