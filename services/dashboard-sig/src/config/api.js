// Configuration des endpoints API des microservices AgroTrace

const API_CONFIG = {
  // URL de base des microservices (à adapter selon l'environnement)
  // BASE_URL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8080",
  BASE_URL: import.meta.env.VITE_API_BASE_URL || "http://localhost",

  // Endpoints des différents microservices
  ENDPOINTS: {
    // Microservice Parcelles
    PARCELLES: {
      BASE: "/api/parcelles",
      GET_ALL: "/api/parcelles",
      GET_BY_ID: (id) => `/api/parcelles/${id}`,
      GET_GEOJSON: "/api/parcelles/geojson",
    },

    // Microservice Prévisions Météo
    PREVISIONS: {
      BASE: "/api/previsions",
      GET_BY_PARCELLE: (parcelleId) => `/api/previsions/parcelle/${parcelleId}`,
      GET_CURRENT: "/api/previsions/current",
    },

    // Microservice Vision (analyse d'images)
    VISION: {
      BASE: "/api/vision",
      GET_RESULTS: "/api/vision/results",
      GET_BY_PARCELLE: (parcelleId) => `/api/vision/parcelle/${parcelleId}`,
    },

    // Microservice Irrigation
    IRRIGATION: {
      BASE: "/api/irrigation",
      GET_RECOMMENDATIONS: "/api/irrigation/recommendations",
      GET_BY_PARCELLE: (parcelleId) => `/api/irrigation/parcelle/${parcelleId}`,
    },

    // Microservice Cultures
    CULTURES: {
      BASE: "/api/cultures",
      GET_ALL: "/api/cultures",
      GET_BY_PARCELLE: (parcelleId) => `/api/cultures/parcelle/${parcelleId}`,
    },
  },
};

export default API_CONFIG;
