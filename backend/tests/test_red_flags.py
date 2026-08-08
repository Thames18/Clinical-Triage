from app.schemas.triage import PatientInput
from app.clinical.red_flags import detect_red_flags

def test_low_oxygen_is_critical():

    patient = PatientInput(
        age=60,
        symptoms=["shortness of breath"],
        oxygen_saturation=85,
    )
    flags = detect_red_flags(patient)
    assert any(
        flag.code == "LOW_OXYGEN"
        for flag in flags
    )

def test_severe_tachycardia():
    patient = PatientInput(
        age=45,
        symptoms=["palpitations"],
        heart_rate=160,
    )
    flags = detect_red_flags(patient)
    assert any(
        flag.code == "SEVERE_TACHYCARDIA"
        for flag in flags
    )


def test_altered_mental_status():
    patient = PatientInput(
        age=70,
        symptoms=["confusion"],
        consciousness="confused",
    )

    flags = detect_red_flags(patient)
    assert any(
        flag.code == "ALTERED_MENTAL_STATUS"
        for flag in flags
    )