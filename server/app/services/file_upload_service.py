import os
import shutil
from typing import List
from fastapi import UploadFile, HTTPException
from app.constant import ALLOWED_CONTENT_TYPES


async def create_folder_upload_files(files: List[UploadFile]) -> str:
    # Create a temporary folder with a unique name
    temp_folder = f"uploads/temp_{os.urandom(8).hex()}"
    os.makedirs(temp_folder, exist_ok=True)

    # Save files to the temporary folder
    for file in files:
        # Validate file content type
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            # Remove the temporary folder and raise an HTTP exception
            shutil.rmtree(temp_folder)
            raise HTTPException(
                status_code=400,
                detail=f"File type '{file.content_type}' not allowed. Only PDF, TXT, and DOCX files are accepted.",
            )

        # Save file to disk
        file_path = os.path.join(temp_folder, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

    return temp_folder
