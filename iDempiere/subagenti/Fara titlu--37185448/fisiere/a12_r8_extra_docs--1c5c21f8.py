from a12_r8_cases import *
from a12_r8_arch import git
dirs=['T224-efactura-pornire','T204-tiparire-loturi-ramase','T203-tiparire-documente-standard','T17-conectare-banci']
pdir='Documentatie/echipa-2026-10-09'
allf=git('ls-tree -d --name-only '+BASE+':'+pdir).decode().splitlines()
dirs=sorted(k for k in allf if re.match(r'T(?:17|203|204|224)-',k));v=git('ls-tree -r -l '+BASE+' -- '+' '.join(shlex.quote(pdir+'/'+z)for z in dirs)).decode().splitlines();xs=[]
for l in v:
 s,p=l.split('\t',1);md,typ,oid,size=s.split()
 if not ((p.count('/')==3 and p.endswith('.md'))or re.search(r'/IM[-_]0?1|21_comit|tabel_21',p,re.I))or int(size)>600000:continue
 xs.append({'oid':oid,'file':p,'size':int(size)})
target=Path('D:/CodexWork/a12-r8-spec-extra');target.mkdir(exist_ok=True)
u=[z['oid'] for z in xs];z=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','git -C /home/saga-server/Documents/EvA-Contab cat-file --batch'],capture_output=True,input=('\n'.join(u)+'\n').encode(),timeout=60);buf=z.stdout;off=0
for row in xs:
 end=buf.index(b'\n',off);hdr=buf[off:end].decode().split();assert hdr[0]==row['oid'];bb=buf[end+1:end+1+int(hdr[2])];assert hashlib.sha1(b'blob '+str(len(bb)).encode()+b'\0'+bb).hexdigest()==row['oid'];fp=target/(row['oid']+'.gz');fp.write_bytes(gzip.compress(bb));off=end+len(bb)+2;row['storage']=str(fp)
wr(target/'index.json',xs)
for task,p in [('T224-',r'\| \x60?[a-f0-9]{7,40}\x60? \|'),('T17-',r'SmartFintech|Smart Fintech'),('T203-',r'D1215.*livrare|livrare.*D1215')]:
 for row in xs:
  if task not in row['file']:continue
  hits=[i for i,l in enumerate(txt(row).splitlines(),1) if re.search(p,l,re.I)]
  if (len(hits)>=14 if task=='T224-'else len(hits)>=2):print(row['file'].split('/',3)[-1],len(hits),hits[:2])
print('files',len(xs))

