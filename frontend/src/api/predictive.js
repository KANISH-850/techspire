import apiClient from './client';

export const predictiveApi = {
  getRevenueForecast: async (months = 6) => {
    const response = await apiClient.get('/predictive/revenue', { params: { months } });
    return response.data;
  },
  getAdmissionsForecast: async (days = 30) => {
    const response = await apiClient.get('/predictive/admissions', { params: { days } });
    return response.data;
  },
  getBedsForecast: async (days = 30) => {
    const response = await apiClient.get('/predictive/beds', { params: { days } });
    return response.data;
  },
  getMedicinesDemand: async (days = 30) => {
    const response = await apiClient.get('/predictive/medicines', { params: { days } });
    return response.data;
  },
  getInventoryForecast: async (days = 30) => {
    const response = await apiClient.get('/predictive/inventory', { params: { days } });
    return response.data;
  },
  getSummary: async () => {
    const response = await apiClient.get('/predictive/summary');
    return response.data;
  }
};

export default predictiveApi;
