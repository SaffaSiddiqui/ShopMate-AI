from typing import List, Dict, Any
from backend.services.database import database


class StoreData:
    """SQLite-backed store initialized with Pakistani shop sample data."""

    def __init__(self):
        self.db = database
        self._load_seed_data()
        self.db.seed_if_empty(self._seed_payload())

    def _load_seed_data(self):
        self._sales_data_7d: List[Dict[str, Any]] = [
            {"day": "Mon", "sales": 4800.0, "orders": 6},
            {"day": "Tue", "sales": 6200.0, "orders": 8},
            {"day": "Wed", "sales": 5500.0, "orders": 7},
            {"day": "Thu", "sales": 7100.0, "orders": 9},
            {"day": "Fri", "sales": 6800.0, "orders": 8},
            {"day": "Sat", "sales": 9100.0, "orders": 12},
            {"day": "Sun", "sales": 8300.0, "orders": 10},
        ]

        self._sales_data_30d: List[Dict[str, Any]] = [
            {"day": "Week 1", "sales": 39700.0, "orders": 51},
            {"day": "Week 2", "sales": 42100.0, "orders": 58},
            {"day": "Week 3", "sales": 45600.0, "orders": 65},
            {"day": "Week 4", "sales": 46850.0, "orders": 74},
        ]

        self._products: List[Dict[str, Any]] = [
            {
                "name": "Premium Basmati Rice",
                "category": "Grocery",
                "sku": "GR-1024",
                "price": 1850.0,
                "stock": 48,
                "sold": 142,
                "emoji": "🍚",
                "color": "sand",
            },
            {
                "name": "Sufi Cooking Oil 5L",
                "category": "Grocery",
                "sku": "GR-1031",
                "price": 2750.0,
                "stock": 9,
                "sold": 98,
                "emoji": "🫒",
                "color": "mint",
            },
            {
                "name": "Everyday Cotton Kurta",
                "category": "Clothing",
                "sku": "CL-2042",
                "price": 3200.0,
                "stock": 26,
                "sold": 86,
                "emoji": "👕",
                "color": "lilac",
            },
            {
                "name": "Royal Chai Blend",
                "category": "Beverages",
                "sku": "BV-3018",
                "price": 980.0,
                "stock": 6,
                "sold": 74,
                "emoji": "🍵",
                "color": "peach",
            },
            {
                "name": "Handwoven Khussa",
                "category": "Footwear",
                "sku": "FW-4056",
                "price": 4500.0,
                "stock": 18,
                "sold": 63,
                "emoji": "🥿",
                "color": "pink",
            },
            {
                "name": "Ajwa Dates (500g)",
                "category": "Grocery",
                "sku": "GR-1067",
                "price": 2250.0,
                "stock": 34,
                "sold": 51,
                "emoji": "🌴",
                "color": "sand",
            },
        ]

        self._orders: List[Dict[str, Any]] = [
            {
                "id": "#SM-2084",
                "customer": "Ayesha Khan",
                "initials": "AK",
                "item": "Premium Basmati Rice",
                "date": "Today, 10:42 AM",
                "amount": 4650.0,
                "status": "Processing",
                "color": "blue",
            },
            {
                "id": "#SM-2083",
                "customer": "Usman Ali",
                "initials": "UA",
                "item": "Everyday Cotton Kurta",
                "date": "Today, 10:18 AM",
                "amount": 3200.0,
                "status": "Shipped",
                "color": "purple",
            },
            {
                "id": "#SM-2082",
                "customer": "Fatima Sheikh",
                "initials": "FS",
                "item": "Sufi Cooking Oil 5L",
                "date": "Today, 9:56 AM",
                "amount": 5500.0,
                "status": "Delivered",
                "color": "green",
            },
            {
                "id": "#SM-2081",
                "customer": "Bilal Ahmed",
                "initials": "BA",
                "item": "Royal Chai Blend",
                "date": "Today, 9:30 AM",
                "amount": 1960.0,
                "status": "Processing",
                "color": "orange",
            },
            {
                "id": "#SM-2080",
                "customer": "Maham Raza",
                "initials": "MR",
                "item": "Handwoven Khussa",
                "date": "Yesterday, 6:12 PM",
                "amount": 4500.0,
                "status": "Delivered",
                "color": "pink",
            },
        ]

        self._customers: List[Dict[str, Any]] = [
            {
                "name": "Ayesha Khan",
                "phone": "+92 300 1234567",
                "city": "Lahore",
                "orders": 12,
                "spent": 38400.0,
                "initials": "AK",
                "color": "blue",
            },
            {
                "name": "Usman Ali",
                "phone": "+92 321 7654321",
                "city": "Karachi",
                "orders": 8,
                "spent": 26750.0,
                "initials": "UA",
                "color": "purple",
            },
            {
                "name": "Fatima Sheikh",
                "phone": "+92 333 9876543",
                "city": "Islamabad",
                "orders": 7,
                "spent": 22100.0,
                "initials": "FS",
                "color": "green",
            },
            {
                "name": "Bilal Ahmed",
                "phone": "+92 312 4567890",
                "city": "Faisalabad",
                "orders": 5,
                "spent": 15800.0,
                "initials": "BA",
                "color": "orange",
            },
            {
                "name": "Maham Raza",
                "phone": "+92 301 8765432",
                "city": "Rawalpindi",
                "orders": 4,
                "spent": 12400.0,
                "initials": "MR",
                "color": "pink",
            },
        ]

    def _seed_payload(self) -> Dict[str, List[Dict[str, Any]]]:
        return {
            "sales_7d": self._sales_data_7d,
            "sales_30d": self._sales_data_30d,
            "products": self._products,
            "orders": self._orders,
            "customers": self._customers,
        }

    def reset(self) -> None:
        self._load_seed_data()
        self.db.reset(self._seed_payload())

    @property
    def sales_data_7d(self) -> List[Dict[str, Any]]:
        return self.db.get_all("sales_7d")

    @property
    def sales_data_30d(self) -> List[Dict[str, Any]]:
        return self.db.get_all("sales_30d")

    @property
    def products(self) -> List[Dict[str, Any]]:
        return self.db.get_all("products")

    @property
    def orders(self) -> List[Dict[str, Any]]:
        return self.db.get_all("orders")

    @property
    def customers(self) -> List[Dict[str, Any]]:
        return self.db.get_all("customers")

    def add_product(self, product: Dict[str, Any]) -> None:
        self.db.add("products", product)

    def update_product(self, product: Dict[str, Any]) -> None:
        self.db.update("products", product["sku"], product)

    def delete_product(self, sku: str) -> None:
        self.db.delete("products", sku)

    def add_order(self, order: Dict[str, Any]) -> None:
        self.db.add("orders", order, prepend=True)

    def create_order_with_stock(
        self,
        order: Dict[str, Any],
        sku: str,
        quantity: int,
    ) -> None:
        self.db.create_order_with_stock(order, sku, quantity)

    def update_order(self, order: Dict[str, Any]) -> None:
        self.db.update("orders", order["id"], order)

    def update_order_status(self, order: Dict[str, Any], status: str) -> None:
        self.db.update_order_status(order["id"], order, status)

    def delete_order(self, order_id: str) -> None:
        self.db.delete("orders", order_id)

    def delete_order_and_restore_stock(self, order_id: str) -> Dict[str, Any]:
        return self.db.delete_order_and_restore_stock(order_id)

    def add_customer(self, customer: Dict[str, Any]) -> None:
        self.db.add("customers", customer)

    def update_customer(self, customer: Dict[str, Any]) -> None:
        self.db.update("customers", customer["phone"], customer)

    def delete_customer(self, phone: str) -> None:
        self.db.delete("customers", phone)


# Global singleton instance
store = StoreData()
