# CultivAR - Docker development workflow

This document explains how to run the backend in a container while you work on the marketing frontend. The compose setup mounts your working tree into the container and runs Flask with --reload so code changes are picked up automatically.

Quick start (PowerShell)

```powershell
# create a local .env (one-time)
@"
SECRET_KEY=dev-secret-change-me
FLASK_ENV=development
FLASK_DEBUG=1
LEAD_MAGNET_DIR=/app/static/lead_magnets
"@ > .env

# start in detached mode (background)
docker compose up -d --build

# view containers
docker compose ps

# stream logs
docker compose logs -f

# enter the running container shell
docker compose exec cultivare /bin/bash

# stop
docker compose down
```

Notes
- The compose service uses `restart: unless-stopped` so the container will be restarted after host reboots.
- For production builds we use the top-level `Dockerfile` which will run Gunicorn by default. The compose dev service uses the build stage and runs Flask with `--reload`.
- Do not commit secrets to source control. Use `.env` for local secrets and ignore it.
