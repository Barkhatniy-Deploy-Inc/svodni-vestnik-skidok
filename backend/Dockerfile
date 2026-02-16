# Multi-stage build для backend
# Stage 1: Сборка зависимостей
FROM python:3.10-alpine as builder

WORKDIR /app

# Установка зависимостей для сборки пакетов
RUN apk add --no-cache gcc musl-dev libffi-dev

# Копируем requirements
COPY requirements.txt .

# Создаем виртуальное окружение и устанавливаем зависимости
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.10-alpine

WORKDIR /app

# Копируем виртуальное окружение из builder stage
COPY --from=builder /opt/venv /opt/venv

# Устанавливаем PATH для использования виртуального окружения
ENV PATH="/opt/venv/bin:$PATH"

# Создаем пользователя для запуска приложения
RUN addgroup -g 1001 -S app &&\
    adduser -u 1001 -S app -G app

# Копируем исходный код
COPY . .

# Меняем владельца файлов на пользователя app
RUN chown -R app:app /app

# Переключаемся на пользователя app
USER app

# Создаем папку для базы данных и логов
RUN mkdir -p /app/data /app/logs && \
    touch /app/logs/app.log && \
    chown -R app:app /app/data /app/logs

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
