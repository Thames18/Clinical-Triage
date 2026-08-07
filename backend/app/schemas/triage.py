from pydantic import BaseModel, Field
from typing import Literal, Optional


class PatientInput(BaseModel):

    age: int = Field(
        ge=0,
        le=120
    )

    sex: Literal[
        "male",
        "female",
        "other",
        "unknown"
    ] = "unknown"


    temperature_c: Optional[float] = Field(
        default=None,
        ge=30,
        le=45
    )


    heart_rate: Optional[int] = Field(
        default=None,
        ge=20,
        le=250
    )


    respiratory_rate: Optional[int] = Field(
        default=None,
        ge=5,
        le=80
    )


    systolic_bp: Optional[int] = Field(
        default=None,
        ge=40,
        le=250
    )


    diastolic_bp: Optional[int] = Field(
        default=None,
        ge=20,
        le=150
    )


    oxygen_saturation: Optional[int] = Field(
        default=None,
        ge=50,
        le=100
    )


    consciousness: Literal[
        "alert",
        "confused",
        "drowsy",
        "unresponsive",
        "unknown"
    ] = "unknown"


    symptoms: list[str]


    symptom_duration_hours: Optional[int] = None


    medical_history: list[str] = []

    medications: list[str] = []

    allergies: list[str] = []



class TriageResponse(BaseModel):

    triage_level: Literal[
        "EMERGENCY",
        "URGENT",
        "SAME_DAY",
        "ROUTINE",
        "SELF_CARE",
        "INSUFFICIENT_INFORMATION"
    ]


    summary: str

    red_flags: list[str]

    recommendations: list[str]

    missing_information: list[str]

    confidence: float