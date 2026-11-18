from typing import List
from fastapi import APIRouter
from backend.models.agent import (
    AgentQueryRequest,
    AgentQueryResponse,
    AgentRecommendation,
)
from backend.agents.shop_agent import ShopMateAgent

router = APIRouter(prefix="/api/agent", tags=["AI Business Agent"])


@router.post("/chat", response_model=AgentQueryResponse)
def chat_with_agent(request: AgentQueryRequest):
    """Chat with the ShopMate AI Agent to receive insights and recommendations based on real-time store metrics."""
    return ShopMateAgent.answer_query(request.message)


@router.post("/guide", response_model=AgentQueryResponse)
def guide_web_query(request: AgentQueryRequest):
    """Ask the Web Guide AI how to navigate and use the ShopMate AI website."""
    return ShopMateAgent.answer_web_guide_query(request.message)


@router.get("/recommendations", response_model=List[AgentRecommendation])
def get_recommendations():
    """Retrieve proactive, automated business recommendations from the AI agent."""
    return ShopMateAgent.generate_recommendations()

