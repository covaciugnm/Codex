from pathlib import Path
import subprocess,os,hashlib,json,io
G=Path('D:/CodexWork/eva-audit-p01-src-20261101');D=Path('D:/CodexWork/a01-r11-hr-frozen');D.mkdir(exist_ok=True)
head='2fe90ed3f128c33dff7cf9f8674e664a70679390';env={**os.environ,'GIT_NO_LAZY_FETCH':'1','GIT_TERMINAL_PROMPT':'0'}
prefix='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/fiscal/'
paths=['backend','scripts/legislatie/extrage_registru.py',prefix+'ParametriModel.java',prefix+'ObligatieD392.java',prefix+'res/t63_l1_parametri.tsv']
tree=subprocess.check_output(['git','-C',str(G),'ls-tree','-r','-z',head,'--',*paths],env=env)
rows=[]
for line in tree.split(b'\0'):
 if not line:continue
meta=[]
for line in tree.split(b'\0'):
 if line:
  a,p=line.split(b'\t',1);mode,kind,oid=a.decode().split();assert kind=='blob';meta.append((p.decode(),oid))
for i in range(0,len(meta),50):
 group=meta[i:i+50];raw=subprocess.check_output(['git','-C',str(G),'cat-file','--batch'],input=('\n'.join(oid for _,oid in group)+'\n').encode(),env=env);stream=io.BytesIO(raw)
 for path,oid in group:
  roid,kind,size=stream.readline().decode().split();b=stream.read(int(size));assert stream.read(1)==b'\n';assert roid==oid and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid
  p=D/path;p.parent.mkdir(exist_ok=True,parents=True);p.write_bytes(b);rows.append({'path':path,'oid':oid,'sha256':hashlib.sha256(b).hexdigest()})
(D/'source_manifest.json').write_text(json.dumps({'head':head,'files':rows},indent=2),encoding='utf8');print('materialized',len(rows))
