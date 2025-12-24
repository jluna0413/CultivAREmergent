import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from algosdk import account, transaction
from app.repositories.algorand.plant_repository import AlgorandPlantRepository
from app.repositories.hybrid.plant_repository import HybridPlantRepository
from app.repositories.interfaces import PlantCreateDTO, PlantDTO, ActivityDTO

# Constants
APP_ID = 12345

@pytest.fixture
def mock_algod():
    client = MagicMock()
    # Mock suggested params
    params = MagicMock()
    params.first = 1000
    params.last = 2000
    params.gh = "gh"
    params.gen = "gen"
    params.fee = 1000
    params.flat_fee = True
    client.suggested_params.return_value = params
    
    # Mock send transaction
    client.send_transaction.return_value = "TX_ID_123"
    
    return client

@pytest.mark.asyncio
async def test_algo_create_plant(mock_algod):
    # Mock account derivation to bypass binascii error in test env
    with patch('algosdk.account.address_from_private_key', return_value="MOCK_ADDR"):
        repo = AlgorandPlantRepository(mock_algod, APP_ID, "dummy_key")
        
        # Mock transaction signing to avoid key check
        with patch('algosdk.transaction.ApplicationCallTxn.sign', return_value="signed_txn_obj"):
            dto = PlantCreateDTO(
                user_id=1,
                name="Algo Plant",
                status_id=1,
                cultivar_id=10,
                is_clone=False
            )
            
            result = await repo.create(dto)
            
            assert result.id == "TX_ID_123"
            assert result.name == "Algo Plant"
            
            # Verify we tried to send
            mock_algod.send_transaction.assert_called_once()

@pytest.mark.asyncio
async def test_hybrid_dual_write(mock_algod):
    # Mock SQL Repo
    sql_repo = AsyncMock()
    sql_repo.create.return_value = PlantDTO(
        id=777,
        user_id="1", 
        name="SQL Plant", 
        status_id=1,
        created_at=None,
        updated_at=None
    )
    
    # Mock algo repo dependencies
    with patch('algosdk.account.address_from_private_key', return_value="MOCK_ADDR"):
        with patch('algosdk.transaction.ApplicationCallTxn.sign', return_value="signed_txn_obj"):
            algo_repo = AlgorandPlantRepository(mock_algod, APP_ID, "dummy_key")
            
            # Hybrid Repo
            hybrid_repo = HybridPlantRepository(sql_repo, algo_repo, migration_mode="dual_write")
            
            dto = PlantCreateDTO(user_id=1, name="Hybrid Plant", status_id=1)
            
            # Execute
            result = await hybrid_repo.create(dto)
            
            # Assert
            assert result.id == 777
            
            # Wait for async task
            await asyncio.sleep(1.0)
            
            # Verify Algorand execution 
            mock_algod.send_transaction.assert_called_once()
