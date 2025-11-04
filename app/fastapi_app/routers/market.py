"""Market Router - Migrated from app/blueprints/market.py"""
from fastapi import APIRouter, Request, Depends
from app.fastapi_app.dependencies import require_login, inject_template_context
from app.models_async.auth import User

router = APIRouter(prefix="/market", tags=["market"])

@router.get("/seed-bank", name="market_seed_bank")
async def seed_bank(request: Request, current_user: User = Depends(require_login), context: dict = Depends(inject_template_context)):
    context.update({
        "page_title": "Seed Bank",
        "page_description": "Browse and purchase cannabis seeds from top breeders. Coming soon!"
    })
    return request.app.state.templates.TemplateResponse("views/coming_soon.html", context)

@router.get("/extensions", name="market_extensions")
async def extensions(request: Request, current_user: User = Depends(require_login), context: dict = Depends(inject_template_context)):
    """Extensions/plugins marketplace page."""
    context.update({
        "page_title": "Extensions",
        "page_description": "Browse and install extensions for CultivAR. Coming soon!"
    })
    return request.app.state.templates.TemplateResponse("views/coming_soon.html", context)

@router.get("/gear", name="market_gear")
async def gear(request: Request, current_user: User = Depends(require_login), context: dict = Depends(inject_template_context)):
    """Growing equipment and gear marketplace page."""
    context.update({
        "page_title": "Gear",
        "page_description": "Browse growing equipment and supplies. Coming soon!"
    })
    return request.app.state.templates.TemplateResponse("views/coming_soon.html", context)

@router.get("/cart", name="market_cart")
async def cart(request: Request, current_user: User = Depends(require_login), context: dict = Depends(inject_template_context)):
    """Shopping cart page."""
    context.update({
        "page_title": "Shopping Cart",
        "page_description": "View and manage your shopping cart. Coming soon!"
    })
    return request.app.state.templates.TemplateResponse("views/coming_soon.html", context)
