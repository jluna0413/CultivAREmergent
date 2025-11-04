"""Diagnostics Router - Migrated from app/blueprints/diagnostics.py"""
from fastapi import APIRouter, Request, Depends
from app.fastapi_app.dependencies import require_login, inject_template_context
from app.models_async.auth import User

router = APIRouter(prefix="/diagnostics", tags=["diagnostics"])

@router.get("/", name="diagnostics_page")
async def diagnostics_page(request: Request, current_user: User = Depends(require_login), context: dict = Depends(inject_template_context)):
    return request.app.state.templates.TemplateResponse("views/diagnostics.html", context)
