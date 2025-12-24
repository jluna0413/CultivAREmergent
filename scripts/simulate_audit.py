import asyncio
import os
import sys

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.trust_engine.orchestrator import AuditOrchestrator

async def run_simulation():
    print("\n--- 🧠 STARTING EVO-AGENT-X NEURO-AUDIT SIMULATION ---\n")
    
    orchestrator = AuditOrchestrator()
    
    # 1. Test Valid Listing
    print(">>> TEST CASE 1: Valid Verification Kush (Should APPROVE)")
    result_valid = await orchestrator.process_audit_request(
        merchant_addr="TEST_MERCHANT_ADDR",
        listing_hash="hash_valid_123",
        strain_name="Verification Kush"
    )
    print(f"Result: {result_valid['status']}")
    
    if result_valid['status'] != "APPROVED":
        print("❌ Test Case 1 FAILED")
        sys.exit(1)
        
    print("\n------------------------------------------------\n")
        
    # 2. Test Invalid Listing (Unknown Strain)
    print(">>> TEST CASE 2: Unknown Strain 'Fake OG' (Should FAIL RAG)")
    result_invalid = await orchestrator.process_audit_request(
        merchant_addr="FRAUD_ATTEMPT_ADDR",
        listing_hash="hash_fraud_456",
        strain_name="Fake OG"
    )
    print(f"Result: {result_invalid['status']}")
    
    if result_invalid['status'] != "FAILED":
        print("❌ Test Case 2 FAILED (Should have failed RAG)")
        sys.exit(1)
        
    print("\n>>> SIMULATION COMPLETE: ALL TESTS PASSED ✅")

if __name__ == "__main__":
    asyncio.run(run_simulation())
