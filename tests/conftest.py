import asyncio
import pytest

@pytest.fixture(scope="session")
def event_loop():
    """
    Provide a session-scoped event loop for pytest-asyncio.
    Creates a fresh loop and closes it after the test session.
    """
    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture
async def client():
    """
    Minimal async client fixture placeholder.

    Tests that require a real HTTP/ASGI test client should override this fixture
    in a more specific test module or extend it to return an actual AsyncClient,
    e.g., httpx.AsyncClient(app=app, base_url="http://test").
    Returning None lets unit tests that do not need a client run without failure.
    """
    yield None


@pytest.fixture
async def authenticated_client():
    """
    Placeholder authenticated client fixture.

    Integration tests should replace this with an authenticated AsyncClient instance.
    """
    yield None