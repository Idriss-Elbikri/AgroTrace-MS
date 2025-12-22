# Prétraitement — Microservice de Normalisation AgroTrace

## Rôle

Préparer les données capteurs et imageries UAV en amont des modèles IA :

- nettoyer et normaliser les séries temporelles issues de TimescaleDB ;
- tuiler et géoréférencer les images UAV stockées dans MinIO ;
- exposer des API asynchrones pour orchestrer les pipelines et fournir des métriques prêtes à consommer.

## Architecture cible

- **Framework** : FastAPI (async) + Uvicorn.
- **Persistance** : TimescaleDB pour les séries et le suivi des jobs (`preprocess_jobs`, `sensor_series_norm`, `uav_tiles_meta`).
- **Stockage objet** : MinIO (`uav-raw/` et `uav-tiles/` avec clés `YYYY/MM/DD/<parcel>/<mission>/<stage>/...`).
- **Messaging** : Kafka topics optionnels (`pretraitement.events`) pour notifier Vision/Prévision.
- **Tâches** : exécution via `BackgroundTasks` FastAPI (remplaçable par Celery / RQ si besoin).
- **Observabilité** : logs structurés (JSON), métriques Prometheus (ex. via `prometheus-fastapi-instrumentator`).

## Structure applicative

```
app/
├── api/
│   ├── __init__.py
│   ├── deps.py              # dépendances communes (sessions, clients)
│   ├── jobs.py              # endpoints GET /jobs
│   ├── sensors.py           # endpoints capteurs
│   └── imagery.py           # endpoints imagerie
├── config.py                # Settings Pydantic (Timescale, MinIO, Kafka…)
├── db.py                    # moteur SQLAlchemy async + session
├── logging.py               # configuration logging
├── main.py                  # création FastAPI + routers + health
├── models.py                # modèles SQLAlchemy (jobs, séries, tuiles)
├── schemas.py               # modèles Pydantic (I/O, jobs, métriques)
├── services/
│   ├── jobs.py              # gestion statut jobs
│   ├── sensors.py           # pipeline nettoyage séries
│   └── imagery.py           # pipeline GDAL/Rasterio
└── workers.py               # fonctions de background (enregistrer job, lancer pipeline)
```

## Contrats JSON

### Lecture capteurs

```json
{
  "sensor_id": "field-23-h1",
  "type": "temperature",
  "value": 23.4,
  "timestamp": "2025-12-19T09:42:11Z",
  "metadata": {
    "unit": "C",
    "parcel_id": "P-001",
    "source": "station",
    "position": { "lat": 31.79, "lng": -7.09, "alt": 420 },
    "quality_flag": "ok"
  }
}
```

### Jobs

```json
{
  "id": "job_20251219T094211Z_e1d8",
  "type": "sensor-cleaning",
  "status": "processing",
  "created_at": "2025-12-19T09:42:11Z",
  "updated_at": "2025-12-19T09:42:11Z",
  "payload": { "parcel_id": "P-001", "count": 250 },
  "result": null,
  "error": null
}
```

## Endpoints (préfixe `/api/v1/pretraitement`)

- `GET /health` — status simple.
- `POST /capteurs/clean` — crée un job de nettoyage (payload optional). Réponse `202 Accepted` + job.
- `POST /images/upload` — upload multipart → MinIO + job de prétraitement.
- `POST /images/tile` — déclenche tuilage depuis un objet MinIO existant.
- `GET /parcelles/{parcel_id}/latest` — renvoie séries normalisées + stats NDVI/nappes.
- `GET /jobs/{job_id}` — récupère statut du job.

## Lancement local

```bash
cd pretraitement
python -m venv .venv && source .venv/bin/activate  # sous Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Variables d'environnement clés : `TIMESCALE_*`, `MINIO_*`, `KAFKA_BOOTSTRAP_SERVERS`, `MINIO_RAW_BUCKET`, `MINIO_TILES_BUCKET`.

## Étapes suivantes

1. Remplacer les placeholders du pipeline capteurs par une vraie stratégie de nettoyage (imputation, agrégation, détection d'anomalies).
2. Intégrer Rasterio/GDAL dans `services/imagery.py` pour générer des tuiles géoréférencées et pousser les rasters vers MinIO.
3. Publier des événements Kafka (`pretraitement.events`) pour notifier Vision/Prévision des jobs terminés.
4. Couvrir par des tests unitaires (PyTest) et ajouter un workflow CI.
5. Écrire scripts d'initialisation MinIO/PostGIS (buckets, tables spatiales) et seed de données d'exemple.

```

```
