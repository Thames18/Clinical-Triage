from app.evidence.schemas import (
    RetrievedEvidence
)

MIN_RELEVANCE_SCORE = 0.45

def sufficient_evidence(
    evidence: list[RetrievedEvidence]
) -> bool:

    relevant = [
        item
        for item in evidence
        if item.relevance_score
        >= MIN_RELEVANCE_SCORE
    ]

    return len(relevant) > 0