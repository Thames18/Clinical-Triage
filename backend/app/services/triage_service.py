from datetime import datetime, timezone

from app.ai.reasoning import AIReasoningService
from app.ai.safety_validator import validate_ai_assessment
from app.clinical.interview import build_follow_up_questions
from app.clinical.missing_information import detect_missing_information
from app.clinical.red_flags import detect_red_flags
from app.clinical.scoring import calculate_risk_score
from app.clinical.uncertainty import calculate_uncertainty
from app.evidence.citations import validate_citations
from app.evidence.policy import sufficient_evidence
from app.evidence.query import build_clinical_query
from app.evidence.schemas import RetrievedEvidence
from app.evidence.service import EvidenceService, EvidenceUnavailable
from app.schemas.triage import PatientInput, TriageResponse


evidence_service = EvidenceService()


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _emergency_response(
    patient: PatientInput,
    red_flags,
    missing_information,
    risk_score: int,
) -> TriageResponse:
    return TriageResponse(
        triage_level="EMERGENCY",
        summary=(
            "A critical finding was detected by the deterministic safety engine. "
            "The emergency classification does not depend on AI or evidence retrieval."
        ),
        red_flags=red_flags,
        recommendations=[
            "Immediate in-person clinical assessment is warranted."
        ],
        missing_information=missing_information,
        follow_up_questions=[],
        confidence=0.95,
        risk_score=risk_score,
        ai_assisted=False,
        evidence_corpus_version=evidence_service.corpus_version,
        created_at=_timestamp(),
    )


def _deterministic_level(risk_score: int, red_flags) -> str:
    if any(flag.severity == "high" for flag in red_flags):
        return "URGENT"

    if risk_score >= 20:
        return "SAME_DAY"

    if not red_flags:
        return "SELF_CARE"

    # This is an engineering category, not a validated clinical scale.
    return "ROUTINE"


def analyze_patient(patient: PatientInput) -> TriageResponse:
    red_flags = detect_red_flags(patient)
    missing_information = detect_missing_information(patient)
    risk_score = calculate_risk_score(patient, red_flags)
    uncertainty = calculate_uncertainty(missing_information)

    critical_flags = [
        flag for flag in red_flags
        if flag.severity == "critical"
    ]

    if critical_flags:
        return _emergency_response(
            patient,
            red_flags,
            missing_information,
            risk_score,
        )

    follow_up_questions = build_follow_up_questions(patient)

    # Critical missing information stops the assessment. Non-critical missing
    # fields are allowed to continue so the system can use the available evidence.
    if any(item.priority in {"critical", "high"} for item in missing_information):
        return TriageResponse(
            triage_level="INSUFFICIENT_INFORMATION",
            summary=(
                "Additional information is required before a safe assessment "
                "can be completed."
            ),
            red_flags=red_flags,
            recommendations=[
                "Provide the requested information and reassess."
            ],
            missing_information=missing_information,
            follow_up_questions=follow_up_questions,
            confidence=max(0.0, 1.0 - uncertainty),
            risk_score=risk_score,
            ai_assisted=False,
            evidence_corpus_version=evidence_service.corpus_version,
            created_at=_timestamp(),
        )

    try:
        evidence = evidence_service.search(
            build_clinical_query(patient),
            top_k=5,
        )
    except EvidenceUnavailable as exc:
        return TriageResponse(
            triage_level="ASSESSMENT_UNAVAILABLE",
            summary=str(exc),
            red_flags=red_flags,
            recommendations=[
                "Do not rely on an AI-generated assessment until the reviewed "
                "evidence index is available."
            ],
            missing_information=missing_information,
            follow_up_questions=follow_up_questions,
            confidence=0.0,
            risk_score=risk_score,
            ai_assisted=False,
            evidence_corpus_version=evidence_service.corpus_version,
            created_at=_timestamp(),
        )
    except RuntimeError as exc:
        return TriageResponse(
            triage_level="ASSESSMENT_UNAVAILABLE",
            summary="Evidence retrieval is currently unavailable.",
            red_flags=red_flags,
            recommendations=[
                "A clinician should review the available information directly."
            ],
            missing_information=missing_information,
            follow_up_questions=follow_up_questions,
            confidence=0.0,
            risk_score=risk_score,
            ai_assisted=False,
            evidence_corpus_version=evidence_service.corpus_version,
            created_at=_timestamp(),
            validation_issues=[str(exc)],
        )

    if not sufficient_evidence(evidence):
        return TriageResponse(
            triage_level="ASSESSMENT_UNAVAILABLE",
            summary=(
                "No sufficiently relevant reviewed evidence was retrieved "
                "for this assessment."
            ),
            red_flags=red_flags,
            recommendations=[
                "Do not rely on an unsupported AI recommendation. "
                "A clinician should review the available information."
            ],
            missing_information=missing_information,
            follow_up_questions=follow_up_questions,
            confidence=0.0,
            risk_score=risk_score,
            ai_assisted=False,
            evidence_corpus_version=evidence_service.corpus_version,
            created_at=_timestamp(),
        )

    try:
        ai_service = AIReasoningService()
        ai_assessment = ai_service.assess(
            patient.model_dump(),
            evidence,
        )
    except Exception as exc:
        return TriageResponse(
            triage_level="ASSESSMENT_UNAVAILABLE",
            summary="The AI assessment service is currently unavailable.",
            red_flags=red_flags,
            recommendations=[
                "A clinician should review the available information directly."
            ],
            missing_information=missing_information,
            follow_up_questions=follow_up_questions,
            confidence=0.0,
            risk_score=risk_score,
            ai_assisted=False,
            evidence_corpus_version=evidence_service.corpus_version,
            created_at=_timestamp(),
            validation_issues=[str(exc)],
        )

    validation = validate_ai_assessment(
        ai_assessment,
        red_flags,
    )

    citation_issues = validate_citations(
        ai_assessment,
        evidence,
    )

    all_issues = validation.issues + citation_issues

    if all_issues:
        return TriageResponse(
            triage_level="ASSESSMENT_UNAVAILABLE",
            summary="The AI assessment failed safety or evidence validation.",
            red_flags=red_flags,
            recommendations=[
                "Do not rely on the AI assessment. "
                "A clinician should review the available information."
            ],
            missing_information=missing_information,
            follow_up_questions=follow_up_questions,
            confidence=0.0,
            risk_score=risk_score,
            ai_assisted=False,
            evidence_corpus_version=evidence_service.corpus_version,
            created_at=_timestamp(),
            validation_issues=all_issues,
        )

    triage_level = _deterministic_level(
        risk_score,
        red_flags,
    )

    final_confidence = min(
        ai_assessment.confidence,
        max(0.0, 1.0 - uncertainty),
    )

    return TriageResponse(
        triage_level=triage_level,
        summary=ai_assessment.summary,
        red_flags=red_flags,
        recommendations=ai_assessment.recommendations,
        missing_information=missing_information,
        follow_up_questions=follow_up_questions,
        confidence=final_confidence,
        risk_score=risk_score,
        ai_assisted=True,
        evidence_citations=ai_assessment.citations,
        evidence_corpus_version=evidence_service.corpus_version,
        model_name="openai",
        model_version=ai_service.model,
        prompt_version=ai_service.prompt_version,
        created_at=_timestamp(),
    )
