import apiClient from './client';

export const clinicalApi = {
  // Patients
  getPatients: async (params = {}) => {
    const response = await apiClient.get('/patients', { params });
    return response.data;
  },
  getPatientById: async (id) => {
    const response = await apiClient.get(`/patients/${id}`);
    return response.data;
  },
  createPatient: async (data) => {
    const response = await apiClient.post('/patients', data);
    return response.data;
  },

  // Appointments
  getAppointments: async (params = {}) => {
    const response = await apiClient.get('/appointments', { params });
    return response.data;
  },
  getAppointmentById: async (id) => {
    const response = await apiClient.get(`/appointments/${id}`);
    return response.data;
  },

  // Admissions
  getAdmissions: async (params = {}) => {
    const response = await apiClient.get('/admissions', { params });
    return response.data;
  },
  getAdmissionById: async (id) => {
    const response = await apiClient.get(`/admissions/${id}`);
    return response.data;
  },

  // Beds
  getBeds: async (params = {}) => {
    const response = await apiClient.get('/beds', { params });
    return response.data;
  },
  getBedById: async (id) => {
    const response = await apiClient.get(`/beds/${id}`);
    return response.data;
  }
};

export default clinicalApi;
