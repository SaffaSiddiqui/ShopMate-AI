"""
ShopMate AI Agent — Powered by Google Gemini AI.

Falls back to rule-based responses if the Gemini API key is not set
or if the API call fails (graceful degradation).
"""

import os
import re
from datetime import datetime
from typing import Dict, Any, List

from dotenv import load_dotenv

from backend.services.store_data import store
from backend.services.analytics_service import AnalyticsService
from backend.services.inventory_service import InventoryService
from backend.models.agent import AgentRecommendation, AgentQueryResponse

# Load .env from the backend directory
_ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(_ENV_PATH)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ---------------------------------------------------------------------------
# Gemini client setup (uses new google.genai SDK)
# ---------------------------------------------------------------------------
_gemini_client = None

def _get_gemini_client():
    """Lazily initialise the Gemini client once."""
    global _gemini_client
    if _gemini_client is not None:
        return _gemini_client
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return None
    try:
        import google.genai as genai
        _gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        return _gemini_client
    except Exception as e:
        print(f"[Gemini] Could not initialise client: {e}")
        return None


# ---------------------------------------------------------------------------
# Main Agent Class
# ---------------------------------------------------------------------------

class ShopMateAgent:
    """
    Intelligent shop advisor for Muhammad's Pakistani retail store.
    Uses Google Gemini AI for natural language responses.
    Falls back to rule-based logic when Gemini is unavailable.
    """

    # -----------------------------------------------------------------
    # Store Analysis Helper
    # -----------------------------------------------------------------

    @classmethod
    def analyze_store(cls) -> Dict[str, Any]:
        """Gathers a snapshot of the live store state."""
        inventory_summary = InventoryService.get_summary()
        analytics = AnalyticsService.get_overview("7 days")
        processing_orders = [o for o in store.orders if o.get("status") == "Processing"]
        low_stock_products = [p for p in store.products if p.get("stock", 0) < 10]
        top_products = AnalyticsService.get_top_products(3)
        top_customers = sorted(store.customers, key=lambda c: c.get("spent", 0), reverse=True)[:3]

        return {
            "inventory": inventory_summary,
            "analytics": analytics,
            "processing_orders": processing_orders,
            "low_stock_products": low_stock_products,
            "top_products": top_products,
            "customer_count": len(store.customers),
            "top_customers": top_customers,
            "total_orders_count": len(store.orders),
            "all_products": store.products,
        }

    @classmethod
    def _build_system_prompt(cls, data: Dict[str, Any]) -> str:
        """Builds a rich system prompt containing live store context."""
        low_stock_lines = "\n".join(
            f"  - {p['name']} (SKU: {p['sku']}) — only {p['stock']} units left"
            for p in data["low_stock_products"]
        ) or "  - None (all products well-stocked)"

        top_product_lines = "\n".join(
            f"  - {p['name']} (SKU: {p['sku']}) — {p['sold']} units sold"
            for p in data["top_products"]
        ) or "  - No sales data yet"

        top_customer_lines = "\n".join(
            f"  - {c['name']} ({c.get('city', 'Pakistan')}) — {c.get('orders', 0)} orders, Rs. {c.get('spent', 0):,.0f} spent"
            for c in data.get("top_customers", [])
        ) or "  - No customer data yet"

        analytics = data["analytics"]
        inv = data["inventory"]

        return f"""You are ShopMate AI — an intelligent, friendly business advisor for a Pakistani retail shop owned by Muhammad.

## Your Role
- Analyze the live store data provided below and give clear, actionable, concise advice in English.
- Keep responses short (2–4 sentences max unless detail is specifically asked for).
- Use Pakistani rupee (Rs. or PKR) for all amounts.
- Be warm and professional, like a smart business partner.

## Live Store Snapshot (as of right now)
**Inventory:**
  - Total products: {inv.get('total_products', 'N/A')}
  - Total stock value: Rs. {inv.get('total_value', 0):,.0f}
  - Low-stock items (< 10 units):
{low_stock_lines}

**Sales (Last 7 Days):**
  - Gross Revenue: Rs. {analytics.get('gross_sales', 0):,.0f}
  - Total Orders: {analytics.get('total_orders', 'N/A')}
  - Growth Rate: {analytics.get('growth_rate', 'N/A')}%
  - Peak Day: {analytics.get('peak_day', {}).get('day', 'N/A')} (Rs. {analytics.get('peak_day', {}).get('sales', 0):,.0f})

**Top Selling Products:**
{top_product_lines}

**Customers & Retention:**
  - Total registered customers: {data['customer_count']}
  - Top Customers by spend:
{top_customer_lines}

**Operations & Fulfilment:**
  - Total recorded orders: {data.get('total_orders_count', len(data['processing_orders']))}
  - Pending (Processing) orders: {len(data['processing_orders'])}

## Rules
- If asked about data not in the snapshot, say you don't have that information right now.
- Never make up numbers that aren't in the snapshot above.
- Respond ONLY to business-relevant questions about the store.
"""

    # -----------------------------------------------------------------
    # Gemini AI Query
    # -----------------------------------------------------------------

    @classmethod
    def _ask_gemini(cls, system_prompt: str, user_query: str) -> str | None:
        """Sends the query to Gemini and returns the response text, or None on failure."""
        client = _get_gemini_client()
        if client is None:
            return None

        # Prioritize fast, active flash-lite models with standard flash fallback
        candidate_models = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.8-flash"]
        full_prompt = f"{system_prompt}\n\n## Owner's Question\n{user_query}"

        for model_name in candidate_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=full_prompt,
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                print(f"[Gemini] Model '{model_name}' attempt failed: {e}")
                continue

        return None

    # -----------------------------------------------------------------
    # Rule-Based Fallback
    # -----------------------------------------------------------------

    @classmethod
    def _rule_based_response(cls, query: str, data: Dict[str, Any]) -> tuple[str, str]:
        """Returns (reply_text, intent_string) using regex matching."""
        text = query.strip().lower()

        # Low stock / inventory intent
        if re.search(r"stock|restock|inventory|shortage|supply", text):
            low_stocks = data["low_stock_products"]
            if low_stocks:
                items_str = ", ".join(
                    f"{p['name']} ({p['stock']} units, SKU: {p['sku']})" for p in low_stocks
                )
                reply = (
                    f"You have {len(low_stocks)} product(s) critically low on stock: {items_str}. "
                    "I recommend placing restock orders today to avoid stockouts."
                )
            else:
                reply = "Great news! All products are currently above the critical threshold of 10 units."
            return reply, "inventory_inquiry"

        # Sales / revenue intent
        if re.search(r"sales|revenue|performance|week|growth|earning|money", text):
            gross = data["analytics"]["gross_sales"]
            orders_count = data["analytics"]["total_orders"]
            peak = data["analytics"]["peak_day"]
            growth = data["analytics"]["growth_rate"]
            reply = (
                f"Your store achieved Rs. {gross:,.0f} in gross revenue across {orders_count} orders "
                f"over the past 7 days, reflecting a {growth}% growth. "
                f"Your strongest trading day was {peak['day']} with Rs. {peak['sales']:,.0f} in sales."
            )
            return reply, "sales_performance"

        # Customer / loyalty intent
        if re.search(r"customer|client|buyer|shopper|loyalty", text):
            count = data["customer_count"]
            top_cust = data.get("top_customers", [])
            top_info = f" Your top customer is {top_cust[0]['name']} (Rs. {top_cust[0]['spent']:,.0f} spent)." if top_cust else ""
            reply = (
                f"You currently track {count} key active customers in your directory.{top_info} "
                "Returning customers account for approximately 68% of visits. "
                "Reach out via WhatsApp or offer a loyalty voucher on their next purchase."
            )
            return reply, "customer_insight"

        # Orders / fulfillment intent
        if re.search(r"order|fulfillment|processing|shipped|shipping|pending", text):
            proc = len(data["processing_orders"])
            total_orders = data.get("total_orders_count", len(store.orders))
            reply = (
                f"You have {total_orders} total orders recorded in the system, with {proc} order(s) "
                "currently in 'Processing' status. Prioritize shipping pending orders to maintain quick delivery."
            )
            return reply, "order_inquiry"

        # Product / catalogue intent
        if re.search(r"product|item|catalog|catalogue|sku|seller|best seller", text):
            total_prods = data["inventory"].get("total_products", len(data.get("all_products", [])))
            top_prod = data["top_products"][0]["name"] if data["top_products"] else "top items"
            reply = (
                f"Your catalogue contains {total_prods} products. Your current best-seller is {top_prod}. "
                "Review slow-moving items and ensure top performers remain well-stocked."
            )
            return reply, "product_inquiry"

        # Default
        top_name = data["top_products"][0]["name"] if data["top_products"] else "top items"
        reply = (
            f"Here is your ShopMate AI briefing: Your top-performing item is {top_name}. "
            f"You have {len(data['low_stock_products'])} item(s) requiring restock, "
            f"and {len(data['processing_orders'])} pending order(s) awaiting shipment. "
            "Focus on restocking fast-moving inventory and fulfilling pending orders promptly."
        )
        return reply, "general_advice"

    # -----------------------------------------------------------------
    # Public Methods
    # -----------------------------------------------------------------

    @classmethod
    def answer_query(cls, query: str) -> AgentQueryResponse:
        """
        Main entry point for the AI agent chat endpoint.
        Tries Gemini first; falls back to rule-based if unavailable.
        """
        timestamp = datetime.now().isoformat()
        data = cls.analyze_store()

        # Try Gemini first
        system_prompt = cls._build_system_prompt(data)
        gemini_reply = cls._ask_gemini(system_prompt, query)

        # Detect domain intent for API compatibility
        _, detected_intent = cls._rule_based_response(query, data)

        if gemini_reply:
            return AgentQueryResponse(
                reply=gemini_reply,
                intent=detected_intent if detected_intent != "general_advice" else "gemini_ai",
                recommendations=cls.generate_recommendations()[:2],
                timestamp=timestamp,
            )

        # Fallback to rule-based
        reply, intent = cls._rule_based_response(query, data)
        low_stocks = data["low_stock_products"]
        recs = [
            AgentRecommendation(
                title=f"Restock {p['name']}",
                category="Inventory",
                priority="High",
                message=f"Stock is down to {p['stock']} units.",
                action_type="restock",
                target_sku=p["sku"],
            )
            for p in low_stocks
        ] if intent == "inventory_inquiry" else cls.generate_recommendations()[:2]

        return AgentQueryResponse(
            reply=reply,
            intent=intent,
            recommendations=recs,
            timestamp=timestamp,
        )

    @classmethod
    def generate_recommendations(cls) -> List[AgentRecommendation]:
        """Generates real-time actionable business recommendations (always rule-based)."""
        data = cls.analyze_store()
        recs: List[AgentRecommendation] = []

        # 1. Low stock alerts
        for p in data["low_stock_products"]:
            recs.append(
                AgentRecommendation(
                    title=f"Restock Alert: {p['name']}",
                    category="Inventory",
                    priority="High",
                    message=f"{p['name']} (SKU: {p['sku']}) has only {p['stock']} units left. Minimum recommended restock is 25 units.",
                    action_type="restock",
                    target_sku=p["sku"],
                )
            )

        # 2. Pending orders
        proc_count = len(data["processing_orders"])
        if proc_count > 0:
            recs.append(
                AgentRecommendation(
                    title="Orders Pending Fulfillment",
                    category="Operations",
                    priority="Medium",
                    message=f"You have {proc_count} order(s) marked as 'Processing'. Advance to 'Shipped' to maintain customer satisfaction.",
                    action_type="review_orders",
                )
            )

        # 3. Top product promotion
        if data["top_products"]:
            best = data["top_products"][0]
            recs.append(
                AgentRecommendation(
                    title=f"Leverage Top Performer: {best['name']}",
                    category="Marketing",
                    priority="Medium",
                    message=f"{best['name']} is your #1 seller with {best['sold']} units sold. Consider bundle discounts or highlighting it on your storefront.",
                    action_type="promote",
                    target_sku=best["sku"],
                )
            )

        # 4. Customer retention
        recs.append(
            AgentRecommendation(
                title="Customer Loyalty Engagement",
                category="Sales",
                priority="Low",
                message="Returning customers generate over 60% of recurring revenue. Send a promotional message to high-value shoppers this weekend.",
                action_type="message_customers",
            )
        )

        return recs

    # -----------------------------------------------------------------
    # Web Guide Assistant (Dedicated to Website Guidance Only)
    # -----------------------------------------------------------------

    @classmethod
    def answer_web_guide_query(cls, query: str) -> AgentQueryResponse:
        """
        Specialized guide assistant that ONLY answers questions about how to use,
        navigate, and operate the ShopMate AI website. Strictly rejects off-topic queries.
        """
        timestamp = datetime.now().isoformat()
        guide_prompt = """You are the official ShopMate Web Guide.
Your SOLE purpose is to help the user understand how to use, navigate, and operate this web application (ShopMate AI retail dashboard for Khan's General Store).

## Website Pages & How To Use Them:
1. **Overview (Dashboard)**:
   - 4 KPI cards: Total sales, Total orders, Total products, Low stock alerts.
   - Sales chart: Toggle between 7 days (daily PKR) and 30 days (weekly).
   - Recent orders: View recent purchases and click the green "Receipt" button to send WhatsApp invoices.
   - Smart restock & Top items: Highlights best-sellers and products needing restock.
   - "+ Add product" button at top-right to quickly add items.
2. **Products Page**:
   - Catalogue view showing all products, SKU numbers, categories, PKR prices, and stock counts.
   - "+ Add product" button opens modal form.
   - "Restock (+20)" button on every row immediately adds 20 units.
3. **Orders Page**:
   - Lists all orders. Click on any status badge (e.g. "Processing") to advance it.
   - "+ Create order" button at top-right to place new orders.
   - Green "Receipt" button opens WhatsApp with a ready-to-send customer bill.
4. **Inventory Page**:
   - Visual stock health tracking, units count, and critical alerts (< 15 units).
   - "Restock (+20)" button to restock any item.
   - "Print report" button triggers printable page view.
5. **Customers Page**:
   - Customer directory with city, phone number, order count, and lifetime PKR spend.
6. **Analytics Page**:
   - Visual charts for 7-day and 30-day performance, average order value, growth rate, and category distribution.
7. **AI Assistant Page**:
   - Live business copilot powered by Google Gemini to analyze store sales, inventory, and customers.
8. **Navigation & Shortcuts**:
   - Left sidebar to switch pages (on mobile, tap the ☰ menu icon at top-left).
   - Search bar or keyboard shortcut Ctrl+K / Cmd+K to search products, orders, and customers.
   - Bottom-right Web Guide button (you) for help using the site.

## Strict Response Rules:
- Answer ONLY questions related to how to use, operate, or navigate this web application.
- If the user asks about anything unrelated to this website (such as general knowledge, sports, unrelated coding, trivia, recipes), politely decline and state: "I am specifically the ShopMate Web Guide. I can only guide you on how to use this website, navigate pages, manage products, fulfill orders, and track sales."
- Provide clear, step-by-step instructions (2-4 sentences or concise bullet points).
"""
        client = _get_gemini_client()
        if client:
            candidate_models = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.8-flash"]
            full_prompt = f"{guide_prompt}\n\n## User Question\n{query}"
            for model_name in candidate_models:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=full_prompt,
                    )
                    if response and response.text:
                        return AgentQueryResponse(
                            reply=response.text.strip(),
                            intent="web_guide",
                            recommendations=[],
                            timestamp=timestamp,
                        )
                except Exception as e:
                    print(f"[Gemini Guide] Attempt failed with {model_name}: {e}")
                    continue

        # Rule-based fallback for web guide
        reply = cls._rule_based_web_guide(query)
        return AgentQueryResponse(
            reply=reply,
            intent="web_guide",
            recommendations=[],
            timestamp=timestamp,
        )

    @classmethod
    def _rule_based_web_guide(cls, query: str) -> str:
        """Fallback rules strictly focused on explaining how to use the website."""
        text = query.strip().lower()

        if re.search(r"product|add item|new item|catalogue|price|sku", text):
            return (
                "To manage products, go to the **Products** page. Click the blue '+ Add product' button "
                "at the top-right to enter a name, category, PKR price, and stock. You can also click "
                "'Restock (+20)' on any product row to instantly add 20 units."
            )
        if re.search(r"order|receipt|whatsapp|fulfill|deliver|processing|invoice", text):
            return (
                "To manage customer orders, visit the **Orders** page. Click '+ Create order' to log a new purchase. "
                "Click on any order's status pill to advance it (Processing ➔ Shipped ➔ Delivered), or click the green "
                "'Receipt' button to automatically open WhatsApp with an invoice ready to send."
            )
        if re.search(r"stock|inventory|shortage|restock|low stock", text):
            return (
                "To track stock health, open the **Inventory** page. Any item below 10 units is flagged with a "
                "'Low stock' warning. Click 'Restock (+20)' next to any product to quickly replenish units. "
                "You can also click 'Print report' to get a printable overview."
            )
        if re.search(r"customer|client|phone|city|directory", text):
            return (
                "To view your customer list, navigate to the **Customers** page. Here you can see each customer's "
                "name, phone number, city, total order history, and total PKR expenditure."
            )
        if re.search(r"analytics|sale|revenue|growth|chart|trend", text):
            return (
                "To check revenue trends, head to the **Analytics** page. Use the timeframe dropdown to toggle between "
                "7 days (daily breakdown) and 30 days (weekly overview). You'll also find category distribution and top performers."
            )
        if re.search(r"ai|assistant|gemini|copilot|advice", text):
            return (
                "The **AI Assistant** in the sidebar is your intelligent retail advisor powered by Google Gemini. "
                "You can ask it business questions such as 'Which products should I restock?' or 'How were our sales this week?' "
                "and it will analyze your live store numbers in Pakistani Rupees."
            )
        if re.search(r"search|shortcut|find|filter|kbd", text):
            return (
                "You can search across products, orders, and customers anytime using the search bar in the top navigation, "
                "or by pressing **Ctrl + K** (or **⌘ + K**) on your keyboard."
            )
        if re.search(r"responsive|mobile|phone|tablet|menu", text):
            return (
                "ShopMate AI is 100% responsive on all mobile phones and tablets. Tap the menu icon (☰) at the top-left "
                "to open the sidebar navigation, and swipe horizontally on tables to view all columns."
            )
        if re.search(r"print|export|report", text):
            return (
                "You can print an inventory report by going to the **Inventory** page and clicking the 'Print report' button."
            )

        # Off-topic or generic query guard
        return (
            "I am specifically the **ShopMate Web Guide**. I am here to help you navigate and use this web application. "
            "Please ask me how to manage products, send WhatsApp receipts, track orders, restock inventory, or view sales charts!"
        )
