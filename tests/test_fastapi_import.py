import os
import importlib


import pytest

@pytest.mark.asyncio
async def test_create_app_root():
    """Smoke test: import the fastapi package and assert root endpoint responds.

    This test sets FASTAPI_SKIP_ROUTERS=1 so the test does not require all
    application dependencies or environment to be present.
    """
    os.environ["FASTAPI_SKIP_ROUTERS"] = "1"
    importlib.invalidate_caches()
    from app.fastapi_app import create_app

    app = create_app()
    
    from httpx import ASGITransport, AsyncClient
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as client:
        r = await client.get("/")
        assert r.status_code == 200
        data = r.json()
        assert "message" in data
        assert data["health"] == "/health"
