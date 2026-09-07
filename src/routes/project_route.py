from fastapi import APIRouter, Path
from pydantic import BaseModel

from src.controllers.project_controller import ProjectController
from src.services.project_service import ProjectService

project_router = APIRouter(
prefix="/projects",
tags=["Projects"]
)

project_service = ProjectService()

project_controller = ProjectController(
project_service=project_service
)

class CreateProjectRequest(BaseModel):

    project_id: int
    project_name: str


@project_router.post("/")
def create_project(
request: CreateProjectRequest
):


    return project_controller.create_project(
        project_id=request.project_id,
        project_name=request.project_name
    )

@project_router.get("/")
def get_all_projects():
    return project_controller.get_all_projects()
    
@project_router.get("/{project_id}")
def get_project(project_id: int = Path(..., gt=0)):
    return project_controller.get_project(
        project_id=project_id
    )


@project_router.delete("/{project_id}")
def delete_project(
project_id: int = Path(..., gt=0)
):


    return project_controller.delete_project(
        project_id=project_id
    )

