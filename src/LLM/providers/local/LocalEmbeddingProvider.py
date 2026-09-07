import logging
from sentence_transformers import SentenceTransformer
from src.LLM.LLMInterface import EmbeddingInterface



class LocalEmbeddingProvider(EmbeddingInterface):

    def __init__(self):
        self.embedding_model = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.logger = logging.getLogger(__name__)

    def set_embedding_model(self, model_id: str, embedding_size: int):
        try:
            self.embedding_model = SentenceTransformer(model_id)
            self.embedding_model_id = model_id
            self.embedding_size = embedding_size

            self.logger.info(
                "Embedding model '%s' loaded successfully",
                model_id
            )

        except Exception:
            self.logger.exception(
                "Failed to load embedding model '%s'",
                model_id
            )

    def embed_text(self, text: str, document_type: str = None):
        if self.embedding_model is None:
            self.logger.error("Embedding model is not initialized")
            return None

        try:
            return self.embedding_model.encode(text).tolist()

        except Exception:
            self.logger.exception("Failed to generate embedding")
            return None






