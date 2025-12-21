# Virtual Interview Navigator – AI Interview System

**Virtual Interview Navigator** is an AI-powered full-stack application designed to simulate real-world technical interviews. It generates personalized interview questions based on the candidate's CV, Job Role, and Job Description, and provides comprehensive, structured feedback on performance.

![Project Status](https://img.shields.io/badge/Status-Live-success)
![Tech Stack](<https://img.shields.io/badge/Stack-MERN%20(Python%2FReact)-blue>)

## 🚀 Key Features

### 🧠 Intelligent Orchestration

- **End-to-End Request Pipeline**: Validates, persists, and processes interview context (CV, Role, JD) to generate highly relevant questions.
- **RAG-Lite Personalization**: Uses "Retrieval-Augmented Generation" principles to tailor prompts based on uploaded documents.

### 🎙️ Interactive Interface

- **Voice-Enabled**: Integrated **Browser Speech Recognition** allows candidates to speak their answers hands-free.
- **Real-Time Responsiveness**: Mobile-friendly, adaptive UI centered around user experience.

### 📊 Comprehensive Feedback System

- **Detailed Scoring**: Assigns weighted scores (0-1.0) per question based on relevance and correctness.
- **Structured Analysis**: Generates rich **Markdown reports** analyzing:
  - **Communication Skills**
  - **Confidence**
  - **Technical Accuracy**
  - **Areas for Improvement**
- **Visual Badges**: Instant "Correct", "Partial", or "Wrong" status indicators.

### 🏗️ Robust Architecture

- **Stateless Backend**: Flask REST API with JWT-based authentication and PostgreSQL persistence.
- **Document Ingestion**: Robust `PyPDF2` and `python-docx` pipelines for text extraction.
- **AI Integration Layer**: Isolated service layer ensuring clean separation between business logic and LLM inference.

---

## 🛠️ Tech Stack

### Frontend

- **React.js (Vite)**: High-performance UI library.
- **Tailwind CSS**: Utility-first styling for responsive design.
- **Web Speech API**: Native browser speech recognition.
- **React Markdown**: Rich text rendering for AI reports.
- **Axios**: HTTP client with interceptors for JWT handling.

### Backend

- **Python Flask**: Lightweight, extensible web framework.
- **PostgreSQL (Neon DB)**: Relational database for persistent storage.
- **SQLAlchemy ORM**: Database abstraction layer.
- **OpenAI GPT-4o**: Large Language Model for inference.
- **PyPDF2 / python-docx**: Document processing.

### Infrastructure

- **Render**: Backend container orchestration.
- **Vercel**: Frontend edge deployment.
- **Neon**: Serverless PostgreSQL.

---

## 🔧 Local Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL

### 1. Database

Create a database named `InterviewNavigator`.

```sql
CREATE DATABASE "InterviewNavigator";
```

### 2. Backend

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
python app.py
```

_Note: Ensure `.env` is configured with `DATABASE_URL` and `OPENAI_API_KEY`._

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

_Note: Ensure `.env` has `VITE_API_URL=http://localhost:5000` locally._

---

## 🚀 Deployment Guide

### Backend (Render)

1.  **Build Command**: `./build.sh` (Installs deps + runs DB migrations).
2.  **Start Command**: `gunicorn app:app --timeout 300` (Increased timeout for long AI generation).
3.  **Env Vars**: `DATABASE_URL` (Neon), `OPENAI_API_KEY`, `CORS_ORIGINS` (Vercel URL).

### Frontend (Vercel)

1.  **Framework**: React (Vite).
2.  **Env Vars**: `VITE_API_URL` (Your Render Backend URL, no trailing slash).

---

## 🛡️ License

MIT License.
