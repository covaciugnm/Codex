import collections,copy,gzip,hashlib,html,json,pathlib,sys
from datetime import datetime,timezone
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');E=B/'executie';R=E/'R12_fisiere';O=R/'A12/Val_03';P=R/'A12/Val_02';H='df85d33c1648ce2b2df130a60a05ef696e2e5480'
MEM={};CACHE={};CHECKS=[];INPUTS=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
def read(p):return MEM[p.name] if p.parent==O and p.name in MEM else p.read_bytes()
def load(p):return json.loads(read(p).decode('utf-8-sig'))
def ref(p,pointer=None):
 b=read(p);d={'path':p.relative_to(B).as_posix(),'sha256':sha(b),'bytes':len(b)}
 if pointer is not None:d['pointer']=pointer
 return d
def put(n,d):
 assert n not in MEM;assert not (O/n).exists(),n;MEM[n]=enc(d);return ref(O/n)
def point(d,p):
 for k in p.lstrip('/').split('/') if p else []:
  k=k.replace('~1','/').replace('~0','~');d=d[int(k)] if isinstance(d,list) else d[k]
 return d
def manifest(p,expected=None):
 if expected:assert sha(read(p))==expected,str(p)
 d=load(p);items=d.get('files',d.get('entries',d.get('artifacts')))
 if items is None:items=[v for v in d.values() if isinstance(v,dict) and 'path' in v and 'sha256' in v]
 if isinstance(items,int):items=d['entries']
 if isinstance(items,dict):items=[dict(v,path=k) for k,v in items.items()]
 for x in items:
  q=(B if x['path'].startswith('executie/') else p.parent)/x['path'];assert sha(read(q))==x['sha256'],str(q);CHECKS.append(ref(q))
 for x in d.get('inputs',[]):
  q=B/x['path'];assert sha(read(q))==x['sha256'];CHECKS.append(ref(q))
 INPUTS.append(ref(p));return d
def priorcheck(p,h):assert sha(read(p))==h;INPUTS.append(ref(p));return load(p)
def lot(directory,manifest_name,mhash,receipt,receipt_hash,seal):
 p=R/directory;manifest(p/manifest_name,mhash);v=priorcheck(R/receipt,receipt_hash);assert mhash in json.dumps(v);manifest(R/seal)
 return p,v,ref(R/receipt)
priorcheck(P/'MANIFEST_R12_Val02.json','f169311d8a251f6f01cc47facdb20b74434a7afe0c9687c6792d587723decc5d');manifest(P/'MANIFEST_R12_Val02.json')
priorcheck(R/'A11/Val02_registru/Verdict_A11_R12_Val02_registru_v1.json','e7f7d03f5198ac40e204943b7b9e16453d19494ae1d2fa58d5bbce4a53b1f6b4');manifest(R/'A11/Val02_registru/Sigiliu_A11_R12_Val02_registru_v1.json')
manifest(O/'MANIFEST_preflight_Val03_0039.json','c7e4cfa0bd47cf692be7be08f71b2e0427d19151d4b5d662c3bdfe6640c0aa5b')
priorcheck(R/'A11/Val03_preflight/Verdict_A11_receptie_supliment_0039_v1.json','00d5813840702b4a11b4bf677213134ac073b880f1427c895e8bc87b4f659756')
prior=[json.loads(x) for x in gzip.decompress(read(P/'Registru_6728_R12_Val02.jsonl.gz')).decode().splitlines()];D={x['path']:x for x in prior};assert len(D)==len(prior)==6728
updated=copy.deepcopy(prior);UD={x['path']:x for x in updated};events=[];cases=[];findings=[];static=[]
A6,v6,r6=lot('A06_T343_instrumente_lot03','MANIFEST_A06_lot03.json','5743839e4a93c1cb2d7e61b010081668693ea1ae4f4fcae388876b96d1a319fe','A11/Val03_loturi/Verdict_A11_A06_lot03_v1.json','0d75650460ef5d40f03882ee3761fda6b74e3caa4f5f9ff1782ec832f1504842','A11/Val03_loturi/Sigiliu_A11_A06_lot03_v1.json')
G,vG,rG=lot('A06_Rezervari_nativ_lot04','MANIFEST_A06_rezervari_lot04.json','bf5dee20c4e539bc10610ec17ba23433d907a71e483f53fb31c0dd36293e4232','A11/Val03_loturi/Verdict_A11_G3_SQL_lot04_v1.json','033ff6bfb76269eb37a29ad888e249d3e009c37aa2d6f6333928fd46a9fa3e73','A11/Val03_loturi/Sigiliu_A11_G3_SQL_lot04_v1.json')
manifest(G/'MANIFEST_supliment_lectura_v1.json','658bf11cbabca391a44453ed1cb356970228bf2ef843585ab7e41c20e67e7455')
cfg=load(pathlib.Path(sys.argv[1]));assert cfg['head']==H
if not cfg.get('A10_receipt') or not cfg.get('N05_checkpoint'):raise SystemExit('Final publishing requires A10 independent receipt and N05 sealed checkpoint or independent receipt.')
A10,v10,r10=lot('A10_Instrumente_ramase_lot03','Manifest_lot03.json','7b3289641e6321eeccbac23e3fb9d03ebc570f9906928e9902b3aea5ff41724d',cfg['A10_receipt']['path'],cfg['A10_receipt']['sha256'],cfg['A10_receipt']['seal'])
manifest(A10/'Manifest_lectura_v1.json','0c181f58d9216adcde136ad88b6ced78cccb4b406958850de1d050be173ac90d')
def identity(path,oid,s,local):
 d=D[path];b=read(local);assert sha(b)==s;assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid==d['git_oid'];return d
def add_event(path,oid,s,local,eid,executor,method,receipt,dossier,details):
 d=identity(path,oid,s,local);assert not any(x['path']==path for x in events)
 ev={'event_id':eid,'path':path,'git_oid':oid,'sha256':s,'source':ref(local),'owner':d['owner'],'planned_peer':d['planned_peer'],'control':d['control'],'pipeline_candidates':d['pipeline_candidates'],'task_candidates_preserved':d['task_candidates'],'actual_executor':executor,'planned_peer_performed_not_inferred':True,'nominal_peer_reception':None,'independent_receipt':receipt,'producer_dossier':dossier,'method_kind':method,'whole_file_accepted':False,'task_closed':False,**details};events.append(ev);return ev
