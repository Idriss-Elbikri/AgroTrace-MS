import logging
from typing import Optional

from .config import VALUE_BOUNDS
from .schemas import SensorPayload

logger = logging.getLogger(__name__)


def clean_payload(payload: SensorPayload) -> Optional[SensorPayload]:
    bounds = VALUE_BOUNDS.get(payload.type)
    if bounds:
        lower, upper = bounds
        if not (lower <= payload.value <= upper):
            logger.warning(
                "Dropping out-of-range reading", extra={
                    "sensor_id": payload.sensor_id,
                    "sensor_type": payload.type,
                    "value": payload.value,
                    "expected_range": bounds,
                }
            )
            return None

    return payload
