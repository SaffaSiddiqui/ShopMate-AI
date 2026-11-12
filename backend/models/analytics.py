from pydantic import BaseModel
from typing import List, Optional


class DailySales(BaseModel):
    day: str
    sales: float
    orders: int


class PeakDay(BaseModel):
    day: str
    sales: float
    orders: int


class TopProduct(BaseModel):
    name: str
    sku: str
    sold: int
    price: float
    revenue: float
    emoji: str
    color: str


class CategoryStat(BaseModel):
    category: str
    total_sales: float
    units_sold: int
    product_count: int


class AnalyticsOverviewResponse(BaseModel):
    gross_sales: float
    total_orders: int
    average_order_value: float
    period: str
    growth_rate: float
    peak_day: PeakDay
    sales_by_day: List[DailySales]
    top_products: List[TopProduct]
    categories: List[CategoryStat]

