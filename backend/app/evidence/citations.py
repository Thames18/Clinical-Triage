import re

from app.ai.schemas import AIClinicalAssessment
from app.evidence.schemas import RetrievedEvidence


def _normalize(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) > 2
    }


def citation_supported(
    citation,
    evidence: RetrievedEvidence,
    min_overlap: float = 0.05,
) -> bool:
    claim_terms = _normalize(citation.claim)
    support_terms = _normalize(citation.supporting_text)
    evidence_terms = _normalize(evidence.text)

    if not claim_terms:
        return False

    if not support_terms:
        return False

    # The quoted supporting text must be materially present in the retrieved chunk.
    support_overlap = len(support_terms & evidence_terms) / len(support_terms)
    if support_overlap < 0.80:
        return False

    # The claim should share at least a small amount of vocabulary with the
    # supplied support. This is a lightweight guard, not a clinical entailment model.
    claim_overlap = len(claim_terms & support_terms) / len(claim_terms)
    return claim_overlap >= min_overlap


def validate_citations(
    assessment: AIClinicalAssessment,
    evidence: list[RetrievedEvidence],
) -> list[str]:
    issues: list[str] = []

    by_chunk = {item.chunk_id: item for item in evidence}
    valid_sources = {item.source_id for item in evidence}

    for citation in assessment.citations:
        evidence_item = by_chunk.get(citation.chunk_id)

        if evidence_item is None:
            issues.append(
                f"Citation {citation.citation_id} references unretrieved evidence."
            )
            continue

        if citation.source_id not in valid_sources:
            issues.append(
                f"Citation {citation.citation_id} references an unavailable source."
            )

        if citation.source_id != evidence_item.source_id:
            issues.append(
                f"Citation {citation.citation_id} source does not match its chunk."
            )

        if citation.url != evidence_item.url:
            issues.append(
                f"Citation {citation.citation_id} URL does not match its chunk."
            )

        if not citation.claim.strip():
            issues.append(
                f"Citation {citation.citation_id} contains an empty claim."
            )

        if not citation.supporting_text.strip():
            issues.append(
                f"Citation {citation.citation_id} contains no supporting text."
            )

        if evidence_item and not citation_supported(citation, evidence_item):
            issues.append(
                f"Citation {citation.citation_id} could not be validated against "
                "the retrieved supporting text."
            )

    return issues
