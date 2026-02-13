# Multi-stage build для frontend
# Stage 1: Сборка
FROM node:18-alpine as build

WORKDIR /app

# Копируем package файлы
COPY package*.json ./

# Устанавливаем зависимости
RUN npm ci

# Копируем исходный код
COPY . .

# Собираем приложение
RUN npm run build

# Stage 2: Сервер
FROM nginx:alpine

# Создаем пользователя для запуска nginx
RUN addgroup -g 1001 -S nginx && \
    adduser -S -D -H -u 1001 -G nginx nginx

# Копируем собранные файлы из stage 1
COPY --from=build /app/dist /usr/share/nginx/html

# Меняем владельца файлов на пользователя nginx
RUN chown -R nginx:nginx /usr/share/nginx/html

# Копируем конфигурацию nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Меняем владельца конфигурационных файлов на пользователя nginx
RUN chown -R nginx:nginx /etc/nginx

# Переключаемся на пользователя nginx
USER nginx

# Открываем порт 80
EXPOSE 80

# Запускаем nginx
CMD ["nginx", "-g", "daemon off;"]