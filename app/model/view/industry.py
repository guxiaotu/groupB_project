from pydantic import BaseModel


class Industry(BaseModel):
    """
    VO for Industry
    """

    class Summary(BaseModel):
        total_products: int
        total_monthly_sales: float
        total_monthly_revenue: float
        brand_count: int

    payload: dict[str, dict]
    summary: Summary
