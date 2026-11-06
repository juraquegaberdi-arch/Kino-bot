"""Database ulanish va pool sozlamasi."""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.config import settings
from src.database.models import Base

engine_kwargs = {
    "echo": settings.DEBUG,
    "future": True,
}
if not settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs.update(pool_size=20, max_overflow=10)

engine = create_async_engine(settings.DATABASE_URL, **engine_kwargs)
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, future=True
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    await engine.dispose()