raw6=load(A6/'Results.json');raw6.append(load(A6/'Supplement_case.json'));ids6={x['id']:(i,x) for i,x in enumerate(raw6)}
oracle6={
'I14_list_None':'Lista completă a ID-urilor declarate; nu execuție de mutanți.', 'I14_list_ext':'Numai mutanții ext și controlul aplicabil.', 'I14_list_panou':'Numai mutanții panou și controlul aplicabil.', 'I14_list_bl':'Numai mutanții bl și controlul aplicabil.', 'I14_list_unknown':'Grup necunoscut: nu se inventează mutanți eligibili.',
'I14_baseline':'Controlul A00 copiază fără modificare semantică; sursa conservată.', 'I14_valid':'O singură modificare în funcția țintă; sursa de intrare conservată.', 'I14_anchor_missing':'Ancoră absentă refuzată explicit.', 'I14_anchor_double':'Ancoră ambiguă refuzată, fără alegere tacită.', 'I14_old_missing':'Textul vechi absent refuzat.', 'I14_old_double':'Textul vechi ambiguu nu dovedește o țintă unică.', 'I14_old_next_function':'Textul din funcția următoare nu trebuie să satisfacă ținta declarată.', 'I14_compile_failure':'Eroarea de compilare separată de mutant valid.', 'I14_unknown_id':'ID necunoscut refuzat înainte de ștergerea destinației.', 'I14_missing_tests':'Lipsa testelor nu este probă de detecție.', 'I14_retry_valid':'Repetarea aceleiași intrări păstrează sursa și modificarea deterministă.', 'I14_unknown_command':'Comanda necunoscută trebuie diagnosticată explicit.', 'I14_no_arguments':'Lipsa comenzii trebuie diagnosticată explicit.',
'I15_assert':'Control valid și aserțiune eșuată: clasificare separată de setup, cu limita cauzală explicită.', 'I15_setup':'Setup eșuat înainte de corp nu demonstrează singur detecția mutantului.', 'I15_collect':'Eroare de colectare separată de aserțiune de business.', 'I15_empty':'Zero teste colectate nu dovedește mutant ucis.', 'I15_pass':'Suită verde pe mutant: mutant viu, nu ucis.', 'I15_baseline_error':'Control roșu trebuie să împiedice recepția mutantului.', 'I15_queue_refused':'Refuz de coadă nu este execuție sau defect de produs.', 'I15_bad_export':'Export invalid trebuie să rămână eroare distinctă.',
'I16_complete':'Control și lista completă pot satisface agregarea numai în fixture cu proveniență declarată.', 'I16_only_control':'Numai A00 nu este numitor complet de mutanți.', 'I16_stale_fail':'Jurnal vechi plus runner eșuat nu demonstrează execuția curentă; cauze combinate.', 'I16_no_log_fail':'Jurnal lipsă și runner eșuat refuzate.', 'I16_duplicate_control':'Control duplicat refuzat.', 'I16_empty':'Jurnal gol refuzat.', 'I16_unknown_live':'Mutant viu/necunoscut nu poate fi numărat ca succes.', 'I16_not_run':'NERULAT nu este mutant verificat.', 'I16_skip':'SARIT nu este mutant verificat.', 'I16_setup_from_original_I15_BL':'BL cu eroare setup și celelalte două seturi sintetice nu certifică detecția semantică.'}
for ix in (14,15,16):
 p=A6/f'Fisa_I{ix}.json';d=load(p);rp=next(i for i,x in enumerate(v6['per_file']) if x['control']==d['control']);rs=ref(R/'A11/Val03_loturi/Verdict_A11_A06_lot03_v1.json',f'/per_file/{rp}')
 ev=add_event(d['file'],d['oid'],d['sha256'],A6/'sources'/pathlib.Path(d['file']).name,'R12V03-'+d['control'],'A06',d['execution_kind'],rs,ref(p),{'audit_control':d['control'],'task_alias':'T343','canonical_task':d['canonical_task'],'task_state':'audit','requirement':d['requirement'],'actor':d['actor'],'entry_point':d['normal_path'],'native_reuse':d['native_idempiere'],'positive':d['positive'],'counterexample':d['counterexample'],'persistent_effect':d['persistent_effect'],'limits':d['limits']+v6['limitations'],'case_ids':d['case_ids']})
 for cid in d['case_ids']:
  i,c=ids6[cid];src=ref(A6/'Results.json',f'/{i}') if i<len(raw6)-1 else ref(A6/'Supplement_case.json')
  cases.append({'id':'A06:'+cid,'producer_id':cid,'control':d['control'],'method_kind':d['execution_kind'],'actor':d['actor'],'expected':oracle6[cid],'oracle_kind':'A12 normative reading of declared protocol and independent receipt; no PASS inferred','oracle_sources':[ref(A6/'Protocol_sigillat_inainte_executie.json','/oracles'),r6],'observed':c,'source':src,'whole_criterion_credit':False})
assert len(cases)==36
for i,x in enumerate(load(A6/'Raport_A06_lot03.json')['findings']):
 j=next(j for j,y in enumerate(v6['findings']) if y['id']==x['id']);findings.append({'id':x['id'],'producer_claim':x,'source':ref(A6/'Raport_A06_lot03.json',f'/findings/{i}'),'effective_A11':v6['findings'][j],'independent_receipt':ref(R/'A11/Val03_loturi/Verdict_A11_A06_lot03_v1.json',f'/findings/{j}'),'task_closed':False})
gresults=load(G/'Results.json');gsrc={x['path']:x for x in load(G/'Sources.json')}
for i,c in enumerate(load(G/'Coverage.json')):
 s=gsrc[c['path']];identity(s['path'],s['oid'],s['sha256'],B/s['source_copy']);j=next(j for j,x in enumerate(vG['per_file']) if x['file']==pathlib.Path(c['path']).name);rs=ref(R/'A11/Val03_loturi/Verdict_A11_G3_SQL_lot04_v1.json',f'/per_file/{j}')
 if not c['sql_comparator']:
  static.append({'path':c['path'],'git_oid':c['oid'],'source':ref(B/s['source_copy']),'scope':'BOUNDED_STATIC_SUPPORT_ONLY','producer':ref(G/'Coverage.json',f'/{i}'),'receipt':rs,'execution_credit':False});continue
 add_event(c['path'],c['oid'],c['sha256'],B/s['source_copy'],'R12V03-G3-'+pathlib.Path(c['path']).stem,'A06','SQL_COMPARATOR_PARTIAL',rs,ref(G/'Coverage.json',f'/{i}'),{'audit_control':None,'canonical_task':None,'task_mapping':'SHARED_NO_TASK_ASSIGNED_PENDING_NOMINAL_MAPPING','requirement':c['requirement'],'actor':'Auditor în SQLite memory cu rânduri sintetice; fără actor ERP/RBAC','entry_point':c['normal_path'],'native_reuse':vG['native_first'],'positive':'9 fixtures concordă cu oracolul rezervărilor SO; comparator SQL, nu Java','counterexample':'3 fixtures diferă; PO este inclus în suma scăzută din disponibil','persistent_effect':'Niciun efect business; SQLite în memorie închisă','limits':vG['limits'],'case_ids':[x['id'] for x in gresults['cases']],'static_formula_clarification':ref(G/'Clarificare_semantica_disponibil_v1.json')})
for i,c in enumerate(gresults['cases']):cases.append({'id':'G3:'+c['id'],'producer_id':c['id'],'method_kind':'SQL_COMPARATOR_PARTIAL','input':c['rows'],'expected':c['expected_sales_reservations'],'observed':c['two_sql_results'],'source':ref(G/'Results.json',f'/cases/{i}'),'evaluation_count':2,'distinct_sql_texts':1,'scope':'12 unique fixtures, not24 requirements or Java tests','derived_available_warning':'Illustrative clamped arithmetic in raw result is not both Java methods output; RezervareStoc has no zero clamp.','whole_criterion_credit':False})
findings.append({'id':vG['finding'],'producer_claim':load(G/'Finding.json'),'source':ref(G/'Finding.json'),'effective_A11':vG,'independent_receipt':rG,'clarification':ref(G/'Clarificare_semantica_disponibil_v1.json'),'count_once_for_two_sites':True,'canonical_task':None})
for ix in (1,4,10,17):
 p=A10/f'Fisa_I{ix:02}.json';d=load(p);s=d['source'];method='ORIGINAL_COMPONENT_PYTHON_AND_JS_SYNTHETIC_DOM' if ix==17 else 'PATH_REMAPPED_SHELL_COMPARATOR_WITH_SHIMS'
 j=next(j for j,x in enumerate(v10['files']) if x['id']==d['id']);assert v10['files'][j]['OID']==s['git_object'] and v10['files'][j]['sha256']==s['sha256']
 ev=add_event(s['path'],s['git_object'],s['sha256'],A10/'sources'/pathlib.Path(s['path']).name,'R12V03-'+d['id'],'A10',method,dict(r10,pointer=f'/files/{j}'),ref(p),{'audit_control':d['id'],'task_alias':d['task']['technical'],'canonical_task':d['task']['canonical'],'task_state':d['task']['state_as_declared'],'producer_task_snapshot_not_current_state_proof':d['task']['source'],'requirement':d['requirement'],'actor':d['actor'],'entry_point':d['normal_path'],'native_reuse':d['native_reuse'],'positive':d['positive'],'positive_limit':d['positive_scope_executed'],'counterexamples':d['counterexamples'],'persistent_effect':d['persistence_observed'],'limits':d['remaining']+v10['rejected_claims']+v10['boundary_limits'],'case_count':d['cases_unique']})
