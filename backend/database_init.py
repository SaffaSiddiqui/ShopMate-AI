"""
Database initialization and seeding for ShopMate AI.
Creates all tables and populates them with Pakistani shop sample data.
Run once on first startup — skips if data already exists.
"""

from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from backend.database import engine, Base, SessionLocal
from backend.models.db_models import ProductDB, CustomerDB, OrderDB, OrderItemDB


# ---------------------------------------------------------------------------
# Initial Pakistani Shop Data
# ---------------------------------------------------------------------------

INITIAL_PRODUCTS = [
    {"sku": "BAS-001", "name": "Basmati Rice (5kg)", "category": "Groceries", "price": 1200.0, "stock": 85, "unit": "bag", "description": "Premium long-grain Basmati rice from Punjab"},
    {"sku": "CHA-001", "name": "Chai Patti (500g)", "category": "Beverages", "price": 450.0, "stock": 120, "unit": "pack", "description": "Strong Danedar chai patti, perfect for doodh pati"},
    {"sku": "KUR-001", "name": "Kurta Shalwar (Men's)", "category": "Clothing", "price": 2500.0, "stock": 35, "unit": "set", "description": "Premium cotton kurta shalwar for men"},
    {"sku": "KHU-001", "name": "Khussa (Embroidered)", "category": "Footwear", "price": 1800.0, "stock": 22, "unit": "pair", "description": "Hand-crafted embroidered khussa shoes"},
    {"sku": "AJW-001", "name": "Ajwa Khajoor (1kg)", "category": "Dry Fruits", "price": 3200.0, "stock": 8, "unit": "kg", "description": "Premium Ajwa dates imported from Madinah"},
    {"sku": "MAN-001", "name": "Attar Mango (Dozen)", "category": "Fruits", "price": 800.0, "stock": 50, "unit": "dozen", "description": "Fresh Chaunsa mangoes from Multan"},
    {"sku": "LAC-001", "name": "Laccha Paratha (10pc)", "category": "Bakery", "price": 350.0, "stock": 40, "unit": "pack", "description": "Frozen flaky laccha paratha for quick meals"},
    {"sku": "ZAF-001", "name": "Zafrani Chai (100g)", "category": "Beverages", "price": 2200.0, "stock": 15, "unit": "box", "description": "Premium saffron-infused green tea blend"},
    {"sku": "SAL-001", "name": "Salwar Kameez (Women's)", "category": "Clothing", "price": 3500.0, "stock": 28, "unit": "set", "description": "Embroidered lawn salwar kameez for ladies"},
    {"sku": "MIX-001", "name": "Desi Ghee (1kg)", "category": "Groceries", "price": 2800.0, "stock": 5, "unit": "tin", "description": "Pure buffalo desi ghee from dairy farms"},
]

INITIAL_CUSTOMERS = [
    {"name": "Ahmed Khan", "email": "ahmed.khan@gmail.com", "phone": "0300-1234567", "city": "Lahore", "address": "House 12, Block C, DHA Phase 5, Lahore", "total_orders": 8, "total_spent": 24500.0},
    {"name": "Fatima Zahra", "email": "fatima.zahra@hotmail.com", "phone": "0321-9876543", "city": "Karachi", "address": "Flat 4A, Clifton Block 2, Karachi", "total_orders": 5, "total_spent": 15800.0},
    {"name": "Bilal Hussain", "email": "bilal.hussain@yahoo.com", "phone": "0333-5551234", "city": "Islamabad", "address": "Street 7, F-8/3, Islamabad", "total_orders": 3, "total_spent": 9200.0},
    {"name": "Sara Malik", "email": "sara.malik@gmail.com", "phone": "0345-7654321", "city": "Faisalabad", "address": "Mohallah Rashidabad, Faisalabad", "total_orders": 6, "total_spent": 18300.0},
    {"name": "Usman Ali", "email": "usman.ali@gmail.com", "phone": "0311-2223333", "city": "Rawalpindi", "address": "Raja Bazaar, Rawalpindi", "total_orders": 2, "total_spent": 5600.0},
]

