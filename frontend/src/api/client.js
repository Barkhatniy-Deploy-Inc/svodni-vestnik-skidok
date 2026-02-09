import axios from 'axios';

// Извлекаем initData из Telegram SDK
const initData = window.Telegram?.WebApp?.initData || '';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
    'X-TG-Init-Data': initData // Передаем паспорт пользователя Telegram
  }
});

export default client;
