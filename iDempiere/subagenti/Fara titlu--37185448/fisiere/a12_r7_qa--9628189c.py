from a12_r7_pg_cui import *
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from functools import lru_cache
import shutil,base64
ROOT=E.parent;R=E/'R7';old=E/'R6';report=rd(R/'A12_raport.json');r6=rd(old/'A12_raport.json');by={v['task']:v for v in r6['records']};ed=rd(R/'Dovezi_criterii.json');ev=ed['evidence'];rev=ed['inverse_task_requirement_links'];q=rd(R/'Registru_reexecutare_R7.json')['records'];tri=rd(RP/'Clasificare_nominala_1587.json')['records'];reg={z['criterion']:z for z in q};scope={v['criterion']:v for v in tri}
def H(bb):return hashlib.sha256(bb).hexdigest()
def K(v):return H(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
@lru_cache(maxsize=512)
def data(p):return p.read_bytes()
@lru_cache(maxsize=256)
def jd(p):return rd(p)
def pt(v,s):
 if not s:return v
 for q in s[1:].split('/'):
  k=q.replace('~1','/').replace('~0','~');v=v[int(k)]if isinstance(v,list)else v[k]
 return v
def cs(w):return sum([w[f]for f in ['operative_criteria_and_audit_criteria','R3_new_criteria','R4_new_criteria']],[])
def link(c):
 l=[(c['source_evidence_id'],'source')]+[(z,'authority')for z in c.get('authority_evidence_ids',[])]
 for ph in ['closure','current']:l += [(z,ph)for z in c[ph]['evidence_ids']]
 for k,f,ph in [('component_assertion_crosscheck','ids','component_candidate'),('cross_financial_observation','evidence_ids','financial_context'),('installed_schema_probe','ids','metadata_context'),('archive_criterion_output','ids','historic_artifact_context')]:l += [(z,ph)for z in c.get(k,{}).get(f,[])]
 l += [(z,'case_context')for z in c.get('strict_related_sources_R5',[])];l +=[(z['evidence'],'R6_scenario')for z in c['R6_new_scenarios']]+[(z['evidence'],'R7_scenario')for z in c['R7_new_scenarios']]+[(z['evidence'],'R7_context')for z in c['R7_context']];return set(l)
def ver(rr):
 w=rd(R/rr['file']);assert sha(R/rr['file'])==rr['sha256']and sha(R/rr['html'])==rr['html_sha256'];oldr=by[rr['task']];assert sha(old/oldr['file'])==oldr['sha256']==rr['R6_sha'];prev=rd(old/oldr['file']);assert [c['id']for c in cs(w)]==[c['id']for c in cs(prev)];page=(R/rr['html']).read_text(encoding='utf8');assert page.count('<h1>')==1
 edge=set();st=Counter();cohort=set();audit=set();new=set();context=set()
 for c,p in zip(cs(w),cs(prev)):
  cid=c['id'];assert f'id="{cid}"'in page;st[c['current']['status']]+=1;edge.update((eid,rr['task'],cid,ph)for eid,ph in link(c))
  if p['current']['status']=='NEEXECUTAT':
   cohort.add(cid);ref=c['R7_cohort_position'];assert pt(jd(ROOT/ref['source']),ref['pointer'])['criterion']==cid;assert reg[cid]['R7_state']==c['current']['status'];assert ref['has_partial_external']==scope[cid]['has_partial_external']
  for v in c['R5_measured_scenarios']:
   if 'R7_recovered_predicate'in v:audit.add(v['evidence'])
  if c['R7_new_scenarios']:new.add(cid)
  if c['R7_context']:context.add(cid)
  for v in c['R7_new_scenarios']:assert v['evidence']in c['current']['evidence_ids']and v['expected']is not None and v['qualification']
 return edge,cohort,st,audit,new,context
with ThreadPoolExecutor(max_workers=10)as ex:checked=list(ex.map(ver,report['records']))
edges=set().union(*(x[0]for x in checked));inverse={(k,v['task'],v['criterion'],v['relation'])for k,r in rev.items()for v in r}
assert inverse==edges and not({z[0]for z in edges}-set(ev));cohort=set().union(*(x[1]for x in checked));assert cohort==set(scope)and len(scope)==1587 and sum(v['has_partial_external']for v in scope.values())==45;states=sum([x[2]for x in checked],Counter());assert sum(states.values())==2619 and states==report['counts']['states'];assert len(reg)==1881
covered=set().union(*(x[3]for x in checked));assert len(covered)==148
for k,v in ev.items():
 if k.startswith('EV7-'):
  p=ROOT/v['source'];assert H(data(p))==v['sha_or_oid'];assert K(pt(jd(p),v['pointer']))==v['strict_primary_locators'][0]['canonical_value_sha256']
 if k in covered:
  z=v['R7_runtime_source'];p=ROOT/z['file'];assert H(data(p))==z['sha'];row=pt(jd(p),z['pointer']);assert row['evidence']==k;cf=row['comparison'];log=RP/cf['trace_log'];assert H(data(log))==cf['log_sha'];l=data(log).decode('utf8').splitlines()[cf['trace_line']-1];assert l.startswith('ANCHOR:')and base64.b64decode(l.split('|')[0][7:]).decode().strip()==cf['r7_actual']
  for ref in cf['source_anchors']:
   sf=repo/ref['file'];a,b=ref['range'];assert sha(sf)==ref['sha']and sf.read_text(encoding='utf8').splitlines()[a-1:b]==ref['source_condition'].splitlines()
  if cf['code_state']=='GRUP_DE_ASERȚIUNI_APEL_IDENTIFICAT':assert cf['child_assertions']
for v,dig in report['inputs'].items():assert sha(ROOT/v)==dig
for v,dig in report['artifacts'].items():assert sha(R/v)==dig
pg=rd(RP/'SQL/Matrice_SQL_reala_R7.json')['rows'];assert len(pg)==20 and all(q['fixture_dropped']and q['exit']==0 for q in pg)and all(q['FAIL']>0 if q['variant']=='mutant'else q['FAIL']==0 for q in pg)
p=RP/'T06_cabinet_amprenta_integrala.json';d=rd(p);assert d['tests'][0]['before']==d['tests'][0]['after']==168 and d['tests'][0]['delta']==0 and d['tests'][0]['content_fingerprint_after']==d['tests'][0]['content_fingerprint_before']
w=(T7/'current_fixture_path.txt').read_text().strip();assert re.fullmatch('/tmp/eva-contab-codex-p01a12r7t06[.][a-zA-Z0-9]+',w);z=sp.run(['ssh','-o','BatchMode=yes',server,'cd '+w+" && grep -E '^CLEANED|remaining_owned_containers=' supervisor-log && docker ps -a --filter label=eva.sesiune=eva-contab-codex-p01a12r7t06 --format '{{.Names}}' | wc -l"],stdout=sp.PIPE,stderr=sp.PIPE,timeout=10);assert z.returncode==0 and 'CLEANED' in z.stdout.decode()and z.stdout.decode().splitlines()[-1]=='0';clean=z.stdout.decode().splitlines()
for n in ['a12_r3_survey.py','a12_r6_exec.py','a12_r7_pg_cui.py','a12_r7_lease_dest.py','a12_r7_cabinet_test.py','a12_r7_run_cab.py','a12_r7_cab168.py','a12_r7_cab_sig.py','a12_r7_pg_suites.py','a12_r7_pg_joblock.py','a12_r7_stack.py','a12_r7_stack79.py','a12_r7_stack_recover.py','a12_r7_atomic.py','a12_r7_ledger.py','a12_r7_classify.py','a12_r7_sourcechecks.py','a12_r7_prepare_results.py','a12_r7_publish.py','a12_r7_qa.py']:
 shutil.copyfile(Path(__file__).parent/n,R/'metoda'/n)
qa={'utc':datetime.now(UTC).isoformat(),'stage':'Control de integritate A12, fără notă unilaterală.','json_cases_checked':len(checked),'html_and_source_R6_immutable_checked':len(checked),'criteria_same_order_as_R6':sum(states.values()),'R6_entire_1587_classified':True,'partial_external_cases':45,'local_only_cases':1542,'EV5_missing_recovered_and_source_hash_checked':len(covered),'predicate_types':Counter(z['comparison']['code_state']for z in rd(RP/'148_predicate_prin_stack.json')['rows']),'direct_criteria':len(set().union(*(x[4]for x in checked))),'context_criteria':len(set().union(*(x[5]for x in checked))),'EV7_pointer_and_source_checked':sum(k.startswith('EV7-')for k in ev),'edges_verified_symmetric':len(edges),'orphan':0,'postgres_variants_executed_and_dropped':20,'original_markers_count':sum(v['OK']for v in pg if v['variant']=='original'),'mutants_detected_count':sum(v['FAIL']>0 for v in pg if v['variant']=='mutant'),'T06_native_after_168_fingerprint_verified':True,'exclusive_synthetic_slot_closed':clean,'remaining_NEEXECUTAT':states['NEEXECUTAT'],'R7_score':None,'report_sha':sha(R/'A12_raport.json'),'queue_sha':sha(R/'Registru_reexecutare_R7.json'),'catalog_sha':sha(R/'Dovezi_criterii.json'),'html_sha':sha(R/'Audit_individual_P01_R7.html')}
wr(R/'Verificare_R7.json',qa);print(qa);print('QA SHA',sha(R/'Verificare_R7.json'))

