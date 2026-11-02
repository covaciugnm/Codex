from a12_r3_survey import *
import subprocess as sp,io,collections
r4=E/'R4';mu=[('DIRECTIVĂ_DE_METODĂ','metodă'),('LIVRABIL_CARTELĂ_NOMINALĂ','livrabil'),('CONTROL_DISPOZIȚIE_MONTARE','montare')];tasks={}
for fp in (E/'R3/taskuri').glob('*.json'):
 w=rd(fp);n=[q for q in w['operative_criteria_and_audit_criteria']+w['R3_new_criteria']if q['current']['status']=='NEEXECUTAT'and q['kind']in dict(mu)]
 if n:tasks[w['task']]=[v['id']for v in n]
p=collections.defaultdict(dict);tree={}
for ln in (D/'tree.raw').read_bytes().split(b'\0'):
 if not ln:continue
 hdr,n=ln.split(b'\t',1);n=n.decode();parts=n.split('/')
 if len(parts)!=4:continue
 mm=re.match(r'(?i)(T[0-9]+(?:\.[0-9]+)?)[-_]',parts[-2]);k=mm[1].upper() if mm else None;f=parts[-1].lower()
 if k not in tasks or not f.endswith('.md')or int(hdr.split()[3])>700000 or not re.search(r'verdict|audit.*(?:plan|spec|cod)|raport_final|auditor.*(?:cod|spec|plan)|raport_montare',f):continue
 if re.search('brief|model|cerer|matrice|propun|plan_audit|script',f):continue
 oid=hdr.split()[2].decode();p[k][n]=oid
# Multiple judgments from distinct audit phases kept as chronology; never infer sibling evidence.
for k in list(p):
 v=sorted(p[k].items());p[k]=dict(v[:4]+v[-4:]) if len(v)>8 else dict(v)
todo=[v for v in {oid for pp in p.values()for oid in pp.values()} if not(D/'blobs'/(v+'.gz')).exists()]
if todo:
 cp=sp.run(['ssh','-C','-o','BatchMode=yes','saga-server@192.168.100.151','cd /home/saga-server/Documents/EvA-Contab && git cat-file --batch'],input=('\n'.join(todo)+'\n').encode(),stdout=sp.PIPE,check=True,timeout=80);st=io.BytesIO(cp.stdout)
 for oid in todo:
  head=st.readline().split();b=st.read(int(head[2]));assert st.read(1)==b'\n'and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid;(D/'blobs'/(oid+'.gz')).write_bytes(gzip.compress(b))
proof={}
for k in tasks:
 docs=[]
 for n,oid in p.get(k,{}).items():
  b=gzip.decompress((D/'blobs'/(oid+'.gz')).read_bytes());ll=b.decode('utf8',errors='replace').splitlines();heads=[[i,l[:260]]for i,l in enumerate(ll,1)if l.startswith('# ')][:1];r=[]
  for i,l in enumerate(ll,1):
   if len(l)>1200 or re.search('passwor|bearer|token\\s*[=:]|parola\\s*[:=]',l,re.I):continue
   if re.search(r'\b(?:verdict|nota|notă|rezultat|scor|total|concluzi)',l,re.I) and re.search(r'\b(?:\d+(?:[.,]\d+)?\s*/\s*10|aprobat|acceptat|respins|parțial|reia|admis|refuzat)\b',l,re.I):r.append([i,l[:295]])
  docs.append({'path':n,'blob':oid,'sha256':hashlib.sha256(b).hexdigest(),'line_count':len(ll),'heading':heads,'verdict_utterances':r[:3]+r[-2:]if len(r)>5 else r})
 proof[k]={'criteria':tasks[k],'exact_task_folder_only':True,'review_documents_found':len(docs),'docs':docs}
wr(r4/'probe/historical_audit_artifacts.json',proof);print('tasks',len(tasks),'with docs',sum(bool(v['docs'])for v in proof.values()),'docs',sum(len(v['docs'])for v in proof.values()),'read new',len(todo))

