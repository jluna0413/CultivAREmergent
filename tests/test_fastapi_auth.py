import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models_async.base import Base
from app.models_async.auth import User

@pytest.fixture(autouse=True)
async def clear_db(fastapi_async_db: AsyncSession):
    """Clear all data from tables before each test."""
    from app.models_async.base import Base
    
    # Iterate over all tables and delete data
    for table in reversed(Base.metadata.sorted_tables):
        await fastapi_async_db.execute(table.delete())
    await fastapi_async_db.commit()
    yield
    # Optional: clear after test too
    for table in reversed(Base.metadata.sorted_tables):
        await fastapi_async_db.execute(table.delete())
    await fastapi_async_db.commit()

# Alias fastapi_async_db to test_db_session for compatibility with existing tests
@pytest.fixture(name="test_db_session")
def test_db_session_alias(fastapi_async_db):
    return fastapi_async_db

@pytest.fixture(name="client")
async def client_fixture(test_db_session: AsyncSession):
    from app.fastapi_app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, test_db_session: AsyncSession):
    response = await client.post(
        "/api/v2/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    # Check username instead of message, as message key might not exist in UserResponse
    assert response.json()["username"] == "testuser"

    user = await test_db_session.execute(select(User).where(User.username == "testuser"))
    assert user.scalar_one_or_none() is not None

@pytest.mark.asyncio
async def test_login_for_access_token(client: AsyncClient, test_db_session: AsyncSession):
    # First, register a user
    await client.post(
        "/api/v2/auth/register",
        json={"username": "loginuser", "email": "login@example.com", "password": "password123"}
    )

    response = await client.post(
        "/api/v2/auth/login",
        json={"username": "loginuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_get_current_user_jwt(client: AsyncClient, test_db_session: AsyncSession):
    # Register and login a user to get a token
    await client.post(
        "/api/v2/auth/register",
        json={"username": "jwtuser", "email": "jwt@example.com", "password": "password123"}
    )
    token_response = await client.post(
        "/api/v2/auth/login",
        json={"username": "jwtuser", "password": "password123"}
    )
    access_token = token_response.json()["access_token"]

    # Use /api/v2/auth/me which is the correct endpoint for current user info
    response = await client.get(
        "/api/v2/auth/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "jwtuser"

@pytest.mark.asyncio
async def test_admin_access_required(client: AsyncClient, test_db_session: AsyncSession):
    # Register a regular user
    await client.post(
        "/api/v2/auth/register",
        json={"username": "regularuser", "email": "regular@example.com", "password": "password123"}
    )
    token_response = await client.post(
        "/api/v2/auth/login",
        json={"username": "regularuser", "password": "password123"}
    )
    access_token = token_response.json()["access_token"]

    # Attempt to access an admin-only endpoint
    # /api/v2/users/list requires admin
    response = await client.get(
        "/api/v2/users/list",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_admin_access_granted(client: AsyncClient, test_db_session: AsyncSession):
    # Register a user (will be non-admin by default)
    await client.post(
        "/api/v2/auth/register",
        json={"username": "adminuser", "email": "admin@example.com", "password": "password123"}
    )
    
    # Manually promote to admin in DB
    result = await test_db_session.execute(select(User).where(User.username == "adminuser"))
    user = result.scalar_one()
    user.is_admin = True
    await test_db_session.commit()
    
    token_response = await client.post(
        "/api/v2/auth/login",
        json={"username": "adminuser", "password": "password123"}
    )
    access_token = token_response.json()["access_token"]

    # Attempt to access an admin-only endpoint
    # /api/v2/users/list requires admin
    response = await client.get(
        "/api/v2/users/list",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    # Verify it returns a list
    assert "items" in response.json()
