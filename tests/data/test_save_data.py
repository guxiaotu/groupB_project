from app.service import save_csv


async def test_sava_data():
    """
    测试保存数据
    """
    await save_csv(file_name="review_chart_data.csv")
    await save_csv(file_name="industry_chart_data.csv")
