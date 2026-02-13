# Инструкция по развертыванию приложения

## Требования к окружению

- Docker
- Docker Compose
- Доступ к VPS по SSH
- Доменное имя (в данном случае используется sslip.io: 158.255.1.190.sslip.io)

## Настройка Secrets для GitHub Actions

Для работы CI/CD pipeline необходимо настроить следующие Secrets в репозитории GitHub:

1. `VPS_IP` - IP адрес вашего VPS (158.255.1.190)
2. `VPS_USER` - Имя пользователя для подключения к VPS
3. `SSH_KEY` - Приватный SSH ключ для подключения к VPS

### Как настроить Secrets в GitHub:

1. Перейдите в настройки репозитория (Settings)
2. В левом меню выберите "Secrets and variables" → "Actions"
3. Нажмите "New repository secret"
4. Введите имя секрета и его значение
5. Повторите для всех необходимых секретов

## Локальное развертывание

Для локального запуска приложения используйте следующую команду:

```bash
docker-compose up --build
```

## Production развертывание

Для развертывания в production среде используйте следующую команду:

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

После запуска контейнеров необходимо инициализировать Let's Encrypt сертификаты:

```bash
./nginx/init-letsencrypt.sh
```

## Структура проекта

```
.
├── backend/                 # Бэкенд приложение (FastAPI)
│   ├── Dockerfile           # Dockerfile для бэкенда
│   ├── .dockerignore       # Игнорируемые файлы для Docker
│   └── ...                  # Исходный код бэкенда
├── frontend/                # Фронтенд приложение (Vue.js)
│   ├── Dockerfile           # Dockerfile для фронтенда
│   ├── .dockerignore        # Игнорируемые файлы для Docker
│   └── ...                  # Исходный код фронтенда
├── nginx/                   # Конфигурация Nginx
│   ├── nginx.conf           # Конфигурационный файл Nginx
│   └── init-letsencrypt.sh   # Скрипт для инициализации SSL сертификатов
├── .github/workflows/      # GitHub Actions workflows
│   └── ci-cd-ghrc.yml       # CI/CD pipeline с использованием GHRC
├── docker-compose.yml        # Конфигурация для локальной разработки
├── docker-compose.prod.yml  # Конфигурация для production с использованием GHRC
└── docker-compose.prod.ghrc.yml  # Шаблон конфигурации для production с GHRC
```

## Обслуживание

### Обновление SSL сертификатов

Сертификаты Let's Encrypt действительны 90 дней. Для автоматического обновления сертификатов можно настроить cron job на сервере:

```bash
# Добавить в crontab (crontab -e)
0 12 * * * /home/user/svodni-vestnik/nginx/init-letsencrypt.sh
```

### Мониторинг

Проверка состояния контейнеров:

```bash
docker-compose -f docker-compose.prod.yml ps
```

Просмотр логов:

```bash
# Логи бэкенда
docker-compose -f docker-compose.prod.yml logs backend

# Логи фронтенда
docker-compose -f docker-compose.prod.yml logs frontend

# Логи Nginx
docker-compose -f docker-compose.prod.yml logs nginx