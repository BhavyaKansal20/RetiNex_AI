import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('retinex_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('retinex_token');
      localStorage.removeItem('retinex_user');
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getProfile: () => api.get('/auth/me'),
};

export const predictionAPI = {
  predict: (formData, useTTA = false) =>
    api.post(`/predictions?use_tta=${useTTA}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 120000,
    }),
  getAll: () => api.get('/predictions'),
  getById: (id) => api.get(`/predictions/${id}`),
};

export const analyticsAPI = {
  getOverview: () => api.get('/analytics/overview'),
  getUserStats: () => api.get('/analytics/user-stats'),
};

export const researchAPI = {
  getMetrics: () => api.get('/research/metrics'),
  getModelInfo: () => api.get('/research/model-info'),
};

export const reportAPI = {
  generate: (data) => api.post('/reports/generate', data),
  download: (reportId) =>
    api.get(`/reports/${reportId}/download`, { responseType: 'blob' }),
};

export default api;
