from app.ai.schemas import FollowUpQuestion
from app.schemas.triage import PatientInput


def build_follow_up_questions(
    patient: PatientInput ) -> list[FollowUpQuestion]:
    questions: list[FollowUpQuestion] = []

    if patient.symptom_duration_hours is None:
        questions.append(
            FollowUpQuestion(
                field="symptom_duration_hours",
                question=(
                    "When did the symptoms begin?"
                ),
                priority="high",
                reason=(
                    "Symptom duration can materially affect urgency."
                )
            )
        )

    if patient.respiratory_rate is None:
        questions.append(
            FollowUpQuestion(
                field="respiratory_rate",
                question=(
                    "What is the patient's respiratory rate per minute?"
                ),
                priority="high",
                reason=(
                    "Respiratory rate helps assess respiratory severity."
                )
            )
        )

    if patient.consciousness == "unknown":
        questions.append(
            FollowUpQuestion(
                field="consciousness",
                question=(
                    "Is the patient fully alert and responding normally?"
                ),
                priority="high",
                reason=(
                    "Mental status is an important safety indicator."
                )
            )
        )

    return questions