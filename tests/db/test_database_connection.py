from sqlalchemy import text

from app.config.config import engine


async def test_connection():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.fetchone()
            assert version is not None
            print(f"✅ 数据库连接成功！数据库版本: {version[0]}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        raise
