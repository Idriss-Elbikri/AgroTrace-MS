import json
import time
import random
from kafka import KafkaProducer
from datetime import datetime

# --- CONFIGURATION ---
KAFKA_BROKER = 'localhost:29092'
TOPICS = {
    'temp': 'capteurs.temperature',
    'hum': 'capteurs.humidite',
    'lum': 'capteurs.luminosite'
}

CAPTEURS = [
    {"id": "1", "nom": "Parcelle Nord"},
    {"id": "2", "nom": "Parcelle Sud"}
]

def get_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
            retries=5
        )
        print(f"✅ Connecté à Kafka sur {KAFKA_BROKER}")
        return producer
    except Exception as e:
        print(f"❌ Erreur de connexion Kafka : {e}")
        return None

def simulate():
    producer = get_producer()
    if not producer: return

    print("🚀 Simulation IoT AgroTrace v2 (Multi-données)...")

    try:
        while True:
            for capteur in CAPTEURS:
                # Simulation d'un pic de chaleur aléatoire pour tester Drools
                # Si > 35°C, Drools devrait changer la recommandation
                temp = round(random.uniform(20.0, 38.0), 2)
                hum = round(random.uniform(25.0, 70.0), 2)
                lum = round(random.uniform(5000, 50000), 1)
                timestamp = datetime.now().isoformat()

                # Construction des messages
                messages = [
                    (TOPICS['temp'], {"sensor_id": capteur["id"], "value": temp, "timestamp": timestamp, "type": "temperature"}),
                    (TOPICS['hum'], {"sensor_id": capteur["id"], "value": hum, "timestamp": timestamp, "type": "humidite"}),
                    (TOPICS['lum'], {"sensor_id": capteur["id"], "value": lum, "timestamp": timestamp, "type": "luminosite"})
                ]

                for topic, data in messages:
                    producer.send(topic, value=data)

                status = "🔥 CHAUD" if temp > 35 else "🌤️ NORMAL"
                print(f"📍 [{capteur['nom']}] {temp}°C ({status}) | Hum: {hum}%")

            producer.flush()
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n🛑 Simulation arrêtée.")
    finally:
        producer.close()

if __name__ == "__main__":
    simulate()