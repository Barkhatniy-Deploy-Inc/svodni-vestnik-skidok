import axios from 'axios';

// Извлекаем initData из Telegram SDK
const initData = window.Telegram?.WebApp?.initData || '';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  headers: {
    'Content-Type': 'application/json',
    'X-TG-Init-Data': initData // Передаем паспорт пользователя Telegram
  }
});

// Глобальная обработка ошибок
client.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      const status = error.response.status;
      if (status === 401) {
        console.error('Ошибка авторизации Telegram');
      } else if (status === 429) {
        // Ошибка Rate Limit (наш ручной кулдаун)
        return Promise.reject(error);
      }
    }
    return Promise.reject(error);
  }
);

export default client;
