import collections,copy,gzip,hashlib,html,json,pathlib,sys
from html.parser import HTMLParser
from datetime import datetime,timezone
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');R=B/'executie/R12_fisiere';P=R/'A12/Val_04';O=R/'A12/Val_05';H='df85d33c1648ce2b2df130a60a05ef696e2e5480'
MEM={};INPUTS=[];CHECKS=[];HC={};JC={}
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return MEM[p.name] if p.parent==O and p.name in MEM else p.read_bytes()
def load(p):
 if p not in JC:JC[p]=json.loads(read(p).decode('utf-8-sig'))
 return JC[p]
def ref(p,pointer=None):
 b=read(p);r={'path':p.relative_to(B).as_posix() if p.is_relative_to(B) else p.as_posix(),'sha256':sha(b),'bytes':len(b)}
 if pointer is not None:r['pointer']=pointer
 return r
def put(n,x):
 assert n not in MEM and not (O/n).exists(),n
 MEM[n]=(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8');return ref(O/n)
def refs(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str) and len(x['sha256'])==64:yield x
  for v in x.values():yield from refs(v)
 elif isinstance(x,list):
  for v in x:yield from refs(v)
def point(x,p):
 for k in p.removeprefix('#').lstrip('/').split('/') if p not in ('','#') else []:
  k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
 return x
def resolve(origin,s):
 p=pathlib.Path(s)
 if p.is_absolute():return p
 if s.startswith('executie/'):return B/p
 q=origin.parent/p
 if q.exists() or q.parent==O and q.name in MEM:return q
 matches=[z/p for z in [origin.parent.parent,origin.parent.parent.parent,R,B] if (z/p).exists()]
 assert len(set(matches))==1,(origin,s,matches)
 return matches[0]
def check(rr,origin):
 if rr['path'].startswith(('idempiere/','frontend/')) and isinstance(rr.get('source'),dict):
  q=B/rr['source']['path'];bb=read(q)
  assert sha(bb)==rr['sha256']==rr['source']['sha256']
  assert hashlib.sha1(b'blob '+str(len(bb)).encode()+b'\0'+bb).hexdigest()==rr['git_oid']
  CHECKS.append(rr);return q
 q=resolve(origin,rr['path'])
 if q not in HC:HC[q]=ref(q)
 assert HC[q]['sha256']==rr['sha256'],(q,HC[q]['sha256'],rr['sha256'])
 if 'bytes' in rr:assert HC[q]['bytes']==rr['bytes'],q
 if rr.get('pointer') is not None:point(load(q),rr['pointer'])
 CHECKS.append(rr);return q
def verify(p,h=None):
 if h:assert ref(p)['sha256']==h,(p,ref(p)['sha256'],h)
 for rr in refs(load(p)):check(rr,p)
 INPUTS.append(ref(p));return load(p)
cfg=load(pathlib.Path(sys.argv[1]));assert cfg['head']==H and cfg['all_lots_received_by_A11']
verify(P/'MANIFEST_R12_Val04.json','0c6ca1b0fda74735ff4b40ae7f8ef4a0f2615f66c55b0d012654e1213bbfef46')
verify(P/'Handoff_R12_Val04_v1.json','04b060555be96ba4c0785c4d429b76bd995611f47a43790480f840c92ff34866')
verify(R/'A11/Val04_registru/Verdict_A11_R12_Val04_registru_v1.json','fbe5eed1c4b228513d194cfaf741e586990f07b8623236f5ac6e55281a4f0932')
verify(O/'MANIFEST_preflight_Val05_0245_v2.json','40b3bab9c238b67fe1130ce04e887f99fabf91ba26266f0dfac90737699e4bdf')
verify(O/'MANIFEST_preflight_Val05_0245.json','ddb532e29613c72143fbe69ed70fa0bdfc9ccc8ac6542b9743a7e897d439ebd1')
verify(R/'A11/Val05_preflight/Verdict_A11_receptie_preflight_A12_0245_v1.json','94f9bafb247c9f500d4c13c0d6113295c4db39e77f7acdeec48951ccb8efaae8')
for rr in cfg['inputs']:verify(B/rr['path'],rr['sha256'])
prior=[json.loads(x) for x in gzip.decompress(read(P/'Registru_6728_R12_Val04.jsonl.gz')).decode().splitlines()];D={r['path']:r for r in prior};assert len(D)==len(prior)==6728
updated=copy.deepcopy(prior);U={r['path']:r for r in updated};lots=[]
for rr in cfg['increments']:
 lot=verify(B/rr['path'],rr['sha256']);assert lot['head']==H and lot['independent_receipt'] and lot['full_file_or_contract_acceptances']==0;lots.append(lot)
assert len(lots)==2 and cfg['native_lot_complete'], 'Predarea nativă și dispoziția A11 sunt obligatorii înainte de sigilare.'
new_events=[copy.deepcopy(e) for lot in lots for e in lot['runtime_events']]
new_support=[copy.deepcopy(e) for lot in lots for e in lot['support_rows']]
assert len({(e['path'],e['event_id']) for e in new_events})==len(new_events)
for e in new_events+new_support:
 d=D[e['path']];assert e['git_oid']==d['git_oid'] and e['owner']==d['owner'] and e['planned_peer']==d['planned_peer']
 p=B/e['source']['path'];bb=read(p);assert sha(bb)==e['sha256']==e['source']['sha256']
 assert hashlib.sha1(b'blob '+str(len(bb)).encode()+b'\0'+bb).hexdigest()==e['git_oid']
 assert not e.get('whole_file_accepted',False)
events=put('Evenimente_Val05.json',{'head':H,'rows':new_events,'unit':'Perechea (cale,event_id) este o asociere. Scenariile, cazurile, apelurile și recitirile se raportează separat în fiecare lot.','lots':[{'execution_receipt':x['independent_receipt'],'cases':x['cases'],'counts':x['counts']} for x in lots],'score':None})
support=put('Observatii_suport_Val05.json',{'head':H,'rows':new_support,'associations':len(new_support),'paths':len({r['path'] for r in new_support}),'runtime_credit':0,'note':'Compilarea, constantele, citirea sursei și contextul sunt distincte; niciuna nu devine automat apel de metodă.'})
def scope_rank(state):
 if state=='UNVERIFIED_R12':return 0
 if 'TYPE_USE' in state:return 1
 if 'FIXTURE' in state or 'BINDING_METADATA' in state:return 2
 if 'COMPARATOR' in state:return 3
 return 4
for i,e in enumerate(new_events):
 u=U[e['path']]
 if not any(x.get('wave')=='Val04' and 'before_Val05' in x for x in u.get('axis_history',[])):
  u.setdefault('axis_history',[]).append({'wave':'Val04','before_Val05':copy.deepcopy(u['axis']),'prior_register':ref(P/'Registru_6728_R12_Val04.jsonl.gz')})
 for k,v in e['accepted_axis_updates'].items():
  assert k in u['axis'] and k!='whole_file_acceptance',k
  if k=='component_exercised' and scope_rank(u['axis'][k])>scope_rank(v):continue
  if k=='component_exercised' and u['axis'][k]=='NATIVE_BUSINESS_METHOD_PARTIAL' and 'TRANSITIVE' in v:continue
  u['axis'][k]=v
 u['current_evidence'].append({'event_id':e['event_id'],'source':ref(O/'Evenimente_Val05.json','/rows/'+str(i)),'method_kind':e['method_kind'],'scope':'PARTIAL_ONLY','independent_reception':e['independent_receipt'],'execution_group':e['execution_group'],'granular_levels':e.get('granular_levels',{})})
 u['peer_receipts']['independent_A11']=e['independent_receipt'];u['executor_for_current_event']=e['actual_executor'];u['planned_peer_performed_not_inferred']=True
for i,s in enumerate(new_support):
 u=U[s['path']]
 if u['axis']['read'] in ['UNVERIFIED_R12','NO_NEW_CREDIT_IN_THIS_WAVE']:u['axis']['read']='BOUNDED_SUPPORT_OBSERVATION_ONLY'
 u['current_evidence'].append({'source':ref(O/'Observatii_suport_Val05.json','/rows/'+str(i)),'scope':s['scope'],'execution_credit':False,'independent_reception':s['independent_receipt'],'granular_levels':s.get('granular_levels',{})})
identity_keys=['id','path','git_oid','git_mode','candidate','owner','planned_peer','control','pipeline_candidates','task_candidates']
for u in updated:
 d=D[u['path']]
 assert all(u[k]==d[k] for k in identity_keys),u['path']
 assert u['R11_reference_only']==d['R11_reference_only'] and u['file_verdict'] is None and u['axis']['whole_file_acceptance'] is None
 assert u['current_evidence'][:len(d['current_evidence'])]==d['current_evidence']
 if u['R11_reference_only']:assert u['R11_reference_only']['credit_transferred'] is False
raw=('\n'.join(json.dumps(r,ensure_ascii=False,separators=(',',':')) for r in updated)+'\n').encode()
MEM['Registru_6728_R12_Val05.jsonl.gz']=gzip.compress(raw,mtime=0)
delta=[{'path':u['path'],'git_oid':u['git_oid'],'owner':u['owner'],'peer':u['planned_peer'],'before_axis':D[u['path']]['axis'],'after_axis':u['axis'],'new_evidence':u['current_evidence'][len(D[u['path']]['current_evidence']):]} for u in updated if u!=D[u['path']]]
deltaref=put('Delta_integrala_Val05.json',{'head':H,'prior_register':ref(P/'Registru_6728_R12_Val04.jsonl.gz'),'current_register':ref(O/'Registru_6728_R12_Val05.jsonl.gz'),'changed_rows':len(delta),'new_identities':0,'rows':delta,'no_previous_evidence_removed':True})
oldidx=load(P/'Index_invers_surse_Val04.json');idx=copy.deepcopy(oldidx['rows'])
for i,e in enumerate(new_events):idx.append({'path':e['path'],'event_id':e['event_id'],'git_oid':e['git_oid'],'owner':e['owner'],'peer':e['planned_peer'],'control':e['control'],'pipelines':e['pipeline_candidates'],'tasks':e['task_candidates_preserved'],'method_kind':e['method_kind'],'execution_group':e['execution_group'],'event_source':ref(O/'Evenimente_Val05.json','/rows/'+str(i))})
forward={(r['path'],e['event_id']) for r in updated for e in r['current_evidence'] if 'event_id' in e};inverse={(e['path'],e['event_id']) for e in idx}
legacy=copy.deepcopy(oldidx['legacy_Val01_pointer_resolution'])
for z in legacy:
 source=z['event_source'];q=check(source,P/'Index_invers_surse_Val04.json');ev=point(load(q),source['pointer']);assert ev['path']==z['path'] and ev['event_id']==z['event_id']
 assert U[z['path']]['current_evidence'][z['existing_forward_evidence_index']]==z['existing_forward_proof']
 forward.add((z['path'],z['event_id']))
assert len(idx)==len(inverse) and forward==inverse
allstatic=copy.deepcopy(oldidx['static_observations'])+[s for s in new_support if s['scope']!='COMPILE_ONLY_NO_METHOD_CREDIT']
compilation=[s for s in new_support if s['scope']=='COMPILE_ONLY_NO_METHOD_CREDIT']
inv=put('Index_invers_surse_Val05.json',{'head':H,'rows':idx,'key':['path','event_id'],'forward_inverse_pairs_equal':True,'legacy_Val01_pointer_resolution':legacy,'static_observations':allstatic,'compilation_support_observations':compilation,'no_method_credit_from_compilation':True,'static_observation_paths':len({s['path'] for s in allstatic}),'note':'Probele vechi, inclusiv comparatoarele SQL, sunt păstrate. Noul nivel principal nu șterge observațiile anterioare și nu mută creditul la alt commit.'})
historic=copy.deepcopy(load(P/'Conservare_652_fise_2619_criterii_Val04.json'))
assert len(historic['all_dossiers_rehashed'])==652 and sum(r['criteria_count_as_historic'] for r in historic['all_dossiers_rehashed'])==2619
for r in historic['all_dossiers_rehashed']:check(r['dossier'],P/'Conservare_652_fise_2619_criterii_Val04.json')
historic['previous_immutable_copy']=ref(P/'Conservare_652_fise_2619_criterii_Val04.json');historic['rechecked_utc']=now();historic['current_new_credit']=0
put('Conservare_652_fise_2619_criterii_Val05.json',historic)
snapshot=B/'executie/delta/2026-11-03T02-45-48-441Z/00_STATUS_TASKURI.json';tasks=load(snapshot);lookup={r['id']:(i,r) for i,r in enumerate(tasks) if r.get('proiect')=='P01'};assert len(tasks)==997 and len(lookup)==694
taskrows=[]
for alias in ['T232','T240','T343','T355','T386']+cfg.get('additional_task_aliases',[]):
 i,t=lookup[alias];assert t['stare_generala']
 taskrows.append({'alias':alias,'canonical':t.get('cod_capitol'),'source':ref(snapshot,'/'+str(i)),'current_state':t['stare_generala'],'state_source_field':'stare_generala','progress_declared':t.get('procent'),'new_task_or_criterion_acceptance':0,'exact_closing_date_not_inferred':True})
matrix=put('Matrice_taskuri_criterii_R12_Val05.json',{'head':H,'previous_matrix':ref(P/'Matrice_taskuri_criterii_R12_Val04.json'),'historic_tasks':652,'historic_criteria':2619,'historic_criteria_newly_accepted':0,'current_rows':taskrows,'T386_prior_intake':ref(P/'Fisa_intake_T386_v1.json'),'new_lot_task_mappings':[{'mapping':x['task_mapping'],'proof':cfg['increments'][i]} for i,x in enumerate(lots)],'nominal_task_links':cfg.get('nominal_task_links',[]),'source_comment_is_not_accepted_criterion':True,'CO_IP':'Autoritatea CO/IP rămâne deschisă; documentul nou T343 nu schimbă oracolul nominal. O stare IP observată poate fi probă de traseu, fără rezolvarea acestei controverse.','population':ref(O/'Supliment_populatie_0245.json'),'all17_contracts_open':True})
prior_metrics=load(P/'Reconciliere_metrici_si_limite_Val04.json');priorbounded={r['path'] for r in prior if r['axis']['component_exercised']!='UNVERIFIED_R12'};bounded=[r for r in updated if r['axis']['component_exercised']!='UNVERIFIED_R12'];groups={}
for r in bounded:
 s=r['axis']['component_exercised'];g='tip_record' if 'TYPE_USE' in s else 'fixture_binding_metadate' if 'FIXTURE' in s or 'BINDING_METADATA' in s else 'comparator_SQL' if 'SQL_COMPARATOR' in s else 'comparator_shell' if 'SHELL_COMPARATOR' in s else 'componenta_sau_traseu_metoda_originala'
 groups.setdefault(g,[]).append(r['path'])
counts={'technical_identities':6728,'historical_tasks':652,'historical_criteria':2619,'current_P01_members':694,'prior_bounded_source_identities':44,'current_bounded_source_identities':len(bounded),'new_bounded_source_identities':len({r['path'] for r in bounded}-priorbounded),'cumulative_event_pairs':len(idx),'new_bounded_evidence_event_associations':len(new_events),'new_bounded_evidence_path_identities':len({r['path'] for r in new_events}),'new_support_associations':len(new_support),'new_support_paths':len({r['path'] for r in new_support}),'new_compile_only_paths':len({r['path'] for r in compilation}),'cumulative_static_observation_paths':len({r['path'] for r in allstatic}),'R11_reference_only':116,'R11_credit_transferred':0,'new_full_file_acceptances':0,'new_full_task_acceptances':0,'new_full_criterion_acceptances':0,'contracts_closed':0,'contracts_open':17}
assert counts['current_bounded_source_identities']>=51 and sum(map(len,groups.values()))==len(bounded)
met=put('Reconciliere_metrici_si_limite_Val05.json',{'head':H,'counts':counts,'current_exclusive_primary_levels':{k:{'count':len(v),'paths':v} for k,v in groups.items()},'component_axis_distribution':dict(collections.Counter(r['axis']['component_exercised'] for r in updated)),'prior_metrics':ref(P/'Reconciliere_metrici_si_limite_Val04.json'),'lot_metrics_separate':[{'receipt':lot['independent_receipt'],'counts':lot['counts']} for lot in lots],'method':'Compilat, clasă încărcată, metodă apelată, traseu tranzitiv, binding și efect persistent sunt câmpuri diferite. Se numără sursele distincte; scenariile, cazurile și martorii independenți nu se însumează ca funcționalități acceptate.','no_sum_as_product_passes':True})
findings=put('Constatari_calificate_Val05.json',{'head':H,'previous_immutable_findings':ref(P/'Constatari_calificate_Val04.json'),'lot_findings':[x['findings'] for x in lots],'no_duplicate_of_prior_mechanism':cfg['finding_count_policy'],'new_full_acceptances':0,'score':None})
prevcheck=load(P/'Checklist_10_zone_Val04.json');zones=[]
for z in prevcheck['rows']:
 owner=z['owner'];zones.append({'owner':owner,'assigned_files':sum(u['owner']==owner for u in updated),'new_event_associations':sum(e['owner']==owner for e in new_events),'new_support_associations':sum(e['owner']==owner for e in new_support),'actual_executors_new':dict(collections.Counter(e['actual_executor'] for e in new_events if e['owner']==owner)),'whole_acceptances':0,'next_action':cfg['zone_actions'][owner],'peer_performed_not_inferred_from_assignment':True})
assert len(zones)==10 and sum(z['assigned_files'] for z in zones)==6728
checklist=put('Checklist_10_zone_Val05.json',{'head':H,'rows':zones,'previous':ref(P/'Checklist_10_zone_Val04.json'),'A11_current':cfg['A11_current_checklist'],'new_lot_next_controls':[x['next_controls'] for x in lots],'contracts':prevcheck['contracts'],'protocol_before_next_product_execution':True,'score':None})
resources=put('Resurse_si_restituire_Val05.json',{'head':H,'previous_resources':ref(P/'Resurse_si_restituire_Val04.json'),'lot_resources':[x['resources'] for x in lots],'eight_retained_roots':['D:/CodexWork/p01-r12-masini-dates','D:/CodexWork/a11-r12-mutator-20261103','D:/CodexWork/a11-r12-mutator-20261103-v2','D:/CodexWork/p01-r12-t343-tools-l03','D:/CodexWork/p01-r12-t343-tools-l03-v2','D:/CodexWork/a10-r12-l03','D:/CodexWork/a11-catalog-oracle-l05-20261103','D:/CodexWork/a08-catalog-json-l05-20261103'],'automatic_cleanup_rejection':'blocked by policy; niciun bypass sau ștergere prin altă metodă','A12':'Zero execuții produs, laborator, DB, container sau port creat. Numai curatoriat de artefacte.','global_cleanup_not_claimed':True})
checkpoints=[]
for i,lot in enumerate(lots):checkpoints.append(put('Checkpoint_'+cfg['lot_names'][i]+'_Val05.json',lot))
sources=put('Surse_si_receptii_Val05.json',{'head':H,'inputs':INPUTS,'preflight':ref(O/'MANIFEST_preflight_Val05_0245_v2.json'),'increments':cfg['increments'],'independent_receptions_do_not_close_tasks':True})
handoff=put('Handoff_R12_Val05_v1.json',{'schema':'eva.audit.r12.a12.wave/5','utc':now(),'head':H,'server_HEAD_not_candidate':'c594a93a1d4e606f8c2e432108a29e97244d692e','mode':'ADITIV_DIN_VAL04; FARA_TESTE_PRODUS_A12','previous_handoff':ref(P/'Handoff_R12_Val04_v1.json'),'previous_manifest':ref(P/'MANIFEST_R12_Val04.json'),'previous_independent_receipt':ref(R/'A11/Val04_registru/Verdict_A11_R12_Val04_registru_v1.json'),'preflight_handoff':ref(O/'Handoff_preflight_Val05_v2.json'),'preflight_receipt':ref(R/'A11/Val05_preflight/Verdict_A11_receptie_preflight_A12_0245_v1.json'),'counts':counts,'register':ref(O/'Registru_6728_R12_Val05.jsonl.gz'),'events':events,'support':support,'delta':deltaref,'matrix':matrix,'inverse':inv,'checkpoints':checkpoints,'metrics':met,'resources':resources,'sources':sources,'checklist':checklist,'A11_registry_receipt_pending':True,'all17_contracts_open':True,'scores':{'audit':None,'product':None}})
sections=''.join('<section><h2>'+html.escape(cfg['lot_titles'][i])+'</h2><p>'+html.escape(lot['public_summary_ro'])+'</p><p>'+html.escape(cfg['public_limits'][i])+'</p><p><a href="'+html.escape(cfg['reading_links'][i],quote=True)+'">Raportul explicat și limitele sale</a></p></section>' for i,lot in enumerate(lots))
level_labels={'tip_record':'Utilizare de tip sau record','fixture_binding_metadate':'Configurare, legare de servicii ori metadate ale fixturei','comparator_SQL':'Comparator SQL','comparator_shell':'Comparator shell','componenta_sau_traseu_metoda_originala':'Componentă sau traseu al metodei originale, în limitele probate'}
rowshtml=''.join('<tr><td>'+html.escape(level_labels[k])+'</td><td>'+str(len(v))+'</td></tr>' for k,v in groups.items())
page=f'''<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Audit EVA — R12 Val05</title><style>body{{font:17px/1.55 system-ui;color:#162333;background:#f5f7fb;max-width:1080px;margin:auto;padding:24px}}section{{background:#fff;border:1px solid #d8e0e9;padding:22px;border-radius:12px;margin:18px 0}}a,code,p,td{{overflow-wrap:anywhere}}.table{{overflow-x:auto}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #d5dce5;padding:9px;text-align:left}}h1{{font-size:1.8rem}}h2{{font-size:1.3rem}}</style></head><body><h1>Val05 — catalog și comandă nativă</h1><p>Versiunea auditată: <code>{H}</code>. HEAD-ul separat al serverului <code>c594a93a…</code> nu primește acoperire. Loturile au recepții independente limitate; registrul acestei ediții se predă separat către A11.</p>{sections}<section><h2>Acoperire fără echivalări</h2><p>Registrul păstrează 6.728 de identități tehnice și alocarea lor. Sunt {len(bounded)} de surse cu dovezi limitate la niveluri diferite, dintre care {counts['new_bounded_source_identities']} apar pentru prima dată în acest numărător față de cele 44 din Val04.</p><div class="table"><table><tr><th>Nivel principal exclusiv</th><th>Surse</th></tr>{rowshtml}</table></div><p>Compilarea sau încărcarea unei clase nu reprezintă acceptarea metodelor sale. Cazurile, subcazurile, recitirile și martorii independenți rămân numărători separate în rapoartele loturilor.</p><p>Cele 652 de fișe și 2.619 criterii istorice rămân păstrate, fără criterii acceptate integral în acest val. Populația actuală este 694 P01 din 997 taskuri. T386 era deja în plan, iar T343 are numai actualizările documentare explicate în preflight. Toate cele 17 contracte business rămân deschise.</p></section><section><h2>Documente de control</h2><ul><li><a href="Handoff_R12_Val05_v1.json">Predarea completă</a></li><li><a href="Reconciliere_metrici_si_limite_Val05.json">Metrici și niveluri</a></li><li><a href="Matrice_taskuri_criterii_R12_Val05.json">Taskuri și cerințe</a></li><li><a href="Checklist_10_zone_Val05.json">Continuarea pe zece zone</a></li><li><a href="Resurse_si_restituire_Val05.json">Resurse și cele opt rădăcini reținute</a></li><li><a href="index_preflight.html">Comparația capturilor și documentul T343</a></li><li><a href="../Val_04/index.html">Val04, păstrat imuabil</a></li></ul><p>CPP și CPA au identități distincte. G2 este necontabilă; cutiile și manopera se înregistrează o singură dată în G1, iar dezambalarea restituie numai componentele recuperabile. Probele curente nu închid contabilitatea G1, autorizarea ori UX-ul nativ.</p><p>Cele opt directoare a căror ștergere a fost respinsă automat sunt păstrate, fără ocolire. Nu se pretinde restituire globală sau audit integral finalizat.</p></section></body></html>'''
MEM['index.html']=page.encode('utf-8')
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,t,attrs):
  if t=='a':self.links.extend(v for k,v in attrs if k=='href')
