from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.triage import PatientInput
from app.services.llm import analyze_patient
from app.api.routes import report, auth
from app.core.dependency import get_current_user

app = FastAPI(
    title="Clinical Triage AI API",
    version="1.0.0"
)

app.include_router(report.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Clinical Triage API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

app.include_router(auth.router)
app.include_router(report.router, dependencies=[Depends(get_current_user)])


@app.post("/triage")
def triage(patient: PatientInput, user: str = Depends(get_current_user)):
    result = analyze_patient(patient)
    return result