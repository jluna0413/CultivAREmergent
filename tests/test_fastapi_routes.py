print("Running tests...")
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import patch, MagicMock
import datetime

from app.models_async.base import Base
from app.fastapi_app.routers.health import HealthCheck

# Setup in-memory SQLite for testing is handled by conftest.py

@pytest_asyncio.fixture(name="test_db_session")
def test_db_session_fixture(fastapi_async_db):
    return fastapi_async_db

@pytest_asyncio.fixture(name="client")
async def client_fixture(fastapi_app):
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_health_check_route(client: AsyncClient):
    # Patch all health checks to ensure they return healthy
    with patch("app.fastapi_app.routers.health.HealthChecker.check_database") as mock_db, \
         patch("app.fastapi_app.routers.health.HealthChecker.check_disk_space") as mock_disk, \
         patch("app.fastapi_app.routers.health.HealthChecker.check_memory") as mock_mem, \
         patch("app.fastapi_app.routers.health.HealthChecker.check_cpu") as mock_cpu, \
         patch("app.fastapi_app.routers.health.HealthChecker.check_environment_variables") as mock_env, \
         patch("app.fastapi_app.routers.health.HealthChecker.check_application_health") as mock_app:
        
        # Configure mocks to return healthy status
        healthy_response = HealthCheck(
            name="test", status="healthy", message="OK", last_check=datetime.datetime.now().isoformat()
        )
        mock_db.return_value = healthy_response
        mock_disk.return_value = healthy_response
        mock_mem.return_value = healthy_response
        mock_cpu.return_value = healthy_response
        mock_env.return_value = healthy_response
        mock_app.return_value = healthy_response

        # Use follow_redirects=True to handle potential slash redirects
        response = await client.get("/health", follow_redirects=True)
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_root_page(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "CultivAR FastAPI Application"

@pytest.mark.asyncio
async def test_404_page(client: AsyncClient):
    response = await client.get("/nonexistent-page")
    assert response.status_code == 404
    # Check for the actual error structure returned by exception handler
    data = response.json()
    assert data["error"] == "HTTP Error"
    assert data["status_code"] == 404

@pytest.mark.asyncio
async def test_api_404_page(client: AsyncClient):
    response = await client.get("/api/v1/nonexistent-api-endpoint")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "HTTP Error"
    assert data["status_code"] == 404

@pytest.mark.asyncio
@patch("app.fastapi_app.routers.health.HealthChecker.check_database", side_effect=Exception("Test 500 error"))
async def test_api_500_page(mock_check_db, client: AsyncClient):
    # We patch a dependency of an API endpoint to trigger an unhandled exception
    # This should trigger the 503 response in health check endpoint when check fails
    # Wait, health check catches exceptions and returns 503 with JSON, NOT 500 Server Error.
    # The health endpoint handles exceptions internally.
    
    response = await client.get("/health", follow_redirects=True)
    assert response.status_code == 503
    assert response.json()["status"] == "unhealthy"
    # Verify that the error message contains our test exception
    # The response structure puts errors in "checks" -> "database" -> "message"
    # OR in "checks" -> "errors" if it was a raw exception not caught by specific check handler?
    # HealthChecker.check_database catches Exception and returns HealthCheck with status="unhealthy".
    # But here we patch the method itself to raise Exception, so it bubbles up to asyncio.gather
    # which returns the exception object in the list.
    # The endpoint then puts it in "errors".

    data = response.json()
    assert "errors" in data["checks"]
    assert any("Test 500 error" in str(err) for err in data["checks"]["errors"])

# Note: Removed tests for /waitlist and /blog as they are not in FastAPI main.py
