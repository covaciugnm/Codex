#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
umask 077
if [ ! -f .env ]; then
  printf 'POSTGRES_PASSWORD=%s\nPGAPP_PASSWORD=%s\n' "$(openssl rand -hex 24)" "$(openssl rand -hex 24)" > .env
fi
docker compose up -d --build app
