from typing import List

from src.LLM.LLMFactory import LLMFactory
from src.LLM.LLMEnums import LLMProvider
from src.stores.vectordb.VectorDBFactory import VectorDBFactory
from src.stores.vectordb.VectorDBEnums import VectorDBEnums
from src.models.data_chunk import RetrievedDocument


class SearchService:

    def __init__(self):
        self.vector_db = VectorDBFactory.create(
            VectorDBEnums.QDRANT
        )
        self.vector_db.connect()

        self.embedding_provider = LLMFactory.create_embedding_provider(
            LLMProvider.LOCAL.value
        )
        self.embedding_provider.set_embedding_model(
                model_id="all-MiniLM-L6-v2",
                embedding_size=384
            )

    def search_by_vector(
    self,
    collection_name: str,
    query: str,
    limit: int = 5,
    file_id: str = None
) -> List[RetrievedDocument]:

        query_vector = self.embedding_provider.embed_text(query)

        if query_vector is None:
            return []

        return self.vector_db.search_by_vector(
            collection_name=collection_name,
            vector=query_vector,
            limit=limit,
            file_id=file_id
        )