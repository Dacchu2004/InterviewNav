# Debug JWT Token Issue

## Steps to Debug

### 1. Check Backend Logs
After restarting the server and trying to login, look at the backend terminal. You should now see detailed error messages like:
```
JWT invalid token error: <actual error message>
```

### 2. Check Browser Console
Open browser DevTools (F12) → Console tab. Look for any errors when trying to access protected routes.

### 3. Check Network Tab
Open DevTools → Network tab:
- Filter by "profile" or "upload-cv"
- Click on the request
- Check the **Request Headers** section
- Look for: `Authorization: Bearer <token>`
- Verify the token is being sent

### 4. Check LocalStorage
In browser console, run:
```javascript
localStorage.getItem('token')
```
This should show a long JWT token string (starts with `eyJ...`)

### 5. Test Token with Debug Endpoint
After logging in, try accessing:
```
http://localhost:5000/api/debug/token
```
This will tell us if the token itself is valid.

---

## Common Issues:

1. **Token not in localStorage**: Login might not be saving the token
2. **Token format wrong**: Should start with `eyJ`
3. **Authorization header missing**: Check Network tab
4. **Token from old secret**: Make sure you logged in AFTER changing JWT_SECRET

---

**Please check the backend terminal logs after trying to login - it should show the actual JWT error message now.**

