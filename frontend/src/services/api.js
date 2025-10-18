import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => axios.post(`${API_BASE_URL}/token/`, credentials),
  register: (userData) => axios.post(`${API_BASE_URL}/register/`, userData),
  refreshToken: (refresh) => axios.post(`${API_BASE_URL}/token/refresh/`, { refresh }),
};

// Books API
export const booksAPI = {
  getAll: () => api.get('/books/'),
  getById: (id) => api.get(`/books/${id}/`),
  create: (bookData) => api.post('/books/', bookData),
  update: (id, bookData) => api.put(`/books/${id}/`, bookData),
  delete: (id) => api.delete(`/books/${id}/`),
  searchGoogle: (query) => api.get(`/google-books/?q=${encodeURIComponent(query)}`),
};

// Loans API
export const loansAPI = {
  getAll: () => api.get('/loans/'),
  getById: (id) => api.get(`/loans/${id}/`),
  create: (loanData) => api.post('/loans/', loanData),
  returnBook: (id) => api.post(`/loans/${id}/return_book/`),
};

// Reservations API
export const reservationsAPI = {
  getAll: () => api.get('/reservations/'),
  getById: (id) => api.get(`/reservations/${id}/`),
  create: (reservationData) => api.post('/reservations/', reservationData),
  cancel: (id) => api.post(`/reservations/${id}/cancel_reservation/`),
  getMy: () => api.get('/reservations/my_reservations/'),
};

// Reviews API
export const reviewsAPI = {
  getAll: () => api.get('/reviews/'),
  getById: (id) => api.get(`/reviews/${id}/`),
  create: (reviewData) => api.post('/reviews/', reviewData),
  delete: (id) => api.delete(`/reviews/${id}/`),
};

// Profile API
export const profileAPI = {
  get: () => api.get('/profiles/'),
  update: (id, profileData) => api.put(`/profiles/${id}/`, profileData),
};

// Dashboard API
export const dashboardAPI = {
  get: () => api.get('/dashboard/'),
};

// Users API
export const usersAPI = {
  getAll: () => api.get('/users/'),
  getById: (id) => api.get(`/users/${id}/`),
  update: (id, userData) => api.put(`/users/${id}/`, userData),
  delete: (id) => api.delete(`/users/${id}/`),
};

export default api;
