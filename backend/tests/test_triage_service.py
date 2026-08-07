from app.schemas.triage import PatientInput
from app.services.triage_service import analyze_patient

def test_critical_red_flag_overrides_missing_information():
    patient = PatientInput(
        age=65,
        symptoms=[
            "shortness of breath"
        ],
        oxygen_saturation=84,
        respiratory_rate=None,
        consciousness="unknown",
    )

    result = analyze_patient(patient)

    assert (
        result.triage_level
        == "EMERGENCY"
    )

def test_missing_information_is_reported():

    patient = PatientInput(
        age=30,
        symptoms=[
            "headache"
        ],
    )

    result = analyze_patient(patient)

    assert len(
        result.missing_information
    ) > 0

def test_high_heart_rate_is_emergency():

    patient = PatientInput(
        age=40,
        symptoms=[
            "palpitations"
        ],
        heart_rate=170,
        respiratory_rate=20,
        consciousness="alert",
    )

    result = analyze_patient(patient)

    assert (
        result.triage_level
        == "EMERGENCY"
    )