shell_oracles={
'I04_acquire_error_stdout':'Acquire rc4 cu stdout nevid: niciun slot dobândit; release nu poate fi declarat reușit fără achiziție demonstrată.',
'I04_acquire_refused':'Acquire refuzat rc4: fără execuție utilă, fără credit produs sau slot.',
'I04_collector_fail':'Eșecul colectorului rămâne vizibil și împiedică atestarea completă; compară rc final cu statutul individual.',
'I04_contra_false':'Controlul negativ false nu justifică recepție completă chiar la rc final0.',
'I04_existing_work':'Director existent: refuz înainte de reutilizare distructivă.',
'I04_judge_fail':'Eșecul judecătorului rămâne distinct de pașii reușiți; nu se deduce PASS din rc final.',
'I04_last_fail':'Eșecul ultimului pas: cauza trebuie păstrată în statut/rc.',
'I04_mask_fail':'Eșecul mascării: oprire, nicio captură nativă recepționată.',
'I04_network_false_hash_mismatch':'Network=false și hash diferit: fără atestare izolare/integritate; pașii8/9 afișează fără aserție.',
'I04_normal':'Parcurs sintetic nominal: păstrează statusurile și numitorul real; nu reprezintă L6 nativ.',
'I04_pg_fail':'Eroare PostgreSQL din stub rc31: oprire, fără test business demonstrat.',
'I04_primary_and_cleanup_fail':'Eroare primară și eroare cleanup: păstrează ambele fără mascarea primei.',
'I04_privacy_fail':'Eșec gardă sintetică: păstrare și propagare potrivit contractului porții.',
'I04_stop_release_fail':'Stop/release rc72: fără declararea restituirii efective; niciun slot real testat.',
'I01_changed':'Membru JAR modificat: diferență detectabilă prin oracol SHA-256 independent.',
'I01_child_fail':'Statusuri copii rc41/42/43 vizibile; rc final0 nu recepționează gărzile.',
'I01_corrupt':'JAR corupt: eroare explicită, fără echivalență binară completă.',
'I01_duplicate_last_base':'Două intrări cu același nume, variantă apoi bază: cardinalitate/identitate diferite chiar dacă dicționarul CRC dă0.',
'I01_duplicate_last_variant':'Două intrări cu același nume, bază apoi variantă: pierderea primului membru nu este acceptabilă chiar dacă CRC diferă.',
'I01_missing_class':'Clasă absentă: diferență de membri detectabilă.',
'I01_missing_jar':'JAR absent: eroare explicită, fără comparație completă.',
'I01_normal':'Membri unici identici: comparație locală concordantă, fără încărcare OSGi.',
'I10_cleanup_fail':'Cleanup no-op rc73 separat de gardă rc41; cauze păstrate, fără ștergere reală demonstrată.',
'I10_merge_conflict':'merge-tree real local rc1 trebuie raportat1 chiar după substituția rev-parse.',
'I10_normal':'Gărzi sintetice nominale și canar rc1 așteptat raportate separat; nu sunt gărzi produs revalidate.',
'I10_partner_fail':'Gardă partener sintetică rc41: diagnostic distinct; impactul asupra porții depinde de consumator.',
'I10_secret_fail':'Gardă secrete sintetică rc42: diagnostic distinct; rc final0 nu validează garda.'}
for name,kind in [('Rezultate_I17_pure_28.json','ORIGINAL_PURE_COMPONENT'),('Rezultate_I17_DOM_18.json','ORIGINAL_COMPONENT_SYNTHETIC_DOM'),('Rezultate_shell_27_cazuri.json','SHELL_COMPARATOR_WITH_SHIMS')]:
 for i,c in enumerate(load(A10/name)):
  cid=c.get('id',c.get('case'));oracle=shell_oracles[cid] if kind=='SHELL_COMPARATOR_WITH_SHIMS' else {'expected_value':c.get('oracle'),'null_is_expected_no_selector_or_value':c.get('oracle') is None}
  cases.append({'id':'A10:'+cid,'producer_id':cid,'method_kind':kind,'oracle':oracle,'oracle_authority':'Original declared fixture/protocol plus receipt-qualified interpretation; shell effects are comparators, no PASS assigned by A12.','observed':c,'source':ref(A10/name,f'/{i}'),'protocol':ref(A10/'Protocol_v1.json'),'independent_receipt':r10,'whole_criterion_credit':False})
assert len(cases)==121 and len({x['id'] for x in cases})==121
for i,f in enumerate(load(A10/'Constatari.json')):
 j=next(j for j,x in enumerate(v10['finding_dispositions']) if f['id'].endswith(x['id']));findings.append({'id':f['id'],'producer_claim':f,'source':ref(A10/'Constatari.json',f'/{i}'),'effective_A11':v10['finding_dispositions'][j],'independent_receipt':dict(r10,pointer=f'/finding_dispositions/{j}'),'scope':'Only receipt-qualified observation, no task closure'})
assert len(events)==9 and len(static)==2
case_ref=put('Cazuri_nominale_121.json',{'head':H,'rows':cases,'counts':{'A06_helper':36,'A10_helper':73,'G3_unique_fixtures':12,'G3_SQL_evaluations':24},'not_global_PASS_total':True})
for ev in events:
 ev['case_links']=[ref(O/'Cazuri_nominale_121.json',f'/rows/{i}') for i,c in enumerate(cases) if (ev['actual_executor']=='A10' and c['id'].startswith('A10:'+ev['audit_control'].split('-')[1]+'_')) or (ev['method_kind']=='SQL_COMPARATOR_PARTIAL' and c['id'].startswith('G3:')) or c.get('control')==ev.get('audit_control') and c.get('control') is not None]
 assert ev['case_links'],ev['event_id']
events_ref=put('Evenimente_9_surse_si_2_lecturi.json',{'head':H,'rows':events,'static_support_only':static,'no_dependency_automatic_credit':True})
put('Constatari_loturi_Val03.json',{'rows':findings,'count_by_finding_id_not_by_affected_file':True,'previous_findings':ref(P/'Constatari_lot02.json'),'score':None})
delta=[]
for i,e in enumerate(events):
 u=UD[e['path']];old=copy.deepcopy(u['axis']);assert old['component_exercised']=='UNVERIFIED_R12'
 u['axis']['read']='OBSERVED_AT_LINKED_SCOPE';u['axis']['component_exercised']='SQL_COMPARATOR_PARTIAL' if e['method_kind']=='SQL_COMPARATOR_PARTIAL' else ('SHELL_COMPARATOR_PARTIAL' if 'SHELL' in e['method_kind'] or 'BASH' in e['method_kind'] else 'ORIGINAL_COMPONENT_PARTIAL')
 u['current_evidence'].append({'event_id':e['event_id'],'source':ref(O/'Evenimente_9_surse_si_2_lecturi.json',f'/rows/{i}'),'method_kind':e['method_kind'],'scope':'PARTIAL_ONLY','independent_reception':e['independent_receipt']});u['peer_receipts']['independent_A11']=e['independent_receipt'];u['executor_for_current_event']=e['actual_executor'];u['planned_peer_performed_not_inferred']=True
 delta.append({'path':u['path'],'before':old,'after':u['axis'],'event_id':e['event_id']})
