from fastapi import APIRouter, Depends

from app.core.dependency import get_current_user
from app.schemas.triage import PatientInput, TriageResponse
from app.services.triage_service import analyze_patient


router = APIRouter()


@router.post(
    "/triage",
    response_model=TriageResponse,
)
def triage_patient(
    patient: PatientInput,
    user: str = Depends(get_current_user),
) -> TriageResponse:
    return analyze_patient(patient)
