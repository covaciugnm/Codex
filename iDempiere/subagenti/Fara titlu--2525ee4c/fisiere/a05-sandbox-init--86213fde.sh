#!/usr/bin/env bash
set -eu -o pipefail
w="$1"; s=codex-a05; a=audit; t=P01.T355; rt=/home/saga-server/Documents/EvA-Contab; ct="$rt/tools/status/containere_test.sh"; net=eva-test-codex-a05-$(basename "$w" | tr -cd 'a-z0-9'); printf '%s\n' "$net" > "$w/net"
allocate() {
 local img="$1" ag="$2" out rc name
 rc=0; bash "$ct" cere "$s" "$a" "$t" --agent "$ag" --scop 'WMS native ERP synthetic audit' --imagine "$img" --durata 45 --runda r1 >"$w/sim-$ag" || rc=$?
 grep -E '^DECIZIE|^CE FACI' "$w/sim-$ag" | head -1 >&2
 grep -q '^DECIZIE PERMIS ' "$w/sim-$ag" || return 20
 rc=0; bash "$ct" cere "$s" "$a" "$t" --agent "$ag" --scop 'WMS native ERP synthetic audit' --imagine "$img" --durata 45 --runda r1 --executa >"$w/dec-$ag" || rc=$?
 name=$(awk '/^DECIZIE PERMIS /{print $3}' "$w/dec-$ag")
 [[ "$rc" == 10 && "$name" == eva-test-p01-t355-auditor-* ]] || { grep -E '^DECIZIE|^CE FACI' "$w/dec-$ag" >&2; return 20; }
 printf '%s\n' "$name" >"$w/$ag"; printf '%s\n' "$name"
}
pg=$(allocate postgres:16 auditor-pg)
id=$(allocate eva-idempiere-rest:13 auditor-app)
bash "$rt/tools/teste/retea_test_interna.sh" "$net" --label eva.sesiune="$s" --label eva.task="$t"
ra=$(bash "$ct" run-args "$s" "$a" "$t" | sed -n 1p)
secret=$(openssl rand -hex 20); umask 077
printf '%s' "$secret" >"$w/db-secret"
docker run -d $ra --name "$pg" --network "$net" --memory 1800m --cpus 2 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD="$secret" postgres:16 >/dev/null
docker exec -d "$pg" sh /eva/autostop.sh
bash "$ct" declara "$pg" "$s" "$a" "$t"; bash "$ct" stare "$pg" pornit
for i in $(seq 1 45); do if docker exec "$pg" pg_isready -q -U postgres; then break; fi; sleep 1; done
printf "CREATE ROLE adempiere LOGIN PASSWORD '%s';\nCREATE DATABASE idempiere OWNER adempiere;\n" "$secret" | docker exec -i "$pg" psql -v ON_ERROR_STOP=1 -U postgres -d postgres >/dev/null
docker exec eva-idempiere-cesiro sh -c "unzip -p /opt/idempiere/data/seed/Adempiere_pg.jar Adempiere_pg.dmp" | docker exec -i "$pg" psql -v ON_ERROR_STOP=1 -q -U postgres -d idempiere >"$w/seed.out" 2>"$w/seed.err"
docker exec "$pg" psql -v ON_ERROR_STOP=1 -U postgres -d idempiere -c "UPDATE adempiere.ad_scheduler SET isactive='N'; SELECT name FROM adempiere.ad_client WHERE ad_client_id>0; SELECT count(*) AS active_schedulers FROM adempiere.ad_scheduler WHERE isactive='Y';"
# Keep only tested binary JARs, no mounts of production database, home or external credentials.
mkdir -m 700 "$w/bundles"; for f in contab saga.native saga.theme; do src=/opt/idempiere/plugins/com.eva.ro.$f'_13.0.0.jar'; docker cp eva-idempiere-cesiro:"$src" "$w/bundles/" >/dev/null; done
docker run -d $ra --name "$id" --network "$net" --memory 3100m --cpus 2 -e DB_HOST="$pg" -e DB_PORT=5432 -e DB_USER=adempiere -e DB_NAME=idempiere -e DB_PASS="$secret" -e DB_ADMIN_PASS="$secret" -e MAIL_HOST=disabled.invalid -v "$w/bundles/com.eva.ro.contab_13.0.0.jar:/opt/idempiere/plugins/com.eva.ro.contab_13.0.0.jar:ro" -v "$w/bundles/com.eva.ro.saga.native_13.0.0.jar:/opt/idempiere/plugins/com.eva.ro.saga.native_13.0.0.jar:ro" -v "$w/bundles/com.eva.ro.saga.theme_13.0.0.jar:/opt/idempiere/plugins/com.eva.ro.saga.theme_13.0.0.jar:ro" eva-idempiere-rest:13 >/dev/null
docker exec -d "$id" sh /eva/autostop.sh; bash "$ct" declara "$id" "$s" "$a" "$t"; bash "$ct" stare "$id" pornit
ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$id")
printf '%s\n' "$ip" > "$w/ip"
for i in $(seq 1 75); do rc=$(curl --max-time 2 --silent --output /dev/null --write-out '%{http_code}' "http://$ip:8080/webui/" || true); if [[ $rc == 200 || $rc == 302 ]]; then echo "webui_http=$rc"; date -Is; exit 0; fi; sleep 2; done
echo 'webui_unavailable'; exit 11
