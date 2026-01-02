# 🌱 AgroTrace MS  
**Plateforme de Precision Agriculture basée sur une architecture microservices**

AgroTrace est une plateforme de gestion agricole permettant le **suivi en temps réel des parcelles** grâce à des capteurs IoT et à l’**analyse de la santé des cultures via drones (UAV)**.  
Elle aide à la prise de décision agricole, notamment pour l’irrigation et le suivi de la santé végétale.

---

## 🏗️ Architecture Technique

La plateforme repose sur une architecture **microservices** interconnectée via un système de messagerie et des bases de données spécialisées.

### Services principaux

- **Ingestion de données**
  - API et workers Python
  - Collecte des données capteurs via **Apache Kafka**

- **Moteur de règles**
  - Service Java utilisant **JBoss Drools**
  - Génération de recommandations d’irrigation basées sur des seuils agronomiques

- **Analyse Vision (Drone)**
  - Traitement d’images UAV
  - Calcul de l’indice **NDVI** et diagnostic de la santé des cultures

- **Dashboard SIG**
  - Interface cartographique en **React**
  - Visualisation spatiale des parcelles avec **PostGIS**

- **Infrastructure**
  - **Nginx** (API Gateway)
  - **MinIO (S3)** pour le stockage
  - **TimescaleDB** pour les séries temporelles

---

## 🧰 Technologies utilisées

### Backend
- Python (**FastAPI**)
- Java (**Spring Boot**)

### Bases de données
- **PostGIS** : données spatiales
- **TimescaleDB** : séries temporelles

### Messaging
- **Apache Kafka**
- **Zookeeper**

### DevOps
- **Docker**
- **Docker Compose**

### SIG & Frontend
- **React**
- **Leaflet.js**
- **OpenStreetMap**

---

## 🚀 Installation et Déploiement

### Prérequis
- Docker et Docker Compose
- Python **3.10+**

### Modèle Utilisé
VisionPlant : https://www.kaggle.com/code/idrissbk/visionplant

PrevisionEau : https://github.com/yahia951/PrevisionEau/blob/main/PrevisionEau/notebooks/train_model.ipynb

### Lancement de l’infrastructure

```bash
git clone [url-du-depot]
cd AgroTrace-MS
docker-compose up -d --build



Fonctionnalités principales

🗺️ Visualisation SIG
Cartographie interactive des parcelles avec état de santé codé par couleur

📡 Monitoring IoT
Suivi en temps réel de l’humidité, de la température et de la vitesse du vent

💧 Aide à la décision
Calcul automatique du volume d’irrigation requis par m² via le moteur Drools

🚁 Analyse Drone
Alertes basées sur l’indice NDVI pour détecter précocement les carences végétales