for i,s in enumerate(static):
 u=UD[s['path']];u['axis']['read']='BOUNDED_STATIC_SUPPORT_ONLY';u['current_evidence'].append({'source':ref(O/'Evenimente_9_surse_si_2_lecturi.json',f'/static_support_only/{i}'),'scope':'STATIC_ONLY_NO_EXECUTION'});assert u['axis']['component_exercised']=='UNVERIFIED_R12'
put('Delta_Val03.json',{'previous_register':ref(P/'Registru_6728_R12_Val02.jsonl.gz'),'rows':delta,'static_support_paths':[x['path'] for x in static],'new_source_identities':0})
# N05 is separately received; configure only nominal, source-OID-verified coverage from the authoritative receipt.
n05=cfg['N05_checkpoint'];n05p=B/n05['path'];priorcheck(n05p,n05['sha256']);n05doc=load(n05p)
for m in n05.get('manifests',[]):manifest(B/m['path'],m['sha256'])
if n05.get('receipt'):
 nr=B/n05['receipt']['path'];priorcheck(nr,n05['receipt']['sha256']);n05doc={'producer':ref(n05p),'independent_receipt':ref(nr),'receipt':load(nr),'producer_summary':n05doc}
native_events=[];native_reads=[];native_phase_counts={}
if cfg.get('publication_allowed'):
 assert n05.get('receipt'),'Native mapping requires actual independent receipt'
 N=n05p.parent;nd=load(n05p);nf=load(N/'Fise_sursee_N05_v1.json');assert nf['head']==H and len(nf['files'])==46
 matrixpath=R/'A11/Val03_loturi/Matrice_A11_N05_sursee_v1.json';nmat=priorcheck(matrixpath,'6f53f02fef8d764938644e3be3f4a695b80257f11986d7f7f5ba4e9821c37e25');nmidx={x['path']:(i,x) for i,x in enumerate(nmat['files'])}
 nqualification=R/'A11/Val03_loturi/Supliment_A11_N05_trasabilitate_v1.json';priorcheck(nqualification,'d118dc5abf7bacd35057133767f18c813415c2f001c3ea9b3a5b253471c63650')
 overlays={x['path']:(i,x) for i,x in enumerate(load(N/'Fise_supliment_cale_normala_v1.json')['files'])}
 for i,s in enumerate(nf['files']):
  ni,nmr=nmidx[s['path']];assert (s['oid'],s['sha256'],s['phase'],s['methods_in_scope'])==(nmr['oid'],nmr['sha256'],nmr['phase'],nmr['methods']);s=dict(s)
  if s['path'] in overlays:s['normal_path']=overlays[s['path']][1]['normal_path']
  local=N/'surse_df85'/s['path'].split('src/com/eva/ro/contab/',1)[1];d=identity(s['path'],s['oid'],s['sha256'],local)
  if s['state'].startswith('LECTUR'):
   assert nmr['scope']=='STATIC_ONLY'
   u=UD[s['path']];before=copy.deepcopy(u['axis']);u['axis']['read']='BOUNDED_STATIC_SUPPORT_ONLY';u['current_evidence'].append({'source':ref(N/'Fise_sursee_N05_v1.json',f'/files/{i}'),'scope':'N05_STATIC_ONLY_NO_EXECUTION','independent_reception':ref(nr)})
   native_reads.append({'path':s['path'],'git_oid':s['oid'],'source':ref(local),'producer':ref(N/'Fise_sursee_N05_v1.json',f'/files/{i}'),'owner':d['owner'],'planned_peer':d['planned_peer'],'scope':'BOUNDED_STATIC_SUPPORT_ONLY','before_axis':before,'after_axis':u['axis'],'independent_receipt':ref(nr),'execution_credit':False});continue
  assert s['path'] in n05['accepted_runtime_paths'] and nmr['scope']!='STATIC_ONLY',s['path']
  phase=s['phase'];method='NATIVE_BUSINESS_METHOD_PARTIAL' if phase=='business' and s['methods_in_scope'] else ('NATIVE_TRANSITIVE_VALUE_TYPE_USE' if phase=='business' else 'NATIVE_FIXTURE_OR_BINDING_PARTIAL')
  ev=add_event(s['path'],s['oid'],s['sha256'],local,'R12V03-N05-'+pathlib.Path(s['path']).stem,'A05',method,ref(nr),ref(N/'Fise_sursee_N05_v1.json',f'/files/{i}'),{'audit_control':'N05','task_alias':'T355','canonical_task':'P01.C03.T0029','task_state_not_inferred_from_test':True,'requirement':s['requirement'],'actor':s['actor'],'entry_point':s.get('normal_path','Native registered handler or fixture path; see producer fiche'),'methods_in_scope':s['methods_in_scope'],'phase':phase,'direct_class_binding_logged':s['direct_class_binding_logged'],'native_reuse':'Existing MProcess, PO.saveEx, EventAdmin and native transactions; EVA original methods/handlers in isolated synthetic clone','positive':s['positive'] if 'positive' in s else 'Binding or fixture only; no whole business acceptance','counterexample':s.get('counterexample'),'persistent_effect':s.get('persistent_effect'),'control_scope':s['control'],'limits':[s.get('limit',''),*nd['limits'],nd['rollback_process_metadata_limit']],'linked_scenarios_not_all_methods_covered':ref(n05p,'/cases')})
  ev['independent_source_matrix']=ref(matrixpath,f'/files/{ni}');ev['independent_scope']=nmr['scope'];ev['scope_qualification']=ref(nqualification)
  if s['path'] in overlays:ev['normal_path_addendum']=ref(N/'Fise_supliment_cale_normala_v1.json',f'/files/{overlays[s["path"]][0]}')
  events.pop();native_events.append(ev)
 assert len(native_events)==17 and len(native_reads)==29
 native_phase_counts=dict(collections.Counter(x['phase'] for x in native_events))
 native_ref=put('Evenimente_N05_17_si_29_lecturi.json',{'head':H,'rows':native_events,'static_only':native_reads,'phase_counts':native_phase_counts,'direct_methods_not_inferred_for_record_enum':True,'owner_peer_preserved_from_dispatch':True,'planned_domain_peers_not_asserted_performed':True,'independent_receipt':ref(nr)})
 for i,e in enumerate(native_events):
  u=UD[e['path']];before=copy.deepcopy(u['axis']);assert before['component_exercised']=='UNVERIFIED_R12';u['axis']['read']='OBSERVED_AT_LINKED_NATIVE_SCOPE';u['axis']['component_exercised']=e['method_kind'];u['axis']['ERP_DB']=e['method_kind']
  if e['direct_class_binding_logged']:u['axis']['installed_binding']='ORIGINAL_CLASS_BOUND_IN_ISOLATED_NATIVE_CLONE_ONLY'
  u['current_evidence'].append({'event_id':e['event_id'],'source':ref(O/'Evenimente_N05_17_si_29_lecturi.json',f'/rows/{i}'),'method_kind':e['method_kind'],'phase':e['phase'],'independent_reception':ref(nr)});u['peer_receipts']['independent_A11']=ref(nr);u['executor_for_current_event']='A05';u['planned_peer_performed_not_inferred']=True
 put('Cazuri_N05_7_scenarii.json',{'head':H,'rows':[{'id':'N05:'+c['id'],'producer':ref(n05p,f'/cases/{i}'),'declared_case':c,'independent_receipt':ref(nr),'whole_criterion_credit':False} for i,c in enumerate(nd['cases'])],'scope':'Seven native scenarios distinct from121 helper/SQL case identities, no multiplication by17 source paths','transaction_boundary':nd['provenance']['coordination_variation'],'rollback_limit':nd['rollback_process_metadata_limit']})
 hdpath=B/'executie/R10/taskuri/Fisa_T355.json';hd=load(hdpath);assert hd['canonical']=='P01.C03.T0029'
 links=[]
 observations={
 'T355-R2-001':('PARTIAL_NATIVE_CONSERVATION_COUNTEREXAMPLE','S01:10→8+1set→10; C01:BOM2→3 while packaging uncommitted, unpacking returns11. Original18-component example, picking and UI not run.'),
 'T355-R2-002':('PARTIAL_NATIVE_CONSERVATION_COUNTEREXAMPLE','BOM/native process/handler and WMS movements observed; nativeQty10 and zero Facts on fixtures. Existing Productie/Dezmembrari screens not opened, full accounting pipeline not accepted.'),
 'T355-R2-003':('NO_NEW_CONFORMITY_EVIDENCE','R01 retries after rollback with a new AD_PInstance and exactly2 movements; it does not repeat the same committed note and cannot resolve the historic idempotency finding.'),
 'T355-R2-004':('NOT_EXECUTED_IN_N05','No box or0.5hour labor fixture, no G1 cost recognition, no credit from zero Fact_Acct.')}
 for i,c in enumerate(hd['operative_criteria_and_audit_criteria']):
  status,obs=observations[c['id']];links.append({'criterion_id':c['id'],'requirement_literal':c['normative_content'],'full_expected_oracle':c['expected_oracle'],'historical_source':ref(hdpath,f'/operative_criteria_and_audit_criteria/{i}'),'new_observation_status':status,'observed_and_limit':obs,'native_proof':ref(n05p),'independent_receipt':ref(nr),'historical_status_not_overwritten':True,'criterion_integrally_accepted':False})
 put('N05_Matrice_4_criterii_istorice.json',{'head':H,'task':'T355','canonical':'P01.C03.T0029','rows':links,'criteria_added':0,'criteria_closed':0,'supersedes_historical_dossier':False,'duplicate_finding_policy':'N05 is stronger native evidence for the same concurrency/conservation issue, not a new statistical defect.'})
