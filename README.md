# 🎯 Virtual Interview Navigator

> An AI-powered mock interview platform that generates personalized questions from your CV and delivers structured performance feedback.

[![Status](https://img.shields.io/badge/Status-Live-success?style=flat-square)](https://interviewnav.vercel.app)
[![Backend](https://img.shields.io/badge/Backend-Flask%20%7C%20Python-blue?style=flat-square)](https://flask.palletsprojects.com)
[![Frontend](https://img.shields.io/badge/Frontend-React%20%7C%20Vite-61DAFB?style=flat-square)](https://vitejs.dev)
[![AI](https://img.shields.io/badge/AI-GPT--4o--mini-412991?style=flat-square)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## 📖 Overview

Virtual Interview Navigator lets you upload your CV, specify a target job role and description, and step into a full mock interview — all powered by OpenAI. The system tailors every question to your specific background and grades your answers with detailed, actionable feedback.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **Personalized Questions** | CV + Job Description fed directly into GPT-4o-mini for context-aware question generation |
| 🎙️ **Voice Input** | Speak your answers using the native Browser Speech Recognition API |
| 📊 **Scored Feedback** | Per-question scores (0–1.0) with Correct / Partial / Wrong badges |
| 📝 **Full Report** | Markdown report covering Communication, Confidence, Technical Accuracy & Improvement Areas |
| 🔐 **Secure Auth** | Stateless JWT authentication with protected routes |
| 📄 **Document Parsing** | Supports PDF and DOCX CV uploads |

---

## 🛠️ Tech Stack

### Frontend
- **React 18** (Vite) — component-based UI
- **Tailwind CSS** — utility-first responsive styling
- **Axios** — HTTP client with JWT interceptors
- **Web Speech API** — browser-native voice recognition
- **React Markdown** — renders AI-generated feedback reports

### Backend
- **Python / Flask** — lightweight REST API
- **PostgreSQL** (Neon) — relational data persistence
- **SQLAlchemy** — ORM and migration management
- **OpenAI GPT-4o-mini** — question generation & answer analysis
- **PyPDF2 / python-docx** — CV text extraction

### Infrastructure
- **Vercel** — frontend deployment
- **Render** — backend container hosting
- **Neon** — serverless PostgreSQL

---

## 🗂️ Project Structure

```
interviewnav/
├── backend/
│   ├── app.py              # Flask app, all API routes
│   ├── model.py            # SQLAlchemy models
│   ├── prompts.py          # OpenAI prompt templates
│   ├── config.py           # Environment configuration
│   ├── extensions.py       # DB & JWT initialization
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── pages/          # Home, Login, Interview, Report …
    │   ├── services/       # api.js, authService.js
    │   └── App.jsx
    └── package.json
```

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (local or Neon)

### 1. Database

```sql
CREATE DATABASE "InterviewNavigator";
```

### 2. Backend

```bash
cd backend
python -m venv venv

# Activate (choose your OS)
# Windows:   venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
flask db upgrade
python app.py
```

Create a `backend/.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/InterviewNavigator
OPENAI_API_KEY=sk-...
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:5173
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Create a `frontend/.env` file:

```env
VITE_API_URL=http://localhost:5000
```

---

## 🚀 Deployment

### Backend — Render

| Setting | Value |
|---|---|
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn app:app --timeout 300` |
| **Env Vars** | `DATABASE_URL`, `OPENAI_API_KEY`, `SECRET_KEY`, `CORS_ORIGINS` |

### Frontend — Vercel

| Setting | Value |
|---|---|
| **Framework** | React (Vite) |
| **Env Vars** | `VITE_API_URL` → your Render backend URL (no trailing slash) |

---

## 🔄 How It Works

```
1. Register / Login  →  JWT issued
2. Upload CV (PDF/DOCX)  →  Text extracted & stored
3. Enter Job Role + JD  →  Sent to GPT-4o-mini with CV context
4. Answer questions  →  Via text or voice input
5. Complete interview  →  GPT analyses all responses
6. View Report  →  Scores, badges & improvement suggestions
```

---
