import apiClient from "./api.service";
import API_CONFIG from "../config/api";

const { PARCELLES } = API_CONFIG.ENDPOINTS;

/**
 * Service pour la gestion des parcelles
 */
const parcellesService = {
  /**
   * Récupère toutes les parcelles
   */
  getAll: async () => {
    const response = await apiClient.get(PARCELLES.GET_ALL);
    return response.data;
  },

  /**
   * Récupère une parcelle par son ID
   */
  getById: async (id) => {
    const response = await apiClient.get(PARCELLES.GET_BY_ID(id));
    return response.data;
  },

  /**
   * Récupère les parcelles au format GeoJSON pour l'affichage sur la carte
   */
  getGeoJSON: async () => {
    const response = await apiClient.get(PARCELLES.GET_GEOJSON);
    return response.data;
  },
};

export default parcellesService;
