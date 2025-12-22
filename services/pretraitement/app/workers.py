from __future__ import annotations

import asyncio
import logging
from typing import Any, Awaitable, Callable

from .db import AsyncSessionFactory
from .models import JobStatusEnum
from .services import imagery as imagery_service
from .services import jobs as job_service
from .services import sensors as sensors_service
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

HandlerType = Callable[[AsyncSession, str, dict[str, Any]], Awaitable[dict[str, Any]]]


async def _execute_job(job_id: str, handler: HandlerType, payload: dict[str, Any]) -> None:
    async with AsyncSessionFactory() as session:
        job = await job_service.get_job(session, job_id)
        if job is None:
            logger.warning("Job %s not found", job_id)
            return

        await job_service.update_job_status(session, job, JobStatusEnum.processing)
        await session.commit()

        try:
            result_payload = await handler(session, job_id, payload)
            await job_service.update_job_status(
                session,
                job,
                JobStatusEnum.completed,
                result_payload=result_payload,
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception("Job %s failed", job_id)
            await job_service.update_job_status(
                session,
                job,
                JobStatusEnum.failed,
                error_payload={'message': str(exc)},
            )
        finally:
            await session.commit()


def _schedule(job_id: str, handler: HandlerType, payload: dict[str, Any]) -> None:
    try:
        asyncio.create_task(_execute_job(job_id, handler, payload))
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.create_task(_execute_job(job_id, handler, payload))


def schedule_sensor_cleaning(job_id: str, payload: dict[str, Any]) -> None:
    _schedule(job_id, sensors_service.perform_cleaning, payload)


def schedule_imagery_tiling(job_id: str, payload: dict[str, Any]) -> None:
    _schedule(job_id, imagery_service.perform_tiling, payload)
