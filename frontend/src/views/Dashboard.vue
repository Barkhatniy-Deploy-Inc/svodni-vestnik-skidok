<template>
  <div class="dashboard">
    <div v-if="store.loading && store.items.length === 0" class="loader">Считываем данные...</div>
    
    <div v-if="store.items.length > 0" class="actions-bar">
      <button @click="updatePrices" :disabled="updating" class="update-all-btn">
        {{ updating ? t('update_running') : '🔄 ' + t('update_btn') }}
      </button>
    </div>

    <div v-if="store.items.length === 0 && !store.loading" class="empty-state">
      <div class="icon">🔍</div>
      <p>{{ t('dashboard_empty') }}</p>
    </div>

    <div v-else class="product-list">
      <div v-for="item in store.items" :key="item.id" class="product-card">
        <div class="card-header">
          <div class="info">
            <h3>{{ item.name }}</h3>
            <div class="price-group">
              <span class="current">{{ item.current_price || '...' }} ₽</span>
              <span class="target">{{ t('add_price_label') }}: {{ item.target_price }} ₽</span>
            </div>
          </div>
          <button @click="deleteProduct(item.id)" class="delete-btn">×</button>
        </div>
        
        <div class="chart-wrapper" v-if="item.price_history && item.price_history.length > 0">
          <PriceChart :history="item.price_history.map(h => h.price)" />
        </div>
        
        <div class="card-footer">
          <span class="last-update">{{ t('last_update') }}: {{ formatDate(item.updated_at) }}</span>
          <div class="status-indicator" :class="{ 'ready': item.current_price <= item.target_price && item.current_price > 0 }">
            {{ (item.current_price <= item.target_price && item.current_price > 0) ? t('status_ready') : t('status_waiting') }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useProductStore } from '../store/products';
import { useTranslation } from '../api/messages';
import client from '../api/client';
import PriceChart from '../components/PriceChart.vue';

const store = useProductStore();
const { t } = useTranslation();
const updating = ref(false);

const updatePrices = async () => {
  updating.value = true;
  try {
    await client.post('/products/update-all');
    alert(t('update_success'));
  } catch (err) {
    const msg = err.response?.data?.detail || 'Ошибка при обновлении';
    alert(msg);
  } finally {
    updating.value = false;
  }
};

onMounted(() => {
  store.fetchProducts();
});

const formatDate = (dateStr) => {
  if (!dateStr) return 'Неизвестно';
  const date = new Date(dateStr);
  return date.toLocaleString('ru-RU', { 
    day: '2-digit', 
    month: '2-digit', 
    hour: '2-digit', 
    minute: '2-digit' 
  });
};

const deleteProduct = async (id) => {
  if (confirm(t('delete_confirm'))) {
    await store.removeProduct(id);
  }
};
</script>

<style scoped>
.actions-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.update-all-btn {
  background: rgba(var(--accent-rgb), 0.1);
  border: 1px solid var(--accent-color);
  color: var(--accent-color);
  padding: 10px 20px;
  border-radius: 12px;
  font-weight: bold;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.update-all-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.update-all-btn:hover:not(:disabled) {
  background: var(--accent-color);
  color: #000;
}

.loader {
  text-align: center;
  margin-top: 100px;
  color: var(--accent-color);
  font-weight: bold;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 0.5; }
  50% { opacity: 1; }
  100% { opacity: 0.5; }
}

.empty-state {
  text-align: center;
  margin-top: 60px;
  color: var(--text-muted);
}

.empty-state .icon {
  font-size: 3rem;
  margin-bottom: 10px;
}

.product-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.product-card {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: all 0.3s ease;
}

.product-card:active {
  transform: scale(0.98);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

h3 {
  font-size: 1.1rem;
  margin: 0 0 8px 0;
  color: #fff;
}

.price-group {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.current {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--accent-color);
}

.target {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.delete-btn {
  background: rgba(239, 68, 68, 0.1);
  border: none;
  color: #ef4444;
  font-size: 1.5rem;
  line-height: 1;
  padding: 0 8px;
  border-radius: 6px;
  cursor: pointer;
}

.status-indicator {
  font-size: 0.65rem;
  font-weight: 900;
  padding: 4px 10px;
  border-radius: 8px;
  background: rgba(148, 163, 184, 0.1);
  color: var(--text-muted);
  border: 1px solid var(--border-color);
}

.status-indicator.ready {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success-color);
  border-color: var(--success-color);
  box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
}

.chart-wrapper {
  margin: 15px -10px;
  background: rgba(15, 23, 42, 0.3);
  border-radius: 12px;
  padding: 10px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.last-update {
  font-size: 0.7rem;
  color: var(--text-muted);
}
</style>
