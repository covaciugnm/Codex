import sys,pathlib,hashlib,json,re,collections,datetime,importlib.machinery
z=importlib.machinery.SourceFileLoader('reg','D:/CodexWork/a05r8-register.py').load_module();z.build();out=z.out
j=z.j
full=set()
lookup={p['criterion']:p for p in z.results}
src=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102/idempiere/plugins/com.eva.ro.contab/test')
for row in z.results:
 ident,key,tid=row['criterion'],row['marker'],row['task']
 native=j(out/'Readback_native.json')['scenarios']
 if ident in native:z.add(row,'READBACK_SQL_SUR_CLONE',native[ident],'Readback_native.json')
 campaign=out/'T163_mutanti_LF'
 if tid=='T163' and key=='C-23':
  for rev in ('9980254afc','6df998aee0'):
   p=campaign/(rev+'.json');d=j(p);z.add(row,'ORIGINAL_GENERATOR_LF_JVM',{'rev':d['version'],'generator_rc':d['generator_rc'],'summary':dict(collections.Counter(x['verdict'] for x in d['mutants'])),'baseline':'GREEN at both refs; table covers 42 mutations plus original, in user-shaped private scratch. Historical Docker launcher adapted to local no-network JVM.'},p)
  z.add(row,'MUTANT_SCOPED_SEPARATE','rv1_apel_scos original has 2 targets at cutoff and cannot apply. Independent one-line mutation WInventarForm.valideaza line 1902, return 1 with 2 targeted FAILs, Git LF; no rewrite of original count.','T163_mutanti_LF/rv1-scoped.json')
 if tid=='T163' and key in ['C-20','C-21','C-24','C-19','C-31','C-18','C-27','C-29']:
  z.add(row,'ZK FOLLOWUP NON_TERMINAL','Trei reîncercări de intrare ZK în sesiuni noi, inclusiv GardenUser, s-au oprit înainte de fereastra ghidului (14 s). Fără efect nou; fiecare caz C-24/C-19/C-31 și celelalte ramuri rămâne deschis la nivelul ecranului. Prima rulare validă pentru C-13/C-14/C-17 este altă sesiune.','ui_t163_secondrole.json')
 if (tid,key)==('T163','C-13'):
  row['full_criterion_reexecuted']=True
 if tid=='T326' and key in ['K-14','K-23','K-18']:row['full_criterion_reexecuted']=True
 if tid=='T326' and key in ['K-06','K-08','K-11','K-17','K-19','K-26']:
  f=out/'JVM/TestListaPicking.txt'
  vals=[(i+1,s[:210]) for i,s in enumerate(f.read_text(encoding='utf8').splitlines()) if re.search(r'\b'+re.escape(key)+r'(?!\d)|LIPSA P3|validator|nevalidat',s,re.I)]
  if vals:z.add(row,'JVM_SUBTESTS_GUARDED',vals[:5],f)
 if tid=='T329' and key in ('C-6','C-7','C-12','C-13','RZ-7.1'):
  d=j(out/'T329_lots_nativ.json');z.add(row,'NATIVE_GARDENWORLD',{'ids':d['ids'],'cases':d['events'],'scope':'2 M_Lot + ASI; un M_InOut cu două poziții același produs același locator, transfer L1 patru unități, PI +1. Fără ecranul EVA Intrări și fără prețurile comparatoare în această probă; motor dezactivat aici.'},'T329_lots_nativ.json')
 if tid=='T329' and key=='C-7':
  d=j(out/'T329_engine-lot.json');z.add(row,'CONTRAPROBĂ_ACELAȘI_ARTICOL',{'doc':d['doc'],'resp':d['resp'],'before':d['before'],'after':d['after'],'gate':'tracking=Y, with MotorStraturi active input refused DR/N/N; previously same product when motor OFF accepted CO with +10 ASI=0. Route M_InOut receiving native REST. No assertion about EVA screen guard behavior with motor inactive.'},'T329_engine-lot.json')
 if tid=='T329' and key=='C-11':
  d=j(out/'T329_CMP.json');z.add(row,'COST_CMP_PE_ASI',{'observed':d['observed'],'strata':d['layer_detail'],'current_oracle':'CO, ieșire valorică 60,00. Scriptul pas0_cmp măsura vechiul T0 68,00 și a emis NU pentru acel etalon vechi. Proba curentă nu citește Fact_Acct pe documentul de consum din acest criteriu.'},'T329_CMP.json')
 if tid=='T329' and key=='RZ-7.1':row['full_criterion_reexecuted']=True
 if tid=='T323' and key=='RZ-1.3':row['full_criterion_reexecuted']=True
 if tid=='T330' and key=='C-24':
  d=j(out/'Matrice_T40.json');z.add(row,'DOCUMENTARY_REPLAY',{k:v['lines']['92'] for k,v in d.items()},'Matrice_T40.json');row['full_criterion_reexecuted']=True
 if tid=='T331' and key in ['RZ-9.1','RZ-9.2','RZ-9.4','RZ-9.6','RZ-9.8','RZ-9.10']:
  w=j(out/'T331_native_corrected.json')
  filt={'RZ-9.1':'NC inventory','RZ-9.2':'NC inventory','RZ-9.4':'NC (?:SO|PO|binding)','RZ-9.6':'registration','RZ-9.8':'NC inventory','RZ-9.10':'movement.*(PR|CO)'}[key]
  z.add(row,'NATIVE_PO/DOCACTION; SQL',{'events':[e for e in w['events'] if re.search(filt,e['case'])],'guarded_state':w['inventory_state'],'stock_and_GL':w['states'][-1],'scope':'New G1/G2 fixture, no ZK screenshots for these actions; CV→CV control IP→CO confirmed after restoring our exact three newly created scoped fixture sysconfig rows. Original first witness had missing-cost refusal and remains in T331_native.json.'},'T331_native_corrected.json')
 topic={'T331':('TestGestiuneNecontabila',{'RZ-9.1':'Fact|contabil','RZ-9.2':'refuzDocument','RZ-9.4':'refuzComanda','RZ-9.6':'marcare|demarcare','RZ-9.7':'fără pereche','RZ-9.8':'inventar|registru','RZ-9.9':'vârsta|31 de zile|29','RZ-9.10':'M_Movement|deplasare|refuzDocument'}),
 'T332':('TestArticolCostInitial',{'RZ-10.2':'setCurrentCostPrice|M_CostDetail','RZ-10.3':'straturi|fără document|fără strat','RZ-10.4':'existent|nu.*rescri'}),
 'T333':('TestAutentificareMobil',{'C-12':'E3|aplicatie','RZ-11.1':'hibrid|jeton','RZ-11.3':'E3|E4','RZ-11.4':'ensure'}),
 'T339':('TestT339ValidareWms',{'RZ-17.2':'costulPus|CMP|strat','RZ-17.4':'strat|metoda','RZ-17.5':'refac|strat'})}
 if tid in topic and key in topic[tid][1]:
  name,ds=topic[tid];f=out/'JVM_extra'/(name+'.txt');f=f if f.exists() else out/'JVM'/(name+'.txt')
  lines=f.read_text(encoding='utf8').splitlines();hits=[(i+1,v.strip()[:220]) for i,v in enumerate(lines) if re.search(ds[key],v,re.I) and re.search(r'(\bOK\b|^==)',v)]
  if hits:z.add(row,'JVM_EXACT_SUBCASES',hits[:6],f)
 if tid=='T327' and key in ['RZ-5.1','RZ-5.2','RZ-5.3']:
  name='TestT327Etichete';f=out/'JVM_service'/f'{name}.txt';js=(src/f'{name}.java').read_bytes();pat={'RZ-5.1':'ZXing|decode','RZ-5.2':'cifra de control|EAN13','RZ-5.3':'CatalogTiparire|T29Catalog'}[key]
  z.add(row,'JVM_GREEN_PLUS_TEST_SOURCE',{'assertion_locations':[(i+1,s.strip()[:200]) for i,s in enumerate(js.decode().splitlines()) if re.search(pat,s,re.I)][:5],'source_blob':hashlib.sha1(b'blob '+str(len(js)).encode()+b'\0'+js).hexdigest(),'total':'467 OK / 0 FAIL; not a scanner hardware or external complete export, individual per-case counts not printed.'},f)
 if tid=='T354' and key in ('C-2','C-9','C-10','C-11','C-14','C-22'):
  d=j(out/'T354_nativ_complet.json')[0]; hits=[s for s in d['lines'] if re.match(r'^CRIT '+re.escape(key)+r'(?:[a-d]?\s)',s)]
  assert hits
  z.add(row,'ORIGINAL_SUITE_33/33_GARDENWORLD',{'metrics':hits,'suite':d['last_safe'],'scope':'Input at staging boundary expressly seeded in the dedicated cabinet. No checkout/API C ingestion, UI and mobile not claimed; repro restores etichete.tsv at cutoff.'},'T354_nativ_complet.json')
  if key in ('C-2','C-9','C-10'):row['full_criterion_reexecuted']=True
 if tid=='T354' and key in ('C-1','C-6','C-24'):
  z.add(row,'ZK_HARNESS_T354_B_FAILED_PRECONDITION',j(out/'T354_B_retry.json'),'T354_B_retry.json')
 if tid in ('T323','T325','T326','T329','T330','T331','T341','T354') and key in ('K-20','K-29','K-32','C-16','C-21','C-25','RZ-4.3','RZ-19.3'):
  z.add(row,'SUITE_SUBSET_DISTINCT_FROM_EXPORT','Selected JVM test classes across three batches; R8 does not reproduce the two full contab/saga clean historical Docker exports, Jar parity or perf specified in this criterion.','JVM_index_progres.json')
 row['classification']='CRITERE_REJOUE_DOCUMENTAIRE' if row['full_criterion_reexecuted'] and tid in ['T329','T330'] and key in ['C-22','C-23','C-24','RZ-7.3','RZ-8.3'] else 'CRITERE_REJOUE' if row['full_criterion_reexecuted'] else 'COMPONENTE_EXECUTEE_RESTE_OUVERT' if row['observations'] else 'DOCUMENT_HISTORIQUE_SEUL' if row['historical_documents'] else 'NEEXECUTAT'
 row['classification']={'CRITERE_REJOUE_DOCUMENTAIRE':'REEXECUTAT_DOCUMENTAR','CRITERE_REJOUE':'REEXECUTAT','COMPONENTE_EXECUTEE_RESTE_OUVERT':'COMPONENTĂ_REEXECUTATĂ_REST_NEEXECUTAT','DOCUMENT_HISTORIQUE_SEUL':'NUMAI_DOCUMENT_ISTORIC'}[row['classification']] if row['classification']!='NEEXECUTAT' else row['classification']
 row['verdict']='DIVERGENȚĂ_DOCUMENTARĂ_REPRODUSĂ' if row['classification']=='REEXECUTAT_DOCUMENTAR' else 'DIVERGENȚĂ_ISTORIC_VS_CURENT' if row['full_criterion_reexecuted'] and (tid,key) in [('T163','C-6'),('T333','C-24')] else 'CONFIRMAT_LA_NIVELUL_DECLARAT' if row['full_criterion_reexecuted'] else 'PARȚIAL_FĂRĂ_VERDICT_INTEGRAL' if row['observations'] else 'NEEXECUTAT'
 row['remaining']=None if row['full_criterion_reexecuted'] else row['remaining']
 row['role_review']='GardenAdmin/rol 102, firmă și organizație 11, operatori comerciali sintetici la procesele T326/T354 ori JVM fără utilizator, după nivelul probei. Actorul exact este în logul nominal. Nicio identitate de producție.'
 row['next_exact']=None if row['full_criterion_reexecuted'] else rawnext if (rawnext:=next(x for x in z.qs if x['criterion']==ident)['next']) else None
