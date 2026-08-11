from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict

from app.ai.schemas import FollowUpQuestion
from app.clinical.models import MissingInformation, RedFlag
from app.evidence.schemas import EvidenceCitation

Sex = Literal["male", "female"]
Consciousness = Literal[
    "alert",
    "confused",
    "drowsy",
    "unresponsive",
    "unknown",
]
TriageLevel = Literal[
    "EMERGENCY",
    "URGENT",
    "SAME_DAY",
    "ROUTINE",
    "SELF_CARE",
    "INSUFFICIENT_INFORMATION",
    "ASSESSMENT_UNAVAILABLE",
]


class PatientInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    age: int = Field(ge=0, le=130)
    sex: Sex

    temperature_c: float | None = Field(default=None, ge=25, le=45)
    heart_rate: int | None = Field(default=None, ge=20, le=250)
    respiratory_rate: int | None = Field(default=None, ge=4, le=80)
    systolic_bp: int | None = Field(default=None, ge=40, le=260)
    diastolic_bp: int | None = Field(default=None, ge=20, le=160)
    oxygen_saturation: float | None = Field(default=None, ge=50, le=100)

    consciousness: Consciousness = "unknown"

    symptoms: list[str] = Field(default_factory=list, max_length=50)
    symptom_duration_hours: float | None = Field(default=None, ge=0, le=8760)

    medical_history: list[str] = Field(default_factory=list, max_length=100)
    medications: list[str] = Field(default_factory=list, max_length=100)
    allergies: list[str] = Field(default_factory=list, max_length=100)


class TriageResponse(BaseModel):
    assessment_id: UUID = Field(default_factory=uuid4)
    created_at: str | None = None

    triage_level: TriageLevel
    summary: str
    red_flags: list[RedFlag] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)

    missing_information: list[MissingInformation] = Field(default_factory=list)
    follow_up_questions: list[FollowUpQuestion] = Field(default_factory=list)

    confidence: float = Field(ge=0, le=1)
    risk_score: int = Field(ge=0)

    ai_assisted: bool = False

    evidence_citations: list[EvidenceCitation] = Field(default_factory=list)
    evidence_corpus_version: str | None = None
    model_name: str | None = None
    model_version: str | None = None
    prompt_version: str | None = None

    validation_issues: list[str] = Field(default_factory=list)
