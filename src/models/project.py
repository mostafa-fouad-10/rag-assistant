from pydantic import BaseModel

class Project(BaseModel):
    project_id: int
    path: str
    project_name: str