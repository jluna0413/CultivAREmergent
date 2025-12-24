import os
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import HTTPException
from starlette import status
from starlette.responses import JSONResponse

from app.fastapi_app.dependencies import inject_template_context, get_cors_origins
from app.fastapi_app.middleware.flash import FlashMiddleware
from app.fastapi_app.middleware.csrf import CSRFMiddleware
from app.fastapi_app.middleware.logging import RequestLoggingMiddleware, PerformanceMonitoringMiddleware, SecurityMonitoringMiddleware
from app.fastapi_app.middleware.security import SecurityHeadersMiddleware, RateLimitMiddleware
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.fastapi_app.routers import (
    activities,
    admin,
    auth, # New auth router
    blog,
    breeders,
    clones,
    cultivars,
    cultivars_legacy,
    dashboard,
    files, # New files router
    health,
    marketing,
    newsletter,
    nutrients, # Nutrients router
    plants, # New plants router
    plants_api, # New plants_api router
    routes, # New routes router
    sensors, # New sensors router
    social,
    strains,
    users,
    websocket, # New websocket router
    zones, # New zones router
    context, # New context router
    ai, # New ai router
)
from app.routers import agents as agents_router  # Agent Hub router


# Initialize FastAPI app
app = FastAPI()

# Environment variable validation function
def get_required_secret(key: str, description: str) -> str:
    """Get required secret from environment, raising error if not set."""
    value = os.environ.get(key)
    if not value:
        raise ValueError(
            f"Required {description} not found in environment variable {key}. "
            f"Please set this environment variable before starting the application."
        )
    return value

# Validate required secret keys before adding middleware
try:
    SESSION_SECRET_KEY = get_required_secret("SESSION_SECRET_KEY", "session secret key")
    CSRF_SECRET_KEY = get_required_secret("CSRF_SECRET_KEY", "CSRF secret key")
    FLASH_SECRET_KEY = get_required_secret("FLASH_SECRET_KEY", "flash secret key")
    print("[OK] All required secret keys validated successfully")
except ValueError as e:
    print(f"[ERROR] CRITICAL ERROR: {e}")
    print("Application cannot start without proper environment variables.")
    raise

# Add Session Middleware for flash messages (with proper validation)
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)



