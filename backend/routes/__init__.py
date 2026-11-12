from backend.routes.health import router as health_router
from backend.routes.products import router as products_router
from backend.routes.orders import router as orders_router
from backend.routes.inventory import router as inventory_router
from backend.routes.customers import router as customers_router
from backend.routes.analytics import router as analytics_router
from backend.routes.agent import router as agent_router

__all__ = [
    "health_router",
    "products_router",
    "orders_router",
    "inventory_router",
    "customers_router",
    "analytics_router",
    "agent_router",
]

