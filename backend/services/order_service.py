from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import HTTPException, status
from backend.services.store_data import store
from backend.models.order import OrderCreate, OrderStatus


class OrderService:
    @staticmethod
    def _extract_initials(name: str) -> str:
        parts = name.strip().split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        elif parts:
            return parts[0][:2].upper()
        return "CU"

    @staticmethod
    def _generate_order_id() -> str:
        highest = 2080
        for o in store.orders:
            raw_id = o.get("id", "").replace("#SM-", "").replace("SM-", "")
            if raw_id.isdigit():
                highest = max(highest, int(raw_id))
        return f"#SM-{highest + 1}"

    @staticmethod
    def get_all(
        status_filter: Optional[str] = None,
        customer_filter: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        results = list(store.orders)

        if status_filter and isinstance(status_filter, str):
            results = [
                o for o in results
                if o.get("status", "").lower() == status_filter.lower().strip()
            ]

        if customer_filter and isinstance(customer_filter, str):
            c = customer_filter.lower().strip()
            results = [o for o in results if c in o.get("customer", "").lower()]

        if search and isinstance(search, str):
            q = search.lower().strip()
            results = [
                o for o in results
                if q in o.get("id", "").lower()
                or q in o.get("customer", "").lower()
                or q in o.get("item", "").lower()
                or q in o.get("status", "").lower()
            ]

        return results

    @staticmethod
    def get_by_id(order_id: str) -> Dict[str, Any]:
        normalized = order_id.strip().upper()
        if not normalized.startswith("#"):
            normalized_with_hash = f"#{normalized}"
        else:
            normalized_with_hash = normalized

        for o in store.orders:
            current_id = o["id"].upper()
            if current_id == normalized or current_id == normalized_with_hash:
                return o

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID '{order_id}' not found",
        )

    @staticmethod
    def create(data: OrderCreate) -> Dict[str, Any]:
        order_dict = data.model_dump()
        product_sku = order_dict.pop("product_sku")
        quantity = order_dict.pop("quantity")
        order_dict["id"] = OrderService._generate_order_id()

        if not order_dict.get("initials"):
            order_dict["initials"] = OrderService._extract_initials(order_dict["customer"])

        order_dict["date"] = datetime.now().strftime("Today, %I:%M %p")
        order_dict["status"] = data.status.value

        if product_sku:
            order_dict["product_sku"] = product_sku.strip().upper()
            order_dict["quantity"] = quantity
            try:
                store.create_order_with_stock(
                    order_dict, order_dict["product_sku"], quantity
                )
            except KeyError:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with SKU '{product_sku}' not found",
                )
            except ValueError as exc:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=str(exc),
                )
        else:
            store.add_order(order_dict)
        return order_dict

    @staticmethod
    def update_status(order_id: str, new_status: OrderStatus) -> Dict[str, Any]:
        order = OrderService.get_by_id(order_id)
        try:
            store.update_order_status(order, new_status.value)
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product for order '{order_id}' not found",
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(exc),
            )
        return order

    @staticmethod
    def delete(order_id: str) -> Dict[str, Any]:
        order = OrderService.get_by_id(order_id)
        if order.get("product_sku"):
            store.delete_order_and_restore_stock(order["id"])
        else:
            store.delete_order(order["id"])
        return order
