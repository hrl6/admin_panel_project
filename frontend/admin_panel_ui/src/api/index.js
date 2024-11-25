import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true
})

export const productAPI = {
  getAll: () => api.get('products/'),
  get: (id) => api.get(`products/${id}/`),
  create: (data) => api.post('products/', data),
  update: (id, data) => api.put(`products/${id}/`, data),
  delete: (id) => api.delete(`products/${id}/`)
};

export const orderAPI = {
  getAll: () => api.get('orders/'),
  get: (id) => api.get(`orders/${id}/`),
  create: (data) => api.post('orders/', data),
  update: (id, data) => api.put(`orders/${id}/`, data),
  delete: (id) => api.delete(`orders/${id}/`)
};

export default api