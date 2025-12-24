
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class HypergraphStrainMapping(Base):
    """
    Mapping table linking SQL UserGenetics records to Graph Strain nodes.
    Used to quickly lookup the graph node ID for ancestry queries.
    """
    __tablename__ = "hypergraph_strain_mapping"
    
    genetics_id = Column(Integer, ForeignKey("user_genetics.id", ondelete="CASCADE"), primary_key=True)
    node_id = Column(String(64), unique=True, nullable=False, index=True)  # Hypergraph UUID
    synced_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship back to genetics
    genetics = relationship("UserGenetics", backref="hypergraph_mapping")

class HypergraphBreederMapping(Base):
    """
    Mapping table linking SQL MarketplaceBreeder records to Graph Breeder nodes.
    Used for compliance and reputation queries.
    """
    __tablename__ = "hypergraph_breeder_mapping"
    
    breeder_id = Column(Integer, ForeignKey("marketplace_breeders.id", ondelete="CASCADE"), primary_key=True)
    node_id = Column(String(64), unique=True, nullable=False, index=True)
    synced_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship back to breeder
    breeder = relationship("MarketplaceBreeder", backref="hypergraph_mapping")

class HypergraphCultivarMapping(Base):
    """
    Mapping table linking SQL master Cultivar records to Graph Strain nodes.
    Essential for global lineage research.
    """
    __tablename__ = "hypergraph_cultivar_mapping"
    
    cultivar_id = Column(Integer, ForeignKey("cultivars.id", ondelete="CASCADE"), primary_key=True)
    node_id = Column(String(64), unique=True, nullable=False, index=True)
    synced_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship back to cultivar
    cultivar = relationship("Cultivar", backref="hypergraph_mapping")
