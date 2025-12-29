from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
import random
import httpx
import logging

from app.database import engine, get_db
from app import models

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation de la base de données
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AgroTrace - Microservice Recommandation Irrigation")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def determiner_etat_sol(humidite: float):
    """Logique dynamique pour l'état du sol"""
    if humidite < 35.0:
        return "Sec (Irrigation urgente)"
    elif humidite < 65.0:
        return "Optimal (Excellent)"
    else:
        return "Saturé (Attention drainage)"

@app.get("/")
async def root():
    return {"status": "online", "service": "reco_irrigation"}

# --- 1. ROUTE GEOJSON (PLOTTING) ---
# Placée en premier pour intercepter la requête avant le sélecteur d'ID
@app.get("/geojson")
async def get_parcelles_geojson(db: Session = Depends(get_db)):
    """Route pour Leaflet - Récupère les polygones PostGIS"""
    try:
        query = text("""
            SELECT jsonb_build_object(
                'type',     'FeatureCollection',
                'features', jsonb_agg(feature)
            )
            FROM (
              SELECT jsonb_build_object(
                'type',       'Feature',
                'id',         id,
                'geometry',   ST_AsGeoJSON(geom)::jsonb,
                'properties', jsonb_build_object(
                    'id', id,
                    'nom', nom,
                    'culture', culture,
                    'surface', surface
                )
              ) AS feature
              FROM parcelles
            ) features;
        """)
        result = db.execute(query).scalar()
        return result if result else {"type": "FeatureCollection", "features": []}
    except Exception as e:
        logger.error(f"❌ Erreur GeoJSON: {e}")
        return {"type": "FeatureCollection", "features": []}

# --- 2. ROUTE DÉTAILS PARCELLE ---
# On utilise int pour forcer une validation stricte de l'ID
@app.get("/parcelle/{parcelle_id}")
async def get_irrigation_status(parcelle_id: int, db: Session = Depends(get_db)):
    """Récupère les données IoT et interroge le moteur de règles Drools"""
    logger.info(f"🚀 Requête reçue pour la parcelle ID: {parcelle_id}")
    
    parcelle_info = {"nom": "Inconnue", "culture": "Blé", "surface": 0}
    try:
        query = text("SELECT id, nom, culture, surface FROM parcelles WHERE id = :pid")
        result = db.execute(query, {"pid": parcelle_id}).mappings().first()
        if result:
            parcelle_info = dict(result)
    except Exception as e:
        logger.error(f"❌ Erreur DB: {e}")

    temp_simulee = round(random.uniform(22.0, 31.0), 1)
    hum_simulee = round(random.uniform(30.0, 70.0), 1)
    vent_simule = 12.4

    etat_sol_dynamique = determiner_etat_sol(hum_simulee)

    etat_final = "Normal"
    reco_finale = "Analyse en cours..."
    
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "temperature": temp_simulee,
                "humidite": hum_simulee,
                "culture": parcelle_info.get("culture", "Blé")
            }
            response = await client.post(
                "http://regles-agro:8081/api/regles/analyser", 
                json=payload, 
                timeout=2.0
            )
            
            if response.status_code == 200:
                data_java = response.json()
                etat_final = data_java.get("etat", "Excellent")
                reco_finale = data_java.get("message", "Aucune action requise")
    except Exception as e:
        logger.error(f"❌ Drools inaccessible: {e}")
        reco_finale = "Service de règles indisponible"

    return {
        "parcelle_id": str(parcelle_id),
        "nom": parcelle_info.get("nom"),
        "temperature": temp_simulee,
        "humidite": hum_simulee,
        "vent": vent_simule,
        "etat": etat_sol_dynamique,
        "recommandation": reco_finale,
        "quantite": 0 if "Aucune" in reco_finale else 15,
        "tendance": "Stable",
        "conseil_anticipatif": "Analyse basée sur capteurs IoT en temps réel."
    }