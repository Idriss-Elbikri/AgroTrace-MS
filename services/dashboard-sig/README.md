# DashboardSIG - Microservice de Visualisation Cartographique

## Description

Ce microservice fournit une interface de visualisation cartographique pour AgroTrace, permettant d'afficher :

- L'état des parcelles agricoles
- Les prévisions météorologiques
- Les résultats d'analyse de vision (images satellite/drone)
- Les recommandations d'irrigation

## Technologies utilisées

- **Frontend**: React.js 19 + Vite
- **Cartographie**: Leaflet / React-Leaflet
- **Communication**: API REST (Axios)
- **Conteneurisation**: Docker + Nginx

## Structure du projet

```
src/
├── components/          # Composants réutilisables
│   ├── Header/         # En-tête avec filtres
│   ├── Map/            # Composant carte Leaflet
│   ├── Sidebar/        # Panneau latéral de détails
│   └── StatsBar/       # Barre de statistiques
├── config/             # Configuration (API endpoints)
├── data/               # Données de démonstration
├── pages/              # Pages de l'application
│   └── Dashboard/      # Page principale
└── services/           # Services API
    ├── api.service.js         # Client Axios configuré
    ├── parcelles.service.js   # Service parcelles
    ├── previsions.service.js  # Service météo
    ├── vision.service.js      # Service analyse vision
    └── irrigation.service.js  # Service irrigation
```

## Installation

### Prérequis

- Node.js 18+
- npm ou yarn

### Installation des dépendances

```bash
npm install
```

### Lancement en développement

```bash
npm run dev
```

L'application sera accessible sur `http://localhost:5173`

## Déploiement Docker

### Build de l'image

```bash
docker build -t agrotrace/dashboard-sig .
```

### Lancement avec docker-compose

```bash
docker-compose up -d
```

L'application sera accessible sur `http://localhost:3000`

## Configuration

### Variables d'environnement

Créer un fichier `.env.local` basé sur `.env.example` :

| Variable                      | Description                  | Défaut                  |
| ----------------------------- | ---------------------------- | ----------------------- |
| `VITE_API_BASE_URL`           | URL de l'API Gateway         | `http://localhost:8080` |
| `VITE_USE_MOCK_DATA`          | Utiliser les données de démo | `true`                  |
| `VITE_MAP_DEFAULT_CENTER_LAT` | Latitude centre carte        | `31.7917`               |
| `VITE_MAP_DEFAULT_CENTER_LNG` | Longitude centre carte       | `-7.0926`               |
| `VITE_MAP_DEFAULT_ZOOM`       | Zoom par défaut              | `6`                     |

## Endpoints API consommés

Le dashboard consomme les endpoints suivants des autres microservices :

### Parcelles

- `GET /api/parcelles` - Liste des parcelles
- `GET /api/parcelles/geojson` - Parcelles au format GeoJSON

### Prévisions

- `GET /api/previsions/parcelle/{id}` - Prévisions pour une parcelle

### Vision

- `GET /api/vision/parcelle/{id}` - Résultats d'analyse pour une parcelle

### Irrigation

- `GET /api/irrigation/parcelle/{id}` - Recommandations pour une parcelle

## Fonctionnalités

### Carte interactive

- Affichage des parcelles avec code couleur selon l'état
- Popup d'information au survol
- Zoom automatique sur les données

### Panneau de détails

- Informations générales de la parcelle
- Prévisions météo
- Résultats d'analyse de vision (NDVI, santé végétale)
- Recommandations d'irrigation

### Filtres

- Par type de culture
- Par état de la parcelle
- Par priorité d'irrigation

## Scripts disponibles

```bash
npm run dev      # Lancement en mode développement
npm run build    # Build de production
npm run preview  # Prévisualisation du build
npm run lint     # Vérification du code
```

## Licence

AgroTrace © 2025
