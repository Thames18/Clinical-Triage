from app.schemas.triage import PatientInput
from app.clinical.models import MissingInformation

def detect_missing_information(
    patient: PatientInput,
) -> list[MissingInformation]:

    missing = []
    if not patient.symptoms:
        missing.append(
            MissingInformation(
                field="symptoms",
                reason=(
                    "Symptoms are required to perform a meaningful triage assessment."
                ),
                priority="critical",
            )
        )

    if patient.respiratory_rate is None:
        missing.append(
            MissingInformation(
                field="respiratory_rate",
                reason=(
                    "Respiratory rate is useful for assessing respiratory severity."
                ),
                priority="high",
            )
        )

    if patient.symptom_duration_hours is None:
        missing.append(
            MissingInformation(
                field="symptom_duration_hours",
                reason=(
                    "Symptom duration helps determine clinical urgency."
                ),
                priority="normal",
            )
        )

    if patient.consciousness == "unknown":
        missing.append(
            MissingInformation(
                field="consciousness",
                reason=(
                    "Mental status is an important safety indicator."
                ),
                priority="high",
            )
        )
    return missing