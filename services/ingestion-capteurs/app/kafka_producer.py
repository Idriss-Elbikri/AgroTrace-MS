import os
import json
import asyncio
import logging
from aiokafka import AIOKafkaProducer

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KafkaProducer")

# Adresse de Kafka (définie dans docker-compose)
KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

# Variable globale pour stocker la connexion
_producer = None

async def get_producer():
    """
    Récupère ou crée une connexion Kafka avec un système de RÉESSAYE (Retry).
    """
    global _producer
    
    if _producer is None:
        logger.info(f"🔌 Tentative de connexion à Kafka sur {KAFKA_SERVER}...")
        
        _producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        # --- BOUCLE DE PATIENCE (RETRY LOOP) ---
        # On essaie 15 fois (30 secondes) avant d'abandonner
        for i in range(15):
            try:
                await _producer.start()
                logger.info("✅ Kafka Connecté avec succès !")
                return _producer # Connexion réussie, on retourne le producteur
            except Exception as e:
                logger.warning(f"⏳ Kafka n'est pas encore prêt (Essai {i+1}/15)... Erreur: {e}")
                await asyncio.sleep(2)
        
        # Si on arrive ici, c'est l'échec total
        logger.error("❌ ABANDON : Impossible de joindre Kafka après 30 secondes.")
        _producer = None 

    return _producer

async def send_to_kafka(topic: str, message: dict):
    """Envoie un message en gérant les erreurs."""
    producer = await get_producer()
    
    if producer:
        try:
            await producer.send_and_wait(topic, message)
        except Exception as e:
            logger.error(f"⚠️ Erreur lors de l'envoi Kafka : {e}")
            # On force la reconnexion au prochain appel
            global _producer
            _producer = None
    else:
        logger.error("🚫 Echec d'envoi : Pas de connexion Kafka.")