"""
Strains Router
Manages strain collection and individual strain details.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.fastapi_app.dependencies import require_login, inject_template_context
from app.models_async.base import get_async_session as get_async_db
from app.models_async.auth import User
from app.models_async.grow import Cultivar, Breeder # Changed Strain to Cultivar
from app.fastapi_app.middleware.flash import flash
from app.handlers_async import strain_handlers, breeder_handlers
from app.logger import logger

router = APIRouter(tags=["strains"])

@router.get("/", name="strains_page")
@router.get("/strains", name="strains_page_collection") # Alternative route
async def strains_page(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Render the strains collection page."""
    cultivars_data = []
    breeders_list = []

    try:
        cultivars_result = await db.execute(
            select(Cultivar).options(selectinload(Cultivar.breeder))
        )
        cultivars = cultivars_result.scalars().all()

        for cultivar in cultivars:
            breeder_name = cultivar.breeder.name if cultivar.breeder else 'Unknown'
            cultivars_data.append({
                'id': cultivar.id,
                'name': cultivar.name,
                'breeder_id': cultivar.breeder_id,
                'breeder_name': breeder_name,
                'indica': cultivar.indica,
                'sativa': cultivar.sativa,
                'autoflower': cultivar.autoflower,
                'cycle_time': cultivar.cycle_time,
                'seed_count': cultivar.seed_count,
                'url': cultivar.url,
                'description': cultivar.description,
                'short_description': cultivar.description[:100] + '...' if cultivar.description and len(cultivar.description) > 100 else cultivar.description or '',
                'type': 'indica' if cultivar.indica > cultivar.sativa else ('sativa' if cultivar.sativa > cultivar.indica else 'hybrid'),
                'parent_1': cultivar.parent_1,
                'parent_2': cultivar.parent_2,
                'lineage_json': cultivar.lineage_json,
                'seedfinder_id': cultivar.seedfinder_id,
                'thc_content': cultivar.thc_content,
                'cbd_content': cultivar.cbd_content,
                'flowering_type': cultivar.flowering_type,
                'categories': cultivar.categories,
            })

        breeders_result = await db.execute(select(Breeder))
        breeders_list = [{'id': b.id, 'name': b.name} for b in breeders_result.scalars().all()]

    except Exception as e:
        logger.error(f"Error loading cultivars data: {e}")
        flash(request, "Error loading cultivars data.", "danger")

    context.update({
        "title": "Collection",
        "strains": cultivars_data,
        "breeders": breeders_list
    })
    return request.app.state.templates.TemplateResponse(
        "views/strains.html",
        context
    )


