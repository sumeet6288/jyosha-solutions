import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

// Create axios instance
const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('chatbase_token');
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
      localStorage.removeItem('chatbase_token');
      localStorage.removeItem('chatbase_user');
      window.location.href = '/signin';
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getCurrentUser: () => api.get('/auth/me'),
  logout: () => api.post('/auth/logout'),
};

// User APIs
export const userAPI = {
  updateProfile: (data) => api.put('/user/profile', data),
  changePassword: (data) => api.put('/user/password', data),
  deleteAccount: () => api.delete('/user/account'),
};

// Chatbot APIs
export const chatbotAPI = {
  list: () => api.get('/chatbots'),
  create: (data) => api.post('/chatbots', data),
  get: (id) => api.get(`/chatbots/${id}`),
  update: (id, data) => api.put(`/chatbots/${id}`, data),
  delete: (id) => api.delete(`/chatbots/${id}`),
};

// Source APIs
export const sourceAPI = {
  list: (chatbotId) => api.get(`/sources/chatbot/${chatbotId}`),
  uploadFile: (chatbotId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/sources/chatbot/${chatbotId}/file`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  addWebsite: (chatbotId, url) => {
    const formData = new FormData();
    formData.append('url', url);
    return api.post(`/sources/chatbot/${chatbotId}/website`, formData);
  },
  addText: (chatbotId, name, content) => {
    const formData = new FormData();
    formData.append('name', name);
    formData.append('content', content);
    return api.post(`/sources/chatbot/${chatbotId}/text`, formData);
  },
  delete: (sourceId) => api.delete(`/sources/${sourceId}`),
};

// Chat APIs
export const chatAPI = {
  sendMessage: (data) => api.post('/chat', data),
  getConversations: (chatbotId) => api.get(`/chat/conversations/${chatbotId}`),
  getMessages: (conversationId) => api.get(`/chat/messages/${conversationId}`),
};

// Analytics APIs
export const analyticsAPI = {
  getDashboard: () => api.get('/analytics/dashboard'),
  getChatbot: (chatbotId, days = 30) => api.get(`/analytics/chatbot/${chatbotId}?days=${days}`),
};

export default api;
