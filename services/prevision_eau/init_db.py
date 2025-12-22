from sqlalchemy import text
from database import get_engine

def init_db():
    engine = get_engine()
    
    # 1. Table INPUT : Données Capteurs (Ce que tu reçois)
    # TimescaleDB demande une colonne 'time' obligatoire
    create_sensors_table = """
    CREATE TABLE IF NOT EXISTS sensor_measurements (
        time TIMESTAMPTZ NOT NULL,
        sensor_id VARCHAR(50) NOT NULL,
        soil_humidity DOUBLE PRECISION,
        temperature DOUBLE PRECISION,
        precipitation DOUBLE PRECISION
    );
    """
    
    # 2. Conversion en Hypertable (Spécialité TimescaleDB pour la performance)
    convert_sensors_hypertable = "SELECT create_hypertable('sensor_measurements', 'time', if_not_exists => TRUE);"

    # 3. Table OUTPUT : Tes Prévisions (Ce que tu envoies au Service 6)
    create_forecast_table = """
    CREATE TABLE IF NOT EXISTS water_forecasts (
        time TIMESTAMPTZ NOT NULL,
        sensor_id VARCHAR(50) NOT NULL,
        predicted_humidity DOUBLE PRECISION,
        model_used VARCHAR(50),
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    
    # 4. Conversion en Hypertable
    convert_forecast_hypertable = "SELECT create_hypertable('water_forecasts', 'time', if_not_exists => TRUE);"

    print("🚀 Initialisation de la Base de Données...")
    
    try:
        with engine.connect() as conn:
            # On exécute les commandes SQL une par une
            conn.execute(text(create_sensors_table))
            print(" - Table 'sensor_measurements' créée.")
            
            conn.execute(text(convert_sensors_hypertable))
            print(" - Optimisation TimescaleDB appliquée (Input).")
            
            conn.execute(text(create_forecast_table))
            print(" - Table 'water_forecasts' créée.")
            
            conn.execute(text(convert_forecast_hypertable))
            print(" - Optimisation TimescaleDB appliquée (Output).")
            
            conn.commit() # On valide les changements
            print("SUCCÈS : Base de données prête !")
            
    except Exception as e:
        print(f"Erreur lors de l'initialisation : {e}")

if __name__ == "__main__":
    init_db()