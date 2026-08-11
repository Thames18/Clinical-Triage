from app.schemas.triage import PatientInput
from app.services.triage_service import analyze_patient

def test_week6_service_has_deterministic_emergency():
    patient = PatientInput(
        age=65, sex="male", symptoms=["shortness of breath"],
        oxygen_saturation=84, respiratory_rate=28,
        consciousness="alert", symptom_duration_hours=1
    )
    result = analyze_patient(patient)
    assert result.triage_level == "EMERGENCY"
    assert result.ai_assisted is False
    assert result.model_name is not None
    assert result.prompt_version is not None

def test_week6_service_generates_structured_followups():
    patient = PatientInput(age=30, sex="female", symptoms=["headache"])
    result = analyze_patient(patient)
    assert result.triage_level == "INSUFFICIENT_INFORMATION"
    assert len(result.follow_up_questions) > 0
