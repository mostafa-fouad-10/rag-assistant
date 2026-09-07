from .VectorDBEnums import VectorDBEnums
from .VectorDBInterface import VectorDBInterface
from .providers.QdrantDBProvider import QdrantDBProvider


class VectorDBFactory:

    @staticmethod
    def create(
        provider: VectorDBEnums,
        host: str = "localhost",
        port: int = 6333
    ) -> VectorDBInterface:

        if provider == VectorDBEnums.QDRANT:
            return QdrantDBProvider(
                host=host,
                port=port
            )

        raise ValueError(f"Unsupported vector database provider: {provider}")