@router.get("/{cultivar_id}", name="strain_detail") # Changed to cultivar_id
async def strain_detail(
    request: Request,
    cultivar_id: int, # Changed to cultivar_id
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Render individual strain detail page."""
    try:
        cultivar_result = await db.execute( # Changed to cultivar_result
            select(Cultivar) # Changed to Cultivar
            .where(Cultivar.id == cultivar_id) # Changed to cultivar_id
            .options(selectinload(Cultivar.breeder))
        )
        cultivar = cultivar_result.scalar_one_or_none() # Changed to cultivar

        if not cultivar:
            flash(request, "Cultivar not found.", "danger")
            return RedirectResponse(url=request.url_for("strains_page"), status_code=status.HTTP_302_FOUND)

        breeder_name = cultivar.breeder.name if cultivar.breeder else 'Unknown'

        cultivar_data = { # Changed to cultivar_data
            'id': cultivar.id,
            'name': cultivar.name,
            'breeder_id': cultivar.breeder_id,
            'breeder_name': breeder_name,
            'indica': cultivar.indica,
            'sativa': cultivar.sativa,
            'autoflower': cultivar.autoflower,
            'cycle_time': cultivar.cycle_time,
            'seed_count': cultivar.seed_count,
            'url': cultivar.url,
            'description': cultivar.description,
            'short_description': cultivar.description[:100] + '...' if cultivar.description and len(cultivar.description) > 100 else cultivar.description or '',
            'parent_1': cultivar.parent_1,
            'parent_2': cultivar.parent_2,
            'lineage_json': cultivar.lineage_json,
            'seedfinder_id': cultivar.seedfinder_id,
            'thc_content': cultivar.thc_content,
            'cbd_content': cultivar.cbd_content,
            'flowering_type': cultivar.flowering_type,
            'categories': cultivar.categories,
        }
        
        breeders_result = await db.execute(select(Breeder))
        breeders_list = breeders_result.scalars().all()

        context.update({
            "title": f"Cultivar: {cultivar.name}", # Changed to cultivar.name
            "strain": cultivar_data, # Changed to cultivar_data
            "breeders": breeders_list
        })
        return request.app.state.templates.TemplateResponse(
            "views/strain.html",
            context
        )

    except Exception as e:
        logger.error(f"Error loading cultivar {cultivar_id}: {e}") # Changed to cultivar_id
        flash(request, "Error loading cultivar details.", "danger")
        return RedirectResponse(url=request.url_for("strains_page"), status_code=status.HTTP_302_FOUND)


@router.get("/add", name="add_strain_page")
@router.get("/strains/add", name="add_strain_page_legacy") # Alternative route
async def add_strain_page(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Render the add strain page."""
    breeders_result = await db.execute(select(Breeder))
    breeders_list = breeders_result.scalars().all()

    context.update({
        "title": "Add New Cultivar", # Changed to Cultivar
        "breeders": breeders_list # Pass actual breeders from DB
    })
    return request.app.state.templates.TemplateResponse(
        "views/add_strain.html",
        context
    )

@router.post("/add", name="add_strain")
async def add_strain(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    name: str = Form(...),
    breeder_id: Optional[int] = Form(None),
    indica: int = Form(0),
    sativa: int = Form(0),
    autoflower: bool = Form(False),
    cycle_time: Optional[int] = Form(None),
    seed_count: int = Form(0),
    url: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    parent_1: Optional[str] = Form(None),
    parent_2: Optional[str] = Form(None),
    lineage_json: Optional[str] = Form(None),
    seedfinder_id: Optional[str] = Form(None),
    thc_content: Optional[float] = Form(None),
    cbd_content: Optional[float] = Form(None),
    flowering_type: Optional[str] = Form(None),
    categories: Optional[str] = Form(None),
):
    """Handle form submission for adding a new strain."""
    cultivar_data = { # Changed to cultivar_data
        "name": name,
        "breeder_id": breeder_id if breeder_id else None,
        "indica": indica,
        "sativa": sativa,
        "autoflower": autoflower,
        "cycle_time": cycle_time,
        "seed_count": seed_count,
        "url": url,
        "description": description,
        "parent_1": parent_1,
        "parent_2": parent_2,
        "lineage_json": json.loads(lineage_json) if lineage_json else None,
        "seedfinder_id": seedfinder_id,
        "thc_content": thc_content,
        "cbd_content": cbd_content,
        "flowering_type": flowering_type,
        "categories": json.loads(categories) if categories else None,
    }

    result = await strain_handlers.add_cultivar_async(db, cultivar_data, current_user.id)

    if result["success"]:
        flash(request, result["message"], "success")
        return RedirectResponse(url=request.url_for("strains_page"), status_code=status.HTTP_302_FOUND)
    else:
        flash(request, result["error"], "danger")
        return RedirectResponse(url=request.url_for("add_strain_page"), status_code=status.HTTP_302_FOUND)

@router.post("/{cultivar_id}/edit", name="edit_strain") # Changed to cultivar_id
async def edit_strain(
    request: Request,
    cultivar_id: int, # Changed to cultivar_id
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    name: str = Form(...),
    breeder_id: Optional[int] = Form(None),
    indica: int = Form(0),
    sativa: int = Form(0),
    autoflower: bool = Form(False),
    cycle_time: Optional[int] = Form(None),
    seed_count: int = Form(0),
    url: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    parent_1: Optional[str] = Form(None),
    parent_2: Optional[str] = Form(None),
    lineage_json: Optional[str] = Form(None),
    seedfinder_id: Optional[str] = Form(None),
    thc_content: Optional[float] = Form(None),
    cbd_content: Optional[float] = Form(None),
    flowering_type: Optional[str] = Form(None),
    categories: Optional[str] = Form(None),
):
    """Handle form submission for editing an existing strain."""
    cultivar_data = { # Changed to cultivar_data
        "name": name,
        "breeder_id": breeder_id if breeder_id else None,
        "indica": indica,
        "sativa": sativa,
        "autoflower": autoflower,
        "cycle_time": cycle_time,
        "seed_count": seed_count,
        "url": url,
        "description": description,
        "parent_1": parent_1,
        "parent_2": parent_2,
        "lineage_json": json.loads(lineage_json) if lineage_json else None,
        "seedfinder_id": seedfinder_id,
        "thc_content": thc_content,
        "cbd_content": cbd_content,
        "flowering_type": flowering_type,
        "categories": json.loads(categories) if categories else None,
    }

    result = await strain_handlers.update_cultivar_async(db, cultivar_id, cultivar_data, current_user.id)

    if result["success"]:
        flash(request, result["message"], "success")
        return RedirectResponse(url=request.url_for("strain_detail", cultivar_id=cultivar_id), status_code=status.HTTP_302_FOUND) # Changed strain_id to cultivar_id
    else:
        flash(request, result["error"], "danger")
        return RedirectResponse(url=request.url_for("strain_detail", cultivar_id=cultivar_id), status_code=status.HTTP_302_FOUND) # Changed strain_id to cultivar_id

@router.post("/{cultivar_id}/delete", name="delete_strain") # Changed to cultivar_id
async def delete_strain(
    request: Request,
    cultivar_id: int, # Changed to cultivar_id
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Handle deletion of a strain."""
    result = await strain_handlers.delete_cultivar_async(db, cultivar_id, current_user.id)

    if result["success"]:
        flash(request, result["message"], "success")
        return RedirectResponse(url=request.url_for("strains_page"), status_code=status.HTTP_302_FOUND)
    else:
        flash(request, result["error"], "danger")
        return RedirectResponse(url=request.url_for("strain_detail", cultivar_id=cultivar_id), status_code=status.HTTP_302_FOUND) # Changed strain_id to cultivar_id

