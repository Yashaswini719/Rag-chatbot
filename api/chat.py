from fastapi import APIRouter
from pydantic import BaseModel

from rag.pipeline import ask


router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


class ChatRequest(BaseModel):
    question: str
    session_id: str


@router.post("/")
def chat(request: ChatRequest):

    return ask(
        request.question,
        request.session_id
    )