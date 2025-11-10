"""
Plants API Router - Pure JSON CRUD operations
RESTful API endpoints under /api/v1/plants with Pydantic contracts
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict, Any
from datetime import datetime, date

from app.fastapi_app.dependencies import get_current_user
from app.models_async.auth import User
from app.models_async.grow import Plant, Cultivar, Status
from app.models_async.base import get_async_session

# Pydantic models for request/response
from pydantic import BaseModel, Field
from typing import Literal

class PlantCreate(BaseModel):
    """Request model for creating a plant"""
    name: str = Field(..., min_length=1, max_length=100, description="Plant name")
    description: Optional[str] = Field(None, max_length=500, description="Plant description")
    status_id: int = Field(..., gt=0, description="Status ID")
    cultivar_id: Optional[int] = Field(None, gt=0, description="Cultivar ID")
    is_clone: bool = Field(False, description="Whether this is a clone")
    autoflower: bool = Field(False, description="Whether this is an autoflower variety")

class PlantUpdate(BaseModel):
    """Request model for updating a plant"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status_id: Optional[int] = Field(None, gt=0)
    cultivar_id: Optional[int] = Field(None, gt=0)
    is_clone: Optional[bool] = None
    autoflower: Optional[bool] = None
    start_date: Optional[date] = None
    last_water_date: Optional[date] = None
    last_feed_date: Optional[date] = None
    harvest_date: Optional[date] = None

class PlantResponse(BaseModel):
    """Response model for a single plant"""
    id: int
    name: str
    description: Optional[str]
    status_id: int
    cultivar_id: Optional[int]
    is_clone: bool
    autoflower: bool
    start_date: Optional[datetime]
    last_water_date: Optional[datetime]
    last_feed_date: Optional[datetime]
    harvest_date: Optional[datetime]
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PlantListResponse(BaseModel):
    """Response model for plant list with pagination"""
    items: List[PlantResponse]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool

class PlantsStatsResponse(BaseModel):
    """Response model for plant statistics"""
    total_plants: int
    active_plants: int
    clones: int
    harvested: int
    by_status: Dict[str, int]

# Create router with /api/v1/plants prefix
router = APIRouter(tags=["plants"])

async def get_current_user_dep(current_user: User = Depends(get_current_user)) -> User:
    """Get current authenticated user"""
    return current_user

from sqlalchemy.orm import selectinload

# ... (imports)

@router.get("/", response_model=PlantListResponse)
async def list_plants(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status_id: Optional[int] = Query(None, ge=1, description="Filter by status ID"),
    cultivar_id: Optional[int] = Query(None, ge=1, description="Filter by cultivar ID"),
    is_clone: Optional[bool] = Query(None, description="Filter by clone status"),
    search: Optional[str] = Query(None, description="Search in plant names"),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_dep)
):
    """Get paginated list of user's plants"""
    try:
        # Build query with filters and eager loading
        query = select(Plant).where(Plant.user_id == current_user.id).options(
            selectinload(Plant.cultivar),
            selectinload(Plant.status),
            selectinload(Plant.zone)
        )
        
        if status_id:
            query = query.where(Plant.status_id == status_id)
        
        if cultivar_id:
            query = query.where(Plant.cultivar_id == cultivar_id)
        
        if is_clone is not None:
            query = query.where(Plant.is_clone == is_clone)
        
        if search:
            query = query.where(Plant.name.ilike(f"%{search}%"))
        
        # Get total count
        count_query = select(func.count(Plant.id)).where(Plant.user_id == current_user.id)
        
        if status_id:
            count_query = count_query.where(Plant.status_id == status_id)
        if cultivar_id:
            count_query = count_query.where(Plant.cultivar_id == cultivar_id)
        if is_clone is not None:
            count_query = count_query.where(Plant.is_clone == is_clone)
        if search:
            count_query = count_query.where(Plant.name.ilike(f"%{search}%"))
        
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0
        
        # Apply pagination and ordering
        query = query.order_by(Plant.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        
        result = await db.execute(query)
        plants = result.scalars().all()
        
        # Calculate pagination info
        has_next = page * page_size < total
        has_prev = page > 1
        
        return PlantListResponse(
            items=[PlantResponse.model_validate(plant) for plant in plants],
            total=total,
            page=page,
            page_size=page_size,
            has_next=has_next,
            has_prev=has_prev
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch plants: {str(e)}")

@router.get("/{plant_id}", response_model=PlantResponse)
async def get_plant(
    plant_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_dep)
):
    """Get a single plant by ID"""
    try:
        result = await db.execute(
            select(Plant).where(
                Plant.id == plant_id,
                Plant.user_id == current_user.id
            ).options(
                selectinload(Plant.cultivar),
                selectinload(Plant.status),
                selectinload(Plant.zone)
            )
        )
        plant = result.scalar_one_or_none()
        
        if not plant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plant not found"
            )
        
        return PlantResponse.model_validate(plant)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch plant: {str(e)}")

