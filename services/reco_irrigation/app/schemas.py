from pydantic import BaseModel
from datetime import datetime

# 1. Schéma de base (données communes)
class RecommendationBase(BaseModel):
    zone_id: str
    water_amount: float  # Dose (en litres ou mm)
    frequency: str       # Fréquence (ex: "2 fois par jour")
    execution_date: str  # Calendrier (ex: "2025-02-01 08:00")

# 2. Schéma pour la CRÉATION (ce qu'on reçoit en entrée de l'API)
class RecommendationCreate(RecommendationBase):
    pass

# 3. Schéma pour la LECTURE (ce qu'on renvoie au Dashboard)
class RecommendationResponse(RecommendationBase):
    id: int
    created_at: datetime

    class Config:
        # Permet à Pydantic de lire les données venant de SQLAlchemy (ORM)
        from_attributes = True