"""
Clone Management Router
Handles clone creation, listing, and management from parent plants.
Dual-router pattern: HTML template routes + Clean JSON API contracts
"""

from fastapi import APIRouter, Request, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.fastapi_app.dependencies import require_login, inject_template_context
from app.models_async.base import get_async_session as get_async_db
from app.models_async.auth import User
from app.models_async.grow import Plant, Cultivar

# HTML routes for backward compatibility - Legacy template support
router = APIRouter(prefix="/clones", tags=["clones"])

# Clean JSON API routes under /api/v1/clones/*
api_router = APIRouter(prefix="/clones", tags=["clones-api"])


# ============================================================================
# Helper Functions
# ============================================================================

def create_paginated_response(items: List, total: int, page: int, page_size: int) -> dict:
    """Create standardized paginated response."""
    pages = (total + page_size - 1) // page_size if total > 0 else 0
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
        "has_next": page < pages,
        "has_prev": page > 1
    }


# ============================================================================
# HTML Pages (Legacy Support)
# ============================================================================

@router.get("/", name="clones_list_page")
async def clones_list_page(
    request: Request,
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """List all clones for the current user - Legacy template support."""
    # TODO: Migrate to async SQLAlchemy
    context.update({
        "page_title": "Clone Management",
        "page_description": "Manage your plant clones and propagation. This feature is being migrated to the new system."
    })
    return request.app.state.templates.TemplateResponse(
        "views/coming_soon.html",
        context
    )


@router.get("/dashboard", name="clones_dashboard_page")
async def clones_dashboard_page(
    request: Request,
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Clone dashboard page - Legacy template support."""
    context.update({
        "page_title": "Clone Dashboard",
        "page_description": "Overview of your clone operations and management"
    })
    return request.app.state.templates.TemplateResponse(
        "clones/dashboard.html",
        context
    )


@router.get("/lineage", name="clones_lineage_page")
async def clones_lineage_page(
    request: Request,
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Clone lineage view page - Legacy template support."""
    context.update({
        "page_title": "Clone Lineage",
        "page_description": "View and manage clone family trees and relationships"
    })
    return request.app.state.templates.TemplateResponse(
        "clones/lineage.html",
        context
    )


@router.get("/{clone_id}", name="clones_detail_page")
async def clones_detail_page(
    clone_id: int,
    request: Request,
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context),
    db: AsyncSession = Depends(get_async_db)
):
    """View details of a specific clone - Legacy template support."""
    try:
        result = await db.execute(
            select(Plant).where(
                Plant.id == clone_id,
                Plant.user_id == current_user.id,
                Plant.is_clone == True
            )
        )
        clone = result.scalar_one_or_none()

        if not clone:
            raise HTTPException(status_code=404, detail="Clone not found")

        # Get parent plant info
        parent = None
        if clone.parent_id:
            result = await db.execute(
                select(Plant).where(
                    Plant.id == clone.parent_id,
                    Plant.user_id == current_user.id
                )
            )
            parent = result.scalar_one_or_none()

        # Get descendant clones (clones of this clone)
        result = await db.execute(
            select(Plant).where(
                Plant.parent_id == clone_id,
                Plant.user_id == current_user.id
            )
        )
        descendants = result.scalars().all()

        # Get full lineage
        lineage_chain = []
        current = clone
        while current:
            lineage_chain.append(current)
            current = current.parent if current.parent_id else None

        context.update({
            "clone": clone,
            "parent": parent,
            "descendants": descendants,
            "lineage": list(reversed(lineage_chain)),
            "now": datetime.now(),
        })
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching clone: {e}")
        raise HTTPException(status_code=500, detail="Error fetching clone details")

    return request.app.state.templates.TemplateResponse(
        "views/clone-detail.html",
        context
    )


# ============================================================================
# Clean JSON API Contracts
# ============================================================================

class CloneListResponse(BaseModel):
    """Response model for clone list API."""
    items: List[dict]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_prev: bool


class CloneCreateResponse(BaseModel):
    """Response model for clone creation API."""
    message: str
    status: str
    clone_ids: List[int]


class CloneDeleteResponse(BaseModel):
    """Response model for clone deletion API."""
    message: str
    status: str


class CloneStatsResponse(BaseModel):
    """Response model for clone statistics API."""
    total_clones: int
    active_clones: int
    harvested_clones: int


@api_router.get("/list", response_model=CloneListResponse, name="api_clones_list")
async def api_clones_list(
    current_user: User = Depends(require_login),
    db: AsyncSession = Depends(get_async_db),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
):
    """Get paginated list of clones - Clean JSON API."""
    try:
        # Build base query
        query = select(Plant).where(
            Plant.user_id == current_user.id,
            Plant.is_clone == True
        )
        
        # Apply search filter
        if search:
            query = query.where(Plant.name.contains(search))
        
        # Get total count
        count_query = select(func.count(Plant.id)).where(
            Plant.user_id == current_user.id,
            Plant.is_clone == True
        )
        if search:
            count_query = count_query.where(Plant.name.contains(search))
        
        result = await db.execute(count_query)
        total = result.scalar() or 0
        
        # Apply pagination and ordering
        query = query.order_by(Plant.name).offset((page - 1) * page_size).limit(page_size)
        
        # Execute main query
        result = await db.execute(query)
        clones = result.scalars().all()
        
        # Transform to response format
        clones_data = []
        for clone in clones:
            clones_data.append({
                "id": clone.id,
                "name": clone.name,
                "status_id": clone.status_id,
                "cultivar_id": clone.cultivar_id,
                "parent_id": clone.parent_id,
                "start_dt": clone.start_dt.isoformat() if clone.start_dt else None,
                "harvest_date": clone.harvest_date.isoformat() if clone.harvest_date else None,
                "zone_name": clone.zone_name,
            })

        return CloneListResponse(**create_paginated_response(clones_data, total, page, page_size))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching clones: {str(e)}")


@api_router.get("/{clone_id}", name="api_clones_get")
async def api_clones_get(
    clone_id: int,
    current_user: User = Depends(require_login),
    db: AsyncSession = Depends(get_async_db)
):
    """Get clone details - Clean JSON API."""
    try:
        result = await db.execute(
            select(Plant).where(
                Plant.id == clone_id,
                Plant.user_id == current_user.id,
                Plant.is_clone == True
            )
        )
        clone = result.scalar_one_or_none()

        if not clone:
            raise HTTPException(status_code=404, detail="Clone not found")

        return {
            "id": clone.id,
            "name": clone.name,
            "status_id": clone.status_id,
            "cultivar_id": clone.cultivar_id,
            "parent_id": clone.parent_id,
            "start_dt": clone.start_dt.isoformat() if clone.start_dt else None,
            "harvest_date": clone.harvest_date.isoformat() if clone.harvest_date else None,
            "zone_name": clone.zone_name,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching clone: {str(e)}")


@api_router.post("/create-from-plant", response_model=CloneCreateResponse, name="api_clones_create")
async def api_clones_create(
    request: Request,
    current_user: User = Depends(require_login),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a clone from an existing plant - Clean JSON API."""
    try:
        data = await request.json()

        parent_id = data.get("parent_id")
        clone_count = data.get("clone_count", 1)

        if not parent_id:
            raise HTTPException(status_code=400, detail="Parent ID required")

        # Verify parent plant exists and belongs to user
        result = await db.execute(
            select(Plant).where(
                Plant.id == parent_id,
                Plant.user_id == current_user.id
            )
        )
        parent = result.scalar_one_or_none()

        if not parent:
            raise HTTPException(status_code=404, detail="Parent plant not found")

        # Create clones
        created_clones = []
        for i in range(int(clone_count)):
            clone = Plant(
                name=data.get(f"name_{i}", f"{parent.name} Clone {i+1}"),
                user_id=current_user.id,
                cultivar_id=parent.cultivar_id,
                status_id=1,  # Start as seedling
                is_clone=True,
                parent_id=parent_id,
                start_dt=datetime.now(),
                zone_id=data.get(f"zone_id_{i}"),
            )
            db.add(clone)
            created_clones.append(clone)

        await db.commit()

        return CloneCreateResponse(
            message=f"Created {len(created_clones)} clone(s)",
            status="created",
            clone_ids=[c.id for c in created_clones]
        )
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating clones: {str(e)}")


@api_router.post("/create-batch", response_model=CloneCreateResponse, name="api_clones_create_batch")
async def api_clones_create_batch(
    request: Request,
    current_user: User = Depends(require_login),
    db: AsyncSession = Depends(get_async_db)
):
    """Create multiple clones from a parent plant with batch data - Clean JSON API."""
    try:
        data = await request.json()

        parent_id = data.get("parent_id")
        clones_data = data.get("clones", [])

        if not parent_id or not clones_data:
            raise HTTPException(status_code=400, detail="Parent ID and clones data required")

        # Verify parent plant exists and belongs to user
        result = await db.execute(
            select(Plant).where(
                Plant.id == parent_id,
                Plant.user_id == current_user.id
            )
        )
        parent = result.scalar_one_or_none()

        if not parent:
            raise HTTPException(status_code=404, detail="Parent plant not found")

        # Create clones from batch data
        created_clones = []
        for clone_data in clones_data:
            clone = Plant(
                name=clone_data.get("name", f"{parent.name} Clone"),
                user_id=current_user.id,
                cultivar_id=parent.cultivar_id,
                status_id=clone_data.get("status_id", 1),  # Default to seedling
                is_clone=True,
                parent_id=parent_id,
                start_dt=clone_data.get("start_dt") or datetime.now(),
                zone_id=clone_data.get("zone_id"),
            )
            db.add(clone)
            created_clones.append(clone)

        await db.commit()

        return CloneCreateResponse(
            message=f"Created {len(created_clones)} clone(s)",
            status="created",
            clone_ids=[c.id for c in created_clones]
        )
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating clones: {str(e)}")


@api_router.delete("/{clone_id}", response_model=CloneDeleteResponse, name="api_clones_delete")
async def api_clones_delete(
    clone_id: int,
    current_user: User = Depends(require_login),
    db: AsyncSession = Depends(get_async_db)
):
    """Delete a clone - Clean JSON API."""
    try:
        result = await db.execute(
            select(Plant).where(
                Plant.id == clone_id,
                Plant.user_id == current_user.id,
                Plant.is_clone == True
            )
        )
        clone = result.scalar_one_or_none()

        if not clone:
            raise HTTPException(status_code=404, detail="Clone not found")

        await db.delete(clone)
        await db.commit()

        return CloneDeleteResponse(
            message="Clone deleted successfully",
            status="deleted"
        )
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting clone: {str(e)}")


@api_router.get("/parents", name="api_clones_available_parents")
async def api_clones_available_parents(
    current_user: User = Depends(require_login),
    db: AsyncSession = Depends(get_async_db)
):
    """Get available parent plants for cloning - Clean JSON API."""
    try:
        # Get living plants that are not already clones (optional)
        result = await db.execute(
            select(Plant).where(
                Plant.user_id == current_user.id,
                Plant.status_id.in_([1, 2, 3])  # Seedling, Vegetative, Flowering
            ).order_by(Plant.name)
        )
        parents = result.scalars().all()

        parents_data = []
        for plant in parents:
            # Count how many clones this plant has
            result = await db.execute(
                select(func.count(Plant.id)).where(Plant.parent_id == plant.id)
            )
            clone_count = result.scalar() or 0

            parents_data.append({
                "id": plant.id,
                "name": plant.name,
                "status_id": plant.status_id,
                "cultivar_id": plant.cultivar_id,
                "cultivar_name": plant.cultivar.name if plant.cultivar else None,
                "clone_count": clone_count,
                "start_dt": plant.start_dt.isoformat() if plant.start_dt else None,
            })

        return {
            "status": "success",
            "data": parents_data,
            "total": len(parents_data),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching parent plants: {str(e)}")


@api_router.get("/stats", response_model=CloneStatsResponse, name="api_clones_stats")
async def api_clones_stats(
    current_user: User = Depends(require_login),
    db: AsyncSession = Depends(get_async_db)
):
    """Get clone statistics - Clean JSON API."""
    try:
        result = await db.execute(
            select(func.count(Plant.id)).where(
                Plant.user_id == current_user.id,
                Plant.is_clone == True
            )
        )
        total_clones = result.scalar() or 0

        result = await db.execute(
            select(func.count(Plant.id)).where(
                Plant.user_id == current_user.id,
                Plant.is_clone == True,
                Plant.status_id.in_([1, 2, 3])
            )
        )
        active_clones = result.scalar() or 0

        result = await db.execute(
            select(func.count(Plant.id)).where(
                Plant.user_id == current_user.id,
                Plant.is_clone == True,
                Plant.status_id == 4
            )
        )
        harvested_clones = result.scalar() or 0

        return CloneStatsResponse(
            total_clones=total_clones,
            active_clones=active_clones,
            harvested_clones=harvested_clones
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching clone stats: {str(e)}")


# Note: This router needs to be included in the main FastAPI app with both routers
# In __init__.py: app.include_router(clones.router, tags=["Clones Legacy"])
#                app.include_router(clones.api_router, prefix="/api/v1", tags=["Clones API"])
