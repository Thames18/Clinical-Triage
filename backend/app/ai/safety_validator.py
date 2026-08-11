from app.ai.schemas import AIClinicalAssessment
from app.clinical.models import RedFlag


class SafetyValidationResult:
    def __init__(self, valid: bool, issues: list[str]):
        self.valid = valid
        self.issues = issues


def validate_ai_assessment(
    assessment: AIClinicalAssessment,
    red_flags: list[RedFlag],
) -> SafetyValidationResult:
    issues: list[str] = []

    if not assessment.summary.strip():
        issues.append("AI returned an empty summary.")

    if not 0 <= assessment.confidence <= 1:
        issues.append("AI confidence is outside the valid range.")

    critical_flags = [
        flag for flag in red_flags
        if flag.severity == "critical"
    ]

    # The AI is never allowed to contradict the deterministic emergency engine.
    if critical_flags and not assessment.summary.strip():
        issues.append("Critical case requires a non-empty safety summary.")

    return SafetyValidationResult(
        valid=len(issues) == 0,
        issues=issues,
    )
