from pathlib import Path
import json,re,hashlib,subprocess,collections,io,datetime,time,gzip
B=Path(r'Z:\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01');D=Path(r'D:\CodexWork\A12_evidence_20261102');D.mkdir(exist_ok=True); (D/'blobs').mkdir(exist_ok=True)
r=lambda f:json.loads((B/f).read_text(encoding='utf-8-sig'));git=r('executie/A12_referinte_git.json');reg={x['id']:x for x in r('capturi/00_STATUS_TASKURI.json')};ix={x['source_id']:x for x in r('A12_index_taskuri.json')['rows']};paths={}; names=collections.defaultdict(list)
for z in (D/'tree.raw').read_bytes().split(b'\0'):
 if z:
  hdr,p=z.split(b'\t',1);mod,ty,oid,size=hdr.split();p=p.decode(); paths[p]=(oid.decode(),int(size));names[Path(p).name].append(p)
target={}; bytask={};parentglob=collections.defaultdict(list)
for n in paths:
 parts=n.split('/')
 if len(parts)==4 and parts[:2]==['Documentatie','echipa-2026-10-09'] and re.match(r'^T\d+(?:\.\d+)?[-_]',parts[2],re.I):
  code=re.match(r'^(T\d+(?:\.\d+)?)',parts[2],re.I)[1].upper(); parentglob[code].append(n)
for x in git['rows']:
 id=x['id'];v=reg[id];picked={}
 def add(path,why):
  if path in paths and paths[path][1]<=1500000 and Path(path).suffix.lower() in ['.md','.txt','.json','.java','.sql','.py','.js','.rb','.sh','.csv','.xml','.yml','.yaml','.tsv','.properties']:
   if re.search(r'(?i)(?:credential|password|parole|token_secret|private_key|fisier_extern)',Path(path).name):return
   picked.setdefault(path,[]).append(why);target[path]=paths[path][0]
 def resolve(s,why):
  for v in [s,s.split('#')[0],s.split(':')[0],s.removeprefix('./')]:
   if v in paths:add(v,why);return
   prefix='Documentatie/echipa-2026-10-09/'+v
   if prefix in paths:add(prefix,why);return
   bs=Path(v).name
   if len(names.get(bs,[]))==1:add(names[bs][0],why);return
 file=v.get('fisier') or '';resolve(file,'fisier')
 for dd in v.get('documente_produse',[]):
  if dd.get('forma_ref')=='cale': resolve(dd['ref'],'document declarat')
 for link in v.get('linkuri',[]) or []:
  if isinstance(link,dict):
   s=link.get('url',''); m=re.search(r'/(?:blob|tree)/[^/]+/(.*)',s); 
   if m:resolve(m[1],'link declarat')
 def flatten(y):
  if isinstance(y,dict):return '\n'.join(flatten(z) for z in y.values())
  if isinstance(y,list):return '\n'.join(flatten(z) for z in y)
  return str(y or '')
 source=flatten({k:v.get(k) for k in ('cerere_proprietar','origine','explicatii','observatii','sursa_deciziei','fisier','descriere')})
 for p in re.findall(r'[\wÀ-ž\-./()]+?\.(?:md|json|txt|py|java|sql|tsv)(?=[:\s#),»\]\x60]|$)',source,re.I):
  resolve(p.strip('.'),'citare în registru')
 for k in {id,id.split('.')[0],str(v.get('agregat_in','') or ''),str(v.get('parinte','') or '')}:
  for n in parentglob.get(k,[]):
   s=Path(n).name.lower()
   if re.search(r'(?:cerinta_proprietar|cerintele_proprietar|brief_manager|manager_brief|verdict_final|raport_montare|decizi[ei]|audit_final|audit_montare)',s):
    add(n,('dosar propriu' if k==id else 'dosar părinte/destinație')+'; relevanță de verificat')
 bytask[id]=picked
for n in paths:
 if any(k in n for k in ('99_PROPUNERE_PAS3.json','99a_DECIZII_PROPRIETAR_PAS3.md','32_RASPUNSURI_PROPRIETAR.md','00_DECIZIE_PROPRIETAR_APLICATIA_VECHE','T285-toate-proiectele-pe-capitole/00_cerinta','Log-Istoric/LOG_ISTORIC.md')):target[n]=paths[n][0]
# Additional source proof from earlier time: inspect declared blobs at historical commit, without replacing them with present files.
historical={}; commits=set()
for x in git['rows']:
 for d in x['documents']:
  for ck in d['checks']:
   w=ck.get('result') or {};oid=w.get('oid')
   if not oid:continue
   if w.get('type')=='commit':commits.add(oid)
   elif w.get('type')=='blob' and w.get('bytes',0)<=1500000 and Path(str(d.get('ref',''))).suffix.lower() in ['.md','.txt','.json','.java','.sql','.py','.js','.rb','.sh','.csv','.xml','.yml','.yaml','.tsv','.properties']:
    historical[oid]=d['ref']
pending=sorted((set(target.values())|set(historical)|commits)-{p.name[:-3] for p in (D/'blobs').glob('*.gz')})
if pending:
 res=subprocess.run(['ssh','-C','-o','BatchMode=yes','-o','ConnectTimeout=10','saga-server@192.168.100.151','cd /home/saga-server/Documents/EvA-Contab && git cat-file --batch'],input=('\n'.join(pending)+'\n').encode(),stdout=subprocess.PIPE,check=True)
 f=io.BytesIO(res.stdout)
 for ex in pending:
  hd=f.readline().split();assert hd[0].decode()==ex and len(hd)==3,hd
  ty=hd[1].decode();n=int(hd[2]);bb=f.read(n);assert f.read(1)==b'\n';assert hashlib.sha1(ty.encode()+b' '+str(n).encode()+b'\0'+bb).hexdigest()==ex
  (D/'blobs'/(ex+'.gz')).write_bytes(gzip.compress(bb))
assert all((D/'blobs'/(o+'.gz')).exists() for o in set(target.values())|set(historical)|commits)
m={'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pinned_commit':'6df998aee0e514d30856c461962afe99ebd0d113','record_blob_verified_count':len(set(target.values())|set(historical)|commits),'target_paths':target,'task_declared_and_context_paths':bytask,'historical_blob_paths':historical,'commit_ids':list(commits),'method':'Git ls-tree complet în aria Documentatie/echipa-2026-10-09 și Log-Istoric, apoi cat-file pe obiecte dedicate, hash Git SHA1 recalculat pe octeții fiecărui obiect. Corpus de referințe, nu declarație că suitele găsite au fost executate.'}
(D/'map.json').write_text(json.dumps(m,ensure_ascii=False),encoding='utf8');print('paths',len(target),'oids',m['record_blob_verified_count'],'rows_with_candidate',sum(bool(x) for x in bytask.values()),'commit',len(commits))

