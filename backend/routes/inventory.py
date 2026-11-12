from typing import List, Annotated
from fastapi import APIRouter, Query
from backend.models.inventory import (
    RestockRequest,
    InventoryItemResponse,
    InventorySummaryResponse,
)
from backend.services.inventory_service import InventoryService

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])


@router.get("", response_model=InventorySummaryResponse)
def get_inventory():
    """Retrieve full inventory summary, metrics, and stock status."""
    return InventoryService.get_summary()


@router.get("/low-stock", response_model=List[InventoryItemResponse])
def get_low_stock(
    threshold: Annotated[int, Query(ge=1, description="Threshold below which stock is considered low")] = 10,
):
    """Retrieve items with stock below the given threshold."""
    return InventoryService.get_low_stock(threshold=threshold)


@router.post("/{sku}/restock")
def restock_product(sku: str, request: RestockRequest):
    """Restock a product by adding units to its inventory."""
    return InventoryService.restock(sku, request.quantity)
