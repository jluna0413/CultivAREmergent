from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
import json
from app.services.trust_engine.hypergraph_rag import HyperGraphRAG
from app.services.trust_engine.circuit_bridge import CircuitSparsityBridge
from app.models_async.trust import AuditLog
from datetime import datetime

class AsyncAuditOrchestrator:
    """
    Coordinates the Neuro-Verified Audit Pipeline (Async).
    Fully integrated with Postgres via SQLAlchemy AsyncSession.
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.rag = HyperGraphRAG() # Assumes mostly stateless or handles its own async connections
        self.bridge = CircuitSparsityBridge(threshold=0.8)
    
    async def process_audit_request(self, trigger_type: str, listing_hash: str, merchant_addr: str, strain_name: str) -> Dict[str, Any]:
        """
        Execute the full audit lifecycle:
        1. Create PENDING, 2. Verify Facts, 3. Verify Circuits, 4. Decision, 5. Persist.
        """
        
        # 1. Create Initial Log
        audit_log = AuditLog(
            listing_id=listing_hash,
            merchant_id=merchant_addr,
            strain_name=strain_name,
            trigger_type=trigger_type,
            status="PENDING"
        )
        self.db.add(audit_log)
        await self.db.commit()
        await self.db.refresh(audit_log)
        
        print(f"Orchestrator: 🧠 Analyzing {strain_name} for {merchant_addr} (Log ID: {audit_log.id})...")
        
        # 2. Fact Check with GeneticsDataAgent (Hybrid B+C: DB → Cache → SeedFinder)
        from app.services.agents.genetics_data_agent import GeneticsDataAgent
        
        genetics_agent = GeneticsDataAgent(self.db)
        try:
            agent_result = await genetics_agent.verify_for_trust_engine(strain_name)
        finally:
            await genetics_agent.close()
        
        # 2a. HyperGraph RAG verification (Graph + SQL)
        rag_result = await self.rag.verify_lineage(strain_name)
        audit_log.rag_confidence = rag_result.get("confidence", 0.0)
        
        # 2b. Enrich RAG result with agent data
        if agent_result.get("strain_verified"):
            rag_result["agent_verified"] = True
            rag_result["agent_source"] = agent_result.get("data_source")
            rag_result["agent_confidence"] = agent_result.get("confidence", 0.0)
            rag_result["lineage"] = agent_result.get("lineage", {})
            rag_result["thc_content"] = agent_result.get("thc_content")
            rag_result["cbd_content"] = agent_result.get("cbd_content")
            
            # Boost RAG confidence if agent found data
            if not rag_result.get("verified") and agent_result.get("confidence", 0) > 0.7:
                rag_result["verified"] = True
                rag_result["confidence"] = max(rag_result.get("confidence", 0), agent_result["confidence"])
                audit_log.rag_confidence = rag_result["confidence"]
                print(f"🔍 Agent enriched verification: {agent_result['data_source']}")
        
        # 2c. Breeder Verification
        breeder_verified = agent_result.get("breeder_verified", False)
        if breeder_verified:
            rag_result["master_breeder"] = agent_result.get("breeder_data", {})
            rag_result["master_breeder"]["verified"] = True

        if not rag_result.get("verified"):
           return await self._finalize_audit(audit_log, "FAILED", "REFUND", rag_result, {}, "Lineage Verification Failed")

        print(f"✅ Verification Passed: {rag_result}")

        # 3. Cognitive Check (Uniqueness/Fraud)
        circuit_result = await self.bridge.verify_circuit_activation()
        audit_log.trust_score = circuit_result.get("trust_score", 0.0)
        
        # Trust Score Adjustments
        if breeder_verified:
            audit_log.trust_score = min(1.0, audit_log.trust_score + 0.1)
            print(f"💎 Verified Breeder Bonus: +0.1")
        
        if agent_result.get("strain_verified") and agent_result.get("data_source") == "seedfinder.eu":
            audit_log.trust_score = min(1.0, audit_log.trust_score + 0.05)
            print(f"🌐 External Verification Bonus: +0.05")

        if not circuit_result.get("is_trusted") and audit_log.trust_score < 0.7:
             return await self._finalize_audit(audit_log, "FAILED", "REFUND", rag_result, circuit_result, "Cognitive Trust Score too low")

        print(f"✅ Circuit Bridge Passed: Trust Score {audit_log.trust_score}")

        # 4. Success
        return await self._finalize_audit(audit_log, "APPROVED", "UNLOCK", rag_result, circuit_result)

    async def _finalize_audit(self, 
                              log: AuditLog, 
                              status: str, 
                              action: str, 
                              rag_data: Dict, 
                              circuit_data: Dict,
                              reason: str = None) -> Dict[str, Any]:
        """
        Helper to update the DB and return the final dict.
        """
        log.status = status
        log.decision_action = action
        log.finalized_at = datetime.utcnow()
        
        full_data = {
            "rag": rag_data,
            "circuit": circuit_data,
            "reason": reason
        }
        log.raw_data = full_data # SQLAlchemy handles JSON serialization if type is JSON
        
        await self.db.commit()
        await self.db.refresh(log)
        
        return {
            "status": status,
            "action": action,
            "trust_score": log.trust_score,
            "rag_confidence": log.rag_confidence,
            "listing_hash": log.listing_id,
            "reason": reason,
            "log_id": log.id
        }

    async def process_appeal(self, listing_id: str, reason: str, admin_user: str) -> Dict[str, Any]:
        """
        Handle a manual appeal override from an Admin.
        """
        # Create a specific log for the appeal
        audit_log = AuditLog(
            listing_id=listing_id,
            strain_name="Unknown (Appeal)", # Might need to fetch this
            trigger_type="MANUAL_APPEAL",
            status="APPROVED_BY_APPEAL",
            decision_action="UNLOCK",
            raw_data={"appeal_reason": reason, "admin": admin_user},
            finalized_at=datetime.utcnow()
        )
        self.db.add(audit_log)
        await self.db.commit()
        
        return {
            "status": "APPROVED_BY_APPEAL",
            "listing_id": listing_id,
            "override_reason": reason,
            "auditor": admin_user,
            "log_id": audit_log.id
        }
