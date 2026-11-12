from pydantic import BaseModel, Field
from typing import Optional


class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Customer name")
    phone: str = Field(..., min_length=7, max_length=20, description="Contact phone number")
    city: str = Field(..., min_length=1, max_length=50, description="City location")
    orders: int = Field(default=0, ge=0, description="Total completed orders")
    spent: float = Field(default=0.0, ge=0.0, description="Total amount spent in PKR")
    initials: Optional[str] = Field(None, description="Customer initials")
    color: Optional[str] = Field("blue", description="Avatar color theme")


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    city: Optional[str] = Field(None, min_length=1, max_length=50)
    orders: Optional[int] = Field(None, ge=0)
    spent: Optional[float] = Field(None, ge=0.0)
    color: Optional[str] = None


class CustomerResponse(CustomerBase):
    class Config:
        from_attributes = True

