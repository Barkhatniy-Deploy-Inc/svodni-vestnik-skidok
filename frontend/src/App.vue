<template>
  <div class="app-container">
    <div class="ambient-orb orb-1"></div>
    <div class="ambient-orb orb-2"></div>
    
    <header class="header">
      <div class="header-content">
        <div class="logo-area">
          <h1>Вестник</h1>
          <p class="subtitle">мониторинг 24/7</p>
        </div>
        <button class="settings-btn" @click="settingsStore.toggleSettings">
          ⚙️
        </button>
      </div>
      <div class="logo-glow"></div>
    </header>
    
    <main class="content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <nav class="nav-bar">
      <router-link to="/" class="nav-item">
        <span class="icon">📊</span>
        Летопись
      </router-link>
      <router-link to="/add" class="nav-item">
        <span class="icon">➕</span>
        Поручение
      </router-link>
    </nav>

    <!-- Модальное окно настроек -->
    <SettingsModal />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useSettingsStore } from './store/settings';
import SettingsModal from './components/SettingsModal.vue';

const settingsStore = useSettingsStore();

onMounted(() => {
  // Применяем сохраненную тему при запуске
  settingsStore.applyTheme();
});
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  max-width: 500px;
  margin: 0 auto;
  position: relative;
  overflow-x: hidden;
  overflow-y: hidden; /* Чтобы шары не расширяли скролл */
}

/* ФОНОВЫЕ ОРБЫ */
.ambient-orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 0;
  animation: float 20s infinite ease-in-out;
  opacity: 0.6;
}

.orb-1 {
  top: -10%;
  left: -10%;
  width: 300px;
  height: 300px;
  background: var(--app-accent);
}

.orb-2 {
  bottom: 10%;
  right: -20%;
  width: 400px;
  height: 400px;
  background: #10b981; /* Зеленоватый оттенок */
  animation-delay: -10s;
}

@keyframes float {
  0% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, 50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0, 0) scale(1); }
}

.header {
  padding: 20px 24px 10px;
  position: relative;
  z-index: 10;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 2;
}

.logo-glow {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  width: 150px;
  height: 80px;
  background: var(--app-accent);
  filter: blur(60px);
  opacity: 0.2;
  z-index: 1;
  pointer-events: none;
}

h1 {
  font-size: 1.6rem;
  margin: 0;
  color: var(--app-text);
  font-weight: 800;
}

.subtitle {
  font-size: 0.75rem;
  color: var(--app-text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 2px;
}

.settings-btn {
  background: var(--card-bg);
  backdrop-filter: var(--glass-blur);
  border: var(--card-border);
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  cursor: pointer;
  box-shadow: var(--card-shadow);
  color: var(--app-text);
}

.content {
  flex: 1;
  padding: 16px;
  padding-bottom: 100px;
}

.nav-bar {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  width: calc(100% - 48px);
  max-width: 400px;
  display: flex;
  justify-content: space-around;
  padding: 14px;
  background: var(--nav-bg);
  backdrop-filter: var(--glass-blur);
  border: var(--card-border);
  border-radius: var(--border-radius);
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
  z-index: 100;
}

.nav-item {
  text-decoration: none;
  color: var(--app-text-muted);
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
}

.icon {
  font-size: 1.25rem;
  opacity: 0.7;
  transition: all 0.3s ease;
}

.router-link-active {
  color: var(--app-accent);
}

.router-link-active .icon {
  opacity: 1;
  transform: translateY(-2px);
}

/* Анимация страниц */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>