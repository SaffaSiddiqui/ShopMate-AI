from typing import List, Dict, Any
from backend.services.store_data import store


class AnalyticsService:
    @staticmethod
    def get_sales_data(period: str = "7 days") -> List[Dict[str, Any]]:
        if period == "30 days":
            return store.sales_data_30d
        return store.sales_data_7d

    @staticmethod
    def get_top_products(limit: int = 5) -> List[Dict[str, Any]]:
        sorted_products = sorted(store.products, key=lambda p: p.get("sold", 0), reverse=True)
        top = sorted_products[:limit]
        return [
            {
                "name": p["name"],
                "sku": p["sku"],
                "sold": p.get("sold", 0),
                "price": p["price"],
                "revenue": p.get("sold", 0) * p["price"],
                "emoji": p.get("emoji", "📦"),
                "color": p.get("color", "blue"),
            }
            for p in top
        ]

    @staticmethod
    def get_category_stats() -> List[Dict[str, Any]]:
        cat_map: Dict[str, Dict[str, Any]] = {}
        for p in store.products:
            cat = p.get("category", "Uncategorized")
            if cat not in cat_map:
                cat_map[cat] = {
                    "category": cat,
                    "total_sales": 0.0,
                    "units_sold": 0,
                    "product_count": 0,
                }
            sold = p.get("sold", 0)
            price = p.get("price", 0.0)
            cat_map[cat]["units_sold"] += sold
            cat_map[cat]["total_sales"] += sold * price
            cat_map[cat]["product_count"] += 1

        return list(cat_map.values())

    @staticmethod
    def get_overview(period: str = "7 days") -> Dict[str, Any]:
        sales_records = AnalyticsService.get_sales_data(period)
        gross_sales = sum(item["sales"] for item in sales_records)
        total_orders = sum(item["orders"] for item in sales_records)
        avg_order = round(gross_sales / total_orders, 2) if total_orders > 0 else 0.0

        peak_day_record = max(sales_records, key=lambda item: item["sales"], default={"day": "N/A", "sales": 0.0, "orders": 0})

        top_products = AnalyticsService.get_top_products(limit=5)
        categories = AnalyticsService.get_category_stats()

        return {
            "gross_sales": gross_sales,
            "total_orders": total_orders,
            "average_order_value": avg_order,
            "period": period,
            "growth_rate": 12.8,
            "peak_day": {
                "day": peak_day_record["day"],
                "sales": peak_day_record["sales"],
                "orders": peak_day_record["orders"],
            },
            "sales_by_day": sales_records,
            "top_products": top_products,
            "categories": categories,
        }

