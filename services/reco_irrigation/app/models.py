from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    # Identifiant unique de la recommandation
    id = Column(Integer, primary_key=True, index=True)
    
    # Identifiant de la zone concernée (ex: "Parcelle-A")
    zone_id = Column(String, index=True)
    
    # Les 3 données demandées dans le cahier des charges :
    # 1. Dose (Quantité d'eau)
    water_amount = Column(Float) 
    # 2. Fréquence
    frequency = Column(String)
    # 3. Calendrier (Date d'application)
    execution_date = Column(String)

    # Date à laquelle on a généré ce conseil (pour l'historique)
    created_at = Column(DateTime(timezone=True), server_default=func.now())