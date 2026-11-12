from typing import List, Optional, Annotated
from fastapi import APIRouter, Query, status
from backend.models.product import ProductCreate, ProductUpdate, ProductResponse
from backend.services.product_service import ProductService

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("", response_model=List[ProductResponse])
def get_products(
    search: Annotated[Optional[str], Query(description="Search term for name, SKU, or category")] = None,
    category: Annotated[Optional[str], Query(description="Filter by category")] = None,
    low_stock: Annotated[bool, Query(description="Filter items with stock < 10")] = False,
    min_price: Annotated[Optional[float], Query(ge=0, description="Minimum price filter")] = None,
    max_price: Annotated[Optional[float], Query(ge=0, description="Maximum price filter")] = None,
):
    """Retrieve all products with optional filtering."""
    return ProductService.get_all(
        search=search,
        category=category,
        low_stock_only=low_stock,
        min_price=min_price,
        max_price=max_price,
    )


@router.get("/{sku}", response_model=ProductResponse)
def get_product(sku: str):
    """Retrieve a single product by SKU."""
    return ProductService.get_by_sku(sku)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    """Add a new product to the catalog."""
    return ProductService.create(product)


@router.put("/{sku}", response_model=ProductResponse)
def update_product(sku: str, update_data: ProductUpdate):
    """Update details of an existing product."""
    return ProductService.update(sku, update_data)


@router.delete("/{sku}", response_model=ProductResponse)
def delete_product(sku: str):
    """Delete a product by SKU."""
    return ProductService.delete(sku)
