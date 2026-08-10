import hashlib
from app.evidence.schemas import (
    EvidenceChunk
)

def _chunk_id(
    source_id: str,
    index: int
) -> str:
    value = (
        f"{source_id}:{index}"
    )
    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()[:16]

def chunk_document(
    source_id: str,
    title: str,
    url: str,
    text: str,
    section: str | None = None,
    chunk_size: int = 1200
) -> list[EvidenceChunk]:

    words = text.split()
    chunks: list[
        EvidenceChunk
    ] = []
    for index in range(
        0,
        len(words),
        chunk_size,
    ):
        chunk_words = words[
            index:index + chunk_size
        ]
        chunk_text = " ".join(
            chunk_words
        )
        chunks.append(
            EvidenceChunk(
                chunk_id=_chunk_id(
                    source_id,
                    index,
                ),
                source_id=source_id,
                title=title,
                text=chunk_text,
                url=url,
                section=section,
            )
        )
    return chunks