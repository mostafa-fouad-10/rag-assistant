from fastapi import UploadFile
from src.helpers.config import Settings
from src.models.enums import ResponseSignal
from pathlib import Path
from src.helpers.id_generator import generate_id
from src.models.file import File
from src.services.project_service import ProjectService
import shutil
import json

from pypdf import PdfReader
import docx


class FileService:

    FILE_ALLOWED_EXTENSIONS = {
        ".txt",
        ".pdf",
        ".docx",
    }

    def __init__(self, config: Settings):
        self.config = config

    # =========================================================
    # Validate Uploaded File
    # =========================================================

    async def validate_uploaded_file(self, file: UploadFile):

        extension = Path(file.filename).suffix.lower()

        if extension not in self.FILE_ALLOWED_EXTENSIONS:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if not self.validate_file_size(file):
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        if extension == ".pdf":

            if not self.validate_pdf(file):
                return False, ResponseSignal.FILE_INVALID_PDF.value

        elif extension == ".docx":

            if not self.validate_docx(file):
                return False, ResponseSignal.FILE_INVALID_DOCX.value

        elif extension == ".txt":

            if not self.validate_txt(file):
                return False, ResponseSignal.FILE_INVALID_TXT.value

        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value

    # =========================================================
    # Save File
    # =========================================================

    async def save_file(
        self,
        file: UploadFile,
        project_id: int
    ):

        project_service = ProjectService()

        project = project_service.get_project(
            project_id=project_id
        )

        if project is None:
            raise ValueError("Project not found")

        extension = Path(file.filename).suffix.lower()

        file_id = generate_id()

        file_dir = Path(project.path) / file_id

        file_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = file_dir / (
            file_id + extension
        )

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # =====================================================
        # Save File Metadata
        # =====================================================

        metadata = {
            "file_id": file_id,
            "file_name": file.filename,
            "project_id": project_id
        }

        metadata_path = file_dir / "file.json"

        with open(
            metadata_path,
            "w",
            encoding="utf-8"
        ) as metadata_file:

            json.dump(
                metadata,
                metadata_file,
                ensure_ascii=False,
                indent=4
            )

        return File(
            file_id=file_id,
            file_name=file.filename,
            project_id=project_id,
            path=str(file_path)
        )

    # =========================================================
    # Delete File
    # =========================================================

    def delete_file(
        self,
        project_id: int,
        file_id: str
    ) -> bool:

        project = ProjectService().get_project(
            project_id=project_id
        )

        if project is None:
            return False

        file_dir = Path(project.path) / file_id

        if not file_dir.exists():
            return False

        shutil.rmtree(file_dir)

        return True

    # =========================================================
    # Get One File
    # =========================================================

    def get_file(
        self,
        project_id: int,
        file_id: str
    ) -> File | None:

        project = ProjectService().get_project(
            project_id=project_id
        )

        if project is None:
            return None

        file_dir = Path(project.path) / file_id

        if not file_dir.exists():
            return None

        metadata_path = file_dir / "file.json"

        if metadata_path.exists():

            with open(
                metadata_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            extension = Path(
                data["file_name"]
            ).suffix

            file_path = file_dir / (
                file_id + extension
            )

            return File(
                file_id=data["file_id"],
                file_name=data["file_name"],
                project_id=data["project_id"],
                path=str(file_path)
            )

        # =====================================================
        # Fallback for old files
        # =====================================================

        for item in file_dir.iterdir():

            if item.is_file():

                return File(
                    file_id=file_id,
                    project_id=project_id,
                    file_name=item.name,
                    path=str(item)
                )

        return None

    # =========================================================
    # Get All Files
    # =========================================================

    def get_all_files(
        self,
        project_id: int
    ) -> list[File]:

        project = ProjectService().get_project(
            project_id=project_id
        )

        if project is None:
            return []

        project_path = Path(project.path)

        files = []

        for file_dir in project_path.iterdir():

            if not file_dir.is_dir():
                continue

            metadata_path = file_dir / "file.json"

            if not metadata_path.exists():
                continue

            with open(
                metadata_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            extension = Path(
                data["file_name"]
            ).suffix

            file_path = file_dir / (
                data["file_id"] + extension
            )

            files.append(
                File(
                    file_id=data["file_id"],
                    file_name=data["file_name"],
                    project_id=data["project_id"],
                    path=str(file_path)
                )
            )

        return files

    # =========================================================
    # Validate PDF
    # =========================================================

    def validate_pdf(
        self,
        file: UploadFile
    ) -> bool:

        try:

            file.file.seek(0)

            header = file.file.read(4)

            if header != b"%PDF":
                return False

            file.file.seek(0)

            PdfReader(file.file)

            file.file.seek(0)

            return True

        except Exception:

            return False

        finally:

            file.file.seek(0)

    # =========================================================
    # Validate DOCX
    # =========================================================

    def validate_docx(
        self,
        file: UploadFile
    ) -> bool:

        try:

            file.file.seek(0)

            docx.Document(file.file)

            file.file.seek(0)

            return True

        except Exception:

            return False

        finally:

            file.file.seek(0)

    # =========================================================
    # Validate TXT
    # =========================================================

    def validate_txt(
        self,
        file: UploadFile
    ) -> bool:

        try:

            file.file.seek(0)

            file.file.read().decode("utf-8")

            file.file.seek(0)

            return True

        except Exception:

            return False

        finally:

            file.file.seek(0)

    # =========================================================
    # Validate File Size
    # =========================================================

    def validate_file_size(
        self,
        file: UploadFile
    ) -> bool:

        file.file.seek(0, 2)

        file_size = file.file.tell()

        file.file.seek(0)

        return file_size <= self.config.MAX_FILE_SIZE