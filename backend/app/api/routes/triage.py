from fastapi import APIRouter, Depends, Request
from app.core.audit import audit_logger
from app.core.dependency import get_current_user
from app.schemas.triage import PatientInput, TriageResponse
from app.services.triage_service import analyze_patient

router = APIRouter(tags=["triage"])

@router.post("/triage", response_model=TriageResponse)
def triage_patient(patient: PatientInput, request: Request, user: str = Depends(get_current_user)) -> TriageResponse:
    result = analyze_patient(patient)
    audit_logger.write({
        "assessment_id": str(result.assessment_id),
        "created_at": result.created_at,
        "request_id": request.state.request_id,
        "user": user,
        "triage_level": result.triage_level,
        "risk_score": result.risk_score,
        "confidence": result.confidence,
        "ai_assisted": result.ai_assisted,
        "model_name": result.model_name,
        "model_version": result.model_version,
        "prompt_version": result.prompt_version,
        "evidence_corpus_version": result.evidence_corpus_version,
        "red_flag_codes": [flag.code for flag in result.red_flags],
        "question_count": len(result.follow_up_questions),
    })
    return result
