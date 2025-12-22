from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from .config import get_settings

_settings = get_settings()

engine: AsyncEngine = create_async_engine(
    _settings.async_database_dsn,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()


async def init_db() -> None:
    from .models import Base

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)