import apiClient from './client';

export const procurementApi = {
  getVendors: async () => {
    const response = await apiClient.get('/procurement/vendors');
    return response.data;
  },
  createVendor: async (data) => {
    const response = await apiClient.post('/procurement/vendors', data);
    return response.data;
  },
  getAIRecommendations: async () => {
    const response = await apiClient.get('/procurement/ai-recommendations');
    return response.data;
  },
  getPurchaseOrders: async () => {
    const response = await apiClient.get('/procurement/purchase-orders');
    return response.data;
  },
  createPurchaseOrder: async (data) => {
    const response = await apiClient.post('/procurement/purchase-orders', data);
    return response.data;
  },
  updatePurchaseOrderStatus: async (id, status) => {
    const response = await apiClient.patch(`/procurement/purchase-orders/${id}`, { status });
    return response.data;
  }
};

export default procurementApi;
