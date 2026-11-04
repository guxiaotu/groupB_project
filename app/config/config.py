from minio import Minio
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    db_protocol: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    endpoint: str
    minio_port: int
    access_key: str
    secret_key: str

    @property
    def database_url(self) -> str:
        return (
            f"{self.db_protocol}://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()


# Strip 'http://' or 'https://' and attach the port
clean_host = settings.endpoint.replace("http://", "").replace("https://", "").strip("/")
minio_endpoint = f"{clean_host}:{settings.minio_port}"

minio_client = Minio(
    endpoint=minio_endpoint,
    access_key=settings.access_key,
    secret_key=settings.secret_key,
    secure=False,
)

# mysql 异步协议：mysql+aiomysql://
# postgresql 异步协议：postgresql+asyncpg，但是由于polars不支持异步，
# 所以使用postgresql同步协议，使用原生asyncpg完成异步写入数据
engine = create_async_engine(
    url=settings.database_url,
    echo=True,  # 调试打印SQL语句
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 连接词大池满后最多再创建20个连接池
    pool_pre_ping=True,  # 防止断连
)

# SessionLocal：会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,  # commit后不会自动过期（可以继续使用对象，比如访问对象属性）
    class_=AsyncSession,  # 指定为SQLModel封装后的AsyncSession，而不是原生SQLAlchemy
)


# FastAPI依赖项，使用SessionLocal
# 异步依赖项
async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
