"""
Breeders Router - CRUD operations for breeder management
Migrated from app/blueprints/breeders.py
Dual-router pattern: HTML template routes + Clean JSON API contracts
"""

from fastapi import APIRouter, Request, Depends, HTTPException, status, Query
from sqlalchemy import select, func, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional, List
import math
from pydantic import BaseModel

from app.fastapi_app.dependencies import require_login, inject_template_context
from app.models_async.base import get_async_session as get_async_db
from app.fastapi_app.models.breeders import (
    BreederCreate, BreederUpdate, BreederResponse, BreederListResponse,
    BreederCreateResponse, BreederUpdateResponse, BreederDeleteResponse, BreederStats
)
from app.models_async.auth import User
from app.models_async.grow import Breeder, Cultivar

# HTML routes for backward compatibility - Legacy template support
router = APIRouter(prefix="/breeders", tags=["breeders"])

# Clean JSON API routes under /api/v1/breeders/*
api_router = APIRouter(prefix="/breeders", tags=["breeders-api"])


# ============================================================================
# Helper Functions
# ============================================================================

def create_paginated_response(items: List, total: int, page: int, page_size: int) -> dict:
    """Create standardized paginated response."""
    pages = math.ceil(total / page_size) if total > 0 else 0
    
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

@router.get("/add", name="add_breeder_page")
async def add_breeder_page(
    request: Request,
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Display form for adding new breeder (legacy template support)."""
    return request.app.state.templates.TemplateResponse("views/add_breeder.html", context)


@router.get("/", name="breeders_list_page")
async def breeders_list_page(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Display list of breeders with legacy template support."""
    try:
        # Get breeders with eager loading of cultivars/strains
        result = await db.execute(
            select(Breeder).options(selectinload(Breeder.cultivars)).order_by(Breeder.name)
        )
        breeders = result.scalars().all()
        
        # Transform to match legacy template format
        breeder_data = []
        for breeder in breeders:
            cultivar_count = len(breeder.cultivars) if breeder.cultivars else 0
            breeder_data.append({
                'id': breeder.id,
                'name': breeder.name,
                'cultivar_count': cultivar_count,
            })
        
        context.update({
            "breeders": breeder_data,
            "breeder_count": len(breeder_data),
        })
        
        return request.app.state.templates.TemplateResponse(
            "views/breeders.html",
            context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading breeders: {str(e)}")


@router.get("/{breeder_id}", name="breeder_detail_page")
async def breeder_detail_page(
    request: Request,
    breeder_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Display breeder detail page with their strains."""
    try:
        result = await db.execute(
            select(Breeder).options(selectinload(Breeder.cultivars)).where(Breeder.id == breeder_id)
        )
        breeder = result.scalar_one_or_none()
        
        if not breeder:
            raise HTTPException(status_code=404, detail="Breeder not found")
        
        breeder_data = {
            'id': breeder.id,
            'name': breeder.name,
            'cultivar_count': len(breeder.cultivars) if breeder.cultivars else 0,
            'cultivars': []
        }
        
        # Add cultivar data if available
        if breeder.cultivars:
            for cultivar in breeder.cultivars:
                breeder_data['cultivars'].append({
                    'id': cultivar.id,
                    'name': cultivar.name,
                    'indica': cultivar.indica or 0,
                    'sativa': cultivar.sativa or 0,
                    'autoflower': cultivar.autoflower or False,
                    'description': cultivar.description
                })
        
        context.update({
            "breeder": breeder_data,
        })
        
        return request.app.state.templates.TemplateResponse(
            "views/breeder.html",
            context
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading breeder: {str(e)}")


# ============================================================================
# Clean JSON API Contracts
# ============================================================================

class BreederListApiResponse(BaseModel):
    """Response model for breeder list API following newsletter pattern."""
    items: List[BreederResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_prev: bool


@api_router.get("/list", response_model=BreederListApiResponse, name="api_breeders_list")
async def api_breeders_list(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
):
    """Get paginated list of breeders with search - Clean JSON API."""
    try:
        # Build base query
        query = select(Breeder).options(selectinload(Breeder.cultivars))
        
        # Apply search filter
        if search:
            query = query.where(Breeder.name.contains(search))
        
        # Get total count
        count_query = select(func.count(Breeder.id))
        if search:
            count_query = count_query.where(Breeder.name.contains(search))
        
        result = await db.execute(count_query)
        total = result.scalar() or 0
        
        # Apply pagination and ordering
        query = query.order_by(Breeder.name).offset((page - 1) * page_size).limit(page_size)
        
        # Execute main query
        result = await db.execute(query)
        breeders = result.scalars().all()
        
        # Transform to response format
        items = []
        for breeder in breeders:
            cultivar_count = len(breeder.cultivars) if breeder.cultivars else 0
            items.append(BreederResponse(
                id=breeder.id,
                name=breeder.name,
                cultivar_count=cultivar_count
            ))
        
        return BreederListApiResponse(**create_paginated_response(items, total, page, page_size))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching breeders: {str(e)}")


@api_router.get("/{breeder_id}", response_model=BreederResponse, name="api_breeder_get")
async def api_breeder_get(
    breeder_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Get breeder details - Clean JSON API."""
    try:
        result = await db.execute(
            select(Breeder).options(selectinload(Breeder.cultivars)).where(Breeder.id == breeder_id)
        )
        breeder = result.scalar_one_or_none()
        
        if not breeder:
            raise HTTPException(status_code=404, detail="Breeder not found")
        
        cultivar_count = len(breeder.cultivars) if breeder.cultivars else 0
        
        return BreederResponse(
            id=breeder.id,
            name=breeder.name,
            cultivar_count=cultivar_count
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching breeder: {str(e)}")


@api_router.post("/", response_model=BreederCreateResponse, name="api_breeder_create")
async def api_breeder_create(
    breeder_data: BreederCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Create a new breeder - Clean JSON API."""
    try:
        # Check for existing breeder with same name
        result = await db.execute(select(Breeder).where(func.lower(Breeder.name) == breeder_data.name.lower()))
        existing = result.scalar_one_or_none()
        
        if existing:
            raise HTTPException(status_code=400, detail="Breeder with this name already exists")
        
        # Create breeder
        breeder = Breeder(name=breeder_data.name)
        
        db.add(breeder)
        await db.commit()
        await db.refresh(breeder)
        
        return BreederCreateResponse(
            message="Breeder created successfully",
            status="created",
            breeder_id=breeder.id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating breeder: {str(e)}")


@api_router.put("/{breeder_id}", response_model=BreederUpdateResponse, name="api_breeder_update")
async def api_breeder_update(
    breeder_id: int,
    breeder_data: BreederUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Update an existing breeder - Clean JSON API."""
    try:
        result = await db.execute(select(Breeder).where(Breeder.id == breeder_id))
        breeder = result.scalar_one_or_none()
        
        if not breeder:
            raise HTTPException(status_code=404, detail="Breeder not found")
        
        # Check for name conflicts if name is being updated
        if breeder_data.name and breeder_data.name.lower() != breeder.name.lower():
            result = await db.execute(
                select(Breeder).where(
                    and_(
                        func.lower(Breeder.name) == breeder_data.name.lower(),
                        Breeder.id != breeder_id
                    )
                )
            )
            existing = result.scalar_one_or_none()
            if existing:
                raise HTTPException(status_code=400, detail="Breeder with this name already exists")
        
        # Update fields
        update_data = breeder_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(breeder, key, value)
        
        await db.commit()
        
        return BreederUpdateResponse(
            message="Breeder updated successfully",
            status="updated"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating breeder: {str(e)}")


@api_router.delete("/{breeder_id}", response_model=BreederDeleteResponse, name="api_breeder_delete")
async def api_breeder_delete(
    breeder_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Delete a breeder - Clean JSON API."""
    try:
        result = await db.execute(select(Breeder).where(Breeder.id == breeder_id))
        breeder = result.scalar_one_or_none()
        
        if not breeder:
            raise HTTPException(status_code=404, detail="Breeder not found")
        
        # Check if breeder has associated cultivars
        result = await db.execute(select(func.count(Cultivar.id)).where(Cultivar.breeder_id == breeder_id))
        cultivar_count = result.scalar() or 0
        
        if cultivar_count > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot delete breeder with {cultivar_count} associated cultivars"
            )
        
        await db.delete(breeder)
        await db.commit()
        
        return BreederDeleteResponse(
            message="Breeder deleted successfully",
            status="deleted"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting breeder: {str(e)}")


@api_router.get("/stats/summary", response_model=BreederStats, name="api_breeder_stats")
async def api_breeder_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Get breeder statistics - Clean JSON API."""
    try:
        # Get total breeders count
        result = await db.execute(select(func.count(Breeder.id)))
        total_breeders = result.scalar() or 0
        
        # Get most prolific breeder (breeder with most cultivars)
        result = await db.execute(
            select(Breeder.name, func.count(Cultivar.id))
            .outerjoin(Cultivar, Breeder.id == Cultivar.breeder_id)
            .group_by(Breeder.id, Breeder.name)
            .order_by(func.count(Cultivar.id).desc())
            .limit(1)
        )
        top_breeder_data = result.first()
        
        most_prolific_breeder = top_breeder_data[0] if top_breeder_data else None
        total_cultivars_from_top_breeder = top_breeder_data[1] if top_breeder_data else 0
        
        return BreederStats(
            total_breeders=total_breeders,
            most_prolific_breeder=most_prolific_breeder,
            total_cultivars_from_top_breeder=total_cultivars_from_top_breeder
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching breeder stats: {str(e)}")


# Note: This router needs to be included in the main FastAPI app with both routers
# In __init__.py: app.include_router(breeders.router, tags=["Breeders Legacy"])
#                app.include_router(breeders.api_router, prefix="/api/v1", tags=["Breeders API"])
