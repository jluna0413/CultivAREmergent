"""
Plants Router - CRUD operations for plant management
Migrated from app/blueprints/dashboard.py
"""

from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.responses import RedirectResponse
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.fastapi_app.dependencies import require_login, inject_template_context
from app.models_async.base import get_async_session  # Unified DB session provider
from app.fastapi_app.schemas import (
    PlantCreate, PlantUpdate, PlantResponse, PlantListResponse
)
from app.models_async.auth import User
from app.models_async.grow import Plant, Cultivar, Status

# HTML routes for backward compatibility - Legacy template support - DEPRECATED
router = APIRouter(tags=["plants LEGACY - DEPRECATED - Use /api/v1/plants"], deprecated=True)

# Clean JSON API routes under /api/v1/plants/* - PREFERRED FOR FLUTTER
api_router = APIRouter(tags=["plants-api FLUTTER READY"])


# ==============================================================================
# HTML Pages (DEPRECATED - Use /api/v1/plants/* endpoints instead)
# ==============================================================================

@router.get("/", name="plants_list", deprecated=True)
async def plants_list(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context),
):
    """DEPRECATED: Use /api/v1/plants/list instead - Display list of user's plants"""
    # Get plants for current user
    result = await db.execute(
        select(Plant).where(Plant.user_id == current_user.id)
    )
    plants = result.scalars().all()
    
    context.update({
        "plants": plants,
        "plant_count": len(plants),
    })
    
    return request.app.state.templates.TemplateResponse(
        "views/plants.html",
        context
    )


