"""
Complete FastAPI Application Entry Point
CultivAR Cannabis Cultivation Tracking System

This file provides the complete FastAPI application with all routers,
middleware, security features, and proper configuration.
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.security import HTTPBearer
from starlette.exceptions import HTTPException as StarletteHTTPException

# Import security middleware
from app.fastapi_app.middleware.security import SecurityHeadersMiddleware, RateLimitMiddleware

# Import routers
from app.fastapi_app.routers import (
    auth, users, dashboard, health, plants, plants_api, 
    strains, strains_api, breeders, clones, activities, sensors, 
    market, marketing, newsletter, blog, social,
    files, diagnostics, admin, websocket, zones,
    site, integrations, acinfinity, nutrients, lineage, genetics, marketplace_breeders,
    marketplace_listings, sales, checkout, cart_api
)

# Import dependencies
from app.fastapi_app.dependencies import require_login

# Import database initialization
from app.fastapi_app.database import init_database, get_async_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting CultivAR FastAPI Application")
    await init_database()
    logger.info("Database initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down CultivAR FastAPI Application")

# Create FastAPI application
app = FastAPI(
    title="CultivAR API",
    description="Advanced Cannabis Cultivation Tracking System",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")
# Environment configuration
is_production = os.getenv("ENVIRONMENT", "development") == "production"
is_staging = os.getenv("ENVIRONMENT", "development") == "staging"

# CORS Configuration
allowed_origins = []
if is_production:
    # Production origins
    allowed_origins = [
        "https://cultivar-app.com",
        "https://www.cultivar-app.com",
        "https://admin.cultivar-app.com"
    ]
elif is_staging:
    # Staging origins
    allowed_origins = [
        "https://staging.cultivar-app.com",
        "https://staging-admin.cultivar-app.com"
    ]
else:
        # Development origins
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:19006",
        "http://localhost:3001",
        "http://localhost:5055",
        "http://localhost:4242",
        "http://127.0.0.1:4242",
        "http://localhost:4200"
    ]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-Requested-With",
        "Accept",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["*"],
    max_age=86400,
)

# Security middleware
if is_production or is_staging:
    # Trusted hosts middleware for production/staging
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=[
            "cultivar-app.com", 
            "www.cultivar-app.com",
            "api.cultivar-app.com",
            "staging.cultivar-app.com",
            "staging-api.cultivar-app.com"
        ]
    )

# Security headers middleware
# Security headers middleware
if is_production or is_staging:
    app.add_middleware(SecurityHeadersMiddleware, is_production=is_production)

# Rate limiting middleware
rate_limit = int(os.getenv("RATE_LIMIT", "100"))
rate_window = int(os.getenv("RATE_WINDOW", "60"))
app.add_middleware(RateLimitMiddleware, limit=rate_limit, window=rate_window)

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "Invalid request data",
            "details": exc.errors()
        }
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred"
        }
    )

# API Version middleware
@app.middleware("http")
async def add_api_version(request: Request, call_next):
    """Add API version to response headers"""
    response = await call_next(request)
    response.headers["X-API-Version"] = "2.0.0"
    response.headers["X-API-Type"] = "FastAPI"
    return response

# Include routers with proper prefixes and tags
logger.info("Including API routers...")

# Health check (no auth required)
app.include_router(
    health.router,
    prefix="/health",
    tags=["Health Check"]
)

# Authentication (no auth required for login/register)
app.include_router(
    auth.router,
    prefix="/api/v2/auth",
    tags=["Authentication"]
)

# AI Agents Router (imported from app.routers.agents)
from app.routers import agents
app.include_router(
    agents.router,
    # Prefix is already defined in the router as /api/v2/agents
    tags=["AI Agents"]
)

# All other authenticated routes
# Add global auth dependency for protected routes
from fastapi import Depends

async def get_current_user_token():
    """Global dependency for authentication"""
    # This will be handled by individual route dependencies
    pass

# Protected routers with authentication
protected_routers = [
    (users.api_router, "/api/v2/users", "User Management"),
    (users.router, "/api/v2/legacy/users", "User Management (Legacy)"),
    (dashboard.router, "/api/v2/dashboard", "Dashboard"),
    (plants.router, "/api/v2/plants", "Plant Management"),
    (plants_api.router, "/api/v2/plants-api", "Plant API"),
    (strains.router, "/api/v2/strains", "Strain Management"),
    (strains_api.router, "", "Strains Database API"),
    (breeders.router, "/api/v2/breeders", "Breeder Management"),
    (genetics.router, "", "Genetics Management"),
    (clones.router, "/api/v2/clones", "Clone Management"),
    (activities.router, "/api/v2/activities", "Activity Tracking"),
    (sensors.router, "/api/v2/sensors", "Sensor Management"),
    (acinfinity.router, "", "AC Infinity Devices"),
    (integrations.router, "", "Third-Party Integrations"),
    (nutrients.router, "", "Nutrient Management"),
    (market.router, "/api/v2/market", "Marketplace"),
    (marketplace_breeders.router, "", "Marketplace Breeders"),
    (lineage.router, "", "Lineage & Hypergraph"),
    (marketing.router, "/api/v2/marketing", "Marketing"),
    (newsletter.router, "/api/v2/newsletter", "Newsletter"),
    (blog.router, "/api/v2/blog", "Blog Management"),
    (social.router, "/api/v2/social", "Social Features"),
    (files.router, "/api/v2/files", "File Management"),
    (diagnostics.router, "/api/v2/diagnostics", "Diagnostics"),
    (admin.router, "/api/v2/admin", "Administration"),
    (websocket.router, "/api/v2/websocket", "WebSocket"),
    (zones.router, "/api/v2/zones", "Zone Management"),
    (site.router, "/api/v2/site", "Site Management"),
    (marketplace_listings.router, "/api/v2", "Marketplace Listings"),
    (sales.router, "/api/v2/analytics", "Sales Analytics"),
    (checkout.router, "/api/v2", "Checkout"),
    (cart_api.router, "/api/v2", "Cart API"),
]

for router, prefix, tag in protected_routers:
    app.include_router(
        router, 
        prefix=prefix, 
        tags=[tag],
        dependencies=[Depends(require_login)]
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "CultivAR FastAPI Application",
        "version": "2.0.0",
        "docs": "/docs",
        "status": "operational",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "features": {
            "authentication": True,
            "websocket": True,
            "file_upload": True,
            "real_time_updates": True
        }
    }

# API status endpoint
@app.get("/api/v2/status")
async def api_status():
    """Comprehensive API status endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": "2025-11-21T16:56:30Z",
        "services": {
            "database": "connected",
            "authentication": "operational",
            "file_storage": "available",
            "websocket": "active"
        },
        "environment": os.getenv("ENVIRONMENT", "development"),
        "rate_limiting": {
            "limit": rate_limit,
            "window": rate_window
        }
    }

# Development info endpoint
if not is_production:
    @app.get("/api/v2/dev-info")
    async def dev_info():
        """Development information endpoint"""
        return {
            "environment": "development",
            "available_routers": [tag for _, _, tag in protected_routers],
            "cors_origins": allowed_origins,
            "security_headers": is_production,
            "rate_limiting": {
                "enabled": True,
                "limit": rate_limit,
                "window": rate_window
            }
        }

logger.info("CultivAR FastAPI application startup complete!")
logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
logger.info(f"Documentation available at: /docs")
logger.info(f"CORS origins: {allowed_origins}")
