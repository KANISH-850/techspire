import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8004/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const dashboardService = {
  getKPIs: async (filters = {}) => {
    const response = await api.get('/dashboard/kpis', { params: filters });
    return response.data;
  },
  getRevenue: async (filters = {}) => {
    const response = await api.get('/dashboard/revenue', { params: filters });
    return response.data;
  },
  getDepartments: async (filters = {}) => {
    const response = await api.get('/dashboard/departments', { params: filters });
    return response.data;
  },
  getAlerts: async () => {
    const response = await api.get('/dashboard/alerts');
    return response.data;
  },
  getAIInsights: async () => {
    const response = await api.get('/dashboard/ai-insights');
    return response.data;
  }
};

export default api;
