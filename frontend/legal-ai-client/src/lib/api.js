// API service for AdvocaDabra frontend
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('advocadabra_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('advocadabra_token');
      localStorage.removeItem('advocadabra_user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },

  signup: async (email, password, name) => {
    const response = await api.post('/auth/signup', { email, password, name });
    return response.data;
  },

  verify: async () => {
    const response = await api.get('/auth/verify');
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('advocadabra_token');
    localStorage.removeItem('advocadabra_user');
  }
};

// File API
export const fileAPI = {
  upload: async (file, onUploadProgress) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress
    });
    return response.data;
  },

  list: async () => {
    const response = await api.get('/files');
    return response.data;
  },

  analyze: async (fileId, analysisType = 'scr', k = 10) => {
    const response = await api.post('/analyze-file', {
      file_id: fileId,
      type: analysisType,
      k
    });
    return response.data;
  }
};

// AI Analysis API
export const aiAPI = {
  scr: async (query, k = 10) => {
    const response = await api.post('/scr', { query, k });
    return response.data;
  },

  pcr: async (query, k = 5, explanation = false) => {
    const response = await api.post('/pcr', { query, k, explanation });
    return response.data;
  }
};

// Health check
export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export default api;
