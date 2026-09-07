from fastapi import APIRouter
from src.controllers.document_controller import DocumentController
from src.services.file_service import FileService
from src.services.document_service import DocumentService
from src.helpers.config import get_settings
from src.services.vector_store_service import VectorStoreService

document_router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

file_service = FileService(config=get_settings())
document_service = DocumentService()
vector_store_service = VectorStoreService()  

@document_router.post("/process/{project_id}/{file_id}")
def process_document(project_id:int,file_id:str):
    document_controller=DocumentController(file_service,document_service,vector_store_service)

    return document_controller.process_document(project_id,file_id)
