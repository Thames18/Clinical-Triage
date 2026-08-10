from app.ai.schemas import (
    AIClinicalAssessment
)
from app.evidence.schemas import (
    RetrievedEvidence
)

def validate_citations(
    assessment: AIClinicalAssessment,
    evidence: list[RetrievedEvidence]
) -> list[str]:

    issues: list[str] = []
    valid_chunks = {
        item.chunk_id
        for item in evidence
    }
    valid_sources = {
        item.source_id
        for item in evidence
    }

    for citation in assessment.citations:

        if (
            citation.chunk_id
            not in valid_chunks
        ):
            issues.append(
                "Citation references "
                "unretrieved evidence."
            )

        if (
            citation.source_id
            not in valid_sources
        ):

            issues.append(
                "Citation references "
                "an unavailable source."
            )

        if not citation.claim.strip():
            issues.append(
                "Citation contains "
                "an empty claim."
            )


        if not citation.supporting_text.strip():

            issues.append(
                "Citation contains "
                "no supporting text."
            )

    return issues