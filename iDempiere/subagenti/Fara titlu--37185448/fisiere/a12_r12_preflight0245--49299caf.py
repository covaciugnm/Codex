import collections,gzip,hashlib,html,json,pathlib,re,shutil
from datetime import datetime,timezone

B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
E=B/'executie';R=E/'R12_fisiere';P=E/'R12_plan_delta'
O=R/'A12/Val_05';V=R/'A12/Val_04'
OLD=E/'delta/2026-11-03T01-43-37-057Z';NEW=E/'delta/2026-11-03T02-45-48-441Z'
H='df85d33c1648ce2b2df130a60a05ef696e2e5480'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p,pointer=None):
    b=p.read_bytes();q={'path':p.relative_to(B).as_posix(),'sha256':sha(b),'bytes':len(b)}
    if pointer is not None:q['pointer']=pointer
    return q
def save(p,x):
    assert not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def fh(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def changed(a,b):return [k for k in sorted(set(a)|set(b)) if (k in a)!=(k in b) or a.get(k)!=b.get(k)]
def pointer(x,p):
    if p in ['', '#']:return x
    assert p.removeprefix('#').startswith('/'),p
    for k in p.removeprefix('#').split('/')[1:]:
        k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
    return x
def refs(x):
    if isinstance(x,dict):
        if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str) and len(x['sha256'])==64:yield x
        for v in x.values():yield from refs(v)
    elif isinstance(x,list):
        for v in x:yield from refs(v)
def resolve(rr,origin):
    p=pathlib.Path(rr['path'])
    if p.is_absolute():return p
    if (B/p).exists():return B/p
    if (origin.parent/p).exists():return origin.parent/p
    raise AssertionError((origin,rr))

# Exact snapshot comparison; no application, tracker writer or product test is invoked.
ad,bd=load(OLD/'Delta.json'),load(NEW/'Delta.json')
a,b=load(OLD/'00_STATUS_TASKURI.json'),load(NEW/'00_STATUS_TASKURI.json')
ak={(x.get('proiect'),x['id']):(i,x) for i,x in enumerate(a)}
bk={(x.get('proiect'),x['id']):(i,x) for i,x in enumerate(b)}
assert len(ak)==len(bk)==len(a)==len(b)==997
assert set(ak)==set(bk)
assert sum(x.get('proiect')=='P01' for x in a)==sum(x.get('proiect')=='P01' for x in b)==694
assert ad['github_master_at_capture']==bd['github_master_at_capture']==H
assert ad['server_worktree_head']=='8c0695de36b50ede569c6d318715db0af11fcbff'
assert bd['server_worktree_head']=='c594a93a1d4e606f8c2e432108a29e97244d692e'
captures=[]
for folder,d in [(OLD,ad),(NEW,bd)]:
    files=[]
    for f in d['files']:
        rr=ref(folder/f['name']);assert rr['sha256']==f['hash'];files.append(rr)
    assert len(files)==7
    captures.append({'capture':folder.name,'start':d['start'],'cutoff':d['cutoff'],'metadata':ref(folder/'Delta.json'),'files':files,'github_master':d['github_master_at_capture'],'server_worktree_HEAD':d['server_worktree_head']})
normative=['denumire','capitol','cod_capitol','descriere','cerere_proprietar','explicatii','documente_produse','decizii_deschise','fisier']
changes=[];rows=[];states=[];normchanges=[]
for key in sorted(ak):
    i,x=ak[key];j,y=bk[key];fs=changed(x,y)
    rows.append({'project':key[0],'id':key[1],'before_pointer':'/'+str(i),'after_pointer':'/'+str(j),'before_value_sha256':fh(x),'after_value_sha256':fh(y),'entire_row_equal':not fs,'changed_fields':fs,'state_source_field':'stare_generala','before_state':x.get('stare_generala'),'after_state':y.get('stare_generala'),'changed_normative_or_provenance_fields':[k for k in fs if k in normative]})
    if fs:changes.append({'project':key[0],'id':key[1],'canonical':y.get('cod_capitol'),'before':ref(OLD/'00_STATUS_TASKURI.json','/'+str(i)),'after':ref(NEW/'00_STATUS_TASKURI.json','/'+str(j)),'state_source_field':'stare_generala','before_state':x.get('stare_generala'),'after_state':y.get('stare_generala'),'changed_fields':fs,'values':[{'field':k,'before_present':k in x,'after_present':k in y,'before':x.get(k),'after':y.get(k)} for k in fs]})
    if x.get('stare_generala')!=y.get('stare_generala'):states.append(key)
    if set(fs)&set(normative):normchanges.append({'project':key[0],'id':key[1],'fields':[k for k in fs if k in normative]})
