#!/bin/bash

# Скрипт для инициализации Let's Encrypt сертификатов

set -e

echo "### Запуск certbot для получения сертификатов ###"
docker-compose -f docker-compose.prod.yml run --rm certbot certonly --webroot --webroot-path=/var/www/certbot --email admin@158.255.1.190.sslip.io --agree-tos --no-eff-email -d 158.255.1.190.sslip.io
echo "### Перезапуск nginx для применения сертификатов ###"
docker-compose -f docker-compose.prod.yml restart nginx
echo "### Готово ###"