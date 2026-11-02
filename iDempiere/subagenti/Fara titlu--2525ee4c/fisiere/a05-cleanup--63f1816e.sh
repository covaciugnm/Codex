#!/bin/bash
set -eu
w=/tmp/codex-a05.ObWQES; ct=/home/saga-server/Documents/EvA-Contab/tools/status/containere_test.sh; ses=codex-a05; task=P01.T355
now=$(date -Is); echo "cleanup_start=$now"
for ag in auditor-app auditor-pg; do
  n=$(cat "$w/$ag"); [[ "$n" == eva-test-p01-t355-auditor-* ]]
  [ "$(docker inspect --format '{{index .Config.Labels "eva.sesiune"}}' "$n")" = "$ses" ]
  [ "$(docker inspect --format '{{index .Config.Labels "eva.task"}}' "$n")" = "$task" ]
  echo "verified_own=$n"
  bash "$ct" elibereaza "$n" --sesiune "$ses" --task "$task" --agent "$ag" --runda r1 --executa >"$w/release-$ag.log" 2>&1 || { tail -4 "$w/release-$ag.log"; exit 2; }
  if docker inspect "$n" >/dev/null 2>&1; then
    [ "$(docker inspect --format '{{index .Config.Labels "eva.sesiune"}}' "$n")" = "$ses" ]
    docker stop -t 12 "$n" >/dev/null
    bash "$ct" stare "$n" oprit --nota 'A05 sandbox audit done'
    docker rm -v "$n" >/dev/null
    bash "$ct" stare "$n" sters --nota 'verified codex-a05 owner, synthetic fixture'
  fi
  if docker inspect "$n" >/dev/null 2>&1; then exit 3; fi
  printf 'removed=%s\n' "$n"
done
net=$(cat "$w/net"); [ "$(docker network inspect -f '{{index .Labels "eva.sesiune"}}' "$net")" = "$ses" ]
[ "$(docker network inspect -f '{{len .Containers}}' "$net")" = 0 ]
docker network rm "$net" >/dev/null
rm -f -- "$w/db-secret" "$w/garden-token"
rest=$(docker ps -a --filter label=eva.sesiune=codex-a05 --format '{{.Names}}'|wc -l); printf 'remaining_owned_containers=%s\n' "$rest"
printf 'removed_network=%s\n' "$net"; date -Is
