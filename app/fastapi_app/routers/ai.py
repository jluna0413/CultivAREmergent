"""
AI Chat Router
Provides conversational interface for AI Grow Advisor.
"""

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime

from app.models_async.base import get_async_session
from app.fastapi_app.dependencies import require_login
from app.models_async.auth import User
from app.services.context_service import ContextService

router = APIRouter(tags=["AI Agent"])

class ChatRequest(BaseModel):
    message: str
    plant_id: int

class ChatResponse(BaseModel):
    response: str
    timestamp: str

@router.post("/api/v1/ai/chat", response_model=ChatResponse)
async def chat_with_advisor(
    request: ChatRequest,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_login),
):
    """
    Chat with the AI Grow Advisor about a specific plant.
    Fetches real-time context and simulates an expert response.
    """
    try:
        # 1. Fetch Context
        context = await ContextService.get_plant_context(request.plant_id, current_user.id, db)
        
        if not context:
            raise HTTPException(status_code=404, detail="Plant not found")
        
        # 2. Construction System Prompt (Simulation)
        # In a real app, this would be sent to OpenAI/Gemini
        plant_name = context['plant']['name']
        stage = context['plant']['stage']
        vpd = context['environment']['current'].get('vpd', 'N/A')
        temp = context['environment']['current'].get('temperature', 'N/A')
        
        # 3. Simulate Logic
        # It "reads" the context and incorporates it into the response.
        
        ai_response_text = (
            f"I'm looking at {plant_name} right now. "
            f"Since it's in the {stage} stage, keeping the environment dialed in is key. "
            f"I see your current temperature is {temp}°F with a VPD of {vpd} kPa. "
        )
        
        if isinstance(vpd, float):
             if vpd < 0.8:
                 ai_response_text += "Your VPD is a bit low, you might want to increase airflow or temperature."
             elif vpd > 1.6:
                 ai_response_text += "Your VPD is running high, consider adding some humidity."
             else:
                 ai_response_text += "That's a great range for vigorous growth!"
        else:
             ai_response_text += "I can't calculate VPD right now due to missing sensor data."

        ai_response_text += f"\n\nRegarding your question: \"{request.message}\" - generally, keeping consistent parameters is the best approach."


        return ChatResponse(
            response=ai_response_text,
            timestamp=datetime.utcnow().isoformat()
        )

    except PermissionError:
        raise HTTPException(status_code=403, detail="Not authorized")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
