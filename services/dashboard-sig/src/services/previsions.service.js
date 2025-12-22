import apiClient from "./api.service";
import API_CONFIG from "../config/api";

const { PREVISIONS } = API_CONFIG.ENDPOINTS;

/**
 * Service pour les prévisions météo
 */
const previsionsService = {
  /**
   * Récupère les prévisions pour une parcelle
   */
  getByParcelle: async (parcelleId) => {
    const response = await apiClient.get(
      PREVISIONS.GET_BY_PARCELLE(parcelleId)
    );
    return response.data;
  },

  /**
   * Récupère les prévisions actuelles
   */
  getCurrent: async () => {
    const response = await apiClient.get(PREVISIONS.GET_CURRENT);
    return response.data;
  },
};

export default previsionsService;
