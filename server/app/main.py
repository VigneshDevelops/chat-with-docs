from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.file_upload import router as file_upload_router
from app.routes.chat import router as chat_upload_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


app.include_router(file_upload_router, prefix="/api/file")
app.include_router(chat_upload_router, prefix="/api/chat")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
