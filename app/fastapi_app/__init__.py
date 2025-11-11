from __future__ import annotations

"""Cultivar Collection Management System - FastAPI package.

This module exposes a lazy `create_app()` factory to avoid importing heavy
router and dependency modules at package import time. That makes the package
safe for tools, docs generation and unit tests which import the package but
don't need the running application.
"""

from typing import List
import os
import logging

from fastapi import FastAPI

_LOGGER = logging.getLogger("fastapi_app")


def get_cors_origins() -> List[str]:
    origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:3000,http://localhost:8000")
    return [o.strip() for o in origins.split(",") if o.strip()]


def create_app() -> FastAPI:
    """Create and return the FastAPI application with routers registered.

    Imports for routers and other heavy modules are done inside this function
    to avoid side effects during package import.
    """
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.middleware.trustedhost import TrustedHostMiddleware

    app = FastAPI(
        title="Cultivar Collection Management API",
        description="Advanced cannabis cultivar tracking and analytics platform",
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_cors_origins(),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "X-Requested-With",
            "Accept",
            "Origin",
            "Access-Control-Request-Method",
            "Access-Control-Request-Headers",
            "X-CSRFToken",
        ],
        expose_headers=["Content-Length", "Content-Range"],
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "*.localhost", os.getenv("ALLOWED_HOSTS", "")],
    )

    # Optionally skip registering routers (useful for docs generation / tests)
    if os.getenv("FASTAPI_SKIP_ROUTERS", "0") != "1":
        try:
            # Import and include routers lazily
            from app.fastapi_app.routers import (
                health,
                plants_api,
                dashboard,
                cultivars,
                cultivars_legacy,
                breeders,
                auth,
                admin,
                market,
                newsletter,
                site,
                clones,
                diagnostics,
                activities,
                blog,
                social,
            )

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

            # Legacy HTML routes (imported last to avoid circulars)
            from app.fastapi_app.routers import plants as plants_legacy

            app.include_router(plants_legacy.router, prefix="/plants", tags=["Plants Legacy"])
        except Exception:  # pragma: no cover - defensive import-time protection
            _LOGGER.exception("Failed to import and include some routers; continuing without them")

    # Basic root endpoint and ping
    @app.get("/", tags=["Root"])
    async def root():
        return {
            "message": "Welcome to the Cultivar Collection Management API",
            "version": "2.0.0",
            "docs": "/docs",
            "health": "/health",
        }

    @app.get("/ping", tags=["Health"])
    async def ping():
        return {"status": "pong", "system": "Cultivar Collection Management API"}

    return app


# By default do not create the app at import time. Set FASTAPI_CREATE_AT_IMPORT=1 to
# force `app` to be created immediately (not recommended for tests/docs).
app = None
if os.getenv("FASTAPI_CREATE_AT_IMPORT", "0") == "1":
    try:
        app = create_app()
    except Exception:
        _LOGGER.exception("Failed to create app at import time")


if __name__ == "__main__":
    # When run directly, create and run the app (development convenience)
    import uvicorn

    uvicorn.run("app.fastapi_app.main:app", host="0.0.0.0", port=5002, reload=True)
"""
Cultivar Collection Management System - FastAPI Application
Main entry point for the FastAPI backend serving cultivar APIs
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
"""Cultivar Collection Management System - FastAPI package.

This module exposes a lazy `create_app()` factory to avoid importing heavy
router and dependency modules at package import time. That makes the package
safe for tools, docs generation and unit tests which import the package but
don't need the running application.
"""

