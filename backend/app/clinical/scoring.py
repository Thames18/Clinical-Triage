from app.clinical.models import RedFlag
from app.schemas.triage import PatientInput

def calculate_risk_score(
    patient: PatientInput,
    red_flags: list[RedFlag],
) -> int:
    score = 0
    for flag in red_flags:
        if flag.severity == "critical":
            score += 100
        elif flag.severity == "high":
            score += 50
        elif flag.severity == "moderate":
            score += 20
    # Additional contextual risk
    if patient.age >= 75:
        score += 10
    if patient.age <= 2:
        score += 10
    return score