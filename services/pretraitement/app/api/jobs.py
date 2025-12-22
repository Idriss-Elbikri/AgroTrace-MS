from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import PreprocessJob
from ..schemas import JobDetail, JobListResponse, JobStatus
from ..services import jobs as job_service
from .deps import get_db_session

router = APIRouter(prefix='/jobs', tags=['jobs'])


def _to_job_detail(job: PreprocessJob) -> JobDetail:
    return JobDetail(
        jobId=job.id,
        status=JobStatus(job.status),
        type=job.job_type,
        createdAt=job.created_at,
        updatedAt=job.updated_at,
        payload=job.payload,
        result=job.result,
        error=job.error,
    )


@router.get('/{job_id}', response_model=JobDetail)
async def get_job(job_id: str, session: AsyncSession = Depends(get_db_session)) -> JobDetail:
    job = await job_service.get_job(session, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail='Job not found')
    return _to_job_detail(job)


@router.get('/', response_model=JobListResponse)
async def list_jobs(
    limit: int = 20,
    offset: int = 0,
    session: AsyncSession = Depends(get_db_session),
) -> JobListResponse:
    jobs = await job_service.list_jobs(session, limit=limit, offset=offset)
    return JobListResponse(items=[_to_job_detail(job) for job in jobs], total=len(jobs))
