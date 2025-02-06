#!/bin/bash
docker run -it --rm \
    -v ${CERT_CONF}:/etc/letsencrypt \
    -v ${CERT_WWW}:/var/lib/letsencrypt \
    -p 80:80 \
    certbot/certbot certonly --standalone \
    --agree-tos \
    --email ${CERT_EMAIL} \
    --no-eff-email \
    -d ${CERT_DOMAIN}  # --dry-run