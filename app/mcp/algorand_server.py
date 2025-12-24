import os
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional

from fastmcp import FastMCP
from algosdk.v2client import algod as algo_client_lib
from app.repositories.algorand.plant_repository import AlgorandPlantRepository
from app.repositories.interfaces import PlantCreateDTO, PlantDTO, ActivityDTO

# Initialize MCP Server
mcp = FastMCP("Algorand Plant Manager")

# Configuration
ALGO_NODE_URL = os.getenv("ALGORAND_NODE_URL", "http://localhost:4001")
ALGO_NODE_TOKEN = os.getenv("ALGORAND_NODE_TOKEN", "a" * 64)
ALGO_APP_ID = int(os.getenv("ALGORAND_APP_ID", "12345"))  # Default/Mock ID
ALGO_SIGNER_SK = os.getenv("ALGORAND_SIGNER_PRIVATE_KEY", "")

# Initialize Clients
try:
    client = algo_client_lib.AlgodClient(ALGO_NODE_TOKEN, ALGO_NODE_URL)
    # If no key provided, we might be in inspection-only mode or failing
    repo = AlgorandPlantRepository(client, ALGO_APP_ID, ALGO_SIGNER_SK)
except Exception as e:
    print(f"Warning: Failed to initialize Algorand Repository: {e}")
    repo = None

# --- Implementation Logic (Testable) ---

async def _create_plant_impl(repo: AlgorandPlantRepository, name: str, cultivar_id: int, user_id: str) -> str:
    if not repo:
        return "Error: Algorand Repository not initialized."

    dto = PlantCreateDTO(
        user_id=user_id,
        name=name,
        cultivar_id=cultivar_id,
        is_clone=False,
        status_id=1
    )
    
    try:
        result = await repo.create(dto)
        return f"Success. Plant Created. ID/Hash: {result.id}"
    except Exception as e:
        return f"Error creating plant on-chain: {str(e)}"

async def _log_activity_impl(repo: AlgorandPlantRepository, plant_id: str, activity_type: str, details_json: Dict[str, Any]) -> str:
    if not repo:
        return "Error: Algorand Repository not initialized."

    try:
        result = await repo.record_activity(plant_id, activity_type, details_json)
        return f"Activity Recorded. Tx Hash: {result.id}"
    except Exception as e:
        return f"Error logging activity: {str(e)}"

async def _get_plant_impl(repo: AlgorandPlantRepository, plant_id: str) -> str:
    if not repo:
        return "Error: Algorand Repository not initialized."
        
    try:
        plant = await repo.get_by_id(plant_id)
        if not plant:
            return "Plant not found on-chain."
        
        return plant.model_dump_json()
    except Exception as e:
        return f"Error fetching plant: {str(e)}"


# --- MCP Tool Definitions ---

@mcp.tool()
async def create_plant_asset(name: str, cultivar_id: int, user_id: str) -> str:
    """
    Mint a new Plant Asset (or State) on the Algorand Blockchain.
    Returns the Transaction ID (or Plant ID).
    """
    return await _create_plant_impl(repo, name, cultivar_id, user_id)

@mcp.tool()
async def log_growth_activity(plant_id: str, activity_type: str, details: str) -> str:
    """
    Record an immutable activity log for a plant.
    'details' should be a JSON string.
    """
    try:
        d_json = json.loads(details)
    except json.JSONDecodeError:
        return "Error: 'details' must be valid JSON string."
        
    return await _log_activity_impl(repo, plant_id, activity_type, d_json)

@mcp.tool()
async def get_plant_provenance(plant_id: str) -> str:
    """
    Fetch the on-chain state/provenance of a plant.
    """
    return await _get_plant_impl(repo, plant_id)

if __name__ == "__main__":
    mcp.run()
