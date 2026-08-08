from app.ai.schemas import AIClinicalAssessment
from app.clinical.models import RedFlag

class SafetyValidationResult:
    def __init__(
        self, valid: bool, issues: list[str] ):
        self.valid = valid
        self.issues = issues

def validate_ai_assessment( 
    assessment: AIClinicalAssessment, red_flags: list[RedFlag] ) -> SafetyValidationResult:

    issues: list[str] = []
    critical_flags = [
        flag
        for flag in red_flags
        if flag.severity == "critical"
    ]

    # Emergency consistency check

    if critical_flags:
        if assessment.confidence < 0:
            issues.append( "Invalid AI confidence." )

        if not assessment.summary.strip():
            issues.append( "AI returned an empty summary." )

    # Confidence validation

    if not 0 <= assessment.confidence <= 1:
        issues.append( "AI confidence is outside the valid range.")
    return SafetyValidationResult(
        valid=len(issues) == 0,
        issues=issues
    )