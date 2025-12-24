"""
Context API Router
Aggregates plant, environmental, and activity data for AI context.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models_async.base import get_async_session
from app.fastapi_app.dependencies import require_login
from app.models_async.auth import User
from app.services.context_service import ContextService

router = APIRouter(tags=["Context API"])

@router.get("/api/v1/context/plant/{plant_id}", name="get_plant_context")
async def get_plant_context(
    plant_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_login),
):
    """
    Get aggregated context for a specific plant.
    Includes identity, environmental data (current + 24h history), and recent logs.
    """
    try:
        context = await ContextService.get_plant_context(plant_id, current_user.id, db)
        
        if not context:
            raise HTTPException(status_code=404, detail="Plant not found")
            
        return context

    except PermissionError:
        raise HTTPException(status_code=403, detail="Not authorized")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
