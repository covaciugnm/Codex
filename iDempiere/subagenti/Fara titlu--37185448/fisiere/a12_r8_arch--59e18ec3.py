from a12_r8_list import *
import subprocess,shlex,gzip,os,hashlib,concurrent.futures
from pathlib import PurePosixPath
BASE='6df998aee0e514d30856c461962afe99ebd0d113'
pool=Path('D:/CodexWork/a12-r8-archives');pool.mkdir(exist_ok=True)
def git(n):
 return subprocess.check_output(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=10','saga-server@192.168.100.151','git -C /home/saga-server/Documents/EvA-Contab '+n],timeout=180)
def folders():
 return sorted(set(str(PurePosixPath(x['source_row']['source_file']).parent) for x in rows if 'Documentatie/'in x['source_row']['source_file']))
def build():
 f=folders();print(f)
 paths=shlex.join(f);raw=git('ls-tree -r -l '+BASE+' -- '+paths).decode('utf8');allr=[]
 for l in raw.splitlines():
  v,p=l.split('\t',1);mode,typ,oid,sz=v.split();allr.append({'file':p,'oid':oid,'size':int(sz)})
 types=collections.Counter(PurePosixPath(x['file']).suffix for x in allr)
 elig=[x for x in allr if PurePosixPath(x['file']).suffix in ['.txt','.log','.md','.tsv','.csv','.json','.sh','.py']and x['size']<=1500000 and re.search(r'(dovezi|probe|audit|verdict|raport|plan|spec)',x['file'],re.I)]
 unc=[]
 for x in elig:
  oid=x['oid']; opt=[D/'blobs'/(oid+'.gz'),Path('D:/CodexWork/p01-r6-annex')/(oid+'.gz'),pool/(oid+'.gz')]
  exist=next((p for p in opt if p.exists()),None)
  if exist:x['storage']=str(exist)
  else:unc.append(x)
 # stream read-only git cat-file batch, not a user data export; scoped proof logs in assigned task paths
 if unc:
  oids=list(dict.fromkeys(x['oid'] for x in unc));p=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','git -C /home/saga-server/Documents/EvA-Contab cat-file --batch'],input=('\n'.join(oids)+'\n').encode(),capture_output=True,timeout=360);p.check_returncode();buf=p.stdout;off=0
  for oid in oids:
   end=buf.index(b'\n',off);hd=buf[off:end].decode().split();assert hd[:2]==[oid,'blob'];size=int(hd[2]);start=end+1;data=buf[start:start+size];assert hashlib.sha1(b'blob '+str(size).encode()+b'\0'+data).hexdigest()==oid
   (pool/(oid+'.gz')).write_bytes(gzip.compress(data));off=start+size+1
  for x in unc:x['storage']=str(pool/(x['oid']+'.gz'))
 for x in elig:
  data=gzip.decompress(Path(x['storage']).read_bytes());assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==x['oid']
 wr(pool/'index.json',elig);print('TOTAL',len(allr),len(elig),len(unc),sum(x['size']for x in elig))
if __name__=='__main__':build()

