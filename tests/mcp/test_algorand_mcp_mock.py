import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from app.repositories.interfaces import PlantDTO, ActivityDTO

# Import the tool functions directly
# We need to patch the repository module globally or within the module before importing, 
# or patch the 'repo' object in ‘app.mcp.algorand_server’.
from app.mcp import algorand_server

@pytest.fixture
def mock_repo():
    mock = AsyncMock()
    mock.create.return_value = PlantDTO(
        id="TX_12345",
        user_id="user_1",
        name="MCP Plant",
        status_id=1,
        cultivar_id=10
    )
    mock.record_activity.return_value = ActivityDTO(
        id="TX_999",
        plant_id="TX_12345",
        activity_type="watering",
        details={"amt": 10},
        timestamp="2024-01-01T12:00:00"
    )
    return mock

@pytest.mark.asyncio
async def test_mcp_create_plant(mock_repo):
    # Test internal implementation directly
    result = await algorand_server._create_plant_impl(
        repo=mock_repo,
        name="MCP Plant", 
        cultivar_id=10, 
        user_id="user_1"
    )
    
    assert "Success" in result
    assert "TX_12345" in result
    
    # Verify call
    mock_repo.create.assert_awaited_once()
    args = mock_repo.create.call_args[0][0]
    assert args.name == "MCP Plant"

@pytest.mark.asyncio
async def test_mcp_log_activity(mock_repo):
    result = await algorand_server._log_activity_impl(
        repo=mock_repo,
        plant_id="TX_12345",
        activity_type="watering",
        details_json={"amount": "10L"}
    )
    
    assert "Activity Recorded" in result
    assert "TX_999" in result
    
    mock_repo.record_activity.assert_awaited_once()