lp=Links();lp.feed(page)
for link in lp.links:
 p=O/link;assert p.exists() or p.parent==O and p.name in MEM,link
MEM['build_val05.py']=pathlib.Path(__file__).read_bytes();MEM['build_val05_configuration.json']=read(pathlib.Path(sys.argv[1]))
reference_count=0;source_rows=0
for n in list(MEM):
 if n.endswith('.json'):
  for rr in refs(load(O/n)):
   if rr['path'] in D:
    assert rr.get('git_oid')==D[rr['path']]['git_oid'];source_rows+=1;continue
   check(rr,O/n);reference_count+=1
for u in updated:
 for rr in refs(u):check(rr,O/'Registru_6728_R12_Val05.jsonl.gz');reference_count+=1
qa=put('QA_R12_Val05.json',{'utc':now(),'head':H,'handoff':handoff,'counts':counts,'reference_instances_checked':reference_count,'all_checked_reference_instances':len(CHECKS),'git_source_rows_checked':source_rows,'all6728_identities_and_routes_preserved':True,'all_prior_evidence_preserved':True,'all652_dossiers_rehashed':True,'criteria':2619,'forward_inverse_pairs':len(idx),'legacy_pairs':len(legacy),'peer_not_inferred_from_assignment':True,'HTML_links_checked':len(lp.links),'HTML_rendering_claimed':False,'whole_acceptances':0,'issues':[],'score':None})
manifest=put('MANIFEST_R12_Val05.json',{'utc':now(),'head':H,'files':[ref(O/n) for n in sorted(MEM)],'inputs':INPUTS,'preflight_immutable':ref(O/'MANIFEST_preflight_Val05_0245_v2.json'),'increments_immutable':cfg['increments'],'independent_registry_reception_pending':True,'no_self_reference':True})
if cfg.get('publish'):
 for n,b in MEM.items():assert not (O/n).exists();(O/n).write_bytes(b)
 for n,b in MEM.items():assert (O/n).read_bytes()==b
 print(json.dumps({'manifest':manifest,'handoff':handoff,'QA':qa,'counts':counts},ensure_ascii=False,indent=2))
else:print(json.dumps({'status':'EN_MEMOIRE; SANS_SIGILARE','files':len(MEM),'counts':counts,'references_checked':reference_count},ensure_ascii=False,indent=2))
