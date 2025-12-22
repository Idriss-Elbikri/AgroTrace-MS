import apiClient from "./api.service";
import API_CONFIG from "../config/api";

const { VISION } = API_CONFIG.ENDPOINTS;

/**
 * Service pour les résultats de vision (analyse d'images)
 */
const visionService = {
  /**
   * Récupère tous les résultats de vision
   */
  getResults: async () => {
    const response = await apiClient.get(VISION.GET_RESULTS);
    return response.data;
  },

  /**
   * Récupère les résultats de vision pour une parcelle
   */
  getByParcelle: async (parcelleId) => {
    const response = await apiClient.get(VISION.GET_BY_PARCELLE(parcelleId));
    return response.data;
  },
};

export default visionService;
