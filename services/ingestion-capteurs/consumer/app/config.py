import os
from typing import List

DEFAULT_TOPICS = [
    "capteurs.temperature",
    "capteurs.humidite",
    "capteurs.luminosite",
    "meteo.raw",
]


def _split_topics(raw: str) -> List[str]:
    return [topic.strip() for topic in raw.split(",") if topic.strip()]


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP", "timescaledb-consumer")
KAFKA_TOPICS = _split_topics(os.getenv("KAFKA_TOPICS", ",".join(DEFAULT_TOPICS)))

DB_HOST = os.getenv("DB_HOST", "timescaledb")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "123456")
DB_NAME = os.getenv("DB_NAME", "sensors")

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

VALUE_BOUNDS = {
    "temperature": (-50.0, 80.0),
    "humidite": (0.0, 100.0),
    "luminosite": (0.0, 200000.0),
}
