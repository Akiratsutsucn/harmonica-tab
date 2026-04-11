import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
});

export const searchSongs = (q = '', page = 1, difficulty = null) =>
  api.get('/songs', { params: { q, page, ...(difficulty ? { difficulty } : {}) } }).then(r => r.data);

export const getHotSongs = () =>
  api.get('/songs/hot').then(r => r.data);

export const getSong = (id) =>
  api.get(`/songs/${id}`).then(r => r.data);

export const getMapping = (key = 'C', tuning = 'paddy') =>
  api.get(`/mapping/${key}`, { params: { tuning } }).then(r => r.data);

export const batchSongs = (ids) =>
  api.post('/songs/batch', ids).then(r => r.data);

export const getKeys = () =>
  api.get('/mapping').then(r => r.data);
