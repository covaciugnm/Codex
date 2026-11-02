from a12_r3_survey import *
import shutil,concurrent.futures as cf,collections,datetime
R=E/'R4';R3=E/'R3';report=rd(R/'A12_raport.json');actions=rd(R/'Registru_1868.json');cata=rd(R/'Dovezi_criterii.json');catalog=cata['evidence'];used=set();csco=collections.Counter();extra=set();normative=0
def dig(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
r3=rd(R3/'A12_raport.json');old3={w['task']:w for w in r3['records']};r1={w['id']:w for w in rd(E/'R1/A12_raport.json')['records']};r2={w['task']:w for w in rd(E/'R2/A12_raport.json')['records']};q1868={x['criterion']:x for x in actions['records']};assert len(q1868)==len(actions['records'])==1868;assert set(report['records'][0])>={'file','sha256','html','html_sha256'};assert len(set(x['task']for x in report['records']))==652
def case(x):
 k=x['task'];pp=R/x['file'];w=rd(pp);hp=R/x['html'];assert dig(pp)==x['sha256'] and dig(hp)==x['html_sha256'] and hp.read_text(encoding='utf8').count('<h1>')==1
 a=old3[k];assert dig(R3/a['file'])==a['sha256']==x['R3_sha'];orig=rd(R3/a['file'])
 if k!='T352':assert dig(E/'R1'/r1[k]['file'])==r1[k]['sha256']and dig(E/'R2'/r2[k]['file'])==r2[k]['sha256']
 origc=[*orig['operative_criteria_and_audit_criteria'],*orig['R3_new_criteria']];now=[*w['operative_criteria_and_audit_criteria'],*w['R3_new_criteria'],*w['R4_new_criteria']];assert len({c['id']for c in now})==len(now)==x['checks'];assert len(w['R4_control_register'])==36 and 'A11_score_R4'in w and w['A11_score_R4']is None
 orneed={c['id']for c in origc if c['current']['status']=='NEEXECUTAT'};assert set(w['R4_first_1868_action_ids'])==orneed;used=set();refs=set();local=collections.Counter()
 for c in now:
  assert c['source_evidence_id'] and c['expected_oracle'] and c['next_action'];links=[(c['source_evidence_id'],'source')]+[(i,'authority')for i in c.get('authority_evidence_ids',[])]
  for phase in ('closure','current'):
   dd=c[phase]
   if dd.get('observed')is not None:assert dd['evidence_ids'],(k,c['id'],phase)
   links += [(i,phase)for i in dd['evidence_ids']]
  for f,field,rel in [('component_assertion_crosscheck','ids','component_candidate'),('cross_financial_observation','evidence_ids','financial_context'),('installed_schema_probe','ids','metadata_context'),('archive_criterion_output','ids','historic_artifact_context')]:
   links += [(i,rel)for i in c.get(f,{}).get(field,[])]
  for eid,relationship in links:
   assert eid in catalog,(k,c['id'],eid);used.add((eid,k,c['id'],relationship))
   if eid.startswith('EV4-'):refs.add(eid)
  local[c['current']['status']]+=1
  if c['id']in orneed:
   q=q1868[c['id']];assert q['current_disposition']==c['current']['status'] and q['task']==k and q['fixture_independent_of_observation'] and q['negative_or_counterexample'] and q['designated_entry_and_evidence'] and q['zone_owner'];assert q['resource_split']['do_not_block_local_steps'] and q['resource_split']['requires_external_or_hardware']==q['requires_external_or_hardware']
 return k,used,orneed,local,refs
refs=set()
with cf.ThreadPoolExecutor(max_workers=9)as ex:
 for k,links,base,count,evr in ex.map(case,report['records']):
  used.update(links);extra.update(base);csco.update(count);refs.update(evr)
reverse={(eid,y['task'],y['criterion'],y['relation'])for eid,ds in cata['inverse_task_requirement_links'].items()for y in ds};assert used==reverse and extra==set(q1868)
seen={}
for eid in refs:
 v=catalog[eid];p=v['source']
 if p.startswith('executie/R4/'):
  f=R/p[len('executie/R4/'):];path=str(f)
  if path not in seen:seen[path]=dig(f)
  assert seen[path]==v['sha_or_oid'],(eid,path)
for z,hash_ in report['current_input_hashes'].items():assert dig(R/'inputs'/z)==hash_
for y in rd(R/'Java/executii.json')+rd(R/'Java/executii2.json')+rd(R/'Java/scaner.json')+rd(R/'Java/retry/executii.json'):
 assert dig(R/'Java'/y['log'])==y['log_sha256'],y['suite']
for y in rd(R/'Java/scan_calibrat/observat.json'):assert dig(R/'Java/scan_calibrat'/y['log'])==y['log_sha256'] and y['screen_connection']==['legatura: 15/15'] and y['rc']==0
for k in ('GardenAdmin','GardenUser'):
 v=rd(R/'T259_ZK'/(k+'.json'));assert v['exact_pairs_equal'] and not v['visible_error'] and v['result']=='PASS_LITERAL_DOM' and len(v['expected'])==4 and dig(R/'T259_ZK'/(k+'_tab.png'))==v['screenshot_sha256']
assert len(rd(R/'T259_ZK/test_original_versionat.json'))==5
assert all(q1868[x]['requires_external_or_hardware']for x in ('T351-R2-001','T351-R2-002','T328-R2-003','T328-R2-004'))and not q1868['T328-R2-002']['requires_external_or_hardware']
w=rd(R/'taskuri/Fisa_T352.json');assert next(v for v in w['R3_new_criteria'] if v['id']=='T352-R09')['current']['status']=='PROVENIENȚĂ_VERIFICATĂ_T352_NEMONTAT_5_DIN_5';assert report['counts']['edge_count']==len(used) and report['counts']['checks_current']==sum(csco.values())
m=R/'metoda';m.mkdir(exist_ok=True);tmp=Path(__file__).parent
for f in ['a12_r4_run.py','a12_r4_recovery_map.py','a12_r4_legacy.py','a12_r4_anchors.py','a12_r4_extra.py','a12_r4_suites.py','a12_r4_more_suites.py','a12_r4_devicesuites.py','a12_r4_scan_retry.py','a12_r4_retry.py','a12_r4_history.py','a12_r4_more.py','a12_r4_attribution.py','a12_r4_static.py','a12_r4_ad.py','a12_r4_ai.py','a12_r4_archive_criteria.py','a12_r4_zk.py','a12_r4_uitest.py','a12_r4_t259_archive.py','a12_r4_android.py','a12_r4_dependencies.py','a12_r4_qa.py']:
 shutil.copyfile(tmp/f,m/f)
# Required code dependencies for reproducing the read-only extraction/replays are the frozen archived R3 method libraries.
for f in ['a12_r3_survey.py','a12_r3_java.py']:shutil.copyfile(E/'R3/metoda'/f,m/f)
qa={'stage':'Control structural A12 la predare; fără punctaj independent.','time':datetime.datetime.now(datetime.UTC).isoformat(),'case_ids_total':652,'per_case_hashes_checked':652,'html_hashes_read_back':652,'previous_r3_individual_records_checked':652,'previous_r1_and_r2_individual_records_checked':651,'all_r3_1868_old_NEEXECUTAT_ids_equal_R4_register':True,'active_2619_checks':sum(csco.values()),'all_symmetric_links':len(used),'dangling_or_asymmetric':0,'EV4_unique_local_source_bytes_verified':len(seen),'EV4_requirement_evidence_IDs_verified':len(refs),'new_physical_and_external_count':sum(v['requires_external_or_hardware'] for v in q1868.values()),'state_distribution':csco,'T259_original_UI_test_and_2_independent_roles_OK':True,'T352_nominal_status_correct':True,'score':None,'report_sha':dig(R/'A12_raport.json'),'catalog_sha':dig(R/'Dovezi_criterii.json'),'html_sha':dig(R/'Audit_individual_P01_R4.html'),'action_register_sha':dig(R/'Registru_1868.json')}
wr(R/'Verificare_R4.json',qa);print(qa['report_sha'],qa['catalog_sha'],qa['html_sha'],qa['action_register_sha'],dig(R/'Verificare_R4.json'))

