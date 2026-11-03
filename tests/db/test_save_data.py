from app.service.save_data import save_csv


async def test_sava_data():
    await save_csv("review_chart_data")
    await save_csv("industry_chart_data")
