from typing import List, Optional, Annotated
from fastapi import APIRouter, Query, status
from backend.models.order import OrderCreate, OrderResponse, OrderStatusUpdate
from backend.services.order_service import OrderService

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.get("", response_model=List[OrderResponse])
def get_orders(
    status_filter: Annotated[Optional[str], Query(alias="status", description="Filter by status (Processing, Shipped, Delivered, Cancelled)")] = None,
    customer: Annotated[Optional[str], Query(description="Filter by customer name")] = None,
    search: Annotated[Optional[str], Query(description="Search ID, customer, item, or status")] = None,
):
    """Retrieve orders with optional filtering."""
    return OrderService.get_all(
        status_filter=status_filter,
        customer_filter=customer,
        search=search,
    )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    """Retrieve an order by ID (e.g. #SM-2084 or SM-2084)."""
    return OrderService.get_by_id(order_id)


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
    """Create an order and, when a product SKU is provided, atomically reserve stock."""
    return OrderService.create(order)


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: str, status_update: OrderStatusUpdate):
    """Update order status (Processing, Shipped, Delivered, Cancelled)."""
    return OrderService.update_status(order_id, status_update.status)


@router.delete("/{order_id}", response_model=OrderResponse)
def delete_order(order_id: str):
    """Cancel and remove an order, restoring its reserved stock when applicable."""
    return OrderService.delete(order_id)
