from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models_async.base import Base

class AuditLog(Base):
    """
    Immutable record of a Trust Engine verification event.
    Stores the inputs (strain, merchant) and outputs (scores, decision)
    of the Neuro-Verified Audit Pipeline.
    """
    __tablename__ = "trust_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Context
    listing_id = Column(String, index=True, nullable=True) # Hash or ID
    merchant_id = Column(String, index=True, nullable=True) # Wallet Address
    strain_name = Column(String, nullable=False)
    trigger_type = Column(String, default="G-NFT_MINT") # e.g., "G-NFT_MINT", "MANUAL_REQUEST"

    # Outcome
    status = Column(String, default="PENDING", index=True) # PENDING, APPROVED, FAILED, APPROVED_BY_APPEAL
    decision_action = Column(String, nullable=True) # UNLOCK, REFUND, NONE

    # Scoring
    trust_score = Column(Float, nullable=True) # 0.0 to 1.0 from Circuit Bridge
    rag_confidence = Column(Float, nullable=True) # 0.0 to 1.0 from HyperGraph
    
    # Forensic Data (JSON)
    raw_data = Column(JSON, nullable=True) # Full output from RAG and Circuit
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    finalized_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, strain='{self.strain_name}', status='{self.status}')>"
