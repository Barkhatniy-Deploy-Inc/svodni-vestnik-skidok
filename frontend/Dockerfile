# Stage 1: Сборка
FROM node:22-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Сервер
FROM nginx:alpine

RUN mkdir -p /var/cache/nginx /var/log/nginx /etc/nginx/conf.d /run/nginx && \
    chown -R nginx:nginx /usr/share/nginx/html /var/cache/nginx /var/log/nginx /etc/nginx /run/nginx

# 2. Копируем файлы из stage 1 с флагом --chown, это быстрее и чище
COPY --from=build --chown=nginx:nginx /app/dist /usr/share/nginx/html

# 3. Копируем конфигурацию nginx
COPY --chown=nginx:nginx nginx.conf /etc/nginx/nginx.conf

# 4. Переключаемся на существующего пользователя nginx
USER nginx

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]