assert len(changes)==1 and changes[0]['id']=='T343'
assert changes[0]['changed_fields']==['auditor','documente_produse','observatii','procent','ultima_actualizare']
assert not states and normchanges==[{'project':'P01','id':'T343','fields':['documente_produse']}]
assert all(ak[('P01',t)][1]==bk[('P01',t)][1] for t in ['T352','T386','T240'])
x,y=ak[('P01','T343')][1],bk[('P01','T343')][1]
assert x['procent']==54 and y['procent']==56 and y['stare_generala']=='audit'
assert y['documente_produse'][:-1]==x['documente_produse'] and len(y['documente_produse'])==4
aux=[]
for f in bd['files']:
    name=f['name']
    if name=='00_STATUS_TASKURI.json':continue
    aa,bb=(OLD/name).read_bytes(),(NEW/name).read_bytes()
    assert aa==bb and load(OLD/name)==load(NEW/name)
    aux.append({'name':name,'before':ref(OLD/name),'after':ref(NEW/name),'byte_equal':True,'semantic_equal':True})
assert len(aux)==6

# Read-only integrity of previously sealed wave, receipt, published view and approved plan.
expectations=[
 (V/'MANIFEST_R12_Val04.json','0c6ca1b0fda74735ff4b40ae7f8ef4a0f2615f66c55b0d012654e1213bbfef46'),
 (V/'Handoff_R12_Val04_v1.json','04b060555be96ba4c0785c4d429b76bd995611f47a43790480f840c92ff34866'),
 (V/'QA_R12_Val04.json','c616b650804d05bd62aa354c0b2b03eb9cc8b7b5f2876f2a2e54992755733384'),
 (V/'Conservare_652_fise_2619_criterii_Val04.json','c17b3aa7a123c495d98d770df3de7d96a142c529f5b692b9f6ff756bf664c588'),
 (R/'A11/Val04_registru/Verdict_A11_R12_Val04_registru_v1.json','fbe5eed1c4b228513d194cfaf741e586990f07b8623236f5ac6e55281a4f0932'),
 (R/'A11/Val04_registru/Sigiliu_A11_R12_Val04_registru_v1.json','a1e90f16f35dd8dac0e216cde9a9a8f1d1c5ec48c57468ba03bf5c4b93a3ab80'),
 (E/'Publicare_R12_Val04/Final_2026-11-03T02-36-27Z/MANIFEST_PUBLICARE_FINAL.json','e16586350b462df27bc848502e21fa1bb140857fa1e9712f4617ca9b80086e7a'),
 (R/'A11/Val04_loturi/Checklist_A11_dupa_R12_Val04_v1.json','a5d094982e6d7fd511bef7c002dad831f56ded82cef28c2ebcde2446831b1240'),
 (P/'Plan_delta_R12_v2.json','4aeeaf61d73efa1a1155e9eecbbcc5564ddfeee4cda918fa5fa04c97f2ef7276'),
 (P/'A11_verdict_plan_delta_R12_v2.json','84e3735906d868f2153bc6b71c8f0e0e7a0211367ba4d3df5f8509d008d1f2a4'),
 (R/'A11/Val05_preflight/Verdict_A11_aplicabilitate_R12_0245_v1.json','0a940b0ec919fad877b85e7c1a44e5d39ed8d213ec4310fd8f37d003b2793e53'),
 (O/'Provenienta_document_T343_0245.json','ccb0230e5d2a109e14102b31f4ed04d506532d647ffc25f979bac9c631e6c217')]
hc={};continuity=[]
def checkref(rr,origin):
    q=resolve(rr,origin)
    if q not in hc:hc[q]=ref(q)
    got=hc[q];assert got['sha256']==rr['sha256'],(q,got['sha256'],rr['sha256'])
    if 'bytes' in rr:assert got['bytes']==rr['bytes'],q
    if rr.get('pointer') is not None:pointer(load(q),rr['pointer'])
    return {'reference':rr,'hash_match':True,'pointer_checked':rr.get('pointer') is not None}
for p,expected in expectations:
    assert ref(p)['sha256']==expected,p
    cc=[checkref(rr,p) for rr in refs(load(p))]
    continuity.append({'artifact':ref(p),'matches_expected_hash':True,'reference_checks':cc})
