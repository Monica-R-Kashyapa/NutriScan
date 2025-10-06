import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getProfile: () => api.get('/auth/profile'),
  updateProfile: (data) => api.put('/auth/profile', data),
};

// Food APIs
export const foodAPI = {
  scanFood: (formData) => {
    return api.post('/food/scan', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  getHistory: (params) => api.get('/food/history', { params }),
  getScanDetail: (scanId) => api.get(`/food/history/${scanId}`),
  getInsights: (period) => api.get('/food/insights', { params: { period } }),
  compareFoods: (data) => api.post('/food/compare', data),
};

// User APIs
export const userAPI = {
  getStats: () => api.get('/user/stats'),
};

export default api;
