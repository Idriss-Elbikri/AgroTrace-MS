import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- CONFIGURATION DYNAMIQUE ---
# Explication : 
# 1. os.getenv("DATABASE_URL") cherche une configuration venant de Docker Compose.
# 2. Si elle n'existe pas (ex: test local dans VS Code), on utilise le lien par défaut vers localhost:5434.
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:password@localhost:5434/agrotrace_db"
)

# Création du moteur
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles
Base = declarative_base()

# Dépendance pour récupérer la DB dans les routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()