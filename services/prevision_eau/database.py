import os
import pandas as pd
from sqlalchemy import create_engine, text

# --- CONFIGURATION CORRIGÉE POUR DOCKER ---
# On récupère les valeurs depuis docker-compose, sinon on met des valeurs par défaut
DB_HOST = os.getenv("DB_HOST", "timescaledb")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "agro_timeseries") # C'était agrotrace_db, il faut agro_timeseries
DB_USER = os.getenv("DB_USER", "admin")           # C'était postgres, il faut admin
DB_PASSWORD = os.getenv("DB_PASSWORD", "adminpassword") # C'était password, il faut adminpassword

# URL de connexion
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

def get_engine():
    return engine

def get_sensor_data(sensor_id):
    """Récupère l'historique d'humidité pour un capteur donné."""
    # Note: On s'assure que la table existe, sinon ça plantera au premier lancement
    try:
        query = text(f"SELECT time, soil_humidity FROM sensor_measurements WHERE sensor_id = '{sensor_id}' ORDER BY time ASC")
        with engine.connect() as conn:
            return pd.read_sql(query, conn)
    except Exception as e:
        print(f"⚠️ Erreur lecture données (Table vide ou inexistante ?): {e}")
        return pd.DataFrame() # Retourne vide pour ne pas crasher

def save_forecasts(df_forecast, sensor_id, model_name):
    """Sauvegarde les prévisions."""
    if df_forecast is None or df_forecast.empty:
        print(f"Rien à sauvegarder pour {model_name}.")
        return

    print(f"Sauvegarde des résultats de {model_name}...")
    
    # On garde juste les colonnes utiles
    output_df = pd.DataFrame({
        'time': df_forecast['ds'],
        'sensor_id': sensor_id,
        'predicted_humidity': df_forecast['yhat'],
        'model_used': model_name
    })

    try:
        with engine.connect() as conn:
            output_df.to_sql('water_forecasts', conn, if_exists='append', index=False)
        print(f"✅ Sauvegarde terminée pour {model_name} !")
    except Exception as e:
        print(f"❌ Erreur sauvegarde SQL : {e}")