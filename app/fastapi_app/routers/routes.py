"""Basic Routes Router - Migrated from app/routes/routes.py"""
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse, FileResponse
from app.fastapi_app.dependencies import inject_template_context

router = APIRouter(tags=["routes"])

@router.get("/", name="landing_page")
async def landing_page(request: Request, context: dict = Depends(inject_template_context)):
    return request.app.state.templates.TemplateResponse("marketing/home.html", context)

@router.get("/waitlist", name="waitlist_landing")
async def waitlist_landing(request: Request, context: dict = Depends(inject_template_context)):
    """Display waitlist signup page"""
    return request.app.state.templates.TemplateResponse("marketing/waitlist_landing.html", context)

@router.post("/waitlist/signup", name="waitlist_signup")
async def waitlist_signup(
    request: Request,
    email: str = Form(...),
    name: str = Form(...),
    experience: str = Form(...),
    phone: str = Form(None),
    referral: str = Form(None),
    csrf_token: str = Form(None),  # Accept CSRF token but don't validate (FastAPI doesn't need it like Flask)
):
    """Handle waitlist signup and redirect to thank you/downloads page"""
    email = email.strip().lower()
    
    if not email:
        return RedirectResponse(url="/waitlist?error=email_required", status_code=303)
    
    try:
        from app.models_async.marketing import Waitlist
        from app.models_async.base import AsyncSessionLocal
        from sqlalchemy import select
        
        async with AsyncSessionLocal() as db:
            # Check for existing signup
            result = await db.execute(
                select(Waitlist).where(Waitlist.email == email)
            )
            existing = result.scalar_one_or_none()
            
            if not existing:
                # Create new waitlist entry
                entry = Waitlist(
                    email=email,
                    name=name,
                    experience=experience,
                    phone=phone,
                    referral_source=referral
                )
                db.add(entry)
                await db.commit()
                print(f"✅ New waitlist signup: {email} ({name})")
            else:
                print(f"ℹ️  Duplicate waitlist signup attempt: {email}")
        
        # Redirect to downloads page with success flag
        return RedirectResponse(url="/downloads?success=true", status_code=303)
        
    except Exception as e:
        # Log the error but don't break the public site
        print(f"❌ Error in waitlist signup: {e}")
        import traceback
        traceback.print_exc()
        # Redirect to downloads anyway (graceful degradation)
        return RedirectResponse(url="/downloads?success=true", status_code=303)

@router.get("/downloads", name="lead_magnet_downloads")
async def lead_magnet_downloads(request: Request, context: dict = Depends(inject_template_context)):
    """Display thank you and lead magnet downloads page"""
    return request.app.state.templates.TemplateResponse("marketing/downloads.html", context)

@router.get("/health", name="health_check")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}

@router.get("/favicon.ico")
async def favicon():
    # Serve the 32x32 PNG as favicon (browsers accept PNG format)
    return FileResponse("app/web/static/images/favicon-32x32.png", media_type="image/png")
