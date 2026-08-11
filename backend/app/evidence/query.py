from app.schemas.triage import PatientInput


def build_clinical_query(patient: PatientInput) -> str:
    symptoms = ", ".join(patient.symptoms) or "none reported"
    vitals: list[str] = []

    if patient.temperature_c is not None:
        vitals.append(f"temperature {patient.temperature_c} C")
    if patient.heart_rate is not None:
        vitals.append(f"heart rate {patient.heart_rate} bpm")
    if patient.respiratory_rate is not None:
        vitals.append(f"respiratory rate {patient.respiratory_rate}/min")
    if patient.systolic_bp is not None:
        vitals.append(f"systolic BP {patient.systolic_bp} mmHg")
    if patient.diastolic_bp is not None:
        vitals.append(f"diastolic BP {patient.diastolic_bp} mmHg")
    if patient.oxygen_saturation is not None:
        vitals.append(f"oxygen saturation {patient.oxygen_saturation}%")

    history = ", ".join(patient.medical_history) or "none reported"

    return (
        f"Patient age {patient.age}, sex {patient.sex}. "
        f"Symptoms: {symptoms}. "
        f"Vital signs: {', '.join(vitals) or 'none reported'}. "
        f"Medical history: {history}."
    )
