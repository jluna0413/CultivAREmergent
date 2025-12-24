from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class CartItem(Base):
    """
    Items currently in a user's shopping cart.
    Persisted to allow multi-device cart sync.
    """
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    listing_id = Column(Integer, ForeignKey("gnft_listings.id"), nullable=False)
    
    quantity = Column(Integer, default=1)
    pack_size = Column(Integer, default=5) # 3, 5, 6, 10, 12
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    listing = relationship("GNFTListing")

    def __repr__(self):
        return f"<CartItem(user_id={self.user_id}, listing_id={self.listing_id}, qty={self.quantity})>"
