from fastapi import FastAPI

from src.routes.file_route import  file_router
from src.routes.document_route import  document_router
from src.routes.search_route import search_router
from src.routes.rag_route import rag_router
from src.routes.project_route import project_router


app = FastAPI(
    title="Semantic Search API"
)

app.include_router(file_router)
app.include_router(document_router)
app.include_router(search_router)
app.include_router(rag_router)
app.include_router(project_router)