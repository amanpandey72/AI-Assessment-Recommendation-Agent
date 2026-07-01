from fastapi import APIRouter

from app.agent import SHLAgent
from app.schemas import ChatRequest, ChatResponse

router = APIRouter()

agent = SHLAgent()


@router.get("/health")
def health():
    return {
        "status": "ok"
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    result = agent.recommend(request.message)

    return ChatResponse(
        status=result["status"],
        response=result["response"]
    )