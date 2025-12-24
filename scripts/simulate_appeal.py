import asyncio
import os
import sys

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.trust_engine.orchestrator import AuditOrchestrator

async def run_appeal_simulation():
    print("\n--- ⚖️ STARTING NEURO-VERIFIED APPEAL SIMULATION ---\n")
    
    orchestrator = AuditOrchestrator()
    
    # 1. Simulate Failed Audit (To have something to appeal)
    print(">>> PART 1: Simulate Initially Rejected Audit (Pre-Packaged Seeds)")
    result_rejected = await orchestrator.process_audit_request(
        merchant_addr="LEGIT_MERCHANT_PREPACK",
        listing_hash="hash_prepack_123",
        strain_name="Rare Heirloom (No Macro)"
    )
    print(f"Initial Status: {result_rejected['status']}") # Should be FAILED
    
    print("\n------------------------------------------------\n")
    
    # 2. Simulate Appeal Submission
    print(">>> PART 2: Admin Override / Appeal Submission")
    
    appeal_reason = "Verified via Breeder Legacy Documentation and Video Call. Pre-packaged seal intact."
    
    result_appeal = await orchestrator.process_appeal(
        listing_id="listing_prepack_123",
        reason=appeal_reason
    )
    
    print(f"Appeal Status: {result_appeal['status']}")
    print(f"Override Reason: {result_appeal['override_reason']}")
    
    if result_appeal['status'] != "APPROVED_BY_APPEAL":
        print("❌ Appeal Failed: Status not updated correctly.")
        sys.exit(1)
        
    print("\n>>> SIMULATION COMPLETE: APPEAL WORKFLOW VERIFIED ✅")

if __name__ == "__main__":
    asyncio.run(run_appeal_simulation())
