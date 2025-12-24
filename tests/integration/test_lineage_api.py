
import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.fastapi_app.main import app
from app.fastapi_app.dependencies import require_login
from app.models_async.auth import User

# Mock Response Data
MOCK_ANCESTRY_TREE = {
    "name": "Blue Dream",
    "ancestors": [
        {"name": "Blueberry", "generation": 1, "relationship": "parent"},
        {"name": "Haze", "generation": 1, "relationship": "parent"}
    ]
}

@pytest.fixture
async def authenticated_user(fastapi_async_db: AsyncSession):
    """
    Ensures a test user exists and overrides the require_login dependency.
    """
    # Check if user exists to avoid UNIQUE constraint error
    stmt = select(User).where(User.username == "integration_test_user")
    result = await fastapi_async_db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(
            username="integration_test_user", 
            email="integration@test.com",
            is_active=True
        )
        user.set_password("TestPassw0rd!")
        fastapi_async_db.add(user)
        await fastapi_async_db.commit()
        await fastapi_async_db.refresh(user)
        
    # Override dependency
    app.dependency_overrides[require_login] = lambda: user
    
    yield user
    
    # Clean up override
    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_create_user_genetics_triggers_sync(fastapi_client: AsyncClient, authenticated_user):
    """
    Test that creating a UserGenetics record triggers the Hypergraph sync.
    """
    with patch("app.fastapi_app.routers.genetics.hypergraph_service") as mock_service:
        mock_service.create_strain_node = AsyncMock(return_value="strain-node-123")
        
        payload = {
            "name": "Test Strain Sync",
            "genetics_type": "SEED",
            "description": "Integration test strain"
        }
        
        # No headers needed due to dependency override
        response = await fastapi_client.post(
            "/api/v2/genetics/",
            json=payload
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Strain Sync"
        
        # Verify sync called
        mock_service.create_strain_node.assert_called_once()
        assert mock_service.create_strain_node.call_args[1]["name"] == "Test Strain Sync"

@pytest.mark.asyncio
async def test_create_breeder_triggers_sync(fastapi_client: AsyncClient, authenticated_user):
    """
    Test that creating a MarketplaceBreeder triggers the Hypergraph sync.
    """
    with patch("app.fastapi_app.routers.marketplace_breeders.hypergraph_service") as mock_service:
        mock_service.create_breeder_node = AsyncMock(return_value="breeder-node-456")
        
        payload = {
            "breeder_name": "Test Sync Breeder",
            "website_url": "https://test.com",
            "bio": "Integration test breeder"
        }
        
        response = await fastapi_client.post(
            "/api/v2/marketplace/breeders/",
            json=payload
        )
        
        assert response.status_code == 201
        
        # Verify sync called
        mock_service.create_breeder_node.assert_called_once()
        assert mock_service.create_breeder_node.call_args[1]["name"] == "Test Sync Breeder"

@pytest.mark.asyncio
async def test_get_ancestry_endpoint_logic(fastapi_client: AsyncClient, authenticated_user):
    """
    Test the endpoint returns 404/503 correctly when mock service behaves in certain ways.
    """
    with patch("app.fastapi_app.routers.lineage.hypergraph_service") as mock_service:
        # 1. Test 404 when mapping not found
        # (Since we didn't create a mapping for ID 999, it should fail lookup in SQL)
        response = await fastapi_client.get("/api/lineage/999/ancestry")
        assert response.status_code == 404
