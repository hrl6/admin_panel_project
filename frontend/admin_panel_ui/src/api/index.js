// src/api/index.js
import axios from 'axios';
import { config } from '@/config';


const api = axios.create({
  baseURL: config.apiUrl,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  },
  withCredentials: true,
  maxRedirects: 5,
  timeout: 10000,

  validateStatus: (status) => {
    return status >= 200 && status < 300 || status === 302 || status === 301;
  }
});

// Add logging interceptor
api.interceptors.request.use(request => {
  console.log('Starting Request:', {
    url: request.url,
    method: request.method,
    headers: request.headers
  });
  return request;
});

api.interceptors.response.use(
  response => {
    console.log('Response:', response);
    return response;
  },
  error => {
    console.error('Request failed:', {
      config: {
        url: error?.config?.url,
        method: error?.config?.method,
        headers: error?.config?.headers,
      },
      status: error?.response?.status,
      data: error?.response?.data
    });
    return Promise.reject(error);
  }
);

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

export default api;

// const api = axios.create({
//   // Use environment variables for flexibility between environments
//   baseURL: import.meta.env.VITE_API_URL || '/api', // This will work with the Vite proxy
//   withCredentials: true,
//   headers: {
//     'Accept': 'application/json',
//     'Content-Type': 'application/json',
//   }
// });

// // Combined interceptors
// api.interceptors.request.use(request => {
//   console.log('Starting Request:', {
//     url: request.url,
//     method: request.method,
//     headers: request.headers
//   });
//   return request;
// });

// api.interceptors.response.use(
//   response => response,
//   error => {
//     console.error('API Error:', {
//       config: {
//         url: error?.config?.url,
//         method: error?.config?.method,
//         headers: error?.config?.headers,
//         baseURL: error?.config?.baseURL,
//       },
//       status: error?.response?.status,
//       statusText: error?.response?.statusText,
//       data: error?.response?.data,
//       message: error?.message
//     });
//     return Promise.reject(error);
//   }
// );

// API endpoints