@router.post("/", response_model=PlantResponse, status_code=status.HTTP_201_CREATED)
async def create_plant(
    plant_data: PlantCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_dep)
):
    """Create a new plant"""
    try:
        # Validate status exists
        result = await db.execute(select(Status).where(Status.id == plant_data.status_id))
        status_obj = result.scalar_one_or_none()
        if not status_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status ID"
            )
        
        # Validate cultivar if provided
        if plant_data.cultivar_id:
            result = await db.execute(select(Cultivar).where(Cultivar.id == plant_data.cultivar_id))
            cultivar = result.scalar_one_or_none()
            if not cultivar:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid cultivar ID"
                )
        
        # Create plant
        plant = Plant(
            name=plant_data.name,
            description=plant_data.description,
            status_id=plant_data.status_id,
            cultivar_id=plant_data.cultivar_id,
            is_clone=plant_data.is_clone,
            autoflower=plant_data.autoflower,
            user_id=current_user.id,
        )
        
        db.add(plant)
        await db.commit()
        await db.refresh(plant)
        
        return PlantResponse.model_validate(plant)
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create plant: {str(e)}"
        )

@router.put("/{plant_id}", response_model=PlantResponse)
async def update_plant(
    plant_id: int,
    plant_data: PlantUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_dep)
):
    """Update an existing plant"""
    try:
        # Get existing plant
        result = await db.execute(
            select(Plant).where(
                Plant.id == plant_id,
                Plant.user_id == current_user.id
            )
        )
        plant = result.scalar_one_or_none()
        
        if not plant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plant not found"
            )
        
        # Update fields from request
        update_data = plant_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(plant, key):
                setattr(plant, key, value)
        
        await db.commit()
        await db.refresh(plant)
        
        return PlantResponse.model_validate(plant)
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update plant: {str(e)}"
        )

@router.delete("/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plant(
    plant_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_dep)
):
    """Delete a plant"""
    try:
        result = await db.execute(
            select(Plant).where(
                Plant.id == plant_id,
                Plant.user_id == current_user.id
            )
        )
        plant = result.scalar_one_or_none()
        
        if not plant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plant not found"
            )
        
        await db.delete(plant)
        await db.commit()
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete plant: {str(e)}"
        )

@router.get("/stats/summary", response_model=PlantsStatsResponse)
async def get_plants_stats(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_dep)
):
    """Get plant statistics for dashboard"""
    try:
        # Get total plants
        result = await db.execute(
            select(func.count(Plant.id)).where(Plant.user_id == current_user.id)
        )
        total_plants = result.scalar() or 0
        
        # Get active plants (seedling, veg, flowering)
        active_status_ids = [1, 2, 3]  # TODO: Make configurable
        result = await db.execute(
            select(func.count(Plant.id)).where(
                Plant.user_id == current_user.id,
                Plant.status_id.in_(active_status_ids)
            )
        )
        active_plants = result.scalar() or 0
        
        # Get clones count
        result = await db.execute(
            select(func.count(Plant.id)).where(
                Plant.user_id == current_user.id,
                Plant.is_clone == True
            )
        )
        clones = result.scalar() or 0
        
        # Get harvested plants
        result = await db.execute(
            select(func.count(Plant.id)).where(
                Plant.user_id == current_user.id,
                Plant.harvest_date.isnot(None)
            )
        )
        harvested = result.scalar() or 0
        
        # Get status breakdown
        result = await db.execute(
            select(Plant.status_id, func.count(Plant.id))
            .where(Plant.user_id == current_user.id)
            .group_by(Plant.status_id)
        )
        status_counts = {str(status_id): count for status_id, count in result.all()}
        
        return PlantsStatsResponse(
            total_plants=total_plants,
            active_plants=active_plants,
            clones=clones,
            harvested=harvested,
            by_status=status_counts
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch plants stats: {str(e)}")
