import apiClient from "./api.service";
import API_CONFIG from "../config/api";

const { IRRIGATION } = API_CONFIG.ENDPOINTS;

/**
 * Service pour les recommandations d'irrigation
 */
const irrigationService = {
  /**
   * Récupère toutes les recommandations d'irrigation
   */
  getRecommendations: async () => {
    const response = await apiClient.get(IRRIGATION.GET_RECOMMENDATIONS);
    return response.data;
  },

  /**
   * Récupère les recommandations pour une parcelle
   */
  getByParcelle: async (parcelleId) => {
    const response = await apiClient.get(
      IRRIGATION.GET_BY_PARCELLE(parcelleId)
    );
    return response.data;
  },
};

export default irrigationService;
