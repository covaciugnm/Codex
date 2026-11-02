from a12_r3_survey import *
import collections,subprocess as sp,io,concurrent.futures as cf,datetime
rr=E/'R4';plan=rd(rr/'Registru_1868.json')['records'];groups=collections.defaultdict(dict)
for s in (D/'tree.raw').read_bytes().split(b'\0'):
 if not s:continue
 hd,n=s.split(b'\t',1);n=n.decode();paths=n.split('/');m=re.search(r'/(T[0-9]+(?:\.[0-9]+)?)[-_]',n,re.I)
 if not m or not re.search(r'dovezi[^/]*/|/probe[^/]*/|/capturi[^/]*/',n,re.I)or not re.search(r'\.(?:txt|json|out|tsv|log|md)$',n,re.I)or int(hd.split()[3])>500000:continue
 groups[m[1].upper()][n]=hd.split()[2].decode()
inds={k:collections.defaultdict(list)for k in groups}
for k,items in groups.items():
 for p,oid in items.items():inds[k][Path(p).name.lower()].append((p,oid))
ids={w['criterion']:w for w in plan};assocs={};sel={}
for c,w in ids.items():
 k=w['task'];s=w['scope_from_task']+' '+w['expected_verbatim'];paths=groups.get(k,{})
 if not paths:continue
 stem=re.match(r'^(K|C|R)[-.]0*(\d+)([a-z]?)\b',s,re.I);matches=[]
 for raw in re.findall(r'(?:[\w.-]+/)*[\w.-]+\.(?:txt|json|log|tsv|out|md)\b',s,re.I):
  rs=inds[k].get(Path(raw).name.lower(),[]);rs2=[(p,o)for p,o in rs if p.lower().endswith('/'+raw.lower())]
  if len(rs2)==1:matches.append((*rs2[0],'chemin explicite du critère'))
 if stem:
  letter,num,sub=stem.groups();reg=re.compile(r'(?<![A-Za-z0-9])'+letter.upper()+(r'[-_.]0*' if letter.upper()=='R' else r'[-_.]?0*')+num+sub+r'(?![A-Za-z0-9])')
  cand=[(p,o,'identifiant du critère dans le nom exact de l’artefact')for p,o in paths.items()if reg.search(Path(p).name) and not re.search('script|brief',p,re.I)]
  if len(cand)<=12:matches.extend(cand)
 if matches:
  mm=[];sn=set()
  for p,oid,why in matches:
   if p in sn:continue
   sn.add(p);mm.append((p,oid,why));sel[p]=oid
  assocs[c]=mm
todo=[o for o in set(sel.values()) if not(D/'blobs'/(o+'.gz')).exists()]
def pack(os):
 pr=sp.run(['ssh','-C','-o','BatchMode=yes','saga-server@192.168.100.151','cd /home/saga-server/Documents/EvA-Contab && git cat-file --batch'],input=('\n'.join(os)+'\n').encode(),stdout=sp.PIPE,check=True,timeout=110);st=io.BytesIO(pr.stdout)
 for oid in os:
  hd=st.readline().split();b=st.read(int(hd[2]));assert st.read(1)==b'\n'and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid;(D/'blobs'/(oid+'.gz')).write_bytes(gzip.compress(b))
for start in range(0,len(todo),250):pack(todo[start:start+250])
files={}
for n,oid in sel.items():
 b=gzip.decompress((D/'blobs'/(oid+'.gz')).read_bytes());ll=b.decode('utf-8-sig',errors='replace').splitlines();stage=next((a for a in n.split('/')if re.match('dovezi|probe|capturi',a,re.I)),'');classif='BAZĂ_SAU_PLAN' if re.search('plan|T0|inainte|înainte',stage+'/'+Path(n).name,re.I)else 'ARHIVĂ_DE_RULARE_NECALIBRATĂ'
 # Archive may contain business data or credentials. Store only aggregate diagnostic and assertion markers, never raw row/values.
 pp=[];fp=[]
 for i,line in enumerate(ll,1):
  tag=re.search(r'\b(?:OK|PASS|FAIL|SKIP|ERROR|REZULTAT|NOK)\b',line,re.I)
  if not tag:continue
  (fp if tag[0].upper()in ('FAIL','NOK','ERROR') else pp).append({'line':i,'marker':tag[0].upper()})
 files[n]={'path':n,'git_blob':oid,'sha256':hashlib.sha256(b).hexdigest(),'stage':stage,'classification':classif,'bytes':len(b),'line_count':len(ll),'positive_or_other_markers':len(pp),'negative_or_error_markers':len(fp),'marker_line_samples':(pp[:4]+fp[:4]),'limit':'Lectură de fișier arhivat pe identitate nominală. Un indicator FAIL poate fi o contraprobă așteptată; nu certifică independent calcule, instalare sau actualitate.'}
out={c:[{'path':p,'match_rule':rule,'blob':oid}for p,oid,rule in matches]for c,matches in assocs.items()}
wr(rr/'probe/archived_criterion_outputs.json',{'current_git':'6df998aee0e514d30856c461962afe99ebd0d113','checked_input_criteria':len(ids),'input_tasks_with_candidate_archive':len(set(w['task']for w in plan)&set(groups)),'archive_paths_inspected_by_name':sum(len(v)for v in groups.values()),'selected_original_criteria':len(assocs),'file_count':len(files),'files':files,'by_criterion':out});print(len(assocs),len(files),len(todo))

