from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class OrderStatus(str, Enum):
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class OrderBase(BaseModel):
    customer: str = Field(..., min_length=1, max_length=100, description="Customer full name")
    item: str = Field(..., min_length=1, max_length=100, description="Item ordered")
    amount: float = Field(..., gt=0, description="Total order amount in PKR")
    status: OrderStatus = Field(default=OrderStatus.PROCESSING, description="Order status")
    initials: Optional[str] = Field(None, description="Customer initials for avatar")
    color: Optional[str] = Field("blue", description="Avatar color theme")


class OrderCreate(OrderBase):
    product_sku: Optional[str] = Field(None, min_length=2, max_length=30)
    quantity: int = Field(default=1, ge=1)


class OrderStatusUpdate(BaseModel):
    status: OrderStatus = Field(..., description="New order status")


class OrderResponse(OrderBase):
    id: str = Field(..., description="Unique Order ID (e.g. #SM-2084)")
    date: str = Field(..., description="Order creation date timestamp string")

    class Config:
        from_attributes = True
