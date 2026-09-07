from src.stores.vectordb.VectorDBFactory import VectorDBFactory
from src.stores.vectordb.VectorDBEnums import VectorDBEnums


class CollectionService:

    def __init__(self):
        self.vector_db = VectorDBFactory.create(
            VectorDBEnums.QDRANT
        )
        self.vector_db.connect()

    def create_collection(
        self,
        collection_name: str,
        embedding_size: int,
        do_reset: bool = False
    ):
        self.vector_db.create_collection(
            collection_name=collection_name,
            embedding_size=embedding_size,
            do_reset=do_reset
        )

    def delete_collection(self, collection_name: str):
        self.vector_db.delete_collection(
            collection_name=collection_name
        )

    def collection_exists(self, collection_name: str) -> bool:
        return self.vector_db.is_collection_existed(
            collection_name
        )

    def list_collections(self):
        return self.vector_db.list_all_collections()

    def get_collection_info(self, collection_name: str):
        return self.vector_db.get_collection_info(
            collection_name
        )