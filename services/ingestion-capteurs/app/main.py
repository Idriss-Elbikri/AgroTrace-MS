from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import asyncio
import json
import os
import logging
from aiokafka import AIOKafkaProducer
from .schemas import SensorData
from .config import TOPIC_MAP

# --- LOGS ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IngestionAPI")

# --- CONFIG ---
KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
producer = None

# --- DEMARRAGE ROBUSTE ---
async def start_kafka():
    global producer
    logger.info(f"🔌 Connexion Kafka sur {KAFKA_SERVER}...")
    temp_producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    for i in range(15):
        try:
            await temp_producer.start()
            producer = temp_producer
            logger.info("✅ Kafka Connecté !")
            return
        except Exception:
            logger.warning(f"⏳ Kafka non prêt (Essai {i+1})...")
            await asyncio.sleep(2)
    logger.error("❌ Kafka inaccessible.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(start_kafka())
    yield
    if producer: await producer.stop()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def health():
    return {"status": "ok", "kafka": "connected" if producer else "waiting"}

@app.post("/")
async def ingest(payload: SensorData):
    if payload.type not in TOPIC_MAP:
        raise HTTPException(400, "Type inconnu")
    
    if not producer:
        return {"status": "error", "detail": "Kafka pas encore prêt"}

    try:
        msg = payload.dict()
        msg["timestamp"] = payload.timestamp.isoformat()
        await producer.send(TOPIC_MAP[payload.type], msg)
        return {"status": "envoyé"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}