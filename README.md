# Clinical-Triage

# ClinicalTriage AI 🏥🤖

AI-powered clinical triage assistant that helps clinicians and students analyze patient vitals and symptoms using Large Language Models (LLMs).

The system accepts patient information, processes it through an AI clinical reasoning workflow, and generates structured triage assessments with risk indicators.

> This project is for educational and demonstration purposes only. It is not a replacement for professional medical judgment or emergency care.

---

# Current Status

## Phase 1 — Foundation Setup (In Progress)

Completed:

* Next.js 14 frontend
* TypeScript configuration
* Tailwind CSS styling
* FastAPI backend
* REST API foundation
* Docker support
* Docker Compose setup
* Environment configuration
* Backend health monitoring endpoint

Upcoming:

* Patient intake form
* Clinical data validation
* LLM integration
* Async report generation
* Celery + Redis workers
* PDF triage reports
* Cloud deployment

---

# Tech Stack

## Frontend

| Technology      | Purpose           |
| --------------- | ----------------- |
| Next.js 14      | React framework   |
| TypeScript      | Type safety       |
| Tailwind CSS    | Styling           |
| Axios           | API communication |
| React Hook Form | Form management   |
| Zod             | Validation        |

---

## Backend

| Technology | Purpose              |
| ---------- | -------------------- |
| FastAPI    | Python API framework |
| Pydantic   | Data validation      |
| Uvicorn    | ASGI server          |

---

## Infrastructure

| Technology     | Purpose             |
| -------------- | ------------------- |
| Docker         | Containerization    |
| Docker Compose | Local orchestration |

---

# Project Structure

```
clinical-triage-ai/

├── frontend/
│   ├── src/
│   │   ├── app/
│   │   └── lib/
│   │       └── api.ts
│   ├── Dockerfile
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── prompts/
│   │   ├── workers/
│   │   └── main.py
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

# Running Locally

## Requirements

Install:

* Node.js 20+
* Python 3.12+
* Docker Desktop
* Git

---

# Environment Variables

Create your local environment file:

```
cp .env.example .env
```

Example:

```
OPENAI_API_KEY= .........

OR

ANTHROPIC_API_KEY= ........

REDIS_URL=redis://redis:6379/0

NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

# Running With Docker

From the project root:

```
docker compose up --build
```

Services:

Frontend:

```
http://localhost:3000
```

Backend:

```
http://localhost:8000
```

API Documentation:

```
http://localhost:8000/docs
```

Health Check:

```
http://localhost:8000/health
```

---

# Backend API

## Health Endpoint

GET

```
/health
```

Response:

```json
{
  "status": "healthy"
}
```

---

# Development Without Docker

## Frontend

```
cd frontend

npm install

npm run dev
```

Frontend runs:

```
http://localhost:3000
```

---

## Backend

```
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend runs:

```
http://localhost:8000
```

---

# Roadmap

## Phase 2

* Patient intake UI
* Vitals form
* Symptoms input
* Backend validation models
* AI triage prompt
* Structured JSON response

## Phase 3

* Celery workers
* Redis queue
* Async PDF generation
* Report storage

## Phase 4

* AWS deployment
* CI/CD pipeline
* Production monitoring
* Authentication

---

# License

MIT License