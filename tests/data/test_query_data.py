from app.model import IndustryChartData, ReviewChartData
from app.service import query_data


async def test_query_review_chart_data():
    """测试查询review_chart_data表"""
    print(await query_data(ReviewChartData))


async def test_query_industry_chart_data():
    """测试查询industry_chart_data表"""
    print(await query_data(IndustryChartData))
