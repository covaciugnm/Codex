from pathlib import Path
import subprocess,shlex,tarfile,io,zipfile,hashlib,json
CACHE=Path('D:/CodexWork/a05-r12-native-cache')
name='org.apache.ant_1.10.12.v20211102-1452'
cmd=['docker','exec','eva-idempiere-cesiro','tar','-C','/opt/idempiere/plugins/'+name,'-cf','-','.']
r=subprocess.run(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','saga-server@192.168.100.151',shlex.join(cmd)],capture_output=True,timeout=60)
assert r.returncode==0,r.stderr.decode()
rows=[]
target=CACHE/(name+'.jar')
assert not target.exists()
with tarfile.open(fileobj=io.BytesIO(r.stdout)) as t,zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
 for m in t.getmembers():
  if not m.isfile():continue
  rel=m.name.removeprefix('./')
  assert not rel.startswith('/') and '..' not in Path(rel).parts
  data=t.extractfile(m).read();z.writestr(rel,data)
  rows.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
report={'origin':name,'operation':'Directory bundle read-only tar then local ZIP; original entry bytes preserved, container not modified','sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'files':rows}
out=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_Nativ_lot02')
(out/'Manifest_bundle_Ant.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print({'files':len(rows),'sha256':report['sha256']})
