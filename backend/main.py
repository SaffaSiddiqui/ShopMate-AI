from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.routes.health import router as health_router
from backend.routes.products import router as products_router
from backend.routes.orders import router as orders_router
from backend.routes.inventory import router as inventory_router
from backend.routes.customers import router as customers_router
from backend.routes.analytics import router as analytics_router
from backend.routes.agent import router as agent_router

app = FastAPI(
    title="ShopMate AI API",
    description="Intelligent E-commerce & Retail Management Backend for ShopMate AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration to allow local frontend development and production access
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:[0-9]+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom error handlers for clean and consistent error responses
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "message": exc.detail,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = " -> ".join(str(loc) for loc in err.get("loc", []))
        errors.append({
            "field": field,
            "message": err.get("msg", "Invalid input"),
            "type": err.get("type", "value_error"),
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "status_code": 422,
            "message": "Validation error in request payload or query parameters",
            "details": errors,
        },
    )


# Root welcome endpoint
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to ShopMate AI API",
        "version": "1.0.0",
        "status": "online",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
        },
        "endpoints": {
            "health": "/api/health",
            "products": "/api/products",
            "orders": "/api/orders",
            "inventory": "/api/inventory",
            "customers": "/api/customers",
            "analytics": "/api/analytics/overview",
            "agent": "/api/agent/chat",
        },
    }


# Register all feature routers
app.include_router(health_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(inventory_router)
app.include_router(customers_router)
app.include_router(analytics_router)
app.include_router(agent_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

