from pydantic import BaseModel, Field
from typing import List, Optional


class AgentQueryRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Question or prompt from store owner")


class AgentRecommendation(BaseModel):
    title: str
    category: str
    priority: str = Field(..., description="High, Medium, or Low")
    message: str
    action_type: Optional[str] = None
    target_sku: Optional[str] = None


class AgentQueryResponse(BaseModel):
    reply: str
    intent: str
    recommendations: List[AgentRecommendation] = []
    timestamp: str

