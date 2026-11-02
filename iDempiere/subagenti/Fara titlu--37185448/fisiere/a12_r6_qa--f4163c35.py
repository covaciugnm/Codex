from a12_r3_survey import *
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from functools import lru_cache
from datetime import datetime,UTC
from pathlib import Path
import shutil
R=E/'R6';R5=E/'R5';report=rd(R/'A12_raport.json');r5=rd(R5/'A12_raport.json');r5m={x['task']:x for x in r5['records']};cat=rd(R/'Dovezi_criterii.json');ev=cat['evidence'];rev=cat['inverse_task_requirement_links']
@lru_cache(maxsize=512)
def source(p):return p.read_bytes()
@lru_cache(maxsize=256)
def jd(p):return rd(p)
def ptr(v,t):
 if t=='':return v
 for x in t[1:].split('/'):
  k=x.replace('~1','/').replace('~0','~');v=v[int(k)]if isinstance(v,list)else v[k]
 return v
def J(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def checks(w):return sum([w[k]for k in ['operative_criteria_and_audit_criteria','R3_new_criteria','R4_new_criteria']],[])
def rels(c):
 l=[(c['source_evidence_id'],'source')]+[(z,'authority')for z in c.get('authority_evidence_ids',[])]
 for k in ['current','closure']:l += [(z,k)for z in c[k]['evidence_ids']]
 for f,key,rel in [('component_assertion_crosscheck','ids','component_candidate'),('cross_financial_observation','evidence_ids','financial_context'),('installed_schema_probe','ids','metadata_context'),('archive_criterion_output','ids','historic_artifact_context')]:l += [(z,rel)for z in c.get(f,{}).get(key,[])]
 l += [(z,'case_context')for z in c.get('strict_related_sources_R5',[])]+[(z['evidence'],'R6_scenario')for z in c.get('R6_new_scenarios',[])];return set(l)
def chk(x):
 f=R/x['file'];hp=R/x['html'];assert sha(f)==x['sha256']and sha(hp)==x['html_sha256'];w=rd(f);r5row=r5m[x['task']];p=R5/r5row['file'];assert sha(p)==r5row['sha256']==x['R5_source_sha'];old=rd(p)
 oldc=checks(old);nc=checks(w);assert [z['id']for z in nc]==[z['id']for z in oldc]and len(nc)==x['criteria']
 t=hp.read_text(encoding='utf8');assert t.count('<h1>')==1
 refs=set();reg=set();count=Counter();ids=set();actual=set()
 for c in nc:
  cid=c['id'];assert f'id="{cid}"'in t;refs.update((eid,x['task'],cid,rel)for eid,rel in rels(c));reg.add(cid)if 'R6_register_position' in c else None;count[c['current']['status']]+=1
  if c.get('R6_numerical_R5_review'):ids.add(cid)
  alt=c.get('R6_new_scenarios',[]);actual.update([cid]if alt else [])
  for z in c['R5_measured_scenarios']:assert len(z['R6_oracle_ref']['sha'])==64 and z['R6_automatic_credit']is False
  for z in alt:assert z['asserted_expected']and z['remaining_scope']and z['evidence'] in c['current']['evidence_ids']
 return refs,reg,count,ids,actual
with ThreadPoolExecutor(max_workers=10)as pool:o=list(pool.map(chk,report['records']))
edges=set().union(*(x[0]for x in o));back={(z,r['task'],r['criterion'],r['relation'])for z,rows in rev.items()for r in rows};assert edges==back and not ({v[0]for v in edges}-ev.keys());reg=set().union(*(x[1]for x in o));co=sum([x[2]for x in o],Counter());scopes=set().union(*(x[3]for x in o));new=set().union(*(x[4]for x in o));assert len(scopes)==108 and len(reg)==1881 and sum(co.values())==2619 and len(r5m)==len(report['records'])==652
table=rd(R/'Registru_reexecutare_R6.json')['records'];assert set(z['criterion']for z in table)==reg
assert all(z['individual_next_step']and z['R6_case_next_action']and z['resource_boundaries']['requires_external_or_hardware'] in (True,False) for z in table)
assert sum(bool(r.get('R5_next_step_was_empty'))for r in table)==81 and {r['criterion']for r in table if r['original_1868']}=={r['criterion']for r in rd(R5/'Registru_reexecutare_R5.json')['records']if r['original_1868']}
n=0
for k,v in ev.items():
 if k.startswith('EV5-'):
  a=v['R6_oracle_locator'];p=B/a['source'];assert hashlib.sha256(source(p)).hexdigest()==a['sha256']and J(ptr(jd(p),a['pointer']))==a['canonical_value_sha256'];n+=1
 if not k.startswith('EV6-'):continue
 p=B/v['source'];assert hashlib.sha256(source(p)).hexdigest()==v['sha_or_oid']
 for a in v['strict_primary_locators']:
  if a['kind']=='text-line':assert hashlib.sha256(source(p).decode('utf-8-sig',errors='replace').splitlines()[a['line']-1].encode()).hexdigest()==a['line_sha256']
  else:assert J(ptr(jd(p),a['pointer']))==a['canonical_value_sha256']
assert n==487 and set(report['counts']['raw_states'])==set(co) and dict(co)==report['counts']['raw_states']
for p,h in report['inputs'].items():assert sha(B/p)==h,p
for p,h in report['artifact_hashes'].items():assert sha(R/p)==h,p
ann=rd(R/'probe/Anexe_1611_pentru_fisa.json')['records'];assert len(ann)==1611 and sum(bool(v['historical_controls'])for v in ann)==99
assert sum(bool(r['resource_boundaries']['requires_external_or_hardware'])for r in table if not r['original_1868'])==1
src=Path(__file__).parent
for p in [src/'a12_r3_survey.py',*[f for f in src.glob('a12_r6_*.py')if f.name!='a12_r6_screen.py']]:shutil.copyfile(p,R/'metoda'/p.name)
qa={'utc':datetime.now(UTC).isoformat(),'stage':'Control A12 al integrității livrării, nicio notă de produs sau de audit decise unilateral.','tasks':652,'individual_json_and_html_read_back':652,'R5_immutable_all_652_sha':True,'criteria_exact_same_sequence_as_R5':2619,'edges':len(edges),'asymmetric_or_dangling':0,'all_487_EV5_expected_or_gap_pointers_reopened':n,'same_108_criteria_reviewed':len(scopes),'new_criteria_individually_tested_or_documented':len(new),'EV6_new_strict_locators_opened':sum(k.startswith('EV6-')for k in ev),'81_empty_now_filled':81,'13_external_flags_classified':True,'historical_archives':{'reviewed_for_cases':1611,'matching_criteria':99,'verified_line_references':sum(len(q['historical_controls'])for q in ann)},'current_neexecutat':co['NEEXECUTAT'],'audit_quality_or_product_score':None,'report_sha':sha(R/'A12_raport.json'),'catalog_sha':sha(R/'Dovezi_criterii.json'),'queue_sha':sha(R/'Registru_reexecutare_R6.json'),'html_sha':sha(R/'Audit_individual_P01_R6.html')}
wr(R/'Verificare_R6.json',qa);print(json.dumps(qa,ensure_ascii=False));print('SHA QA',sha(R/'Verificare_R6.json'))

