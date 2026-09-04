import axios from 'axios';

const API_BASE = 'http://localhost:8001/api/v1/predictive';

export const predictiveApi = {
  checkHealth: async () => {
    const response = await axios.get(`${API_BASE}/health`);
    return response.data;
  },
  getSummary: async () => {
    const response = await axios.get(`${API_BASE}/summary`);
    return response.data;
  },
  getRevenue: async (days = 30) => {
    const response = await axios.get(`${API_BASE}/revenue?days=${days}`);
    return response.data;
  },
  getAdmissions: async (days = 30) => {
    const response = await axios.get(`${API_BASE}/admissions?days=${days}`);
    return response.data;
  },
  getBedOccupancy: async (days = 7) => {
    const response = await axios.get(`${API_BASE}/bed-occupancy?days=${days}`);
    return response.data;
  },
  getMedicineDemand: async (days = 30) => {
    const response = await axios.get(`${API_BASE}/medicine-demand?days=${days}`);
    return response.data;
  },
  getInventory: async () => {
    const response = await axios.get(`${API_BASE}/inventory`);
    return response.data;
  }
};
