"""
Plants Router - CRUD operations for plant management
Migrated from app/blueprints/dashboard.py
"""

from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.responses import RedirectResponse
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.repositories.interfaces import PlantRepository, PlantCreateDTO, PlantUpdateDTO
from app.fastapi_app.dependencies import require_login, inject_template_context, get_plant_repository
from app.models_async.base import get_async_session  # Unified DB session provider (legacy support)
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

@router.post("/api/create", name="api_plant_create")
async def api_plant_create(
    request: Request,
    repo: PlantRepository = Depends(get_plant_repository),
    current_user: User = Depends(require_login),
    name: str = Form(...),
    description: str = Form(None),
    status_id: int = Form(...),
    cultivar_id: Optional[int] = Form(None),
    is_clone: bool = Form(False),
    autoflower: bool = Form(False),
):
    """Create a new plant using Repository Pattern."""
    try:
        dto = PlantCreateDTO(
            user_id=current_user.id,
            name=name,
            status_id=status_id,
            cultivar_id=cultivar_id,
            is_clone=is_clone,
            zone_id=None # Default
        )
        
        plant = await repo.create(dto)
        
        # Backward compatibility for redirect
        return RedirectResponse(
            url=request.url_for("api_plant_get", plant_id=plant.id),
            status_code=status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/api/{plant_id}", name="api_plant_update")
async def api_plant_update(
    request: Request,
    plant_id: int,
    repo: PlantRepository = Depends(get_plant_repository),
    current_user: User = Depends(require_login),
    plant_data: Optional[PlantUpdate] = None,
):
    """Update a plant using Repository Pattern."""
    try:
        # Verify ownership
        existing = await repo.get_by_id(plant_id)
        if not existing or existing.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Plant not found")
        
        if plant_data:
            update_dto = PlantUpdateDTO(
                name=plant_data.name,
                status_id=plant_data.status_id,
                # Mapping other fields as needed from schema
            )
            updated = await repo.update(plant_id, update_dto)
            return {"message": "Plant updated successfully", "plant_id": updated.id}
            
        return {"message": "No data provided"} 
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api/{plant_id}", name="api_plant_delete")
async def api_plant_delete(
    plant_id: int,
    repo: PlantRepository = Depends(get_plant_repository),
    current_user: User = Depends(require_login),
):
    """Delete a plant using Repository Pattern."""
    try:
        existing = await repo.get_by_id(plant_id)
        if not existing or existing.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Plant not found")
            
        await repo.delete(plant_id)
        return {"message": "Plant deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/list", name="api_plants_list")
async def api_plants_list(
    repo: PlantRepository = Depends(get_plant_repository),
    current_user: User = Depends(require_login),
):
    """Get list of user's plants (JSON API)."""
    try:
        plants = await repo.get_by_user(current_user.id)
        
        plant_list = [
            {
                "id": p.id,
                "name": p.name,
                "status_id": p.status_id,
                "cultivar_id": p.cultivar_id,
                "is_clone": p.is_clone,
                "start_dt": p.start_dt.isoformat() if p.start_dt else None,
                # DTO properties
                "status_name": p.status_name,
                "strain_name": p.strain_name
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
    repo: PlantRepository = Depends(get_plant_repository),
    current_user: User = Depends(require_login),
):
    """Get plant details (JSON API)."""
    try:
        plant = await repo.get_by_id(plant_id)
        
        if not plant:
             raise HTTPException(status_code=404, detail="Plant not found")
             
        if plant.user_id != current_user.id:
             raise HTTPException(status_code=403, detail="Not authorized")
        
        return {
            "status": "success",
            "data": plant.model_dump() # DTO to generic dictionary
        }
    except HTTPException:
        raise
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
    """Get plant statistics for dashboard. 
    NOTE: Keeping as direct DB for now as Repos are for Entity CRUD, 
    Aggregation is usually a separate repo method or service.
    """
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
