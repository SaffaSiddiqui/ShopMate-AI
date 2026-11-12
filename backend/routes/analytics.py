from typing import List, Annotated
from fastapi import APIRouter, Query
from backend.models.analytics import (
    AnalyticsOverviewResponse,
    DailySales,
    TopProduct,
    CategoryStat,
)
from backend.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/analytics", tags=["Sales Analytics"])


@router.get("/overview", response_model=AnalyticsOverviewResponse)
def get_analytics_overview(
    period: Annotated[str, Query(description="Time period ('7 days' or '30 days')")] = "7 days",
):
    """Retrieve full sales analytics overview, metrics, and trends."""
    return AnalyticsService.get_overview(period=period)


@router.get("/sales", response_model=List[DailySales])
def get_sales_trend(
    period: Annotated[str, Query(description="Time period ('7 days' or '30 days')")] = "7 days",
):
    """Retrieve day-by-day sales and order volume."""
    return AnalyticsService.get_sales_data(period=period)


@router.get("/top-products", response_model=List[TopProduct])
def get_top_products(
    limit: Annotated[int, Query(ge=1, le=50, description="Number of top products to return")] = 5,
):
    """Retrieve highest-selling products by units sold."""
    return AnalyticsService.get_top_products(limit=limit)


@router.get("/categories", response_model=List[CategoryStat])
def get_category_distribution():
    """Retrieve sales and product distribution across categories."""
    return AnalyticsService.get_category_stats()