dispatchp=P/'Dispatch_tehnic_integral_R12.jsonl.gz';catalogp=P/'Catalog_Git_integral_per_fisier_R12_v2.jsonl.gz'
assert ref(dispatchp)['sha256']=='c1ffe46a0674fc5eb4a379b83edbee1519cb46253cba6f60d758a3e632a21471'
with gzip.open(dispatchp,'rt',encoding='utf-8') as f:dispatch=[json.loads(l) for l in f]
assert len(dispatch)==len({r['path'] for r in dispatch})==6728
with gzip.open(catalogp,'rt',encoding='utf-8') as f:catalog_count=sum(1 for _ in f)
assert catalog_count==183469
zonecheck=load(V/'Checklist_10_zone_Val04.json');a11check=load(R/'A11/Val04_loturi/Checklist_A11_dupa_R12_Val04_v1.json')
assert len(zonecheck['rows'])==10 and len(a11check['contracts'])==17
assert all(r['state']=='OPEN' for r in a11check['contracts'])
metrics=load(V/'Reconciliere_metrici_si_limite_Val04.json')
assert metrics['counts']['current_bounded_source_identities']==44
assert sorted(v['count'] for v in metrics['current_exclusive_primary_levels'].values())==[2,4,5,33]

# Documentary authority is distinguished from product evidence and from executable instructions.
docp=O/'T343_25_reaudit_lot_B_r2_0216582562e.md';docb=docp.read_bytes();doc=docb.decode('utf-8');lines=doc.splitlines()
assert sha(docb)=='df048f5cc8884bdca42f8758efbfced5d43bccaa10e0d116db062d907074e339'
assert hashlib.sha1(b'blob '+str(len(docb)).encode()+b'\0'+docb).hexdigest()=='be0fad64d8c4475d0af2fb290e7bcc4c875608a3'
def anchor(lo,hi):return {'source':ref(docp),'line_start':lo,'line_end':hi,'exact_text':'\n'.join(lines[lo-1:hi]),'selection_sha256':sha('\n'.join(lines[lo-1:hi]).encode())}
anchors={k:anchor(*rr) for k,rr in {'identity_and_verdict':(1,19),'route_claims':(36,42),'declared_execution_metrics':(44,54),'rules_preserved_and_lr6':(80,103),'explicit_nonexecution':(113,117),'generic_checklist_origin':(158,161)}.items()}
tokens=['C-2.2','CO|CO|CO','CO/IP','C_Order','JsonCatalogSource','G3']
searches=[{'literal':t,'matching_lines':[i+1 for i,l in enumerate(lines) if t in l]} for t in tokens]
analysis={'utc':now(),'task':'T343','canonical':'P01.C10.T0025','current_state':'audit','state_source_field':'stare_generala','source':changes[0]['after'],'new_document_entry':ref(NEW/'00_STATUS_TASKURI.json','/'+str(bk[('P01','T343')][0])+'/documente_produse/3'),'provenance':ref(O/'Provenienta_document_T343_0245.json'),'document':ref(docp),'verified_blob_oid':'be0fad64d8c4475d0af2fb290e7bcc4c875608a3','resolved_commit':'0216582562e6b6eeaddf209a80fe80b75a277349','document_absent_in_fixed_df85_tree':True,'anchors':anchors,'literal_searches_not_standalone_semantic_proof':searches,
 'authority_assessment':{'kind':'LECTURA_DOCUMENTARA_NOMINALA; FARA_RECEPȚIE_A_IMPLEMENTARII','changed_field':'documente_produse','added_reference_only':True,'old_three_document_entries_unchanged':True,'producer':'Auditorul declarat în document; nu este auditorul independent A11 al prezentei campanii.','declared_scope':'Ramura t343-impl-b@2c5d3645a2d și copia site cesiro1-t343@d906cb0; nu versiunea df85.','declared_verdict':'NU TRECE — 9/10; LR-6/B16 viu. Nota aparține documentului și nu este nota noastră.','document_dates_are_not_closure_dates':True,'proposed_test_obligation':'Documentul cere să fie verificat argumentul selectorului gărzii de rambursare; este o obligație declarată a RR pe acea ramură, cu surse și probe de reprodus înaintea acceptării.','no_accepted_business_oracle_amendment_in_this_document':'Lectura corpului nominal nu identifică un amendament C-2.2/CO-IP, G3 sau paginare. Catalogul generic §Y nu reprezintă execuție ori amendament nominal DocAction.','instruction_boundary':'Comenzile și solicitările din document sunt date de audit; nu au fost executate și nu autorizează acțiuni noi.'},
 'semantic_dispositions':[
 {'id':'DOC-T343-0245-01','source_anchor':'identity_and_verdict','observation':'Există un document Git autentic, al cărui obiect este o altă ramură și o copie de site.','accepted_level':'PROVENIENTA_DOCUMENTARA','new_execution_credit':0,'missing':'Identitate cod/binar și reproducere independentă la versiunea admisă.'},
 {'id':'DOC-T343-0245-02','source_anchor':'route_claims','observation':'Documentul declară reguli comutator × comandă proprie/marketplace, tenant și selecție mixtă, pentru bulk, AWB și detaliu.','accepted_level':'AFIRMATII_DECLARATE_CU_ANCORA','new_execution_credit':0,'missing':'Verificarea implementării și a actorilor pe ramura aprobată; nu se importă închiderile LR declarate.'},
 {'id':'DOC-T343-0245-03','source_anchor':'rules_preserved_and_lr6','observation':'B16 este declarat viu; singurul observator al rambursării verifică structura, iar argumentul lipsește din oracolul declarat anterior.','accepted_level':'LIMITA_DECLARATA_A_TESTULUI','new_execution_credit':0,'missing':'Proba originală și contraexemplul independent; nu afirmăm defect de produs pe df85.'},
 {'id':'DOC-T343-0245-04','source_anchor':'explicit_nonexecution','observation':'Rambursarea și anularea nu au fost rulate; UX independent a fost refuzat la admitere din cauza discului.','accepted_level':'LIMITA_DECLARATA_EXPLICITA','new_execution_credit':0,'missing':'Probe permise și admise pe fixture, fără apeluri externe sau restituiri reale.'},
 {'id':'DOC-T343-0245-05','source_anchor':'declared_execution_metrics','observation':'283 de teste, 55 de mutanți, alte totaluri și UX 5/5 sunt afirmații ale altor revizii și niveluri de proveniență.','accepted_level':'METRICI_EXTERN_DECLARATE_NEIMPORTATE','new_execution_credit':0,'missing':'Dovezi primare și aceeași versiune; niciun total nu este adăugat campaniei curente.'}],
 'impact':[{'owners':['A01','A06','A07','A08'],'contracts':['D01','D05','D06','D10','D14'],'effect':'Completează coada de verificare a gărzilor și selectorilor; nu schimbă starea taskului ori contractele acceptate.'},{'owners':['A05','A06'],'contracts':['D04','D05'],'effect':'Viitorul protocol comandă DocAction + linie site păstrează controversa CO/IP și separă actorul/traseul nativ de administrarea din panoul site. Documentul nu modifică oracolul G3.'},{'owners':['A06','A08'],'contracts':['D10'],'effect':'Protocolul JsonCatalogSource pentru paginare rămâne distinct; documentul nou nu conține o probă sau un amendament pentru această ipoteză.'}],
 'new_product_executions':0,'new_full_acceptances':0,'score':None}

