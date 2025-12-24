import pytest
import httpx
from httpx import ASGITransport

@pytest.fixture(scope="function")
def admin_credentials():
    return {
        "username": "testuser",
        "password": "password"
    }

@pytest.fixture(scope="function")
async def auth_token(fastapi_app, admin_credentials, test_user):
    """Fixture to get an authentication token."""
    # test_user fixture ensures the user exists in the DB
    transport = ASGITransport(app=fastapi_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v2/auth/login", json=admin_credentials)
        response.raise_for_status()
        return response.json()["access_token"]

@pytest.mark.asyncio
async def test_health_live_unauthenticated(fastapi_app):
    """
    Tests the /health/live endpoint to ensure the application is running.
    """
    transport = ASGITransport(app=fastapi_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health/live")
        
        # Check that the response status code is 200 (OK)
        assert response.status_code == 200
        
        # Check that the response body is valid JSON
        response_json = response.json()
        
        # Check for the expected keys and values
        assert "status" in response_json
        assert response_json["status"] == "alive"
        assert "timestamp" in response_json
        assert "uptime_seconds" in response_json

@pytest.mark.asyncio
async def test_health_live_authenticated(fastapi_app, auth_token):
    """
    Tests the /health/live endpoint with authentication.
    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    transport = ASGITransport(app=fastapi_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        response = await client.get("/health/live")
        
        # Check that the response status code is 200 (OK)
        assert response.status_code == 200
        
        # Check that the response body is valid JSON
        response_json = response.json()
        
        # Check for the expected keys and values
        assert "status" in response_json
        assert response_json["status"] == "alive"