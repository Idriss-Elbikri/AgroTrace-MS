import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

TOPIC_MAP = {
    "temperature": "capteurs.temperature",
    "humidite": "capteurs.humidite",
    "luminosite": "capteurs.luminosite",
    "meteo": "meteo.raw",
}

VALUE_BOUNDS = {
    "temperature": (-50.0, 80.0),
    "humidite": (0.0, 100.0),
    "luminosite": (0.0, 200000.0),
}
