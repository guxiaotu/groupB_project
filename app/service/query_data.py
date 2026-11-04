from typing import TypeVar

from sqlmodel import SQLModel, select

from app.config.settings import get_session

# 定义泛型：继承自SQLModel的类
T = TypeVar("T", bound=SQLModel)


async def query_data[T: SQLModel](model: T) -> list[T]:
    async with get_session() as session:
        # 1. 获取模型中除了 'id' 以外的所有数据库列
        columns = [col for col in model.__table__.columns if col.name != "id"]

        # 2. 构造只包含这些列的 select 语句
        stmt = select(*columns)

        # 2. 使用 session.exec 执行语句
        result = await session.exec(stmt)
        raw_mappings = result.all()

        # 3. model_validate() 会对字典中的类型进行自动校验与转化，并转化为对应的SQLModel类实力
        return [model.model_validate(row) for row in raw_mappings]
