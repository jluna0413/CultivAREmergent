"""
User Genetics model for tracking source genetics (mothers, seeds, pollen).
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.models_async.base import Base

class GeneticsType(enum.Enum):
    SEED = "seed"
    CLONE = "clone"
    POLLEN = "pollen"
    MOTHER = "mother"

class UserGenetics(Base):
    """
    Represents a specific genetic asset owned by a user.
    Used as the source for G-NFT minting.
    """
    __tablename__ = "user_genetics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    genetics_type = Column(Enum(GeneticsType), default=GeneticsType.MOTHER)
    description = Column(Text)
    
    # Optional link to cultivar info
    cultivar_id = Column(Integer, ForeignKey("cultivars.id"))

    # Lineage
    lineage_string = Column(String(255))  # "Parent1 x Parent2"
    pheno_number = Column(Integer, nullable=True)  # Added per user request
    parent1_id = Column(Integer, ForeignKey("user_genetics.id"))
    parent2_id = Column(Integer, ForeignKey("user_genetics.id"))
    generation = Column(Integer)  # F1, F2, etc.

    # Cannabinoids
    thc_percentage = Column(Float)
    cbd_percentage = Column(Float)
    indica_percentage = Column(Float)
    sativa_percentage = Column(Float)

    # Terpenes
    dominant_terpenes = Column(JSON)  # ["Myrcene", "Limonene"]

    # Breeding
    flower_time_days = Column(Integer)
    is_stabilized = Column(Boolean)
    
    # G-NFT linkage (One genetics source can start a pack run)
    gnft_pack_id = Column(Integer, ForeignKey("gnft_packs.id"))
    
    # Tracking
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User")
    cultivar = relationship("Cultivar")
    parent1 = relationship("UserGenetics", remote_side=[id], foreign_keys=[parent1_id])
    parent2 = relationship("UserGenetics", remote_side=[id], foreign_keys=[parent2_id])
    # gnft_pack = relationship("GNFTPack") # Avoid circular import issues for now, or use string reference if possible
