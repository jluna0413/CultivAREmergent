import pytest
from unittest.mock import AsyncMock, patch

from app.services.sync_handlers import sync_create_breeder


def test_sync_create_breeder_injects_user_id_with_session():
    """When user_id is provided and no user_id in breeder_data, it should be injected."""
    mock_async = AsyncMock(return_value={"success": True, "breeder_id": 99})
    with patch("app.services.sync_handlers.async_create_breeder", mock_async):
        # pass a dummy session object to avoid async session creation path
        result = sync_create_breeder({"name": "Test"}, session=object(), user_id=123)

    # Ensure async handler was awaited and received injected user_id
    assert mock_async.await_count == 1
    called_data, called_session = mock_async.call_args[0]
    assert called_data["user_id"] == 123
    assert result["success"] is True


def test_sync_create_breeder_does_not_override_existing_user_id():
    """If breeder_data already contains user_id, the provided user_id param should not override it."""
    mock_async = AsyncMock(return_value={"success": True})
    with patch("app.services.sync_handlers.async_create_breeder", mock_async):
        result = sync_create_breeder({"name": "Test", "user_id": 7}, session=object(), user_id=123)

    assert mock_async.await_count == 1
    called_data = mock_async.call_args[0][0]
    # original user_id should be preserved
    assert called_data["user_id"] == 7
    assert result["success"] is True
