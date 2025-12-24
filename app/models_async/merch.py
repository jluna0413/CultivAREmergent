
from datetime import datetime
from typing import Optional
import enum

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, 
    Text, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import relationship

from .base import Base

class ProductCategory(enum.Enum):
    """Categories for merchandise"""
    APPAREL = "apparel"
    EQUIPMENT = "equipment"
    ACCESSORY = "accessory"
    NUTRIENT = "nutrient"
    SUBSCRIPTION = "subscription"
    GENETICS = "genetics"
    GROW_GEAR = "grow_gear"
    OTHER = "other"

class MerchProduct(Base):
    """
    Traditional ecommerce products (non-NFT).
    """
    __tablename__ = "merch_products"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Product Details
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(SQLEnum(ProductCategory), default=ProductCategory.OTHER, nullable=False, index=True)
    
    # Pricing & Inventory
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    sku = Column(String(50), unique=True, nullable=True)
    
    # Media
    image_url = Column(String(500), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = relationship("MerchOrder", back_populates="product")
    
    def __repr__(self):
        return f"<MerchProduct(id={self.id}, name={self.name}, price={self.price})>"

class MerchOrderStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class MerchOrder(Base):
    """
    Orders specific to merchandise.
    """
    __tablename__ = "merch_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Buyer
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Product (Simple 1 product per order for MVP, or could be relation to OrderItem)
    # Keeping it simple as requested for Phase 1.1 "Create merch marketplace tables"
    product_id = Column(Integer, ForeignKey("merch_products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    
    # Payment
    total_amount = Column(Float, nullable=False)
    status = Column(SQLEnum(MerchOrderStatus), default=MerchOrderStatus.PENDING, index=True)
    payment_txn_id = Column(String(100), nullable=True)
    
    # Shipping
    shipping_address = Column(Text, nullable=True)
    tracking_number = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    product = relationship("MerchProduct", back_populates="orders")
    
    def __repr__(self):
        return f"<MerchOrder(id={self.id}, user_id={self.user_id}, status={self.status})>"
