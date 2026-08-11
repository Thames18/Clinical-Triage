from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, report
from app.core.dependency import get_current_user
from app.schemas.triage import PatientInput, TriageResponse
from app.services.triage_service import analyze_patient


app = FastAPI(
    title="Clinical Triage AI API",
    version="2.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://triage.mustafalsalem.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(
    report.router,
    dependencies=[Depends(get_current_user)],
)


@app.get("/")
def root():
    return {
        "message": "Clinical Triage API",
        "version": "2.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "clinical-triage",
    }


@app.post("/triage", response_model=TriageResponse)
def triage(
    patient: PatientInput,
    user: str = Depends(get_current_user),
) -> TriageResponse:
    return analyze_patient(patient)
