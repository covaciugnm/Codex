from a12_r7_pg_cui import *
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict,Counter
from functools import lru_cache
from pathlib import PurePosixPath
import unicodedata
ROOT=E.parent;R6=E/'R6'; reps=rd(R6/'A12_raport.json')['records'];pool=ThreadPoolExecutor(10);docs={w['task']:w for w in pool.map(lambda x:rd(R6/x['file']),reps)};reg={r['criterion']:r for r in rd(R6/'Registru_reexecutare_R6.json')['records']if r['R6_state']=='NEEXECUTAT'}; assert len(reg)==1587
todo={};meta={}
for k,w in docs.items():
 for f in ['operative_criteria_and_audit_criteria','R3_new_criteria','R4_new_criteria']:
  for c in w[f]:
   if c['id']in reg:todo[c['id']]=c;meta[c['id']]=w
assert set(todo)==set(reg)
def norm(v):return ''.join(c for c in unicodedata.normalize('NFKD',str(v).casefold())if unicodedata.category(c)!='Mn')
def cut(s,n=300):return s[:n] if isinstance(s,str)else s
origidx=rd(E/'A12_referinte_git.json')['rows']; ownidx={r['id']:r for r in origidx};original=rd(R6/'probe/Anexe_1611_pentru_fisa.json')['records'];ann={r['criterion']:r for r in original}
tree={}
for line in (D/'tree.raw').read_bytes().split(b'\0'):
 if not line:continue
 st,path=line.decode('utf8',errors='replace').split('\t',1);fields=st.split()
 if len(fields)>=4 and fields[1]=='blob':tree[path]=(fields[2],int(fields[3]))
folders=defaultdict(set)
for k,rr in ownidx.items():
 p=rr.get('declared_file');g=rr.get('declared_file_git')
 if p and g and g.get('type')=='tree'and p.startswith('Documentatie/echipa-2026-10-09/') and not p.startswith('Documentatie/echipa-2026-10-09/T139-'):folders[k].add((p.rstrip('/')+'/','direct registered task directory'))
for cid,r in reg.items():
 p=r['entry_and_oracle_specific_to_case']['source_file'];k=r['task']
 if p and p.startswith('Documentatie/echipa-2026-10-09/') and not any(x in p for x in ['/T139-','/COORDONARE_','/00_']):
  bits=p.split('/')
  if len(bits)>=4 and re.match(r'T[0-9]',bits[2]):folders[k].add(('/'.join(bits[:3])+'/','directory of the verified primary nominal source'))
inverse=defaultdict(set)
for k,w in docs.items():
 for z in w.get('disposition_admin',{}).get('successors',[]):
  dest=z.get('target')
  if dest in docs and k!=dest:
   for p,why in folders[k]:inverse[dest].add((p,'ancestor '+k+' via recorded disposition; documentary scope not inherited automatically'))
def historical(c):
 s=norm(c['normative_content']);kind=c['kind']
 cid=c['id'];task=reg[cid]['task']
 # The verb/criterion must concern an actual historic installation order, nominated release or formal dated approval.
 if cid in {'T32.08-R3-001','T32.09-R3-001','T89-R3-001','T261-R3-001','T296-R3-001','T303-R3-001','T358-R3-001','T361-R2-001','T362-R2-001','T364-R2-001','T365-R2-001','T367-R2-001','T372-R2-001','T378-R2-001'} or task in {f'T38.{i:02}'for i in range(1,11)} and cid.endswith('-R3-001'):return 'disposition'
 if kind in ['CONTROL_DISPOZIȚIE_MONTARE','DIRECTIVĂ_DE_METODĂ']:return 'disposition'if kind=='CONTROL_DISPOZIȚIE_MONTARE'else 'method'
 if kind=='LIVRABIL_CARTELĂ_NOMINALĂ' and (s=='planul taskului auditat' or re.search(r'\bauditat|\bnota audit',s)):return 'plan'
 if s in ('planul taskului auditat','planul de task auditat'):return 'plan'
 if re.match(r'^(refa planul|revizorul auditeaza|documenteaza .*url|raportul auditat|suita completa din export curat|poarta:|forma: t02/)',s):return 'documentary'
 if kind=='CRITERIU_PLAN_NOMINAL':
  ff=reg[c['id']]['entry_and_oracle_specific_to_case'];cmd=norm(ff.get('recipe_from_own_row')or'')
  if re.match(r'^.*(?:git diff|git merge-tree|git show|git log).*',cmd)and re.search(r'<varf>|<baza>|merge-base|master\\.\\.\\.head',cmd):
   if not ff.get('named_test_fixtures_in_source')and not any(x in s for x in ('din buton','documentul co','din ecran','la pornire','cele doua sesiuni')):return 'historical_delta'
 return None
