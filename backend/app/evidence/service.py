from app.evidence.embeddings import (
    EmbeddingService
)

from app.evidence.retriever import (
    EvidenceRetriever
)

from app.evidence.schemas import (
    RetrievedEvidence
)


class EvidenceService:
    def __init__(
        self,
        retriever: EvidenceRetriever
    ):

        self.retriever = retriever
        self.embeddings = (
            EmbeddingService()
        )

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> list[RetrievedEvidence]:

        query_embedding = (
            self.embeddings.embed(
                query
            )
        )
        return self.retriever.retrieve(
            query_embedding,
            top_k=top_k,
        )