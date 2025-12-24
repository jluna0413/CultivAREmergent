"""
Soulbound Token (SBT) models for the Burn-to-Redeem workflow.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.models_async.base import Base

class SBTBadgeTier(enum.Enum):
    MASTER_GROWER = "Master Grower" # 100% Consumption
    CULTIVATOR = "Cultivator"       # < 100% Consumption
    NOVICE = "Novice"               # minimal / error fallback

class GrowJournalSBT(Base):
    """
    Soulbound Token issued when a G-NFT is burned.
    Proves consumption and growing experience.
    """
    __tablename__ = "grow_journal_sbts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Origin Metadata
    burned_gnft_id = Column(String(100), nullable=False) # The original NFT ID (ASA ID)
    strain_name = Column(String(100), nullable=False)
    
    # Tokenomics / Stats
    pack_size = Column(Integer, default=10)
    seeds_planted = Column(Integer, default=0)
    consumption_ratio = Column(Float, default=0.0) # 0.0 to 1.0
    
    badge_tier = Column(Enum(SBTBadgeTier), default=SBTBadgeTier.CULTIVATOR)
    
    # Blockchain Data
    sbt_asa_id = Column(String(100), nullable=True) # The ID of the minted SBT on Algo
    mint_tx_id = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="sbts")
