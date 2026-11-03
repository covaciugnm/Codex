from build_val03 import *
import html
n02file=O/'A11/Verdict_A11_R11_N02_V10_v1.json'
n02=source(n02file,'453728e98ac5adefc3d94315128309972d2be1393b0bcaf75042cf3b25179de1')
source(O/'A11/Sigiliu_A11_R11_N02_V10_v1.json','e2a9656767bf98f49501c1476216176129445c9fb4424ee6fe306fa7a5d02487')
for group in ['inputs','proofs','reproduction_methods']:
 for q in n02[group]:source(B/q['path'],q['sha256'])
for s in suite_rows:
 s['independent_consolidation_review']=ref(n02file)
 if s['new_execution_for_val03']:s['review_state']='A11_ACCEPTA_COMPONENTA_CU_CORECTII_N02_C01_C02_C03'
sunique={(s['file'],e['id'],e['stage'])for s in suite_rows for e in s['reported_events_original']}
assert len(sunique)==1128 and sum(phase_totals.values())==1134
runtime_limit='Originale T58 inspectate; Node nu este sandbox OS și nu blochează exhaustiv rețeaua: UDP local controlat a trecut; selecția JS folosește markeri textuali, nu hash. Nicio autorizație pentru programe necunoscute.'
candidatef=V/'semantic_task_map_candidate.json'
cand=source(candidatef,'456df86c8f992ae076b8da03db4a90be421320dac411ea2603e113cfae88fe76')
assert len(cand['candidate_mappings'])==8
for q in cand['sources'].values():source(B/q['path'],q['sha256'])
frozen=[]
for name,r in cand['original_product_sources_verified'].items():
 p=Path(r['read_only_source_path']);data=p.read_bytes()
 assert hashlib.sha256(data).hexdigest()==r['sha256']
 assert hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest()==r['git_blob']
 assert R[name]['git_oid']==r['git_blob']
 out=V/'sources'/name;out.parent.mkdir(parents=True,exist_ok=True)
 if out.exists():assert out.read_bytes()==data
 else:out.write_bytes(data)
 frozen.append({'file':name,'git_oid':r['git_blob'],'frozen_bytes':ref(out),'origin':r['read_only_source_path']})
 add(name,candidatef,'/original_product_sources_verified/'+name.replace('~','~0').replace('/','~1'),'A12',['inspected'],'Lectura sursei și identitatea Git pentru asocierea semantică, fără execuție nouă.',{'sha256':r['sha256'],'git_oid':r['git_blob']},'Importarea unui fișier nu este credit pentru toate funcțiile.')
for i,f in enumerate(cand['executed_or_read_fragments']):
 name=f['file'];r=cand['original_product_sources_verified'][name]
 raw=Path(r['read_only_source_path']).read_bytes().decode('utf8').splitlines(keepends=True)
 piece=''.join(raw[f['line_start']-1:f['line_end']]).encode()
 assert hashlib.sha256(piece).hexdigest()==f['fragment_sha256_utf8_lines_including_original_newlines'],f['symbol']
 ax=['inspected']if f['symbol'].startswith('translation keys')else['inspected','exercised']
 add(name,candidatef,'/executed_or_read_fragments/'+str(i),'COORDONATOR',ax,'A12 a legat fragmentul exact la aserțiunile originale și evenimentele V10; nu o nouă rulare.',f,{'limit':f['precise_limit'],'A11_receipt':ref(n02file),'runtime_limit':runtime_limit})
newlinks=[]
bycriteria={r['criterion']:r for r in matrix['criterion_rows']}
def controlref(x):
 q=cand['sources'][x['source']];f=B/q['path'];j=source(f,q['sha256']);r=ptr(j,x['pointer'])
 assert r['id']==x['original_test_id']and r['stage']==x['reported_stage']and r['outcome']==x['reported_outcome']
 return ref(f,x['pointer'])
