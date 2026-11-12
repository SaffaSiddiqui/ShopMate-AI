import os
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
_test_database = tempfile.NamedTemporaryFile(prefix="shopmate-tests-", suffix=".db", delete=False)
_test_database.close()
os.environ["SHOPMATE_DATABASE_PATH"] = _test_database.name

from fastapi import HTTPException
from pydantic import ValidationError

from backend.services.store_data import store
from backend.models.product import ProductCreate, ProductUpdate
from backend.models.order import OrderCreate, OrderStatus, OrderStatusUpdate
from backend.models.inventory import RestockRequest
from backend.models.customer import CustomerCreate, CustomerUpdate
from backend.models.agent import AgentQueryRequest

from backend.routes.health import health_check
from backend.routes.products import (
    get_products,
    get_product,
    create_product,
    update_product,
    delete_product,
)
from backend.routes.orders import (
    get_orders,
    get_order,
    create_order,
    update_order_status,
    delete_order,
)
from backend.routes.inventory import (
    get_inventory,
    get_low_stock,
    restock_product,
)
from backend.routes.customers import (
    get_customers,
    get_customer,
    create_customer,
    update_customer,
    delete_customer,
)
from backend.routes.analytics import (
    get_analytics_overview,
    get_sales_trend,
    get_top_products,
    get_category_distribution,
)
from backend.routes.agent import (
    chat_with_agent,
    get_recommendations,
)

passed = 0
failed = 0


def assert_true(cond, msg="Assertion failed"):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print(f"❌ [FAIL] {msg}", file=sys.stderr)


