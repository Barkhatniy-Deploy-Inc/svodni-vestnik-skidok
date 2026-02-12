import { defineStore } from 'pinia';
import client from '../api/client';

export const useProductStore = defineStore('products', {
  state: () => ({
    items: [],
    loading: false,
    error: null
  }),
  actions: {
    // Получение списка всех товаров с сервера
    async fetchProducts() {
      this.loading = true;
      this.error = null;
      try {
        const response = await client.get('/api/v1/products/');
        this.items = response.data;
      } catch (err) {
        console.error('Ошибка при загрузке товаров:', err);
        this.error = 'Не удалось загрузить список товаров';
      } finally {
        this.loading = false;
      }
    },

    // Добавление нового товара через бэкенд
    async addProduct(url, targetPrice) {
      this.loading = true;
      try {
        const response = await client.post('/api/v1/products/', {
          url: url,
          target_price: targetPrice
        });
        this.items.push(response.data);
        return true;
      } catch (err) {
        console.error('Ошибка при добавлении товара:', err);
        this.error = 'Не удалось добавить товар. Проверьте ссылку.';
        return false;
      } finally {
        this.loading = false;
      }
    },

    // Удаление товара
    async removeProduct(id) {
      try {
        await client.delete(`/api/v1/products/${id}`);
        this.items = this.items.filter(item => item.id !== id);
      } catch (err) {
        console.error('Ошибка при удалении товара:', err);
      }
    }
  }
});
