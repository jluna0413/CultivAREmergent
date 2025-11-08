"""
Clones API Router - Pure JSON CRUD operations
RESTful API endpoints under /api/v1/clones with Pydantic contracts
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict

from app.fastapi_app.dependencies import get_current_user
from app.models_async.auth import User
from app.models_async.grow import Plant
from app.models_async.base import get_async_session
from app.fastapi_app.models.clones import CloneCreate, CloneUpdate, CloneResponse, CloneListResponse

router = APIRouter(tags=["clones"])

async def get_current_user_dep(current_user: User = Depends(get_current_user)) -> User:
    """Get current authenticated user"""
    return current_user

from sqlalchemy.orm import selectinload
from datetime import datetime

# ... (imports)

@router.get("/", response_model=CloneListResponse)
async def list_clones(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    parent_plant_id: Optional[int] = Query(None, ge=1, description="Filter by parent plant ID"),
    search: Optional[str] = Query(None, description="Search in clone names"),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_dep)
):
    """Get paginated list of user's clones"""
    query = select(Plant).where(Plant.user_id == current_user.id, Plant.is_clone == True).options(
        selectinload(Plant.parent),
        selectinload(Plant.status),
        selectinload(Plant.zone)
    )
    count_query = select(func.count(Plant.id)).where(Plant.user_id == current_user.id, Plant.is_clone == True)

    if parent_plant_id:
        query = query.where(Plant.parent_id == parent_plant_id)
        count_query = count_query.where(Plant.parent_id == parent_plant_id)
    
    if search:
        query = query.where(Plant.name.ilike(f"%{search}%"))
        count_query = count_query.where(Plant.name.ilike(f"%{search}%"))

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    query = query.order_by(Plant.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    clones = result.scalars().all()
    
    items = []
    for clone in clones:
        parent_plant_name = ""
        if clone.parent:
            parent_plant_name = clone.parent.name
        
        items.append(CloneResponse(
            id=clone.id,
            name=clone.name,
            parent_plant_id=clone.parent_id,
            parent_plant_name=parent_plant_name,
            zone_id=clone.zone_id,
            status=clone.status.name if clone.status else "unknown",
            cloning_date=clone.start_dt,
            description=clone.description,
            user_id=clone.user_id,
            zone_name=clone.zone.name if clone.zone else None,
            age_days=(datetime.utcnow() - clone.start_dt).days if clone.start_dt else 0,
            created_at=clone.created_at,
            updated_at=clone.updated_at,
        ))

    return CloneListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        has_next=page * page_size < total,
        has_prev=page > 1
    )

@router.post("/", response_model=CloneResponse, status_code=status.HTTP_201_CREATED)
async def create_clone(
    clone_data: CloneCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_dep)
):
    """Create a new clone"""
    parent_plant_result = await db.execute(select(Plant).where(Plant.id == clone_data.parent_plant_id, Plant.user_id == current_user.id))
    parent_plant = parent_plant_result.scalar_one_or_none()
    if not parent_plant:
        raise HTTPException(status_code=404, detail="Parent plant not found")

    new_clone = Plant(
        name=clone_data.name,
        parent_id=clone_data.parent_plant_id,
        zone_id=clone_data.zone_id,
        status_id=1, # Default to seedling/cutting status
        start_dt=clone_data.cloning_date,
        description=clone_data.description,
        user_id=current_user.id,
        is_clone=True,
        cultivar_id=parent_plant.cultivar_id
    )
    db.add(new_clone)
    await db.commit()
    await db.refresh(new_clone)

    return CloneResponse(
        id=new_clone.id,
        name=new_clone.name,
        parent_plant_id=new_clone.parent_id,
        parent_plant_name=parent_plant.name,
        zone_id=new_clone.zone_id,
        status=new_clone.status.name if new_clone.status else "unknown",
        cloning_date=new_clone.start_dt,
        description=new_clone.description,
        user_id=new_clone.user_id,
        zone_name=new_clone.zone.name if new_clone.zone else None,
        age_days=0,
        created_at=new_clone.created_at,
        updated_at=new_clone.updated_at,
    )