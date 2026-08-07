from app.schemas.triage import PatientInput

def validate_patient(patient: PatientInput):

    warnings = []

    if (
        patient.systolic_bp
        and patient.diastolic_bp
        and patient.systolic_bp < patient.diastolic_bp
    ):
        warnings.append(
            "Invalid blood pressure relationship"
        )

    if not patient.symptoms:
        warnings.append(
            "Symptoms missing"
        )

    return warnings