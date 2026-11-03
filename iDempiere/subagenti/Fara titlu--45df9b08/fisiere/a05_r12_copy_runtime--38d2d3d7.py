from pathlib import Path
import subprocess,shlex,hashlib,json,tarfile,datetime
BASE=Path('D:/CodexWork/a05-r12-native-cache')
OUT=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_Nativ_lot02')
archive=BASE/'native-bundles.tar'
assert not archive.exists()
cmd=['docker','exec','eva-idempiere-cesiro','sh','-c',"cd /opt/idempiere/plugins && find . -maxdepth 1 -type f -name '*.jar' ! -name 'com.eva.*' -print0 | tar --null -T - -cf -"]
with archive.open('wb') as f:
    r=subprocess.run(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','saga-server@192.168.100.151',shlex.join(cmd)],stdout=f,stderr=subprocess.PIPE,timeout=240)
assert r.returncode==0,r.stderr.decode(errors='replace')
rows=[]
with tarfile.open(archive) as t:
    for m in t.getmembers():
        assert m.isfile() and m.name.startswith('./') and '/' not in m.name[2:] and m.name.endswith('.jar')
        target=BASE/m.name[2:]
        assert not target.exists()
        data=t.extractfile(m).read()
        target.write_bytes(data)
        rows.append({'name':target.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'SSH docker exec read-only find/tar stdout; native binaries only; no operational configs copied','origin':'eva-idempiere-cesiro:/opt/idempiere/plugins','archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'count':len(rows),'files':rows}
(OUT/'Manifest_binare_native_copiate.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print({'copied':len(rows),'bytes':sum(x['bytes'] for x in rows),'core':[x for x in rows if x['name'].startswith('org.adempiere.base_')],'provider':[x for x in rows if 'postgresql.provider' in x['name']]})
