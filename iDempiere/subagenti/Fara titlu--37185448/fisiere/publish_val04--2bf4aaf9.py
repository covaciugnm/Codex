from build_val04 import *
import html
# Populate only after independent receipts arrive; accepted producer evidence is not self approval.
cfg=source(V/'receptii_independente.json')
assert cfg['all_supplements_received']is True
reviewed=[]
def refs_recursive(x):
 if isinstance(x,dict):
  if x.get('path','').startswith('executie/')and x.get('sha256'):source(B/x['path'],x['sha256'])
  for y in x.values():refs_recursive(y)
 elif isinstance(x,list):
  for y in x:refs_recursive(y)
for ss in cfg['seals']:source(B/ss['path'],ss['sha256'])
for rp in cfg['verdicts']:
 f=B/rp['path'];j=source(f,rp['sha256']);reviewed.append(ref(f))
 refs_recursive(j)
 for group in ['inputs','proofs','methods','reproduction_methods']:
  rs=j.get(group,[])
  if isinstance(rs,list):
   for q in rs:
    if isinstance(q,dict)and q.get('path','').startswith('executie/')and q.get('sha256'):source(B/q['path'],q['sha256'])
  elif isinstance(rs,dict):
   for path,h in rs.items():
    if isinstance(h,str)and len(h)==64:
     t=B/path if path.startswith('executie/')else O/path
     source(t,h)
# Add partial independent receipt metadata; do not infer a second runtime execution from a review.
uivf=O/'A11/Verdict_A11_R11_UI_V12_v1.json'
source(uivf,'97bc276c0a40aaca6343db3522f5fab9fa563146fc9eba8b3ce316583f4e2f2e')
for r in ui['file_records']:
 R[r['path']].setdefault('Val04_independent_reviews',[]).append({'source':ref(uivf),'scope':'Recepție limitată UI/configurare/help; efecte ERP și criterion assignment rămân separate.'})
hrreview=next(r for r in reviewed if 'backend_HR' in r['path'])
a05review=next(r for r in reviewed if 'A05_native' in r['path'])
for r in hr['sources']:
 R[r['path']].setdefault('Val04_independent_reviews',[]).append({'source':hrreview,'scope':'Recepție limitată HR; nu credit de task din #86.'})
for r in a05['source_trace']:
 R[cont+'src/com/eva/ro/contab/'+r['file']].setdefault('Val04_independent_reviews',[]).append({'source':a05review,'scope':'Lectură și binding pe clasa declarată;24 martori beforeSave nativi cu gettere sintetice nu se aplică întregii surse EVA.'})
latestf=B/'executie/delta/2026-11-02T22-49-25-027Z/Comparatie_ultimul_checkpoint.json';latest=source(latestf)
assert latest['old_head']==HEAD and latest['new_head']=='df85d33c1648ce2b2df130a60a05ef696e2e5480'and latest['changes']==[]and latest['p01']==693
addf=O/'A11/Addendum_A11_T32_L6j_limita_Val04.json';addj=source(addf,'9b82837accc4a466e99893ac2b88ca004f8f092eebf933d89c713e0ec1d522f1')
assert R[addj['file']]['git_oid']==addj['git_oid']
add(addj['file'],addf,'/required_interpretation','A11',['inspected'],'Limită a oracolului pozitiv în4 instanțe; nu defect de produs sau răspuns500 observat.',addj['required_interpretation'],addj['scope'])
case['limitation'].append(addj['required_interpretation']);case['proofs'].append(ref(addf))
selected[addj['file']]['Val04_oracle_addendum']=ref(addf)
selected[addj['file']]['semantic_limit']+=' '+addj['required_interpretation']
planf=O/'A05/Val_04/Pregatire_clona_nativa_N05_propusa.json';source(planf,'a0cdefc673584dfd035d9201f965a54777674ab33e3e2f5a6a4534ff91472253')
# Owner, phase and full suite status remain separate.
selected_rows=list(selected.values())
for s in selected_rows:
 s['effective_nonfailed_call_events']=sum(e['event']['stage']=='call'and e['event']['outcome']=='passed'for e in s['selected_events'])
 s['effective_failed_call_events']=sum(e['event']['stage']=='call'and e['event']['outcome']=='failed'for e in s['selected_events'])
 if s['file'].endswith('test_tenant_isolation_116.py'):
  assert s['effective_nonfailed_call_events']==s['effective_failed_call_events']==0
  assert R[s['file']]['axis']['exercised']=='UNVERIFIED'
  s['effective_scope']='20_SKIP_ZERO_CALL_FARA_CREDIT_FUNCTIONAL'
 assert len(s['history'])==len({(x['path'],x['pointer'])for x in s['history']})
