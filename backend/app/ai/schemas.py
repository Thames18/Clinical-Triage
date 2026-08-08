from typing import Literal
from pydantic import BaseModel, Field

class AIClinicalAssessment(BaseModel):
    summary: str
    clinical_concerns: list[str] = Field(
        default_factory=list
    )
    suggested_questions: list[str] = Field(
        default_factory=list
    )
    uncertainty_reasons: list[str] = Field(
        default_factory=list
    )
    confidence: float = Field(
        ge=0,
        le=1,
    )

class FollowUpQuestion(BaseModel):
    field: str
    question: str
    priority: Literal[
        "critical",
        "high",
        "normal"
    ]
    reason: str