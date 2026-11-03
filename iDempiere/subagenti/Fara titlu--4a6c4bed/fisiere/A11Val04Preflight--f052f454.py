import json,pathlib,hashlib,datetime
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';O=B/'A11/Val04_preflight';O.mkdir(parents=True,exist_ok=True)
oldp=R/'executie/delta/2026-11-03T00-39-34-490Z';newp=R/'executie/delta/2026-11-03T01-43-37-057Z'
def raw(p):return p.read_bytes()
def sha(p):return hashlib.sha256(raw(p)).hexdigest()
def j(p):return json.loads(raw(p).decode('utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':len(raw(p))}
def write(p,d):
 assert not p.exists(),str(p)
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
checks=[]
def ck(n,b,detail=None):
 checks.append({'check':n,'ok':bool(b),'detail':detail});assert b,(n,detail)
old=j(oldp/'00_STATUS_TASKURI.json');new=j(newp/'00_STATUS_TASKURI.json');key=lambda x:(x.get('proiect'),x['id'])
om={key(x):(i,x) for i,x in enumerate(old)};nm={key(x):(i,x) for i,x in enumerate(new)}
ck('unambiguous project+id identity',len(om)==len(old)==996 and len(nm)==len(new)==997)
ck('P01 population 693 to694',sum(x.get('proiect')=='P01' for x in old)==693 and sum(x.get('proiect')=='P01' for x in new)==694)
ck('only added T386 no removed',nm.keys()-om.keys()=={('P01','T386')} and not om.keys()-nm.keys())
changes=[]
for k in sorted(om.keys()&nm.keys(),key=str):
 i,a=om[k];n,b=nm[k]
 if a!=b:
  fields=[f for f in sorted(a.keys()|b.keys()) if a.get(f)!=b.get(f)]
  changes.append({'project':k[0],'id':k[1],'before_pointer':'/'+str(i),'after_pointer':'/'+str(n),'fields':fields,'before_after':{f:{'before':a.get(f),'after':b.get(f)} for f in fields}})
ck('only one existing row changed',len(changes)==1 and changes[0]['id']=='T240')
ck('T240 claims only',set(changes[0]['fields'])=={'observatii','procent','ultima_actualizare'})
ck('all old structured fields and states preserved',all({k:v for k,v in a.items() if k not in ['observatii','procent','ultima_actualizare']}=={k:v for k,v in nm[t][1].items() if k not in ['observatii','procent','ultima_actualizare']} for t,(i,a) in om.items()))
captures=[]
for p in sorted(oldp.glob('00_*.json')):
 q=newp/p.name;captures.append({'name':p.name,'old':ref(p),'new':ref(q),'same_bytes':raw(p)==raw(q)})
d=j(newp/'Delta.json');ck('recorded capture candidate fixed',d['github_master_at_capture']=='df85d33c1648ce2b2df130a60a05ef696e2e5480')
ck('recorded server working HEAD excluded',d['server_worktree_head']=='8c0695de36b50ede569c6d318715db0af11fcbff')
for f in d['files']:ck('capture declared SHA '+f['name'],sha(newp/f['name'])==f['hash'])
ca=j(oldp/'00_CORESPONDENTA_COD_CAPITOL.json');cb=j(newp/'00_CORESPONDENTA_COD_CAPITOL.json')
ck('correspondence only adds one row',all(ca[k]==cb[k] for k in ca if k!='coduri') and len(cb['coduri'])==len(ca['coduri'])+1 and all(x in cb['coduri'] for x in ca['coduri']))
map_added=[x for x in cb['coduri'] if x not in ca['coduri']];ck('T386 canonical mapping unique',len(map_added)==1 and map_added[0]['cod']=='P01.C10.T0030' and map_added[0]['id_tehnic']=='T386')
for n in ['00_STATUS_RAMASE.json','00_STATUS_FINALIZATE.json']:
 ck('derived list unchanged '+n,raw(oldp/n)==raw(newp/n));ck('T386 not in derived text '+n,'T386' not in raw(newp/n).decode('utf8'))
plan=R/'executie/R12_plan_delta/Plan_delta_R12_v2.json';gate=R/'executie/R12_plan_delta/A11_verdict_plan_delta_R12_v2.json'
ck('frozen plan hash',sha(plan)=='4aeeaf61d73efa1a1155e9eecbbcc5564ddfeee4cda918fa5fa04c97f2ef7276')
g=j(gate);ck('prior plan gate50of50',g['quality_score_plan']==10 and g['subchecks_satisfied']==g['subchecks_total']==50)
receipt=B/'A11/Val03_registru/Verdict_A11_R12_Val03_registru_v1.json';checklist=B/'A11/Val03_loturi/Checklist_A11_dupa_R12_Val03_v1.json'
ck('Val03 receipt preserved',sha(receipt)=='e284136e81d919cb5b8b6dec6ea5ade3af24a59a60ad80e89b4226752a859114')
ck('Val03 checklist preserved',sha(checklist)=='3e6aff18819a2d88cd6de04b7ee71dbdd159b80ea7df5652524896306a9dd3ba')
task=nm[('P01','T386')][1]
out={'schema':'A11.R12.Val04.population.applicability.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11 independent','method':'Comparare independentă a tuturor rândurilor capturilor locale, verificare SHA și identitate proiect+id, lectură plan și controale. HEAD-urile sunt cele din captura read-only a coordonatorului; nu reprezintă interogare Git remote nouă A11. Zero execuții produs, zero scrieri operaționale.',
 'candidate':d['github_master_at_capture'],'excluded_server_worktree_head':d['server_worktree_head'],'captures':captures,'capture_delta':ref(newp/'Delta.json'),'delta_baseline_warning':'Delta.json compară față de începutul auditului, nu față de checkpointul00:39. Cele15 schimbări/new_final1 nu sunt schimbări noi ale acestei reluări.',
 'population':{'before_all':996,'after_all':997,'before_P01':693,'after_P01':694,'added':1,'removed':0,'existing_changed_rows':1,'existing_state_changes':0,'historic_dossiers':652,'historic_criteria':2619,'technical_dispatch':6728,'technical_sources_with_partial_observations':39,'partial_level_partition':[26,7,2,4],'R11_reference_only':116,'open_contracts':17,'whole_file_or_task_acceptance':0},'existing_changes':changes,
 'new_task_addendum':{'task':'P01.C10.T0030','alias':'P01.T386','source':dict(ref(newp/'00_STATUS_TASKURI.json'),pointer='/996'),'state':'plan','canonical_map':map_added[0],'requirement':task['descriere'],'origin_claim':task['cerere_proprietar'],'source_of_authority':'Cerință din registrul capturat, nu instrucțiune executabilă și nu confirmare independentă a originii reconstituite.','historical_cohort_added':False,'criterion_credit':0,'file_credit':0,'new_defect_confirmed':False,'routing':{'primary':'A06','cross_review':['A09','A02'],'independent':'A11','nominal':'A12','contracts':['D01','D04','D10','D11']},'required_next_nominal_actions':['A12 păstrează rândul nou și codul canonic, în afara celor652fișe istorice; nu atribuie dată de închidere ori criterii nescrise.','Înaintea unei probe T386: fixează OID și consumatori OperatiiCanale/CanalGrupe, actor/rol/client/canal, inventarul real al regulilor și oracolul comun; cele19reguli sunt o afirmație din registru până la verificare.','Adaptarea preferată este delegarea pe scriitorul existent și MCampaign/PO/Trx native, fără un nou motor paralel; teste de creare/reutilizare/legare/dezlegare, refuz interclient/rol, rollback și retry/concurență.','Reconcilierea paginilor derivate rămâne deschisă: Rămase/Finalizate byte-identice și nu includ T386; nu deduce inexistența taskului din aceste liste.'],'impact_on_current_proposals':'Nu schimbă oracolul SO versus PO al G3 și nu schimbă codul snapshotului df85. Dacă protocolul folosește scriitorii de campanii/grupe, trebuie revizuit explicit înainte de acele operații.'},
 'plan':ref(plan),'prior_gate':ref(gate),'last_receipt':ref(receipt),'authoritative_remaining_checklist':ref(checklist),
 'decision':'APLICABILITATE MENȚINUTĂ LIMITAT LA df85, CU ADDENDUM NOMINAL T386; PROTOCOALELE CONCRETE G3/FRONTEND ÎNCĂ ÎN AȘTEPTAREA CONTROLULUI ÎNAINTEA EXECUȚIEI.',
 'score':{'prior_plan':10,'prior_subchecks':'50/50','new_product_score':None,'full_audit_score':None},
 'execution_conditions':['Nu executa working tree8c0695de ori branch6354d628 revendicat în observațiile T240; niciun transfer de rezultat fără delta și poartă.','G3: surse/JAR/runtime/AD/schema și canari fixate; metode native reale, SO/PO sintetice, client/ASI/IsActive/ownership explicite, oracol separat și readback persistent; DocAction/C_Order neexecutate dacă rămân în afara protocolului.','Frontend: original exact, consumator/template și rol public declarate, interceptare completă locală, oracol DOM independent, pozitiv/eroare/retry/concurență; fără presupunere ZK/ERP sau backend din DOM sintetic.','N05 deja primit se reutilizează numai ca infrastructură documentată, fără repetare inutilă și fără credit nou.','Conservă toate17contractele și toate diferențele de nivel de probă; remedierea G2 recuperează componentele recuperabile, nu cutii consumate/manoperă.','Nu atinge cele6rădăcini al căror cleanup a fost respins; niciun laborator nou creat prin această verificare.'],
 'checks':checks,'product_execution':0,'operational_writes':0,'resources_created':'Numai aceste documente și scriptul de verificare locală.'}
p=O/'Verdict_A11_aplicabilitate_R12_0143_v1.json';write(p,out)
runner=O/'Runner_A11_preflight_0143_v1.py';assert not runner.exists();runner.write_bytes(pathlib.Path(__file__).read_bytes())
s=O/'SIGILIU_A11_preflight_0143_v1.json';write(s,{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[ref(p),ref(runner)],'immutable':True})
print(json.dumps({'verdict':ref(p),'seal':ref(s),'checks':len(checks)},ensure_ascii=False))
