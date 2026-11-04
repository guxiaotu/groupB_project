import pytest_asyncio

from app.config import engine  # 替换为你实际的 SQLAlchemy AsyncEngine 对象


@pytest_asyncio.fixture(autouse=True)
async def dispose_db_engine():
    """每个测试用例执行完成后，自动销毁底层数据库连接池，防止挂起的 Task / Warning。"""
    yield
    await engine.dispose()
