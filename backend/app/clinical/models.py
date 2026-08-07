from pydantic import BaseModel
from typing import Literal

class RedFlag(BaseModel):
    code: str
    severity: Literal["critical", "high", "moderate"]
    title: str
    explanation: str
    evidence: str

class MissingInformation(BaseModel):
    field: str
    reason: str
    priority: Literal["critical", "high", "normal"]

class ClinicalAssessment(BaseModel):
    red_flags: list[RedFlag]
    missing_information: list[MissingInformation]