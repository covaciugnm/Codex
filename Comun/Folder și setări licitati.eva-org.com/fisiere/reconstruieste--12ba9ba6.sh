#!/bin/bash
# Reconstruiește și repornește un site. Folosire:  ./reconstruieste.sh dracula-book | schallergasse35 | cesiro1-site | production-site | dracula-design | dracula-food
# (Necesar doar după modificări în backend/, nginx.conf, Dockerfile sau .env — fișierele din public/ sunt live imediat.)
set -e
S="$1"; D="/home/saga-server/site-uri/$S"
[ -f "$D/docker-compose.yml" ] || { echo "Folosire: $0 dracula-book | schallergasse35 | cesiro1-site | production-site | dracula-design | dracula-food | licitatii.eva-org.com"; exit 1; }
cd "$D"; if [ -f docker-compose.cloudflare.yml ]; then docker compose -f docker-compose.yml -f docker-compose.cloudflare.yml up -d --build; else docker compose --profile tunnel up -d --build; fi
sleep 5; docker compose ps --format 'table {{.Name}}\t{{.Status}}'
case "$S" in dracula-book) U=https://dracula-book.com/ ;; schallergasse35) U=https://www.ac-wohnart.at/ ;; cesiro1-site) U=https://cesiro.com/ ;; production-site) U=https://production.cesiro.com/ ;; dracula-design) U=https://dracula-design.com/ ;; dracula-food) U=https://dracula-food.com/ ;; licitatii.eva-org.com) U=https://licitatii.eva-org.com/ ;; esac
echo "Public: $U -> $(curl -s -o /dev/null -w '%{http_code}' -m 15 "$U")"
