from src.models.data_chunk import DataChunk
from src.LLM.LLMFactory import LLMFactory
from src.LLM.LLMEnums import LLMProvider
from src.stores.vectordb.VectorDBFactory import VectorDBFactory
from src.stores.vectordb.VectorDBEnums import VectorDBEnums


class VectorStoreService:

    def __init__(self):
        self.vector_db = VectorDBFactory.create(
            VectorDBEnums.QDRANT
        )
        self.vector_db.connect()
        
        if not self.vector_db.is_collection_existed("documents"):
            self.vector_db.create_collection(
                collection_name="documents",
                embedding_size=384
            )

        self.embedding_provider = LLMFactory.create_embedding_provider(
            LLMProvider.LOCAL.value
        )
        self.embedding_provider.set_embedding_model(
                model_id="all-MiniLM-L6-v2",
                embedding_size=384
            )

    def store_chunks(self, chunks: list[DataChunk]):
        if not chunks:
            return
        texts = []
        vectors = []
        metadata = []
        record_ids = []

        for chunk in chunks:
            vector = self.embedding_provider.embed_text(chunk.text)

            if vector is None:
                continue

            texts.append(chunk.text)
            vectors.append(vector)

            metadata.append({
                "file_id": chunk.file_id,
                "project_id": chunk.project_id,
                "chunk_index": chunk.chunk_index
            })

            record_ids.append(chunk.chunk_id)
        
        self.vector_db.insert_many(
            collection_name="documents",
            texts=texts,
            vectors=vectors,
            metadata=metadata,
            record_ids=record_ids
        )

    
    def store_chunk(self, chunk: DataChunk):
        vector = self.embedding_provider.embed_text(chunk.text)

        if vector is None:
            return

        metadata = {
            "file_id": chunk.file_id,
            "project_id": chunk.project_id,
            "chunk_index": chunk.chunk_index
        }

        self.vector_db.insert_one(
            collection_name="documents",
            text=chunk.text,
            vector=vector,
            metadata=metadata,
            record_id=chunk.chunk_id
        )    