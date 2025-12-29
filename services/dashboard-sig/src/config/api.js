/**
 * Configuration des endpoints API pour le Dashboard SIG AgroTrace.
 * Toutes les requêtes passent par la Gateway Nginx (localhost:80).
 */

const API_CONFIG = {
  // URL de base pointant vers Nginx
  BASE_URL: import.meta.env.VITE_API_BASE_URL || "http://localhost",

  // Endpoints correspondant aux règles de routage définies dans nginx.conf
  ENDPOINTS: {
    // Microservice Parcelles (via microservice reco_irrigation)
    PARCELLES: {
      BASE: "/api/parcelles",
      GET_GEOJSON: "/api/parcelles/geojson",
      GET_BY_ID: (id) => `/api/parcelles/${id}`,
    },

    // Microservice Irrigation & Recommandations (via microservice reco_irrigation)
    // FIX : Pointe vers /api/parcelle/ pour éviter le retour HTML de Nginx
    IRRIGATION: {
      BASE: "/api/parcelle",
      GET_BY_PARCELLE: (id) => `/api/parcelle/${id}`,
      GET_RECOMMENDATIONS: "/api/parcelle/all",
    },

    // Microservice Vision (analyse d'images UAV)
    VISION: {
      BASE: "/api/vision",
      GET_BY_PARCELLE: (id) => `/api/vision/${id}`,
      GET_RESULTS: "/api/vision/results",
    },

    // Microservice Prévisions (LSTM / Prophet)
    PREVISIONS: {
      BASE: "/api/previsions",
      GET_BY_PARCELLE: (id) => `/api/previsions/${id}`,
      GET_CURRENT: "/api/previsions/current",
    },
  },
};

export default API_CONFIG;