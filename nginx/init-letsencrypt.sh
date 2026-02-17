#!/bin/bash

# Скрипт для инициализации Let's Encrypt сертификатов

# Закомментирован код certbot, так как сервис отключен
# set -e

# echo "### Запуск certbot для получения сертификатов ###"
# docker-compose -f docker-compose.prod.yml run --rm certbot certonly --webroot --webroot-path=/var/www/certbot --email admin@89.232.177.172.sslip.io --agree-tos --no-eff-email -d 89.232.177.172.sslip.io
# echo "### Перезапуск nginx для применения сертификатов ###"
# docker-compose -f docker-compose.prod.yml restart nginx
# echo "### Готово ###"

echo "### Certbot отключен ###"
echo "### Для использования SSL необходимо настроить альтернативный способ получения сертификатов ###"