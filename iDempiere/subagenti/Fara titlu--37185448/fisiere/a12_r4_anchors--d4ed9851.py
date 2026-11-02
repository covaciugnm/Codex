from a12_r3_survey import *
import subprocess as sp,io
r4=E/'R4';rows=rd(r4/'probe/25_aliasuri.json');idx=rd(E/'R3/A12_raport.json');reg=rd(B/'capturi/00_STATUS_TASKURI.json');reg=reg if isinstance(reg,list)else reg['taskuri']
for k in rows:
 w=next(r for r in reg if r['id']==k);rq=rd(E/'R1/taskuri'/('Fisa_'+k+'.json'))['source_identity_notes'];rows[k]['raw_card']={j:w.get(j)for j in ('nume_sugestiv','descriere','id_vechi','documente','documente_produse','origine')};rows[k]['alt_alias_row']=rq.get('aliases',[])
root='Documentatie/echipa-2026-10-09';prims=list((D/'tree.raw').read_bytes().split(b'\0'));pp={}
for s in prims:
 if not s:continue
 h,p=s.split(b'\t',1); pp[p.decode()]=(h.split()[2].decode(),int(h.split()[3]))
requests={k:{'al':y['alias']or k,'parent':k.split('.')[0].lower(),'canon':next(w['canonical']for w in idx['records']if w['task']==k)} for k,y in rows.items()}
sel={}
for n,(oid,ns) in pp.items():
 d=n.split('/')
 if len(d)!=4 or ns>1400000 or not n.lower().endswith(('.md','.txt','.py','.sh')):continue
 m=re.match(r'(T\d+)[.-]',d[-2],re.I)
 if not m:continue
 par=m[1].lower()
 if not any(q['parent']==par or par=='t01' for q in requests.values()): continue
 f=d[-1].lower()
 if re.search('plan|anex|decizi|deciz|cerint|spec|brief|sursa|script',f):sel[n]=oid
todo=[o for o in set(sel.values()) if not(D/'blobs'/(o+'.gz')).exists()]
if todo:
 q=sp.run(['ssh','-C','-o','BatchMode=yes','saga-server@192.168.100.151','cd /home/saga-server/Documents/EvA-Contab && git cat-file --batch'],input=('\n'.join(todo)+'\n').encode(),stdout=sp.PIPE,check=True,timeout=110);f=io.BytesIO(q.stdout)
 for o in todo:
  h=f.readline().split();bb=f.read(int(h[2]));assert f.read(1)==b'\n'and hashlib.sha1(b'blob '+str(len(bb)).encode()+b'\0'+bb).hexdigest()==o;(D/'blobs'/(o+'.gz')).write_bytes(gzip.compress(bb))
for k,y in rows.items():
 q=requests[k];hits=[]
 for n,oid in sel.items():
  d=n.split('/');parent=d[-2].split('-')[0].lower()
  if parent not in (q['parent'],'t01'):continue
  exp=r'(?<![\w.])(?:P01\.)?'+re.escape(q['al'])+r'(?![\w.-])'; lines=gzip.decompress((D/'blobs'/(oid+'.gz')).read_bytes()).decode('utf8',errors='replace').splitlines()
  if q['al']!=k and ('-' in q['al'] or ':' in q['al']):
   tail=re.split('[-:]',q['al'])[-1];ex2=r'^\s*\|\s*'+re.escape(tail)+r'\s*\|' if len(tail)>1 else r'(?!)'
  else:ex2=r'(?!)'
  for j,line in enumerate(lines,1):
   if (re.search(exp,line,re.I) or (parent==q['parent'] and re.search(ex2,line,re.I))) and not re.search('passw|mot de passe|parola[:=]|bearer [a-z]|token["\s]*[:=]\s*["\w-]{15,}',line,re.I):
    score=3*(line.lstrip().startswith('|'))+3*(parent==q['parent'])+2*('decizi' in n.lower())+2*(re.search('→|⇒|[Tt]rebuie|[Tt]est|[Aa]rtefact|[Oo]biectiv|[Pp]rob|[Oo]racol',line)!=None)
    hits.append((score,{'path':n,'line':j,'oid':oid,'literal':line[:1000],'near':[a[:350]for a in lines[max(0,j-2):j+1]]}))
 hits.sort(key=lambda rr:(-rr[0],rr[1]['path'],rr[1]['line']));y['additional_exact_sources']=[v for _,v in hits[:12]];y['candidate_count']=len(hits)
wr(r4/'probe/25_aliasuri_extinse.json',rows);print(len(sel),len(todo),[(k,r['candidate_count']) for k,r in rows.items()])

