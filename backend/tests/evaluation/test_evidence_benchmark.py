def test_emergency_cases_do_not_depend_on_ai():
  
    from app.schemas.triage import PatientInput
    from app.services.triage_service import (
        analyze_patient
    )

    patient = PatientInput(
        age=72,
        sex="female",
        temperature_c=38.2,
        heart_rate=128,
        respiratory_rate=32,
        systolic_bp=108,
        diastolic_bp=68,
        oxygen_saturation=84,
        consciousness="alert",
        symptoms=[
            "shortness of breath"
        ],
        symptom_duration_hours=4,
        medical_history=[],
        medications=[],
        allergies=[],
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