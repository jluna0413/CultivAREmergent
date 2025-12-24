# FastAPI Migration Guide

This document outlines the migration from a Flask-based application to a FastAPI-based application.

## Overview

Code migration: 95% complete; Operational: Dual-stack fully supported via `run_*.py` scripts and new Compose files; Flask production-ready on port 5000, FastAPI testable on port 8000 with /docs; Shared database ensures consistency. For production deployment, see `DEPLOYMENT.md`.

The CultivAR application has been migrated from Flask to FastAPI to leverage FastAPI's modern asynchronous capabilities, Pydantic for data validation, and automatic OpenAPI documentation generation. This migration involved:

-   Replacing Flask blueprints with FastAPI `APIRouter`s.
-   Updating HTML rendering to use Jinja2Templates with FastAPI.
-   Implementing async database sessions with SQLAlchemy 2.0.
-   Refactoring authentication to support both JWT (for API) and session-based (for HTML forms) mechanisms.
-   Implementing custom middleware for flash messages and CSRF protection.
-   Consolidating and harmonizing SQLAlchemy and Pydantic models for data consistency.
-   Updating Docker configurations and entrypoints to run the FastAPI application with Uvicorn.

## Key Changes

### Project Structure

-   `app/fastapi_app/`: Contains all FastAPI-specific code, including routers, dependencies, middleware, and Pydantic models.
-   `app/fastapi_main/main.py`: The main FastAPI application entry point.
-   `app/models_async/`: Contains asynchronous SQLAlchemy models.
-   `app/handlers_async/`: Contains asynchronous business logic handlers.
-   `scripts/init_db_async.py`: Script for initializing the database and seeding initial data for the async models.
-   `scripts/migrate_async.py`: Script for running async database migrations (currently creates all tables).

### Dependencies

-   `fastapi`: The web framework.
-   `uvicorn[standard]`: ASGI server for running FastAPI.
-   `asyncpg` (for PostgreSQL) / `aiosqlite` (for SQLite): Asynchronous database drivers.
-   `python-jose[cryptography]`: For JWT handling.
-   `passlib[bcrypt]`: For password hashing.
-   `python-multipart`: For handling form data.
-   FastAPI-specific secrets (e.g., `JWT_SECRET_KEY`, `SESSION_SECRET_KEY`, `CSRF_SECRET_KEY`, `FLASH_SECRET_KEY`, `FRONTEND_ORIGINS`) are required only when `APP_MODE=fastapi` or in dual-stack mode.
-   requirements.txt retains Flask dependencies (Flask, Flask-SQLAlchemy, etc.) alongside FastAPI packages (fastapi, uvicorn, asyncpg, etc.) for dual-stack parallel operation during migration; no removals needed.

### Running the Application

The application is now designed to be run with Uvicorn.

#### Local Development

To run the FastAPI application locally:

```bash
python run_fastapi.py # Imports and runs `app.fastapi_main.main:app` via uvicorn on port 8000
```

For Flask:

```bash
python run_flask.py # Creates app via `cultivar_app:create_app()` and runs on port 5000
```

#### Docker

The `Dockerfile` and `docker-compose.fastapi.yml` files have been updated to build and run the FastAPI application as the primary setup.

**FastAPI-only**: Use `docker compose -f docker-compose.fastapi.yml up --build` (sets `APP_MODE=fastapi`, port 8000, runs uvicorn via `docker-entrypoint.sh` with PostgreSQL by default).

To switch to SQLite, set `CULTIVAR_DB_DRIVER=sqlite` in environment variables, comment out the `db` service in the compose file, and add a volume mount like `./data:/app/data`.

**Dual-stack**: Use `docker compose -f docker-compose.dual.yml up --build` to run both Flask and FastAPI side-by-side for migration validation (shared DB, ports 5000/8000; Flask defaults to `APP_MODE=flask`, FastAPI sets `APP_MODE=fastapi`).

The updated `Dockerfile` uses `docker-entrypoint.sh` for conditional startup based on `APP_MODE` (defaults to Flask if not set, but compose files specify FastAPI).

#### Docker Migration Status

- Flask-only compose files (`docker-compose.yml`, `docker-compose.postgres.yml`, `docker-compose.sqlite.yml`) have been removed.
- FastAPI is now the default Docker setup via `docker-compose.fastapi.yml` (with PostgreSQL support).
- The Dockerfile supports both frameworks via the `APP_MODE` environment variable.
- Dual-stack testing is available via `docker-compose.dual.yml` for side-by-side comparison during migration.

### Database Migrations

Initial database setup and migrations are handled by `scripts/migrate_async.py` which calls `scripts/init_db_async.py` for seeding. For more complex schema evolution, Alembic should be configured for async SQLAlchemy.

### Authentication

-   **API Endpoints:** Use JWT tokens for authentication.
-   **HTML Forms:** Use session-based authentication.
-   The `get_current_user` dependency in `app/fastapi_app/dependencies.py` handles both mechanisms.

### CSRF Protection

-   `CSRFMiddleware` in `app/fastapi_app/middleware/csrf.py` provides CSRF protection for HTML forms.
-   API routes can be excluded from CSRF protection using `exclude_paths` in the middleware configuration.

### Flash Messages

-   `FlashMiddleware` in `app/fastapi_app/middleware/flash.py` provides flash message functionality similar to Flask.
-   `get_flashed_messages` now supports `with_categories` parameter.

## Verification

Comprehensive testing is crucial to ensure all functionalities are preserved. New FastAPI-focused tests have been added in `tests/test_fastapi_auth.py`, `tests/test_fastapi_security.py`, and `tests/test_fastapi_routes.py`. The CI/CD pipeline (`.github/workflows/pr-smoke.yml`) has been updated to run these tests.

Additionally, you can run the `scripts/verify_migration.py` script to get a status report on the migration and generate `MIGRATION_STATUS.md`. For dual-stack deployment, traffic splitting via Nginx, and production considerations, see `DEPLOYMENT.md` and `nginx.conf.example`.

## Future Considerations

-   Full Alembic integration for advanced database migrations.
-   More granular rate limiting configuration.
-   Detailed documentation for each API endpoint.
-   Complete feature parity testing for all migrated routes.
