# Quick Start Guide

## ✅ What Was Done

1. **Project Restructured**
   - Separated into `backend/` (Flask) and `frontend/` (React)
   - All HTML/JS converted to React with Tailwind CSS
   - Backend converted to REST API with JWT authentication

2. **Bugs Fixed**
   - ✅ CV text now included in OpenAI prompt (questions are personalized)
   - ✅ Feedback saved to database
   - ✅ OpenAI model updated to GPT-4o-mini

3. **Key Features**
   - JWT authentication
   - CORS enabled for frontend-backend communication
   - Voice input using Web Speech API
   - AI-powered question generation and feedback

---

## 🚀 Quick Setup (Local Development)

### 1. Database Setup
```sql
-- In PostgreSQL:
CREATE DATABASE "InterviewNavigator";
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt

# Create .env file with your credentials
# See backend/.env.example for format

flask db upgrade
python app.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install

# Create .env file:
# VITE_API_URL=http://localhost:5000

npm run dev
```

---

## 📝 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/InterviewNavigator?schema=public
JWT_SECRET=your-jwt-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here
SECRET_KEY=your-flask-secret-key-here
CORS_ORIGINS=http://localhost:5173
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:5000
```

---

## 🔑 Important Notes

1. **Database Name**: Must be exactly `InterviewNavigator` (case-sensitive, with quotes in SQL)

2. **JWT_SECRET & OPENAI_API_KEY**: Use the full values you provided (with all the asterisks replaced)

3. **Speech Recognition**: Requires Chrome/Edge browser (Web Speech API support)

4. **CV Files**: Must be PDF or DOCX format

---

## 📚 Documentation

- **SETUP_GUIDE.md** - Detailed setup instructions
- **DEPLOYMENT_GUIDE.md** - Deployment to Render, Vercel, Neon
- **README.md** - Full project documentation

---

## 🐛 Troubleshooting

**Database connection fails?**
- Check database name is exactly `InterviewNavigator`
- Verify PostgreSQL is running
- Check username/password in DATABASE_URL

**CORS errors?**
- Ensure backend CORS_ORIGINS includes frontend URL
- Check frontend VITE_API_URL matches backend

**OpenAI errors?**
- Verify API key is correct
- Check API key has credits/quota

---

## ✨ Next Steps

1. ✅ Create database (see above)
2. ✅ Set up .env files
3. ✅ Run backend and frontend locally
4. ✅ Test the application
5. ✅ Deploy (see DEPLOYMENT_GUIDE.md)

---

**Need help? Check the detailed guides or review the code comments!**

