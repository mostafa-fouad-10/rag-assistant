from src.services.file_service import FileService
from src.services.document_service import DocumentService
from fastapi.responses import JSONResponse


class DocumentController:

    def __init__(self, file_service, document_service, vector_store_service):
        self.file_service = file_service
        self.document_service = document_service
        self.vector_store_service = vector_store_service

    def process_document(self, project_id, file_id):
        file = self.file_service.get_file(project_id, file_id)

        if file is None:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "message": "File not found"
                }
            )

        chunks = self.document_service.process_file(file)
        self.vector_store_service.store_chunks(chunks)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Document processed successfully",
                "chunks": [chunk.model_dump() for chunk in chunks]
            }
        )
