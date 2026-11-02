import json,hashlib,subprocess,gzip,io,collections,pathlib,re,base64
from pathlib import Path
D=Path(r'D:\CodexWork\A12_evidence_20261102');B=Path(r'Z:\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01');E=B/'executie';E.mkdir(exist_ok=True)
m=json.loads((D/'map.json').read_text(encoding='utf8')); full=list()
for z in (D/'tree.raw').read_bytes().split(b'\0'):
 if z:
  hd,n=z.split(b'\t',1);full.append((n.decode(),hd.split()[2].decode()))
extras={n:o for n,o in full if ('cartele_pas3/' in n and n.endswith('.json')) or n.endswith('/02a_inventar.json') and 'T125-' in n}
def ssh(args,inp=None):return subprocess.run(['ssh','-C','-o','BatchMode=yes','-o','ConnectTimeout=9','saga-server@192.168.100.151',args],input=inp,stdout=subprocess.PIPE,check=True).stdout
rstr='cd /home/saga-server/Documents/EvA-Contab && '
hits=ssh(rstr+'git rev-parse 55808bac2d:Documentatie/echipa-2026-10-09/T125-registru-complet-taskuri/02a_inventar.json').decode().strip();extras['historical/55808bac2d/02a_inventar.json']=hits
pend=sorted({o for o in extras.values() if not (D/'blobs'/(o+'.gz')).exists()})
if pend:
 res=io.BytesIO(ssh(rstr+'git cat-file --batch',('\n'.join(pend)+'\n').encode()))
 for o in pend:
  h=res.readline().split();b=res.read(int(h[2]));assert res.read(1)==b'\n' and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==o;(D/'blobs'/(o+'.gz')).write_bytes(gzip.compress(b))
m['target_paths'].update(extras);(D/'map.json').write_text(json.dumps(m,ensure_ascii=False),encoding='utf8')
remote="""import json,subprocess,sys
ids=LIST
sha='6df998aee0e514d30856c461962afe99ebd0d113'
def run(*args):return subprocess.run(['git',*args],cwd='/home/saga-server/Documents/EvA-Contab',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out={}
for id in ids:
 q=run('diff-tree','--root','--no-commit-id','--no-renames','-r','--raw','-z',id); ss=q.stdout.split(b'\\x00'); dd=[]
 for j in range(0,len(ss)-1,2):
  if j+1>=len(ss):break
  hdr=ss[j].decode().split();name=ss[j+1].decode(errors='replace')
  if len(hdr)>=5 and name:dd.append({'path':name,'change':hdr[4],'before':hdr[2],'after':hdr[3]})
 out[id]={'ancestor':run('merge-base','--is-ancestor',id,sha).returncode==0,'changed':dd,'diff_rc':q.returncode}
print(json.dumps(out,ensure_ascii=False))
""".replace('LIST',repr(m['commit_ids'])).replace("b'\x00'","b'\\x00'")
out=json.loads(ssh('python3 -',remote.encode()));(D/'commitdiff.json').write_text(json.dumps(out,ensure_ascii=False),encoding='utf8');print('extra oids',len(set(extras.values())),'commits',len(out),'changed files',sum(len(v['changed']) for v in out.values()))
spec=next(o for n,o in extras.items() if n.endswith('P01.C11.T0005.json'));x=json.loads(gzip.decompress((D/'blobs'/(spec+'.gz')).read_bytes()).decode('utf-8-sig'));print('card sample',str(x)[:1700])
y=json.loads(gzip.decompress((D/'blobs'/(hits+'.gz')).read_bytes()).decode('utf-8-sig'));print('125sample',list(y),str(y)[:1500])

