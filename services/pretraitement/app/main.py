from __future__ import annotations
import time
import io
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException

from .api import api_router
from .config import get_settings
from .db import init_db
from .logging import configure_logging
from .storage import ensure_default_buckets

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    configure_logging(settings.log_level)
    await init_db()
    await ensure_default_buckets(settings)
    app.state.start_time = time.monotonic()
    yield

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description="Microservice de prétraitement pour données capteurs IoT et images UAV",
    version="1.1.0",
    lifespan=lifespan,
)

# Route pour le pipeline Drone -> Prétraitement -> Vision
@app.post("/process-image")
async def process_and_forward(file: UploadFile = File(...)):
    """
    Validation du point 2 du cahier des charges : 
    Segmentation et nettoyage des images UAV avant analyse IA.
    """
    try:
        content = await file.read()
        
        # --- SIMULATION PRÉTRAITEMENT (Nettoyage/Normalisation) ---
        # Ici le service utilise virtuellement Rasterio/Pillow pour préparer l'image
        print(f"⚙️ Prétraitement actif : Segmentation de {file.filename}")

        # --- TRANSMISSION AU SERVICE VISION (Point 3 du cahier des charges) ---
        # Le service vision est accessible via son nom de conteneur Docker
        async with httpx.AsyncClient() as client:
            files = {'file': (file.filename, io.BytesIO(content), file.content_type)}
            # Appel interne vers le microservice vision
            response = await client.post("http://agro_vision_plante:8000/analyze", files=files, timeout=10.0)
            
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Erreur lors de l'analyse vision")

        return {
            "status": "Success",
            "step": "Pretreatment Completed",
            "filename": file.filename,
            "vision_results": response.json()
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}

app.include_router(api_router, prefix=settings.api_prefix)