from __future__ import annotations

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api import api_router
from .config import get_settings
from .db import init_db
from .logging import configure_logging
from .schemas import HealthResponse
from .storage import ensure_default_buckets


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    configure_logging(settings.log_level)
    await init_db()
    await ensure_default_buckets(settings)
    app.state.start_time = time.monotonic()
    yield


settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description="Microservice de prétraitement pour données capteurs IoT et images UAV",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {"name": "jobs", "description": "Gestion des jobs de prétraitement"},
    ],
    contact={
        "name": "AgroTrace Team",
        "email": "contact@agrotrace.com",
    },
    license_info={
        "name": "MIT",
    },
)
app.include_router(api_router, prefix=settings.api_prefix)
