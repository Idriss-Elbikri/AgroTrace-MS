import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- CONFIGURATION DE LA CONNEXION ---
# Explication des paramètres :
# - admin:adminpassword -> Utilisateur et mot de passe définis dans docker-compose
# - agro_postgis -> Nom du conteneur Docker de la base de données
# - 5432 -> Port interne du réseau Docker
# - agro_business -> Nom de la base de données spatiale
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:adminpassword@agro_postgis:5432/agro_business"
)

# Création du moteur SQLAlchemy pour PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Configuration de la session (utilisée par FastAPI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles ORM
Base = declarative_base()

# Dépendance pour injecter la session de base de données dans les routes API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()