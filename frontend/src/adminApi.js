import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
});

// Inject auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = (password) =>
  api.post('/admin/login', { password }).then(r => r.data);

export const getDashboard = () =>
  api.get('/admin/dashboard').then(r => r.data);

export const getAdminSongs = (params = {}) =>
  api.get('/admin/songs', { params }).then(r => r.data);

export const createSong = (data) =>
  api.post('/admin/songs', data).then(r => r.data);

export const updateSong = (id, data) =>
  api.put(`/admin/songs/${id}`, data).then(r => r.data);

export const deleteSong = (id) =>
  api.delete(`/admin/songs/${id}`).then(r => r.data);

export const getSongNotes = (id) =>
  api.get(`/admin/songs/${id}/notes`).then(r => r.data);

export const updateSongNotes = (id, notes) =>
  api.put(`/admin/songs/${id}/notes`, { notes }).then(r => r.data);

export const verifySong = (id) =>
  api.post(`/admin/songs/${id}/verify`).then(r => r.data);

export const rejectSong = (id) =>
  api.post(`/admin/songs/${id}/reject`).then(r => r.data);

export const submitAIGenerate = (data) =>
  api.post('/admin/tasks/ai-generate', data).then(r => r.data);

export const submitCrawl = (data) =>
  api.post('/admin/tasks/crawl', data).then(r => r.data);

export const submitImport = (file) => {
  const form = new FormData();
  form.append('file', file);
  return api.post('/admin/tasks/import', form).then(r => r.data);
};

export const getTasks = (params = {}) =>
  api.get('/admin/tasks', { params }).then(r => r.data);

export const getTask = (id) =>
  api.get(`/admin/tasks/${id}`).then(r => r.data);
