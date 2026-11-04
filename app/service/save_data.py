import asyncio
import io
import logging
import re

import asyncpg
import polars as pl

from app.config import minio_client, settings

logger = logging.getLogger(__name__)


async def save_csv(table_name: str, bucket: str = "data", directory: str = "csv"):
    # 1. 从 MinIO 拿对象
    response = minio_client.get_object(bucket, f"{directory}/{table_name}.csv")

    # 2. 在线程池中异步读取 CSV，避免阻塞 asyncio 事件循环
    df = await asyncio.to_thread(pl.read_csv, io.BytesIO(response.read()))

    # 3. 获取列名与行元组数据
    columns = df.columns
    records = list(df.iter_rows())

    # 4. 重新设置同步协议，清除（+异步协议）
    url = re.sub(r"\+[^:]*:", ":", settings.database_url)

    # 5. 使用 asyncpg 建立异步连接并执行 COPY 批量入库
    logger.info(f"\033[36m📥 开始处理表 [{table_name}]，bucket={bucket}\033[0m")
    conn = await asyncpg.connect(url)

    try:
        logger.debug(f"\033[90m🔗 正在连接数据库...\033[0m")
        logger.debug(
            f"\033[90m📤 准备 COPY 入库，行数={len(records)}，列数={len(columns)}\033[0m"
        )

        result = await conn.copy_records_to_table(
            table_name=table_name, records=records, columns=columns
        )

        # COPY 返回值类似 "COPY 122"
        logger.info(
            f"\033[32m🎉 入库成功！表=[{table_name}]，写入行数={len(records)} COPY结果={result}\033[0m"
        )

    except Exception as e:
        logger.error(
            f"\033[31m💥 入库失败！表=[{table_name}]，错误类型={type(e).__name__}，错误={e}\033[0m",
            exc_info=True,
        )
        raise

    finally:
        await conn.close()
        logger.debug(f"\033[90m🔌 数据库连接已关闭，表=[{table_name}]\033[0m")
