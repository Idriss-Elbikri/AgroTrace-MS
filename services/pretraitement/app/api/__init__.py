from fastapi import APIRouter

from . import imagery, jobs, sensors

api_router = APIRouter()
api_router.include_router(sensors.router)
api_router.include_router(imagery.router)
api_router.include_router(jobs.router)
