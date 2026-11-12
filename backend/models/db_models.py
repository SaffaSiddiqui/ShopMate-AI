"""
SQLAlchemy ORM models for ShopMate AI database tables.
Defines Product, Order, OrderItem, Customer tables.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.database import Base


class ProductDB(Base):
    """Products table — maps to in-memory store.products list."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    unit = Column(String(50), default="piece")
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to order items
    order_items = relationship("OrderItemDB", back_populates="product")


class CustomerDB(Base):
    """Customers table — maps to in-memory store.customers list."""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, index=True)
    phone = Column(String(50), unique=True, index=True)
    city = Column(String(100), default="")
    address = Column(Text, default="")
    total_orders = Column(Integer, default=0)
    total_spent = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to orders
    orders = relationship("OrderDB", back_populates="customer")


class OrderDB(Base):
    """Orders table — maps to in-memory store.orders list."""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(50), unique=True, index=True, nullable=False)
    customer_name = Column(String(200), nullable=False)
    customer_phone = Column(String(50), default="")
    customer_city = Column(String(100), default="")
    status = Column(String(50), default="Processing")
    total = Column(Float, default=0.0)
    payment_method = Column(String(100), default="Cash on Delivery")
    notes = Column(Text, default="")
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("CustomerDB", back_populates="orders")
    items = relationship("OrderItemDB", back_populates="order", cascade="all, delete-orphan")


class OrderItemDB(Base):
    """Order items table — line items within each order."""
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    sku = Column(String(50), nullable=False)
    name = Column(String(200), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)

    # Relationships
    order = relationship("OrderDB", back_populates="items")
    product = relationship("ProductDB", back_populates="order_items")

