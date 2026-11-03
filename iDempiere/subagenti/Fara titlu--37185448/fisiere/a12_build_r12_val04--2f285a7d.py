import collections,copy,gzip,hashlib,html,json,pathlib,sys
from html.parser import HTMLParser
from datetime import datetime,timezone
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');R=B/'executie/R12_fisiere';O=R/'A12/Val_04';P=R/'A12/Val_03';I=O/'Increment_01_frontend';H='df85d33c1648ce2b2df130a60a05ef696e2e5480'
MEM={};INPUTS=[];CHECKS=[];HC={};JC={}
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return MEM[p.name] if p.parent==O and p.name in MEM else p.read_bytes()
def load(p):
 if p not in JC:JC[p]=json.loads(read(p).decode('utf-8-sig'))
 return JC[p]
def ref(p,pointer=None):
 b=read(p);d={'path':p.relative_to(B).as_posix(),'sha256':sha(b),'bytes':len(b)}
 if pointer is not None:d['pointer']=pointer
 return d
def put(n,x):
 assert n not in MEM and not (O/n).exists(),n
 MEM[n]=(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8');return ref(O/n)
def refs(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str) and len(x['sha256'])==64:yield x
  for v in x.values():yield from refs(v)
 elif isinstance(x,list):
  for v in x:yield from refs(v)
def point(d,p):
 for k in p.removeprefix('#').lstrip('/').split('/') if p not in ('','#') else []:
  k=k.replace('~1','/').replace('~0','~');d=d[int(k)] if isinstance(d,list) else d[k]
 return d
def resolve(origin,s):
 q=pathlib.Path(s)
 if q.is_absolute():return q
 if s.startswith('executie/'):return B/q
 if s.startswith('idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/'):
  return R/'A05_G3_nativ_lot04/surse_df85'/s.split('src/com/eva/ro/contab/',1)[1]
 direct=origin.parent/q
 if direct.exists() or direct.parent==O and direct.name in MEM:return direct
 matches=[root/q for root in (origin.parent.parent,origin.parent.parent.parent,R,B) if (root/q).exists()]
 assert len(set(matches))==1,('Referință ambiguă/lipsă',origin,s,matches)
 return matches[0]
def validate_ref(rr,origin):
 p=resolve(origin,rr['path'])
 if p not in HC:HC[p]=ref(p)
 assert HC[p]['sha256']==rr['sha256'],(p,HC[p]['sha256'],rr['sha256'])
 if 'bytes' in rr:assert HC[p]['bytes']==rr['bytes'],p
 if rr.get('pointer') is not None:point(load(p),rr['pointer'])
 CHECKS.append(rr);return p
def verify(p,expected=None):
 r=ref(p)
 if expected:assert r['sha256']==expected,p
 for rr in refs(load(p)):validate_ref(rr,p)
 INPUTS.append(r);return load(p)
cfg=load(pathlib.Path(sys.argv[1]))
assert cfg['head']==H and cfg['native_receipt_complete'], 'Nu se sigilează înaintea raportului nativ și a recepției independente.'
verify(P/'MANIFEST_R12_Val03.json','5f80d3973e34be94ce12aafdea307eec43aca359b42f2a0042c740e6c9db9a23')
verify(P/'MANIFEST_lectura_finala_Val03_v1.json','1b40caa6b7587badc3e304467ad0a4386c5a3f725f4c4b9c3f0efd107b530dfe')
verify(P/'Handoff_R12_Val03_v2.json','58c7de3c525c69af3dd41799eed8e485f682e577233ea47f9acef3d7bda15dbb')
verify(R/'A11/Val03_registru/Sigiliu_A11_R12_Val03_registru_v1.json','81595e4ecb34ca09e664d2fcf57f4d57e6e2e787e6ea2a6685b145cc153f5c61')
verify(O/'MANIFEST_preflight_Val04_0143.json','80d766c3c38cbcb925c4c9cc38cc660b12252da2f4bec15af42c5895d6c9199f')
verify(R/'A11/Val04_preflight/Verdict_A11_receptie_preflight_A12_0143_v1.json','dedbc15a0d3b58fc0ede5f9b277a3823cd1d472a9ac732109e7a05d0cd442a2d')
verify(I/'MANIFEST_increment_frontend.json','b158dcdf8ad6ff4b3d69db75c6567965dada28a2257b1ad993be623a779e1b81')
for rr in cfg['inputs']:verify(B/rr['path'],rr['sha256'])
prior=[json.loads(l) for l in gzip.decompress(read(P/'Registru_6728_R12_Val03.jsonl.gz')).decode('utf-8').splitlines()]
D={r['path']:r for r in prior};assert len(D)==len(prior)==6728
updated=copy.deepcopy(prior);U={r['path']:r for r in updated}
front=load(I/'Evenimente_frontend_2_cai_un_blob.json');frontstatic=load(I/'Lecturi_statice_9_asocieri_8_cai.json')
native=load(B/cfg['native_curated']['path']);assert sha(read(B/cfg['native_curated']['path']))==cfg['native_curated']['sha256']
assert native['head']==H and native['independent_receipt'] and native['full_file_or_contract_acceptances']==0
new_events=copy.deepcopy(front['rows'])+copy.deepcopy(native['runtime_events'])
new_static=copy.deepcopy(frontstatic['rows'])+copy.deepcopy(native['static_only_rows'])
assert len({(e['path'],e['event_id']) for e in new_events})==len(new_events)
for e in new_events+new_static:
 d=D[e['path']];assert e['git_oid']==d['git_oid'] and e['owner']==d['owner'] and e['planned_peer']==d['planned_peer']
 assert e['source']['sha256']==e['sha256'];p=B/e['source']['path'];b=read(p)
 assert sha(b)==e['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_oid']
 assert not e.get('whole_file_accepted',False)
eventsref=put('Evenimente_Val04.json',{'head':H,'rows':new_events,'grouping_rule':'Perechea (cale,event_id) identifică o asociere; execuțiile se numără separat după grupul de probă și caz. Două căi ale aceluiași blob JS nu dublează cazurile.','frontend_cases':ref(I/'Cazuri_frontend_10.json'),'native_case_source':native['cases'],'score':None})
staticref=put('Lecturi_statice_Val04.json',{'head':H,'rows':new_static,'associations':len(new_static),'distinct_paths':len({r['path'] for r in new_static}),'runtime_credit':0,'backend_overflow_hypothesis':frontstatic['hypothesis'],'limits':'Lectura sursei sau a clasei montate nu înseamnă apel de metodă, UI, DocAction ori acceptare integrală.'})
for i,e in enumerate(new_events):
 u=U[e['path']]
 u.setdefault('axis_history',[]).append({'wave':'Val03','before_Val04':copy.deepcopy(u['axis']),'prior_register':ref(P/'Registru_6728_R12_Val03.jsonl.gz')})
 u['axis']['read']='OBSERVED_AT_LINKED_SCOPE' if e['actual_executor']=='A08' else 'OBSERVED_AT_LINKED_NATIVE_SCOPE'
 if e['actual_executor']=='A08':u['axis']['component_exercised']='ORIGINAL_JS_SYNTHETIC_DOM_PARTIAL'
 else:
  for k,v in e['accepted_axis_updates'].items():
   assert k in u['axis'] and k!='whole_file_acceptance',k
   if k=='component_exercised' and u['axis'][k]=='NATIVE_BUSINESS_METHOD_PARTIAL' and v=='NATIVE_TRANSITIVE_METHOD_PARTIAL':
    continue  # Dovada cumulativă anterioară rămâne; noul traseu limitat este explicit în eveniment.
   u['axis'][k]=v
 u['current_evidence'].append({'event_id':e['event_id'],'source':ref(O/'Evenimente_Val04.json','/rows/'+str(i)),'method_kind':e['method_kind'],'scope':'PARTIAL_ONLY','independent_reception':e['independent_receipt'],'execution_group':e['execution_group']})
 u['peer_receipts']['independent_A11']=e['independent_receipt'];u['executor_for_current_event']=e['actual_executor'];u['planned_peer_performed_not_inferred']=True
for i,s in enumerate(new_static):
 u=U[s['path']]
 if u['axis']['read'] in ('NO_NEW_CREDIT_IN_THIS_WAVE','UNVERIFIED_R12'):u['axis']['read']='BOUNDED_STATIC_SUPPORT_ONLY'
 u['current_evidence'].append({'source':ref(O/'Lecturi_statice_Val04.json','/rows/'+str(i)),'scope':'STATIC_ONLY_NO_EXECUTION','independent_reception':s['independent_receipt']})
identity_keys=['id','path','git_oid','git_mode','candidate','owner','planned_peer','control','pipeline_candidates','task_candidates']
for row in updated:
 old=D[row['path']]
 for k in identity_keys:assert row[k]==old[k],(row['path'],k)
 assert row['R11_reference_only']==old['R11_reference_only'] and row['file_verdict'] is None and row['axis']['whole_file_acceptance'] is None
 assert row['current_evidence'][:len(old['current_evidence'])]==old['current_evidence']
 if row['R11_reference_only'] is not None:assert not row['R11_reference_only']['credit_transferred']
raw=('\n'.join(json.dumps(x,ensure_ascii=False,separators=(',',':')) for x in updated)+'\n').encode('utf-8')
assert not (O/'Registru_6728_R12_Val04.jsonl.gz').exists();MEM['Registru_6728_R12_Val04.jsonl.gz']=gzip.compress(raw,mtime=0)
delta=[{'path':r['path'],'git_oid':r['git_oid'],'owner':r['owner'],'peer':r['planned_peer'],'before_axis':D[r['path']]['axis'],'after_axis':r['axis'],'new_evidence':r['current_evidence'][len(D[r['path']]['current_evidence']):]} for r in updated if r!=D[r['path']]]
delta_ref=put('Delta_integrala_Val04.json',{'head':H,'prior_register':ref(P/'Registru_6728_R12_Val03.jsonl.gz'),'current_register':ref(O/'Registru_6728_R12_Val04.jsonl.gz'),'changed_rows':len(delta),'new_identities':0,'rows':delta,'no_previous_evidence_removed':True})
oldindex=load(P/'Index_invers_surse_Val03.json');idx=copy.deepcopy(oldindex['rows'])
for i,e in enumerate(new_events):idx.append({'path':e['path'],'event_id':e['event_id'],'git_oid':e['git_oid'],'owner':e['owner'],'peer':e['planned_peer'],'control':e['control'],'pipelines':e['pipeline_candidates'],'tasks':e['task_candidates_preserved'],'method_kind':e['method_kind'],'execution_group':e['execution_group'],'event_source':ref(O/'Evenimente_Val04.json','/rows/'+str(i))})
forward={(r['path'],e['event_id']) for r in updated for e in r['current_evidence'] if 'event_id' in e};inverse={(r['path'],r['event_id']) for r in idx}
legacy=[]
for row in idx:
 pair=(row['path'],row['event_id'])
 if pair in forward:continue
 assert row['event_id'] in ('R12V01-R12-I18','R12V01-R12-I19')
 rr=row['event_source'];q=validate_ref(rr,P/'Index_invers_surse_Val03.json');event=point(load(q),rr['pointer'])
 assert event['path']==row['path'] and event['event_id']==row['event_id'] and event['git_oid']==row['git_oid']
 evproof=event['evidence'];matches=[j for j,e in enumerate(U[row['path']]['current_evidence']) if all(e.get(k)==evproof.get(k) for k in ('path','sha256','pointer'))]
 assert len(matches)==1
 legacy.append({'path':row['path'],'event_id':row['event_id'],'event_source':rr,'existing_forward_evidence_index':matches[0],'existing_forward_proof':evproof,'method':'Val01 păstra direct pointerul raportului în current_evidence, fără event_id. Identificatorul se rezolvă din evenimentul original cu egalitate exactă a căii/OID/pointerului/sha. Fără execuție sau credit nou.'})
 forward.add(pair)
assert len(idx)==len(inverse) and forward==inverse
allstatic=copy.deepcopy(oldindex['static_sources_not_in_execution_count'])+new_static
invref=put('Index_invers_surse_Val04.json',{'head':H,'rows':idx,'key':['path','event_id'],'forward_inverse_pairs_equal':True,'legacy_Val01_pointer_resolution':legacy,'static_observations':allstatic,'static_observation_paths':len({r['path'] for r in allstatic}),'note':'Un fișier poate păstra o probă SQL comparator și primi o probă Java nativă distinctă; identitatea de sursă se numără o dată, evenimentele și metodele separat.'})
historic=copy.deepcopy(load(P/'Conservare_652_fise_2619_criterii.json'))
for r in historic['all_dossiers_rehashed']:validate_ref(r['dossier'],P/'Conservare_652_fise_2619_criterii.json')
assert len(historic['all_dossiers_rehashed'])==652 and sum(r['criteria_count_as_historic'] for r in historic['all_dossiers_rehashed'])==2619
historic['previous_immutable_copy']=ref(P/'Conservare_652_fise_2619_criterii.json');historic['rechecked_utc']=now();historic['current_new_credit']=0
put('Conservare_652_fise_2619_criterii_Val04.json',historic)
snapshot=B/'executie/delta/2026-11-03T01-43-37-057Z/00_STATUS_TASKURI.json';tasks=load(snapshot);lookup={r['id']:(i,r) for i,r in enumerate(tasks) if r.get('proiect')=='P01'}
taskrows=[]
for alias in ['T232','T240','T343','T355','T386']:
 i,r=lookup[alias];assert r.get('stare_generala')
 taskrows.append({'alias':alias,'canonical':r.get('cod_capitol'),'source':ref(snapshot,'/'+str(i)),'current_state':r['stare_generala'],'state_source_field':'stare_generala','progress_declared':r.get('procent'),'new_task_or_criterion_acceptance':0,'exact_closing_date_not_inferred':True,'new_evidence_mapping':'Nicio asociere nominală de criteriu nou demonstrată în loturile frontend/G3 partajate.'})
matrix=put('Matrice_taskuri_criterii_R12_Val04.json',{'head':H,'previous_corrected_matrix':ref(P/'Matrice_taskuri_criterii_R12_Val03_corectata_v1.json'),'historic_tasks':652,'historic_criteria':2619,'historic_criteria_newly_accepted':0,'current_rows':taskrows,'new_task_intake':ref(O/'Fisa_intake_T386_v1.json'),'frontend_mapping':'SHARED_NO_TASK_ASSIGNED_PENDING_NOMINAL_MAPPING','G3_mapping':native['task_mapping'],'prior_N05_matrix_preserved':ref(P/'N05_Matrice_4_criterii_istorice.json'),'CO_IP':'Autoritatea CO/IP rămâne deschisă; actualizarea observațiilor nu amendează automat oracolul înghețat CO|CO|CO.','population':ref(O/'Supliment_populatie_0143.json'),'all17_contracts_open':True})
findings=put('Constatari_calificate_Val04.json',{'head':H,'frontend':ref(I/'Constatari_frontend_calificate.json'),'native':native['findings'],'native_disposition':native['finding_count_policy'],'backend_overflow_static_hypothesis':frontstatic['hypothesis'],'prior_N05_preserved':ref(P/'N05_checkpoint_separat.json'),'new_full_file_task_contract_acceptances':0,'score':None})
put('G3_checkpoint_nativ_Val04.json',native)
previous_checklist=load(P/'Checklist_10_zone_Val03.json');zone_actions={
 'A01':'Exercită drepturile și separarea firmă/canal pe rutele reale; lectura rezervărilor sau un actor public sintetic nu probează RBAC. Pentru T386 cere refuzuri interclient/rol.',
 'A02':'Reutilizează schema și modelele native; păstrează ASI/IsActive/client/locator explicit și reconcilierea registrului principal cu listele derivate pentru T386.',
 'A03':'DocAction, Fact_Acct și soldurile valorice G1 în două scheme rămân de probat. G2 este necontabilă; cutiile/manopera se recunosc o singură dată în G1.',
 'A04':'Continuă importul, achiziția și recepția native cu refuzuri și citire după commit. Acest val nu adaugă execuții A04.',
 'A05':'Folosește numai limitele recepției G3; păstrează distincte fixturele native, metodele de calcul/citire și documentele complete neexecutate. N05 anterior rămâne nereparat.',
 'A06':'Rezolvă filtrarea SO/PO în mecanismul existent, apoi verifică fluxul canal–rezervare–comandă fără dublă scădere. Pentru T386 fixează cele19 reguli declarate și un singur scriitor înaintea execuției.',
 'A07':'Pick, aviz, AWB, factură și retur cer flux nativ complet; nicio recepție de livrare din catalog ori calculul G3.',
 'A08':'Adaptează funcția existentă: catch/finally, response.ok/schema și corelarea ultimei cereri. Reauditează cu oracol afirmativ filtru=cerere=produse, mesaj de eroare și retry. Templatele complete, CSS, debounce și rolurile nu sunt acoperite.',
 'A09':'Probează Mașini parse/save/commit, cele șapte termene și ambele editoare; ZK/scanare necesită actor/rol real. T386 are cross-review de domeniu repartizat, fără recenzie dedusă.',
 'A10':'Păstrează df85 separat de HEAD server8c și de commitul declarat6354. Verifică mediu, bundle și restituire; cele șase directoare cu cleanup respins nu se șterg prin ocolire.'}
zones=[]
for z in previous_checklist['rows']:
 owner=z['owner'];owned=[r for r in updated if r['owner']==owner]
 zones.append({'owner':owner,'assigned_files':len(owned),'new_event_associations':sum(e['owner']==owner for e in new_events),'new_static_associations':sum(e['owner']==owner for e in new_static),'actual_executors_new':dict(collections.Counter(e['actual_executor'] for e in new_events if e['owner']==owner)),'whole_acceptances':0,'next_action':zone_actions[owner],'peer_performed_not_inferred_from_assignment':True})
assert sum(z['assigned_files'] for z in zones)==6728
check=put('Checklist_10_zone_Val04.json',{'head':H,'rows':zones,'previous':ref(P/'Checklist_10_zone_Val03.json'),'A11_inherited':ref(R/'A11/Val03_loturi/Checklist_A11_dupa_R12_Val03_v1.json'),'A11_current':ref(R/'A11/Val04_loturi/Checklist_A11_dupa_R12_Val04_v1.json'),'current_frontend_requirements':ref(R/'A11/Val04_loturi/Verdict_A11_catalog_lot04_v1.json','/required_next_tests'),'native_next':native['next_controls'],'contracts':previous_checklist['contracts'],'protocol_before_next_product_execution':True,'score':None})
levels=collections.Counter(r['axis']['component_exercised'] for r in updated)
bounded=[r for r in updated if r['axis']['component_exercised']!='UNVERIFIED_R12'];priorbounded={r['path'] for r in prior if r['axis']['component_exercised']!='UNVERIFIED_R12'}
groups={}
for r in bounded:
 state=r['axis']['component_exercised']
 group='tip_record' if 'TYPE_USE' in state else 'fixture_binding_metadate' if 'FIXTURE' in state or 'BINDING_METADATA' in state else 'comparator_SQL' if 'SQL_COMPARATOR' in state else 'comparator_shell' if 'SHELL_COMPARATOR' in state else 'componenta_sau_traseu_metoda_originala'
 groups.setdefault(group,[]).append(r['path'])
assert sum(map(len,groups.values()))==len(bounded)
counts={'technical_identities':6728,'historical_tasks':652,'historical_criteria':2619,'current_P01_members':694,'prior_bounded_source_identities':39,'current_bounded_source_identities':len(bounded),'new_bounded_source_identities':len(set(r['path'] for r in bounded)-priorbounded),'new_runtime_event_associations':len(new_events),'new_runtime_path_identities':len({r['path'] for r in new_events}),'cumulative_event_pairs':len(idx),'new_static_associations':len(new_static),'new_static_distinct_paths':len({r['path'] for r in new_static}),'cumulative_static_observation_paths':len({r['path'] for r in allstatic}),'frontend_original_blobs_exercised':1,'frontend_path_identities':2,'frontend_executor_case_identities':10,'frontend_independent_witnesses_separate':5,'native_metrics_separate':native['counts'],'R11_reference_only':116,'R11_credit_transferred':0,'new_full_file_acceptances':0,'new_full_task_acceptances':0,'new_full_criterion_acceptances':0,'contracts_closed':0,'contracts_open':17}
counts['current_static_observation_paths_without_component_evidence']=len({r['path'] for r in allstatic if U[r['path']]['axis']['component_exercised']=='UNVERIFIED_R12'})
counts['new_bounded_evidence_event_associations']=counts.pop('new_runtime_event_associations')
counts['new_bounded_evidence_path_identities']=counts.pop('new_runtime_path_identities')
met=put('Reconciliere_metrici_si_limite_Val04.json',{'head':H,'counts':counts,'current_exclusive_primary_levels':{k:{'count':len(v),'paths':v} for k,v in groups.items()},'component_axis_distribution':dict(levels),'prior_metric_scope':ref(P/'Reconciliere_metrici_si_limite.json'),'method':'Nivelul principal al unei surse poate crește printr-o probă nouă, dar istoricul comparatorului se păstrează. Sursele, asocierile, cazurile, evaluările și martorii independenți sunt numărători diferite.','no_sum_as_product_passes':True,'all_methods_of_a_file_not_implied':True})
resources=put('Resurse_si_restituire_Val04.json',{'head':H,'frontend':load(I/'Checkpoint_increment_frontend.json')['resources'],'native':native['resources'],'A12':'Doar fișiere de audit; zero produs, proces de laborator, port, DB sau container creat de A12.','prior_six_retained_roots':load(P/'Resurse_si_restituire_Val03.json'),'automatic_rejection_must_not_be_bypassed':True,'global_cleanup_not_claimed':True})
sources=put('Surse_si_receptii_Val04.json',{'head':H,'inputs':INPUTS,'preflight':ref(O/'MANIFEST_preflight_Val04_0143.json'),'frontend_increment':ref(I/'MANIFEST_increment_frontend.json'),'native_curated':cfg['native_curated'],'receipts_do_not_close_whole_tasks':True})
handoff=put('Handoff_R12_Val04_v1.json',{'schema':'eva.audit.r12.a12.wave/4','utc':now(),'head':H,'server_HEAD_not_candidate':'8c0695de36b50ede569c6d318715db0af11fcbff','mode':'ADITIV_DIN_VAL03; FARA_TESTE_PRODUS_A12','previous_handoff':ref(P/'Handoff_R12_Val03_v2.json'),'previous_manifest':ref(P/'MANIFEST_R12_Val03.json'),'previous_independent_receipt':ref(R/'A11/Val03_registru/Verdict_A11_R12_Val03_registru_v1.json'),'preflight_manifest':ref(O/'MANIFEST_preflight_Val04_0143.json'),'preflight_receipt':ref(R/'A11/Val04_preflight/Verdict_A11_receptie_preflight_A12_0143_v1.json'),'counts':counts,'register':ref(O/'Registru_6728_R12_Val04.jsonl.gz'),'events':eventsref,'static':staticref,'delta':delta_ref,'matrix':matrix,'inverse':invref,'native_checkpoint':ref(O/'G3_checkpoint_nativ_Val04.json'),'metrics':met,'resources':resources,'sources':sources,'checklist':check,'A11_registry_receipt_pending':True,'scores':{'audit':None,'product':None},'all17_contracts_open':True})
htmlpage=f'''<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Audit EVA — R12 Val04</title><style>body{{font:17px/1.55 system-ui;color:#162333;background:#f5f7fb;max-width:1080px;margin:auto;padding:24px}}section{{background:#fff;border:1px solid #d8e0e9;padding:22px;border-radius:12px;margin:18px 0}}a,code,p,td{{overflow-wrap:anywhere}}.table{{overflow-x:auto}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #d5dce5;padding:9px;text-align:left}}h1{{font-size:1.8rem}}h2{{font-size:1.3rem}}small{{color:#4f6175}}</style></head><body><h1>Val04: catalogul de vânzări și disponibilul G3</h1><p>Cod auditat: <code>{H}</code>. HEAD-ul serverului <code>8c0695de…</code> și commitul declarat de T240 <code>6354d628…</code> sunt distincte și nu primesc automat acoperire. Loturile au recepții independente limitate; registrul acestei ediții este predat separat către A11.</p><section><h2>Ce demonstrează probele</h2><p>{html.escape(native['public_summary_ro'])}</p><p>Catalogul frontend are trei mecanisme confirmate în componenta originală: după eroare de rețea/JSON nu se mai lansează cereri; un răspuns HTTP500 în forma sintetică testată este prezentat ca rezultat gol; schimbarea filtrului în timpul unei cereri poate afișa produsele vechi sub noul titlu. Ultimul caz permite recuperare ulterioară și nu este un blocaj permanent.</p><p>Testul frontend a folosit un DOM sintetic și răspunsuri locale, fără API, ERP sau DB real. Două căi conțin același blob: <strong>10 cazuri, nu 20</strong>. Cele 5 controale pozitive și 5 contraexemple sunt distincte de cei 5 martori A11.</p><p>Lectura backend despre paginare și overflow rămâne ipoteză neexecutată. Nu explică automat erorile HTTP injectate și nu adaugă un defect confirmat.</p></section><section><h2>Acoperire și limite</h2><div class="table"><table><tr><th>Numărător</th><th>Situație</th></tr><tr><td>Identități tehnice</td><td>6.728, aceeași alocare și proveniență</td></tr><tr><td>Surse cu dovezi parțiale, la niveluri diferite</td><td>{len(bounded)}; componente, comparatoare, tipuri și binding se separă în registrul de metrici</td></tr><tr><td>Taskuri istorice / criterii</td><td>652 /2.619, fără închideri noi</td></tr><tr><td>Contracte business</td><td>17 deschise; 0 acceptate integral</td></tr></table></div><p>T386 /P01.C10.T0030 este nou în plan și are fișă de intrare; nu extinde lotul istoric de taskuri finalizate. T240 rămâne în implementare. Datele exacte de închidere absente rămân nedocumentate.</p><p>N05 anterior rămâne separat: evidența cantitativă WMS arată 11 din 10 în cazul concurent, fără numărare fizică sau certificare valorică G1. Recuperarea la dezambalare privește componentele recuperabile; cutiile consumate și manopera nu se recreează automat.</p></section><section><h2>Ce se verifică în continuare</h2><p>Reutilizarea funcțiilor existente rămâne prioritară. Catalogul cere tratarea explicită a erorii, eliberarea stării și corelarea ultimei cereri cu filtrul și produsele. O remediere nu se acceptă doar pentru că o singură stare greșită a dispărut.</p><p>Rămân distincte G3, rezervarea nativă, canalul, comanda, DocAction, G1 și UI reală. G2 este necontabilă; costurile cutiilor și manoperei se înregistrează o singură dată în G1. CPP și CPA au identități diferite.</p><ul><li><a href="Handoff_R12_Val04_v1.json">Predarea completă</a></li><li><a href="Reconciliere_metrici_si_limite_Val04.json">Metrici și niveluri de probă</a></li><li><a href="G3_checkpoint_nativ_Val04.json">Probele native G3 și limitele recepției</a></li><li><a href="Increment_01_frontend/Cazuri_frontend_10.json">Cele 10 cazuri frontend</a></li><li><a href="../../A08_Storefront_catalog_lot04/Raport_A08_catalog_lot04_v3.html">Raportul frontend explicat</a></li><li><a href="Matrice_taskuri_criterii_R12_Val04.json">Taskuri, stări și cerințe</a></li><li><a href="Checklist_10_zone_Val04.json">Checklist pe cele 10 zone</a></li><li><a href="Fisa_intake_T386_v1.json">T386 — fișă de intrare</a></li><li><a href="Resurse_si_restituire_Val04.json">Laboratoare și resurse păstrate</a></li><li><a href="../Val_03/index_final.html">Val03 anterior, păstrat imuabil</a></li></ul><small>Resursele al căror cleanup a fost respins automat sunt păstrate. Nu se pretinde restituire globală sau audit integral finalizat.</small></section></body></html>'''
htmlpage=htmlpage.replace('<li><a href="G3_checkpoint_nativ_Val04.json">','<li><a href="../../A05_G3_nativ_lot04/Raport_G3_nativ_lectura_v3.html">Raportul nativ G3 explicat</a></li><li><a href="G3_checkpoint_nativ_Val04.json">')
for a,b in [('înregistrat10','înregistrat 10'),('SO2','SO 2'),('PO de la0 la5','PO de la 0 la 5'),('de la8 la3','de la 8 la 3'),('rămâne8','rămâne 8'),('PO15','PO 15'),('întoarce−7','întoarce −7'),('plafonează la0','plafonează la 0')]:htmlpage=htmlpage.replace(a,b)
assert not (O/'index.html').exists();MEM['index.html']=htmlpage.encode('utf-8')
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag=='a':self.links.extend(v for k,v in attrs if k=='href')
lp=Links();lp.feed(htmlpage)
for link in lp.links:
 q=O/link;assert q.exists() or q.parent==O and q.name in MEM,(link,q)
MEM['build_val04.py']=pathlib.Path(__file__).read_bytes();MEM['build_val04_configuration.json']=read(pathlib.Path(sys.argv[1]))
references_checked=0;git_source_rows_checked=0
for n in list(MEM):
 if n.endswith('.json'):
  for rr in refs(load(O/n)):
   if rr['path'] in D:
    assert rr.get('git_oid')==D[rr['path']]['git_oid']
    if 'source' in rr:assert rr['source']['sha256']==rr['sha256']
    git_source_rows_checked+=1;continue
   validate_ref(rr,O/n);references_checked+=1
for row in updated:
 for rr in refs(row):validate_ref(rr,O/'Registru_6728_R12_Val04.jsonl.gz');references_checked+=1
qa=put('QA_R12_Val04.json',{'utc':now(),'head':H,'handoff':handoff,'counts':counts,'reference_instances_checked':references_checked,'all_checked_reference_instances':len(CHECKS),'git_source_rows_checked':git_source_rows_checked,'all6728_identities_and_routing_preserved':True,'all_previous_evidence_preserved':True,'all652_historic_dossiers_rehashed':True,'criterion_count':2619,'forward_inverse_pairs':len(idx),'legacy_forward_evidence_resolved':len(legacy),'source_roles_not_promoted_from_assignment':True,'HTML_links_checked':len(lp.links),'HTML_rendering_claimed':False,'no_whole_file_or_task_acceptance':True,'issues':[],'score':None})
manifest=put('MANIFEST_R12_Val04.json',{'utc':now(),'head':H,'files':[ref(O/n) for n in sorted(MEM)],'inputs':INPUTS,'preflight_immutable':ref(O/'MANIFEST_preflight_Val04_0143.json'),'frontend_increment_immutable':ref(I/'MANIFEST_increment_frontend.json'),'independent_registry_reception_pending':True,'no_self_reference':True})
if cfg.get('publish'):
 for n,b in MEM.items():assert not (O/n).exists();(O/n).write_bytes(b)
 for n,b in MEM.items():assert (O/n).read_bytes()==b
 print(json.dumps({'manifest':manifest,'handoff':handoff,'QA':qa,'counts':counts},ensure_ascii=False))
else:print(json.dumps({'status':'PREGĂTIT ÎN MEMORIE; FĂRĂ SIGILARE','files':len(MEM),'counts':counts,'references_checked':references_checked},ensure_ascii=False))
