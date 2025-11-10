"""
Cultivar Collection Management System - FastAPI Application
Main entry point for the FastAPI backend serving cultivar APIs
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
import os
from contextlib import asynccontextmanager

# Import routers (skip if FASTAPI_SKIP_ROUTERS is set - helpful for docs generation/test runs)
_SKIP_ROUTERS = os.getenv("FASTAPI_SKIP_ROUTERS", "0") == "1"
if not _SKIP_ROUTERS:
    from app.fastapi_app.routers import health
    from app.fastapi_app.routers import plants_api
    from app.fastapi_app.routers import dashboard
    from app.fastapi_app.routers import cultivars
    from app.fastapi_app.routers import cultivars_legacy
    from app.fastapi_app.routers import breeders
    from app.fastapi_app.routers import auth
    from app.fastapi_app.routers import admin
    from app.fastapi_app.routers import market
    from app.fastapi_app.routers import newsletter
    from app.fastapi_app.routers import site
    from app.fastapi_app.routers import clones
    from app.fastapi_app.routers import diagnostics
    from app.fastapi_app.routers import activities
    from app.fastapi_app.routers import blog
    from app.fastapi_app.routers import social

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Cultivar Collection Management System...")
    yield
    # Shutdown
    print("Shutting down Cultivar Collection Management System...")

# Create FastAPI application
app = FastAPI(
    title="Cultivar Collection Management API",
    description="Advanced cannabis cultivar tracking and analytics platform",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration - Updated for Comment 16
def get_cors_origins():
    """Get CORS origins from environment or use defaults"""
    origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
    return [origin.strip() for origin in origins if origin.strip()]

# Add CORS middleware with secure configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),  # Environment-driven origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],  # Specific methods
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-Requested-With",
        "Accept",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
        "X-CSRFToken"
    ],  # Specific headers
    expose_headers=["Content-Length", "Content-Range"]  # Expose headers
)

# Add Trusted Host middleware for security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.localhost", os.getenv("ALLOWED_HOSTS", "")]
)


# Include routers if they were imported
if not _SKIP_ROUTERS:
    app.include_router(health.router, prefix="/health", tags=["Health"])
    app.include_router(plants_api.router, prefix="/api/v1/plants", tags=["Plants"])
    app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
    app.include_router(cultivars.router, prefix="/api/v1/cultivars", tags=["Cultivars"])
    app.include_router(cultivars_legacy.router, prefix="/api/v1/strains", tags=["Strains (Legacy)"])
    app.include_router(breeders.api_router, prefix="/api/v1/breeders", tags=["Breeders"])
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(admin.api_router, prefix="/api/v1/admin", tags=["Admin"])
    app.include_router(market.router, prefix="/api/v1/market", tags=["Market"])
    app.include_router(newsletter.api_router, prefix="/api/v1/newsletter", tags=["Newsletter"])
    app.include_router(site.router, prefix="", tags=["Site"])
    app.include_router(clones.router, prefix="/api/v1/clones", tags=["Clones"])
    app.include_router(diagnostics.router, prefix="/api/v1/diagnostics", tags=["Diagnostics"])
    app.include_router(activities.api_router, prefix="/api/v1/activities", tags=["Activities"])
    app.include_router(blog.router, prefix="/api/v1/blog", tags=["Blog"])
    app.include_router(social.router, prefix="/api/v1/social", tags=["Social"])

    # Legacy HTML routes
    from app.fastapi_app.routers import plants
    app.include_router(plants.router, prefix="/plants", tags=["Plants Legacy"])
    from app.fastapi_app.routers import breeders
    app.include_router(breeders.router, prefix="/breeders", tags=["Breeders Legacy"])
    from app.fastapi_app.routers import admin
    app.include_router(admin.router, prefix="/admin", tags=["Admin Legacy"])
    from app.fastapi_app.routers import newsletter
    app.include_router(newsletter.router, prefix="/newsletter", tags=["Newsletter Legacy"])
    from app.fastapi_app.routers import activities
    app.include_router(activities.router, prefix="/activities", tags=["Activities Legacy"])


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the Cultivar Collection Management API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
        "auth_docs": "/api/v1/auth/docs",
        "available_endpoints": {
            "plants": "/api/v1/plants",
            "dashboard": "/api/v1/dashboard",
            "cultivars": "/api/v1/cultivars (primary)",
            "strains": "/api/v1/strains (legacy)",
            "breeders": "/api/v1/breeders"
        }
    }

# Health check endpoint
@app.get("/ping", tags=["Health"])
async def ping():
    return {"status": "pong", "system": "Cultivar Collection Management API"}

# Additional endpoints for Comment 8 - Request/Trace IDs
@app.middleware("http")
async def add_request_id(request, call_next):
    """Add request ID middleware for tracking"""
    import uuid
    from fastapi import Request
    
    # Generate unique request ID
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Add to response headers
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    
    return response

@app.get("/api/v1/system/info", tags=["System"])
async def system_info():
    """Get system information including version and build metadata"""
    return {
        "version": "2.0.0",
        "build_date": "2025-01-29",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "api_version": "v1",
        "status": "running"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.fastapi_app:app",
        host="0.0.0.0",
        port=5002,
        reload=True
    )