for i,m in enumerate(cand['candidate_mappings']):
 cid=m['criterion_id_original'];old=bycriteria[cid]
 assert old['requirement_original']==m['normative_content_exact']and old['task']=='T58'and old['canonical']is None
 assert not old['R11_cases']
 ppos=[controlref(x)for x in m['positive_control']]
 pneg=[controlref(x)for x in m['negative_control']]
 proofs=[ref(candidatef,'/candidate_mappings/'+str(i)),ref(n02file,'/T58_nominal_credit')]+ppos+pneg
 proofs=list({(p['path'],p['pointer']):p for p in proofs}.values())
 caseid='R11V3.T58.'+m['plan_label_original']
 case={'case':caseid,'criteria':[cid],'proofs':proofs,'files':[{'id':R[n]['id'],'path':n,'git_oid':R[n]['git_oid'],'owner':R[n]['owner'],'peer':R[n]['peer']}for n in cand['original_product_sources_verified']if n not in ['backend/tests/conftest.py','backend/tests/fixtures/samanta_l6j.py']],
 'actor':m['probe_actor'],'entry_native_or_adapter':'FastAPI TestClient / client iDempiere simulat / fișier JSON temporar + SQLite; JS extras în Node pentru portal. Numai funcțiile/liniile din semantic_task_map_candidate.',
 'expected_for_this_case':m['oracle_asserted_by_original_tests'],'observed':m['actual_effect_supported_by_source_assertions_and_reported_events'],
 'positive':ppos,'negative':pneg,'negative_missing':len(pneg)==0,'limitation':m['limits']+[m['effect_evidence_limit'],runtime_limit],
 'native_ERP_executed':False,'result_at_scope':'OBSERVATIE_COMPONENTA_L1_B_PARTIALA','whole_task_verdict':None,'complete_pipeline':False,
 'A11_receipt_component_only':ref(n02file),'scope_of_original_task':m['subcondition_mapped']}
 matrix['cases'].append(case);old['R11_cases'].append(caseid);old['R11_status']='OBSERVATIE_LA_SUBCONDITIA_EXPLICITA';old['R11_oracle_complete']=False
 link={'case':caseid,'task':'T58','canonical':None,'criterion':cid,'expected_original':m['normative_content_exact'],'normative_record':old['baseline'],
 'proofs':proofs,'result_in_R11':case['result_at_scope'],'claim':m['subcondition_mapped'],'limit':case['limitation'],
 'previous_R10_result':old['R10_result_historical'],'R10_is_current_verdict':False,'A11_nominal_acceptance':'Val_03 în așteptarea controlului matricii; N02 recepționează numai componenta.'}
 matrix['nominal_links'].append(link);newlinks.append(link)
for t in matrix['task_rows']:
 cs=[c for c in matrix['criterion_rows']if c['task']==t['task']]
 t['R11_direct_cases']=sorted({i for c in cs for i in c['R11_cases']})
 t['R11_linked_criteria']=[c['criterion']for c in cs if c['R11_cases']]
 assert t['whole_task_current_verdict']is None
matrix.update({'utc':now(),'previous_matrix':ref(PREV/'Matrice_criterii_task_probe.json'),'Val03_new_links':len(newlinks),'Val03_independent_reviews':reviews,'score':None})
# Preserve the pending contracts verbatim. T58 L1-B is context for D16, never its native execution.
contracts['utc']=now();contracts['previous']=ref(PREV/'Contracte_17_si_capitole.json')
contracts['A11_partial_reviews'].extend(reviews)
contracts['Val03_note']='L1-B T58 confirmă interfața cu verdict simulat; nu se atribuie automat contractului D16 cu două scheme și documente native.'
for c in contracts['contracts']:
 c['Val03_review_sources']=[ref(verdict)]if c['id']in['D01','D06','D07','D09','D11','D12','D15']else[]
 c['Val03_acceptance_complete']=False
 if c['id']=='D16':c['Val03_context_only']=ref(candidatef,'/explicit_rejections')
