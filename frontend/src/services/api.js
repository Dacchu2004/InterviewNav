import axios from 'axios';
import toast from 'react-hot-toast';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
});

// Add token to requests and set Content-Type only for JSON
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    // Only set Content-Type for JSON requests (not for multipart/form-data)
    if (!config.headers['Content-Type'] && !(config.data instanceof FormData)) {
      config.headers['Content-Type'] = 'application/json';
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token expiration and errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const errorMessage = error.response?.data?.error || 'An unexpected error occurred';
    
    if (error.response?.status === 401 || error.response?.status === 422) {
      // 401 = Unauthorized, 422 = Unprocessable Entity (JWT errors)
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      
      toast.error('Session expired. Please login again.');
      
      // Only redirect if not already on login/signup page
      if (!window.location.pathname.includes('/login') && !window.location.pathname.includes('/signup')) {
        setTimeout(() => {
            window.location.href = '/login';
        }, 1500); // Small delay to let user see the toast
      }
    } else {
        // Show toast for other errors too (optional, but good for UX)
         toast.error(errorMessage);
    }
    return Promise.reject(error);
  }
);

export default api;

