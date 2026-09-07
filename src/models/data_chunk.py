from pydantic import BaseModel

class DataChunk(BaseModel):
    chunk_id:str
    file_id:str
    project_id:int
    chunk_index:int
    text:str

class RetrievedDocument(BaseModel):
    text: str
    score: float    