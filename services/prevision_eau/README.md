# 🌊 Microservice 4 : PrévisionEau (AgroTrace-MS)

Ce microservice fait partie du projet **AgroTrace-MS**. Il est responsable de la prédiction du stress hydrique des cultures à court terme (1 à 7 jours) en utilisant des modèles d'Intelligence Artificielle.

## 📋 Fonctionnalités
* **Connexion TimescaleDB :** Récupération de l'historique des capteurs.
* **Modèle A (Prophet) :** Analyse des tendances journalières et saisonnières.
* **Modèle B (LSTM - PyTorch) :** Réseau de neurones récurrent pour une précision séquentielle accrue.
* **Output Standardisé :** Sauvegarde des prévisions pour le service *RecoIrrigation*.

## 🛠️ Technologies
* **Langage :** Python 3.9
* **IA :** PyTorch (LSTM), Prophet (Facebook)
* **Base de données :** TimescaleDB (PostgreSQL optimisé séries temporelles)
* **Conteneurisation :** Docker & Docker Compose

---

## 🚀 Installation et Lancement (Recommandé)

Le projet est entièrement conteneurisé. Vous n'avez besoin que de Docker.

1.  **Lancer le microservice et la base de données :**
    ```bash
    docker-compose up --build
    ```
    *Cette commande installe les dépendances, entraîne les modèles et sauvegarde les résultats.*

2.  **Arrêter les services :**
    ```bash
    docker-compose down
    ```

---

## 💾 Structure de la Base de Données

### 1. INPUT (Ce que le service lit)
Table : `sensor_measurements` (Remplie par le Service 1 - Ingestion)

| Colonne | Type | Description |
| :--- | :--- | :--- |
| `time` | TIMESTAMPTZ | Date et heure de la mesure |
| `sensor_id` | VARCHAR | Identifiant du capteur |
| `soil_humidity` | FLOAT | Humidité du sol (Donnée cible) |
| `temperature` | FLOAT | Donnée météo contextuelle |

### 2. OUTPUT (Ce que le service génère)
Table : `water_forecasts` (Lue par le Service 6 - RecoIrrigation et Service 7 - Dashboard)

| Colonne | Type | Description |
| :--- | :--- | :--- |
| `time` | TIMESTAMPTZ | Date future prédite |
| `sensor_id` | VARCHAR | Identifiant du capteur |
| `predicted_humidity`| FLOAT | **Prévision du stress hydrique** |
| `model_used` | VARCHAR | 'Prophet' ou 'LSTM_PyTorch' |
| `created_at` | TIMESTAMPTZ | Date de génération du calcul |

---

## 🔧 Développement Local (Sans Docker)

Si vous devez modifier le code Python :

1.  Créer un environnement virtuel :
    ```bash
    python -m venv venv
    source venv/bin/activate  # ou .\venv\Scripts\activate sur Windows
    ```
2.  Installer les dépendances :
    ```bash
    pip install -r requirements.txt
    ```
3.  Lancer la base de données seule :
    ```bash
    docker-compose up -d timescaledb
    ```
4.  Exécuter le script principal :
    ```bash
    python main.py
    ```
