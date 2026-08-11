import json
import os
from pathlib import Path

from app.evidence.embeddings import EmbeddingService
from app.evidence.loader import load_chunks, load_embeddings
from app.evidence.retriever import EvidenceRetriever
from app.evidence.schemas import RetrievedEvidence


class EvidenceUnavailable(RuntimeError):
    pass


class EvidenceService:
    def __init__(
        self,
        chunks_path: str | Path | None = None,
        embeddings_path: str | Path | None = None,
    ):
        base = Path(
            os.getenv(
                "EVIDENCE_DATA_DIR",
                str(Path(__file__).resolve().parents[3] / "data" / "evidence"),
            )
        )

        self.chunks_path = Path(
            chunks_path or base / "chunks.jsonl"
        )
        self.embeddings_path = Path(
            embeddings_path or base / "embeddings.json"
        )
        self.manifest_path = base / "manifest.json"

        self._embedding_service: EmbeddingService | None = None
        self._retriever: EvidenceRetriever | None = None

        self._load_index()

    def _load_index(self) -> None:
        chunks = load_chunks(self.chunks_path)
        embeddings = load_embeddings(self.embeddings_path)

        if not chunks or not embeddings:
            self._retriever = None
            return

        self._retriever = EvidenceRetriever(chunks, embeddings)

    @property
    def corpus_version(self) -> str | None:
        if not self.manifest_path.exists():
            return None

        try:
            with self.manifest_path.open("r", encoding="utf-8") as file:
                manifest = json.load(file)
            return manifest.get("corpus_version")
        except (OSError, json.JSONDecodeError):
            return None

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedEvidence]:
        if self._retriever is None:
            raise EvidenceUnavailable(
                "The evidence index is not available. "
                "Build a reviewed evidence corpus before enabling AI assessment."
            )

        if self._embedding_service is None:
            self._embedding_service = EmbeddingService()

        query_embedding = self._embedding_service.embed(query)

        return self._retriever.retrieve(
            query_embedding,
            top_k=top_k,
        )