peerA03=priorcheck(R/'A03/A03_peer_N05_v1.json','a9e499e4db9c74d43add7f0401daafbf0e5a03ff6fd5ca7d30015088ca34464d')
finalChecklist=priorcheck(R/'A11/Val03_loturi/Checklist_A11_dupa_R12_Val03_v1.json','3e6aff18819a2d88cd6de04b7ee71dbdd159b80ea7df5652524896306a9dd3ba');manifest(R/'A11/Val03_loturi/SIGILIU_Checklist_A11_R12_Val03_v1.json','80580db4e361757e2034ca8025020f97ce246b22c07944571dd016156c6235a9')
manifest(R/'A05_N05_lot03/MANIFEST_lectura_v2.json','0c59818ffd482277d9179e615281523374b7f6c934006801d056849f83b57c78')
manifest(R/'A05_N05_lot03/MANIFEST_lectura_v3.json','b552489faa6ed8a272b6c42e901f763822547636140814fe0ba6535893550220')
put('N05_checkpoint_separat.json',{'head':H,'domain_peer_A03_read_only':ref(R/'A03/A03_peer_N05_v1.json'),'domain_peer_adds_tests':0,'reading_copy':ref(R/'A05_N05_lot03/Raport_N05_lectura_v3.html'),'checkpoint':n05doc,'scope':n05['scope'],'nominal_coverage_events':ref(O/'Evenimente_N05_17_si_29_lecturi.json') if native_events else [],'phase_counts':native_phase_counts,'case_matrix':ref(O/'Cazuri_N05_7_scenarii.json') if native_events else None,'criterion_matrix':ref(O/'N05_Matrice_4_criterii_istorice.json') if native_events else None,'quantity_language':'Evidența cantitativă WMS arată11 din10; nu s-au numărat piese fizice. nativeQty este M_StorageOnHand, fără certificare Fact_Acct/G1.','remedy_architecture_limit':'Reconstituirea exactă la dezambalare privește componentele recuperabile ale setului. Cutiile consumate și manopera nu se recreează sau inversează automat. Recunoașterea singulară în G1 are un contract și teste separate.','no_implicit_file_or_contract_credit':True,'all17_contracts_open':True})
put('Constatari_prioritare_Val03.json',{'head':H,'first_priority':{'id':'A05.R11.G2.BOM.1','alias':'N05','new_unique_defect_increment':0,'task':'P01.C03.T0029','evidence':ref(O/'N05_checkpoint_separat.json'),'classification':'P1 propus integritatea evidenței cantitative WMS; fără impact contabil G1 demonstrat','remediation_contract':ref(R/'A11/Val03_loturi/Checklist_A11_dupa_R12_Val03_v1.json','/items/1')},'other_findings_and_limits':ref(O/'Constatari_loturi_Val03.json'),'qualification_precedence':ref(R/'A11/Val03_loturi/Checklist_A11_dupa_R12_Val03_v1.json'),'no_prior_findings_closed':True,'score':None})
all_new_events=events+native_events
full_delta=[{'path':a['path'],'git_oid':a['git_oid'],'before_axis':a['axis'],'after_axis':b['axis'],'new_evidence':b['current_evidence'][len(a['current_evidence']):]} for a,b in zip(prior,updated) if a!=b]
assert len(full_delta)==57 if native_events else len(full_delta)==11
put('Delta_integrala_Val03.json',{'head':H,'previous':ref(P/'Registru_6728_R12_Val02.jsonl.gz'),'rows':full_delta,'changed_rows':len(full_delta),'unchanged_identity_and_routing':True,'no_new_paths':True})
raw=('\n'.join(json.dumps(x,ensure_ascii=False,separators=(',',':')) for x in updated)+'\n').encode();MEM['Registru_6728_R12_Val03.jsonl.gz']=gzip.compress(raw,mtime=0)
fields=['id','path','git_oid','git_mode','owner','planned_peer','control','pipeline_candidates','task_candidates','R11_reference_only']
assert all(all(a[k]==b[k] for k in fields) for a,b in zip(prior,updated));assert sum(x['axis']['component_exercised']!='UNVERIFIED_R12' for x in updated)==22+len(native_events)
assert sum(bool(x['R11_reference_only']) and x['R11_reference_only']['axes']['exercised']!='UNVERIFIED' for x in updated)==116
assert all(x['file_verdict'] is None for x in updated)
old_index=load(P/'Index_invers_13_fisiere.json')['rows'];idx=old_index+[{**{k:e[k] for k in ['path','event_id','git_oid','owner']},'peer':e['planned_peer'],'control':e['control'],'pipelines':e['pipeline_candidates'],'tasks':e['task_candidates_preserved'],'method_kind':e['method_kind'],'event_source':ref(O/('Evenimente_9_surse_si_2_lecturi.json' if e in events else 'Evenimente_N05_17_si_29_lecturi.json'),f'/rows/{events.index(e) if e in events else native_events.index(e)}')} for e in all_new_events]
assert len(idx)==22+len(native_events)==len({(x['path'],x['event_id']) for x in idx});assert len({x['path'] for x in idx})==len(idx)
put('Index_invers_surse_Val03.json',{'head':H,'rows':idx,'key':['path','event_id'],'static_sources_not_in_execution_count':static+native_reads,'forward_inverse_pairs_equal':True})
for x in idx:
 d=D[x['path']];assert [x['owner'],x['peer'],x['control'],x['pipelines'],x['tasks']]==[d['owner'],d['planned_peer'],d['control'],d['pipeline_candidates'],d['task_candidates']]
