from app.evidence.retriever import (
    EvidenceRetriever
)

from app.evidence.schemas import (
    EvidenceChunk
)

def test_retriever_returns_most_similar():
    chunks = [
        EvidenceChunk(
            chunk_id="one",
            source_id="source",
            title="Respiratory",
            text="Respiratory evidence.",
            url="https://example.com",
        ),
        EvidenceChunk(
            chunk_id="two",
            source_id="source",
            title="Cardiac",
            text="Cardiac evidence.",
            url="https://example.com",
        ),
    ]

    embeddings = {
        "one": [1.0, 0.0],
        "two": [0.0, 1.0],
    }

    retriever = EvidenceRetriever(
        chunks,
        embeddings,
    )

    results = retriever.retrieve(
        [1.0, 0.0],
        top_k=1,
    )

    assert len(results) == 1

    assert (
        results[0].chunk_id
        == "one"
    )