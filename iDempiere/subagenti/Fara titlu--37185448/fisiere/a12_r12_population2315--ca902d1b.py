import gzip,hashlib,json,pathlib,re
from datetime import datetime,timezone
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');E=B/'executie';P=E/'R12_plan_delta';A=P/'A12'
H='df85d33c1648ce2b2df130a60a05ef696e2e5480'
def sha(x):return hashlib.sha256(x).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p,pointer=None):
 b=p.read_bytes();r={'path':p.relative_to(B).as_posix(),'sha256':sha(b),'bytes':len(b)}
 if pointer is not None:r['pointer']=pointer
 return r
def field_sha(x):return sha(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
old_dir=E/'delta/2026-11-02T22-49-25-027Z';new_dir=E/'delta/2026-11-02T23-15-23-444Z'
old_path=old_dir/'00_STATUS_TASKURI.json';new_path=new_dir/'00_STATUS_TASKURI.json';old=load(old_path);new=load(new_path)
given=load(new_dir/'Comparatie_ultimul_checkpoint.json');plan_path=P/'Plan_delta_R12_v2.json';plan=load(plan_path);v_path=P/'A11_verdict_plan_delta_R12_v2.json';verdict=load(v_path)
assert given['source_hashes']==[sha(old_path.read_bytes()),sha(new_path.read_bytes())]
assert plan['candidate']==given['head']==H and verdict['candidate']==H
assert verdict['quality_score_plan']==10 and verdict['source_sha256']==sha(plan_path.read_bytes())
oldkeys={(r.get('proiect'),r['id']):i for i,r in enumerate(old)};newkeys={(r.get('proiect'),r['id']):i for i,r in enumerate(new)}
assert len(oldkeys)==len(old)==len(newkeys)==len(new)==996
assert set(oldkeys)==set(newkeys)
changes=[];state_changes=[]
for key,i in oldkeys.items():
 j=newkeys[key];r=old[i];s=new[j]
 fields=[k for k in sorted(set(r)|set(s)) if r.get(k)!=s.get(k)]
 if fields:changes.append({'project':key[0],'technical':key[1],'old_pointer':'/'+str(i),'new_pointer':'/'+str(j),'fields':[{'name':f,'before':r.get(f),'after':s.get(f),'before_sha256':field_sha(r.get(f)),'after_sha256':field_sha(s.get(f)),'old_source':ref(old_path,f'/{i}/{f}'),'new_source':ref(new_path,f'/{j}/{f}')} for f in fields]})
 if r.get('stare_generala')!=s.get('stare_generala'):state_changes.append(key)
assert len(changes)==1 and changes[0]['technical']=='T343' and changes[0]['project']=='P01'
assert {f['name'] for f in changes[0]['fields']}=={'observatii','procent','ultima_actualizare'} and not state_changes
assert sum(r.get('proiect')=='P01' for r in old)==sum(r.get('proiect')=='P01' for r in new)==693
old_t=old[oldkeys[('P01','T343')]];new_t=new[newkeys[('P01','T343')]]
assert old_t['stare_generala']==new_t['stare_generala']=='audit'
assert 'P01.C10.T0025' in new_t['denumire']
capture_refs=[]
for label,d in [('old',old_dir),('new',new_dir)]:
 capture_refs.append({'label':label,'capture':d.name,'files':[ref(p) for p in sorted(d.iterdir()) if p.is_file()],'semantic_registry':ref(d/'00_STATUS_TASKURI.json'),'note':'Delta.json, când există, poate avea altă bază; concluzia prezentă este recalculată direct între cele două registre nominale.'})
with gzip.open(P/'Catalog_Git_integral_per_fisier_R12_v2.jsonl.gz','rt',encoding='utf-8') as f:catalog={r['path']:r for r in map(json.loads,f)}
prefix='Documentatie/echipa-2026-10-09/T343-comenzi-site-mutate-in-program/'
sources=[]
for p in sorted((A/'Sources_2315').glob('*.md')):
 data=p.read_bytes();gitpath=prefix+p.name;blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert catalog[gitpath]['git_object']==blob
 sources.append(dict(ref(p),git_path=gitpath,git_blob=blob,head=H,executed=False))
criterion_file=A/'Sources_2315/03_audit_r0_criterii.md';lines=criterion_file.read_text(encoding='utf-8-sig').splitlines();line107=lines[106];assert '| C-2.2 |' in line107 and 'CO \\| CO \\| CO' in line107
authority01b=P/'Sources_lues'/prefix/'01b_decizii_orchestrator.md';authority_text=authority01b.read_text(encoding='utf-8-sig')
assert not re.search(r'D-343-60|D343-60',authority_text)
files14e=[p for p in catalog if p.startswith(prefix+'14e')];assert not files14e
def pp(pointer):return ref(plan_path,pointer)
out={
 'schema':'eva.audit.r12.population-supplement/1','utc':datetime.now(timezone.utc).isoformat(),'mode':'READ_ONLY_PREFLIGHT; no product tests','head':H,
 'previous_inventory_unchanged':ref(P/'Manifest_A12_receptie_R12_v2.json'),
 'approved_plan':ref(plan_path),'A11_gate':dict(ref(v_path),decision=verdict['decision'],plan_grade=10,not_execution_grade=True),
 'capture_rehashes':capture_refs,'provided_comparison':ref(new_dir/'Comparatie_ultimul_checkpoint.json'),
 'independent_semantic_comparison':{'key':['proiect','id'],'records_old':996,'records_new':996,'p01_old':693,'p01_new':693,'membership_added':[],'membership_removed':[],'changed_rows':changes,'changed_states':[],'historic_completed_cohort':652,'historic_criteria':2619,'cohort_additions':0,'technical_inventory_still':6728,'all_git_paths_still':183469,'new_execution_credit':0},
 'task':{'technical':'T343','canonical':'P01.C10.T0025','current_state':'audit','completed_task':False,'progress_as_declared':[old_t['procent'],new_t['procent']],'last_edit_as_declared':new_t['ultima_actualizare'],'closure_date_inferred':None,'owner':'A06','instrument_peer':'A01','business_consumers':['A08','A07'],'independent_reviewer':'A11'},
 'claims':[{'id':'POP2315-T343-A9','claim':'A-9 comis: ruta stării iDempiere, 56/0 plus mock26/0','classification':'DECLARATION_NOT_ACCEPTED_EVIDENCE','required_evidence':'Commit exact, blob/JAR și instalare distinctă, lista cazurilor și expected→observed; separă56 de26 și componenta mock de ruta nativă.'},{'id':'POP2315-T343-SUITE','claim':'306 clase, una roșie reparată, bloc etichete','classification':'DECLARATION_NOT_ACCEPTED_EVIDENCE','required_evidence':'Numitor nominal, jurnal înainte/după, SHA reparației și martor regresie; nu se transferă306 la T330 sau la altă versiune/JAR.'},{'id':'POP2315-T343-UI','claim':'Proba A-10 din buton în rulare','classification':'IN_PROGRESS_NOT_COMPLETED','required_evidence':'Finalizare din intrarea normală, actor, menu/formă, IDs și efecte persistente; status/procent nu probează succes.'},{'id':'POP2315-T343-C22','claim':'D-343-60: C-2.2 amendat la nativ, C_Order IP pe drumul T22/T216; T-NOU normalizare; validare r0bis-3/14e în curs','classification':'NORMATIVE_CHANGE_CLAIM_REQUIRES_AUTHORITY_AND_ORACLE','required_evidence':'Textul amendamentului și recepția lui, cu commit/data/autor; criteriul vechi păstrat, diferența IP/CO explicată și condițiile documentelor aval neschimbate ori amendate explicit.'}],
 'normative_comparison':{'frozen_criterion':dict(ref(criterion_file),git_path=prefix+'03_audit_r0_criterii.md',git_blob=catalog[prefix+'03_audit_r0_criterii.md']['git_object'],line=107,line_sha256=sha(line107.encode()),text=line107),'old_exact_oracle':'C_Order CO | M_InOut CO | C_Invoice ARI CO | număr linii legate','new_registry_claim':'C_Order IP; alte stări, motive și efecte aval nu sunt precizate în această observație','important_distinction':'IP și CO sunt stări diferite. IP nu devine implicit finalizare comercială, avizare, facturare sau normalizare implementată. Acest supliment nu decide că IP este defect și nu relaxează criteriul vechi.','authority_check':{'14e_present_in_fixed_head':False,'searched_prefix':prefix+'14e','D34360_present_in_frozen_01b':False,'01b_source':ref(authority01b),'boundary':'Absență doar în arborii/documentele fixate inspectate; nu afirmă inexistența unei ramuri, a unui worktree sau a unei recepții ulterioare.'}},
 'plan_impact':[{'scope':'Versiune/populație','plan_source':pp('/version_policy'),'finding':'Același HEAD și aceleași stări; nu cere catalog Git nou, nu extinde cohorta și nu invalidează prin sine celelalte loturi aprobate.'},{'scope':'D05, continuitate site→C_Order→aviz','plan_source':pp('/remaining_contracts/4'),'contract_owner':'A08','contract_peer':'A07','nominal_producer':'A06','covered':'Intrare normală, sursă/canal/SO/linie, cititorul existent DetaliuComanda.din, unSO, efect persistent, refuz fără SO și retry fără duplicate.','gap':'D05 nu definește excepția IP față de criteriul nominal C-2.2 CO/CO/CO; legătura T343 la această revendicare trebuie făcută nominal, nu prin simplă apartenență la C10.'},{'scope':'D06, aviz→factură→încasare','plan_source':pp('/remaining_contracts/5'),'contract_owner':'A07','contract_peer':'A03','covered':'Politica de facturare, DocAction, documente native, integritate origine și postări fără dublare.','gap':'Noua observație nu spune dacă factura/livrarea/numărul liniilor rămân cele din C-2.2; nu se presupune amendarea lor.'},{'scope':'G01/G02/G03/G05/G07/G08/G10','plan_sources':[pp('/mandatory_gates_inherited/'+str(i)) for i in [0,1,2,4,6,7,9]],'covered':'Identitate sursă versus instalare, oracol autoritativ, nativ înainte de duplicare, efect persistent și recepție peer/A11; cifrele din registru nu sunt probe.'}],
 'disposition':{'inventory_or_population_amendment_required':False,'targeted_acceptance_oracle_amendment_required':True,'applies_to':'Numai recepția nominală T343/C-2.2 în sensul noii afirmații IP; nu suspendă automat toate loturile R12.','existing_plan_coverage':'Acoperă metoda și traseul de măsurare, dar nu este suficient pentru a accepta tacit înlocuirea oracolului CO cu IP.','next_actions':[{'owner':'A06','peer':'A07','action':'Recuperează D-343-60 și 14e cu SHA/autor/stare; verifică dacă se aplică sursei df85 sau unei ramuri ulterioare. Fără ele criteriul rămâne etalonul înghețat, cu noua revendicare în așteptare.'},{'owner':'A06','peer':'A08','action':'Propune precizarea nominală: actor, originea exactă, acțiunea T22/T216, precondiții și starea așteptată înainte/după pe C_Order/Line, M_InOut/Line și C_Invoice/Line. A11 recepționează diferența de oracol înainte de un verdict pe noua formulare.'},{'owner':'A07','peer':'A03','action':'Menține D05/D06: aceeași origine și aceleași chei, DocumentStatus/DocAction/Processed separat, documente aval, client/org, retry și conexiune nouă; IP singur nu îndeplinește lanțul.'},{'owner':'A12','peer':'A11','action':'Păstrează cerința originală, observația nouă și eventuala decizie ca versiuni distincte. Nicio identitate comercială nouă pentru textul T-NOU și nicio rezolvare implicită a LR-urilor lotuluiB.'}],'permitted_interpretation_before_amendment':'Măsurători pe df85 în metoda deja aprobată se pot consemna ca observații cu etalonul vechi și revendicarea nouă separate; nicio promovare PASS a C-2.2 după IP înaintea recepției nominale A11. Orice alt SHA urmează poarta de delta existentă.','authority':'Aceasta este propunerea A12 de tratare; A11 decide impactul pe poarta de plan, fără autoaprobare.'},
 'source_documents_read_only':sources,'resources':{'created_product_services':0,'created_product_databases':0,'operational_writes':0,'product_tests':0,'new_files':'Numai sursele de documentare copiate byte-exact și acest supliment; inventarele/sigiliile anterioare intacte.'},
 'verification':{'both_registry_hashes_match_capture_comparison':True,'all996_rows_compared_by_project_id':True,'single_changed_row_and_three_fields_only':True,'all_source_blob_ids_verified_against_fixed_head_catalog':True,'approved_plan_hash_matches_A11_gate':True,'issues':[],'quality_score':None}
}
dest=A/'Supliment_populatie_2315.json';assert not dest.exists();dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
for source in sources:assert sha((B/source['path']).read_bytes())==source['sha256']
assert sha(plan_path.read_bytes())==out['approved_plan']['sha256']
assert sha((P/'Manifest_A12_receptie_R12_v2.json').read_bytes())==out['previous_inventory_unchanged']['sha256']
print(json.dumps({'file':ref(dest),'population':[996,693,652,2619],'source_documents':len(sources),'targeted_oracle_amendment_required':True,'product_tests':0},ensure_ascii=False,indent=2))