historic=load(P/'Conservare_652_fise_2619_criterii.json')
for x in historic['all_dossiers_rehashed']:assert sha(read(B/x['dossier']['path']))==x['dossier']['sha256'];CHECKS.append(x['dossier'])
assert len(historic['all_dossiers_rehashed'])==652 and sum(x['criteria_count_as_historic'] for x in historic['all_dossiers_rehashed'])==2619
put('Conservare_652_fise_2619_criterii.json',historic)
pop=load(E/'delta/2026-11-03T00-39-34-490Z/00_STATUS_TASKURI.json');bytask={x['id']:(i,x) for i,x in enumerate(pop) if x.get('proiect')=='P01'}
taskrows=[]
for alias in ['T232','T240','T343','T355']:
 i,t=bytask[alias];taskrows.append({'alias':alias,'original_row':ref(E/'delta/2026-11-03T00-39-34-490Z/00_STATUS_TASKURI.json',f'/{i}'),'current_state':t.get('stare'),'progress_declared':t.get('procent'),'observations_are_not_accepted_execution':True,'exact_closing_date_not_inferred':True,'current_events':[x['event_id'] for x in all_new_events if x.get('task_alias')==alias],'whole_task_closed_by_wave':False})
put('Matrice_taskuri_criterii_R12_Val03.json',{'head':H,'previous':ref(P/'Matrice_taskuri_criterii_R12_Val02.json'),'historic_tasks':652,'historic_criteria':2619,'historic_criteria_newly_accepted':0,'current_rows':taskrows,'G3_mapping':'SHARED_NO_TASK_ASSIGNED_PENDING_NOMINAL_MAPPING','Masini_mapping':'SHARED_NO_TASK_ASSIGNED','N05':ref(O/'N05_checkpoint_separat.json'),'CO_IP':'CO|CO|CO remains the frozen oracle until nominal authoritative amendment is received; no automatic PASS or FAIL for IP.','population':ref(O/'Supliment_populatie_0039.json'),'all17_contracts_open':True})
put('Ipoteza_G3_dubla_scadere_NEEXECUTATA.json',{'audit_id':'VAL03-HYP-G3-DOUBLE','status':'IPOTEZA_DE_AUDIT_NEEXECUTATA','commercial_task':None,'source':ref(G/'sources/FisaCanalProces.java'),'git_oid':'ff0cc2f8a95fc6f1e74f1ce94611759f4625f58e','anchors':[{'line':344,'text':'BigDecimal cerere = s.cerereSet(produs, SetLista.FiltruCerere.NELIVRATE_FARA_COMANDA);'},{'line':375,'text':'+ " AND l.m_inout_id IS NULL AND coalesce(c.eva_starevalidare,\'\')<>? AND " + SetLista.produsLinieSite("?"),'}],'observation':'Rezervările native și liniile site nelivrate sunt însumate separat; pe calea simplă nu este vizibil aici un filtru fără comandă emisă, spre deosebire de filtrul cererii de set. Alte dependențe sau tranziții pot modifica situația; nu s-a executat acest caz.','proposed_native_fixture':{'actor':'Gestionar/vânzări autorizat, tenant și canal sintetice','precondition':'Stoc10, aceeași cerere site de2 legată de C_Order real cu rezervare nativă2, fără livrare; documentele create pe calea nativă normală','oracle':'Aceeași obligație economică se scade o singură dată:8 dacă niciun alt termen nu intervine;6 ar fi doar un semnal de investigat prin proveniența fiecărui termen','positive':'Cerere site încă fără C_Order:2 scăzute o singură dată','counterexample':'A doua cerere independentă de2 trebuie să ducă6; evitați eliminarea greșită a unei obligații distincte','observations':'Înainte/după/retry, C_Order/linie, rezervare, legătura site, codul nativ apelant și afișarea canalului; păstrează starea și identitatea fiecărei surse','postcondition':'Restituire fixture/clonă; niciun apel partener sau date de producție'},'separate_from':['R12-STOC-SO-PO-01','T343 CO/IP authority conflict'],'new_execution_credit':0,'finding_confirmed':False,'priority':None})
hyp=load(O/'Ipoteza_G3_dubla_scadere_NEEXECUTATA.json')
for anchor in hyp['anchors']:assert read(G/'sources/FisaCanalProces.java').decode('utf8').splitlines()[anchor['line']-1].strip()==anchor['text']
put('Ipoteza_G3_promo_NEEXECUTATA.json',{'audit_id':'VAL03-HYP-G3-PROMO','status':'IPOTEZA_DE_AUDIT_NEEXECUTATA','source':ref(G/'sources/FisaCanalCalcul.java'),'git_oid':'daea2da32194a453bc4b314787a2af7f0f801b52','source_range':'corpSheet; lines410–417','observation':'Cu discount pozitiv payloadul include regular_price_ron și on_sale=true; la discount0 se trimite numai price_ron în această ramură. Omisiunea poate fi legitimă dacă receptorul resetează câmpurile.','proposed_test':{'actor':'Responsabil de canal autorizat într-un canal sintetic','entry':'Fișa canalului → corpSheet → API receptor → starea salvată și pagina site','fixture':'Preț100, discount10% apoi0; reia aceeași publicare și compară înainte/după/retry','oracle':'După0, preț100 și fără promoție activă dacă acesta este contractul receptorului; verifică explicit resetarea on_sale/regular_price, nu deduce din absența cheilor','counterexample':'Un alt canal cu promoție10% trebuie păstrat; revenirea canalului inițial la10% este un caz pozitiv separat','missing_condition':'Contractul de patch/reset al receptorului și calea nativă reală nu au fost încă probate'},'finding_confirmed':False,'new_execution_credit':0,'priority':None,'other_open_axes':['limbă','import atribute']})
resources={'A12':{'product_tests':0,'services_created':0,'DB_created':0,'operational_writes':0},'retained_after_auto_review':{'count':6,'reason':'blocked by policy','roots':['D:/CodexWork/p01-r12-masini-dates','D:/CodexWork/a11-r12-mutator-20261103','D:/CodexWork/a11-r12-mutator-20261103-v2','D:/CodexWork/p01-r12-t343-tools-l03','D:/CodexWork/p01-r12-t343-tools-l03-v2','D:/CodexWork/a10-r12-l03'],'sources':[ref(P/'Resurse_si_restituire.json'),ref(A6/'Cleanup.json'),ref(R/'A11/Val03_loturi/Cleanup_mutator_independent_v1.json'),ref(A10/'Cleanup_laborator.json')],'no_workaround_used':True},'N05':n05.get('resources'),'all_laboratory_resources_returned':False}
put('Resurse_si_restituire_Val03.json',resources)
counts={'technical_identities':6728,'prior_partial_sources':13,'new_bounded_execution_or_comparator_sources':9+len(native_events),'current_bounded_execution_or_comparator_sources':22+len(native_events),'new_static_only_sources':2+len(native_reads),'native_business_method_paths_including_transitive':11,'native_type_record_uses_not_methods':2,'native_fixture_binding_sources':3,'native_binding_metadata_sources':1,'native_scenarios':7,'new_audit_tools_total':19,'tools_with_partial_component_or_comparator_evidence':19,'tools_with_whole_file_acceptance':0,'new_tool_original_component_sources':2,'new_tool_shell_comparator_sources':5,'new_application_SQL_sites':2,'distinct_SQL_texts':1,'application_parser_from_Val02':1,'historic_R11_reference_only':116,'historic_transferred_credit':0,'historic_tasks':652,'historic_criteria':2619,'historic_criteria_newly_accepted':0,'full_files_accepted':0,'full_tasks_closed':0,'business_contracts_closed':0,'business_contracts_open':17,'new_cases_helpers_A06':36,'new_cases_helpers_A10':73,'new_G3_unique_fixtures':12,'new_G3_SQL_evaluations':24,'independent_A11_cases_not_added_to_executor':True,'real_UI_ZK_scenarios_in_helper_G3_lots':0,'native_N05_scope_separate':True}
put('Reconciliere_metrici_si_limite.json',{'head':H,'counts':counts,'previous_counts':ref(P/'Reconciliere_metrici_si_limite.json'),'A06':v6['counts'],'G3':load(G/'Raport_rezervari_SQL.json')['counts'],'A10':{'original_pure_components':28,'original_JS_synthetic_DOM':18,'shell_comparator_cases':27,'unique_case_identities':73,'independent_receipt':r10},'N05':ref(O/'N05_checkpoint_separat.json'),'not_global_pass_sum':True,'limits':['All19 new audit tools now have bounded observations; all19 still need complete-file acceptance.','Two SQL sites share one text; no Java, PostgreSQL, UI or business persistence demonstrated by that comparator.','Original component is not original full CLI or normal environment.','Claims from server1687 or other branches do not transfer to df85.']})
zones=[]
for z in [f'A{i:02}' for i in range(1,11)]:
 zr=[x for x in updated if x['owner']==z];zones.append({'owner':z,'assigned_files':len(zr),'current_partial_sources':sum(x['axis']['component_exercised']!='UNVERIFIED_R12' for x in zr),'new_events':[x['event_id'] for x in all_new_events if x['owner']==z],'actual_executors_new':dict(collections.Counter(x['actual_executor'] for x in all_new_events if x['owner']==z)),'full_acceptance':0,'peer_review_not_inferred_from_assignment':True,'N05_separate':ref(O/'N05_checkpoint_separat.json') if z=='A05' else None,'next_action':{'A01':'Verificare normală tenancy/RBAC și gărzile reale; comparatorii I01/I10 nu certifică instalarea.','A02':'Reconciliere metadate/schema în clonă și însușirea exactă SO/PO/ASI.','A03':'DocAction/Fact_Acct, cutii/manoperă o singură dată G1, retry/reversare și scheme.','A04':'Achiziție/import/recepție nativă cu efecte și refuzuri; fără noi probe în acest val.','A05':'N05 conform checkpointului separat; conservare CPP/CPA/G1/G2 și concurență nativă.','A06':'Rezervări native SO/PO și flux canal→comandă; rezolvarea autorității CO/IP.','A07':'Pick/aviz/AWB/factură/retur în flux nativ complet; fără noi probe în acest val.','A08':'Ajutor și raportare prin interfața reală cu rol; DOM sintetic nu este ZK autentificat.','A09':'Mașini parse/save/commit și cele șapte termene prin ambele editoare; menținere scope fără task atribuit.','A10':'Rulare originală în mediul aprobat, propagare erori și restituire; menținere refuz cleanup fără ocolire.'}[z]})
