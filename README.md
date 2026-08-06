# ClinicalTriage AI

AI-powered clinical triage assistant that helps clinicians and students analyze patient vitals and symptoms using Large Language Models (LLMs). The system accepts patient information, processes it through an AI clinical reasoning workflow, generates structured triage assessments, and produces downloadable PDF reports — all behind JWT-protected endpoints, deployed to AWS with automated CI/CD.

> This project is for educational and demonstration purposes only. It is not a replacement for professional medical judgment or emergency care.

---

## Current Status — All Phases Complete ✅

### Phase 1 — Foundation Setup
- Next.js 16 frontend, TypeScript, Tailwind CSS
- FastAPI backend, REST API foundation
- Docker + Docker Compose
- Health monitoring endpoint

### Phase 2 — AI Clinical Triage
- Patient intake UI (vitals + symptoms)
- Backend validation models (Pydantic)
- LLM-driven triage reasoning
- Structured JSON triage response

### Phase 3 — Async Reporting Infrastructure
- Celery workers for background task processing
- Redis as message broker + result backend
- Asynchronous PDF triage report generation (ReportLab)
- Flower dashboard for background task monitoring

### Phase 4 — Production Deployment
- JWT authentication protecting triage and report endpoints
- AWS EC2 deployment (Docker Compose in production)
- GitHub Actions CI/CD — auto-deploys on push to `main`
- Background task monitoring accessible in production via Flower

---

## Tech Stack

### Frontend
| Technology | Purpose |
|---|---|
| Next.js 16 | React framework |
| TypeScript | Type safety |
| Tailwind CSS | Styling |
| Axios | API communication |

### Backend
| Technology | Purpose |
|---|---|
| FastAPI | Python API framework |
| Pydantic | Data validation |
| Uvicorn | ASGI server |
| python-jose | JWT encode/decode |
| passlib + bcrypt | Password hashing |

### Async Processing
| Technology | Purpose |
|---|---|
| Celery | Distributed task queue |
| Redis | Message broker + result backend |
| Flower | Task monitoring dashboard |
| ReportLab | PDF generation |

### Infrastructure
| Technology | Purpose |
|---|---|
| Docker / Docker Compose | Containerization & orchestration |
| AWS EC2 | Production hosting |
| GitHub Actions | CI/CD — auto-deploy on push |

---

## Architecture

```
                    ┌─────────────┐
                    │   Frontend   │  (Next.js, :3000)
                    └──────┬──────┘
                           │ REST
                    ┌──────▼──────┐
                    │   Backend    │  (FastAPI, :8000)
                    │  + JWT auth  │
                    └───┬──────┬──┘
                        │      │
              ┌─────────▼┐   ┌▼──────────┐
              │  Redis   │◄──┤  Celery    │
              │  :6379   │   │  Worker    │
              └────┬─────┘   └────────────┘
                   │
             ┌─────▼─────┐
             │  Flower    │  (:5555 — task monitoring)
             └────────────┘
```

---

## Project Structure

```
Clinical-Triage/
├── .github/workflows/
│   └── deploy.yml              # CI/CD — deploys to EC2 on push to main
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/api.ts
│   ├── Dockerfile
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   │   ├── auth.py         # POST /auth/login
│   │   │   └── report.py       # /reports/* — protected
│   │   ├── core/
│   │   │   ├── celeryapp.py    # Celery app config
│   │   │   ├── config.py       # Settings (env vars)
│   │   │   ├── security.py     # JWT + password hashing
│   │   │   └── dependency.py   # get_current_user dependency
│   │   ├── schemas/
│   │   ├── services/
│   │   │   └── llm.py          # LLM triage reasoning
│   │   ├── workers/
│   │   │   └── task.py         # generate_triage_report Celery task
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml          # frontend, backend, redis, celery_worker, flower
├── .env.example
└── README.md
```

---

## Environment Variables

```bash
cp .env.example .env
```

```
OPENAI_API_KEY=...
# or
ANTHROPIC_API_KEY=...

REDIS_URL=redis://redis:6379/0
NEXT_PUBLIC_API_URL=http://localhost:8000

JWT_SECRET_KEY=<generate: python -c "import secrets; print(secrets.token_hex(32))">
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=<generate: see Authentication section below>
```

---

## Running With Docker (Recommended)

```bash
docker compose up -d --build
```

| Service | URL | Purpose |
|---|---|---|
| Frontend | http://localhost:3000 | Patient intake UI |
| Backend | http://localhost:8000 | API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Health Check | http://localhost:8000/health | Liveness check |
| Flower | http://localhost:5555 | Background task monitoring |

---

## Authentication

All `/triage` and `/reports/*` endpoints require a JWT bearer token.

**1. Generate a password hash once, locally:**
```bash
docker compose exec backend python -c "from passlib.context import CryptContext; print(CryptContext(schemes=['bcrypt']).hash('yourpassword'))"
```
Paste the output into `ADMIN_PASSWORD_HASH` in `.env`, restart the backend.

**2. Log in to get a token:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -d "username=admin&password=yourpassword"
```
Returns:
```json
{ "access_token": "eyJhbGciOi...", "token_type": "bearer" }
```

**3. Use the token on protected routes:**
```bash
curl http://localhost:8000/triage \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{ ... patient data ... }'
```

---

## Backend API Reference

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `/health` | No | Health check |
| POST | `/auth/login` | No | Get a JWT access token |
| POST | `/triage` | Yes | Run AI triage analysis |
| POST | `/reports/generate` | Yes | Queue async PDF report generation |
| GET | `/reports/status/{task_id}` | Yes | Poll Celery task status |
| GET | `/reports/download/{task_id}` | Yes | Download completed PDF report |

---

## Async Report Generation Flow

1. `POST /reports/generate` → returns a `task_id`, work is queued to Celery via Redis
2. Celery worker picks it up, generates the PDF with ReportLab
3. `GET /reports/status/{task_id}` → poll until `status: "SUCCESS"`
4. `GET /reports/download/{task_id}` → streams back the PDF
5. Watch it happen live in Flower at `http://localhost:5555`

---

## Development Without Docker

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

**Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Celery worker** (separate terminal, from `backend/`)
```bash
celery -A app.core.celeryapp.celery_app worker --loglevel=info
```

**Flower** (separate terminal, from `backend/`)
```bash
celery -A app.core.celeryapp.celery_app flower --port=5555
```

> Both require a running Redis instance — `docker run -p 6379:6379 redis:7-alpine` if you don't have one locally.

---

## Deployment (AWS EC2 + GitHub Actions)

Production runs the same `docker-compose.yml` on an EC2 instance. Every push to `main` triggers `.github/workflows/deploy.yml`, which SSHes into the instance and redeploys automatically:

```
git pull origin main
docker compose down
docker compose up -d --build
```

Required GitHub Actions secrets: `EC2_HOST`, `EC2_USER`, `EC2_SSH_KEY`.

---

## License

MIT License