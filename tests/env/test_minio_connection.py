import logging

from app.config import minio_client

logger = logging.getLogger(__name__)


async def test_minio_connection():
    """
    SILO连接测试
    """
    try:
        buckets = minio_client.list_buckets()
        logger.info(f"\033[36m✅ SILO连通成功，共{len(buckets)}个bucket\033[0m")
    except Exception as e:
        logger.error(f"\033[31m❌ SILO连接失败: {e}\033[0m")
        raise