def run_tests():
    global passed, failed
    print("=" * 65)
    print("🚀 RUNNING COMPREHENSIVE SHOPMATE AI BACKEND TEST SUITE")
    print("=" * 65)

    # Reset store to clean state
    store.reset()

    # 1. HEALTH CHECK
    print("\n[1/6] Testing Health Check Endpoints...")
    health = health_check()
    assert_true(health["status"] == "ok", "Health status is not 'ok'")
    assert_true(health["service"] == "ShopMate AI Backend", "Health service name mismatch")
    assert_true("timestamp" in health, "Health missing timestamp")
    print("  ✓ Health check passed")

    # 2. PRODUCTS
    print("\n[2/6] Testing Products Endpoints & Validation...")
    products = get_products()
    assert_true(len(products) == 6, f"Expected 6 products initially, got {len(products)}")

    rice = get_products(search="Basmati")
    assert_true(len(rice) == 1 and rice[0]["sku"] == "GR-1024", "Product search failed")

    groceries = get_products(category="Grocery")
    assert_true(len(groceries) == 3, f"Expected 3 grocery products, got {len(groceries)}")

    low_stocks = get_products(low_stock=True)
    assert_true(all(p["stock"] < 10 for p in low_stocks), "Low stock filter failed")

    budget = get_products(max_price=2000.0)
    assert_true(all(p["price"] <= 2000.0 for p in budget), "Price range filter failed")

    single = get_product("GR-1024")
    assert_true(single["name"] == "Premium Basmati Rice", "Product name mismatch for GR-1024")

    try:
        get_product("DOES-NOT-EXIST")
        assert_true(False, "Expected 404 for non-existent SKU")
    except HTTPException as e:
        assert_true(e.status_code == 404, f"Expected 404 status code, got {e.status_code}")

    new_product_model = ProductCreate(
        name="Kashmiri Chai (Pink Tea)",
        category="Beverages",
        sku="BV-9000",
        price=1250.0,
        stock=35,
        sold=15,
        emoji="🌸",
        color="pink",
    )
    created = create_product(new_product_model)
    assert_true(created["sku"] == "BV-9000", "Created product SKU mismatch")
    assert_true(len(store.products) == 7, "Product count was not incremented")

    try:
        create_product(new_product_model)
        assert_true(False, "Duplicate SKU should have raised HTTPException 400")
    except HTTPException as e:
        assert_true(e.status_code == 400, f"Expected 400 for duplicate SKU, got {e.status_code}")

    try:
        ProductCreate(
            name="Bad Product",
            category="Beverages",
            sku="BV-BAD",
            price=-10.0,
            stock=5,
        )
        assert_true(False, "Negative price should have failed Pydantic validation")
    except ValidationError:
        assert_true(True, "Pydantic caught invalid negative price")

    try:
        ProductCreate(
            name="Bad Product 2",
            category="Beverages",
            sku="BV-BAD2",
            price=100.0,
            stock=-5,
        )
        assert_true(False, "Negative stock should have failed Pydantic validation")
    except ValidationError:
        assert_true(True, "Pydantic caught invalid negative stock")

    update_data = ProductUpdate(price=1400.0, stock=50)
    updated = update_product("BV-9000", update_data)
    assert_true(updated["price"] == 1400.0 and updated["stock"] == 50, "Update product failed")

    deleted = delete_product("BV-9000")
    assert_true(deleted["sku"] == "BV-9000", "Delete product returned wrong item")
    assert_true(len(store.products) == 6, "Product was not removed from store")
    print("  ✓ Products endpoints and validation passed")

    # 3. ORDERS
    print("\n[3/6] Testing Orders Endpoints...")
    all_orders = get_orders()
    assert_true(len(all_orders) == 5, f"Expected 5 orders initially, got {len(all_orders)}")

    order_single = get_order("SM-2084")
    assert_true(order_single["id"] == "#SM-2084", "Get order by ID mismatch")

    new_order_data = OrderCreate(
        customer="Zain Malik",
        item="Everyday Cotton Kurta",
        amount=3200.0,
        status=OrderStatus.PROCESSING,
    )
    created_order = create_order(new_order_data)
    assert_true(created_order["customer"] == "Zain Malik", "Created order customer mismatch")
    assert_true(created_order["initials"] == "ZM", "Generated customer initials incorrect")
    assert_true(created_order["id"].startswith("#SM-"), "Generated order ID format incorrect")
    order_id = created_order["id"]

    status_update = OrderStatusUpdate(status=OrderStatus.SHIPPED)
    updated_order = update_order_status(order_id, status_update)
    assert_true(updated_order["status"] == "Shipped", "Order status update failed")

    status_update_del = OrderStatusUpdate(status=OrderStatus.DELIVERED)
    updated_order_del = update_order_status(order_id, status_update_del)
    assert_true(updated_order_del["status"] == "Delivered", "Advance to Delivered failed")

    del_order = delete_order(order_id)
    assert_true(del_order["id"] == order_id, "Delete order failed")
    assert_true(len(store.orders) == 5, "Order count after deletion mismatch")

    product_stock = next(p["stock"] for p in store.products if p["sku"] == "CL-2042")
    stocked_order = create_order(OrderCreate(
        customer="Zain Malik",
        item="Everyday Cotton Kurta",
        amount=6400.0,
        product_sku="CL-2042",
        quantity=2,
    ))
    assert_true(
        next(p["stock"] for p in store.products if p["sku"] == "CL-2042") == product_stock - 2,
        "Creating a SKU-linked order did not reserve inventory",
    )
    cancelled_order = update_order_status(
        stocked_order["id"],
        OrderStatusUpdate(status=OrderStatus.CANCELLED),
    )
    assert_true(cancelled_order["status"] == "Cancelled", "Order cancellation failed")
    assert_true(
        next(p["stock"] for p in store.products if p["sku"] == "CL-2042") == product_stock,
        "Cancelling a SKU-linked order did not restore inventory",
    )
    update_order_status(
        stocked_order["id"],
        OrderStatusUpdate(status=OrderStatus.PROCESSING),
    )
    delete_order(stocked_order["id"])
    assert_true(
        next(p["stock"] for p in store.products if p["sku"] == "CL-2042") == product_stock,
        "Deleting a SKU-linked order did not restore inventory",
    )
    print("  ✓ Orders endpoints passed")

    # 4. INVENTORY
    print("\n[4/6] Testing Inventory Endpoints...")
    inventory = get_inventory()
    assert_true(inventory["total_units"] > 0, "Inventory total units <= 0")
    assert_true(inventory["total_products"] == 6, "Inventory total products mismatch")
    assert_true(len(inventory["items"]) == 6, "Inventory items list mismatch")

    low_stock_items = get_low_stock(threshold=10)
    assert_true(len(low_stock_items) == 2, f"Expected 2 low stock items, got {len(low_stock_items)}")
    assert_true(all(item["is_critical"] for item in low_stock_items), "Critical flag not set")

    restock_res = restock_product("BV-3018", RestockRequest(quantity=20))
    assert_true(restock_res["stock"] == 26, f"Expected 26 units after restock, got {restock_res['stock']}")
    assert_true(restock_res["stock_status"] == "In stock", "Restocked status label mismatch")

    try:
        RestockRequest(quantity=0)
        assert_true(False, "Restock quantity 0 should fail validation")
    except ValidationError:
        assert_true(True, "Pydantic caught quantity 0")

    print("  ✓ Inventory endpoints passed")

    # 5. CUSTOMERS
    print("\n[5/6] Testing Customers Endpoints...")
    customers = get_customers()
    assert_true(len(customers) == 5, f"Expected 5 customers, got {len(customers)}")

    cust = get_customer("+92 300 1234567")
    assert_true(cust["name"] == "Ayesha Khan", "Customer lookup by phone failed")

    new_cust = CustomerCreate(
        name="Hamza Tariq",
        phone="+92 345 7788990",
        city="Peshawar",
        orders=3,
        spent=9500.0,
    )
    created_cust = create_customer(new_cust)
    assert_true(created_cust["name"] == "Hamza Tariq", "Created customer name mismatch")
    assert_true(created_cust["initials"] == "HT", "Initials generation failed")

    try:
        create_customer(new_cust)
        assert_true(False, "Duplicate customer phone should raise 400")
    except HTTPException as e:
        assert_true(e.status_code == 400, "Duplicate customer didn't return 400")

    cust_update = CustomerUpdate(city="Islamabad", spent=12000.0)
    updated_cust = update_customer("+92 345 7788990", cust_update)
    assert_true(updated_cust["city"] == "Islamabad" and updated_cust["spent"] == 12000.0, "Update customer failed")

    delete_customer("+92 345 7788990")
    assert_true(len(store.customers) == 5, "Customer was not deleted")
    print("  ✓ Customers endpoints passed")

    # 6. SALES ANALYTICS & AI AGENT
    print("\n[6/6] Testing Sales Analytics & AI Agent Endpoints...")
    overview = get_analytics_overview("7 days")
    assert_true(overview["gross_sales"] > 0, "Gross sales <= 0")
    assert_true(overview["total_orders"] > 0, "Total orders <= 0")
    assert_true(overview["average_order_value"] > 0, "Average order value <= 0")
    assert_true(len(overview["sales_by_day"]) == 7, "Expected 7 daily sales records")

    overview_30 = get_analytics_overview("30 days")
    assert_true(len(overview_30["sales_by_day"]) == 4, "Expected 4 weekly sales records for 30 days")

    top = get_top_products(limit=3)
    assert_true(len(top) == 3, "Expected 3 top products")
    assert_true(top[0]["sold"] >= top[1]["sold"], "Top products not sorted by sold descending")

    cats = get_category_distribution()
    assert_true(len(cats) >= 3, "Expected at least 3 categories")

    agent_stock_res = chat_with_agent(AgentQueryRequest(message="Which products should I restock?"))
    assert_true(agent_stock_res.intent == "inventory_inquiry", "Agent inventory intent mismatch")
    assert_true("stock" in agent_stock_res.reply.lower(), "Agent reply didn't discuss stock")

    agent_sales_res = chat_with_agent(AgentQueryRequest(message="How were our sales this week?"))
    assert_true(agent_sales_res.intent == "sales_performance", "Agent sales intent mismatch")
    assert_true("rs." in agent_sales_res.reply.lower(), "Agent reply didn't include PKR currency figure")

    recommendations = get_recommendations()
    assert_true(len(recommendations) >= 3, "Expected at least 3 agent recommendations")
    assert_true(any(r.priority == "High" for r in recommendations), "Expected high priority alert")
    print("  ✓ Sales Analytics and AI Agent passed")

    print("\n" + "=" * 65)
    print(f"🎉 ALL CHECKS PASSED: {passed} assertions passed, {failed} failed!")
    print("=" * 65)
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    try:
        run_tests()
    finally:
        for path in (_test_database.name, _test_database.name + "-shm", _test_database.name + "-wal"):
            if os.path.exists(path):
                os.remove(path)