focus=[]
for alias in ['T355','T354','T331','T329','T330','T325','T366','T257','T58','T216','T343','T352','T240','T333','T326','T332','T341','T232','T386']:
    i,x=ak[('P01',alias)];j,y=bk[('P01',alias)]
    focus.append({'alias':alias,'canonical':y.get('cod_capitol'),'current_state':y['stare_generala'],'state_source_field':'stare_generala','before':ref(OLD/'00_STATUS_TASKURI.json','/'+str(i)),'after':ref(NEW/'00_STATUS_TASKURI.json','/'+str(j)),'normative_fields':[{'field':k,'before_present':k in x,'after_present':k in y,'equal':(k in x)==(k in y) and x.get(k)==y.get(k),'before_value_sha256':fh(x.get(k)),'after_value_sha256':fh(y.get(k))} for k in normative],'entire_row_equal':x==y,'new_execution_credit':0})
assert [(r['alias'],n['field']) for r in focus for n in r['normative_fields'] if not n['equal']]==[('T343','documente_produse')]
areaeffects={
 'A01':'T343 adaugă afirmații despre selectori tenant și gardă pe comandă. Sunt lectură documentară, fără RBAC demonstrat sau acceptare de securitate; cere sursa și actorul real înainte de probă.',
 'A02':'Cele șase registre auxiliare sunt identice. T386 este deja în populație, fără includere în cohorta istorică; nu se creează alt alias. Nicio schimbare DB demonstrată.',
 'A03':'G1, postarea și schemele contabile rămân deschise. Metadatele de stoc și declarațiile T343 nu probează valori Fact_Acct sau contabilizarea cutiilor/manoperei.',
 'A04':'Cerințele de achiziții, import și recepție nativă sunt neschimbate. Nu există probă nouă acceptată pentru NIR, retur furnizor sau factură.',
 'A05':'N05/T355 și taskurile WMS sunt normative neschimbate. Planul DocAction/comandă nativă și corelarea site trebuie recepționat separat. Findingul WMS și limitele G3 anterioare se păstrează.',
 'A06':'T343 are proveniență nouă, nu o stare nouă. CO/IP rămâne deschis; G3 și dubla scădere site/rezervare nu sunt demonstrate de document. T386 plan este identic cu precedentul.',
 'A07':'Documentul nou declară gărzile AWB/bulk și limita rambursării; nu transferă probe de livrare, anulare, încasare sau restituire. Continuarea cere fixture și oracol individual.',
 'A08':'T240 este identic. Paginarea JsonCatalogSource este o ipoteză separată de documentul T343; frontendul catalogului păstrează constatările și oracolele afirmative din Val04.',
 'A09':'Nu există scenariu nou ZK, rol nativ, mobil ori scanare. Refuzul de admitere UX din documentul T343 nu este defect de produs și nici scenariu trecut.',
 'A10':'Server HEAD c594 este distinct de candidatul df85. Nota și totalurile externe nu transferă acoperire. Cele șase rădăcini cu ștergere respinsă se păstrează; nu sunt atinse.'}
zones=[]
for i,z in enumerate(zonecheck['rows']):
    owner=z['owner'];assert sum(d['owner']==owner for d in dispatch)==z['assigned_files']
    zones.append({'owner':owner,'assigned_files_unchanged':z['assigned_files'],'source':ref(V/'Checklist_10_zone_Val04.json','/rows/'+str(i)),'disposition':areaeffects[owner],'new_executions':0,'peer_performed_inferred':False})

# Write additive outputs only; old waves remain byte-for-byte unchanged.
save(O/'Analiza_document_nou_T343_0245.json',analysis)
save(O/'Comparatie_997_randuri.json',{'utc':now(),'key':['proiect','id'],'before':ref(OLD/'00_STATUS_TASKURI.json'),'after':ref(NEW/'00_STATUS_TASKURI.json'),'rows':rows,'added':[],'removed':[]})
comparison={'schema':'eva.audit.checkpoint_comparison/3','utc':now(),'baseline_capture':OLD.name,'current_capture':NEW.name,'captures':captures,'comparison_key':['proiect','id'],'total':[997,997],'P01':[694,694],'added':[],'removed':[],'existing_changes':changes,'state_changes':[],'normative_or_provenance_changes':normchanges,'normative_change_interpretation':'Singura schimbare este adăugarea unei surse documentare la T343. Nu echivalăm documente_produse schimbat cu normative integral egale; analiza semantică este separată.','all_shared_rows_compared':997,'rows_ledger':ref(O/'Comparatie_997_randuri.json'),'auxiliary_registries':aux,'version_metadata':ref(O/'Provenienta_document_T343_0245.json'),
 'historic_completed_cohort':{'tasks':652,'criteria':2619,'new_final_vs_last_checkpoint':0,'reopened_vs_last_checkpoint':0,'T352_entire_row_equal':True,'T386_already_present_and_entire_row_equal':True,'T386_in_historic_652':False},'generic_delta_warning':{'source':ref(NEW/'Delta.json'),'its_comparison_base':bd['baseline'],'used_for_current_finalization':False,'explanation':'new_final din Delta generic folosește începutul auditului; nu este o închidere nouă față de captura 01:43.'},'exact_completion_dates_absent_remain_undocumented':True,'product_tests':0}
