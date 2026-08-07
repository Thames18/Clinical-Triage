from app.services.triage_service import analyze_patient
from app.schemas.triage import PatientInput
def test_low_oxygen():
    patient=PatientInput(
        age=60,
        symptoms=[
            "shortness of breath"
        ],
        oxygen_saturation=85
    )
    result=analyze_patient(patient)
    assert (
        result.triage_level
        ==
        "EMERGENCY"
    )