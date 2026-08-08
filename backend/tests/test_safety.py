from app.schemas.triage import PatientInput
from app.services.triage_service import (
    analyze_patient
)

def test_llm_cannot_override_emergency():
    patient = PatientInput(
        age=70,
        sex="female",
        oxygen_saturation=84,
        heart_rate=160,
        respiratory_rate=None,
        systolic_bp=None,
        diastolic_bp=None,
        temperature_c=None,
        consciousness="unknown",
        symptoms=[
            "shortness of breath",
        ]
    )

    result = analyze_patient(
        patient
    )

    assert (
        result.triage_level
        == "EMERGENCY"
    )

    assert (
        result.ai_assisted
        is False
    )