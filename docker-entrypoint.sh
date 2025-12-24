#!/bin/bash

# Docker entrypoint script for CultivAR application
# This script handles conditional startup for either Flask or FastAPI based on APP_MODE
# Make sure to run: chmod +x docker-entrypoint.sh

set -e

# Handle initialization tasks (database migrations, etc.)
echo "Running initialization tasks..."
# Run database initialization if the script exists
if [ -f scripts/init_db_dual.py ]; then
    echo "Initializing database..."
    export PYTHONPATH=/app
    python scripts/init_db_dual.py
fi
# Add other initialization tasks here as needed (e.g., alembic upgrade head)

# Check APP_MODE environment variable
if [ "$APP_MODE" = "fastapi" ]; then
    echo "Starting FastAPI application on port 8000..."
    exec uvicorn app.fastapi_main.main:app --host 0.0.0.0 --port 8000 --workers 4 "$@"
else
    echo "Starting Flask application on port 5000..."
    exec gunicorn --bind 0.0.0.0:5000 "cultivar_app:create_app()" --workers 3 --worker-class gthread --threads 2 "$@"
fi