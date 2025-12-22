from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, validator

from .config import TOPIC_MAP, VALUE_BOUNDS


class SensorData(BaseModel):
    sensor_id: str = Field(..., min_length=1, max_length=64)
    type: str
    value: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None

    @validator("sensor_id")
    def normalize_sensor_id(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("sensor_id cannot be empty")
        return cleaned

    @validator("type")
    def validate_type(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in TOPIC_MAP:
            raise ValueError(f"Unsupported sensor type '{value}'")
        return normalized

    @validator("value")
    def validate_value(cls, value: float, values: Dict[str, Any]) -> float:
        sensor_type = values.get("type")
        bounds = VALUE_BOUNDS.get(sensor_type) if sensor_type else None
        if bounds:
            low, high = bounds
            if not (low <= value <= high):
                raise ValueError(
                    f"Value {value} outside accepted range {bounds} for type '{sensor_type}'"
                )
        return value
