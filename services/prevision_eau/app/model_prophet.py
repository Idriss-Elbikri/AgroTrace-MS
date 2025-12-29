import pandas as pd
from prophet import Prophet
from app.database import get_sensor_data
import logging

# On rend Prophet un peu moins bavard dans la console
logging.getLogger('cmdstanpy').setLevel(logging.WARNING)

def run_prophet_model(sensor_id, days_to_predict=7):
    print(f"[Prophet] Entraînement en cours pour {sensor_id}...")

    # 1. Récupération des données depuis la BDD
    df = get_sensor_data(sensor_id)
    
    if df.empty:
        print("Aucune donnée trouvée !")
        return None

    # 2. Préparation pour Prophet
    # Prophet est très strict : il veut deux colonnes nommées exactement 'ds' (date) et 'y' (valeur)
    # Le .dt.tz_localize(None) sert à retirer le fuseau horaire qui gêne parfois Prophet
    df['time'] = pd.to_datetime(df['time']).dt.tz_localize(None)
    
    training_data = df.rename(columns={'time': 'ds', 'soil_humidity': 'y'})

    # 3. Création et Entraînement du modèle
    model = Prophet(daily_seasonality=True) # On lui dit que l'humidité change chaque jour (cycle jour/nuit)
    model.fit(training_data)

    # 4. Prédiction
    print(f"[Prophet] Calcul des prévisions sur {days_to_predict} jours...")
    future = model.make_future_dataframe(periods=days_to_predict, freq='h') # 'h' pour heures
    forecast = model.predict(future)

    # 5. On ne garde que la fin (les jours futurs)
    # On retourne juste la date (ds) et la prédiction (yhat)
    future_forecast = forecast.tail(days_to_predict * 24)[['ds', 'yhat']]
    
    return future_forecast

# --- BLOC DE TEST ---
# Ce code ne s'exécute que si tu lances le fichier directement
if __name__ == "__main__":
    result = run_prophet_model('capteur_parcelle_A')
    print("\n--- RÉSULTAT DU TEST ---")
    print(result.head()) # Affiche les 5 premières prédictions
    print("...")