save(NEW/'Comparatie_ultimul_checkpoint.json',comparison)
save(O/'Continuitate_sigilii_Val04.json',{'utc':now(),'mode':'Verificare numai în citire a manifestelor, predării, recepției independente și publicării Val04.','artifacts':continuity,'referenced_file_instances_checked':sum(len(x['reference_checks']) for x in continuity),'unique_reference_files':len(hc),'all_valid':True,'limits':'Identitatea fișierului și validitatea pointerului JSON nu sunt execuție de produs. Câmpurile pending din edițiile imuabile sunt guvernate de recepția separată ulterioară.','previous_artifacts_modified':0})
save(O/'Dispozitii_10_zone_preflight_Val05.json',{'utc':now(),'candidate':H,'rows':zones,'A11_checklist':ref(R/'A11/Val04_loturi/Checklist_A11_dupa_R12_Val04_v1.json'),'contracts':a11check['contracts'],'contracts_closed':0,'technical_inventory':{'dispatch':ref(dispatchp),'catalog':ref(catalogp),'dispatch_identities':6728,'whole_git_paths':catalog_count,'new_source_exports_or_tests':0},'score':None})
counts={'bounded_evidence_source_identities':44,'original_component_or_method_primary':33,'shell_comparator_primary':5,'record_or_type_primary':2,'fixture_binding_metadata_primary':4,'event_pairs':50,'historic_R11_reference_only':116,'technical_identities':6728,'historical_task_dossiers':652,'historical_criteria':2619,'full_files':0,'full_tasks':0,'full_contracts':0,'open_contracts':17,'new_coverage_from_this_preflight':0}
supp={'schema':'eva.audit.r12.preflight0245/1','utc':now(),'candidate':H,'server_HEAD_at_capture':bd['server_worktree_head'],'mode':'LECTURA_SNAPSHOT_DOCUMENT_SI_CONTINUITATE; ZERO_TESTE_PRODUS','comparison':ref(NEW/'Comparatie_ultimul_checkpoint.json'),'previous_handoff':ref(V/'Handoff_R12_Val04_v1.json'),'previous_independent_receipt':ref(R/'A11/Val04_registru/Verdict_A11_R12_Val04_registru_v1.json'),'continuity':ref(O/'Continuitate_sigilii_Val04.json'),'document_analysis':ref(O/'Analiza_document_nou_T343_0245.json'),'focus_requirement_equality':focus,'all_fields_definition':'entire_row_equal compară întregul rând; egalitatea fiecărui câmp normativ/de proveniență este explicită separat. La T343 documente_produse diferă.','zones':ref(O/'Dispozitii_10_zone_preflight_Val05.json'),
 'gate_applicability_proposal':{'plan':ref(P/'Plan_delta_R12_v2.json'),'approved_plan_gate':ref(P/'A11_verdict_plan_delta_R12_v2.json'),'status':'PROPUNERE_A12; CONFIRMAREA_INDEPENDENTA_A11_IN_ASTEPTARE','existing_fixed_df85_scope':'Propunem păstrarea aplicabilității limitate la candidatul df85 și exporturile/binarele identificate. Populația și stările sunt identice; noul document este despre alte revizii, iar lectura nu identifică un amendament al oracolelor G3/paginare/CO-IP.','new_document':'Proveniență nominală schimbată explicit și analizată; LR-6 este obligație de test declarată pe altă ramură. Pentru auditarea acelei implementări sau modificarea oracolului, se cere plan nominal recepționat separat.','server_HEAD_c594_covered':False,'document_commit_021658_covered_as_product':False,'site_copy_d906cb0_covered_as_product':False,'no_credit_from_OID_identity':True,'completed_population_expansion_required':False,'T386':'Plan deja introdus și identic; în afara celor 652, fără credit nou și fără dată de închidere inventată.','next_JsonCatalogSource':'Protocol concret separat, cu sursă originală, index valid/absent/gol, limite numerice și martor; zero teste în acest preflight.','next_DocAction_site_G3':'Protocol concret separat, comandă nativă/rezervare/linie site, actor și ownership, citiri înainte/după/rollback/retry; fără extrapolarea probei PO directe din Val04.','native_preconditions':'Identitatea exactă a codului și JAR, seed/schema, serviciile, rolul și contextul trebuie probate la fiecare laborator. LastBuildInfo placeholder și FailOnBuildDiffer=N nu certifică echivalența buildurilor.','N05':'Findingul cantitativ WMS rămâne; G2 necontabilă, CPP/CPA distincte, numai componente recuperabile la dezambalare, fără refacerea automată a cutiilor sau manoperei.','DocAction_and_ZK':'Nu se atribuie noi tranzacții, note contabile, roluri sau clickuri ZK.','T343_CO_IP':'Controversa anterioară rămâne deschisă; acest document nu amendează nominal oracolul CO|CO|CO.','all17_contracts_open':True,'product_score':None},
 'population':{'total':997,'P01':694,'added':0,'removed':0,'existing_changed_rows':1,'state_changes':0,'changed_normative_provenance_rows':1,'historic_final_dossiers':652,'historic_criteria':2619,'newly_final':0,'reopened':0},'preserved_counts_NOT_new_execution':counts,
 'resources':{'A12_product_executions':0,'A12_new_labs_or_product_processes':0,'operational_mutations':0,'six_retained_scratch_roots_untouched':True,'cleanup_note':'Resursele reținute după refuzul automat nu sunt șterse, nici declarate restituite. Nu se ocolește refuzul.','existing_resources_source':ref(V/'Resurse_si_restituire_Val04.json'),'new_native_processes_in_this_preflight':0},'exact_completion_dates_absent_remain_undocumented':True,'audit_score':None}
