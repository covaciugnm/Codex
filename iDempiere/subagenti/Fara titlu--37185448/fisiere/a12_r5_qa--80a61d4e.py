from a12_r3_survey import *
from collections import Counter,defaultdict
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime,UTC
import shutil,html,re
R=E/'R5'; R4=E/'R4'; report=rd(R/'A12_raport.json');registry=rd(R/'Registru_reexecutare_R5.json');cat=rd(R/'Dovezi_criterii.json');ev=cat['evidence'];inv=cat['inverse_task_requirement_links'];r4=rd(R4/'A12_raport.json'); r4m={w['task']:w for w in r4['records']};assert sha(R4/'A12_raport.json')=='a81a12d23f080685a21690fba2377948fa3a9c7823022ebb55959bdf141583ab'
def digestval(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
@lru_cache(maxsize=256)
def jd(p):return rd(p)
@lru_cache(maxsize=600)
def raw(p):return p.read_bytes()
def ptr(v,t):
 if not t:return v
 assert t.startswith('/')
 for q in t[1:].split('/'):
  q=q.replace('~1','/').replace('~0','~');v=v[int(q)]if isinstance(v,list)else v[q]
 return v
def links(c):
 a=[(c['source_evidence_id'],'source')]+[(z,'authority')for z in c.get('authority_evidence_ids',[])]
 for k in ['current','closure']:a.extend((z,k)for z in c[k]['evidence_ids'])
 for f,k,r in [('component_assertion_crosscheck','ids','component_candidate'),('cross_financial_observation','evidence_ids','financial_context'),('installed_schema_probe','ids','metadata_context'),('archive_criterion_output','ids','historic_artifact_context')]:a.extend((z,r)for z in c.get(f,{}).get(k,[]))
 a.extend((z,'case_context')for z in c.get('strict_related_sources_R5',[]));return set(a)
def criteria(w):return sum([w[x]for x in ['operative_criteria_and_audit_criteria','R3_new_criteria','R4_new_criteria']],[])
def one(rr):
 k=rr['task'];w=rd(R/rr['file']);old=r4m[k];assert sha(R4/old['file'])==old['sha256']==rr['R4_sha'];assert sha(R/rr['file'])==rr['sha256'] and sha(R/rr['html'])==rr['html_sha256'];original=rd(R4/old['file'])
 ids=[c['id']for c in criteria(w)]; assert ids==[c['id']for c in criteria(original)];page=(R/rr['html']).read_text(encoding='utf8');assert page.count('<h1>')==1 and all('id="'+html.escape(i)+'"'in page for i in ids)
 ed={(z,k,c['id'],a)for c in criteria(w)for z,a in links(c)};ex={c['id']:c['current']['status']for c in criteria(w)};new=[];nominal={}
 for c in criteria(w):
  if c.get('R5_measured_scenarios'):new.append(c['id'])
  for sc in c.get('R5_measured_scenarios',[]):
   assert sc['evidence'] in c['current']['evidence_ids']and sc['result']and sc['entry'] and sc['scope_limit']
   nominal[sc['evidence']]=c['id']
 return ed,ex,new,nominal
with ThreadPoolExecutor(max_workers=9) as exec:cases=list(exec.map(one,report['records']))
edges=set().union(*(r[0]for r in cases)); states=dict(t for z in cases for t in z[1].items());updated=set().union(*(set(r[2])for r in cases));reverse={(eid,x['task'],x['criterion'],x['relation'])for eid,rows in inv.items()for x in rows}
assert edges==reverse and not ({z for z,*_ in edges}-set(ev)) and len(states)==2619 and set(r4m)=={k['task']for k in report['records']} and len(r4m)==652
rows=registry['records'];assert len(rows)==1881 and len({r['criterion']for r in rows})==1881;orig=rd(R4/'Registru_1868.json')['records']; assert {r['criterion']for r in rows if r['original_1868']}=={r['criterion']for r in orig};assert all(states[r['criterion']]==r['R5_state']and r['protocol_ref']in rd(R/'Protocol_exec.json')and r['entry_and_oracle_specific_to_case']['sha_or_git_blob'] for r in rows)
all4=rd(R/'probe/locatori_EV4_verificați.json');assert all4['resolved_ids']==1220
strict_num=Counter()
for eid,v in ev.items():
 if not eid.startswith(('EV4-','EV5-')):continue
 if eid.startswith('EV4-'):
  assert v['strict_primary_locators']==all4['by_id'][eid]['confirmed_locators'];strict_num['EV4']+=len(v['strict_primary_locators']);continue
 path=B/v['source'];assert hashlib.sha256(raw(path)).hexdigest()==v['sha_or_oid']
 for a in v['strict_primary_locators']:
  if a['kind']=='json-pointer':assert digestval(ptr(jd(path),a['pointer']))==a['canonical_value_sha256']
  else:assert hashlib.sha256(raw(path).decode('utf-8-sig',errors='replace').splitlines()[int(a['line'])-1].encode()).hexdigest()==a['line_sha256']
  strict_num['EV5']+=1
assert len(updated)==report['counts']['distinct_criteria_measured_this_round']
nots=[k for k,v in states.items()if v=='NEEXECUTAT']; assert len(nots)==report['counts']['current_unexecuted']
nominal=defaultdict(set)
for _,_,_,r in cases:
 for eid,cid in r.items():nominal[eid].add(cid)
# Separate links to the same finding when two distinct criteria actually exercise its boundary.
multi={eid:sorted(q) for eid,q in nominal.items()if len(q)>1}
for eid,ids in multi.items():assert ev[eid]['level'] not in ('EXECUȚIE_COMPONENTĂ_ASERȚIUNE','SQL_PRODUS_PORTAT_POSTGRESQL','FUNCȚIE_CU_ORACOL_INDEPENDENT'),(eid,ids)
for src,h in report['sources'].items():assert sha(B/src)==h,src
for fn,h in report['artifact_hashes'].items():assert sha(R/fn)==h
allpg=rd(R/'sql_batch/executii.json')+rd(R/'sql_batch/recalibrare/executii.json');praw=[v for v in allpg if v['psql_exit'] is not None]; assert len(praw)==95 and all(x['fixture_closed']for x in praw)
markers=Counter(r['state']for j in praw for r in j['actual_assertions']);assert sum(markers.values())==2578
for p in [R/'sql_batch/executii.json',R/'sql_batch/recalibrare/executii.json']:
 for q in rd(p):
  for a,k in [('pglog','pglog_sha'),('sql','sql_sha'),('gen_log','gen_log_sha')]:
   if q.get(a)and q.get(k):assert sha(p.parent/q[a])==q[k],(a,q['task_suite'])
zh=rd(R/'probe/comparatie_C_W.json');assert len(zh['cases'])==8 and set(zh['task_scope'])=={'T20','T22','T35','T352','T354'} and 'EX08'not in zh['task_scope']['T352']['related_results']
assert sha(E/'supliment_CESIRO1/probe/EX08_peer_A12.json')=='2590f3f79ae88e32651c74c25cfa4593630b179a2c60701331c746b61c9bfd44'
met=R/'metoda';met.mkdir(exist_ok=True)
for n in ['a12_r3_survey.py','a12_r5_locators.py','a12_r5_ex08peer.py','a12_r5_sql_suite.py','a12_r5_sql_repair.py','a12_r5_sqlsecond.py','a12_r5_vectors.py','a12_r5_calibrated.py','a12_r5_make_matches.py','a12_r5_fetchcal3.py','a12_r5_profiles.py','a12_r5_core.py','a12_r5_cases.py','a12_r5_qa.py']:
 p=Path(__file__).parent/n
 if p.is_file():shutil.copyfile(p,met/n)
qa={'stage':'Contrôle technique de livraison, sans score indépendant.','utc':datetime.now(UTC).isoformat(),'checked_task_hashes':652,'current_html_hashes_verified':652,'R4_individual_source_sha_verified':652,'criteria_cases':'2619 exact same IDs and grouping as R4','all_bidirectional_edges':len(edges),'orphan_edges':0,'R4_strict_EVs':1220,'validated_locator_instances':strict_num,'EV5_fully_rehashed':sum(k.startswith('EV5-')for k in ev),'explicit_observed_criterion_ids':len(updated),'unexecuted':len(nots),'same_component_assertion_attributed_twice':False,'queue':1881,'historical_1868_set_preserved':True,'pg_fixtures_closed':95,'verified_native_SQL_test_markers':markers,'A11_score':None,'R5_report_sha':sha(R/'A12_raport.json'),'evidence_sha':sha(R/'Dovezi_criterii.json'),'registry_sha':sha(R/'Registru_reexecutare_R5.json'),'index_sha':sha(R/'Audit_individual_P01_R5.html')}
wr(R/'Verificare_R5.json',qa);print(json.dumps(qa,ensure_ascii=False));print('QA',sha(R/'Verificare_R5.json'))