histids={cid:historical(c)for cid,c in todo.items()if historical(c)}; selected=defaultdict(list)
def candidates():
 bydir=defaultdict(list)
 for path,(oid,size)in tree.items():
  if size>750000 or not path.endswith('.md'):continue
  parts=path.split('/')
  if len(parts)!=4:continue
  nm=norm(parts[-1])
  if not (('audit' in nm or 'aviz' in nm)and ('plan' in nm or 'poarta' in nm or 'spec' in nm)):continue
  if 'brief'in nm or 'instruct' in nm or 'fisa' in nm or 'cerere'in nm:continue
  bydir['/'.join(parts[:3])+'/'].append((path,oid))
 for cid,h in histids.items():
  task=reg[cid]['task']
  for fol,authority in list(folders[task])+list(inverse[task]):
   links=sorted(bydir.get(fol,[]),key=lambda r:('plan'not in norm(r[0]),'final'not in norm(r[0]),r[0]))
   selected[cid].extend([(p,o,authority)for p,o in links[:5]])
candidates();store=RP/'archive_data';store.mkdir(exist_ok=True)
def cached(oid):
 for q in [D/'blobs'/(oid+'.gz'),Path('D:/CodexWork/p01-r6-annex')/(oid+'.gz'),store/(oid+'.gz')]:
  if q.is_file():return gzip.decompress(q.read_bytes())
 return None
oids=sorted({o for l in selected.values()for _,o,_ in l});need=[o for o in oids if cached(o)is None]
if need:
 body=sp.check_output(['ssh','-o','BatchMode=yes',server,cmdgit+'cat-file --batch'],input=('\n'.join(need)+'\n').encode('ascii'))
 i=0
 for oid in need:
  j=body.index(b'\n',i);head=body[i:j].decode().split();assert head[0]==oid and head[1]=='blob';size=int(head[2]);raw=body[j+1:j+1+size];assert hashlib.sha1(b'blob '+str(size).encode()+b'\0'+raw).hexdigest()==oid;(store/(oid+'.gz')).write_bytes(gzip.compress(raw));i=j+size+2
@lru_cache(maxsize=512)
def review(pair):
 path,oid=pair;raw=cached(oid);assert raw is not None and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==oid
 ls=raw.decode('utf-8-sig',errors='replace').splitlines();hits=[]
 for i,l in enumerate(ls,1):
  if re.search(r'(?i)\b(?:verdict|nota|scor|aviz|admis|respins|aprob|decizie)\b',l)and re.search(r'(?:\b(?:10|[0-9](?:[,.]\d+)?)\s*/\s*10\b|admis|respins|trece poarta|poarta trec)',l,re.I)and len(l)<=1050:
   hits.append({'line':i,'literal':l[:500],'line_sha':hashlib.sha256(l.encode()).hexdigest()})
 return {'path':path,'blob':oid,'sha256':hashlib.sha256(raw).hexdigest(),'title':next((v[:180]for v in ls if v.strip().startswith('#')),''),'actual_lines_with_authored_decision':hits[:3]+(hits[-1:]if len(hits)>3 else[])}
histents={}
for cid,h in histids.items():
 v=[]
 for p,o,authority in selected[cid]:
  z=review((p,o))
  if z['actual_lines_with_authored_decision']:v.append({**z,'authority':authority})
 histents[cid]={'task':reg[cid]['task'],'criterion':cid,'question_type':h,'primary_root':sorted(folders[reg[cid]['task']]),'documented_ancestor_roots':sorted(inverse[reg[cid]['task']]),'candidate_docs_read':len(selected[cid]),'documents_with_a_decision_line':v,'qualification':'Le document reproduit effectivement cette mention. La date de clôture, la signature et la version de la fonctionnalité ne sont pas déduites de la note écrite dans une autre phase.'}
wr(RP/'Istoric_verdicturi_nominale.json',{'commit':shaGit,'verified_blobs':len(oids),'new_blob_reads':len(need),'origin_trace':'Dossier déclaré dans /claude ou parent d’une source nominale. Un dossier de prédécesseur est présenté à part et ne prouve pas l’acceptation du successeur.','records':list(histents.values())})
print('hist',len(histents),len(oids),sum(bool(d['documents_with_a_decision_line'])for d in histents.values()))

