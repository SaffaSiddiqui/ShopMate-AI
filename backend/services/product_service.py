from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from backend.services.store_data import store
from backend.models.product import ProductCreate, ProductUpdate


class ProductService:
    @staticmethod
    def get_all(
        search: Optional[str] = None,
        category: Optional[str] = None,
        low_stock_only: Optional[bool] = False,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        results = list(store.products)

        if search and isinstance(search, str):
            q = search.lower().strip()
            results = [
                p for p in results
                if q in p["name"].lower() or q in p["sku"].lower() or q in p["category"].lower()
            ]

        if category and isinstance(category, str):
            results = [p for p in results if p["category"].lower() == category.lower().strip()]

        if low_stock_only is True:
            results = [p for p in results if p["stock"] < 10]

        if min_price is not None and isinstance(min_price, (int, float)):
            results = [p for p in results if p["price"] >= min_price]

        if max_price is not None and isinstance(max_price, (int, float)):
            results = [p for p in results if p["price"] <= max_price]

        return results

    @staticmethod
    def get_by_sku(sku: str) -> Dict[str, Any]:
        normalized_sku = sku.strip().upper()
        for p in store.products:
            if p["sku"].upper() == normalized_sku:
                return p
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with SKU '{sku}' not found",
        )

    @staticmethod
    def create(data: ProductCreate) -> Dict[str, Any]:
        normalized_sku = data.sku.strip().upper()
        # Check duplicate SKU
        for p in store.products:
            if p["sku"].upper() == normalized_sku:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product with SKU '{data.sku}' already exists",
                )

        product_dict = data.model_dump()
        product_dict["sku"] = normalized_sku
        store.add_product(product_dict)
        return product_dict

    @staticmethod
    def update(sku: str, data: ProductUpdate) -> Dict[str, Any]:
        product = ProductService.get_by_sku(sku)
        update_fields = data.model_dump(exclude_unset=True)

        for key, value in update_fields.items():
            if value is not None:
                product[key] = value

        store.update_product(product)
        return product

    @staticmethod
    def delete(sku: str) -> Dict[str, Any]:
        product = ProductService.get_by_sku(sku)
        store.delete_product(product["sku"])
        return product
