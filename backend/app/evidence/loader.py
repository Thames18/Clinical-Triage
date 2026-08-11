import json
from pathlib import Path

from app.evidence.schemas import EvidenceChunk, EvidenceSource


def load_sources(path: str | Path) -> list[EvidenceSource]:
    source_path = Path(path)
    with source_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return [EvidenceSource(**source) for source in data]


def load_chunks(path: str | Path) -> list[EvidenceChunk]:
    chunk_path = Path(path)
    if not chunk_path.exists():
        return []

    chunks: list[EvidenceChunk] = []
    with chunk_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                chunks.append(EvidenceChunk(**json.loads(line)))
    return chunks


def load_embeddings(path: str | Path) -> dict[str, list[float]]:
    embedding_path = Path(path)
    if not embedding_path.exists():
        return {}

    with embedding_path.open("r", encoding="utf-8") as file:
        raw = json.load(file)

    return {
        str(chunk_id): [float(value) for value in vector]
        for chunk_id, vector in raw.items()
    }
