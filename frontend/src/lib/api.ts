import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export const fetchReviews = async () => {
  const res = await api.get('/reviews');
  return res.data.reviews;
};

export const fetchInsights = async () => {
  const res = await api.get('/insights');
  return res.data.insights;
};

export const fetchDashboardStats = async () => {
  const res = await api.get('/dashboard-stats');
  return res.data.stats;
};

export const triggerAnalysis = async () => {
  const res = await api.post('/analyze');
  return res.data;
};

export const chatWithAssistant = async (text: string) => {
  const res = await api.post('/chat', { text });
  return res.data.response;
};

export const uploadCSV = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await api.post('/upload-csv', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  return res.data;
};
