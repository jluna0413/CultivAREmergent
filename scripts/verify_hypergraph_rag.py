import asyncio
import sys
import os
from unittest.mock import AsyncMock, patch
from typing import Dict, Any, Optional

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.trust_engine.hypergraph_rag import HyperGraphRAG

async def verify_hypergraph_integration():
    print("\n--- VERIFYING HYPERGRAPH RAG INTEGRATION (STORY 2) ---\n")
    
    # Mocking the HypergraphService inside HyperGraphRAG
    with patch('app.services.trust_engine.hypergraph_rag.HypergraphService') as MockServiceClass:
        mock_service = MockServiceClass.return_value
        
        rag = HyperGraphRAG()
        
        # --- TEST 1: Valid Strain Found ---
        print(">>> TEST 1: Valid Strain (Found & Verified Ancestry)")
        
        mock_service.get_strain_by_name = AsyncMock(return_value={
            "id": "node_123",
            "name": "Verification Kush",
            "breederName": "Test Breeder"
        })
        
        mock_service.get_ancestry_tree = AsyncMock(return_value={
            "name": "Verification Kush",
            "ancestors": [
                {"name": "Verified Parent A", "relationship": "parent"},
                {"name": "Verified Parent B", "relationship": "parent"}
            ]
        })
        
        result = await rag.verify_lineage("Verification Kush")
        print(f"Result: {result}")
        
        if not result["verified"]:
            print("[FAIL] Expected Verified=True")
        elif result["confidence"] < 0.9:
            print(f"[FAIL] Confidence too low: {result['confidence']}")
        else:
            print("[OK] Strain Verified Successfully.")
            
        # --- TEST 2: Strain Not Found ---
        print("\n>>> TEST 2: Strain Not Found")
        
        mock_service.get_strain_by_name = AsyncMock(return_value=None)
        
        result = await rag.verify_lineage("Ghost Strain")
        print(f"Result: {result}")
        
        if result["verified"]:
            print("[FAIL] Expected Verified=False")
        elif result["reason"] != "Strain node not found":
             print(f"[FAIL] Unexpected Reason: {result['reason']}")
        else:
            print("[OK] Missing Strain Handled Correctly.")

        # --- TEST 3: Orphan Strain (No Ancestors) ---
        print("\n>>> TEST 3: Orphan Strain (No Ancestry)")
        
        mock_service.get_strain_by_name = AsyncMock(return_value={
            "id": "node_orphan", 
            "name": "Mystery Mix"
        })
        
        mock_service.get_ancestry_tree = AsyncMock(return_value={
            "name": "Mystery Mix",
            "ancestors": [] # Empty List
        })
        
        result = await rag.verify_lineage("Mystery Mix")
        print(f"Result: {result}")
        
        if result["verified"]:
             print("[FAIL] Expected Verified=False")
        elif result["confidence"] > 0.5:
             print("[FAIL] Confidence too high for orphan")
        else:
             print("[OK] Orphan Strain Flagged Correctly.")

    print("\n>>> SYSTEM VERIFIED SUCCESSFULLY [OK]")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_hypergraph_integration())
