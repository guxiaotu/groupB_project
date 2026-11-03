import asyncio
import io

import asyncpg
import polars as pl
from minio import Minio

client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="fastapicloud",
    secure=False,
)

bucket = "data"


async def save_csv(table):
    """按 chart_type 分组，输出可直接喂给 ECharts 的 JSON 结构"""

    # 1. 从 MinIO 拿对象
    response = client.get_object(bucket, f"csv/{table}.csv")

    # 2. 在线程池中异步读取 CSV，避免阻塞 asyncio 事件循环
    df = await asyncio.to_thread(pl.read_csv, io.BytesIO(response.read()))

    # 3. 获取列名与行元组数据
    columns = df.columns
    records = list(df.iter_rows())

    # 4. 使用 asyncpg 建立异步连接并执行 COPY 批量入库
    conn = await asyncpg.connect("postgres://postgres:fastapicloud@localhost:5432/test")
    try:
        await conn.copy_records_to_table(
            table_name=table, records=records, columns=columns
        )
    finally:
        await conn.close()