for ch in contracts['chapters']:
 ts=[t for t in matrix['task_rows']if t['chapter']==ch['chapter']]
 ch['with_R11_direct_observation']=sum(bool(t['R11_direct_cases'])for t in ts)
 ch['linked_criteria']=sum(len(t['R11_linked_criteria'])for t in ts)
for owner,v in contracts['ten_zones'].items():
 v['content_inspected_files']=sum(r['owner']==owner and r['axis']['inspected']!='UNVERIFIED'for r in R.values())
 v['exercise_scope_files']=sum(r['owner']==owner and r['axis']['exercised']!='UNVERIFIED'for r in R.values())
 v['Val03_new_events']=sum(r['owner']==owner for ev in events for r in [R[ev['path']]])
 v['Val03_new_domain_execution_by_A12']=False
progress=[]
for i,n in enumerate(chk['priority']):
 state='DESCHIS_FARA_EXECUTIE_NATIVA_NOUA';extra=[]
 if n['id']=='N01':state='INTEGRAT_CU_LIMITAREA_FIECAREI_CONSTATARI';extra=[ref(verdict),ref(peer)]
 if n['id']=='N02':state='RECEPTIE_COMPONENTE_CU_TREI_CORECTII_EXPLICITE';extra=[ref(n02file),ref(confile)]
 if n['id']=='N12':state='EXTINS_8_SUBCONDITII_T58;RECEPTIE_NOMINALA_VAL03_IN_ASTEPTARE';extra=[ref(candidatef)]
 progress.append({**n,'source':ref(chkf,'/priority/'+str(i)),'state':state,'evidence':extra,'complete_native_objective':False})
gate_rows=[]
for i,g in enumerate(chk['mandatory_gates']):
 status='PARTIAL_LA_PROBELE_LINKATE_NU_GLOBAL'
 if g['id']=='G10':status='MATRICE_VAL03_DEPUSA_SPRE_VERIFICARE_INDEPENDENTA'
 gate_rows.append({**g,'source':ref(chkf,'/mandatory_gates/'+str(i)),'status':status,'whole_audit_pass':False})
# Exact references in both directions, all previous scope and identities preserved.
for r in R.values():
 assert r['candidate']==HEAD and r['file_verdict']is None
 for e in r['evidence']:
  j=source(B/e['source_file'],e['source_sha256']);ptr(j,e['pointer'])
for link in matrix['nominal_links']:
 assert link['case']in bycriteria[link['criterion']]['R11_cases']
 for pr in link['proofs']:ptr(source(B/pr['path'],pr['sha256']),pr.get('pointer',''))
for row in matrix['criterion_rows']:
 for ci in row['R11_cases']:assert any(l['criterion']==row['criterion']and l['case']==ci for l in matrix['nominal_links'])
def taskhash(t):
 d=t['historical_dossier'];assert sha(B/d['file'])==d['sha256'];return t['task']
