from fastapi import FastAPI, HTTPException
from .schemas import SensorData
from .kafka_producer import send_to_kafka
from .config import TOPIC_MAP
import os
import asyncpg

app = FastAPI(title="IngestionCapteurs API")

DB_HOST = os.getenv("DB_HOST", "timescaledb")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "123456")
DB_NAME = os.getenv("DB_NAME", "sensors")

async def get_db_connection():
    return await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

@app.post("/ingest")
async def ingest_data(payload: SensorData):

    # Validate topic
    if payload.type not in TOPIC_MAP:
        raise HTTPException(status_code=400, detail="Unknown sensor type")

    topic = TOPIC_MAP[payload.type]

    message = payload.dict()
    message["timestamp"] = payload.timestamp.isoformat()

    # Send to Kafka
    await send_to_kafka(topic, message)

    return {"status": "ok", "topic": topic}

@app.get("/ingested_types")
async def get_ingested_types():
    return {"types": list(TOPIC_MAP.keys())}

@app.get("/data")
async def get_all_data(limit: int = 100, sensor_type: str | None = None, sensor_id: str | None = None):
    """Récupérer les données depuis TimescaleDB avec filtres optionnels"""
    conn = await get_db_connection()
    try:
        query = "SELECT * FROM sensor_readings WHERE 1=1"
        params = []
        
        if sensor_type:
            params.append(sensor_type)
            query += f" AND sensor_type = ${len(params)}"
        
        if sensor_id:
            params.append(sensor_id)
            query += f" AND sensor_id = ${len(params)}"
        
        query += f" ORDER BY observed_at DESC LIMIT {limit}"
        
        rows = await conn.fetch(query, *params)
        
        return {
            "count": len(rows),
            "data": [dict(row) for row in rows]
        }
    finally:
        await conn.close()

@app.get("/data/latest")
async def get_latest_readings():
    """Récupérer les dernières lectures par capteur"""
    conn = await get_db_connection()
    try:
        query = """
            SELECT DISTINCT ON (sensor_id) 
                sensor_id, sensor_type, value, observed_at, metadata
            FROM sensor_readings
            ORDER BY sensor_id, observed_at DESC
        """
        rows = await conn.fetch(query)
        
        return {
            "count": len(rows),
            "sensors": [dict(row) for row in rows]
        }
    finally:
        await conn.close()

@app.get("/data/stats")
async def get_stats():
    """Statistiques globales"""
    conn = await get_db_connection()
    try:
        stats_query = """
            SELECT 
                sensor_type,
                COUNT(*) as total_readings,
                AVG(value) as avg_value,
                MIN(value) as min_value,
                MAX(value) as max_value,
                MAX(observed_at) as last_reading
            FROM sensor_readings
            GROUP BY sensor_type
        """
        rows = await conn.fetch(stats_query)
        
        return {
            "stats": [dict(row) for row in rows]
        }
    finally:
        await conn.close()

