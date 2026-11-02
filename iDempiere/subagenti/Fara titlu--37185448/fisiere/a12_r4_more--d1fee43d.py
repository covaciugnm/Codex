from a12_r3_survey import *
import subprocess as sp,gzip,io
r4=E/'R4';o=r4/'probe';q=r"""import json,subprocess as sp,pathlib,re,hashlib
sha='6df998aee0e514d30856c461962afe99ebd0d113';cwd='/home/saga-server/Documents/EvA-Contab'
def run(*args):return sp.run(args,cwd=cwd,capture_output=True)
d={};base='Documentatie/echipa-2026-10-09';p=base+'/T27-implementare-p1-4-echipe/T27e2/D4-M02/01b_decizii_orchestrator_n1.md';r=run('git','show','f0af10f15c94:'+p)
if not r.returncode:
 txt=r.stdout.decode(errors='replace');d['T27.34_decision']={'sha256':hashlib.sha256(r.stdout).hexdigest(),'path':p,'lines':[[i,l[:440]]for i,l in enumerate(txt.splitlines(),1)if re.search(r'^#|^\| (Q|D|P)-',l)][:22]}
for k,pt in [('T33.06','(?:T33[-_:]P2|\\bP2\\b)'),('T33.07','(?:T33[-_:]P3|\\bP3\\b)'),('T36.66','L6'),('T40.14','T40-L1')]:
 patt=pt.replace('(?:','(').replace('\\b','');r=run('git','ls-tree','-r','-z',sha,'--',base+'/'+k.split('.')[0]); 
 # T33 / T36 directories are named by a suffix; drill same technical parent only, not neighbouring tasks.
 rr=run('git','ls-tree','-r','-z',sha,'--',base);nh=[]
 for rec in rr.stdout.split(b'\0'):
  if not rec:continue
  h,b=rec.split(b'\t',1);n=b.decode();parent=k.split('.')[0]+'-'
  if '/'+parent not in n:continue
  leaf=n.split('/')[-1]
  if k.startswith('T33'):
   if re.search(r'(?:^|[-_/])P'+k[-1].replace('6','2').replace('7','3')+r'(?:\W|_)',n,re.I):nh.append([n,h.split()[2].decode()])
  elif k=='T36.66' and '07-L6_anexa_audit_etichete.py' in n:nh.append([n,h.split()[2].decode()])
  elif k=='T40.14' and '02_L1_anexa_A' in n:nh.append([n,h.split()[2].decode()])
 for row in nh[:14]:
  b=run('git','cat-file','blob',row[1]).stdout;ls=b.decode(errors='replace').splitlines();row.append([[i,l[:350]]for i,l in enumerate(ls,1)if l.startswith(('# ','## ','def ','class '))][:13])
 d[k]={'direct_files':nh[:14],'count':len(nh)}
for tag in ['r22-20261013b','r23-20261013','13-pre-T43b','13-pre-T43c']:
 res=run('docker','image','inspect','--format','{{.Id}}','eva-idempiere-rest:'+tag);d[tag]={'exit':res.returncode,'image':res.stdout.decode().strip() if not res.returncode else None}
ft='/repo/frontend/data/saga_import_map.json';cmd='import json,hashlib; p="'+ft+'"; b=open(p,"rb").read();d=json.loads(b);print(json.dumps({"sha":hashlib.sha256(b).hexdigest(),"bytes":len(b),"keys":list(d)[:25] if isinstance(d,dict) else None,"counts":{k:len(v) for k,v in d.items() if isinstance(v,(dict,list))} if isinstance(d,dict) else None}))'
rc=run('docker','exec','eva-contab-frontend','python3','-c',cmd);d['map_content_runtime']={'rc':rc.returncode,'summary':json.loads(rc.stdout) if rc.returncode==0 else None}
print(json.dumps(d,ensure_ascii=False))
""";rc=sp.run(['ssh','-C','-o','BatchMode=yes','saga-server@192.168.100.151','python3 -'],input=q.encode(),capture_output=True,check=True,timeout=70);d=json.loads(rc.stdout);wr(o/'autoritate_si_montari_istorice.json',d);print([(k,v.get('count',v.get('exit',v.get('rc'))))for k,v in d.items()])