planpath=E/'R12_plan_delta/Plan_delta_R12_v2.json';plan=load(planpath);assert len(plan['remaining_contracts'])==17
put('Checklist_10_zone_Val03.json',{'head':H,'rows':zones,'prior_checklist':ref(R/'A11/Val02_registru/Checklist_A11_dupa_R12_Val02_v1.json'),'current_independent_checklist':ref(R/'A11/Val03_loturi/Checklist_A11_dupa_R12_Val03_v1.json'),'hypotheses_not_findings':[ref(O/'Ipoteza_G3_dubla_scadere_NEEXECUTATA.json'),ref(O/'Ipoteza_G3_promo_NEEXECUTATA.json')],'contracts':[{'id':c['id'],'objective':c['objective'],'owner':c['owner'],'peer':c['peer'],'normative_contract':ref(planpath,f'/remaining_contracts/{i}'),'status':'OPEN','no_closure_credit':True} for i,c in enumerate(plan['remaining_contracts'])],'gate_reception_separate':True,'score':None})
sources=put('Surse_si_receptii_Val03.json',{'head':H,'inputs':INPUTS,'artifact_instances_rehashed':len(CHECKS),'A11_is_independent_not_planned_peer_substitute':True,'scope':'Producer pending labels preserved; later independent receipts attached separately.'})
handoff=put('Handoff_R12_Val03.json',{'schema':'eva.audit.r12.a12.wave/3','utc':datetime.now(timezone.utc).isoformat(),'head':H,'server_HEAD_not_candidate':'1687cc8376902e7aa7163a883e07c7271bcae511','mode':'ADDITIVE_FROM_VAL02_NO_PRODUCT_EXECUTION_BY_A12','previous_manifest':ref(P/'MANIFEST_R12_Val02.json'),'previous_independent_receipt':ref(R/'A11/Val02_registru/Verdict_A11_R12_Val02_registru_v1.json'),'preflight_manifest':ref(O/'MANIFEST_preflight_Val03_0039.json'),'preflight_receipt':ref(R/'A11/Val03_preflight/Verdict_A11_receptie_supliment_0039_v1.json'),'counts':counts,'register':ref(O/'Registru_6728_R12_Val03.jsonl.gz'),'events':events_ref,'native_events':ref(O/'Evenimente_N05_17_si_29_lecturi.json'),'delta':ref(O/'Delta_integrala_Val03.json'),'cases':case_ref,'matrix':ref(O/'Matrice_taskuri_criterii_R12_Val03.json'),'inverse':ref(O/'Index_invers_surse_Val03.json'),'N05':ref(O/'N05_checkpoint_separat.json'),'resources':ref(O/'Resurse_si_restituire_Val03.json'),'sources':sources,'checklist':ref(O/'Checklist_10_zone_Val03.json'),'A11_registry_reception_pending':True,'scores':{'execution_quality':None,'product':None},'all17_contracts_open':True})
tr=''.join('<tr><td>'+html.escape(e.get('audit_control') or 'G3 · fără task atribuit')+'</td><td>'+html.escape(e['path'])+'</td><td>'+html.escape(e['method_kind'])+'</td><td>'+html.escape(e['actual_executor'])+'</td></tr>' for e in events)
page='''<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>R12 Val03 — registru de audit</title><style>body{font:16px/1.5 system-ui;max-width:1160px;margin:30px auto;padding:0 16px;background:#f6f8fb;color:#183041}p,td,code,a{overflow-wrap:anywhere}.table{overflow-x:auto}table{border-collapse:collapse;width:100%;background:white}th,td{padding:10px;border-bottom:1px solid #ddd;vertical-align:top;text-align:left}.note{background:#e7f1f5;border-left:4px solid #35748b;padding:12px}</style><h1>R12 · Val03 — WMS nativ, rezervări și instrumente</h1>'''
page+='<p>Revizie fixată <code>'+H+'</code>. HEAD-ul local al serverului, <code>1687cc8…</code>, este distinct și nu primește acoperire. Compararea populației cu ultima captură recepționată păstrează 996 înregistrări, 693 P01 și cohorta istorică de 652 fișe / 2.619 criterii.</p><p class="note"><strong>39 surse cu observații parțiale:</strong> 13 din Val02, șapte instrumente, două situri SQL și 17 surse N05 cu niveluri distincte. N05 cuprinde 11 trasee de metode business (inclusiv tranzitive), două utilizări de record/enum, trei surse numai fixture/binding și una de metadate. Alte 31 surse sunt numai suport citit. Nu sunt 39 fișiere validate integral. Cele 116 surse R11 rămân istoric fără transfer. Toate cele 17 contracte business rămân deschise.</p><h2>Prioritate: conservarea stocului WMS</h2><p><strong>N05 / P01.C03.T0029:</strong> recepția A11 confirmă că modificarea concurentă a rețetei BOM de la două la trei componente, în timp ce ambalarea este necomisă, face ca evidența cantitativă WMS să arate 11 piese din 10. Nu s-au numărat piese fizice. M_StorageOnHand rămâne10; nu este demonstrată creșterea soldului contabil G1. Este aceeași constatare N05, întărită prin integrare nativă, nu un defect nou statistic.</p><p>Serialul folosește ProceseEcran original cu tranzacție administrată nativ. Concurența și rollbackul folosesc același proces original cu managedTrx=false și commit coordonat extern; fără sesiuni ZK concurente. La rollback dispar efectele WMS, dar poate persista AD_PInstance/result1; retry are exact două mișcări. Contextul rolului este injectat nativ, fără login frontend. Se propune coordonarea procesului și handlerului existent asupra aceleiași versiuni BOM, cu blocare/revalidare până la commit sau rollback, apoi regresii pe mai multe gestiuni. Dezambalarea reface componentele recuperabile; cutiile consumate și manopera nu se recreează și nu se inversează automat. <a href="../../A05_N05_lot03/Raport_N05_lectura_v3.html">Raportul explicativ N05, cu schemă</a> · <a href="N05_checkpoint_separat.json">Dovezi și recepție</a>.</p><h2>Instrumente și comparator SQL</h2><p>A06: 18 cazuri pe Python original și 18 cazuri pe două comparatoare shell. A10: 28 cazuri pe componente originale, 18 pe DOM sintetic și 27 pe comparatoare shell. G3: 12 fixtures evaluate în două situri cu același SQL. Numerele descriu metode diferite, nu un total de teste de produs trecute. Martorii A11 sunt contabilizați separat.</p><div class="table"><table><thead><tr><th>Control</th><th>Sursă</th><th>Metodă</th><th>Executor</th></tr></thead><tbody>'+tr+'</tbody></table></div><h2>Concluzii și limite</h2><p>Instrumentele existente au nevoie de ținte de mutație neambigue, proveniență și numitori expliciți, separarea erorilor de infrastructură de detecția semantică și propagarea statusurilor. Recepțiile A11 limitează fiecare constatare; prioritățile privind integritatea dovezilor nu sunt incidente ERP demonstrate.</p><p>SQL-ul rezervărilor adună și cantități PO în suma scăzută din disponibil. Se propune adaptarea la semantica nativă SO/PO, păstrând firma, produsul, gestiunea, ASI și politica IsActive. Nu s-au executat Java sau UI în acel lot. La fizic10, SO2 și PO15, formula RezervareStoc ar deriva −7, iar FisaCanalCalcul plafonează la0; sunt derivate, nu valori capturate din aplicație.</p><p>Cele șapte scenarii N05 sunt separate de cazurile instrumentelor și SQL. Laboratorul N05 a fost restituit, cu cache/harness pasive păstrate. Nu se deduce validarea întregului flux WMS, DocAction, contabilitate ori ZK. Conflictul de autoritate T343 CO/IP rămâne deschis.</p><h2>Resurse și continuare</h2><p>Șase directoare scratch au rămas după respingerea automată a ștergerii cu motivul «blocked by policy». Nu s-a încercat ocolirea. Situația N05 este separată; nu se declară restituirea integrală a tuturor resurselor.</p><p><a href="Handoff_R12_Val03.json">Predare și hashuri</a> · <a href="Constatari_prioritare_Val03.json">Constatări și recepții</a> · <a href="Cazuri_nominale_121.json">Cazuri nominale</a> · <a href="Checklist_10_zone_Val03.json">Checklist pe zece zone</a> · <a href="N05_checkpoint_separat.json">N05 separat</a> · <a href="Resurse_si_restituire_Val03.json">Resurse</a></p></html>'
MEM['index.html']=page.encode()
seen={};issues=[]
def scan(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and x['path'].startswith('executie/') and 'sha256' in x:
   key=(x['path'],x['sha256'],x.get('pointer'))
   if key not in seen:
    try:
     p=B/x['path'];assert sha(read(p))==x['sha256']
     if x.get('pointer') is not None:point(load(p),x['pointer'])
     seen[key]=True
    except Exception as e:issues.append({'ref':x,'error':str(e)})
  for y in x.values():scan(y)
 elif isinstance(x,list):
  for y in x:scan(y)
for n,b in list(MEM.items()):
 if n.endswith('.json'):scan(json.loads(b))
for x in updated:scan(x)
assert not issues,issues[:10]
qa=put('QA_R12_Val03.json',{'utc':datetime.now(timezone.utc).isoformat(),'head':H,'handoff':handoff,'counts':counts,'local_references_and_pointers':len(seen),'artifact_instances_rehashed':len(CHECKS),'all6728_identity_fields_preserved':True,'new_OID_SHA_verified_sources':57,'source_levels_preserved':{'native11business_method_paths':11,'native2record_types':2,'native3fixture_binding':3,'native1metadata':1},'all652_historical_dossiers_rehashed':True,'criteria_count':2619,'forward_inverse_pair_count':len(idx),'five_routing_dimensions_equal':True,'all_original_seals_unchanged':True,'issues':issues,'score':None})
MEM['build_val03.py']=pathlib.Path(__file__).read_bytes();MEM['build_val03_configuration.json']=read(pathlib.Path(sys.argv[1]))
manifest_data={'schema':'eva.audit.r12.a12.wave3.manifest','utc':datetime.now(timezone.utc).isoformat(),'head':H,'files':[ref(O/n) for n in sorted(MEM)],'inputs':INPUTS,'preflight_immutable':ref(O/'MANIFEST_preflight_Val03_0039.json'),'independent_registry_reception_pending':True,'no_self_reference':True}
put('MANIFEST_R12_Val03.json',manifest_data)
if '--publish' in sys.argv:
 assert cfg.get('publication_allowed') is True, 'N05 independent receipt or approved checkpoint is required before publishing'
 for n,b in MEM.items():assert not (O/n).exists(),n
 for n,b in MEM.items():(O/n).write_bytes(b)
 for x in manifest_data['files']:assert sha((B/x['path']).read_bytes())==x['sha256']
 print(json.dumps({'manifest':ref(O/'MANIFEST_R12_Val03.json'),'handoff':handoff,'QA':qa,'counts':counts},ensure_ascii=False))
else:print(json.dumps({'status':'PREPARED_IN_MEMORY_ONLY','files':len(MEM),'counts':counts,'references':len(seen),'issues':issues},ensure_ascii=False))
