#!/usr/bin/env bash
# Chạy trên VPS, trong thư mục repo đã clone:  sudo bash deploy/deploy.sh
set -euo pipefail
DOMAIN="taxisocial.bbl.id.vn"
WEBROOT="/var/www/taxisocial"
CONF="/etc/nginx/sites-available/${DOMAIN}"

mkdir -p "$WEBROOT"
cp public/index.html "$WEBROOT/index.html"
chown -R www-data:www-data "$WEBROOT"

if [ ! -f "$CONF" ]; then
  cp "deploy/nginx-${DOMAIN}.conf" "$CONF"
  ln -sf "$CONF" "/etc/nginx/sites-enabled/${DOMAIN}"
fi
nginx -t && systemctl reload nginx

# Bật HTTPS lần đầu (cần DNS đã trỏ đúng IP VPS)
if ! [ -d "/etc/letsencrypt/live/${DOMAIN}" ]; then
  certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --redirect -m "admin@bbl.id.vn" || \
    echo "Chưa cấp được SSL: kiểm tra DNS rồi chạy lại: certbot --nginx -d $DOMAIN"
fi
echo "Đã deploy: http://${DOMAIN}"
