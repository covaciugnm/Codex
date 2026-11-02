import subprocess,json,datetime,sys
from pathlib import Path
here=Path(__file__).resolve().parent
cmd=['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=5','saga-server@192.168.100.151','docker exec -i eva-postgres-cesiro sh -c \'exec psql -X -qAt -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d idempiere\'']
r=subprocess.run(cmd,input=(here/'meta.sql').read_bytes(),capture_output=True,timeout=22)
obj={'id':'A06-AD-CESIRO','when':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':r.returncode,'error':r.stderr.decode().strip(),'rows':(json.loads(r.stdout.decode()) if r.returncode==0 else None)}
(here/'meta.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8');print(r.returncode, obj['error'],len((obj['rows'] or {}).get('tables',[])))

