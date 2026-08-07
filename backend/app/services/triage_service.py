from app.schemas.triage import (
    PatientInput,
    TriageResponse
)

def analyze_patient(
    patient: PatientInput
):
    missing=[]

    red_flags=[]

    if patient.oxygen_saturation:

        if patient.oxygen_saturation < 90:

            red_flags.append(
                "Low oxygen saturation"
            )

    if patient.heart_rate:

        if patient.heart_rate > 150:

            red_flags.append(
                "Severe tachycardia"
            )


    if patient.consciousness in [
        "confused",
        "drowsy",
        "unresponsive"
    ]:

        red_flags.append(
            "Altered mental status"
        )

    if not patient.respiratory_rate:

        missing.append(
            "Respiratory rate"
        )

    if red_flags:

        level="EMERGENCY"

    elif missing:

        level="INSUFFICIENT_INFORMATION"

    else:

        level="ROUTINE"

    return TriageResponse(

        triage_level=level,

        summary=(
            "Assessment generated using "
            "ClinicalTriage v2 safety layer"
        ),
        red_flags=red_flags,

        recommendations=[
            "Clinical evaluation recommended"
        ],
        missing_information=missing,

        confidence=0.5
    )