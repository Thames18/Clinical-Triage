# ClinicalTriage AI

AI-powered clinical triage assistant that helps clinicians and students analyze patient vitals and symptoms using Large Language Models (LLMs).

The system accepts patient information, processes it through an AI clinical reasoning workflow, and generates structured triage assessments with risk indicators.

**Live app:** [triage.mustafalsalem.com](https://triage.mustafalsalem.com/)

> This project is moving from demo to production. Until Phase 4 (Evaluation) and Phase 6 (Serious Engineering) are complete, it should not be used as a substitute for professional medical judgment or emergency care.

---

## Where This Project Stands

This README tracks two eras of the project: the original **demo build** (proof of concept) and the **production hardening plan** currently underway. Jump to whichever you need.

- [ Demo Phase (Archived)](#-demo-phase-archived) — what shipped before this rebuild
- [ Production Phase (Active)](#-production-phase-active) — what's being built now, and where we are today

---

## Demo Phase (Archived)

The original prototype validated the core idea: patient intake → AI reasoning → structured triage output. It was never intended for real clinical use — no safety layer, no evaluation, no auth.

### Demo Phase 1 — Foundation Setup Completed
- Next.js 16+ frontend
- TypeScript configuration
- Tailwind CSS styling
- FastAPI backend
- REST API foundation
- Docker + Docker Compose setup
- Environment configuration
- Backend health monitoring endpoint

### Demo Phase 2 — AI Clinical Triage Completed
- Patient intake UI (basic)
- Vitals form
- Symptoms input
- Backend validation models
- AI triage prompt
- Structured JSON response

**Status:** superseded. This build proved the concept but lacked a real patient schema, clinical safety checks, evaluation, and production infrastructure — which is exactly what the plan below addresses.

---

## Production Phase (Active)

Full rebuild plan to take ClinicalTriage AI from demo to a real, safety-checked, evaluated product.

**Current stage: Phase 2 — Clinical Safety (in progress)**

| Phase | Focus | Status |
|---|---|---|
| Phase 1 | Make the current prototype real | Done |
| **Phase 2** | **Clinical safety** |  |
| Phase 3 | Better AI | Done |
| Phase 4 | Evaluation | Done |
| Phase 5 | Product | Done |
| Phase 6 | Serious engineering | 🔄 **In progress** |

### Phase 1 — Make the current prototype real (Week 1)
- [x] Proper intake UI
- [x] Better patient schema
- [x] Structured BP
- [x] Respiratory rate
- [x] Symptom duration
- [x] Demographics
- [x] Validation
- [x] Loading/error states

### Phase 2 — Clinical safety (Week 2) 
- [x] Deterministic red flags
- [x] Vital-sign validation
- [x] Emergency override
- [x] Missing-data detection
- [x] Standardized triage categories
- [x] Uncertainty handling

### Phase 3 — Better AI (Week 3)
- [x] Structured output schema
- [x] Better prompts
- [x] Clinical reasoning layer
- [x] Evidence retrieval
- [x] Citations
- [x] Safety validator

### Phase 4 — Evaluation (Week 4)
- [x] 100–500 synthetic cases
- [x] Emergency cases
- [x] Ambiguous cases
- [x] Adversarial cases
- [x] Sensitivity/specificity analysis
- [x] False-negative analysis
- [x] Regression testing

### Phase 5 — Product (Week 5)
- [x] Polished dashboard
- [x] History
- [x] Reports
- [x] PDF export
- [x] Student mode
- [x] Scenario simulator
- [x] Explanations

### Phase 6 — Serious engineering (Week 6+)
- [x] Audit logging
- [x] FHIR compatibility
- [x] Monitoring
- [x] Model/version tracking
- [ ] Security hardening
- [x] Deployment pipeline
- [x] CI/CD


---

## Tech Stack

### Frontend

| Technology | Purpose |
|---|---|
| Next.js 16 | React framework |
| TypeScript | Type safety |
| Tailwind CSS | Styling |
| Axios | API communication |
| React Hook Form | Form management |
| Zod | Validation |

### Backend

| Technology | Purpose |
|---|---|
| FastAPI | Python API framework |
| Pydantic | Data validation |
| Uvicorn | ASGI server |

### Infrastructure

| Technology | Purpose |
|---|---|
| Docker | Containerization |
| Docker Compose | Local orchestration |

---

## Project Structure

```
clinical-triage-ai/

├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/
│   │       └── api.ts
│   ├── Dockerfile
│   └── package.json
│   └── .dockerignore
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
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

## Out of Scope (Security)
Since this will be used with the same staff it was opted out the security (Login/ Log out) it wont be needed for now

---

## Running Locally

### Requirements
- Node.js 20+
- Python 3.12+
- Docker Desktop
- Git

### Environment Variables

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

### Running With Docker

From the project root:

```
docker compose up --build
```

Services:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### Development Without Docker

**Frontend**
```
cd frontend
npm install
npm run dev
```
Runs at `http://localhost:3000`

**Backend**
```
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Runs at `http://localhost:8000`

---

## Backend API

### Health Endpoint

`GET /health`

Response:
```json
{
  "status": "healthy"
}
```

---

## License

MIT License