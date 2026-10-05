import apiClient, { downloadFile } from './client';

export const reportsApi = {
  getReportTypes: async () => {
    const response = await apiClient.get('/reports/types');
    return response.data;
  },
  generateReport: async (payload) => {
    const response = await apiClient.post('/reports/generate', payload);
    return response.data;
  },
  getHistory: async () => {
    const response = await apiClient.get('/reports/history');
    return response.data;
  },
  downloadPdf: async (reportId) => {
    return await downloadFile(`/reports/${reportId}/pdf`, `report_${reportId}.pdf`);
  },
  downloadExcel: async (reportId) => {
    return await downloadFile(`/reports/${reportId}/excel`, `report_${reportId}.xlsx`);
  }
};

export default reportsApi;
