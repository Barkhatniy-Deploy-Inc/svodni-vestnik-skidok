#!/bin/bash

# Скрипт для инициализации Let's Encrypt сертификатов

# set -e

echo "### Запуск certbot для получения сертификатов ###"
docker compose -f ../docker-compose.prod.ghrc.yml run --rm certbot certonly --webroot --webroot-path=/var/www/certbot --email admin@89.232.177.172.sslip.io --agree-tos --no-eff-email -d 89.232.177.172.sslip.io
echo "### Перезапуск nginx для применения сертификатов ###"
# docker compose -f ../docker-compose.prod.ghrc.yml restart nginx
echo "### Готово ###"