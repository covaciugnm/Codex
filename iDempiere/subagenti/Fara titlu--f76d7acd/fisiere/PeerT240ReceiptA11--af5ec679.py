from pathlib import Path
import json,hashlib,zipfile,csv,io,datetime,sys,re
sys.stdout.reconfigure(encoding='utf8')
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');O=R/'executie/R12_fisiere/A11/T240_lot01';D=O/'Peer_receptie_T240'
def H(b):return hashlib.sha256(b).hexdigest()
def h(p):return H(p.read_bytes())
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':h(p)}
checks=[]
def chk(name,condition,details=None):
 checks.append({'check':name,'passed':bool(condition),'details':details});assert condition,(name,details)
v=O/'Verdict_A11_R12_T240_lot01_v1.json';s=O/'Sigiliu_A11_receptie_T240_lot01_v1.json';c=O/'Checklist_A11_dupa_T240_lot01_v1.json';w=O/'Control_independent_T240_titlu_E_v1.json'
chk('verdict hash',h(v)=='3d0bdd5cfc5010cf8cdd994a4c7d1ed2205f3d973250eb9592129cc5a55ea371')
chk('seal hash',h(s)=='23d6eee3345cf05a84e5a7ffe4dd9cb8d76e49f943d2d8ac52b27f22311462c8')
seal=j(s);ver=j(v);checklist=j(c);witness=j(w)
for f in seal['artifacts']:chk('sealed '+f['path'],h(R/f['path'])==f['sha256'])
inputzip=R/witness['input_fixture_archive']['path'];outzip=R/witness['artifacts'][0]['path']
chk('two distinct archive roles',inputzip!=outzip and h(inputzip)==witness['input_fixture_archive']['sha256'] and h(outzip)==witness['artifacts'][0]['sha256'])
with zipfile.ZipFile(inputzip) as a,zipfile.ZipFile(outzip) as z:
 source=z.read('verifica_proba.py')
 chk('exact source both archives',source==a.read('verifica_proba.py') and H(source)==witness['source']['sha256'])
 chk('exact Git blob',hashlib.sha1(b'blob '+str(len(source)).encode()+b'\0'+source).hexdigest()==witness['source']['git_object'])
 text=source.decode('utf8');lines=text.splitlines()
 chk('source contract E col2','E col. 2' in lines[7] or 'E col. 2' in text[:2000])
 chk('source drops E col2',"r.append(l.split('\\t')[0].strip())" in text)
 chk('source trusts TSV inventory label',"not tf.endswith(' — ' + r['titlu_inventar'])" in text)
 chk('baseline originates in general input archive',z.read('baseline/raport.tsv')==a.read('positive/raport.tsv') and z.read('baseline/ecrane.tsv')==a.read('positive/ecrane.tsv'))
 chk('4 expected R3 case identifiers',[x['id'] for x in witness['cases']]==['baseline','display_only','report_title_triple_forged','inventory_second_column_changed'])
 rows_by_case={};inventory_by_case={}
 for case in witness['cases']:
  name=case['id'];rraw=z.read(name+'/raport.tsv');eraw=z.read(name+'/ecrane.tsv')
  chk('archived report hash '+name,H(rraw)==case['report_sha256'])
  chk('archived E hash '+name,H(eraw)==case['inventory_sha256'])
  chk('archived stdout '+name,z.read(name+'/stdout.txt').decode('utf8').replace('\r\n','\n')==case['stdout'])
  chk('archived stderr '+name,z.read(name+'/stderr.txt').decode('utf8').replace('\r\n','\n')==case['stderr'])
  rs=list(csv.DictReader(io.StringIO(rraw.decode('utf8')),delimiter='\t'));es={x[0]:x[1] for x in csv.reader(io.StringIO(eraw.decode('utf8')),delimiter='\t')}
  violations=[(r['ecran'],r['limba']) for r in rs if r['tip']!='REGES' and not r['titlu_afisat'].endswith(' — '+es[r['ecran']])]
  declared=[(x['screen'],x['language']) for x in case['inventory_mismatches']]
  chk('independent E-col2 oracle '+name,violations==declared and bool(not violations)==case['independent_inventory_oracle_accepts'])
  rows_by_case[name]=rs;inventory_by_case[name]=es
 chk('no inventory change in triple forged',inventory_by_case['baseline']==inventory_by_case['report_title_triple_forged'])
 diff=[(i,k) for i,(b,f) in enumerate(zip(rows_by_case['baseline'],rows_by_case['report_title_triple_forged'])) for k in b if b[k]!=f[k]]
 chk('only3 declared report fields changed',set(diff)=={(0,'titlu_asteptat'),(0,'titlu_afisat'),(0,'titlu_inventar')})
 chk('E-only case report unchanged',rows_by_case['baseline']==rows_by_case['inventory_second_column_changed'])
 chk('observed rc vector as stated',[x['component_exit'] for x in witness['cases']]==[0,1,0,0])
 chk('both false accepts have13of13',all('13/13 conforme' in x['stdout'] for x in witness['cases'][2:]))
