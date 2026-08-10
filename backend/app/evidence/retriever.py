import math
from app.evidence.schemas import (
    EvidenceChunk,
    RetrievedEvidence
)

def cosine_similarity(
    a: list[float],
    b: list[float]
) -> float:
    dot = sum(
        x * y
        for x, y in zip(a, b)
    )
    magnitude_a = math.sqrt(
        sum(x * x for x in a)
    )
    magnitude_b = math.sqrt(
        sum(x * x for x in b)
    )

    if (
        magnitude_a == 0
        or magnitude_b == 0
    ):
        return 0.0

    return (
        dot
        / (
            magnitude_a
            * magnitude_b
        )
    )

class EvidenceRetriever:
    def __init__(
        self,
        chunks: list[EvidenceChunk],
        embeddings: dict[str, list[float]],
    ):
        self.chunks = chunks
        self.embeddings = embeddings

    def retrieve(
        self,
        query_embedding: list[float],
        top_k: int = 5
    ) -> list[RetrievedEvidence]:

        scored = []
        for chunk in self.chunks:
            embedding = (
                self.embeddings.get(
                    chunk.chunk_id
                )
            )
            if embedding is None:
                continue
            score = cosine_similarity(
                query_embedding,
                embedding,
            )
            scored.append(
                (
                    score,
                    chunk,
                )
            )
        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            RetrievedEvidence(
                chunk_id=chunk.chunk_id,
                source_id=chunk.source_id,
                title=chunk.title,
                text=chunk.text,
                url=chunk.url,
                relevance_score=score,
                section=chunk.section,
            )

            for score, chunk
            in scored[:top_k]
        ]