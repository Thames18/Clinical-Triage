import hashlib
import re

from app.evidence.schemas import EvidenceChunk


def _chunk_id(source_id: str, text: str, index: int) -> str:
    digest = hashlib.sha256(
        f"{source_id}:{index}:{text}".encode("utf-8")
    ).hexdigest()
    return digest[:16]


def chunk_document(
    source_id: str,
    title: str,
    url: str,
    text: str,
    section: str | None = None,
    chunk_size: int = 1200,
    overlap: int = 150,
) -> list[EvidenceChunk]:
    words = text.split()
    if not words:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[EvidenceChunk] = []
    start = 0
    index = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_text = " ".join(words[start:end]).strip()

        chunks.append(
            EvidenceChunk(
                chunk_id=_chunk_id(source_id, chunk_text, index),
                source_id=source_id,
                title=title,
                text=chunk_text,
                url=url,
                section=section,
                metadata={
                    "start_word": start,
                    "end_word": end,
                },
            )
        )

        if end == len(words):
            break

        start = end - overlap
        index += 1

    return chunks


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
