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

        return {
            "inventory": inventory_summary,
            "analytics": analytics,
            "processing_orders": processing_orders,
            "low_stock_products": low_stock_products,
            "top_products": top_products,
            "customer_count": len(store.customers),
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

**Operations:**
  - Pending (Processing) orders: {len(data['processing_orders'])}
  - Total customers: {data['customer_count']}

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
        try:
            full_prompt = f"{system_prompt}\n\n## Owner's Question\n{user_query}"
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=full_prompt,
            )
            return response.text.strip()
        except Exception as e:
            print(f"[Gemini] API error: {e}")
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
            reply = (
                f"You currently track {count} key active customers in your directory. "
                "Returning customers account for approximately 68% of visits. "
                "Reach out via WhatsApp or offer a loyalty voucher on their next purchase."
            )
            return reply, "customer_insight"

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

        if gemini_reply:
            return AgentQueryResponse(
                reply=gemini_reply,
                intent="gemini_ai",
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
