from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.services.rag_service import RAGService


rag_router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)

rag_service = RAGService()


class RAGRequest(BaseModel):
    query: str
    file_id: str


@rag_router.post("/")
def generate_answer(request: RAGRequest):

    try:
        answer = rag_service.answer(
            query=request.query,
            file_id=request.file_id
        )

        return {
            "success": True,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )