import json,pathlib,hashlib,datetime
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01'); B=R/'executie/R12_fisiere'; O=B/'A11/Val05_preflight'
OLD=R/'executie/delta/2026-11-03T01-43-37-057Z'; NEW=R/'executie/delta/2026-11-03T02-45-48-441Z'
def raw(p): return p.read_bytes()
def sha(p): return hashlib.sha256(raw(p)).hexdigest()
def j(p): return json.loads(raw(p).decode('utf-8-sig'))
def ref(p): return {'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':len(raw(p))}
def write(p,v):
 assert not p.exists(),str(p)
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
checks=[]
def ck(n,b,details=None):
 checks.append({'check':n,'ok':bool(b),'details':details}); assert b,(n,details)
old=j(OLD/'00_STATUS_TASKURI.json'); new=j(NEW/'00_STATUS_TASKURI.json'); key=lambda x:(x.get('proiect'),x['id'])
om={key(x):(i,x) for i,x in enumerate(old)}; nm={key(x):(i,x) for i,x in enumerate(new)}
ck('997 identități unice înainte și după',len(om)==len(old)==len(nm)==len(new)==997)
ck('694 membri P01 înainte și după',sum(x.get('proiect')=='P01' for x in old)==sum(x.get('proiect')=='P01' for x in new)==694)
ck('Nicio adăugare sau eliminare',om.keys()==nm.keys())
changes=[]; state_changes=[]
for k in sorted(om,key=str):
 i,a=om[k]; n,b=nm[k]
 if a!=b:
  fields=[f for f in sorted(a.keys()|b.keys()) if (f in a)!=(f in b) or a.get(f)!=b.get(f)]
  changes.append({'project':k[0],'id':k[1],'before_pointer':'/'+str(i),'after_pointer':'/'+str(n),'fields':fields,'before_after':{f:{'before':a.get(f),'after':b.get(f)} for f in fields}})
 if a['stare_generala']!=b['stare_generala']: state_changes.append(k)
ck('Numai T343 schimbat',len(changes)==1 and changes[0]['id']=='T343')
ck('Cele cinci câmpuri T343',set(changes[0]['fields'])=={'auditor','documente_produse','observatii','procent','ultima_actualizare'})
ck('Zero stări schimbate',not state_changes)
for t in ['T240','T386']: ck(t+' identic integral',om[('P01',t)][1]==nm[('P01',t)][1])
ck('T343 progres 54 la 56, fără scor de audit',om[('P01','T343')][1]['procent']==54 and nm[('P01','T343')][1]['procent']==56)
captures=[]
for p in sorted(OLD.glob('00_*.json')):
 q=NEW/p.name; captures.append({'name':p.name,'old':ref(p),'new':ref(q),'same_bytes':raw(p)==raw(q)})
 if p.name!='00_STATUS_TASKURI.json': ck('Registru auxiliar identic: '+p.name,raw(p)==raw(q))
d=j(NEW/'Delta.json')
ck('Candidat fixat df85',d['github_master_at_capture']=='df85d33c1648ce2b2df130a60a05ef696e2e5480')
ck('HEAD server separat',d['server_worktree_head']=='c594a93a1d4e606f8c2e432108a29e97244d692e')
for f in d['files']: ck('SHA captură '+f['name'],sha(NEW/f['name'])==f['hash'])
doc=B/'A12/Val_05/T343_25_reaudit_lot_B_r2_0216582562e.md'; prov=B/'A12/Val_05/Provenienta_document_T343_0245.json'; pr=j(prov)
ck('Document T343 exact SHA și lungime',sha(doc)=='df048f5cc8884bdca42f8758efbfced5d43bccaa10e0d116db062d907074e339' and len(raw(doc))==138124)
oid=hashlib.sha1(b'blob '+str(len(raw(doc))).encode()+b'\0'+raw(doc)).hexdigest()
ck('Git blob calculat independent',oid==pr['blob_oid']=='be0fad64d8c4475d0af2fb290e7bcc4c875608a3')
for c in pr['commands']:
 ck('Comandă documentară reușită: '+c['kind'],c['exit']==0)
 if 'stdout' in c: ck('SHA stdout '+c['kind'],hashlib.sha256(c['stdout'].encode()).hexdigest()==c['stdout_sha256'] and len(c['stdout'].encode())==c['stdout_bytes'])
ck('Document absent la df85 conform citirii ls-tree arhivate',next(c for c in pr['commands'] if c['kind']=='candidate_presence')['stdout']=='')
lines=raw(doc).decode('utf8').splitlines()
anchors=[]
for term in ['## VERDICT:', 'Obiectul |', '283 passed', 'B16', 'Rambursarea și anularea nu le-am rulat', 'Proba UX din buton n-a rulat']:
 found=[{'line':i+1,'text':v} for i,v in enumerate(lines) if term in v];ck('Ancoră documentară '+term,bool(found));anchors.append({'term':term,'matches':found})
plan=R/'executie/R12_plan_delta/Plan_delta_R12_v2.json'; gate=R/'executie/R12_plan_delta/A11_verdict_plan_delta_R12_v2.json'
ck('Plan imuabil',sha(plan)=='4aeeaf61d73efa1a1155e9eecbbcc5564ddfeee4cda918fa5fa04c97f2ef7276')
g=j(gate);ck('Poartă de plan 50/50',g['quality_score_plan']==10 and g['subchecks_satisfied']==g['subchecks_total']==50)
receipt=B/'A11/Val04_registru/Verdict_A11_R12_Val04_registru_v1.json'; checklist=B/'A11/Val04_loturi/Checklist_A11_dupa_R12_Val04_v1.json'; publication=R/'executie/Publicare_R12_Val04/Final_2026-11-03T02-36-27Z/MANIFEST_PUBLICARE_FINAL.json'
for p,h in [(receipt,'fbe5eed1c4b228513d194cfaf741e586990f07b8623236f5ac6e55281a4f0932'),(checklist,'a5d094982e6d7fd511bef7c002dad831f56ded82cef28c2ebcde2446831b1240'),(publication,'e16586350b462df27bc848502e21fa1bb140857fa1e9712f4617ca9b80086e7a')]: ck('Continuitate '+p.name,sha(p)==h)
out={'schema':'A11.R12.Val05.population.applicability.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11 independent',
'method':'Comparare independentă integrală a celor 997 de rânduri, rehash capturi, recalcul Git blob al documentului nou și lectură semantică țintită a corpului verdictului T343. Comenzile remote sunt dovezi capturate de coordonator/A12, nu interogări remote noi A11. Nicio comandă din documentul T343 nu a fost executată.',
'candidate':d['github_master_at_capture'],'excluded_server_worktree_head':d['server_worktree_head'],'captures':captures,'delta_capture':ref(NEW/'Delta.json'),'delta_warning':'Delta.json compară cu 2026-11-02T14:06:00.673Z. Cele 15 schimbări și new_final=1 nu reprezintă schimbări noi față de checkpointul 01:43.',
'population':{'before_all':997,'after_all':997,'before_P01':694,'after_P01':694,'added':0,'removed':0,'changed_rows':1,'changed_states':0,'historic_dossiers':652,'historic_criteria':2619,'technical_dispatch':6728,'partial_sources':44,'partial_partition':{'original_component_or_method':33,'shell_comparator':5,'transitive_type':2,'fixture_binding_metadata':4},'path_event_pairs':50,'R11_reference_only':116,'open_contracts':17,'whole_acceptances':0},
'changes':changes,'new_document_addendum':{'task':'P01.C10.T0025','alias':'P01.T343','document':ref(doc),'provenance':ref(prov),'git_blob_independently_computed':oid,'resolved_document_commit':pr['resolved_commit'],'scope':'Lot B pe t343-impl-b@2c5d3645a2d și copia site d906cb0, nu candidatul df85.','document_verdict':'NU TRECE — 9/10, LR-6/B16 deschis; afirmație a documentului, fără preluarea scorului în auditul nostru.','interpretation':['documente_produse este o schimbare de proveniență nominală relevantă; nu declarăm toate câmpurile normative egale.','LR-6 privește observatorul structural al argumentului gărzii de rambursare. Raportul declară mutantul B16 viu și absența execuției comportamentale a rambursării/anulării. Nu este o constatare nouă reprodusă la df85.','Proba UX independentă descrisă în acel raport a fost refuzată la admitere; rezultatele UX ale autorului și mutanții serverului nu înlocuiesc acea execuție.','Nu a fost identificat în corpul relevant un amendament CO/IP, C-2.2 sau pentru paginarea JsonCatalogSource ori delimitarea SO/PO. §9/§Y generale nu constituie execuții DocAction.','283 de rezultate, 55 de mutanți și închiderile LR declarate rămân atribuite versiunilor documentului. Zero transfer de credit către cele 652 de fișe istorice, df85 sau contractele curente.','Data/discul/resursele declarate sunt istorice; nu sunt măsurători actuale A11 și nu autorizează operații de curățare.'],'anchors':anchors,'new_product_tests':0,'criterion_credit':0},
'decision':'APLICABILITATE MENȚINUTĂ EXCLUSIV LA df85, CU ADDENDUM DOCUMENTAR T343; PROTOCOALELE CONCRETE DOCAction ȘI PAGINARE RĂMÂN ÎN AȘTEPTAREA CONTROLULUI ÎNAINTE DE EXECUȚIE.',
'plan':ref(plan),'prior_plan_gate':ref(gate),'last_registry_receipt':ref(receipt),'current_checklist':ref(checklist),'last_publication_manifest':ref(publication),
'conditions':['Nu se execută working tree c594a93a ori ramurile/copia site citate de T343; orice versiune nouă necesită delta și poartă separate.','DocAction: se fixează DocSubType, prepare/complete, stările native efective, MStorageReservation și delta M_StorageReservationLog cu legături document/linie; contextul injectat de laborator nu dovedește login/RBAC.','Pentru o linie EVA corelată, se disting stările accesibile ale generatorului de fixturele artificiale order-only; orice generator suplimentar necesită protocol explicit, fără GET extern ori înlocuirea unui hook pentru a pretinde flux integral.','Paginare: originalul JsonCatalogSource, catalog sintetic valid, catalog absent/gol și limite întregi; oracol pe rezultat/excepție exactă, fără presupunerea unui HTTP 500 sau a unei cauzalități cu frontendul mock.','Se păstrează nivelurile Val04 și cele 17 contracte deschise; noua probă nu închide integral un fișier, task sau pipeline.','Cele șase rădăcini cu ștergere refuzată rămân neatinse. Niciun laborator creat prin această recepție.'],
'checks':checks,'product_score':None,'audit_global_score':None,'product_executions':0,'operational_writes':0,'resources_created':'Numai verdictul și runnerul local. Recepția nominală a suplimentului A12 va fi separată după sigilarea sa.'}
O.mkdir(parents=True,exist_ok=True); p=O/'Verdict_A11_aplicabilitate_R12_0245_v1.json';write(p,out);runner=O/'Runner_A11_preflight_0245_v1.py';assert not runner.exists();runner.write_bytes(pathlib.Path(__file__).read_bytes()); seal=O/'SIGILIU_A11_preflight_0245_v1.json';write(seal,{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[ref(p),ref(runner)],'immutable':True});print(json.dumps({'verdict':ref(p),'seal':ref(seal),'checks':len(checks)},ensure_ascii=False))
