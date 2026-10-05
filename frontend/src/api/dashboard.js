import apiClient from './client';

export const dashboardApi = {
  getKPIs: async (params = {}) => {
    const response = await apiClient.get('/dashboard/kpis', { params });
    return response.data;
  },
  getRevenue: async (params = {}) => {
    const response = await apiClient.get('/dashboard/revenue', { params });
    return response.data;
  },
  getDepartments: async (params = {}) => {
    const response = await apiClient.get('/dashboard/departments', { params });
    return response.data.departments || response.data;
  },
  getAlerts: async () => {
    const response = await apiClient.get('/dashboard/alerts');
    return response.data;
  },
  getAIInsights: async () => {
    const response = await apiClient.get('/dashboard/ai-insights');
    return response.data;
  }
};

export default dashboardApi;
