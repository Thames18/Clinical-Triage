from app.schemas.triage import (
    PatientInput, TriageResponse
)

from app.clinical.red_flags import (
    detect_red_flags
)

from app.clinical.missing_information import (
    detect_missing_information
)

from app.clinical.scoring import (
    calculate_risk_score
)

from app.clinical.uncertainty import (
    calculate_uncertainty
)

from app.clinical.interview import (
    build_follow_up_questions
)

from app.ai.reasoning import (
    AIReasoningService
)

from app.ai.safety_validator import (
    validate_ai_assessment
)


def analyze_patient(
    patient: PatientInput ) -> TriageResponse:

    # 1. Deterministic clinical safety engine

    red_flags = detect_red_flags(
        patient
    )

    missing_information = (
        detect_missing_information(
            patient
        )
    )


    risk_score = calculate_risk_score(
        patient,
        red_flags
    )


    uncertainty = calculate_uncertainty(
        missing_information
    )

    # 2. Emergency override

    critical_flags = [
        flag
        for flag in red_flags
        if flag.severity == "critical"
    ]

    if critical_flags:
        return TriageResponse(
            triage_level="EMERGENCY",
            summary=(
                "A critical clinical finding was detected by the deterministic safety engine."
            ),
            red_flags=red_flags,
            recommendations=[
                (
                    "Immediate in-person clinical assessment is warranted."
                )
            ],
            missing_information=missing_information,
            follow_up_questions=[],
            confidence=0.95,
            risk_score=risk_score,
            ai_assisted=False,
        )

    # 3. Ask for any important that might be missin

    follow_up_questions = (
        build_follow_up_questions(
            patient
        )
    )

    if follow_up_questions:
        return TriageResponse(
            triage_level=(
                "INSUFFICIENT_INFORMATION"
            ),
            summary=(
                "Additional information is needed before completing the assessment."
            ),
            red_flags=red_flags,
            recommendations=[
                (
                    "Provide the requested information and then reassess."
                )
            ],

            missing_information=missing_information,
            follow_up_questions=(
                follow_up_questions
            ),

            confidence=max(
                0.0,
                1.0 - uncertainty,
            ),

            risk_score=risk_score,
            ai_assisted=False,
        )

    # 4. AI reasoning

    ai_service = AIReasoningService()
    patient_data = patient.model_dump()
    ai_assessment = ai_service.assess(
        patient_data
    )

    # 5. AI safety validation

    validation = (
        validate_ai_assessment(
            ai_assessment,
            red_flags
        )
    )

    if not validation.valid:
        return TriageResponse(
            triage_level=(
                "INSUFFICIENT_INFORMATION"
            ),
            summary=(
                "The AI assessment could not be validated safely."
            ),
            red_flags=red_flags,
            recommendations=[
                (
                    "A clinician should review the available information."
                )
            ],

            missing_information=missing_information,
            follow_up_questions=[],
            confidence=0.0,
            risk_score=risk_score,
            ai_assisted=True,
        )

    # 6. Determine final triage level

    if risk_score >= 50:
        triage_level = "URGENT"
    elif risk_score >= 20:
        triage_level = "SAME_DAY"
    else:
        triage_level = "ROUTINE"

    # 7. Return combined result

    final_confidence = min(
        ai_assessment.confidence,
        max(
            0.0,
            1.0 - uncertainty
        ),
    )

    return TriageResponse(
        triage_level=triage_level,
        summary=ai_assessment.summary,
        red_flags=red_flags,
        recommendations=[
            (
                "Use this assessment as decision support and confirm clinically."
            )
        ],

        missing_information=missing_information,
        follow_up_questions=[],
        confidence=final_confidence,
        risk_score=risk_score,
        ai_assisted=True
    )