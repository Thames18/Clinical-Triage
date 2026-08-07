from app.schemas.triage import PatientInput

def generate_follow_up_questions(
    patient: PatientInput ) -> list[dict]:

    questions = []

    if patient.symptom_duration_hours is None:
        questions.append(
            {
                "field": "symptom_duration_hours",
                "question": (
                    "How long have the symptoms been present ?"
                ),
                "priority": "high",
            }
        )

    if patient.respiratory_rate is None:
        questions.append(
            {
                "field": "respiratory_rate",
                "question": (
                    "What is the patient's respiratory rate per minute ?"
                ),
                "priority": "high",
            }
        )


    if patient.consciousness == "unknown":
        questions.append(
            {
                "field": "consciousness",
                "question": (
                    "Is the patient fully alert and responding normally?"
                ),
                "priority": "high",
            }
        )

    return questions