#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
python3 ops/prepare.py
docker compose config --quiet
docker compose up -d --build
docker compose ps
printf '\nDracula Design: http://127.0.0.1:4181\nAdministration: http://127.0.0.1:4181/admin/\n'
