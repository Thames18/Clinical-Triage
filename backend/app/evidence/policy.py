MIN_RELEVANCE_SCORE = 0.45
MIN_RELEVANT_CHUNKS = 1


def sufficient_evidence(evidence) -> bool:
    relevant = [
        item
        for item in evidence
        if item.relevance_score >= MIN_RELEVANCE_SCORE
    ]
    return len(relevant) >= MIN_RELEVANT_CHUNKS
