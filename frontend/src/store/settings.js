import { defineStore } from 'pinia';

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    // Режим темы: 'dark' | 'light'
    themeMode: localStorage.getItem('vestnik_theme') || 'dark',
    // Стиль оформления: 'glass' | 'material' | 'liquid'
    designStyle: localStorage.getItem('vestnik_design') || 'glass',
    // Тональность общения: 'ironic' | 'friendly' | 'hype'
    toneOfVoice: localStorage.getItem('vestnik_tone') || 'friendly',
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
    setToneOfVoice(tone) {
      this.toneOfVoice = tone;
      this.saveSettings();
    },
    toggleSettings() {
      this.isOpen = !this.isOpen;
    },
    saveSettings() {
      localStorage.setItem('vestnik_theme', this.themeMode);
      localStorage.setItem('vestnik_design', this.designStyle);
      localStorage.setItem('vestnik_tone', this.toneOfVoice);
      this.applyTheme();
    },
    applyTheme() {
      // Применяем классы к body для глобальной смены стилей
      const body = document.body;
      body.classList.remove(
        'theme-dark', 'theme-light', 
        'design-glass', 'design-material', 'design-liquid',
        'tone-ironic', 'tone-friendly', 'tone-hype'
      );
      
      body.classList.add(`theme-${this.themeMode}`);
      body.classList.add(`design-${this.designStyle}`);
      body.classList.add(`tone-${this.toneOfVoice}`);
      
      // Настройка цветов Telegram SDK
      if (window.Telegram?.WebApp) {
        const bgColor = this.themeMode === 'dark' ? '#0f172a' : '#f8fafc';
        const secondaryColor = this.themeMode === 'dark' ? '#1e293b' : '#ffffff';
        
        // В стиле Liquid Glass (iOS) используем более светлые заголовки
        const headerColor = this.designStyle === 'liquid' ? secondaryColor : bgColor;
        
        window.Telegram.WebApp.setHeaderColor(headerColor);
        window.Telegram.WebApp.setBackgroundColor(bgColor);
      }
    }
  }
});
