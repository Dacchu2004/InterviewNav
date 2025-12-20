# Virtual Interview Navigator

AI-powered virtual interviewer system that generates personalized interview questions based on your CV and provides real-time feedback.

## Tech Stack

### Backend
- **Python Flask** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Flask-JWT-Extended** - JWT authentication
- **OpenAI GPT-4o-mini** - AI question generation and feedback
- **PyPDF2 & python-docx** - CV text extraction

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Web Speech API** - Voice recognition

## Project Structure

```
InterviewPrac/
├── backend/           # Flask API
│   ├── app.py
│   ├── model.py
│   ├── config.py
│   ├── extensions.py
│   ├── requirements.txt
│   ├── migrations/
│   └── uploads/
│
└── frontend/          # React App
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   └── utils/
    ├── package.json
    └── vite.config.js
```

## Setup Instructions

### Prerequisites
1. Python 3.11+
2. Node.js 18+
3. PostgreSQL installed and running

### Step 1: Database Setup

1. Open PostgreSQL command line or pgAdmin
2. Connect to PostgreSQL
3. Create the database:
   ```sql
   CREATE DATABASE "InterviewNavigator";
   ```
4. Note: Database name must be exactly `InterviewNavigator` (case-sensitive)

### Step 2: Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create `.env` file in backend directory:
   ```env
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/InterviewNavigator?schema=public
   JWT_SECRET=your-jwt-secret-key
   OPENAI_API_KEY=your-openai-api-key
   SECRET_KEY=your-flask-secret-key
   CORS_ORIGINS=http://localhost:5173,http://localhost:3000
   ```

6. Run database migrations:
   ```bash
   flask db upgrade
   ```

7. Start the backend server:
   ```bash
   python app.py
   ```

   Backend runs on `http://localhost:5000`

### Step 3: Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env` file in frontend directory:
   ```env
   VITE_API_URL=http://localhost:5000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

   Frontend runs on `http://localhost:5173`

## Key Features

✅ **CV-Based Question Generation** - Questions are personalized based on your CV content  
✅ **Voice Input** - Answer questions using speech recognition  
✅ **Real-time Feedback** - Get AI-powered feedback on your responses  
✅ **Performance Tracking** - View your interview performance reports  
✅ **Multi-level Interviews** - Beginner, Intermediate, and Advanced levels  

## API Endpoints

- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/profile` - Get user profile
- `POST /api/upload-cv` - Upload CV and generate questions
- `GET /api/interview/question` - Get current interview question
- `POST /api/interview/answer` - Submit answer
- `POST /api/report/generate` - Generate performance report
- `GET /api/reports` - Get all reports

## Deployment

### Backend (Render)
1. Connect GitHub repository
2. Set root directory: `backend`
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add environment variables in Render dashboard

### Database (Neon)
1. Create project on Neon.tech
2. Get connection string
3. Update `DATABASE_URL` in Render environment variables

### Frontend (Vercel)
1. Connect GitHub repository
2. Set root directory: `frontend`
3. Build command: `npm run build`
4. Output directory: `dist`
5. Add environment variable: `VITE_API_URL` (your Render backend URL)

## Notes

- Speech recognition requires a browser that supports Web Speech API (Chrome, Edge)
- CV files should be PDF or DOCX format
- OpenAI API key is required for question generation and feedback

## License

MIT

