# Virtual Interview Navigator - Setup & Migration Guide

## Step-by-Step Setup Instructions

### Step 1: Create PostgreSQL Database

1. **Open PostgreSQL Command Line or pgAdmin**

2. **Connect to PostgreSQL** (default user is usually `postgres`)

3. **Create the Database:**
   ```sql
   CREATE DATABASE "InterviewNavigator";
   ```
   
   Note: Use quotes because the name has capital letters. The database name is exactly: `InterviewNavigator`

4. **Verify the database was created:**
   ```sql
   \l
   ```
   You should see `InterviewNavigator` in the list.

5. **Your DATABASE_URL format:**
   ```
   postgresql://postgres:YOUR_PASSWORD@localhost:5432/InterviewNavigator?schema=public
   ```
   Replace `YOUR_PASSWORD` with your actual PostgreSQL password.

---

### Step 2: Environment Variables Setup

Create a `.env` file in the **backend** folder with:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/InterviewNavigator?schema=public
JWT_SECRET=c1d57fddf74067fbe1897f9c79e6662d8376d76206fb11b6681bf50d854cc*****************************************************************************
OPENAI_API_KEY=sk-proj-UBtvWvNej2wy7*******************************************************************************************************__OR-Et3L0TXCpiWqcVDoN2***********************WqaB6zVtj2I1IA
SECRET_KEY=your-flask-secret-key-here
FLASK_ENV=development
```

**Important:** Replace the asterisks (*) with your actual JWT_SECRET and OPENAI_API_KEY values.

---

### Step 3: Project Structure

The project will be restructured as:

```
InterviewPrac/
├── backend/                    # Flask API
│   ├── app.py
│   ├── config.py
│   ├── model.py
│   ├── forms.py
│   ├── extensions.py
│   ├── requirements.txt
│   ├── .env                    # Environment variables
│   ├── migrations/
│   └── uploads/
│
├── frontend/                   # React App
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── utils/
│   │   └── App.jsx
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js         # Using Vite for React
│
└── README.md
```

---

### Step 4: What You Need to Do

1. ✅ **Create the PostgreSQL database** (Step 1 above)

2. ✅ **Create .env file** in backend folder with your credentials (Step 2)

3. ✅ **Install PostgreSQL** (if not already installed)

4. ✅ **Install Node.js and npm** (for React frontend)

5. ⏳ **Wait for me to complete the code migration**

---

### Step 5: After Code Migration - Installation

#### Backend Setup:
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
flask db upgrade
python app.py
```

#### Frontend Setup:
```bash
cd frontend
npm install
npm run dev
```

---

### Step 6: Deployment Setup (After Local Testing)

#### Backend (Render):
- Connect GitHub repo
- Set build command: `pip install -r requirements.txt`
- Set start command: `gunicorn app:app`
- Add environment variables in Render dashboard

#### Database (Neon):
- Create project on Neon.tech
- Get connection string
- Update DATABASE_URL in Render environment variables

#### Frontend (Vercel):
- Connect GitHub repo
- Set root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`
- Add environment variables (API URL)

---

## Key Changes in This Migration

1. ✅ **Frontend**: HTML/JS → React with Tailwind CSS
2. ✅ **Authentication**: Flask-Login → JWT tokens (better for API)
3. ✅ **Backend**: Returns JSON instead of HTML templates
4. ✅ **CORS**: Enabled for React frontend to communicate with Flask
5. ✅ **CV Bug Fixed**: CV text now included in OpenAI prompt
6. ✅ **Model Updated**: GPT-3.5-turbo → GPT-4o-mini
7. ✅ **Structure**: Separated for easy deployment

---

## ✅ Migration Complete!

The code migration is now complete! Here's what was done:

### Changes Made:

1. ✅ **Backend Converted to REST API**
   - All routes now return JSON
   - JWT authentication implemented
   - CORS enabled for React frontend

2. ✅ **CV Bug Fixed**
   - CV text now properly included in OpenAI prompt
   - Questions are truly personalized based on CV content

3. ✅ **OpenAI Model Updated**
   - Changed from gpt-3.5-turbo to gpt-4o-mini
   - Updated to use new OpenAI SDK format

4. ✅ **Feedback Saved to Database**
   - Feedback now properly stored in PerformanceReport model

5. ✅ **React Frontend Created**
   - All pages converted to React components
   - Tailwind CSS integrated
   - Speech recognition using Web Speech API

6. ✅ **Deployment Ready**
   - Backend configured for Render
   - Frontend configured for Vercel
   - Database ready for Neon

### Next Steps:

1. ✅ **Complete database setup** (Step 1 above)

2. **Create .env files:**
   - Backend: Copy `.env.example` to `.env` and fill in your values
   - Frontend: Create `.env` with `VITE_API_URL=http://localhost:5000`

3. **Test locally:**
   ```bash
   # Terminal 1 - Backend
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   flask db upgrade
   python app.py

   # Terminal 2 - Frontend
   cd frontend
   npm install
   npm run dev
   ```

4. **Deploy:**
   - Deploy database to Neon.tech
   - Deploy backend to Render
   - Deploy frontend to Vercel
   - Update environment variables in each platform

---

**All code is ready! Start with database creation and then follow the setup steps.**