supp['gate_applicability_proposal']['independent_applicability']=ref(R/'A11/Val05_preflight/Verdict_A11_aplicabilitate_R12_0245_v1.json')
supp['gate_applicability_proposal']['status']='APLICABILITATE_LIMITATA_DF85_CONFIRMATA_DE_A11; RECEPTIA_SUPLIMENTULUI_A12_IN_ASTEPTARE; PROTOCOALELE_CONCRETE_SEPARATE'
save(O/'Supliment_populatie_0245.json',supp)
save(O/'Handoff_preflight_Val05_v1.json',{'utc':now(),'candidate':H,'server_HEAD_at_capture':bd['server_worktree_head'],'previous':ref(V/'Handoff_R12_Val04_v1.json'),'previous_manifest':ref(V/'MANIFEST_R12_Val04.json'),'previous_independent_receipt':ref(R/'A11/Val04_registru/Verdict_A11_R12_Val04_registru_v1.json'),'supplement':ref(O/'Supliment_populatie_0245.json'),'comparison':ref(NEW/'Comparatie_ultimul_checkpoint.json'),'document_analysis':ref(O/'Analiza_document_nou_T343_0245.json'),'zones':ref(O/'Dispozitii_10_zone_preflight_Val05.json'),'A11_applicability_pending':True,'A11_A12_supplement_reception_pending':True,'counts_preserved':counts,'new_product_execution_credit':0,'next_action':'A11 confirmă aplicabilitatea porții și recepționează acest supliment; protocoalele concrete de paginare și DocAction/site se aprobă separat înainte de execuție.','score':None})
page='''<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Val05 — verificarea capturii 02:45</title><style>body{font:17px/1.55 system-ui;margin:auto;padding:24px;max-width:960px;color:#152334;background:#f6f8fb}a,code,td{overflow-wrap:anywhere}article{background:white;padding:22px;border:1px solid #d4dce4;border-radius:10px}.table{overflow-x:auto}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd5de;padding:8px;text-align:left}h1{font-size:1.7rem}</style><article><h1>Val05: populație identică, un document nou la T343</h1><p>Captura din 3 noiembrie 2026, 02:45:48 UTC, este comparată direct cu cea din 01:43:37 UTC. Sunt păstrate 997 de taskuri în tracker, dintre care 694 în P01. Nu există task nou, schimbare de stare, închidere sau redeschidere față de această bază.</p><div class="table"><table><tr><th>Verificare</th><th>Rezultat</th></tr><tr><td>Toate rândurile și șase registre auxiliare</td><td>997 de rânduri comparate; șase registre auxiliare identice octet cu octet.</td></tr><tr><td>T343 / P01.C10.T0025</td><td>Rămâne în audit. Progres 54 → 56; se schimbă auditorul declarat, observațiile, actualizarea și lista documentelor.</td></tr><tr><td>T386 / P01.C10.T0030</td><td>Este același task în plan, deja introdus în Val04; nu este nou aici.</td></tr><tr><td>Cohorta istorică</td><td>652 de fișe și 2.619 criterii, fără credit nou.</td></tr></table></div><h2>Ce dovedește documentul T343</h2><p>Fișierul Git a fost verificat la commitul declarat. El descrie o altă ramură și o copie de site, cu verdictul propriu «NU TRECE — 9/10» și un mutant B16 declarat viu. Rambursarea și anularea nu au fost executate în acel dosar; proba UX independentă a fost refuzată la admitere. Nota, cele 283 de teste și mutanții declarați nu devin rezultate ale auditului nostru.</p><p>Lista documentelor constituie o schimbare de proveniență nominală. Nu afirmăm că toate câmpurile normative sunt egale. Lectura nu identifică un amendament pentru controversa CO/IP, G3 sau paginarea catalogului.</p><h2>Versiunea și limita verificării</h2><p>Candidatul rămâne <code>df85d33c1648ce2b2df130a60a05ef696e2e5480</code>. HEAD-ul serverului din captură este separat: <code>c594a93a1d4e606f8c2e432108a29e97244d692e</code>. Acesta nu primește acoperire. Preflightul nu execută produsul și nu schimbă date operaționale.</p><p>Cele 44 de surse cu dovezi limitate din Val04 rămân 33 de surse cu metode/componente originale, 5 comparatoare shell, 2 utilizări de tip și 4 legături de fixture/metadate. Nu sunt 44 de funcționalități recepționate integral. Toate cele 17 contracte rămân deschise.</p><h2>Continuare</h2><p>Aplicabilitatea porții se propune pentru aceeași versiune și același domeniu, spre confirmare A11. Paginarea Java și comanda nativă cu linie site necesită protocoale concrete separate. Cele șase directoare reținute după refuzul automat de ștergere nu sunt atinse.</p><ul><li><a href="Supliment_populatie_0245.json">Suplimentul nominal</a></li><li><a href="Analiza_document_nou_T343_0245.json">Analiza documentului T343, cu ancore</a></li><li><a href="Comparatie_997_randuri.json">Comparația tuturor rândurilor</a></li><li><a href="Continuitate_sigilii_Val04.json">Verificarea sigiliilor Val04</a></li><li><a href="Dispozitii_10_zone_preflight_Val05.json">Dispoziții pentru cele zece zone</a></li><li><a href="Handoff_preflight_Val05_v1.json">Predarea pentru continuare</a></li></ul><p>Recepția independentă ulterioară rămâne un document separat; acest pachet nu își acordă notă sau acceptare.</p></article></html>'''
assert not (O/'index_preflight.html').exists()
(O/'index_preflight.html').write_text(page,encoding='utf-8')
shutil.copyfile(__file__,O/'build_preflight_0245.py')
instances=0;pointers=0
for p in [x for x in O.iterdir() if x.suffix=='.json']+[NEW/'Comparatie_ultimul_checkpoint.json']:
    for rr in refs(load(p)):
        checkref(rr,p);instances+=1;pointers+=rr.get('pointer') is not None