for f in ['Restituire_R8.txt','T331_native.json','T331_native_corrected.json','T329_CMP.json','T329_engine-lot.json','T354_nativ_initial.json','T354_nativ_complet.json','T354_B_initial.json','T354_B_retry.json','T163_nativ_initial.json','Executie_scripturi_originale.json','Reper_istoric.json','JVM_service/index.json','JVM_extra/index.json','T163_mutanti_LF/9980254afc.json','T163_mutanti_LF/6df998aee0.json','T163_mutanti_LF/rv1-scoped.json','T163_mutanti_LF/rv1-scoped.log','ui_t163_extra2.json','ui_follow_progress.json']:
 z.ev(f)
for f in (out/'zk_r8').glob('*.png'):z.ev(f)
assert all(len(t['historical_documents'])>0 or t['observations'] for t in z.results)
assert 'remaining_owned_containers=0' in (out/'Restituire_R8.txt').read_text(encoding='utf-8-sig')
rowmap={k:[v['criterion'] for v in z.results if v['classification']==k] for k in set(v['classification'] for v in z.results)}
doc={'schema':'eva.audit.R8.A05.nominal.v1','submitted_utc':z.utc(),'reviewer':'A11','zone':'A05','source_cutoff':z.cut,'queue_sha256':z.sha(z.queue),'batch':135,'ledger_base':'EVA accounting 6df998a; native backend installed r57 in privately registered GardenWorld (test-only). Cross-version source hashes and references per row.','manifest_paths_relative_to_audit_root':True,'counts':{k:len(v) for k,v in sorted(rowmap.items())},'task_counts':dict(collections.Counter(r['task'] for r in z.results)),'results_by_kind':rowmap,'score':None,'rows':z.results,'proofs':dict(sorted(z.refs.items())),'warnings':['Original T163 C-6 at its integration 0, at cutoff 3; later WInventarForm changes must not be retro-attributed to T163. T333 C-24 zero writer policy at skeleton differs from the active mobile journal.','T329/T330 matrix 3.09/4.19 retains ❌ in checked Git versions; this contradicts the documentary acceptance target, not the successful receipt, FEFO or CMP behavior.','T329 tagged article with tracking Y accepted ASI0 in an actual receipt with strata engine OFF; same article and document type refused ASI0 in DR with engine active. Frontend Intrări policy not inferred.','T163 original mutant generator: at integration 42 killed, baseline green. Current version 41 killed and one duplicate anchor unresolved in original runner. A separate method-scoped replay killed RV1. Only canonical LF camp counted; first Windows results retained as harness diagnostics.','T354 source suite 33/33 includes a signed-in synthetic staging→ERP route. The EX05 checkout case was a different external UUID. Receipt/storno, physical scanner, cross-role or FE/DocAction results are distinguished.','Some historical dossiers and probes refer to q31/CESIRO or full old Docker exports. GardenWorld IDs are synthetic. No promotion to full across different roles, baseline, products, languages or external integration.'] ,'laboratory':'Only owned clonal resources; 0 containers and networks on cleanup. §40 occupation and §61 suite slot released. No code/product or production DB changes.'}
target=out/'Registru_nominal_final_A05.json'
with target.open('x',encoding='utf8',newline='\n') as f:json.dump(doc,f,ensure_ascii=False,indent=2);f.write('\n')
for p,h in doc['proofs'].items():assert z.sha(z.base/p)==h,p
assert len(set(x['criterion'] for x in doc['rows']))==135
print(z.sha(target),doc['counts'],len(doc['proofs']))
