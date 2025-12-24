# CultivAR - FastAPI Docker Development Workflow

This document explains how to run the FastAPI backend in a container while you work on the marketing frontend. The compose setup mounts your working tree into the container and runs FastAPI with hot-reload so code changes are picked up automatically.

## Quick Start (PowerShell)

```powershell
# create a local .env (one-time)
@"
APP_MODE=fastapi
FASTAPI_PORT=8000
SECRET_KEY=dev-secret-change-me
SESSION_SECRET_KEY=dev-session-secret
CSRF_SECRET_KEY=dev-csrf-secret
FLASH_SECRET_KEY=dev-flash-secret
CULTIVAR_DB_DRIVER=postgres
CULTIVAR_DB_HOST=db
CULTIVAR_DB_PORT=5432
CULTIVAR_DB_USER=cultivar
CULTIVAR_DB_PASSWORD=cultivar
CULTIVAR_DB_NAME=cultivardb
FRONTEND_ORIGINS=http://localhost:3000,http://localhost:8000
"@ > .env

# start in detached mode (background)
docker compose -f docker-compose.fastapi.yml up -d --build

# view containers
docker compose -f docker-compose.fastapi.yml ps

# stream logs
docker compose -f docker-compose.fastapi.yml logs -f

# enter the running container shell
docker compose -f docker-compose.fastapi.yml exec cultivar_fastapi /bin/bash

# stop
docker compose -f docker-compose.fastapi.yml down
```

Access the FastAPI application at `http://localhost:8000` and API documentation at `http://localhost:8000/docs`.

## Running Flask (Legacy)

For migration testing or if you need to run the legacy Flask version alongside FastAPI, use the dual-stack compose file:

```powershell
# Start both Flask and FastAPI simultaneously
docker compose -f docker-compose.dual.yml up -d --build

# Flask will be available at http://localhost:5000
# FastAPI will be available at http://localhost:8000
```

This allows side-by-side comparison during the migration from Flask to FastAPI.

## Notes

- The compose service uses `restart: unless-stopped` so the container will be restarted after host reboots.
- The Dockerfile uses `docker-entrypoint.sh` which conditionally starts FastAPI or Flask based on the `APP_MODE` environment variable (defaults to FastAPI).
- FastAPI runs with Uvicorn (ASGI) instead of Gunicorn (WSGI) for better async performance.
- Do not commit secrets to source control. Use `.env` for local secrets and ignore it.