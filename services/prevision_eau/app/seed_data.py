import pandas as pd
import numpy as np
from database import get_engine
from datetime import datetime

def generate_fake_data():
    engine = get_engine()
    print("🌱 Génération de données factices pour l'entraînement...")

    # 1. On crée une chronologie sur les 60 derniers jours (1 mesure par heure)
    # Cela fait environ 1440 points de données, suffisant pour tester.
    dates = pd.date_range(end=datetime.now(), periods=60*24, freq='H')
    
    # 2. On simule des valeurs un peu réalistes
    # Humidité du sol entre 30% et 80% (avec un peu de hasard)
    humidity = np.random.uniform(30, 80, size=len(dates))
    
    # Température entre 10°C et 35°C
    temperature = np.random.uniform(10, 35, size=len(dates))
    
    # 3. Création du DataFrame (Tableau de données)
    df = pd.DataFrame({
        'time': dates,
        'sensor_id': 'capteur_parcelle_A', # On simule un capteur nommé A
        'soil_humidity': humidity,
        'temperature': temperature,
        'precipitation': 0.0 # On met 0 pluie pour simplifier l'exemple
    })

    # 4. Envoi vers la base de données (Table INPUT)
    try:
        df.to_sql('sensor_measurements', engine, if_exists='append', index=False)
        print(f"SUCCÈS : {len(df)} mesures insérées pour le 'capteur_parcelle_A'.")
        print("   Tu as maintenant un historique pour entraîner tes IA !")
    except Exception as e:
        print(f"Erreur lors de l'insertion : {e}")

if __name__ == "__main__":
    generate_fake_data()