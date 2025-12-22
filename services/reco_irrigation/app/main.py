from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
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

@app.post("/recommendations/", response_model=schemas.RecommendationResponse)
def create_recommendation(
    reco: schemas.RecommendationCreate, 
    db: Session = Depends(get_db)
):
    """
    Créer une nouvelle recommandation d'irrigation (Plan d'action).
    """
    # On transforme le schéma Pydantic en modèle SQLAlchemy
    db_reco = models.Recommendation(
        zone_id=reco.zone_id,
        water_amount=reco.water_amount,
        frequency=reco.frequency,
        execution_date=reco.execution_date
    )
    
    # On sauvegarde dans la base de données
    db.add(db_reco)
    db.commit()
    db.refresh(db_reco) # On récupère l'ID généré automatiquement
    
    return db_reco

@app.get("/recommendations/", response_model=List[schemas.RecommendationResponse])
def read_recommendations(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Récupérer l'historique des recommandations pour le Dashboard.
    """
    recommendations = db.query(models.Recommendation).offset(skip).limit(limit).all()
    return recommendations