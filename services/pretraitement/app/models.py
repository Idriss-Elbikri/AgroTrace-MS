from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, Integer, String, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class JobStatusEnum(str, Enum):
    pending = 'pending'
    processing = 'processing'
    completed = 'completed'
    failed = 'failed'


class PreprocessJob(Base):
    __tablename__ = 'preprocess_jobs'

    id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        default=lambda: f"job_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}",
    )
    job_type: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default=JobStatusEnum.pending.value)
    payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    result: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    error: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('NOW()'),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('NOW()'),
        onupdate=datetime.utcnow,
    )

    sensor_series: Mapped[list[SensorSeriesNormalized]] = relationship(back_populates='job')
    tiles: Mapped[list[UavTileMetadata]] = relationship(back_populates='job')


class SensorSeriesNormalized(Base):
    __tablename__ = 'sensor_series_norm'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_id: Mapped[str | None] = mapped_column(String(64), ForeignKey('preprocess_jobs.id'), index=True)
    parcel_id: Mapped[str | None] = mapped_column(String(64), index=True)
    sensor_id: Mapped[str] = mapped_column(String(64), index=True)
    metric_type: Mapped[str] = mapped_column(String(32), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    value: Mapped[float] = mapped_column(Float)
    quality_flag: Mapped[str | None] = mapped_column(String(16))
    meta: Mapped[dict | None] = mapped_column('metadata', JSONB)

    job: Mapped[PreprocessJob | None] = relationship(back_populates='sensor_series')


Index('ix_sensor_series_norm_parcel_metric_time', SensorSeriesNormalized.parcel_id, SensorSeriesNormalized.metric_type, SensorSeriesNormalized.timestamp.desc())


class UavTileMetadata(Base):
    __tablename__ = 'uav_tiles_meta'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[str | None] = mapped_column(String(64), ForeignKey('preprocess_jobs.id'), index=True)
    parcel_id: Mapped[str | None] = mapped_column(String(64), index=True)
    mission_id: Mapped[str | None] = mapped_column(String(64), index=True)
    tile_path: Mapped[str] = mapped_column(String(512), nullable=False)
    bounds: Mapped[dict | None] = mapped_column(JSONB)
    crs: Mapped[str | None] = mapped_column(String(32))
    resolution: Mapped[float | None] = mapped_column(Float)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    meta: Mapped[dict | None] = mapped_column('metadata', JSONB)

    job: Mapped[PreprocessJob | None] = relationship(back_populates='tiles')


Index('ix_uav_tiles_meta_parcel_generated', UavTileMetadata.parcel_id, UavTileMetadata.generated_at.desc())
Index('ix_uav_tiles_meta_mission', UavTileMetadata.mission_id)