with ThreadPoolExecutor(max_workers=8)as pool:verified_tasks=list(pool.map(taskhash,matrix['task_rows']))
for r in inputs.values():assert sha(B/r['path'])==r['sha256']
# The eight scoped mappings increase the number of links, not whole criteria acceptance.
linked=sum(bool(c['R11_cases'])for c in matrix['criterion_rows']);tasklinked=sum(bool(t['R11_direct_cases'])for t in matrix['task_rows'])
assert linked==20 and tasklinked==6 and len(matrix['criterion_rows'])==2619 and len(matrix['task_rows'])==652
outreg=V/'Registru_6709_val_03.jsonl.gz';assert not outreg.exists()
with outreg.open('wb')as f:
 with gzip.GzipFile(fileobj=f,mode='wb',filename='',mtime=0)as gz:
  for r in R.values():gz.write((json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n').encode())
matf=save('Matrice_criterii_task_probe_val03.json',matrix)
pipef=save('Contracte_17_si_capitole_val03.json',contracts)
evf=save('Evenimente_val_03.json',{'utc':now(),'head':HEAD,'previous':ref(PREV/'Registru_6709_val_02.jsonl.gz'),'new_events':events,'distinct_files':len({e['path']for e in events}),'no_whole_file_verdict':True})
sf=save('Reconciliere_55_suite_val03.json',{'utc':now(),'head':HEAD,'consolidation':ref(confile),'rows':suite_rows,'program_count':55,'exit_counts':{'0':43,'1':12},'phase_reported_events':dict(phase_totals),'raw_event_count':1134,'distinct_file_nodeid_phase':1128,'counts_are_not_distinct_tests':True,'mandatory_corrections':n02['mandatory_interpretation_corrections'],'independent_receipt':ref(n02file),'runtime_limit':runtime_limit,'V7_preserved':True,'V10_replaces_only_one_suite':True,'excluded_followups':['V11','V12']})
cf=save('Checklist_val03.json',{'utc':now(),'source':ref(chkf),'priority':progress,'mandatory_gates':gate_rows,'remaining_contracts':chk['remaining_contracts'],'all_contracts_complete':False,'A11_val03_review_pending':True})
ff=save('Surse_T58_fixate.json',{'utc':now(),'head':HEAD,'files':frozen,'method':'Octeți păstrați, SHA256 și SHA1 Git blob recalculate. Fișierele produsului nu au fost modificate.','compiled_or_executed_here':False})
counts={'files':6709,'tasks':652,'criteria':2619,'linked_partial_criteria':linked,'tasks_with_partial_links':tasklinked,'new_criterion_links':8,'full_task_verdicts':0,'full_file_verdicts':0,'new_events':len(events),'new_event_distinct_files':len({e['path']for e in events}),'files_by_axis':{a:sum(r['axis'][a]!='UNVERIFIED'for r in R.values())for a in next(iter(R.values()))['axis']}}
deltacount={a:counts['files_by_axis'][a]-prior['counts']['files_by_axis'][a]for a in counts['files_by_axis']}
summary={'utc':now(),'head':HEAD,'previous_handoff':ref(PREV/'Handoff_val_02_v2.json'),'previous_manifest':ref(PREV/'MANIFEST_val_02_v2.json'),'previous_A11':ref(checkpoint),'live_checkpoint':ref(delta),
 'register':ref(outreg),'task_matrix':ref(matf),'contracts':ref(pipef),'events':ref(evf),'suites':ref(sf),'checklist':ref(cf),'frozen_sources':ref(ff),'semantic_review':ref(candidatef),
 'counts':counts,'axis_difference_from_val02':deltacount,'real_coverage_change':['Lot04 adaugă recepția a9 constatări și doi martori independenți; nu nouă taskuri ori nouă defecte noi.','T58:8 criterii originale legate la fragmente API/JS cu ERP simulat; niciun criteriu nou sau închidere de task.','Suite55: T58 V10 substituie o singură înregistrare; +6 evenimente call passed, -4 call failed, -2 setup skipped; fără dublarea V7.'],
 'scores':{'audit':None,'product':None},'A11_val03_pending':True,'independent_supplements':[ref(verdict),ref(peer),ref(n02file)],
 'limitations':['652 fișe istorice au propriul commit și nu devin verdictul candidatului nou.','20skip la izolare rămân fără credit funcțional.','Evenimentele pytest/subtestele nu reprezintă teste distincte.','Node are limita UDP/markeri documentată; recepția este numai pentru sursele originale inspectate.','T58 L1-B nu certifică ZK/GL_Journal/Fact_Acct ori D16; C67 nu are toate cele4 suite cerute.','17 contracte rămân deschise. V11/V12 ulterioare nu sunt incluse.'],
 'resource_state':{'new_product_tests_launched_by_A12':0,'containers_created':0,'local_databases_created':0,'services_started':0,'production_writes':0,'active_A12_resources':0,'work':'Lectură, verificare hash/proveniență și scriere numai în Val_03.'},'inputs':list(inputs.values()),'historical_sha_verified':652,'method':ref(Path(__file__)),'constructor':ref(V/'build_val03.py')}
report=save('Handoff_val_03.json',summary)
# Responsive human-readable index, linked to the exact frozen JSONs.
text='<html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>R11 · Valul03</title><style>body{font:16px system-ui;max-width:1100px;margin:auto;padding:20px;color:#193047;line-height:1.5;overflow-wrap:anywhere}h1,h2{line-height:1.2}.table{overflow-x:auto}table{border-collapse:collapse;width:100%}th,td{padding:8px;border-bottom:1px solid #ccd;text-align:left}a{color:#075e99}.notice{border-left:4px solid #da8;padding:12px;background:#fff9e9}</style><h1>R11 · Valul03</h1><p>652 taskuri · 2.619 criterii · 6.709 fișiere. Revizie separată, fără modificarea valului02.</p><p class="notice">20 criterii din6 taskuri au observații parțiale. Nu există verdict integral de task/fișier; recepția A11 a matricei Val03 este în așteptare.</p><h2>Ce s-a adăugat</h2><ul>'+''.join('<li>'+html.escape(x)+'</li>'for x in summary['real_coverage_change'])+'</ul><h2>Documente</h2><ul>'+''.join('<li><a href="'+p.name+'">'+html.escape(p.name)+'</a></li>'for p in [report,matf,pipef,sf,cf,ff,candidatef])+'</ul><h2>Cele zece zone</h2><div class="table"><table><tr><th>Zona</th><th>Fișiere alocate</th><th>Cu exercițiu parțial</th><th>Stare</th></tr>'+''.join('<tr><td>'+o+'</td><td>'+str(v['assigned_files'])+'</td><td>'+str(v['exercise_scope_files'])+'</td><td>Restul metodelor/fluxurilor rămâne deschis</td></tr>'for o,v in contracts['ten_zones'].items())+'</table></div><h2>Limite</h2><ul>'+''.join('<li>'+html.escape(x)+'</li>'for x in summary['limitations'])+'</ul><p>Git: '+HEAD+'</p></html>'
idx=V/'index.html';assert not idx.exists();idx.write_text(text,encoding='utf8')
# Readback uses serialized outputs, never in-memory map cardinality.
q=[json.loads(x)for x in gzip.decompress(outreg.read_bytes()).decode().splitlines()]
qm=json.loads(matf.read_text(encoding='utf8'))
assert len(q)==len({r['id']for r in q})==len({r['path']for r in q})==6709
assert sum(bool(c['R11_cases'])for c in qm['criterion_rows'])==counts['linked_partial_criteria']
assert sum(bool(t['R11_direct_cases'])for t in qm['task_rows'])==counts['tasks_with_partial_links']
qa=save('Verificare_val_03.json',{'utc':now(),'report':ref(report),'register':ref(outreg),'matrix':ref(matf),'files':len(q),'tasks':len(qm['task_rows']),'criteria':len(qm['criterion_rows']),'new_links':len(newlinks),'source_files_hashed':len(inputs),'prior_manifest_members':checks,'evidence_pointer_count':sum(len(r['evidence'])for r in q),'historical_dossiers_hash_verified':len(verified_tasks),'issues':[],'score':None,'scope':'Integritate și trasabilitate; calitatea independentă a Val03 rămâne de recepționat A11.'})
man=save('MANIFEST_val_03.json',{'utc':now(),'head':HEAD,'algorithm':'SHA256','files':[ref(p)for p in sorted(V.rglob('*'))if p.is_file()],'self_reference':False})
for r in json.loads(man.read_text(encoding='utf8'))['files']:assert sha(B/r['path'])==r['sha256']
for r in inputs.values():assert sha(B/r['path'])==r['sha256']
print(json.dumps({'manifest':ref(man),'report':ref(report),'QA':ref(qa),'counts':counts,'axis_delta':deltacount},ensure_ascii=False))

