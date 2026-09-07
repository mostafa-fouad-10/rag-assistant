from qdrant_client import models, QdrantClient
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums
import logging
from typing import List
from src.models.data_chunk import RetrievedDocument

class QdrantDBProvider(VectorDBInterface):

    def __init__(self, host: str = "localhost", port: int = 6333):
        self.host = host
        self.port = port
        self.client = None

        self.logger = logging.getLogger(__name__)

    def connect(self):
        try:
            self.client = QdrantClient(host=self.host, port=self.port)
            self.logger.info("Connected to Qdrant at %s:%d", self.host, self.port)
        except Exception as e:
            self.logger.error("Failed to connect to Qdrant: %s", str(e))
            raise    


    def disconnect(self):
        self.client = None
        self.logger.info("Disconnected from Qdrant")        


    def is_collection_existed(self, collection_name: str) -> bool:
        try:
            return self.client.collection_exists(collection_name)
        except Exception as e:
            self.logger.error("Error checking collection existence: %s", str(e))
            raise    

    
    def list_all_collections(self) -> List:
        try:
            return self.client.get_collections().collections
        except Exception as e:
            self.logger.error("Error listing collections: %s", str(e))
            raise        

    
    def get_collection_info(self, collection_name: str) -> dict:
        try:
            return self.client.get_collection(collection_name).dict()
        except Exception as e:
            self.logger.error("Error getting collection info: %s", str(e))
            raise        


    def delete_collection(self, collection_name: str):
        try:
            self.client.delete_collection(collection_name)
            self.logger.info("Collection '%s' deleted successfully", collection_name)
        except Exception as e:
            self.logger.error("Error deleting collection: %s", str(e))
            raise        


    def create_collection(
    self,
    collection_name: str,
    embedding_size: int,
    do_reset: bool = False,
    distance_method: DistanceMethodEnums = DistanceMethodEnums.COSINE
):
        try:
            if do_reset and self.is_collection_existed(collection_name):
                self.delete_collection(collection_name)

            if not self.is_collection_existed(collection_name):
                distance = models.Distance[distance_method.name]

                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(
                        size=embedding_size,
                        distance=distance
                    )
                )

                self.logger.info(
                    "Collection '%s' created successfully",
                    collection_name
                )
            else:
                self.logger.info(
                    "Collection '%s' already exists",
                    collection_name
                )

        except Exception as e:
            self.logger.error("Error creating collection: %s", str(e))
            raise


    def insert_one(
        self,
        collection_name: str,
        text: str,
        vector: list,
        metadata: dict = None,
        record_id: str = None
    ):
        try:
            payload = {"text": text}
            if metadata:
                payload.update(metadata)

            self.client.upsert(
                collection_name=collection_name,
                points=[
                    models.PointStruct(
                        id=record_id,
                        vector=vector,
                        payload=payload
                    )
                ]
            )

            self.logger.info(
                "Inserted one record into collection '%s'",
                collection_name
            )
        except Exception as e:
            self.logger.error("Error inserting one record: %s", str(e))
            raise        


    def insert_many(
        self,
        collection_name: str,
        texts: list,
        vectors: list,
        metadata: list = None,
        record_ids: list = None,
        batch_size: int = 50
    ):
        try:
            points = []
            for i in range(len(texts)):
                payload = {"text": texts[i]}
                if metadata and i < len(metadata):
                    payload.update(metadata[i])

                point_id = record_ids[i] if record_ids and i < len(record_ids) else None

                points.append(
                    models.PointStruct(
                        id=point_id,
                        vector=vectors[i],
                        payload=payload
                    )
                )

            for i in range(0, len(points), batch_size):
                batch_points = points[i:i + batch_size]
                self.client.upsert(
                    collection_name=collection_name,
                    points=batch_points
                )

            self.logger.info(
                "Inserted %d records into collection '%s'",
                len(points),
                collection_name
            )
        except Exception as e:
            self.logger.error("Error inserting many records: %s", str(e))
            raise        


    def search_by_vector(
    self,
    collection_name: str,
    vector: list,
    limit: int,
    file_id: str = None
) -> List[RetrievedDocument]:
        try:

            query_filter = None

            if file_id:
                query_filter = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="file_id",
                            match=models.MatchValue(
                                value=file_id
                            )
                        )
                    ]
                )

            search_result = self.client.query_points(
                collection_name=collection_name,
                query=vector,
                query_filter=query_filter,
                limit=limit
            ).points

            retrieved_documents = [
                RetrievedDocument(
                    text=point.payload.get("text", ""),
                    score=point.score
                )
                for point in search_result
            ]

            return retrieved_documents

        except Exception as e:
            self.logger.error(
                "Error searching by vector: %s",
                str(e)
            )
            raise