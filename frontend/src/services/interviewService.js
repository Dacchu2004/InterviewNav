import api from './api';

export const interviewService = {
  uploadCV: async (formData) => {
    // Don't set Content-Type header - let browser set it automatically with boundary
    const response = await api.post('/api/upload-cv', formData);
    return response.data;
  },

  getCurrentQuestion: async (sessionId) => {
    const response = await api.get('/api/interview/question', {
      params: { session_id: sessionId },
    });
    return response.data;
  },

  submitAnswer: async (sessionId, answer) => {
    const response = await api.post('/api/interview/answer', {
      session_id: sessionId,
      answer,
    });
    return response.data;
  },

  generateReport: async (sessionId) => {
    const response = await api.post('/api/report/generate', {
      session_id: sessionId,
    });
    return response.data;
  },

  getReports: async () => {
    const response = await api.get('/api/reports');
    return response.data;
  },

  getProfile: async () => {
    const response = await api.get('/api/profile');
    return response.data;
  },

  getPastReports: async () => {
    const response = await api.get('/api/profile/reports');
    return response.data;
  },

  getReportDetail: async (sessionId) => {
    const response = await api.get(`/api/report/${sessionId}`);
    return response.data;
  },
};

