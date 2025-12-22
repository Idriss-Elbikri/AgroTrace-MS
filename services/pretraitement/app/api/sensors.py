from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import JobCreateResponse, JobStatus, SensorCleaningRequest
from ..services import jobs as job_service
from ..services import sensors as sensors_service
from ..workers import schedule_sensor_cleaning
from .deps import get_db_session

router = APIRouter(prefix='/capteurs', tags=['capteurs'])


@router.post('/clean', status_code=status.HTTP_202_ACCEPTED, response_model=JobCreateResponse)
async def enqueue_sensor_cleaning(
    request: SensorCleaningRequest,
    session: AsyncSession = Depends(get_db_session),
) -> JobCreateResponse:
    payload = request.model_dump(by_alias=True, exclude_none=True)
    job = await job_service.create_job(session, 'sensor-cleaning', payload=payload)
    await session.commit()
    schedule_sensor_cleaning(job.id, payload)
    return JobCreateResponse(jobId=job.id, status=JobStatus(job.status), type=job.job_type)


@router.get('/parcelles/{parcel_id}/latest')
async def get_latest_series(
    parcel_id: str,
    limit: int = 200,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    series = await sensors_service.fetch_latest_series(session, parcel_id, limit)
    return {
        'parcel_id': parcel_id,
        'count': len(series),
        'series': series,
    }
