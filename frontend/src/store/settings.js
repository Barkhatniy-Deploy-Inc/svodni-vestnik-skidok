import { defineStore } from 'pinia';

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    // 'dark' | 'light'
    themeMode: localStorage.getItem('vestnik_theme') || 'dark',
    // 'glass' | 'material'
    designStyle: localStorage.getItem('vestnik_design') || 'glass',
    isOpen: false
  }),
  actions: {
    toggleTheme() {
      this.themeMode = this.themeMode === 'dark' ? 'light' : 'dark';
      this.saveSettings();
    },
    setDesignStyle(style) {
      this.designStyle = style;
      this.saveSettings();
    },
    toggleSettings() {
      this.isOpen = !this.isOpen;
    },
    saveSettings() {
      localStorage.setItem('vestnik_theme', this.themeMode);
      localStorage.setItem('vestnik_design', this.designStyle);
      this.applyTheme();
    },
    applyTheme() {
      // Применяем классы к body для глобальной смены стилей
      const body = document.body;
      body.classList.remove('theme-dark', 'theme-light', 'design-glass', 'design-material');
      
      body.classList.add(`theme-${this.themeMode}`);
      body.classList.add(`design-${this.designStyle}`);
      
      // Настройка цвета статус-бара Telegram
      if (window.Telegram?.WebApp) {
        const bgColor = this.themeMode === 'dark' ? '#0f172a' : '#f8fafc';
        const secondaryColor = this.themeMode === 'dark' ? '#1e293b' : '#ffffff';
        
        window.Telegram.WebApp.setHeaderColor(this.designStyle === 'glass' ? secondaryColor : bgColor);
        window.Telegram.WebApp.setBackgroundColor(bgColor);
      }
    }
  }
});
