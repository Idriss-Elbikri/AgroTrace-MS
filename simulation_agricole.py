import requests
import time
import random
import json
from datetime import datetime

# --- CONFIGURATION ---
API_URL = "http://localhost:8000/ingest" 
SENSOR_IDS = ["capteur_parcelle_A", "capteur_parcelle_B", "capteur_serre_1"]

def send_measurement(sensor_id, type_mesure, valeur):
    """Envoie une mesure au format validé par config.py"""
    
    payload = {
        "sensor_id": sensor_id,
        "type": type_mesure,      
        "value": float(valeur),
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": {}
    }

    try:
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            # On affiche un joli message vert
            print(f"✅ [{sensor_id}] {type_mesure}: {valeur}")
        else:
            # On affiche l'erreur détaillée
            print(f"❌ Erreur {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"⚠️ Erreur de connexion : {e}")

def run_simulation():
    print(f"🚜 Démarrage de la simulation vers {API_URL}...")
    print("--- Envoi des données compatibles : temperature, humidite, luminosite ---")
    print("Appuyez sur CTRL+C pour arrêter.")
    
    try:
        while True:
            for sensor in SENSOR_IDS:
                # 1. Température (Autorisé)
                temp = round(random.uniform(20.0, 35.0), 2)
                send_measurement(sensor, "temperature", temp)

                # 2. Humidité (Correction : soil_humidity -> humidite)
                hum = round(random.uniform(30.0, 60.0), 2)
                send_measurement(sensor, "humidite", hum)

                # 3. Luminosité (Remplacement de uv_index car non supporté)
                lum = round(random.uniform(1000.0, 50000.0), 1)
                send_measurement(sensor, "luminosite", lum)
            
            print("--- Cycle terminé, pause de 2s ---")
            time.sleep(2) 
            
    except KeyboardInterrupt:
        print("\n🛑 Simulation arrêtée.")

if __name__ == "__main__":
    run_simulation()