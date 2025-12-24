from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.fastapi_app.dependencies import get_db, require_login
from app.models_async.auth import User
from app.services.commission_service import CommissionService

router = APIRouter(prefix="/sales", tags=["sales"])

@router.get("/analytics/history", response_model=List[Dict[str, Any]])
async def get_sales_history(
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_login)
):
    """
    Get daily sales history for the authenticated breeder.
    """
    history = await CommissionService.get_daily_sales_history(db, current_user.id, days=days)
    return history
