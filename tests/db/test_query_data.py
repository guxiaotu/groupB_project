from app.service import query_industry, query_review


async def test_query_review():
    """
    测试查询review_chart_data表
    """
    await query_review()


async def test_query_industry():
    """
    测试查询industry_chart_data表
    """
    await query_industry()
