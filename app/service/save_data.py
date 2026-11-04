import asyncio
import io
import re

import asyncpg
import polars as pl

from app.config import minio_client, settings


async def save_csv(table_name: str, bucket: str = "data"):
    # 1. 从 MinIO 拿对象
    response = minio_client.get_object(bucket, f"csv/{table_name}.csv")

    # 2. 在线程池中异步读取 CSV，避免阻塞 asyncio 事件循环
    df = await asyncio.to_thread(pl.read_csv, io.BytesIO(response.read()))

    # 3. 获取列名与行元组数据
    columns = df.columns
    records = list(df.iter_rows())

    # 4. 重新设置同步协议，清除（+异步协议）
    url = re.sub(r"\+[^:]*:", ":", settings.database_url)

    # 5. 使用 asyncpg 建立异步连接并执行 COPY 批量入库
    conn = await asyncpg.connect(url)
    try:
        await conn.copy_records_to_table(
            table_name=table_name, records=records, columns=columns
        )
    finally:
        await conn.close()
