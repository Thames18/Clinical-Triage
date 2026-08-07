from fastapi import APIRouter
from app.schemas.triage import (
    PatientInput,
    TriageResponse
)

from app.services.triage_service import (
    analyze_patient
)

router = APIRouter()
@router.post(
    "/triage",
    response_model=TriageResponse
)
def triage_patient(
    patient: PatientInput
):
    return analyze_patient(patient)