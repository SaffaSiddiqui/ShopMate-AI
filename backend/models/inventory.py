from pydantic import BaseModel, Field
from typing import List, Optional


class RestockRequest(BaseModel):
    quantity: int = Field(..., gt=0, description="Number of units to add to stock")


class InventoryItemResponse(BaseModel):
    sku: str
    name: str
    category: str
    price: float
    stock: int
    sold: int
    emoji: str
    color: str
    stock_status: str = Field(..., description="'Low stock' (<10), 'Running low' (10-14), or 'In stock' (>=15)")
    is_critical: bool = Field(..., description="True if stock < 10")


class InventorySummaryResponse(BaseModel):
    total_units: int
    well_stocked_count: int
    running_low_count: int
    critical_stock_count: int
    total_products: int
    items: List[InventoryItemResponse]

