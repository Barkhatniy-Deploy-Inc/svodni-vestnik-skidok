<template>
  <div class="dashboard">
    <div v-if="store.loading" class="loader">Считываем данные...</div>
    
    <div v-else class="product-list">
      <div v-for="item in store.items" :key="item.id" class="product-card">
        <div class="card-header">
          <div class="info">
            <h3>{{ item.name }}</h3>
            <div class="price-group">
              <span class="current">{{ item.current_price }} ₽</span>
              <span class="target">Цель: {{ item.target_price }} ₽</span>
            </div>
          </div>
          <div class="status-indicator" :class="{ 'ready': item.current_price <= item.target_price }">
            {{ item.current_price <= item.target_price ? 'ВЫГОДНО' : 'ОЖИДАНИЕ' }}
          </div>
        </div>
        
        <div class="chart-wrapper">
          <PriceChart :history="item.history" />
        </div>
        
        <div class="card-footer">
          <span class="last-update">Обновлено: только что</span>
          <button class="details-btn">История →</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useProductStore } from '../store/products';
import PriceChart from '../components/PriceChart.vue';
const store = useProductStore();
</script>

<style scoped>
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

.details-btn {
  background: transparent;
  border: none;
  color: var(--accent-color);
  font-size: 0.8rem;
  font-weight: bold;
  cursor: pointer;
}
</style>