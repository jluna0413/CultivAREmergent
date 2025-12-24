# CultivAR Deployment Guide

## Overview

This document outlines the deployment strategy for CultivAR, with FastAPI as the primary framework and Flask available for legacy support. The dual-stack option enables side-by-side operation during migration.

## Prerequisites

Before deployment, ensure the following are in place:

*   **Docker & Docker Compose:** For containerized deployments.
*   **Python 3.8+:** If deploying directly without Docker.
*   **PostgreSQL Database:** Recommended for production. Ensure connection details are available.
*   **Available Ports:** Flask typically uses `5000`, FastAPI `8000`. Ensure these ports are open and not in use.
*   **SSL Certificates:** For production environments, configure SSL (e.g., via Nginx or a load balancer).

## Deployment Options

CultivAR supports several deployment modes, controlled primarily by environment variables and Docker Compose configurations.

### Option A: FastAPI (Primary/Recommended)

This mode runs only the FastAPI application.

*   **Environment Variable:** `APP_MODE=fastapi`
*   **Docker Compose:** Use `docker-compose.fastapi.yml` with the `docker compose` command (for example: `docker compose -f docker-compose.fastapi.yml up -d`).
*   **Direct Python:** `python run_fastapi.py` or `uvicorn app.fastapi_main.main:app --host 0.0.0.0 --port 8000`
*   **Port:** 8000
*   **Docs:** Available at `/docs` and `/redoc`

### Option B: Flask (Legacy/Fallback)

This mode runs only the Flask application.

*   **Environment Variable:** `APP_MODE=flask` or omit (but not recommended)
*   **Docker Compose:** Use `docker-compose.dual.yml` with the `docker compose` command (for example: `docker compose -f docker-compose.dual.yml up -d cultivar_flask`) to run only the `cultivar_flask` service.
*   **Direct Python:** `python run_flask.py` or `FLASK_APP=cultivar_app.py flask run`
*   **Port:** 5000

### Option C: Dual-Stack (Migration/Testing)

This mode runs both Flask and FastAPI applications simultaneously.

*   **Docker Compose:** Use `docker-compose.dual.yml` with the `docker compose` command (for example: `docker compose -f docker-compose.dual.yml up -d`) to run both applications simultaneously
*   **Ports:** Flask on port 5000, FastAPI on port 8000
*   **Database:** Shared database for consistency
*   **Use Case:** Useful for A/B testing and gradual migration

## Production Configuration

### Environment Variables

All sensitive information and configuration parameters should be managed via environment variables. Refer to `.env.example` for a comprehensive list.

*   **`SECRET_KEY`**: Critical for security. Generate a strong, unique key.
*   **`DEBUG`**: Set to `false` in production.
*   **Database Configuration (`CULTIVAR_DB_DRIVER`, `CULTIVAR_DB_HOST`, etc.)**: Configure for your production PostgreSQL instance.
*   **FastAPI Specific (`SESSION_SECRET_KEY`, `CSRF_SECRET_KEY`, `FLASH_SECRET_KEY`, etc.)**: Generate strong, unique keys for these.
*   **`FRONTEND_ORIGINS`**: Configure for your production frontend domains to enable CORS.

### Server Setup

For production deployments, use FastAPI with Uvicorn workers managed by Gunicorn for optimal performance:
*   **Command:** `gunicorn app.fastapi_main.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000`
*   **Workers:** Adjust `-w` based on your server resources (typically 2-4 workers per CPU core).

### Database

*   **PostgreSQL:** Ensure your PostgreSQL server is properly secured, backed up, and accessible from your application containers.
*   **Migrations:** Apply database migrations using Alembic.
    *   `alembic upgrade head` (for Flask/sync models)
    *   `python scripts/init_db_dual.py` (for FastAPI/async models, if separate initialization is needed)

### SSL/TLS

Terminate SSL at your reverse proxy (e.g., Nginx) or load balancer. Do not expose the application directly to the internet without SSL.

## Docker Deployment

For production, use `docker-compose.fastapi.yml` with the `docker compose` command to deploy FastAPI with database support (e.g. `docker compose -f docker-compose.fastapi.yml build --no-cache && docker compose -f docker-compose.fastapi.yml up -d`).

1.  **Build Images:**
    ```bash
    docker compose -f docker-compose.fastapi.yml build --no-cache
    ```
2.  **Run Containers:**
    ```bash
    docker compose -f docker-compose.fastapi.yml up -d
    ```
3.  **Volumes:** Ensure persistent data (e.g., PostgreSQL data) is mapped to Docker volumes. Code volumes (`./:/app:cached`) are useful for development but consider read-only volumes or copying code into the image for production.
4.  **Healthchecks:** The provided `docker-compose` files include basic healthchecks. Monitor these to ensure services are running correctly.

## Load Balancer / Reverse Proxy (Nginx Example)

An Nginx configuration can be used to route traffic to either Flask or FastAPI, enabling strategies like:

*   **Path-based routing:** `/api/v1/` to Flask, `/api/v2/` to FastAPI.
*   **Header-based routing:** Route based on specific headers.
*   **Gradual rollout:** Use `split_clients` to send a percentage of traffic to FastAPI.

Refer to `nginx.conf.example` for a starting point.

## Migrations

*   **Alembic:** Use Alembic for managing Flask (sync) database schema migrations.
*   **FastAPI Async Models:** If your FastAPI models use a separate async engine/session, ensure their tables are created and managed. The `scripts/init_db_dual.py` can be used for initial setup or specific async model migrations.

## Monitoring and Logging

*   **Health Endpoints:** Both Flask (`/`) and FastAPI (`/health`) provide basic health endpoints. Integrate these with your monitoring system.
*   **Container Logs:** Use `docker compose logs -f` to view container logs. Implement a centralized logging solution for production.

## Rollback Strategy

In case of issues with the FastAPI migration:

1.  **Revert Traffic:** Adjust your load balancer/reverse proxy configuration (e.g., Nginx) to route 100% of traffic back to the Flask application.
2.  **Revert Deployment:** If necessary, revert your Docker Compose files or `APP_MODE` environment variables to run only the Flask stack.
3.  **Database Rollback:** If database schema changes were applied specifically for FastAPI and are incompatible with Flask, use Alembic to downgrade the database.

## Troubleshooting

*   **Missing Environment Variables:** Check `.env` file and deployment environment for all required variables.
*   **Port Conflicts:** Ensure no other processes are using ports `5000` or `8000`.
*   **Database Connection Issues:** Verify `CULTIVAR_DB_HOST`, `CULTIVAR_DB_PORT`, `CULTIVAR_DB_USER`, `CULTIVAR_DB_PASSWORD`, `CULTIVAR_DB_NAME`. Check database logs.
*   **Container Startup Failures:** Use `docker compose logs <service_name>` to inspect startup errors.
*   **Application Errors:** Check application logs for stack traces.
*   **CORS Issues:** Ensure `FRONTEND_ORIGINS` is correctly configured for FastAPI.
