from typing import Literal
from pydantic import BaseModel, Field

TriageLevel = Literal[
    "EMERGENCY",
    "URGENT",
    "SAME_DAY",
    "ROUTINE",
    "SELF_CARE",
    "INSUFFICIENT_INFORMATION"
]

class BenchmarkCase(BaseModel):
    case_id: str
    description: str
    patient: dict
    expected_triage: TriageLevel
    emergency: bool = False
    expected_red_flags: list[str] = Field(
        default_factory=list
    )
    rationale: str
    tags: list[str] = Field(
        default_factory=list
    )

class EvaluationResult(BaseModel):
    case_id: str
    expected_triage: TriageLevel
    predicted_triage: TriageLevel
    correct: bool
    expected_emergency: bool
    predicted_emergency: bool
    false_negative: bool
    false_positive: bool
    risk_score: int
    confidence: float

class BenchmarkReport(BaseModel):
    total_cases: int
    correct: int
    accuracy: float
    emergency_sensitivity: float
    emergency_specificity: float
    false_negatives: int
    false_positives: int
    results: list[EvaluationResult]