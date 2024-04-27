from fastapi import FastAPI
from app.routes.file_upload import router as file_upload_router

app = FastAPI()


app.include_router(file_upload_router, prefix="/api")
