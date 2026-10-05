import axios from 'axios';
import authStorage from '../auth/authStorage';

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request Interceptor: Attach Bearer token
apiClient.interceptors.request.use(
  (config) => {
    const token = authStorage.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Global 401 Handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      authStorage.clear();
      window.dispatchEvent(new CustomEvent('techspire_unauthorized'));
    }
    return Promise.reject(error);
  }
);

/**
 * Stream reader for Chatbot SSE streaming endpoint
 */
export const fetchStream = async (endpoint, body, onChunk, signal) => {
  const token = authStorage.getToken();
  const headers = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
    signal,
  });

  if (!response.ok) {
    if (response.status === 401) {
      authStorage.clear();
      window.dispatchEvent(new CustomEvent('techspire_unauthorized'));
    }
    const errText = await response.text();
    throw new Error(errText || `Streaming failed with status ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder('utf-8');
  let done = false;

  while (!done) {
    const { value, done: readerDone } = await reader.read();
    done = readerDone;
    if (value) {
      const chunk = decoder.decode(value, { stream: true });
      onChunk(chunk);
    }
  }
};

/**
 * File downloader helper for PDF/Excel report downloads
 */
export const downloadFile = async (endpoint, filename) => {
  const response = await apiClient.get(endpoint, {
    responseType: 'blob',
  });
  
  const blobUrl = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = blobUrl;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(blobUrl);
};

export default apiClient;
