# JWT 422 Error Fix

## Problem
Getting 422 (UNPROCESSABLE ENTITY) errors when trying to access protected endpoints like `/api/profile` and `/api/upload-cv`.

## Root Cause
1. **Multipart/form-data header issue**: When uploading files, we were manually setting `Content-Type: multipart/form-data`, but browsers need to set this automatically with the boundary parameter.
2. **Missing JWT error handlers**: Flask-JWT-Extended returns 422 for invalid tokens, but we didn't have proper error handlers.

## Fixes Applied

### 1. Frontend API Service (`frontend/src/services/api.js`)
- Fixed Content-Type header handling - only set for JSON, not for FormData
- Let browser automatically set Content-Type for file uploads
- Improved error handling for 422 (JWT errors)

### 2. Frontend Interview Service (`frontend/src/services/interviewService.js`)
- Removed manual Content-Type header for file uploads
- Let axios/browser handle it automatically

### 3. Backend (`backend/app.py`)
- Added JWT error handlers for better error messages:
  - `expired_token_loader` - 401 for expired tokens
  - `invalid_token_loader` - 422 for invalid tokens
  - `unauthorized_loader` - 401 for missing tokens

## Testing

1. **Clear browser localStorage** (to remove any bad tokens):
   ```javascript
   localStorage.clear()
   ```

2. **Login again** to get a fresh token

3. **Try uploading CV** - should work now

## If Still Getting 422:

1. Check browser console for the actual error message
2. Verify token is stored: `localStorage.getItem('token')`
3. Check network tab - see if Authorization header is being sent
4. Make sure you're logged in and have a valid token

## Common Issues:

- **Token not stored**: Login might have failed silently - check login response
- **Token expired**: Even though we set it to not expire, check your JWT_SECRET is set correctly
- **CORS issues**: Make sure CORS_ORIGINS includes your frontend URL

