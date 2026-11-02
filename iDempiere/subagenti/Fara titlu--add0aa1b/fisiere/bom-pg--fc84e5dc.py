import datetime,json,subprocess,re
from pathlib import Path
here=Path(__file__).resolve().parent
sql=(here/'installed-query.sql').read_text(encoding='utf-8-sig').strip()
args=iter(["'NONBIZ-PREFIX'","11","101","-1","true","'REZERVAT'","false","'EXCLUS'"])
rendered=re.sub(r'\?',lambda _: next(args),sql)
ddl=(here/'history.py').read_text(encoding='utf8').split('db.executescript("""')[1].split('""")')[0]
psql=ddl+'\nSELECT '+"""json_build_object('case','v1','value', ("""+rendered+"));\nUPDATE pp_product_bomline SET qtybom=3 WHERE pp_product_bom_id=1;\nSELECT json_build_object('case','modified','value', ("+rendered+"));\nUPDATE pp_product_bom SET isactive='N' WHERE pp_product_bom_id=1;\nSELECT json_build_object('case','inactive','value', ("+rendered+"));\n"
(here/'bom-pg.sql').write_text(psql,encoding='utf8')
sh="""set -eu
queue=/home/saga-server/Documents/EvA-Contab/tools/status/coada_builduri.sh
slot=$("$queue" cere codex-a06-audit codex P01.T354 --tip suita --pid $$ --scop 'A06 SQL istoric BOM izolat') || exit $?
container=''; cleanup(){ if [ -n "$container" ] && [ "$(docker inspect -f '{{index .Config.Labels "eva.audit.owner"}}' "$container" 2>/dev/null)" = 'codex-a06-20261102' ]; then docker rm -f -v "$container" >/dev/null; fi; "$queue" elibereaza "$slot" >&2; }
trap cleanup EXIT; trap 'exit 130' INT TERM
container=$(docker run --detach --network none --label eva.audit.owner=codex-a06-20261102 --label eva.audit.scope=P01.T354 --tmpfs /var/lib/postgresql/data:rw,size=512m --cpus=1 --memory=768m -e POSTGRES_HOST_AUTH_METHOD=trust postgres:16)
echo "FIXTURE=$container"
for n in $(seq 1 25); do docker exec "$container" pg_isready -U postgres >/dev/null 2>&1 && break; sleep 1; done
docker exec -i "$container" psql -X -qAt -U postgres -d postgres -v ON_ERROR_STOP=1 <<'TESTSQL'
"""+psql+"\nTESTSQL\n"
r=subprocess.run(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=5','saga-server@192.168.100.151','bash -s'],input=sh.encode(),capture_output=True,timeout=70)
data={'id':'A06-BOM-PG','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':r.returncode,'stderr':r.stderr.decode(),'stdout':r.stdout.decode(),'scope':'§61 slot and own empty tmpfs/network=none PG16 fixture only. No production data.'}
(here/'bom-pg.json').write_text(json.dumps(data,indent=2),encoding='utf8');print(json.dumps(data))

