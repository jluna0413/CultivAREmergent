"""
Zones Router - Manages grow zones.
"""

from fastapi import APIRouter, Request, Depends, HTTPException, status, Form, Query
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any

from app.fastapi_app.dependencies import require_login, inject_template_context
from app.models_async.base import get_async_session as get_async_db
from app.models_async.auth import User
from app.models_async.grow import Zone, Plant
from app.fastapi_app.middleware.flash import flash
from app.logger import logger

router = APIRouter(tags=["zones"])
api_router = APIRouter(tags=["zones-api"])


# ============================================================================
# Helper Functions
# ============================================================================

async def get_zone_details(db: AsyncSession, zone_id: int, user_id: int) -> Optional[Zone]:
    """Helper to get a zone by ID, ensuring it belongs to the user."""
    result = await db.execute(
        select(Zone)
        .where(Zone.id == zone_id, Zone.user_id == user_id)
        .options(selectinload(Zone.plants))
    )
    return result.scalar_one_or_none()


# ============================================================================
# HTML Routes
# ============================================================================

@router.get("/", name="zones_list_page")
async def zones_list_page(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Render the zones list page."""
    try:
        result = await db.execute(
            select(Zone)
            .where(Zone.user_id == current_user.id)
            .options(selectinload(Zone.plants))
            .order_by(Zone.name)
        )
        zones = result.scalars().all()

        zones_data = []
        for zone in zones:
            zones_data.append({
                "id": zone.id,
                "name": zone.name,
                "description": zone.description,
                "plant_count": len(zone.plants) if zone.plants else 0,
                "created_at": zone.created_at,
                "updated_at": zone.updated_at,
            })

        context.update({
            "title": "Grow Zones",
            "zones": zones_data,
        })
        return request.app.state.templates.TemplateResponse(
            "views/zones.html",
            context
        )
    except Exception as e:
        logger.error(f"Error loading zones for user {current_user.id}: {e}")
        flash(request, "Error loading grow zones.", "danger")
        return RedirectResponse(url=request.url_for("dashboard_dashboard"), status_code=status.HTTP_302_FOUND)


@router.get("/add", name="zones_add_page")
async def zones_add_page(
    request: Request,
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Render the add zone page."""
    context.update({
        "title": "Add New Grow Zone",
    })
    return request.app.state.templates.TemplateResponse(
        "views/add_zone.html",
        context
    )


@router.post("/add", name="zones_add")
async def zones_add(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    name: str = Form(...),
    description: Optional[str] = Form(None),
):
    """Handle form submission for adding a new zone."""
    try:
        # Check if zone name already exists for this user
        existing_result = await db.execute(
            select(Zone).where(Zone.user_id == current_user.id, Zone.name == name)
        )
        if existing_result.scalar_one_or_none():
            flash(request, f"A zone named '{name}' already exists.", "danger")
            return RedirectResponse(url=request.url_for("zones_add_page"), status_code=status.HTTP_302_FOUND)

        new_zone = Zone(
            name=name,
            description=description,
            user_id=current_user.id
        )
        db.add(new_zone)
        await db.commit()
        await db.refresh(new_zone)

        flash(request, f"Zone '{new_zone.name}' added successfully!", "success")
        return RedirectResponse(url=request.url_for("zones_list_page"), status_code=status.HTTP_302_FOUND)
    except Exception as e:
        logger.error(f"Error adding zone for user {current_user.id}: {e}")
        await db.rollback()
        flash(request, "Error adding new grow zone.", "danger")
        return RedirectResponse(url=request.url_for("zones_add_page"), status_code=status.HTTP_302_FOUND)


@router.get("/{zone_id}/edit", name="zones_edit_page")
async def zones_edit_page(
    request: Request,
    zone_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Render the edit zone page."""
    zone = await get_zone_details(db, zone_id, current_user.id)
    if not zone:
        flash(request, "Zone not found.", "danger")
        return RedirectResponse(url=request.url_for("zones_list_page"), status_code=status.HTTP_302_FOUND)

    context.update({
        "title": f"Edit Zone: {zone.name}",
        "zone": zone,
    })
    return request.app.state.templates.TemplateResponse(
        "views/edit_zone.html",
        context
    )


@router.post("/{zone_id}/edit", name="zones_edit")
async def zones_edit(
    request: Request,
    zone_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    name: str = Form(...),
    description: Optional[str] = Form(None),
):
    """Handle form submission for editing an existing zone."""
    try:
        zone = await get_zone_details(db, zone_id, current_user.id)
        if not zone:
            flash(request, "Zone not found.", "danger")
            return RedirectResponse(url=request.url_for("zones_list_page"), status_code=status.HTTP_302_FOUND)

        # Check for name conflict if name is changed
        if zone.name != name:
            existing_result = await db.execute(
                select(Zone).where(Zone.user_id == current_user.id, Zone.name == name)
            )
            if existing_result.scalar_one_or_none():
                flash(request, f"A zone named '{name}' already exists.", "danger")
                return RedirectResponse(url=request.url_for("zones_edit_page", zone_id=zone_id), status_code=status.HTTP_302_FOUND)

        zone.name = name
        zone.description = description
        await db.commit()
        await db.refresh(zone)

        flash(request, f"Zone '{zone.name}' updated successfully!", "success")
        return RedirectResponse(url=request.url_for("zones_list_page"), status_code=status.HTTP_302_FOUND)
    except Exception as e:
        logger.error(f"Error editing zone {zone_id} for user {current_user.id}: {e}")
        await db.rollback()
        flash(request, "Error updating grow zone.", "danger")
        return RedirectResponse(url=request.url_for("zones_edit_page", zone_id=zone_id), status_code=status.HTTP_302_FOUND)


@router.post("/{zone_id}/delete", name="zones_delete")
async def zones_delete(
    request: Request,
    zone_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Handle deletion of a zone."""
    try:
        zone = await get_zone_details(db, zone_id, current_user.id)
        if not zone:
            flash(request, "Zone not found.", "danger")
            return RedirectResponse(url=request.url_for("zones_list_page"), status_code=status.HTTP_302_FOUND)

        # Check if there are plants in this zone
        if zone.plants:
            flash(request, f"Cannot delete zone '{zone.name}' because it contains {len(zone.plants)} plants.", "danger")
            return RedirectResponse(url=request.url_for("zones_list_page"), status_code=status.HTTP_302_FOUND)

        await db.delete(zone)
        await db.commit()

        flash(request, f"Zone '{zone.name}' deleted successfully!", "success")
        return RedirectResponse(url=request.url_for("zones_list_page"), status_code=status.HTTP_302_FOUND)
    except Exception as e:
        logger.error(f"Error deleting zone {zone_id} for user {current_user.id}: {e}")
        await db.rollback()
        flash(request, "Error deleting grow zone.", "danger")
        return RedirectResponse(url=request.url_for("zones_list_page"), status_code=status.HTTP_302_FOUND)


# ============================================================================
# API Routes
# ============================================================================

class ZoneResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    plant_count: int
    created_at: datetime
    updated_at: datetime

class ZoneListResponse(BaseModel):
    items: List[ZoneResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_prev: bool

class ZoneCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ZoneUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


@api_router.get("/", response_model=ZoneListResponse, name="api_zones_list")
async def api_zones_list(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by zone name or description"),
):
    """Get paginated list of user's grow zones."""
    query = select(Zone).where(Zone.user_id == current_user.id)
    count_query = select(func.count(Zone.id)).where(Zone.user_id == current_user.id)

    if search:
        search_pattern = f"%{search}%"
        query = query.where(or_(Zone.name.ilike(search_pattern), Zone.description.ilike(search_pattern)))
        count_query = count_query.where(or_(Zone.name.ilike(search_pattern), Zone.description.ilike(search_pattern)))

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.order_by(Zone.name).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query.options(selectinload(Zone.plants)))
    zones = result.scalars().all()

    items = []
    for zone in zones:
        items.append(ZoneResponse(
            id=zone.id,
            name=zone.name,
            description=zone.description,
            plant_count=len(zone.plants) if zone.plants else 0,
            created_at=zone.created_at,
            updated_at=zone.updated_at,
        ))
    
    pages = (total + page_size - 1) // page_size if total > 0 else 0

    return ZoneListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1
    )


@api_router.get("/{zone_id}", response_model=ZoneResponse, name="api_zones_get")
async def api_zones_get(
    zone_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Get details for a specific grow zone."""
    zone = await get_zone_details(db, zone_id, current_user.id)
    if not zone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zone not found")
    
    return ZoneResponse(
        id=zone.id,
        name=zone.name,
        description=zone.description,
        plant_count=len(zone.plants) if zone.plants else 0,
        created_at=zone.created_at,
        updated_at=zone.updated_at,
    )


@api_router.post("/", response_model=ZoneResponse, status_code=status.HTTP_201_CREATED, name="api_zones_create")
async def api_zones_create(
    zone_data: ZoneCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Create a new grow zone."""
    existing_result = await db.execute(
        select(Zone).where(Zone.user_id == current_user.id, Zone.name == zone_data.name)
    )
    if existing_result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"A zone named '{zone_data.name}' already exists.")

    new_zone = Zone(
        name=zone_data.name,
        description=zone_data.description,
        user_id=current_user.id
    )
    db.add(new_zone)
    await db.commit()
    await db.refresh(new_zone)

    return ZoneResponse(
        id=new_zone.id,
        name=new_zone.name,
        description=new_zone.description,
        plant_count=0,
        created_at=new_zone.created_at,
        updated_at=new_zone.updated_at,
    )


@api_router.put("/{zone_id}", response_model=ZoneResponse, name="api_zones_update")
async def api_zones_update(
    zone_id: int,
    zone_data: ZoneUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Update an existing grow zone."""
    zone = await get_zone_details(db, zone_id, current_user.id)
    if not zone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zone not found")

    if zone_data.name and zone.name != zone_data.name:
        existing_result = await db.execute(
            select(Zone).where(Zone.user_id == current_user.id, Zone.name == zone_data.name)
        )
        if existing_result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"A zone named '{zone_data.name}' already exists.")

    update_dict = zone_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(zone, key, value)
    
    await db.commit()
    await db.refresh(zone)

    return ZoneResponse(
        id=zone.id,
        name=zone.name,
        description=zone.description,
        plant_count=len(zone.plants) if zone.plants else 0,
        created_at=zone.created_at,
        updated_at=zone.updated_at,
    )


@api_router.delete("/{zone_id}", status_code=status.HTTP_204_NO_CONTENT, name="api_zones_delete")
async def api_zones_delete(
    zone_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Delete a grow zone."""
    zone = await get_zone_details(db, zone_id, current_user.id)
    if not zone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zone not found")

    if zone.plants:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot delete zone '{zone.name}' because it contains {len(zone.plants)} plants.")

    await db.delete(zone)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
