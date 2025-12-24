
import pytest
import gql
from app.services.hypergraph_service import HypergraphService
from app.fastapi_app.routers import lineage
from app.fastapi_app.routers import genetics
from app.fastapi_app.routers import marketplace_breeders

@pytest.mark.asyncio
async def test_sanity():
    assert True
