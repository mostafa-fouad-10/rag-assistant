from pathlib import Path
import shutil
import json

from src.models.project import Project
from src.helpers.config import get_settings


class ProjectService:

    def get_or_create_project(
        self,
        project_id: int,
        project_name: str
    ) -> Project:

        settings = get_settings()

        path = Path(settings.DATA_PATH) / str(project_id)
        path.mkdir(parents=True, exist_ok=True)

        metadata_path = path / "project.json"

        # Project already exists
        if metadata_path.exists():

            with open(metadata_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            return Project(
                project_id=data["project_id"],
                project_name=data["project_name"],
                path=str(path)
            )

        # Create new project metadata
        data = {
            "project_id": project_id,
            "project_name": project_name
        }

        with open(metadata_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return Project(
            project_id=project_id,
            project_name=project_name,
            path=str(path)
        )

    def get_project(self, project_id: int) -> Project | None:

        settings = get_settings()

        path = Path(settings.DATA_PATH) / str(project_id)
        metadata_path = path / "project.json"

        if not metadata_path.exists():
            return None

        with open(metadata_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return Project(
            project_id=data["project_id"],
            project_name=data["project_name"],
            path=str(path)
        )

    def delete_project(self, project_id: int) -> bool:

        settings = get_settings()

        path = Path(settings.DATA_PATH) / str(project_id)

        if not path.exists():
            return False

        shutil.rmtree(str(path))

        return True


    def get_all_projects(self) -> list[Project]:

        settings = get_settings()

        data_path = Path(settings.DATA_PATH)

        projects = []

        if not data_path.exists():
            return projects

        for project_path in data_path.iterdir():

            if not project_path.is_dir():
                continue

            metadata_path = project_path / "project.json"

            if not metadata_path.exists():
                continue

            with open(metadata_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            projects.append(
                Project(
                    project_id=data["project_id"],
                    project_name=data["project_name"],
                    path=str(project_path)
                )
            )

        return projects    