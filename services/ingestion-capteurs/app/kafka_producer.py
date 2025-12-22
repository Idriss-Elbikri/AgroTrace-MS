import json
from aiokafka import AIOKafkaProducer
from .config import KAFKA_BOOTSTRAP_SERVERS

producer = None

async def get_producer():
    global producer
    if producer is None:
        producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await producer.start()
    return producer

async def send_to_kafka(topic: str, message: dict):
    p = await get_producer()
    await p.send_and_wait(topic, message)
