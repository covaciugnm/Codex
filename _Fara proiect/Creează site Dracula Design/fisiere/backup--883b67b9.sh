#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
umask 077
mkdir -p backups
target="backups/dracula-$(date +%Y%m%d-%H%M%S).dump"
docker compose exec -T db pg_dump -U dracula_owner -d dracula_design -Fc > "$target"
test -s "$target"
printf 'Backup: %s\n' "$target"