method=(O/'A11R12T240InventoryTitle.py').read_text(encoding='utf8')
chk('reproducer extracts own baseline and invokes exact CLI',"baseline={x:z.read(x) for x in z.namelist() if x.startswith('positive/')" in method and "str(scratch/'verifica_proba.py'),str(d),'--ecrane'" in method)
chk('R3 P2 confined to helper',ver['findings_disposition'][0]['priority']=='P2 — corectitudinea uneltei de recepție' and 'Nicio eroare UI reală' in ver['findings_disposition'][0]['business_scope'])
chk('scores limited',ver['scores']['execution_entire_audit'] is None and ver['scores']['product'] is None and ver['scores']['task'] is None)
chk('zero complete coverage',all(ver['coverage'][k]==0 for k in ['complete_files_received','complete_tasks_received','complete_contracts_received']))
measure=ver['accepted_measurements']
chk('46 original baseline distinct',measure['baseline_original_without_mutants']['cases']==measure['baseline_original_without_mutants']['passed']==46 and measure['baseline_original_without_mutants']['skipped']==0)
chk('33 mutants7batches1518 evaluations',measure['mutants_original_functions_in_batches']['batches']==7 and measure['mutants_original_functions_in_batches']['distinct_original_mutants']==measure['mutants_original_functions_in_batches']['detected']==33 and measure['mutants_original_functions_in_batches']['evaluations']==33*46)
chk('main timeout noPASS',measure['full_original_program']['status']=='TIMEOUT60' and measure['full_original_program']['exit_success'] is False and measure['full_original_program']['credit']==0)
chk('metrics not summed',measure['additional_methods']['not_unique_test_sum'] is True)
ar=R/'executie/R12_fisiere/A08_T240/Lot_01_final_v1/Raport_A08_T240_R12_lot01_v1.json';aj=j(ar)
chk('A08 report fixed',h(ar)=='b787ebbacdbed52aa5dfb3ac8b61d4e2ad331d043b489306b110986afbe5aa69')
chk('A08 no native whole claims',aj['native_UI_or_ERP_executed'] is False and aj['whole_task_verdict'] is None and aj['whole_file_verdict'] is None)
ex=R/'executie/R12_fisiere/A08_T240/2026-11-02T23-17-56Z/Execution.json';x=j(ex);modes={x['mode']:x for x in x['records']}
chk('primary execution distinguishes timeout',modes['original']['exit_code']==0 and modes['original_full']['timed_out'] is True and modes['original_full']['exit_code'] is None)
chk('mutant identities33unique',sorted(x['index'] for x in aj['mutants'])==list(range(33)) and all(x['status']=='UCIS' and len(x['case_results'])==46 and x['witnesses'] for x in aj['mutants']))
chk('remaining instrument exact set',[x['instrument'] for x in checklist['remaining_new_instruments']]==['R12-I%02d'%i for i in range(1,18)])
chk('remaining contract exact set',[x['id'] for x in checklist['remaining_contracts']]==['D%02d'%i for i in range(1,18)] and all(x['status'].startswith('DESCHIS') for x in checklist['remaining_contracts']))
chk('checklist has native preparation and no externalblock',any(x['id']=='N08' and x['status']=='REALIZABIL_INTERN_NU_BLOCAJ_EXTERN' for x in checklist['next_actions']) and checklist['outside_dependency_required_now'] is False)
D.mkdir(exist_ok=True)
report={'schema':'peer.A11.T240.receipt.semantic.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'author':'peer_t240_receipt, independent de emitentul verdictului A11','scope':'Lectură/verificare semantică și hashuri; zero rerulări produs, zero rescrieri de dovezi.','inputs':[ref(v),ref(s),ref(w),ref(c),ref(inputzip),ref(outzip),ref(ar),ref(ex)],'checks':checks,'decision':'ADMIS — nu am identificat supralicitare de acoperire sau contradicție între probe și recepția limitată.','conclusions':['R3/Ecol2 este demonstrat de4 fixture și sursa exactă:2 acceptări false față de numele E. P2 se referă la judecătorul de dovezi, nu la UI nativă.','Arhiva generală este intrare de fixture/sursă; arhiva de titlu conține cele4 execuții. Distincția este corectă și explicită.','46baseline și33mutanți în7loturi sunt măsurători distincte;1518 sunt evaluări reutilizând46cazuri. Main timeout60 nu este primit PASS.','17instrumente restante și17contracte sunt păstrate deschise; zero taskuri/fișiere/fluxuri native recepționate integral.'],'limits':['Nu am rerulat produsul; confruntarea proprie a oracolului citește bytes TSV și E din arhiva originală.','Nota10/10 rămâne numai planului v2.','Nu revalidez toate195 controalele mecanice A11 și nu primesc valul nominal A12 încă nepredat.'],'product_execution':False,'operational_writes':0,'prior_artifact_mutations':0,'check_count':len(checks),'all_passed':all(x['passed'] for x in checks),'method':{'path':str(Path(__file__)),'sha256':h(Path(__file__))}}
rp=D/'Peer_receptie_T240_v1.json';assert not rp.exists();rp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
sp=D/'Sigiliu_peer_receptie_T240_v1.json';assert not sp.exists();sp.write_text(json.dumps({'utc':report['utc'],'report':ref(rp),'inputs':report['inputs'],'method':report['method']},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'report':ref(rp),'seal':ref(sp),'checks':len(checks)},ensure_ascii=False))
