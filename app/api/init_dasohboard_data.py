from app.model.view import DashboardData
from app.view import get_industry, get_review


async def load_dashboard_data() -> DashboardData:
    return DashboardData(
        industry=await get_industry(),
        review=await get_review(),
    )
