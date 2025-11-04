# FastAPI-only Dockerfile for CultivAR v2.0.0
FROM python:3.11-slim AS build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# system deps for FastAPI and async database drivers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /app/requirements.txt

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# copy installed packages from build stage
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# copy app
COPY . /app

# non-root user
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5002

# Run FastAPI with Uvicorn
# In production: Use gunicorn with uvicorn workers
# In development: Use uvicorn with reload
CMD ["uvicorn", "app.fastapi_app:app", "--host", "0.0.0.0", "--port", "5002"]
