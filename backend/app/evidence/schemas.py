from typing import Literal

from pydantic import BaseModel, Field

EvidenceSourceType = Literal[
    "guideline",
    "government",
    "peer_reviewed",
    "institutional",
]


class EvidenceSource(BaseModel):
    source_id: str
    title: str
    organization: str
    source_type: EvidenceSourceType
    url: str
    publication_date: str | None = None
    version: str | None = None
    retrieved_at: str | None = None
    content_sha256: str | None = None
    status: Literal["active", "retired"] = "active"


class EvidenceChunk(BaseModel):
    chunk_id: str
    source_id: str
    title: str
    text: str
    url: str
    section: str | None = None
    metadata: dict = Field(default_factory=dict)


class RetrievedEvidence(BaseModel):
    chunk_id: str
    source_id: str
    title: str
    text: str
    url: str
    relevance_score: float
    section: str | None = None


class EvidenceCitation(BaseModel):
    citation_id: str
    source_id: str
    chunk_id: str
    claim: str
    supporting_text: str
    url: str


class EvidenceAssessment(BaseModel):
    citations: list[EvidenceCitation] = Field(default_factory=list)
    evidence_summary: str
    evidence_confidence: float = Field(ge=0, le=1)
