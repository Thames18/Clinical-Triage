from typing import Literal

from pydantic import BaseModel, Field

from app.evidence.schemas import EvidenceCitation


class AIClinicalAssessment(BaseModel):
    summary: str
    clinical_concerns: list[str] = Field(default_factory=list)
    suggested_questions: list[str] = Field(default_factory=list)
    uncertainty_reasons: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    citations: list[EvidenceCitation] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


class FollowUpQuestion(BaseModel):
    field: str
    question: str
    priority: Literal["critical", "high", "normal"]
    reason: str
