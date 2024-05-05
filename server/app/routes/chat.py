from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Any
from fastapi.responses import StreamingResponse

from app.services.langchain_service import chat, chat_stream

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str
    history: List[Any]


# Define the POST endpoint
@router.post("/")
async def chat_api(chat_request: ChatRequest):
    try:
        prompt = chat_request.prompt
        history = chat_request.history
        result = await chat(prompt, history)
        return result
    except Exception as e:
        print(e)
        raise e


@router.post("/stream")
async def chat_api_stream(chat_request: ChatRequest):
    try:
        prompt = chat_request.prompt
        history = chat_request.history
        print(prompt)

        result = chat_stream(prompt, history)
        print(result)
        return StreamingResponse(
            result,
            media_type="text/event-stream",
        )
    except Exception as e:
        print(e)
        raise e
