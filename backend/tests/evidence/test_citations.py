from app.ai.schemas import (
    AIClinicalAssessment
)

from app.evidence.citations import (
    validate_citations
)

from app.evidence.schemas import (
    EvidenceCitation,
    RetrievedEvidence
)

def make_evidence():
    return [
        RetrievedEvidence(
            chunk_id="chunk-1",
            source_id="source-1",
            title="Example",
            text="Example evidence.",
            url="https://example.com",
            relevance_score=0.9,
        )
    ]

def test_valid_citation():
    assessment = AIClinicalAssessment(
        summary="Assessment.",
        citations=[
            EvidenceCitation(
                citation_id="citation-1",
                source_id="source-1",
                chunk_id="chunk-1",
                claim="Example claim.",
                supporting_text=(
                    "Example evidence."
                ),
                url="https://example.com",
            )
        ],
        confidence=0.8,
    )

    issues = validate_citations(
        assessment,
        make_evidence(),
    )

    assert issues == []

def test_unknown_citation_fails():

    assessment = AIClinicalAssessment(
        summary="Assessment.",
        citations=[
            EvidenceCitation(
                citation_id="citation-1",
                source_id="source-999",
                chunk_id="chunk-999",
                claim="Unsupported claim.",
                supporting_text="Fake evidence.",
                url="https://example.com",
            )
        ],
        confidence=0.8,
    )

    issues = validate_citations(
        assessment,
        make_evidence(),
    )

    assert len(issues) > 0