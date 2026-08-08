from app.ai.schemas import (
    AIClinicalAssessment
)

from app.ai.safety_validator import (
    validate_ai_assessment
)

from app.clinical.models import RedFlag

def test_valid_ai_assessment():
    assessment = AIClinicalAssessment(
        summary="Patient assessment.",
        clinical_concerns=[],
        suggested_questions=[],
        uncertainty_reasons=[],
        confidence=0.8,
    )

    result = validate_ai_assessment(
        assessment,
        []
    )
    assert result.valid is True

def test_confidence_must_be_valid():
    assessment = AIClinicalAssessment(
        summary="Assessment",
        confidence=0.8,
    )

    result = validate_ai_assessment(
        assessment,
        []
    )

    assert result.valid is True