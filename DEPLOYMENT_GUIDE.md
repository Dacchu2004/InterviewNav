# Deployment Guide - Virtual Interview Navigator

## Prerequisites

- GitHub account with code pushed
- Render account (for backend)
- Vercel account (for frontend)
- Neon account (for database)

---

## Step 1: Deploy Database (Neon)

1. Go to [Neon.tech](https://neon.tech) and sign up/login

2. Create a new project
   - Choose a project name
   - Select region closest to your users
   - PostgreSQL version: 15 or 16

3. Copy the connection string
   - It will look like: `postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require`

4. Update the connection string format:
   - Replace database name with: `InterviewNavigator`
   - Full format: `postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/InterviewNavigator?sslmode=require`

5. Save this connection string - you'll use it in Render

---

## Step 2: Deploy Backend (Render)

1. Go to [Render.com](https://render.com) and sign up/login

2. Create a new Web Service
   - Connect your GitHub repository
   - Select the repository

3. Configure the service:
   - **Name**: `interview-navigator-api` (or any name)
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your main branch)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

4. Add Environment Variables:
   ```
   DATABASE_URL=<your-neon-connection-string>
   JWT_SECRET=<your-jwt-secret>
   OPENAI_API_KEY=<your-openai-api-key>
   SECRET_KEY=<your-flask-secret-key>
   FLASK_ENV=production
   CORS_ORIGINS=https://your-frontend-url.vercel.app,http://localhost:5173
   ```

5. Deploy
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note the service URL (e.g., `https://interview-navigator-api.onrender.com`)

6. Run database migrations:
   - Go to Render dashboard → Your service → Shell
   - Run:
     ```bash
     flask db upgrade
     ```

---

## Step 3: Deploy Frontend (Vercel)

1. Go to [Vercel.com](https://vercel.com) and sign up/login

2. Import Project
   - Click "Add New" → "Project"
   - Import from GitHub
   - Select your repository

3. Configure the project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

4. Add Environment Variable:
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```
   (Use your Render backend URL)

5. Deploy
   - Click "Deploy"
   - Wait for deployment to complete
   - Note your frontend URL (e.g., `https://interview-navigator.vercel.app`)

---

## Step 4: Update Backend CORS

1. Go back to Render dashboard
2. Update the `CORS_ORIGINS` environment variable:
   ```
   CORS_ORIGINS=https://your-frontend-url.vercel.app
   ```
3. Redeploy the service (Render will auto-redeploy when env vars change)

---

## Step 5: Final Configuration

### Backend Environment Variables (Render):
```
DATABASE_URL=<neon-connection-string>
JWT_SECRET=<your-secret>
OPENAI_API_KEY=<your-key>
SECRET_KEY=<your-secret>
FLASK_ENV=production
CORS_ORIGINS=https://your-frontend.vercel.app
```

### Frontend Environment Variable (Vercel):
```
VITE_API_URL=https://your-backend.onrender.com
```

---

## Step 6: Test Your Deployment

1. Visit your Vercel frontend URL
2. Try registering a new account
3. Upload a CV and test the interview flow
4. Verify all features work correctly

---

## Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL is correct
- Check if database name is `InterviewNavigator` (case-sensitive)
- Ensure SSL mode is set: `?sslmode=require`

### CORS Errors
- Verify CORS_ORIGINS includes your Vercel URL
- Make sure URL is exact (no trailing slash)
- Redeploy backend after changing CORS settings

### API Not Working
- Check backend logs in Render dashboard
- Verify environment variables are set correctly
- Test API endpoints directly with Postman/curl

### Frontend Build Errors
- Check Vercel build logs
- Ensure VITE_API_URL is set correctly
- Verify all dependencies are in package.json

---

## Monitoring

- **Render**: Monitor backend logs in dashboard
- **Vercel**: Monitor frontend analytics and logs
- **Neon**: Monitor database usage and connections

---

## Security Notes

- Never commit `.env` files to GitHub
- Use strong secrets for JWT_SECRET and SECRET_KEY
- Keep your OpenAI API key secure
- Enable HTTPS (automatically enabled by Render/Vercel)
- Regularly update dependencies

---

Your application should now be live! 🚀

