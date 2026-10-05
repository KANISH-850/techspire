import apiClient from './client';

export const inventoryApi = {
  getStatus: async () => {
    const response = await apiClient.get('/inventory/status');
    return response.data;
  },
  getLowStock: async () => {
    const response = await apiClient.get('/inventory/low-stock');
    return response.data;
  },
  getExpiryAlerts: async () => {
    const response = await apiClient.get('/inventory/expiry');
    return response.data;
  },
  getItems: async (params = {}) => {
    const response = await apiClient.get('/inventory/items', { params });
    return response.data;
  },
  getItemById: async (id) => {
    const response = await apiClient.get(`/inventory/items/${id}`);
    return response.data;
  },
  createItem: async (data) => {
    const response = await apiClient.post('/inventory/items', data);
    return response.data;
  }
};

export default inventoryApi;
