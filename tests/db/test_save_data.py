from app.service import save_csv


async def test_sava_data():
    await save_csv(table_name="review_chart_data")
    await save_csv(table_name="industry_chart_data")
