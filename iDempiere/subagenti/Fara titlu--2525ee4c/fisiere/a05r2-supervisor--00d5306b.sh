#!/bin/bash
set -eu -o pipefail
w=$1; s=eva-contab-codex-a05r2; a=audit; t=P01.T355; ag1=auditor-pg; ag2=auditor-app
rt=/home/saga-server/Documents/EvA-Contab; ct="$rt/tools/status/containere_test.sh"; q="$rt/tools/status/coada_builduri.sh"; occ="$rt/tools/status/ocupare_taskuri.py"
dump=/tmp/codex-a07-handoff-6kab32p2/GardenWorld-A07.dump
[ "$(sha256sum "$dump"|cut -d' ' -f1)" = 54d2a646a663949df78e24206a4dc2a30b7eab609aafba1229c1e6c28e97c6a4 ];[ "$(stat -c '%a' "$dump")" = 600 ]
umask 077; date -Is; echo "verified A07 seed hash + mode"
slot=$(bash "$q" cere "$s" "$a" "$t" --tip suita --pid $$ --asteapta 30 --scop 'R2 A05 AND03 AND04 T366 native ERP');echo "$slot" >"$w/slot";echo "slot=$slot";owned=0;net=eva-test-a05r2-$(basename "$w"|tr -cd 'a-z0-9')
cleanup(){
 set +e
 cd "$w"
 for ag in "$ag2" "$ag1";do
  [ -f "$w/$ag" ] || continue; n=$(cat "$w/$ag")
  if docker inspect "$n" >/dev/null 2>&1;then
   if [ "$(docker inspect --format '{{index .Config.Labels "eva.sesiune"}}' "$n")" != "$s" ];then echo "REFUSED mismatched owner $n";continue;fi
  fi
  bash "$ct" elibereaza "$n" --sesiune "$s" --task "$t" --agent "$ag" --runda r2 --executa >"$w/release-$ag.log" 2>&1
  if docker inspect "$n" >/dev/null 2>&1 && [ "$(docker inspect --format '{{index .Config.Labels "eva.sesiune"}}' "$n")" = "$s" ];then docker stop -t 10 "$n" >/dev/null; bash "$ct" stare "$n" oprit;docker rm -v "$n" >/dev/null;bash "$ct" stare "$n" sters;fi
 done
 if docker network inspect "$net" >/dev/null 2>&1 && [ "$(docker network inspect -f '{{index .Labels "eva.sesiune"}}' "$net")" = "$s" ] && [ "$(docker network inspect -f '{{len .Containers}}' "$net")" = 0 ]; then docker network rm "$net" >/dev/null;fi
 rm -f -- "$w/db-secret" "$w/mobile-lab-secrets.json" "$w/mobile-secrets.json"
 if [ "$owned" = 1 ];then python3 -I "$occ" elibereaza "$t" --sesiune "$s" --motiv 'R2 A05 test cabinet closed' >"$w/release-task" 2>&1;fi
 bash "$q" elibereaza "$slot" >"$w/release-slot" 2>&1
 echo "remaining_owned_containers=$(docker ps -a --filter label=eva.sesiune=$s --format '{{.Names}}'|wc -l)"; date -Is; echo CLEANED
}
trap cleanup EXIT
quote=$(printf '\302\253reia auditul\302\273'); python3 -I "$occ" ocupa "$t" --sesiune "$s" --cont "$a" --cerere "$quote" ;owned=1
bash "$ct" heartbeat-daemon "$s" --pid $$ >"$w/pulse" 2>&1 &
allocate(){
 local img="$1" ag="$2" rc=0 name
 bash "$ct" cere "$s" "$a" "$t" --agent "$ag" --scop 'R2 A05 synthetic WMS native ERP' --imagine "$img" --durata 85 --runda r2 >"$w/sim-$ag" || rc=$?
 grep -E '^DECIZIE|^CE FACI' "$w/sim-$ag" | head -1 >&2;grep -q '^DECIZIE PERMIS ' "$w/sim-$ag" || return 20
 rc=0;bash "$ct" cere "$s" "$a" "$t" --agent "$ag" --scop 'R2 A05 synthetic WMS native ERP' --imagine "$img" --durata 85 --runda r2 --executa >"$w/dec-$ag" || rc=$?
 name=$(awk '/^DECIZIE PERMIS /{print $3}' "$w/dec-$ag"); [[ "$rc" == 10 && "$name" == eva-test-p01-t355-auditor-* ]] || { grep -E '^DECIZIE|^CE FACI' "$w/dec-$ag" >&2;return 20; }
 printf '%s\n' "$name" >"$w/$ag"; printf '%s\n' "$name"
}
pg=$(allocate postgres:16 "$ag1"); id=$(allocate eva-idempiere-rest:r57-20261102 "$ag2")
bash "$rt/tools/teste/retea_test_interna.sh" "$net" --label eva.sesiune="$s" --label eva.task="$t"
ra=$(bash "$ct" run-args "$s" "$a" "$t"|sed -n 1p)
secret=$(openssl rand -hex 20);printf '%s' "$secret">"$w/db-secret"
docker run -d $ra --name "$pg" --network "$net" --network-alias smtp-fixture --memory 1800m --cpus 2 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD="$secret" postgres:16 >/dev/null
docker exec -d "$pg" sh /eva/autostop.sh;bash "$ct" declara "$pg" "$s" "$a" "$t";bash "$ct" stare "$pg" pornit
for i in $(seq 1 65);do if docker exec "$pg" pg_isready -q -U postgres;then break;fi;sleep 1;done
printf "CREATE ROLE adempiere LOGIN PASSWORD '%s';\nCREATE DATABASE idempiere OWNER adempiere;\n" "$secret" |docker exec -i "$pg" psql -v ON_ERROR_STOP=1 -U postgres -d postgres >/dev/null
docker exec -i "$pg" pg_restore --exit-on-error --no-owner --no-privileges --role=adempiere -U postgres -d idempiere <"$dump" >"$w/restore.out" 2>"$w/restore.err"
docker exec -i "$pg" psql -U postgres -d idempiere -v ON_ERROR_STOP=1 -At <<'SQL'
CREATE OR REPLACE FUNCTION adempiere.a05r2_no_scheduler() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN NEW.isactive='N'; RETURN NEW; END $$;
CREATE TRIGGER a05r2_no_scheduler BEFORE INSERT OR UPDATE OF isactive ON adempiere.ad_scheduler FOR EACH ROW EXECUTE FUNCTION adempiere.a05r2_no_scheduler();
UPDATE adempiere.ad_scheduler SET isactive='N' WHERE isactive='Y';
SELECT 'schedulers/foreign clients', (SELECT count(*) FROM adempiere.ad_scheduler WHERE isactive='Y'),(SELECT count(*) FROM adempiere.ad_client WHERE ad_client_id NOT IN(0,11));
DO $$BEGIN IF EXISTS(SELECT FROM adempiere.ad_client WHERE ad_client_id NOT IN(0,11)) THEN RAISE EXCEPTION 'foreign client'; END IF;END$$;
SQL
docker run -d $ra --name "$id" --network "$net" --memory 3500m --cpus 2 -e DB_HOST="$pg" -e DB_PORT=5432 -e DB_USER=adempiere -e DB_NAME=idempiere -e DB_PASS="$secret" -e DB_ADMIN_PASS="$secret" -e MAIL_HOST=smtp-fixture eva-idempiere-rest:r57-20261102 >/dev/null
docker exec -d "$id" sh /eva/autostop.sh;bash "$ct" declara "$id" "$s" "$a" "$t";bash "$ct" stare "$id" pornit
ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$id");echo "$ip">"$w/ip"
for i in $(seq 1 90);do rc=$(curl --noproxy '*' -ks --max-time 3 -o /dev/null -w '%{http_code}' "https://$ip:8443/webui/" || true);[ "$rc" = 200 ] && break;sleep 2;done
echo "webui=$rc clone_ip=$ip";test "$rc" = 200;printf 'READY %s\n' "$(date -Is)" >"$w/ready"
for i in $(seq 1 960);do [ -e "$w/finish" ] && break;sleep 5;done

