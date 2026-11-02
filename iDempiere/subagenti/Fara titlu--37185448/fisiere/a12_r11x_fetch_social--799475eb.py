from a12_r11x_base import *
from pathlib import PurePosixPath
patterns=[':(glob)idempiere/plugins/**/src/**','idempiere/plugins/com.eva.ro.contab/test/fixtures/help/ecrane.tsv','idempiere/plugins/com.eva.ro.saga.native/test/TestT232GardaConsola.java','idempiere/plugins/com.eva.ro.saga.native/META-INF','idempiere/plugins/com.eva.ro.saga.native/OSGI-INF']
from shlex import quote
cmd='git -C /home/saga-server/Documents/EvA-Contab archive --format=tar.gz '+head+' -- '+' '.join(quote(p)for p in patterns);res=sp.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151',cmd],capture_output=True,timeout=140);assert res.returncode==0,res.stderr.decode()[-500:]
items=[];collisions=[]
with tarfile.open(fileobj=io.BytesIO(res.stdout),mode='r:gz')as arc:
 for m in arc.getmembers():
  if not m.isfile():continue
  p=PurePosixPath(m.name);assert not p.is_absolute()and'..'not in p.parts;b=arc.extractfile(m).read();oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert catalog[p.as_posix()]['git_object']==oid
  o=LOCAL/p.as_posix()
  if o.exists() and o.read_bytes()!=b:
   other=W/'case_sensitive_objects'/oid;other.parent.mkdir(exist_ok=True);other.write_bytes(b);collisions.append({'path':p.as_posix(),'sha256':sha_bytes(b),'windows_alias_sha256':sha(o),'git_oid':oid,'masking_limited_to_windows_materialization':True})
  else:
   o.parent.mkdir(parents=True,exist_ok=True)
   if not o.exists():o.write_bytes(b)
  items.append({'path':p.as_posix(),'oid':oid,'sha256':sha_bytes(b)})
f=A/'Sources_complement_SAGA_et_T201.json';save(f,{'utc':now(),'head':head,'inputs':patterns,'distinct_blob_paths':len(items),'case_collisions':collisions,'provenance_only':True,'rows':items});print(ref(f),len(items),len(collisions))

