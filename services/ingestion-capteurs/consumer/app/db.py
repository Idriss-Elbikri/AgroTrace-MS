import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.sql import text

from .config import DATABASE_URL
from .models import Base

logger = logging.getLogger(__name__)

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb"))
        await conn.execute(
            text(
                "SELECT create_hypertable('sensor_readings', 'observed_at', if_not_exists => TRUE)"
            )
        )
        await conn.execute(
            text(
                "SELECT create_hypertable('weather_readings', 'observed_at', if_not_exists => TRUE)"
            )
        )
    logger.info("TimescaleDB schema ready")


def get_session() -> AsyncSession:
    return SessionLocal()
