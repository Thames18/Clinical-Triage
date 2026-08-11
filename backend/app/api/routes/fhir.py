from fastapi import APIRouter, Depends, Query
from app.core.dependency import get_current_user
from app.core.fhir import triage_to_fhir_bundle
from app.schemas.triage import PatientInput
from app.services.triage_service import analyze_patient

router = APIRouter(prefix="/fhir", tags=["fhir"])

@router.post("/triage")
def triage_as_fhir(
    patient: PatientInput,
    patient_id: str = Query(..., min_length=1, max_length=64),
    _user: str = Depends(get_current_user),
):
    result = analyze_patient(patient)
    return triage_to_fhir_bundle(patient, result, patient_id)
