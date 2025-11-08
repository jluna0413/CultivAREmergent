"""
Marketing API Router - Pure JSON CRUD operations
RESTful API endpoints under /api/v1/marketing with Pydantic contracts
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.fastapi_app.dependencies import get_current_admin_user
from app.models_async.auth import User
from app.models_async.marketing import WaitlistEntry, LeadMagnet
from app.models_async.base import get_async_session
from app.fastapi_app.models.marketing import WaitlistEntryCreate, WaitlistEntryResponse, WaitlistStats, LeadMagnetCreate, LeadMagnetResponse

router = APIRouter(tags=["marketing"])

@router.post("/waitlist", response_model=WaitlistEntryResponse, status_code=status.HTTP_201_CREATED)
async def join_waitlist(
    entry_data: WaitlistEntryCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Join the waitlist"""
    new_entry = WaitlistEntry(**entry_data.dict())
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    return WaitlistEntryResponse.from_orm(new_entry)

@router.get("/waitlist/stats", response_model=WaitlistStats)
async def get_waitlist_stats(
    db: AsyncSession = Depends(get_async_session)
):
    """Get waitlist statistics"""
    # This is placeholder data. A real implementation would query the database.
    return WaitlistStats(total=100, today=5, this_week=20)

@router.post("/lead-magnets", response_model=LeadMagnetResponse, status_code=status.HTTP_201_CREATED)
async def create_lead_magnet(
    magnet_data: LeadMagnetCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_admin_user)
):
    """Create a new lead magnet"""
    new_magnet = LeadMagnet(**magnet_data.dict())
    db.add(new_magnet)
    await db.commit()
    await db.refresh(new_magnet)
    return LeadMagnetResponse.from_orm(new_magnet)

@router.get("/lead-magnets", response_model=List[LeadMagnetResponse])
async def list_lead_magnets(
    db: AsyncSession = Depends(get_async_session)
):
    """List all lead magnets"""
    result = await db.execute(select(LeadMagnet))
    magnets = result.scalars().all()
    return [LeadMagnetResponse.from_orm(magnet) for magnet in magnets]
