#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
docker compose -f docker-compose.yml -f docker-compose.cloudflare.yml config --quiet
docker compose -f docker-compose.yml -f docker-compose.cloudflare.yml up -d --build
docker compose -f docker-compose.yml -f docker-compose.cloudflare.yml ps
