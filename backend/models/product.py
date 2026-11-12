from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Product display name")
    category: str = Field(..., min_length=1, max_length=50, description="Product category")
    sku: str = Field(..., min_length=2, max_length=30, description="Unique SKU code (e.g. GR-1024)")
    price: float = Field(..., gt=0, description="Product price in PKR")
    stock: int = Field(..., ge=0, description="Current stock units available")
    sold: int = Field(default=0, ge=0, description="Total units sold")
    emoji: str = Field(default="📦", description="Emoji icon for product")
    color: str = Field(default="blue", description="Theme color tag (e.g. sand, mint, lilac, peach, pink)")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    sold: Optional[int] = Field(None, ge=0)
    emoji: Optional[str] = None
    color: Optional[str] = None


class ProductResponse(ProductBase):
    class Config:
        from_attributes = True

