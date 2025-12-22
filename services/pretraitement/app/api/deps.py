from fastapi import Depends

from ..config import Settings, get_settings
from ..db import get_session


async def get_db_session():
    async for session in get_session():
        yield session


def get_app_settings() -> Settings:
    return get_settings()
