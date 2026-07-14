from fastapi import APIRouter
from app.schemas.chat import ChatRequest
from app.langgraph.agent import run_agent

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)

@router.post("/")
def chat(request: ChatRequest):
    result = run_agent(request.message)
    return result