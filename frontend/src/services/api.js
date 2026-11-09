import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create Axios client instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
});

// Request interceptor: attach dynamic Role and User headers
apiClient.interceptors.request.use(
  (config) => {
    const currentRole = localStorage.getItem('mi_growth_user_role') || 'CFO';
    const currentUserName = localStorage.getItem('mi_growth_user_name') || `${currentRole}_User`;
    config.headers['X-User-Role'] = currentRole;
    config.headers['X-User-Name'] = currentUserName;
    return config;
  },
  (error) => Promise.reject(error)
);

/**
 * Format error responses from Django REST Framework into readable text messages.
 */
export const formatApiError = (error) => {
  if (!error.response) {
    return error.message || 'Unable to connect to the backend server. Please verify Django is running on http://localhost:8000.';
  }

  const { data, status } = error.response;

  if (status === 403) {
    return data.detail || 'Access Denied: Your current role does not have permission for this action.';
  }

  if (status === 404) {
    return data.detail || 'The requested growth level record was not found.';
  }

  if (data && typeof data === 'object') {
    const errorMessages = [];
    for (const [key, val] of Object.entries(data)) {
      const fieldTitle = key === 'non_field_errors' ? '' : `${key.replace('_', ' ').toUpperCase()}: `;
      if (Array.isArray(val)) {
        errorMessages.push(`${fieldTitle}${val.join(' ')}`);
      } else if (typeof val === 'string') {
        errorMessages.push(`${fieldTitle}${val}`);
      } else {
        errorMessages.push(`${fieldTitle}${JSON.stringify(val)}`);
      }
    }
    return errorMessages.join(' | ') || `Error (${status}): Operation failed.`;
  }

  return `Error (${status}): Server returned unexpected response.`;
};

export const growthLevelsApi = {
  /**
   * List all MI Net Growth Levels with optional filters, search, and pagination.
   */
  getAll: async (params = {}) => {
    const response = await apiClient.get('/mi-net-growth-levels/', { params });
    return response.data;
  },

  /**
   * Retrieve a single record by PK ID.
   */
  getById: async (id) => {
    const response = await apiClient.get(`/mi-net-growth-levels/${id}/`);
    return response.data;
  },

  /**
   * Create a new level. Supports FormData (multipart/form-data) or JSON.
   */
  create: async (data) => {
    const isFormData = data instanceof FormData;
    const response = await apiClient.post('/mi-net-growth-levels/', data, {
      headers: {
        'Content-Type': isFormData ? 'multipart/form-data' : 'application/json',
      },
    });
    return response.data;
  },

  /**
   * Full update of a level record. Supports FormData or JSON.
   */
  update: async (id, data) => {
    const isFormData = data instanceof FormData;
    // Use POST or PATCH/PUT. With multipart on Django, PATCH/PUT works cleanly or multipart PUT:
    const response = await apiClient.patch(`/mi-net-growth-levels/${id}/`, data, {
      headers: {
        'Content-Type': isFormData ? 'multipart/form-data' : 'application/json',
      },
    });
    return response.data;
  },

  /**
   * Delete a level record.
   */
  delete: async (id) => {
    const response = await apiClient.delete(`/mi-net-growth-levels/${id}/`);
    return response.data;
  },

  /**
   * Fetch aggregate statistics for dashboard KPI cards.
   */
  getStatistics: async () => {
    const response = await apiClient.get('/mi-net-growth-levels/statistics/');
    return response.data;
  },

  /**
   * Download attachment file as a browser blob.
   */
  downloadAttachment: async (id, filename = 'attachment') => {
    const response = await apiClient.get(`/mi-net-growth-levels/${id}/download_attachment/`, {
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
  },
};

export default apiClient;
