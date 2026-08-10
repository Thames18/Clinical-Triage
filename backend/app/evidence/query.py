from app.schemas.triage import (
    PatientInput
)

def build_clinical_query(
    patient: PatientInput
) -> str:

    symptoms = ", ".join(
        patient.symptoms
    )
    vitals = []
    if patient.temperature_c is not None:
        vitals.append(
            f"temperature {patient.temperature_c} C"
        )
    if patient.heart_rate is not None:
        vitals.append(
            f"heart rate {patient.heart_rate}"
        )

    if patient.respiratory_rate is not None:
        vitals.append(
            f"respiratory rate {patient.respiratory_rate}"
        )
    if patient.oxygen_saturation is not None:
        vitals.append(
            f"oxygen saturation "
            f"{patient.oxygen_saturation}%"
        )
    return (
        f"Patient age {patient.age}, "
        f"sex {patient.sex}. "
        f"Symptoms: {symptoms}. "
        f"Vital signs: "
        f"{', '.join(vitals)}."
    )