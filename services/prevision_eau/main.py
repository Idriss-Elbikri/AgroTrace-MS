import time
from model_prophet import run_prophet_model
from model_lstm import run_lstm_model
from database import save_forecasts

def main():
    SENSOR_ID = 'capteur_parcelle_A'
    print(f"🚀 Microservice PrévisionEau DÉMARRÉ pour {SENSOR_ID}")

    while True:
        print("\n--- 🔄 Début du cycle de prévision ---")
        
        # --- 1. Prophet ---
        try:
            print("Exécution Prophet...")
            forecast_prophet = run_prophet_model(SENSOR_ID, days_to_predict=7)
            save_forecasts(forecast_prophet, SENSOR_ID, "Prophet")
        except Exception as e:
            print(f"⚠️ Erreur Prophet (Pas assez de données ?): {e}")

        # --- 2. LSTM ---
        try:
            print("Exécution LSTM...")
            forecast_lstm = run_lstm_model(SENSOR_ID, days_to_predict=7)
            save_forecasts(forecast_lstm, SENSOR_ID, "LSTM_PyTorch")
        except Exception as e:
            print(f"⚠️ Erreur LSTM : {e}")

        print("--- ✅ Cycle terminé. Pause de 60 secondes... ---")
        time.sleep(60) # Pause avant le prochain calcul

if __name__ == "__main__":
    # Petite pause au démarrage pour laisser la DB s'allumer
    time.sleep(10) 
    main()