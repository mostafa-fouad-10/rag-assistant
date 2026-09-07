from fastapi.responses import JSONResponse

from src.services.project_service import ProjectService


class ProjectController:

    def __init__(self, project_service: ProjectService):
        self.project_service = project_service

    def create_project(self, project_id: int, project_name: str):

        project = self.project_service.get_or_create_project(
            project_id=project_id,
            project_name=project_name
        )

        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "message": "Project created successfully",
                "project": project.model_dump()
            }
        )

    def get_project(self, project_id: int):

        project = self.project_service.get_project(
            project_id=project_id
        )

        if project is None:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "message": "Project not found"
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "project": project.model_dump()
            }
        )

    def delete_project(self, project_id: int):

        deleted = self.project_service.delete_project(
            project_id=project_id
        )

        if not deleted:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "message": "Project not found"
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Project deleted successfully"
            }
        )


    def get_all_projects(self):

        projects = self.project_service.get_all_projects()

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "projects": [
                    project.model_dump()
                    for project in projects
                ]
            }
        )    