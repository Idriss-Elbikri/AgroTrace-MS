from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import SensorSeriesNormalized


async def perform_cleaning(
    session: AsyncSession,
    job_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    readings = payload.get('readings') or []
    parcel_id = payload.get('parcel_id')

    normalized_count = 0
    dropped_count = 0

    for entry in readings:
        try:
            normalized = SensorSeriesNormalized(
                job_id=job_id,
                parcel_id=parcel_id or (entry.get('metadata', {}) or {}).get('parcel_id'),
                sensor_id=entry['sensor_id'],
                metric_type=entry['type'],
                timestamp=datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00')),
                value=float(entry['value']),
                quality_flag=(entry.get('metadata') or {}).get('quality_flag'),
                meta=entry.get('metadata'),
            )
            session.add(normalized)
            normalized_count += 1
        except Exception:
            dropped_count += 1

    await session.flush()
    return {
        'normalized_count': normalized_count,
        'dropped_count': dropped_count,
        'parcel_id': parcel_id,
    }


async def fetch_latest_series(
    session: AsyncSession,
    parcel_id: str,
    limit: int,
) -> list[dict[str, Any]]:
    stmt = (
        select(SensorSeriesNormalized)
        .where(SensorSeriesNormalized.parcel_id == parcel_id)
        .order_by(SensorSeriesNormalized.timestamp.desc())
        .limit(limit)
    )
    result = await session.execute(stmt)
    rows = result.scalars().all()
    return [
        {
            'sensor_id': row.sensor_id,
            'metric_type': row.metric_type,
            'timestamp': row.timestamp.isoformat(),
            'value': row.value,
            'quality_flag': row.quality_flag,
            'metadata': row.meta,
        }
        for row in rows
    ]
