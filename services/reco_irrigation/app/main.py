from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text  # <--- IMPORTANT : Pour les requêtes SQL brutes (PostGIS)
from typing import List

from app.database import engine, get_db
from app import models, schemas

# Création des tables si elles n'existent pas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RecoIrrigation API",
    description="Microservice de recommandation d'irrigation pour AgroTrace",
    version="1.0.0"
)

# --- ROUTES ---

# 1. Route pour la Carte (CELLE QUI MANQUAIT !)
@app.get("/geojson")
def get_parcelles_geojson(db: Session = Depends(get_db)):
    """
    Récupère les parcelles au format GeoJSON via PostGIS.
    """
    try:
        # Requête SQL optimisée pour PostGIS
        # Elle construit l'objet JSON directement dans la base de données
        sql_query = text("""
            SELECT json_build_object(
                'type', 'FeatureCollection',
                'features', coalesce(json_agg(
                    json_build_object(
                        'type', 'Feature',
                        'geometry', ST_AsGeoJSON(geom)::json,
                        'properties', json_build_object(
                            'id', id,
                            'nom', nom,
                            'culture', culture,
                            'surface_ha', surface_ha
                        )
                    )
                ), '[]'::json)
            )
            FROM parcelles;
        """)
        
        result = db.execute(sql_query).scalar()
        return result
        
    except Exception as e:
        print(f"Erreur GeoJSON: {e}")
        # En cas d'erreur, on renvoie une collection vide pour ne pas casser le front
        return {"type": "FeatureCollection", "features": []}


# 2. Routes existantes (Recommandations)
@app.post("/recommendations/", response_model=schemas.RecommendationResponse)
def create_recommendation(
    reco: schemas.RecommendationCreate, 
    db: Session = Depends(get_db)
):
    db_reco = models.Recommendation(
        zone_id=reco.zone_id,
        water_amount=reco.water_amount,
        frequency=reco.frequency,
        execution_date=reco.execution_date
    )
    db.add(db_reco)
    db.commit()
    db.refresh(db_reco)
    return db_reco

@app.get("/recommendations/", response_model=List[schemas.RecommendationResponse])
def read_recommendations(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    recommendations = db.query(models.Recommendation).offset(skip).limit(limit).all()
    return recommendations