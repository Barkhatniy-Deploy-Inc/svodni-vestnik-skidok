# Implementation Plan: Система тем и тональностей общения

Этот план описывает этапы реализации динамического интерфейса.

## Фаза 1: Инфраструктура настроек
- [ ] Task: Обновить `frontend/src/store/settings.js` для поддержки новых параметров.
- [ ] Task: Реализовать сохранение/загрузку из `localStorage`.
- [ ] Task: Conductor - User Manual Verification 'Фаза 1: Инфраструктура настроек' (Protocol in workflow.md)

## Фаза 2: Визуальные стили (CSS)
- [ ] Task: Определить наборы CSS-переменных для Glassmorphism, Pure Android и Liquid Glass.
- [ ] Task: Реализовать переключение классов на корневом элементе `App.vue`.
- [ ] Task: Добавить "Bad UX" эффект размытия при наведении в глобальные стили.
- [ ] Task: Conductor - User Manual Verification 'Фаза 2: Визуальные стили (CSS)' (Protocol in workflow.md)

## Фаза 3: Тональность общения (ToV)
- [ ] Task: Создать файл констант `frontend/src/api/messages.js` со всеми строками интерфейса для трех режимов.
- [ ] Task: Реализовать хук или глобальную функцию `t(key)` для получения строки в текущем тоне.
- [ ] Task: Заменить статические строки в `Dashboard.vue` и `AddItem.vue` на вызовы `t()`.
- [ ] Task: Conductor - User Manual Verification 'Фаза 3: Тональность общения (ToV)' (Protocol in workflow.md)

## Фаза 4: Пользовательский интерфейс и Финализация
- [ ] Task: Обновить `SettingsModal.vue`, добавив выбор стиля и тона.
- [ ] Task: Проверить корректность отображения всех 9 комбинаций (3 стиля x 3 тона).
- [ ] Task: Conductor - User Manual Verification 'Фаза 4: Пользовательский интерфейс и Финализация' (Protocol in workflow.md)
