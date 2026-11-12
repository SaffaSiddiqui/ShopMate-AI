from fastapi import APIRouter
from datetime import datetime
from backend.services.database import database

router = APIRouter(tags=["Health"])


@router.get("/health")
@router.get("/api/health")
def health_check():
    """Health check endpoint to verify backend status."""
    return {
        "status": "ok",
        "service": "ShopMate AI Backend",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "database": "SQLite connected" if database.path.is_file() else "SQLite unavailable",
    }
