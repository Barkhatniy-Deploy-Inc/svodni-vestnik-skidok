<template>
  <div class="settings-overlay" :class="{ 'open': settingsStore.isOpen }" @click.self="settingsStore.toggleSettings">
    <div class="settings-sheet">
      <div class="drag-handle"></div>
      <h2>Настройки Вида</h2>
      
      <div class="setting-group">
        <label>Режим</label>
        <div class="toggle-container">
          <button 
            @click="settingsStore.themeMode = 'light'; settingsStore.saveSettings()"
            :class="{ active: settingsStore.themeMode === 'light' }"
          >🌞 Свет</button>
          <button 
            @click="settingsStore.themeMode = 'dark'; settingsStore.saveSettings()"
            :class="{ active: settingsStore.themeMode === 'dark' }"
          >🌑 Тьма</button>
        </div>
      </div>

      <div class="setting-group">
        <label>Стиль Дизайна</label>
        <div class="style-options">
          <div 
            class="style-option" 
            :class="{ active: settingsStore.designStyle === 'glass' }"
            @click="settingsStore.setDesignStyle('glass')"
          >
            <div class="preview glass">Aa</div>
            <span>Liquid Glass</span>
          </div>
          
          <div 
            class="style-option" 
            :class="{ active: settingsStore.designStyle === 'material' }"
            @click="settingsStore.setDesignStyle('material')"
          >
            <div class="preview material">Aa</div>
            <span>Material 3</span>
          </div>
        </div>
      </div>

      <button class="close-btn" @click="settingsStore.toggleSettings">Готово</button>
    </div>
  </div>
</template>

<script setup>
import { useSettingsStore } from '../store/settings';
const settingsStore = useSettingsStore();
</script>

<style scoped>
.settings-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 1000;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.settings-overlay.open {
  opacity: 1;
  pointer-events: all;
}

.settings-sheet {
  background: var(--card-bg);
  backdrop-filter: var(--glass-blur);
  width: 100%;
  max-width: 500px;
  border-radius: 24px 24px 0 0;
  padding: 24px;
  border-top: var(--card-border);
  transform: translateY(100%);
  transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
  box-shadow: 0 -10px 40px rgba(0,0,0,0.2);
}

.settings-overlay.open .settings-sheet {
  transform: translateY(0);
}

.drag-handle {
  width: 40px;
  height: 4px;
  background: var(--app-border);
  border-radius: 2px;
  margin: 0 auto 20px;
}

h2 {
  text-align: center;
  margin-bottom: 24px;
  font-size: 1.2rem;
  color: var(--app-text);
}

.setting-group {
  margin-bottom: 24px;
}

label {
  display: block;
  margin-bottom: 12px;
  font-size: 0.9rem;
  color: var(--app-text-muted);
  font-weight: 600;
}

.toggle-container {
  display: flex;
  background: var(--input-bg);
  padding: 4px;
  border-radius: 12px;
}

.toggle-container button {
  flex: 1;
  border: none;
  background: transparent;
  padding: 10px;
  border-radius: 8px;
  color: var(--app-text-muted);
  font-weight: 600;
  cursor: pointer;
}

.toggle-container button.active {
  background: var(--app-bg);
  color: var(--app-text);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.style-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.style-option {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.preview {
  width: 100%;
  height: 80px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.style-option.active .preview {
  border-color: var(--app-accent);
}

.preview.glass {
  background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.2);
}

.preview.material {
  background: var(--app-bg);
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

span {
  font-size: 0.8rem;
  color: var(--app-text);
}

.close-btn {
  width: 100%;
  padding: 16px;
  background: var(--app-accent);
  color: #fff;
  border: none;
  border-radius: 16px;
  font-weight: bold;
  font-size: 1rem;
  margin-top: 10px;
}
</style>
