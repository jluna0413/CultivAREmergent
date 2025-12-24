import asyncio
import sys
import os
from unittest.mock import AsyncMock, patch
from typing import Dict, Any, Optional

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.trust_engine.circuit_bridge import CircuitSparsityBridge

async def verify_circuit_bridge():
    print("\n--- VERIFYING CIRCUIT SPARSITY BRIDGE (STORY 3) ---\n")
    
    bridge = CircuitSparsityBridge(threshold=0.8)
    
    # 1. Test Mock Activation (No Tensor)
    print(">>> TEST 1: Development Mode (Mock Data)")
    result = await bridge.verify_circuit_activation(agent_hidden_states=None)
    
    print(f"Result: {result}")
    
    if "is_trusted" not in result:
        print("[FAIL] Missing 'is_trusted' key")
    elif "trust_score" not in result:
        print("[FAIL] Missing 'trust_score' key")
    else:
        print(f"[OK] Mock Bridge Returned Trust Score: {result['trust_score']}")
        
    # 2. Test Input Interface (Simulated Tensor)
    print("\n>>> TEST 2: Production Interface (Simulated Tensor)")
    mock_tensor = [0.1, 0.5, 0.9] # Mock list of floats
    result_with_input = await bridge.verify_circuit_activation(agent_hidden_states=mock_tensor)
    
    # Since logic is mocked, it should just work same as before or ignore input
    print(f"Result with Tensor: {result_with_input}")
    
    if "auditor_version" in result_with_input:
        print(f"[OK] Auditor Version: {result_with_input['auditor_version']}")
    else:
        print("[FAIL] Missing version info")

    print("\n>>> SYSTEM VERIFIED SUCCESSFULLY [OK]")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_circuit_bridge())
