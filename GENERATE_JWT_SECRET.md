# Generate JWT Secret - Quick Command

## Option 1: Python (Recommended)
```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

This generates a secure, URL-safe random token (86 characters).

## Option 2: PowerShell (No Python needed)
```powershell
$bytes = New-Object byte[] 64; [System.Security.Cryptography.RandomNumberGenerator]::Fill($bytes); [Convert]::ToBase64String($bytes) -replace '[/+=]', ''
```

## Option 3: Shorter token (32 bytes = 43 chars)
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

**Steps:**
1. Run one of the commands above
2. Copy the generated token
3. Paste it in `backend/.env` file:
   ```
   JWT_SECRET=<paste-your-generated-token-here>
   ```
4. Restart the backend server
5. Logout and login again to get a new token with the new secret

