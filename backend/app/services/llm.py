import json
from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def analyze_patient(patient):

    prompt = f"""You are a clinical triage assistant.

Analyze the patient information.

Return ONLY JSON.

Patient:

Age:
{patient.age}

Temperature:
{patient.temperature}

Heart rate:
{patient.heart_rate}

Blood pressure:
{patient.blood_pressure}

Oxygen:
{patient.oxygen_level}

Symptoms:
{patient.symptoms}


Return:

{{
"risk_level":"",
"summary":"",
"red_flags":[],
"recommendations":[]
}}
"""


    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[
            {
                "role":"system",
                "content":
                "You provide structured clinical triage assistance."
            },
            {
                "role":"user",
                "content":prompt
            }
        ],

        response_format={
            "type":"json_object"
        }
    )


    return json.loads(
        response.choices[0].message.content
    )