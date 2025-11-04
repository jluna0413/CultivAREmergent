"""
Async Commerce Models
Order and Product models for e-commerce features.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models_async.base import Base


class Product(Base):
    """Product model for marketplace."""
    
    __tablename__ = "product"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Pricing
    price: Mapped[float] = mapped_column(Float, nullable=False)
    compare_at_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Inventory
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sku: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True)
    
    # Categorization
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Media
    featured_image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    @property
    def in_stock(self) -> bool:
        """Check if product is in stock."""
        return self.stock_quantity > 0
    
    @property
    def on_sale(self) -> bool:
        """Check if product is on sale."""
        return self.compare_at_price is not None and self.price < self.compare_at_price
    
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"


class Order(Base):
    """Order model for purchases."""
    
    __tablename__ = "order"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    
    # Order Info
    order_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default='pending', nullable=False)
    
    # Pricing
    subtotal: Mapped[float] = mapped_column(Float, nullable=False)
    tax: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    shipping: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Customer Info
    customer_email: Mapped[str] = mapped_column(String(120), nullable=False)
    customer_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Shipping
    shipping_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Payment
    payment_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    payment_status: Mapped[str] = mapped_column(String(50), default='unpaid', nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self) -> str:
        return f"<Order(id={self.id}, order_number='{self.order_number}', status='{self.status}')>"


class OrderItem(Base):
    """Order line item model."""
    
    __tablename__ = "order_item"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("order.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.id"), nullable=False)
    
    # Item Details
    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    subtotal: Mapped[float] = mapped_column(Float, nullable=False)
    
    def __repr__(self) -> str:
        return f"<OrderItem(id={self.id}, product='{self.product_name}', qty={self.quantity})>"
