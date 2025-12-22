from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    pending = 'pending'
    processing = 'processing'
    completed = 'completed'
    failed = 'failed'


class SensorPosition(BaseModel):
    lat: float
    lng: float
    alt: Optional[float] = None


class SensorMetadata(BaseModel):
    unit: Optional[str] = None
    parcel_id: Optional[str] = None
    source: Optional[str] = None
    position: Optional[SensorPosition] = None
    quality_flag: Optional[str] = None
    extra: Dict[str, Any] | None = None


class SensorReading(BaseModel):
    sensor_id: str
    type: str
    value: float
    timestamp: datetime
    metadata: Optional[SensorMetadata] = None


class SensorCleaningRequest(BaseModel):
    readings: List[SensorReading] | None = None
    parcel_id: Optional[str] = None
    from_timestamp: Optional[datetime] = Field(default=None, alias='fromTimestamp')
    to_timestamp: Optional[datetime] = Field(default=None, alias='toTimestamp')
    strategy: str = 'default'


class SensorCleaningResult(BaseModel):
    normalized_count: int
    dropped_count: int
    parcel_id: Optional[str] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)


class MinioObjectRef(BaseModel):
    bucket: str
    object_name: str


class ImageTilingRequest(BaseModel):
    source: MinioObjectRef
    parcel_id: Optional[str] = None
    mission_id: Optional[str] = None
    tile_size: int = 512
    overlap: int = 0
    target_crs: str = 'EPSG:4326'


class JobCreateResponse(BaseModel):
    job_id: str = Field(alias='jobId')
    status: JobStatus
    type: str


class JobDetail(JobCreateResponse):
    created_at: datetime = Field(alias='createdAt')
    updated_at: datetime = Field(alias='updatedAt')
    payload: Dict[str, Any] | None = None
    result: Dict[str, Any] | None = None
    error: Dict[str, Any] | None = None


class JobListResponse(BaseModel):
    items: List[JobDetail]
    total: int


class HealthResponse(BaseModel):
    status: str
    uptime_seconds: float
