import pathlib,json,hashlib,ast,re,datetime,sys,copy
sys.stdout.reconfigure(encoding='utf8')
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere/A08_T240';F=B/'Lot_01_final_v1';O=R/'executie/R12_fisiere/A11/T240_lot01'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':h(p),'bytes':p.stat().st_size}
manifest=F/'MANIFEST_A08_T240_R12_lot01_v1.json';report=F/'Raport_A08_T240_R12_lot01_v1.json'
assert h(manifest)=='c4fdf5311d70f9dcbdbb37c24db802021065b34162accc98525dd40ad4514c4d'
assert h(report)=='b787ebbacdbed52aa5dfb3ac8b61d4e2ad331d043b489306b110986afbe5aa69'
m=j(manifest);r=j(report);refs=[];checks=[]
def check(label,ok,detail=None):
 checks.append({'check':label,'passed':bool(ok),'detail':detail});assert ok,(label,detail)
def walk(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and x['path'].startswith('executie/') and 'sha256' in x:
   p=R/x['path'];assert p.is_file() and h(p)==x['sha256'],x
   if 'bytes' in x:assert p.stat().st_size==x['bytes'],x
   refs.append(x)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(m);walk(r)
check('manifest_owns89_artifacts',len(m['files'])==89)
check('candidate_exact',r['head']=='df85d33c1648ce2b2df130a60a05ef696e2e5480')
source_bytes={}
for s in r['sources']:
 p=R/s['local_evidence']['path'];raw=p.read_bytes();source_bytes[p.name]=raw
 check('source_SHA_OID_'+p.name,h(p)==s['sha256'] and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==s['git_oid'])
 check('matches_frozen_plan_copy_'+p.name,raw==(R/'executie/R12_plan_delta/Sources_lues'/s['path']).read_bytes())
tree=ast.parse(source_bytes['test_clasa_verifica_proba.py'].decode('utf8'));assignments={t.id:n.value for n in tree.body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}
mutants=ast.literal_eval(assignments['MUTANTI']);names=[ast.literal_eval(t.elts[0]) for t in assignments['CAZURI'].elts]+[ast.literal_eval(t.elts[0]) for t in assignments['CAZURI_FIS'].elts]+['Perioade în afara E']
check('original_case_inventory46_unique',len(names)==46 and len(set(names))==46)
baseline=(B/'2026-11-02T23-17-56Z/original.stdout.txt').read_text(encoding='utf8').splitlines()
parsed=[re.match(r'^OK (.+?) \(rc (\d+)\): (.*)$',line) for line in baseline if line.startswith('OK ')]
check('baseline46_declared_names_exact',len(parsed)==46 and all(parsed) and [p.group(1) for p in parsed]==names)
check('baseline_final46of46',baseline[-1]=='cazuri: OK 46/46')
exec0=j(B/'2026-11-02T23-17-56Z/Execution.json');modes={x['mode']:x for x in exec0['records']}
check('original_baseline_rc0_unmodified',modes['original']['exit_code']==0 and not modes['original']['timed_out'])
check('full_main_timeout_no_credit',modes['original_full']['timed_out'] and modes['original_full']['exit_code'] is None and r['counts']['full_original_program_with_mutants'].startswith('TIMEOUT60'))
check('unused_selected_branch_not_executed','selected' not in modes)
judge=source_bytes['verifica_proba.py'].decode('utf8');actual=[];batchdir=B/'Supplement_2026-11-02T23-23-08Z'
for p in sorted(batchdir.glob('mutants_*/result_mutants_*.json')):
 d=j(p);evt=[json.loads(x) for x in p.with_name('events_'+d['mode']+'.jsonl').read_text(encoding='utf8').splitlines() if x]
 check('batch_events_equal_'+d['mode'],evt==d['mutants'])
 ex=j(p.parent/'Execution.json');check('batch_success_'+d['mode'],ex['exit_code']==0 and ex['timeout'] is False)
 for x in d['mutants']:
  n,old,new=mutants[x['index']];muttext=judge.replace(old,new);poss={hashlib.sha256(muttext.encode()).hexdigest():'LF',hashlib.sha256(muttext.replace('\n','\r\n').encode()).hexdigest():'CRLF'}
  check('mutant_anchor_hash_'+str(x['index']),x['name']==n and x['occurrences']==judge.count(old)==1 and x['mutant_sha256'] in poss)
  check('mutant_cases_'+str(x['index']),len(x['case_results'])==46 and [c['name'] for c in x['case_results']]==names)
  witnesses=[c['name'] for c in x['case_results'] if not c['original_expectation_passed']]
  check('mutant_genuine_witness_'+str(x['index']),x['status']=='UCIS' and bool(witnesses) and witnesses==x['witnesses'])
  final=next(v for v in r['mutants'] if v['index']==x['index']);check('mutant_report_matches_log_'+str(x['index']),all(final[k]==v for k,v in x.items()))
  actual.append(x)
check('mutant_0_to32_disjoint_complete',sorted(x['index'] for x in actual)==list(range(33)) and len(actual)==33)
check('mutation1518_not_new_tests',sum(len(x['case_results']) for x in actual)==1518 and r['counts']['mutation_case_evaluations']==1518)
ind=j(B/'2026-11-02T23-17-56Z/result_independent.json')
check('20_independent_cases_exact',len(ind['cases'])==len(r['cases_A08'])==20 and all(all(final.get(k)==v for k,v in original.items()) for original,final in zip(ind['cases'],r['cases_A08'])), 'Raportul final adaugă controale/cerințe/referințe; toate câmpurile originale rămân identice.')
for c in ind['cases']:
 f=B/'2026-11-02T23-17-56Z'/(c['case_id']+'_report.tsv');check('preserved_fixture_'+c['case_id'],h(f)==c['files_after']['raport.tsv'] and c['source_inputs_unchanged'] and c['files_before']==c['files_after'])
check('unicode_CLI_refuses',j(batchdir/'cli_utf8/Execution.json')['exit_code']==1 and 'UnicodeDecodeError' in (batchdir/'cli_utf8/stderr.txt').read_text(encoding='utf8'))
check('performance_measured_parser_only',r['performance']['max_judge_seconds']==max(c['elapsed_seconds'] for c in ind['cases'] if c['case_id'] in r['performance']['cases']) and 'nu este RSS' in r['performance']['measurement_limit'])
for x in r['cleanup']:
 d=j(R/x['path']);root=d.get('root') or d.get('owned_absolute_target') or d.get('owned_target')
 check('cleanup_'+pathlib.Path(x['path']).parent.name,d['removed'] and (not pathlib.Path(root).exists() if root else True))
check('no_native_or_whole_credit',r['native_UI_or_ERP_executed'] is False and r['whole_task_verdict'] is None and r['whole_file_verdict'] is None)
check('13_RO_fixture_no12_credit',ind['fixture_count']=={'RO':13,'EN_TEXTE':10,'EN_PERIOADE':1,'total':24})
output={'schema':'A11.R12.T240.receipt_controls.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':[ref(manifest),ref(report)],'references_rehashed':len(refs),'unique_files_rehashed':len(set(x['path'] for x in refs)),'checks':checks,'independent_active_witnesses':[ref(O/'Control_independent_T240_v1.json'),ref(O/'Control_independent_T240_titlu_E_v1.json'),ref(O/'QA_A11_T240_martori_v1.json')],'method':{'path':str(pathlib.Path(__file__)),'sha256':h(pathlib.Path(__file__))},'summary':{'checks':len(checks),'passed':sum(c['passed'] for c in checks),'baseline':46,'mutants':33,'mutation_evaluations':1518,'A08_independent':20,'A08_UTF8_CLI':1,'A11_independent_CLI':19,'not_additive_as_unique_tests':True,'full_original_main_pass':False,'native_product_tested':False}}
dest=O/'Control_A11_receptie_A08_T240_v1.json';assert not dest.exists();dest.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'artifact':ref(dest),'summary':output['summary'],'refs':len(refs)},ensure_ascii=False))
