import logging

from sqlalchemy import text

from app.config import engine

logger = logging.getLogger(__name__)


async def test_connection():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.fetchone()
            assert version is not None
            logger.info(f"\033[36m✅ 数据库连接成功！数据库版本: {version[0]}\033[0m")
    except Exception as e:
        logger.error(f"\033[31m❌ 连接失败: {e}\033[0m")
        raise
