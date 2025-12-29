from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import random
from datetime import datetime, timedelta
from app.database import get_db

app = FastAPI(title="PrevisionEau API (LSTM/Prophet)", version="1.1.0")

@app.get("/parcelle/{parcelle_id}")
def get_forecast(parcelle_id: str, db: Session = Depends(get_db)):
    """
    Simule une prédiction LSTM/Prophet sur 7 jours.
    Calcule le risque de stress hydrique futur.
    """
    # 1. Simulation d'une tendance de stress (0 à 100)
    # Dans un vrai système, on utiliserait Prophet ici sur les données de TimescaleDB
    hsi_futur = round(random.uniform(10.0, 85.0), 1)
    
    # 2. Détermination du jour critique
    jours_avant_stress = random.randint(1, 7)
    date_critique = (datetime.now() + timedelta(days=jours_avant_stress)).strftime("%d/%m/%Y")

    tendance = "Stable"
    if hsi_futur > 60:
        tendance = "Hausse du stress"
        message = f"Risque de stress hydrique élevé prévu pour le {date_critique}"
    elif hsi_futur < 30:
        tendance = "Favorable"
        message = "Conditions optimales prévues pour les 7 prochains jours"
    else:
        message = "Vigilance modérée sur l'évapotranspiration"

    return {
        "parcelle_id": parcelle_id,
        "forecast_period": "7 jours",
        "hsi_forecast": hsi_futur,
        "tendance": tendance,
        "date_critique": date_critique,
        "conseil_anticipatif": message,
        "modele_utilise": "LSTM / Prophet (Simulation)"
    }