for t in matrix['task_rows']:
 cs=[c for c in matrix['criterion_rows']if c['task']==t['task']]
 t['R11_direct_cases']=sorted({ci for c in cs for ci in c['R11_cases']})
 t['R11_linked_criteria']=[c['criterion']for c in cs if c['R11_cases']]
 assert t['whole_task_current_verdict']is None
matrix['utc']=now();matrix['previous_matrix']=ref(B/prior['task_matrix']['path'])
matrix['Val04_new_criterion_ids']=0;matrix['Val04_new_case_links']=1
matrix['Val04_supplements']=[ref(ui_file),ref(be_file),ref(hr_file),ref(a05f)]
matrix['Val04_independent_receipts']=reviewed
matrix['prior_checkpoint_acceptance']=ref(previous_A11)
matrix['new_HEAD_not_covered']={'head':latest['new_head'],'evidence':ref(latestf),'tested':False}
contracts['utc']=now();contracts['previous']=ref(B/prior['contracts']['path'])
for co in contracts['contracts']:
 co['Val04_scope']='PROBE_ADITIONALE_LIMITATE;CONTRACT_NATIV_RAMANE_DESCHIS'
 co['Val04_complete']=False
 if co['id']=='D03':co['Val04_evidence']=[ref(a05f,'/source_trace'),ref(a05f,'/native_findings')]
 if co['id']=='D16':co['Val04_context_only']='C67 are cele4 suite în rulări separate; nu este închidere nativă, două scheme ori jurnal GL.'
 if co['id']=='D01':co['Val04_context_only']='HR probează ASGI/context/JWT pe PG sintetic, fără login UI sau două instanțe de cabinet.'
for owner,v in contracts['ten_zones'].items():
 v['content_inspected_files']=sum(r['owner']==owner and r['axis']['inspected']!='UNVERIFIED'for r in R.values())
 v['exercise_scope_files']=sum(r['owner']==owner and r['axis']['exercised']!='UNVERIFIED'for r in R.values())
 v['Val04_new_events']=sum(R[e['path']]['owner']==owner for e in events)
 v['Val04_whole_zone_verdict']=None
for ch in contracts['chapters']:
 ts=[t for t in matrix['task_rows']if t['chapter']==ch['chapter']]
 ch['with_R11_direct_observation']=sum(bool(t['R11_direct_cases'])for t in ts)
 ch['linked_criteria']=sum(len(t['R11_linked_criteria'])for t in ts)
# Preserve all contexts and granular physical effects before/after; no raw business data.
actors=source(O/'HR_izolare_Val03/actors.json',hr['results']['independent_auth_matrix']['sha256'])
assert len(actors['requests'])==27 and all(x['matches_expected']and x['fresh_connection_verification']for x in actors['requests'])
assert actors['tenant_context_unmodified']and actors['jwt_signer_real_synthetic_secret']
assert all(x['native_unchanged']for x in actors['requests'])
for r in R.values():
 assert r['candidate']==HEAD and r['file_verdict']is None
 for e in r['evidence']:ptr(source(B/e['source_file'],e['source_sha256']),e['pointer'])
cm={c['criterion']:c for c in matrix['criterion_rows']}
for link in matrix['nominal_links']:
 assert link['case']in cm[link['criterion']]['R11_cases']
 for q in link['proofs']:ptr(source(B/q['path'],q['sha256']),q.get('pointer',''))
for c in cm.values():
 for cas in c['R11_cases']:assert any(l['case']==cas and l['criterion']==c['criterion']for l in matrix['nominal_links'])
def vh(t):
 q=t['historical_dossier'];assert sha(B/q['file'])==q['sha256'];return t['task']
with ThreadPoolExecutor(max_workers=8)as ex:verified=list(ex.map(vh,matrix['task_rows']))
for q in inputs.values():assert sha(B/q['path'])==q['sha256'],q['path']
counts={'files':len(R),'tasks':len(matrix['task_rows']),'criteria':len(cm),
 'linked_partial_criteria':sum(bool(c['R11_cases'])for c in cm.values()),'tasks_with_partial_links':sum(bool(t['R11_direct_cases'])for t in matrix['task_rows']),
 'new_criterion_ids':0,'new_semantic_case_links':1,'full_task_verdicts':0,'full_file_verdicts':0,
 'new_events':len(events),'new_event_distinct_files':len({e['path']for e in events}),
 'files_by_axis':{a:sum(r['axis'][a]!='UNVERIFIED'for r in R.values())for a in next(iter(R.values()))['axis']}}
