<template>
  <div class="settings-overlay" :class="{ 'open': settingsStore.isOpen }" @click.self="settingsStore.toggleSettings">
    <div class="settings-sheet">
      <div class="drag-handle"></div>
      <h2>{{ t('nav_history') }} & {{ t('app_subtitle') }}</h2>
      
      <!-- Тема: Светлая / Темная -->
      <div class="setting-group">
        <label>Цветовая схема</label>
        <div class="toggle-container">
          <button 
            @click="settingsStore.themeMode = 'light'; settingsStore.saveSettings()"
            :class="{ active: settingsStore.themeMode === 'light' }"
          >🌞 Светлая</button>
          <button 
            @click="settingsStore.themeMode = 'dark'; settingsStore.saveSettings()"
            :class="{ active: settingsStore.themeMode === 'dark' }"
          >🌑 Темная</button>
        </div>
      </div>

      <!-- Стиль дизайна -->
      <div class="setting-group">
        <label>Стиль оформления</label>
        <div class="style-options">
          <div 
            class="style-option" 
            :class="{ active: settingsStore.designStyle === 'glass' }"
            @click="settingsStore.setDesignStyle('glass')"
          >
            <div class="preview glass">Aa</div>
            <span>Glassmorphism</span>
          </div>
          
          <div 
            class="style-option" 
            :class="{ active: settingsStore.designStyle === 'material' }"
            @click="settingsStore.setDesignStyle('material')"
          >
            <div class="preview material">Aa</div>
            <span>Pure Android</span>
          </div>

          <div 
            class="style-option" 
            :class="{ active: settingsStore.designStyle === 'liquid' }"
            @click="settingsStore.setDesignStyle('liquid')"
          >
            <div class="preview liquid">Aa</div>
            <span>Liquid Glass</span>
          </div>
        </div>
      </div>

      <!-- Тональность общения -->
      <div class="setting-group">
        <label>Тон общения (Tone of Voice)</label>
        <div class="tone-options">
          <button 
            @click="settingsStore.setToneOfVoice('ironic')"
            :class="{ active: settingsStore.toneOfVoice === 'ironic' }"
          >🧐 Ироничный</button>
          <button 
            @click="settingsStore.setToneOfVoice('friendly')"
            :class="{ active: settingsStore.toneOfVoice === 'friendly' }"
          >😊 Дружелюбный</button>
          <button 
            @click="settingsStore.setToneOfVoice('hype')"
            :class="{ active: settingsStore.toneOfVoice === 'hype' }"
          >🚀 Хайповый</button>
        </div>
      </div>

      <button class="close-btn" @click="settingsStore.toggleSettings">Готово</button>
    </div>
  </div>
</template>

<script setup>
import { useSettingsStore } from '../store/settings';
import { useTranslation } from '../api/messages';

const settingsStore = useSettingsStore();
const { t } = useTranslation();
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
  border-radius: 30px 30px 0 0;
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
  font-size: 1.1rem;
  color: var(--app-text);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.setting-group {
  margin-bottom: 24px;
}

label {
  display: block;
  margin-bottom: 12px;
  font-size: 0.8rem;
  color: var(--app-text-muted);
  font-weight: 800;
  text-transform: uppercase;
}

.toggle-container, .tone-options {
  display: flex;
  background: rgba(0,0,0,0.1);
  padding: 4px;
  border-radius: 12px;
  gap: 4px;
}

.tone-options {
  flex-direction: column;
}

.toggle-container button, .tone-options button {
  flex: 1;
  border: none;
  background: transparent;
  padding: 10px;
  border-radius: 8px;
  color: var(--app-text-muted);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.toggle-container button {
  text-align: center;
}

.toggle-container button.active, .tone-options button.active {
  background: var(--app-accent);
  color: #000;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.style-options {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
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
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1rem;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.style-option.active .preview {
  border-color: var(--app-accent);
  transform: scale(1.05);
}

.preview.glass {
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255,255,255,0.2);
}

.preview.material {
  background: #211f26;
  border: 1px solid #49454f;
  color: #d0bcff;
}

.preview.liquid {
  background: rgba(28, 28, 30, 0.8);
  border-radius: 18px;
  border: 0.5px solid rgba(255,255,255,0.2);
}

.style-option span {
  font-size: 0.65rem;
  font-weight: 700;
  color: var(--app-text-muted);
  text-align: center;
}

.close-btn {
  width: 100%;
  padding: 16px;
  background: var(--app-text);
  color: var(--app-bg);
  border: none;
  border-radius: 16px;
  font-weight: 900;
  font-size: 0.9rem;
  text-transform: uppercase;
  margin-top: 10px;
}
</style>
