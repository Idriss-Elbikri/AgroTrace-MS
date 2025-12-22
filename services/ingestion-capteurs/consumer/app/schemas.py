from datetime import datetime
from typing import Any, Dict

from dateutil import parser as date_parser
from pydantic import BaseModel, Field, validator


class SensorPayload(BaseModel):
    sensor_id: str
    type: str
    value: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] | None = None

    @validator("timestamp", pre=True)
    def parse_timestamp(cls, value):  # noqa: D401
        """Ensure timestamps are converted to datetime."""
        if isinstance(value, datetime):
            return value
        return date_parser.isoparse(value)


class WeatherPayload(BaseModel):
    station_id: str
    metric: str
    value: float | None = None
    units: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] | None = None

    @validator("timestamp", pre=True)
    def parse_timestamp(cls, value):  # noqa: D401
        """Ensure timestamps are converted to datetime."""
        if isinstance(value, datetime):
            return value
        return date_parser.isoparse(value)
