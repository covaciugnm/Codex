from a12_r11x_base import *
from shlex import quote
from pathlib import PurePosixPath
cont='idempiere/plugins/com.eva.ro.contab/';saga='idempiere/plugins/com.eva.ro.saga.native/'
tests=['TestComparatieSaga','TestComparatieSagaEcran','TestT201Registre','TestT201Ecrane','TestT257Repostare']
paths=[cont+'com.eva.ro.contab_13.0.0.jar',cont+'src',cont+'test/fixtures/banca',*[cont+'test/'+s+'.java'for s in tests],saga+'lib/sqlite-jdbc.jar',saga+'com.eva.ro.saga.native_13.0.0.jar']
cmd="git -C /home/saga-server/Documents/EvA-Contab archive --format=tar.gz "+head+' -- '+' '.join(quote(p)for p in paths);res=sp.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151',cmd],capture_output=True,timeout=120);assert res.returncode==0,res.stderr.decode()[-400:]
items=[]
with tarfile.open(fileobj=io.BytesIO(res.stdout),mode='r:gz') as arc:
 for m in arc.getmembers():
  if not m.isfile():continue
  p=PurePosixPath(m.name);assert not p.is_absolute()and '..'not in p.parts
  body=arc.extractfile(m).read(); oid=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest();assert catalog[p.as_posix()]['git_object']==oid
  out=LOCAL/p.as_posix();out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(body);items.append({'path':p.as_posix(),'oid':oid,'sha256':sha_bytes(body),'bytes':len(body)})
f=A/'Sources_banca_DB_candidate.json';save(f,{'utc':now(),'candidate':head,'method':'git archive of explicit candidate SHA; independently framed Git blob SHA1 computed from each byte stream','paths':paths,'content_count':len(items),'rows':items});print(ref(f),len(items))

