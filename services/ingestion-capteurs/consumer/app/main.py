import asyncio
import json
import logging
from contextlib import asynccontextmanager

from aiokafka import AIOKafkaConsumer
from pydantic import ValidationError

from .config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_CONSUMER_GROUP,
    KAFKA_TOPICS,
    LOG_LEVEL,
)
from .db import get_session, init_db
from .models import SensorReading, WeatherReading
from .processing import clean_payload
from .schemas import SensorPayload, WeatherPayload

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("consumer")


@asynccontextmanager
async def session_scope():
    session = get_session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def handle_message(record, session):
    # Check if this is a weather station message
    if record.topic == "meteo.raw":
        await handle_weather_message(record, session)
    else:
        await handle_sensor_message(record, session)


async def handle_sensor_message(record, session):
    payload = SensorPayload(**record.value)
    cleaned = clean_payload(payload)
    if cleaned is None:
        return

    raw_payload = cleaned.dict()
    raw_payload["timestamp"] = cleaned.timestamp.isoformat()

    reading = SensorReading(
        sensor_id=cleaned.sensor_id,
        sensor_type=cleaned.type,
        value=cleaned.value,
        observed_at=cleaned.timestamp,
        extra_data=cleaned.metadata,
        raw_payload=raw_payload,
    )
    session.add(reading)


async def handle_weather_message(record, session):
    payload = WeatherPayload(**record.value)
    
    raw_payload = payload.dict()
    raw_payload["timestamp"] = payload.timestamp.isoformat()

    reading = WeatherReading(
        station_id=payload.station_id,
        metric=payload.metric,
        value=payload.value,
        units=payload.units,
        observed_at=payload.timestamp,
        extra_data=payload.metadata,
        raw_payload=raw_payload,
    )
    session.add(reading)


async def consume():
    await init_db()

    consumer = AIOKafkaConsumer(
        *KAFKA_TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_CONSUMER_GROUP,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        enable_auto_commit=False,
        auto_offset_reset="earliest",
    )

    await consumer.start()
    logger.info("Kafka consumer started", extra={"topics": KAFKA_TOPICS})

    try:
        async for message in consumer:
            try:
                async with session_scope() as session:
                    await handle_message(message, session)
                await consumer.commit()
            except ValidationError as exc:
                logger.error(f"Validation failed: {exc.errors()}, payload: {message.value}")
                await consumer.commit()  # Skip invalid messages
            except Exception:
                logger.exception("Failed to process message")
                # Don't commit - will retry on restart
    finally:
        await consumer.stop()
        logger.info("Kafka consumer stopped")


def main():
    asyncio.run(consume())


if __name__ == "__main__":
    main()
