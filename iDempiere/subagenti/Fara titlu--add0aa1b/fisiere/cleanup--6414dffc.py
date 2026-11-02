import json,subprocess,datetime,os,re,hashlib
from pathlib import Path
h=Path(__file__).resolve().parent;w=(h/'remote.txt').read_text().strip();assert re.fullmatch(r'/tmp/eva-contab-codex-ex05\.[A-Za-z0-9]{8}',w)
p=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/supliment_CESIRO1/probe');host='saga-server@192.168.100.151';ssh=['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',host]
lines=subprocess.check_output(ssh+['cd '+w+' && tail -4 events.log && cat release-slot && docker ps -aq --filter label=eva.sesiune=eva-contab-codex-p01ex05r1 |wc -l && docker network ls --filter label=eva.sesiune=eva-contab-codex-p01ex05r1 --format "{{.Name}}" |wc -l && test ! -f sourcekey && test ! -f cursorkey && echo ephemeral-secrets-removed'],text=True).splitlines()
assert 'CLEANED' in lines and 'ephemeral-secrets-removed' in lines and lines[-3:-1]==['0','0'],lines
dbs=[json.loads((h/'cursor-seed.json').read_text())['db'],json.loads((p/'EX04-evidence/wire.json').read_text())['fixture_database']]
assert all(re.fullmatch('cesiro_ex_[0-9a-f]{8}',i) for i in dbs)
rc=subprocess.check_output(['D:/CodexWork/p01-local-pg16/pgsql/bin/psql.exe','-wXAt','-h','127.0.0.1','-p','56481','-U','audit_owner','-d','postgres','-c',"select count(*) from pg_database where datname in ('"+"','".join(dbs)+"')"],env={**os.environ,'PGPASSFILE':'D:/CodexWork/p01-local-pg16/pgpass.conf'},text=True).strip();assert rc=='0'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
out=p/'EX04_EX05_cleanup.json';assert not out.exists()
out.write_text(json.dumps({'subject':['EX04','EX05'],'subject_hashes':{n:sha(p/(n+'.json')) for n in ['EX04','EX05']},'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner':'eva-contab-codex-p01ex05r1','cubicle':'P01.T220 GardenWorld synthetic','server_clean_report':lines,'ended_fixture_databases':dbs,'still_existing':int(rc),'other_database':'A08 synthetic a08_cesiro read-only: original fixture preserved, no changes from A06 gateway.'},indent=2),encoding='utf8');print(sha(out),lines,rc)

