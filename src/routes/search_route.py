from fastapi import APIRouter
from pydantic import BaseModel

from src.services.search_service import SearchService

search_router = APIRouter(
    prefix="/search",
    tags=["Search"]
)

search_service = SearchService()


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


@search_router.post("/")
def search(request: SearchRequest):

    results = search_service.search_by_vector(
        collection_name="documents",
        query=request.query,
        limit=request.limit
    )

    return {
        "success": True,
        "results": [
            {
                "text": result.text,
                "score": result.score
            }
            for result in results
        ]
    }