for href in re.findall(r'href="([^"]+)"',page):assert (O/href).exists()
assert all(ref(p)['sha256']==expected for p,expected in expectations)
qa={'utc':now(),'method':'Comparaison exacte des données et SHA/pointeurs; aucun test de produit.','all_shared_rows_checked':997,'P01':694,'added':0,'removed':0,'state_changes':0,'changed_rows':['T343'],'changed_fields_count':5,'normative_provenance_changes':['T343.documente_produse'],'focus_tasks':len(focus),'focus_normative_predicates':len(focus)*len(normative),'capture_file_hashes_checked':14,'auxiliary_equal_bytes':6,'reference_instances_checked':instances,'JSON_pointers_checked':pointers,'technical_identity_count':6728,'whole_git_path_count':catalog_count,'historical_cohort':[652,2619],'zones':10,'open_contracts':17,'new_product_executions':0,'new_functional_acceptances':0,'html_links_exist':6,'visual_browser_review_performed':False,'previous_expected_hashes_rechecked':len(expectations),'issues':[],'score':None}
qa['method']='Comparație exactă a datelor, SHA și pointeri; zero teste de produs.'
save(O/'QA_preflight_0245.json',qa)
manifest={'utc':now(),'candidate':H,'files':[ref(p) for p in sorted(O.iterdir())]+[ref(NEW/'Comparatie_ultimul_checkpoint.json')],'inputs':[ref(p) for p,_ in expectations]+[ref(dispatchp),ref(catalogp),ref(V/'Checklist_10_zone_Val04.json'),ref(V/'Reconciliere_metrici_si_limite_Val04.json')],'A11_applicability_and_receipt_pending':True,'no_self_reference':True,'old_artifacts_modified':0,'no_product_execution':True}
save(O/'MANIFEST_preflight_Val05_0245.json',manifest)
print(json.dumps({'manifest':ref(O/'MANIFEST_preflight_Val05_0245.json'),'handoff':ref(O/'Handoff_preflight_Val05_v1.json'),'supplement':ref(O/'Supliment_populatie_0245.json'),'comparison':ref(NEW/'Comparatie_ultimul_checkpoint.json'),'QA':qa},ensure_ascii=False,indent=2))
