import { defineStore } from 'pinia';
import client from '../api/client';

export const useProductStore = defineStore('products', {
  state: () => ({
    items: JSON.parse(localStorage.getItem('vestnik_items')) || [
      { id: 1, name: 'Видеокарта RTX 4060', current_price: 32000, target_price: 30000, history: [35000, 34000, 32000] },
      { id: 2, name: 'Монитор 27" IPS', current_price: 15000, target_price: 16000, history: [18000, 17000, 15000] }
    ],
    loading: false,
    error: null
  }),
  actions: {
    async fetchProducts() {
      // В демо-режиме просто имитируем загрузку
      this.loading = true;
      setTimeout(() => { this.loading = false; }, 500);
    },
    async addProduct(url, targetPrice) {
      const newItem = {
        id: Date.now(),
        name: url.split('/').pop() || 'Новый товар',
        current_price: Math.floor(Math.random() * 10000) + 1000,
        target_price: targetPrice,
        history: [Math.floor(Math.random() * 10000) + 5000]
      };
      this.items.push(newItem);
      this.saveToLocal();
      return true;
    },
    saveToLocal() {
      localStorage.setItem('vestnik_items', JSON.stringify(this.items));
    }
  }
});
