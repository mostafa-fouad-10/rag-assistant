from fastapi import UploadFile
from src.services.file_service import FileService
from fastapi.responses import JSONResponse
from src.models.enums import ResponseSignal


class FileController:

    def __init__(self, file_service: FileService):
        self.file_service = file_service

    

    async def upload_file(self, file: UploadFile, project_id: int):

        is_valid, message = await self.file_service.validate_uploaded_file(file)

        if not is_valid:

            if message == ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value:
                return JSONResponse(
                    status_code=415,
                    content={
                        "success": False,
                        "message": message
                    }
                )

            if message == ResponseSignal.FILE_SIZE_EXCEEDED.value:
                return JSONResponse(
                    status_code=413,
                    content={
                        "success": False,
                        "message": message
                    }
                )

            return JSONResponse(
                status_code=422,
                content={
                    "success": False,
                    "message": message
                }
            )

        saved_file = await self.file_service.save_file(
                file=file,
                project_id=project_id
            )

        return JSONResponse(
                status_code=201,
                content={
                    "success": True,
                    "message": "File uploaded successfully",
                    "file": saved_file.model_dump()
                }
            )

    def delete_file(self, project_id: int, file_id: str):

        deleted = self.file_service.delete_file(
            project_id=project_id,
            file_id=file_id
        )

        if not deleted:
            return {
                "success": False,
                "message": "File not found"
            }

        return {
            "success": True,
            "message": "File deleted successfully"
        }


    def get_all_files(self, project_id: int):

        files = self.file_service.get_all_files(
            project_id=project_id
        )

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "files": [
                    file.model_dump()
                    for file in files
                ]
            }
        )    