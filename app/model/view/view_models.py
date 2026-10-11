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



class Review(BaseModel):
    """
       VO for Review
    """

    class Summary(BaseModel):
        negative_total: int
        positive_total: int
        motivation_total: int
        sample_negative: int
        sample_positive: int
        sample_motivation: int

    payload: dict[str, dict]
    summary: Summary
