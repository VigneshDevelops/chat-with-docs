from fastapi import FastAPI
from typing import Dict

app = FastAPI()  # <- the ASGI entrypoint


@app.get("/")
def index() -> Dict:
    return {"greating": "hello"}