@router.get("/{plant_id}", name="plant_detail", deprecated=True)
async def plant_detail(
    request: Request,
    plant_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """DEPRECATED: Use /api/v1/plants/{plant_id} instead - Display plant detail page."""
    result = await db.execute(
        select(Plant).where(
            Plant.id == plant_id,
            Plant.user_id == current_user.id
        )
    )
    plant = result.scalar_one_or_none()
    
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    context.update({
        "plant": plant,
        "cultivar": plant.cultivar,
        "status": plant.status,
    })
    
    return request.app.state.templates.TemplateResponse(
        "views/plant-detail.html",
        context
    )


@router.get("/new", name="plant_create_page", deprecated=True)
async def plant_create_page(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """DEPRECATED: Use /api/v1/plants (POST) instead - Display plant creation form."""
    result = await db.execute(select(Cultivar))
    cultivars = result.scalars().all()
    
    result = await db.execute(select(Status))
    statuses = result.scalars().all()
    
    context.update({
        "cultivars": cultivars,
        "statuses": statuses,
    })
    
    return request.app.state.templates.TemplateResponse(
        "views/plant-form.html",
        context
    )


@router.get("/{plant_id}/edit", name="plant_edit_page", deprecated=True)
async def plant_edit_page(
    request: Request,
    plant_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """DEPRECATED: Use /api/v1/plants/{plant_id} (PATCH) instead - Display plant edit form."""
    result = await db.execute(
        select(Plant).where(
            Plant.id == plant_id,
            Plant.user_id == current_user.id
        )
    )
    plant = result.scalar_one_or_none()
    
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    result = await db.execute(select(Cultivar))
    cultivars = result.scalars().all()
    
    result = await db.execute(select(Status))
    statuses = result.scalars().all()
    
    context.update({
        "plant": plant,
        "cultivars": cultivars,
        "statuses": statuses,
    })
    
    return request.app.state.templates.TemplateResponse(
        "views/plant-form.html",
        context
    )


# ==============================================================================
# API Endpoints - CRUD Operations (FLUTTER PREFERRED)
# ==============================================================================

@router.post("/api/create", name="api_plant_create", deprecated=True)
async def api_plant_create(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_login),
    name: str = Form(...),
    description: str = Form(None),
    status_id: int = Form(...),
    cultivar_id: Optional[int] = Form(None),
    is_clone: bool = Form(False),
    autoflower: bool = Form(False),
):
    """Create a new plant."""
    try:
        # Validate status exists
        result = await db.execute(select(Status).where(Status.id == status_id))
        status_obj = result.scalar_one_or_none()
        if not status_obj:
            raise HTTPException(status_code=400, detail="Invalid status")
        
        # Validate cultivar if provided
        if cultivar_id:
            result = await db.execute(select(Cultivar).where(Cultivar.id == cultivar_id))
            cultivar = result.scalar_one_or_none()
            if not cultivar:
                raise HTTPException(status_code=400, detail="Invalid cultivar")
        
        # Create plant
        plant = Plant(
            name=name,
            description=description,
            status_id=status_id,
            cultivar_id=cultivar_id,
            is_clone=is_clone,
            autoflower=autoflower,
            user_id=current_user.id,
        )
        
        db.add(plant)
        await db.commit()
        await db.refresh(plant)
        
        return RedirectResponse(
            url=request.url_for("plant_detail", plant_id=plant.id),
            status_code=status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/api/{plant_id}", name="api_plant_update")
async def api_plant_update(
    request: Request,
    plant_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_login),
    plant_data: Optional[PlantUpdate] = None,
):
    """Update a plant."""
    try:
        result = await db.execute(
            select(Plant).where(
                Plant.id == plant_id,
                Plant.user_id == current_user.id
            )
        )
        plant = result.scalar_one_or_none()
        
        if not plant:
            raise HTTPException(status_code=404, detail="Plant not found")
        
        # Update fields from request
        if plant_data:
            update_data = plant_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(plant, key, value)
        
        await db.commit()
        
        return {"message": "Plant updated successfully", "plant_id": plant.id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api/{plant_id}", name="api_plant_delete")
async def api_plant_delete(
    plant_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_login),
):
    """Delete a plant."""
    try:
        result = await db.execute(
            select(Plant).where(
                Plant.id == plant_id,
                Plant.user_id == current_user.id
            )
        )
        plant = result.scalar_one_or_none()
        
        if not plant:
            raise HTTPException(status_code=404, detail="Plant not found")
        
        await db.delete(plant)
        await db.commit()
        
        return {"message": "Plant deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/list", name="api_plants_list")
async def api_plants_list(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_login),
):
    """Get list of user's plants (JSON API)."""
    try:
        result = await db.execute(
            select(Plant).where(Plant.user_id == current_user.id)
        )
        plants = result.scalars().all()
        
        plant_list = [
            {
                "id": p.id,
                "name": p.name,
                "status_id": p.status_id,
                "cultivar_id": p.cultivar_id,
                "is_clone": p.is_clone,
                "start_dt": p.start_dt.isoformat() if p.start_dt else None,
            }
            for p in plants
        ]
        
        return {
            "status": "success",
            "data": plant_list,
            "count": len(plant_list),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/{plant_id}", name="api_plant_get")
async def api_plant_get(
    plant_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_login),
):
    """Get plant details (JSON API)."""
    try:
        result = await db.execute(
            select(Plant).where(
                Plant.id == plant_id,
                Plant.user_id == current_user.id
            )
        )
        plant = result.scalar_one_or_none()
        
        if not plant:
            raise HTTPException(status_code=404, detail="Plant not found")
        
        return {
            "status": "success",
            "data": {
                "id": plant.id,
                "name": plant.name,
                "description": plant.description,
                "status_id": plant.status_id,
                "cultivar_id": plant.cultivar_id,
                "is_clone": plant.is_clone,
                "autoflower": plant.autoflower,
                "start_dt": plant.start_dt.isoformat() if plant.start_dt else None,
                "last_water_date": plant.last_water_date.isoformat() if plant.last_water_date else None,
                "last_feed_date": plant.last_feed_date.isoformat() if plant.last_feed_date else None,
                "harvest_date": plant.harvest_date.isoformat() if plant.harvest_date else None,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================================================
# Dashboard Statistics
# ==============================================================================

@router.get("/api/stats", name="api_plants_stats")
async def api_plants_stats(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_login),
):
    """Get plant statistics for dashboard."""
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
        
        return {
            "status": "success",
            "data": {
                "total_plants": total_plants,
                "active_plants": active_plants,
                "clones": clones,
                "harvested": harvested,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
