<template>
  <div class="add-item">
    <div class="form-card">
      <h2>Новое поручение</h2>
      <p class="description">Вверьте ссылку Вестнику, и он начнет бдение.</p>
      
      <form @submit.prevent="handleSubmit" class="form">
        <div class="input-group">
          <label>Ссылка на товар</label>
          <input 
            v-model="url" 
            type="url" 
            placeholder="https://..." 
            required 
          />
        </div>
        
        <div class="input-group">
          <label>Желаемая цена</label>
          <div class="price-input">
            <input 
              v-model.number="targetPrice" 
              type="number" 
              placeholder="0" 
              required 
            />
            <span class="currency">₽</span>
          </div>
        </div>

        <button type="submit" :disabled="submitting" class="submit-btn">
          {{ submitting ? 'ЗАПИСЫВАЕМ...' : 'В РАБОТУ' }}
          <div v-if="!submitting" class="btn-glow"></div>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useProductStore } from '../store/products';

const url = ref('');
const targetPrice = ref('');
const submitting = ref(false);
const store = useProductStore();
const router = useRouter();

const handleSubmit = async () => {
  submitting.value = true;
  await store.addProduct(url.value, targetPrice.value);
  submitting.value = false;
  router.push('/');
};
</script>

<style scoped>
.add-item {
  padding-top: 20px;
}

.form-card {
  background: var(--card-bg);
  backdrop-filter: var(--glass-blur);
  border: var(--card-border);
  border-radius: var(--border-radius);
  padding: 30px;
  box-shadow: var(--card-shadow);
  transition: all 0.4s ease;
}

h2 { margin: 0 0 8px 0; font-size: 1.5rem; color: var(--app-text); }
.description { color: var(--app-text-muted); font-size: 0.9rem; margin-bottom: 24px; }

.form { display: flex; flex-direction: column; gap: 24px; }
.input-group { display: flex; flex-direction: column; gap: 8px; }

label {
  font-size: 0.7rem;
  font-weight: 800;
  color: var(--app-text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
}

input {
  padding: 16px;
  background: rgba(0,0,0,0.1);
  border: 1px solid var(--app-border);
  border-radius: calc(var(--border-radius) / 2);
  color: var(--app-text);
  font-size: 1rem;
}

.price-input { position: relative; }
.currency { position: absolute; right: 16px; top: 50%; transform: translateY(-50%); color: var(--app-text-muted); }

.submit-btn {
  padding: 18px;
  background: var(--app-accent);
  color: #000;
  border: none;
  border-radius: calc(var(--border-radius) / 2.5);
  font-size: 0.9rem;
  font-weight: 900;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.submit-btn:disabled { opacity: 0.5; }
</style>
