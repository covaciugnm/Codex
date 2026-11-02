import pathlib,hashlib,json,collections,concurrent.futures,datetime,re
O=pathlib.Path(__file__).parent;E=O.parent;F=E/'R4';R=E.parent
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fh(p):x=p.read_bytes();return hashlib.sha256(x).hexdigest(),json.loads(x.decode('utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=1,default=str)+'\n',encoding='utf8')
rep=rd(F/'A12_raport.json'); catalog=rd(F/'Dovezi_criterii.json');acts=rd(F/'Registru_1868.json'); before=rd(E/'A11_ledger_652_R3.json'); old={r['task']:r for r in before['cases']};r3={x['task']:x for x in rd(E/'R3/A12_raport.json')['records']};assert set(old)==set(r3)=={t['task'] for t in rep['records']} and len(old)==652
for name,sha in [('A12_raport.json','a81a12d23f080685a21690fba2377948fa3a9c7823022ebb55959bdf141583ab'),('Dovezi_criterii.json','08993eda3a2777eaf80c531ecb04fa60cc6a886895e32e373b2b7cfefc594fbd'),('Registru_1868.json','ef764ed18874939b45c17fecdf824afec9d535f1aee6d19de679c789273beab6'),('Verificare_R4.json','ca27cf3f90727d5d807c846354d3be15193b8583d2f0438406299fb082717749')]:assert h(F/name)==sha
ev=catalog['evidence'];reverse={(eid,v['task'],v['criterion'],v['relation'])for eid,li in catalog['inverse_task_requirement_links'].items() for v in li}; action={a['criterion']:a for a in acts['records']};assert len(action)==len(acts['records'])==1868
def classification(c):
 s=c['current']['status'];k=c['kind']
 if s=='PASS_DOVEDIT':return 'DOCUMENTAR_ADMIN' if k=='DISPOZIȚIE_ADMINISTRATIVĂ' else 'DOCUMENTAR_REFERINȚĂ' if k=='CONTROL_DISPOZIȚIE_REFERINȚE' else 'REVERIFICARE_PASS'
 if s=='PASS_NATIV_PE_ORACOLUL_LITERAL':return 'FUNCȚIONAL_LITERAL_CURENT'
 if s=='PASS_PROBĂ_LITERALĂ_CURENTĂ':return 'TEST_PUBLIC_LITERAL_CURENT'
 if s=='ȚINTĂ_DOCUMENTARĂ_NESATISFĂCUTĂ':return 'DEFECT_ȚINTĂ_DOCUMENTARĂ'
 if 'CONTRAEXEMPLU_' in s:return 'CONTRAEXEMPLU_SECVENȚĂ_AUTORIZARE'
 if s=='PROBĂ_NATIVĂ_MULTISTADIU_LIMITATĂ':return 'NATIV_MULTIETAPĂ_LIMITAT'
 if s=='PARȚIAL_ANDROID_POST_R3':return 'ANDROID_SEGMENT'
 if 'NATIV' in s and s!='NEEXECUTAT':return 'NATIV_SEGMENT'
 if s in ('NEEXECUTAT','INCONCLUDENT','BLOCAT_ACCES'):return s
 if 'METADATE' in s:return 'METADATE_NUMAI'
 if 'DOCUMENTAR' in s or 'ISTORIC' in s or 'ARTEFACT' in s or 'PROVENIENȚĂ' in s or 'INSTALARE' in s and s.startswith('DOVEDIT_'):return 'DOCUMENT/PROVENIENȚĂ_CONFORM_LIMITĂ'
 if s in ('FAIL_DOVEDIT','FAIL_DOVEDIT_LA_NIVEL_COMPONENTĂ'):return 'DISCREPANȚĂ_ADMIN' if k=='DISPOZIȚIE_ADMINISTRATIVĂ'else 'DEFECT_COMPONENTĂ'
 return 'SEGMENT_CALIFICAT'
def audit(t):
 q=t['task'];sha,j=fh(F/t['file']); b3,j3=fh(E/'R3'/r3[q]['file']);assert sha==t['sha256'] and b3==t['R3_sha']==old[q]['sha_R3'] and h(F/t['html'])==t['html_sha256'];assert j['A11_score_R4'] is None
 oldc=j3['operative_criteria_and_audit_criteria']+j3['R3_new_criteria']; prior={c['id']:c for c in oldc}; current=j['operative_criteria_and_audit_criteria']+j['R3_new_criteria']+j['R4_new_criteria']; assert len(current)==len({c['id']for c in current})==t['checks'];assert set(prior)<={c['id']for c in current}; oids={c['id'] for c in oldc if c['current']['status']=='NEEXECUTAT'};assert oids==set(j['R4_first_1868_action_ids']); assert len(j['R4_control_register'])==36
 links=set(); decisions=[]; grades=set(old[q]['earned_R3_subcheck_ids']); external=0; pendingexternal=0; currentstatus=collections.Counter();cats=collections.Counter(); actionissues=[];nreused=0
 for c in current:
  id=c['id'];curr=c['current'];s=curr['status'];cx=classification(c); cats[cx]+=1;currentstatus[s]+=1; quals=[(c['source_evidence_id'],'source')]+[(x,'authority')for x in c.get('authority_evidence_ids',[])]
  for phase in ('closure','current'):
   vv=c[phase];assert not vv.get('observed') or vv['evidence_ids'],(q,id,phase);quals.extend((x,phase) for x in vv['evidence_ids'])
  for field,prop,tag in [('component_assertion_crosscheck','ids','component_candidate'),('cross_financial_observation','evidence_ids','financial_context'),('installed_schema_probe','ids','metadata_context'),('archive_criterion_output','ids','historic_artifact_context')]:
   vals=(c.get(field)or{}).get(prop,[]);quals.extend((x,tag)for x in vals)
  for eid,rel in quals:assert eid in ev;links.add((eid,q,id,rel))
  nreused+=str(c['expected_oracle']).strip()==str(c['normative_content']).strip()
  edge=action.get(id);summary=None
  if id in oids:
   assert edge and edge['task']==q and edge['original_NEEXECUTAT_R3'] and edge['current_disposition']==s and edge['expected_verbatim']==c['expected_oracle'] and edge['source_location'] and edge['steps'] and edge['negative_or_counterexample']
   ext=edge['requires_external_or_hardware'];assert ext==edge['resource_split']['requires_external_or_hardware'];external+=ext;pendingexternal+=bool(ext and s=='NEEXECUTAT')
   summary={'owner':edge['zone_owner'],'resource':edge['resource_split']['classification'],'external_portion':ext,'current_disposition':s,'next':str(edge['individual_dependency'])[:300]}
  decisions.append({'id':id,'kind':c['kind'],'status':s,'closure_status':c['closure']['status'],'A11_scope':cx,'current_evidence':curr['evidence_ids'],'source':c['source_evidence_id'],'first_1868_action':summary,'was_new_R4':id not in prior,'prior_status':prior[id]['current']['status'] if id in prior else None})
 assert sum(currentstatus.values())==t['checks'];assert currentstatus['NEEXECUTAT']==t['unexecuted_current']
 if j['R4_new_criteria'] and all(c['source_evidence_id'] for c in j['R4_new_criteria']):grades.add('QC02-R4')
 if q in ('T352','T366','T257','T259','T07.03','T08.03','T10.04','T10.06','T36.53','T333','T334'):grades.add('QC10-R2')
 if q=='T259':
  assert len(current)==2 and all(c['current']['status']=='PASS_NATIV_PE_ORACOLUL_LITERAL' and c['closure']['status']=='PROBĂ_BROWSER_ISTORICĂ_VERIFICATĂ'for c in current)
  grades.update(['QC02-R1','QC02-R2','QC02-R3','QC03-R1','QC03-R2','QC03-R5','QC04-R1','QC05-R1','QC08-R1','QC08-R2','QC08-R4','QC09-R1','QC09-R2','QC09-R5','QC10-R3'])
 if q=='T352':grades.add('QC01-R5')
 if q in ('T07.03','T08.03','T10.06','T10.04'):grades.add('QC02-R4')
 if q in ('T366','T257','T333','T334'):grades.update(['QC09-R2','QC08-R2'])
 nextitems=[]
 if q=='T259':nextitems.append('Cele două obiective literale ale fișei au rezultate pozitive la versiunea curentă; testul browser original și rezultatul istoric separat sunt demonstrate. Aceasta nu certifică toate funcțiile sau toate rolurile modulului Contracte.')
 if q=='T352':nextitems.append('Distingeți N calcul conform, contribuție Y absentă din calculatorul Git, T352 lipsă pe cele cinci JAR montate. Handoff extern EX încă neexecutat în această versiune.')
 if q=='T257':nextitems.append('Operația reală L8/L12/guard este probată pe import sintetic; schema secundară pierdută cere oracol de politică. Alte tipuri și căi G1–G6 nu sunt validate prin această singură factură.')
 if q in ('T333','T334'):nextitems.append('Pentru rol doar citire comparați cheia existentă 409 vs cheia nouă 403: se observă ordinea guard-ului, nu s-a observat divulgarea valorilor ori o scriere nouă.')
 if q=='T366':nextitems.append('Validarea pe articol/retry/storno și pereche G1/G2 sunt segmente native. Închideți destinațiile de cost și lanțul operatorului pe documentele proprii.')
 if q=='T08.03':nextitems.append('79 fișiere TSV încă au marcajul de ciornă; confirmarea istorică a consultantului și starea documentară rămân distincte.')
 if currentstatus['NEEXECUTAT']:nextitems.append('Reexecutare la intrarea nominală pentru '+', '.join(d['id']for d in decisions if d['status']=='NEEXECUTAT')+'.')
 if not nextitems:nextitems.append('Confirmați separat criteriile funcționale/documentare și urmele istorice; efectele componentei nu se extind în afara versiunii și ariei testate.')
 return {'task':q,'canonical':t['canonical'],'title':t['title'],'R3_hash':b3,'R4_hash':sha,'R4_html_hash':t['html_sha256'],'R3_score':old[q]['R3_quality_score'],'R4_quality_score':len(grades)/5,'verified_subchecks':sorted(grades),'task_quality_gate':'PARȚIAL_DE_REAUDITAT','all_literal_current_functional_criteria_pass_for_complete_case':q=='T259','all_criteria':decisions,'tier_counts':dict(cats),'statuses':dict(currentstatus),'external_original1868':external,'external_of_open_original1868':pendingexternal,'oracle_equals_requirement':nreused,'next':nextitems},links
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as pool:runs=list(pool.map(audit,rep['records']))
rows=[r[0]for r in runs];fwd=set().union(*(r[1]for r in runs));assert fwd==reverse and len(fwd)==7274
ss=collections.Counter();cc=collections.Counter();hist=collections.Counter();extra=pendext=0; actdone=collections.Counter()
for r in rows:
 ss.update(r['statuses']);cc.update(r['tier_counts']);hist[str(r['R4_quality_score'])]+=1;extra+=r['external_original1868'];pendext+=r['external_of_open_original1868']
 for c in r['all_criteria']:
  if c['first_1868_action']:actdone[c['status']]+=1
assert sum(ss.values())==2619 and ss['NEEXECUTAT']==1713 and len(action)==sum(actdone.values())==1868 and extra==52 and pendext==48
v={'reviewer':'A11','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'report_sha256':h(F/'A12_raport.json'),'R3_ledger_sha256':h(E/'A11_ledger_652_R3.json'),'R4_catalog_sha256':h(F/'Dovezi_criterii.json'),'R4_1868_sha256':h(F/'Registru_1868.json'),'records':len(rows),'complete_quality_10_records':0,'all_current_literal_case_positives':['T259'],'quality_score_rule':'Punctaj cumulativ per fișa individuală pentru subcontroalele cu dovezi. Nu este sănătatea produsului și nu este echivalent cu o achiziție sau un capitol întreg recertificat.','historic_projector':'Restrângeți T07.03 la expresia literală pe paginile citite, T259 la cele două obiective și două roluri, T352/T366 la segmentele documentate.','status_counts':ss,'A11_tier_counts':cc,'historic_rework1868':actdone,'bidirectional_edges':len(fwd),'symmetric_difference':len(fwd^reverse),'original1868_need_external_portion':extra,'original1868_still_open_need_external_portion':pendext,'original1868_still_open_other':actdone['NEEXECUTAT']-pendext,'new_R4_still_open':ss['NEEXECUTAT']-actdone['NEEXECUTAT'],'quality_histogram':hist,'cases':rows}
out=E/'A11_ledger_652_R4.json';write(out,v);print(h(out),v['status_counts']['NEEXECUTAT'],v['A11_tier_counts'],v['quality_histogram'])

