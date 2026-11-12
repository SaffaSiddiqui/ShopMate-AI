from typing import List, Dict, Any
from fastapi import HTTPException, status
from backend.services.store_data import store
from backend.services.product_service import ProductService


class InventoryService:
    @staticmethod
    def _calculate_stock_status(stock: int) -> tuple[str, bool]:
        if stock < 10:
            return "Low stock", True
        elif stock < 15:
            return "Running low", False
        return "In stock", False

    @staticmethod
    def get_summary() -> Dict[str, Any]:
        items = []
        total_units = 0
        well_stocked = 0
        running_low = 0
        critical = 0

        for p in store.products:
            stock = p["stock"]
            total_units += stock
            status_label, is_crit = InventoryService._calculate_stock_status(stock)

            if stock < 10:
                critical += 1
            elif stock < 15:
                running_low += 1
            else:
                well_stocked += 1

            items.append({
                "sku": p["sku"],
                "name": p["name"],
                "category": p["category"],
                "price": p["price"],
                "stock": stock,
                "sold": p.get("sold", 0),
                "emoji": p.get("emoji", "📦"),
                "color": p.get("color", "blue"),
                "stock_status": status_label,
                "is_critical": is_crit,
            })

        return {
            "total_units": total_units,
            "well_stocked_count": well_stocked,
            "running_low_count": running_low,
            "critical_stock_count": critical,
            "total_products": len(store.products),
            "items": items,
        }

    @staticmethod
    def get_low_stock(threshold: int = 10) -> List[Dict[str, Any]]:
        results = []
        for p in store.products:
            if p["stock"] < threshold:
                status_label, is_crit = InventoryService._calculate_stock_status(p["stock"])
                results.append({
                    "sku": p["sku"],
                    "name": p["name"],
                    "category": p["category"],
                    "price": p["price"],
                    "stock": p["stock"],
                    "sold": p.get("sold", 0),
                    "emoji": p.get("emoji", "📦"),
                    "color": p.get("color", "blue"),
                    "stock_status": status_label,
                    "is_critical": is_crit,
                })
        return results

    @staticmethod
    def restock(sku: str, quantity: int) -> Dict[str, Any]:
        if quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restock quantity must be greater than zero",
            )
        product = ProductService.get_by_sku(sku)
        product["stock"] += quantity
        store.update_product(product)
        status_label, is_crit = InventoryService._calculate_stock_status(product["stock"])

        return {
            "sku": product["sku"],
            "name": product["name"],
            "category": product["category"],
            "price": product["price"],
            "stock": product["stock"],
            "sold": product.get("sold", 0),
            "emoji": product.get("emoji", "📦"),
            "color": product.get("color", "blue"),
            "stock_status": status_label,
            "is_critical": is_crit,
            "message": f"Successfully added {quantity} units to {product['name']}. Current stock: {product['stock']}",
        }
