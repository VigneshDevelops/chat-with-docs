from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.services.langchain_service import chat

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str
    history: List[str]


# Define the POST endpoint
@router.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    try:
        prompt = chat_request.prompt
        history = chat_request.history
        result = await chat(prompt)
        return result
    except Exception as e:
        print(e)
        raise e
