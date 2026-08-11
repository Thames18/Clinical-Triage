from datetime import datetime, timezone

from pydantic import BaseModel, Field


class TriageAuditRecord(BaseModel):
    assessment_id: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    model_name: str | None = None
    model_version: str | None = None
    prompt_version: str | None = None
    evidence_corpus_version: str | None = None

    ai_assisted: bool
    triage_level: str
    risk_score: int
    confidence: float

    red_flag_codes: list[str] = Field(default_factory=list)
    question_count: int = 0
    validation_issues: list[str] = Field(default_factory=list)
