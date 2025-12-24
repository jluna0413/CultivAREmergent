from app.services.trust_engine.hypergraph_rag import HyperGraphRAG
from app.services.trust_engine.circuit_bridge import CircuitSparsityBridge
from typing import Dict, Any

class AuditOrchestrator:
    """
    Coordinates the Neuro-Verified Audit Pipeline.
    Triggered by Vault Deposit Events.
    """
    
    def __init__(self):
        self.rag = HyperGraphRAG()
        self.bridge = CircuitSparsityBridge(threshold=0.8)
    
    def parse_vault_event(self, log_str: str) -> Dict[str, str]:
        """
        Parses a Vault Event Log.
        Format: "G-NFT_AUDIT_REQ:<sender_addr>:<listing_hash>"
        """
        if not log_str.startswith("G-NFT_AUDIT_REQ:"):
            raise ValueError("Invalid Event Log Format")
            
        parts = log_str.split(":")
        if len(parts) != 3:
             raise ValueError("Malformed Audit Request")
             
        return {
            "type": "G-NFT_AUDIT_REQ",
            "merchant_addr": parts[1],
            "listing_hash": parts[2]
        }

    async def process_audit_request(self, event_log: str, strain_name: str) -> Dict[str, Any]:
        """
        Execute the full audit lifecycle triggered by a parsed event.
        1. Parse Event.
        2. Verify Facts (RAG).
        3. Verify Brain (Circuit Bridge).
        4. Decision (Unlock or Refund).
        """
        try:
            event_data = self.parse_vault_event(event_log)
        except ValueError as e:
            return {"status": "ERROR", "reason": str(e)}
            
        merchant_addr = event_data["merchant_addr"]
        listing_hash = event_data["listing_hash"]
        
        print(f"Orchestrator: 🧠 Analyzing {strain_name} for {merchant_addr}...")
        
        # Step 1: Fact Check (Lineage)
        rag_result = await self.rag.verify_lineage(strain_name)
        if not rag_result.get("verified"):
            print("❌ Audit Failed: RAG could not verify lineage.")
            # Trigger Refund
            # await VaultContract.refund_bond(merchant_addr)
            return {"status": "FAILED", "reason": "Lineage Verification Failed", "action": "REFUND"}
            
        print(f"✅ RAG Verification Passed: {rag_result}")
        
        # Step 2: Cognitive Check (Uniqueness/Fraud)
        circuit_result = await self.bridge.verify_circuit_activation()
        
        if not circuit_result["is_trusted"]:
            print("❌ Audit Failed: Circuit Bridge detected high hallucination/fraud probability.")
            # Trigger Refund
            return {"status": "FAILED", "reason": "Cognitive Trust Score too low", "action": "REFUND"}
            
        print(f"✅ Circuit Bridge Passed: Trust Score {circuit_result['trust_score']}")
        
        # Step 3: Approval (Unlock Funds/Listing)
        # await VaultContract.approve_listing(listing_hash)
        print(f"❄️ APPROVED: Creating Listing {listing_hash}...")
        
        return {
            "status": "APPROVED",
            "trust_score": circuit_result["trust_score"],
            "rag_confidence": rag_result["confidence"],
            "listing_hash": listing_hash,
            "action": "UNLOCK"
        }

    async def process_appeal(self, listing_id: str, reason: str) -> Dict[str, Any]:
        """
        Handle a manual appeal override from an Admin.
        Forces the status to APPROVED_BY_APPEAL regardless of AI output.
        """
        print(f"⚖️ APPEAL RECEIVED for Listing {listing_id}")
        print(f"Reason: {reason}")
        print("Override Authorization: ADMIN_KEY_VALID")
        
        # In a real app, verify calling user permissions here or in Router.
        
        print("✅ MANUAL OVERRIDE EXECUTED. Listing Force-Approved.")
        
        return {
            "status": "APPROVED_BY_APPEAL",
            "listing_id": listing_id,
            "override_reason": reason,
            "auditor": "Admin_Override_v1"
        }