INITIAL_ORDERS = [
    {
        "order_id": "ORD-1001",
        "customer_name": "Ahmed Khan",
        "customer_phone": "0300-1234567",
        "customer_city": "Lahore",
        "status": "Delivered",
        "total": 4700.0,
        "payment_method": "EasyPaisa",
        "notes": "",
        "items": [
            {"sku": "BAS-001", "name": "Basmati Rice (5kg)", "quantity": 2, "price": 1200.0},
            {"sku": "CHA-001", "name": "Chai Patti (500g)", "quantity": 2, "price": 450.0},
            {"sku": "MAN-001", "name": "Attar Mango (Dozen)", "quantity": 1, "price": 800.0},
        ],
    },
    {
        "order_id": "ORD-1002",
        "customer_name": "Fatima Zahra",
        "customer_phone": "0321-9876543",
        "customer_city": "Karachi",
        "status": "Processing",
        "total": 5300.0,
        "payment_method": "JazzCash",
        "notes": "Please wrap the khussa in gift box",
        "items": [
            {"sku": "KHU-001", "name": "Khussa (Embroidered)", "quantity": 1, "price": 1800.0},
            {"sku": "SAL-001", "name": "Salwar Kameez (Women's)", "quantity": 1, "price": 3500.0},
        ],
    },
    {
        "order_id": "ORD-1003",
        "customer_name": "Bilal Hussain",
        "customer_phone": "0333-5551234",
        "customer_city": "Islamabad",
        "status": "Shipped",
        "total": 6400.0,
        "payment_method": "Bank Transfer",
        "notes": "",
        "items": [
            {"sku": "AJW-001", "name": "Ajwa Khajoor (1kg)", "quantity": 2, "price": 3200.0},
        ],
    },
    {
        "order_id": "ORD-1004",
        "customer_name": "Sara Malik",
        "customer_phone": "0345-7654321",
        "customer_city": "Faisalabad",
        "status": "Processing",
        "total": 3250.0,
        "payment_method": "Cash on Delivery",
        "notes": "",
        "items": [
            {"sku": "KUR-001", "name": "Kurta Shalwar (Men's)", "quantity": 1, "price": 2500.0},
            {"sku": "LAC-001", "name": "Laccha Paratha (10pc)", "quantity": 2, "price": 350.0},
        ],
    },
    {
        "order_id": "ORD-1005",
        "customer_name": "Usman Ali",
        "customer_phone": "0311-2223333",
        "customer_city": "Rawalpindi",
        "status": "Delivered",
        "total": 2800.0,
        "payment_method": "Cash on Delivery",
        "notes": "",
        "items": [
            {"sku": "MIX-001", "name": "Desi Ghee (1kg)", "quantity": 1, "price": 2800.0},
        ],
    },
]


# ---------------------------------------------------------------------------
# Seeder Function
# ---------------------------------------------------------------------------

def init_db():
    """Creates all tables and seeds data if the DB is empty."""
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # Only seed if products table is empty
        existing = db.query(ProductDB).count()
        if existing > 0:
            print(f"[DB] Database already has {existing} products — skipping seed.")
            return

        print("[DB] Seeding initial ShopMate data...")

        # Insert products
        products_map = {}
        for p_data in INITIAL_PRODUCTS:
            p = ProductDB(**p_data)
            db.add(p)
            db.flush()  # Get ID
            products_map[p.sku] = p

        # Insert customers
        customers_map = {}
        for c_data in INITIAL_CUSTOMERS:
            c = CustomerDB(**c_data)
            db.add(c)
            db.flush()
            customers_map[c.phone.replace("-", "").replace(" ", "")] = c

        # Insert orders with items
        base_time = datetime.utcnow() - timedelta(days=6)
        for i, o_data in enumerate(INITIAL_ORDERS):
            items_data = o_data.pop("items")
            order = OrderDB(
                **o_data,
                created_at=base_time + timedelta(days=i),
            )
            db.add(order)
            db.flush()

            for item_data in items_data:
                prod = products_map.get(item_data["sku"])
                item = OrderItemDB(
                    order_id=order.id,
                    product_id=prod.id if prod else None,
                    **item_data,
                )
                db.add(item)

        db.commit()
        print("[DB] ✅ Seed complete — products, customers, and orders loaded.")

    except Exception as e:
        db.rollback()
        print(f"[DB] ⚠️  Seed error: {e}")
    finally:
        db.close()