assert counts['files']==6709 and counts['tasks']==652 and counts['criteria']==2619 and counts['linked_partial_criteria']==20 and counts['tasks_with_partial_links']==6
assert dict(phase)=={'call|passed':1206,'setup|skipped':38,'call|skipped':13,'call|failed':2}
reg=V/'Registru_6709_val_04.jsonl.gz';assert not reg.exists()
with reg.open('wb')as f:
 with gzip.GzipFile(fileobj=f,mode='wb',filename='',mtime=0)as gz:
  for r in R.values():gz.write((json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n').encode())
matf=save('Matrice_criterii_task_probe_val04.json',matrix)
pipef=save('Contracte_17_si_capitole_val04.json',contracts)
evf=save('Evenimente_val_04.json',{'utc':now(),'head':HEAD,'previous':ref(B/prior['register']['path']),'events':events,'scope':'Nu se adună execuția unei probe native limitate la toate sursele citite sau la toate criteriile taskului.'})
sf=save('Reconciliere_63_suite_val04.json',{'utc':now(),'head':HEAD,'previous':ref(B/prior['suites']['path']),
 'rows':selected_rows,'program_sources':63,'added_program_sources':8,'replaced_whole_UI_program_snapshots':7,'replaced_HR_case_events':3,
 'HR_substitutions':hr_substitutions,'HR_other_suite_cases_rerun':False,
 'latest_whole_program_snapshot_exit_counts':{'0':57,'1':6},'mixed_selective_HR_suites':2,
 'latest_full_suite_exit_cannot_be_inferred_from_selected_cases':True,
 'current_selected_report_events_by_phase':dict(phase),'current_selected_report_events_by_type':dict(typed),
 'report_events_count':sum(phase.values()),'events_are_not_distinct_tests':True,
 'native_or_mock_layers':{'V7_V10_V12_V13':'Mock context/ERP as original tests; SQLite and local fixture. V12/V13 no Node.','HR_original_three':'Original tenant stub/SQLite plus minimal read-only PG projection.','HR_27_ASGI_separate':'Original JWT/context and SQL gateway PG; native mirror remains mock; no OSGi.','A05_four_native_method_cases_separate':'Only MPPProductBOMLine.beforeSave with synthetic getters; not PO.saveEx.'},
 'method_erratum':ref(err_file),'independent_receipts':reviewed,'whole_task_acceptance':False,
 'remaining_signals':['SAGA /webui/ versus /app/remote assertion remains failed; native navigation to prove.','Help AST finds16/70 missing dedicated articles; actual generic fallback functions.','Two storefront CLI inputs still require catalog/translation fixtures, no fabricated commercial translation pass.','tenant_isolation_116 has20skip/0call, no functional credit.','HR whole suites were not rerun:3 selected old failures resolved separately.']})
nativef=save('Referinte_native_suplimentare_val04.json',{'utc':now(),'head':HEAD,'source':ref(a05f),'native_records':native_refs,'native_records_added_to_primary_6709':0,'executor_native_method_cases':4,'peer_native_method_cases':24,'peer_receipt':a05review,'do_not_sum_into_unique_case_total':True,'complete_PO_saves':0,'scope':'Șapte referințe iDempiere externe corpusului urmărit; nu schimbă numitorul sau probează10 surse EVA prin4 beforeSave.','native_lab_plan':{'source':ref(planf),'status':'PROPUS_NU_APROBAT_NU_EXECUTAT','dependency':'Clonă internă realizabilă, nu hardware extern.'}})
unmappedf=save('Cerintele_fara_alias_nou_val04.json',{'utc':now(),'HR':{'requirement':hr['nominal_requirement'],'evidence':ref(hr_file,'/nominal_requirement'),'result':'Proba funcțională este păstrată; T86 juridic și T187 tranzitiv nu primesc aceste teste automat.'},'UI':ui['observations'],'backend_extra':be['records'],'scope':'Rânduri de probe și cerințe funcționale, fără creare de IDuri comerciale sau atribuirea taskurilor doar din titluri.'})
delta_axis={a:counts['files_by_axis'][a]-prior['counts']['files_by_axis'][a]for a in counts['files_by_axis']}
summary={'utc':now(),'head':HEAD,'previous_handoff':ref(PREV/'Handoff_val_03.json'),'previous_manifest':ref(PREV/'MANIFEST_val_03.json'),'previous_A11':ref(previous_A11),
 'audited_revision_is_current_master':False,'new_HEAD_not_tested':latest['new_head'],'latest_population_and_HEAD_observation':ref(latestf),'live_checkpoint_of_audited_snapshot':prior['live_checkpoint'],'register':ref(reg),'task_matrix':ref(matf),'contracts':ref(pipef),'events':ref(evf),'suites':ref(sf),'native_refs':ref(nativef),'unmapped_requirements':ref(unmappedf),
 'counts':counts,'axis_difference_from_val03':delta_axis,'real_coverage_change':['8 surse de test noi,7 substituții UI și3 reprobe HR nominale;63 surse de suită, fără dublarea istoricului.','C67: toate4 suitele au observații separate,310 call passed; nu pretinde execuția comenzii combinate.','HR:27 cereri ASGI și5 controale SQL distincte de cele3 teste originale; identitatea contractuală HR rămâne neconfirmată.','N05:10 surse EVA citite,8 clase comparate cu JAR montat și4 beforeSave izolate;0 PO complet,0 ZK,0 Fact_Acct.'],
 'independent_supplements':reviewed,'scores':{'audit':None,'product':None},'A11_val04_pending':True,
 'limits':['17 contracte native rămân deschise.','1.206 evenimente passed și2 failed selectate nu sunt teste distincte ori criterii închise.','57 exit0/6 exit1 sunt ultimele snapshoturi ale programelor;2 dintre6 au numai reprobele HR selective, nu un exit nou de suită.','20skip fără credit se păstrează. V12/V13 interzic subprocess: textul origin despre Node era moștenit și este corectat prin erată.','Legăturile istorice R10 rămân la propriul commit. Nu s-au modificat taskuri, cod produs, cabinete sau rundele anterioare.','HR mirror nativ mock și proiecția PG minimală nu sunt execuție iDempiere.'],
 'resources':{'A12_product_executions':0,'A12_services_started':0,'A12_containers_created':0,'A12_active_resources':0,'production_writes':0,'producer_cleanup':'Conform recepțiilor sigilate, cu limitele de verificare indicate de fiecare.'},
 'inputs':list(inputs.values()),'manifest_receipts':manifest_receipts,'methods':[ref(Path(__file__)),ref(V/'build_val04.py')]}
report=save('Handoff_val_04.json',summary)
htmltext='<html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>R11 · Valul04</title><style>body{font:16px system-ui;max-width:1100px;margin:auto;padding:20px;line-height:1.5;overflow-wrap:anywhere}.table{overflow-x:auto}td,th{padding:8px;border-bottom:1px solid #ccd;text-align:left}table{border-collapse:collapse;width:100%}.note{background:#fff5d9;padding:12px}</style><h1>R11 · Valul04</h1><p>652 taskuri ·2.619 criterii ·6.709 fișiere.20 criterii din6 taskuri au observații parțiale;0 verdict integral.</p><p class="note">63 surse de suită distincte.7 reluări UI înlocuiesc probe vechi; HR schimbă doar3 cazuri. Nu confundați procesele, evenimentele pytest și cerințele.</p><ul>'+''.join('<li>'+html.escape(x)+'</li>'for x in summary['real_coverage_change'])+'</ul><h2>Probe și registre</h2><ul>'+''.join('<li><a href="'+p.name+'">'+html.escape(p.name)+'</a></li>'for p in [report,matf,sf,pipef,nativef,unmappedf])+'</ul><h2>Cele zece zone</h2><div class="table"><table><tr><th>Zona</th><th>Fișiere atribuite</th><th>Exercițiu parțial</th><th>Verdict integral</th></tr>'+''.join('<tr><td>'+o+'</td><td>'+str(v['assigned_files'])+'</td><td>'+str(v['exercise_scope_files'])+'</td><td>Deschis</td></tr>'for o,v in contracts['ten_zones'].items())+'</table></div><h2>Limite</h2><ul>'+''.join('<li>'+html.escape(x)+'</li>'for x in summary['limits'])+'</ul></html>'
idx=V/'index.html';assert not idx.exists();idx.write_text(htmltext,encoding='utf8')
qr=[json.loads(x)for x in gzip.decompress(reg.read_bytes()).decode().splitlines()]
qm=json.loads(matf.read_text(encoding='utf8'));qs=json.loads(sf.read_text(encoding='utf8'))
assert len(qr)==len({r['id']for r in qr})==6709 and len(qs['rows'])==63
assert sum(bool(c['R11_cases'])for c in qm['criterion_rows'])==20
for q in inputs.values():assert sha(B/q['path'])==q['sha256'],q['path']
qa=save('Verificare_val_04.json',{'utc':now(),'report':ref(report),'register':ref(reg),'matrix':ref(matf),'files':len(qr),'tasks':652,'criteria':2619,'unique_suite_sources':63,'selected_event_count':1259,'preserved_HR_suite_exit_not_forged':True,'evidence_pointers':sum(len(r['evidence'])for r in qr),'historical_task_hashes':len(verified),'input_sources_rehashed':len(inputs),'issues':[],'quality_grade':None})
man=save('MANIFEST_val_04.json',{'utc':now(),'head':HEAD,'algorithm':'SHA256','files':[ref(f)for f in sorted(V.rglob('*'))if f.is_file()],'self_reference':False})
for q in json.loads(man.read_text(encoding='utf8'))['files']:assert sha(B/q['path'])==q['sha256']
print(json.dumps({'manifest':ref(man),'report':ref(report),'QA':ref(qa),'counts':counts,'delta_axis':delta_axis},ensure_ascii=False))