# Custom Middleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(PerformanceMonitoringMiddleware)
app.add_middleware(SecurityMonitoringMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Rate Limiting Middleware
app.add_middleware(RateLimitMiddleware, limit=100, window=60)

# CSRF Middleware (using validated CSRF_SECRET_KEY)
app.add_middleware(CSRFMiddleware, secret=CSRF_SECRET_KEY, exclude_paths=["/api/"])

# Flash Messages Middleware (using validated FLASH_SECRET_KEY)
app.add_middleware(FlashMiddleware, secret_key=FLASH_SECRET_KEY)

# CORS Middleware (Outermost - added last)
origins = get_cors_origins()
print(f"DEBUG: Loaded CORS origins: {origins}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")

# Configure Jinja2Templates
templates = Jinja2Templates(directory="app/web/templates")
app.state.templates = templates # Make templates accessible via app.state

# Include routers
# HTML Routers (legacy support or direct HTML rendering)
app.include_router(routes.router, tags=["General HTML"]) # General routes like /, /waitlist, /downloads
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(marketing.router, prefix="/marketing", tags=["Marketing HTML"])
app.include_router(newsletter.router, prefix="/newsletter", tags=["Newsletter HTML"])
app.include_router(social.router, prefix="/social", tags=["Social HTML"])
app.include_router(strains.router, prefix="/strains", tags=["Strains HTML"])
app.include_router(breeders.router, prefix="/breeders", tags=["Breeders HTML"])
app.include_router(clones.router, prefix="/clones", tags=["Clones HTML"])
app.include_router(admin.router, prefix="/admin", tags=["Admin HTML"])
app.include_router(zones.router, prefix="/zones", tags=["Zones HTML"])
app.include_router(files.router, prefix="/files", tags=["Files"]) # New files router
app.include_router(plants.router, prefix="/plants", tags=["Plants HTML"]) # New plants HTML router
app.include_router(sensors.router, prefix="/sensors", tags=["Sensors HTML"]) # New sensors HTML router
app.include_router(activities.router, prefix="/activities", tags=["Activities HTML"])

# API Routers (JSON contracts)
app.include_router(activities.api_router, prefix="/api/v1/activities", tags=["Activities API"])
app.include_router(auth.api_router, prefix="/api/v1/auth", tags=["Auth API"])
app.include_router(blog.router, prefix="/api/v1/blog", tags=["Blog API"])
app.include_router(breeders.api_router, prefix="/api/v1/breeders", tags=["Breeders API"])
app.include_router(clones.api_router, prefix="/api/v1/clones", tags=["Clones API"])
app.include_router(cultivars.router, prefix="/api/v1/cultivars", tags=["Cultivars API"])
app.include_router(cultivars_legacy.router, prefix="/api/v1/cultivars-legacy", tags=["Cultivars Legacy API"])
app.include_router(health.router, prefix="/health", tags=["Health & Monitoring"])
app.include_router(marketing.api_router, prefix="/api/v1/marketing", tags=["Marketing API"])
app.include_router(newsletter.api_router, prefix="/api/v1/newsletter", tags=["Newsletter API"])
app.include_router(plants_api.router, prefix="/api/v1/plants", tags=["Plants API"]) # New plants API router
app.include_router(sensors.api_router, prefix="/api/v1/sensors", tags=["Sensors API"]) # New sensors API router
app.include_router(users.api_router, prefix="/api/v1/users", tags=["Users API"])
app.include_router(zones.api_router, prefix="/api/v1/zones", tags=["Zones API"]) # New zones API router
app.include_router(context.router, prefix="", tags=["Context API"]) # Context API
app.include_router(ai.router, prefix="", tags=["AI Agent"]) # AI Agent API
app.include_router(nutrients.router, tags=["Nutrients API"])
app.include_router(agents_router.router, tags=["Agents API"])  # Agent Hub API


# WebSocket Router
app.include_router(websocket.router, prefix="/ws", tags=["WebSockets"]) # New websocket router


@app.get("/", response_class=HTMLResponse, name="root")
async def root(request: Request, context: dict = Depends(inject_template_context)):
    """Root endpoint - redirects to marketing home or dashboard if logged in."""
    # This logic might need to be adjusted based on actual authentication status
    # For now, let's redirect to marketing home
    return RedirectResponse(url=request.url_for("site_home"), status_code=status.HTTP_302_FOUND)

# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Global handler for StarletteHTTPException.
    Returns JSON for API paths, HTML for others.
    """
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )
    
    context = await inject_template_context(request)
    if exc.status_code == 404:
        context["title"] = "Page Not Found"
        context["request"] = request
        return templates.TemplateResponse("marketing/404.html", context, status_code=status.HTTP_404_NOT_FOUND)
    
    # For other client errors, you might want a generic error page
    # For now, we focus on 404 and 500
    
    # Default to a JSON response if not a 404, and not an API path (could be other client errors)
    # Or, more gracefully, show a generic error page
    context["title"] = "Error"
    context["detail"] = exc.detail
    context["request"] = request
    return templates.TemplateResponse("marketing/500.html", context, status_code=exc.status_code)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    Global handler for FastAPI's HTTPException.
    Returns JSON for API paths, HTML for others.
    """
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )

    context = await inject_template_context(request)
    if exc.status_code == 404:
        context["title"] = "Page Not Found"
        context["request"] = request
        return templates.TemplateResponse("marketing/404.html", context, status_code=status.HTTP_404_NOT_FOUND)
    
    # Generic error page for other HTTP exceptions on web routes
    context["title"] = "An Error Occurred"
    context["detail"] = exc.detail
    context["request"] = request
    return templates.TemplateResponse("marketing/500.html", context, status_code=exc.status_code)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Global handler for any other unhandled exception.
    Returns JSON for API paths, HTML for others.
    This is a catch-all for 500 Internal Server Errors.
    """
    # In a production environment, you would log the exception details
    # from exc, like traceback.
    
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal Server Error"}
        )
    
    context = await inject_template_context(request)
    context["title"] = "Server Error"
    context["request"] = request
    return templates.TemplateResponse("marketing/500.html", context, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
