from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import JobStatusEnum, PreprocessJob


async def create_job(
    session: AsyncSession,
    job_type: str,
    payload: dict | None = None,
) -> PreprocessJob:
    job = PreprocessJob(job_type=job_type, payload=payload)
    session.add(job)
    await session.flush()
    return job


async def get_job(session: AsyncSession, job_id: str) -> PreprocessJob | None:
    result = await session.execute(select(PreprocessJob).where(PreprocessJob.id == job_id))
    return result.scalar_one_or_none()


async def list_jobs(session: AsyncSession, limit: int = 50, offset: int = 0) -> Sequence[PreprocessJob]:
    stmt = (
        select(PreprocessJob)
        .order_by(PreprocessJob.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_job_status(
    session: AsyncSession,
    job: PreprocessJob,
    status: JobStatusEnum,
    result_payload: dict | None = None,
    error_payload: dict | None = None,
) -> PreprocessJob:
    job.status = status.value
    job.result = result_payload
    job.error = error_payload
    await session.flush()
    return job