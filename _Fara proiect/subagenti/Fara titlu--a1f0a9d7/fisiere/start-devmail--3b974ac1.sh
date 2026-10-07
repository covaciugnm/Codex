#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
python3 ops/prepare.py
docker compose -f docker-compose.yml -f docker-compose.devmail.yml config --quiet
docker compose -f docker-compose.yml -f docker-compose.devmail.yml build backend
docker compose -f docker-compose.yml -f docker-compose.devmail.yml run --rm --no-deps backend python seed_email_content.py
docker compose -f docker-compose.yml -f docker-compose.devmail.yml up -d --wait --wait-timeout 120 --no-deps backend mailpit mail-worker
docker compose exec -T admin nginx -s reload
docker compose -f docker-compose.yml -f docker-compose.devmail.yml ps
