import json,pathlib,hashlib,collections,concurrent.futures,datetime,re
O=pathlib.Path(__file__).parent;E=O.parent;R=E.parent;F=E/'R3'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def hf(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=1)+'\n',encoding='utf8')
def fhashdata(p):d=p.read_bytes();return hashlib.sha256(d).hexdigest(),json.loads(d.decode('utf-8-sig'))
def checkhead(p,sha):assert hf(p)==sha,p
rep=rd(F/'A12_raport.json');checkhead(F/'A12_raport.json','777e0376218b486877dd903f8e5db3ef5a359c65303b27f7d9c05872698390c8'); checkhead(F/'Dovezi_criterii.json','2b18c5cd9bf90b930aafdca7cdc3dafe525c473ded737567eb22afafac0a29a2')
catalog=rd(F/'Dovezi_criterii.json');ev=catalog['evidence'];inverse={(k,x['task'],x['criterion'],x['relation']) for k,edges in catalog['inverse_task_requirement_links'].items() for x in edges}
j1=rd(E/'R1/A12_raport.json');j2=rd(E/'R2/A12_raport.json');r1={t['id']:t for t in j1['records']};r2={t['task']:t for t in j2['records']}
oldledger={x['task']:x for x in rd(E/'A11_ledger_651_R2.json')['records']};oldset=set(r2);newset={t['task'] for t in rep['records']};assert len(newset)==len(rep['records'])==652 and newset-oldset=={'T352'} and not oldset-newset
oldunknown={t['task'] for t in j2['records'] if t['functional_source_unidentified']};reexam={x['task']:x for x in rd(F/'Reexaminare_368.json')};assert oldunknown==set(reexam) and len(oldunknown)==368
gate=rd(E/'delta/2026-11-02T15-00-35-559Z/Addendum_plan_R2.json');approved={x['id']:x for x in gate['controls']};spec={
'T352':['R09: NEMONTAT în cele cinci cabinete observate; constatare de proveniență, cu JAR Git separat, nu DOVEDIT_DOAR_INSTALARE.','R01–R08: app/DAO/SQL nu dovedesc editor+publicare+persistență reală pe doi clienți. Cereți predările A06/A08 și dovada confirmării AI, înainte/refuz/după, drepturi și retry.'],
'T366':['Șase probe proiectate păstrate. R06 arată montare; R01–R05 au componente, 26/26 declarații SQL și suite, nu întregul flux al operatorului validare pe două produse/concurență/retur/repost. Integrați proba A05 pe versiunea sa distinctă.'],
'T257':['R3 a recuperat două criterii, cu test original 37/38 și calibrare separată 38/38. Reverificarea nativă exterioară a exercitat repostarea pe factură ordinară cu două scheme și storno; protecția exactă a notelor importate SAGA-FIDEL rămâne condiție separată.'],
'T259':['Interogarea nativă name/description returnează 4 rânduri, vechiul Value eșuează 42703; testul citit rulează pe bytecode, nu pornește forma Contracte. Testați real rol/rută/selector/încărcare și recuperare.'],
'T161.01':['Citatul original despre trecerea lunii este separat corect de metodă și de oracolele pentru producție neterminată; determinați lanțul de documente de producție/închidere pe două luni înainte de PASS.'],
'T354':['Revizuire explicită a R2-027 justificată. Canal global 13 după 7 din 20; suma 6 per operație-gărză separată nu dovedește canalul; IsSOTrx=N are efect distinct. Repro A11 pe alt set 20 vs14 și 15 vs18.'],
'T07.03':['Alias original T07.5. Registrul păstrează chiar sursa nominală cu tester, GET pe 7 limbi/implicit și țintă 7 rezultate zero. Clasificați ca obiectiv de test al interfeței fără a deduce autorizarea la închidere.'],
'T08.03':['Alias original T08.4: validare texte proprietar/consultant înainte de eliminarea marcajului „ciornă”. Înregistrați condiția verificabilă pentru livrare și țineți decizia istorică distinctă.'],
'T10.06':['Alias T10.7: manualul 15_manager_plan_v3.md:321 și :450 identifică „Hartă import” servită de frontend, precedență T10.6 și decizie proprietar înainte de deploy. Nu există temei pentru a lăsa și această condiție neidentificată.'],
'T10.04':['Alias T10.5: sursele descriu etapa audit/livrare și extinderea scriptului comun pentru JAR montat. Distingeți ce este cerut, deja existent și ulterior amânat înainte de a marca lipsa unei definiții.'],
'T36.53':['Alias T36-L4: commit nominal bfc6cd5278, UI cursuri, eroare/import nerecunoscut, valoare implicită data de azi. Verificați diff la commit și cereți sursa de autorizare; subiectul commitului nu certifică acceptarea.'],
'T224':['Trei bloburi la reviziile indicate valide; aceasta este probă documentară, nu auditarea reimportului SAGA sau acceptarea funcției.'],
'T229':['Anulare istorică versus stare activă/date în liste; păstrați contradicția administrativă separată de sănătatea aplicației.'],
'T227':['Determinarea JAR/AD în CESIRO nu exclude alte instalări și nu substituie formular/rulare pe rol.']}
origslots={'DOVEDIT_DOAR_INSTALARE':'PROVENIENȚĂ_DE_MONTAJ','FAIL_DOVEDIT_LA_NIVEL_COMPONENTĂ':'DEFECT_COMPONENTĂ','NEEXECUTAT':'NEEXECUTAT','CORECȚIE_SEGMENT_CANAL':'CORECȚIE_DOMENIU_DE_APLICARE','INCONCLUDENT_PREDARE_ANDROID':'PREDARE_PARȚIALĂ_ANDROID','ARTEFACT_DOCUMENTAR_PARȚIAL':'DOCUMENTAR_PARȚIAL','PARȚIAL_SEGMENT':'COMPONENTĂ_PARȚIALĂ','PARȚIAL':'COMPONENTĂ_PARȚIALĂ','INCONCLUDENT':'NECONCLUDENT','BLOCAT_ACCES':'BLOCAT','FAIL_DOVEDIT':'DISCREPANȚĂ_ADMINISTRATIVĂ'}
def review(t):
 tid=t['task'];digest,j=fhashdata(F/t['file']);p2=oldledger.get(tid);ct=j['operative_criteria_and_audit_criteria']+j['R3_new_criteria'];changed=[];issues=[];oldkeys={}
 assert digest==t['sha256'] and hf(F/t['html'])==t['html_sha256']; assert tid==j['task'] and j['canonical']==t['canonical'] and j['A11_score_R3'] is None
 if p2:
  d2,j2x=fhashdata(E/'R2'/r2[tid]['file']);d1,j1x=fhashdata(E/'R1'/r1[tid]['file']); assert d1==r1[tid]['sha256'] and d2==r2[tid]['sha256']==p2['R2_hash']==t['r2']
  oldkeys={c['id']:c for c in j2x['operative_criteria_and_audit_criteria']}
 else: d1=None; d2=None
 actual={c['id']:c for c in j['operative_criteria_and_audit_criteria']};assert set(actual)==set(oldkeys); 
 for cid,c in actual.items():
  if c!=oldkeys[cid]:
   assert c['R2_current_immutable']==oldkeys[cid]['current']
   changed.append(cid)
 assert len({c['id'] for c in ct})==len(ct) and len(j['control_register_R3'])==36
 assert len(ct)==t['total_checks'] and len(j['R3_new_criteria'])==t['new_criteria'];assert all(c['expected_oracle'] and c['next_action'] and c['normative_content'] for c in ct)
 if tid in ('T352','T366'):
  assert all(c['id'] in approved and approved[c['id']]['expected']==c['expected_oracle'] for c in j['R3_new_criteria'])
 edges=set();rows=[];casecounts=collections.Counter();newkinds=collections.Counter();openrisk=False
 for c in ct:
  isnew=c['id'] not in oldkeys; kind=c['kind'];curr=c['current'];status=curr['status']; cstyle=origslots.get(status)
  if status=='PASS_DOVEDIT':cstyle='DOCUMENTAR_REFERINȚĂ' if kind=='CONTROL_DISPOZIȚIE_REFERINȚE' else 'DOCUMENTAR_DISPOZIȚIE' if kind=='DISPOZIȚIE_ADMINISTRATIVĂ' else 'REVERIFICAȚI_PASS_FUNCȚIONAL'
  if c['id']=='T352-R09':cstyle='ABSENȚĂ_CLASE_ÎN_CINCI_JAR_MONTATE';issues.append('Eticheta DOVEDIT_DOAR_INSTALARE sugerează opusul observației despre absența claselor T352.')
  assert cstyle
  rel=[(c['source_evidence_id'],'source')]+[(x,'authority') for x in c.get('authority_evidence_ids',[])]
  for m in ['current','closure']:
   ph=c[m]; rel+= [(x,m) for x in ph['evidence_ids']];assert ph['observed'] or ph.get('blocking_reason') or ph.get('constraint') or c.get('constraint'),(tid,c['id'],m)
   if ph['observed']:assert ph['evidence_ids'],(tid,c['id'],m)
  for i,tag in rel:assert i in ev;edges.add((i,tid,c['id'],tag))
  if c['id'] in changed: change_note='Reformulare current cu versiunea R2 păstrată.'
  else:change_note='Nou R3' if isnew else 'Păstrat din R2'
  obs=c['expected_oracle'].strip()==c['normative_content'].strip()
  rows.append({'id':c['id'],'origin':kind,'source':c['source_evidence_id'],'from_previous_or_new':change_note,'state_at_closure':c['closure']['status'],'current_R3':status,'A11_disposition':cstyle,'current_evidence':curr['evidence_ids'],'oracle_repeats_requirement_verbatim':bool(isnew and obs)})
  casecounts[cstyle]+=1
  if isnew:newkinds[kind]+=1
  if not curr['evidence_ids'] and status!='NEEXECUTAT':openrisk=True
 if tid in ('T07.03','T08.03','T10.04','T10.06','T36.53'):issues.append('Ancora istorică exactă documentează o țintă/condiție ori un indiciu tehnic ce trebuie clasificat separat de pretinsa funcționare.')
 if tid in ('T352','T366'):assert t['state']==('închis' if tid=='T352' else 'montat')
 if tid in reexam:
  assert j['functional_criteria_unidentified']==(reexam[tid]['reconstructed']==0)
 earned=set(p2['earned_subchecks_R2'] if p2 else ['QC01-R1','QC01-R2','QC01-R4','QC03-R5','QC07-R4','QC07-R5','QC08-R4','QC09-R1'])
 if tid in reexam and j['R3_new_criteria'] and not issues:earned.add('QC02-R4')
 if tid in ('T257','T259','T352','T366','T354','T161.01'):earned.add('QC10-R2')
 if tid in ('T257','T259','T352','T366') and len(rows)>1:earned.update(['QC05-R1','QC09-R2'])
 if tid in ('T07.03','T08.03','T10.06'):earned.discard('QC02-R4')
 if tid=='T352':earned.discard('QC01-R5')
 fixes=list(spec.get(tid,[]))
 if not fixes:
  if j['functional_criteria_unidentified']:fixes.append('Dacă sursele numesc doar transferul/lotul, păstrați funcția nedeterminabilă; revedeți identitatea exactă și definițiile tehnice înainte de a atribui criterii ale părintelui.')
  if rows and any(c['current_R3']=='NEEXECUTAT' for c in rows):fixes.append('Urmărire specifică pe '+', '.join(c['id'] for c in rows if c['current_R3']=='NEEXECUTAT')+'. Confirmați efectul în fixture-ul corespunzător ori documentați imposibilitatea concretă.')
  if not fixes:fixes.append('Păstrați verificarea documentară/segmentul la aria probată; cereți dovadă distinctă pentru închiderea și funcționarea întregului task.')
 return {'task':tid,'canonical':t['canonical'],'title':t['title'],'file':t['file'],'sha_R1':d1,'sha_R2':d2,'sha_R3':digest,'html_sha_R3':t['html_sha256'],'R2_quality_score':p2['A11_R2_quality'] if p2 else None,'R3_quality_score':len(earned)/5,'earned_R3_subcheck_ids':sorted(earned),'R3_criteria_and_controls':len(ct),'delta_criteria_kinds':dict(newkinds),'changed_R2_current':changed,'residual_unknown_origin':j['functional_criteria_unidentified'],'R3_issues':issues,'semantic_disposition_counts':dict(casecounts),'all_criterion_decisions':rows,'case_gate':'PARȚIAL_DE_RELUAT','actions':fixes},edges
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool: pairs=list(pool.map(review,rep['records']))
rows=[x[0] for x in pairs];edges=set().union(*(x[1] for x in pairs)); assert edges==inverse and len(edges)==5307
counts=collections.Counter(); qhist=collections.Counter();newtypes=collections.Counter();status=collections.Counter();repeated=0;olds=0
for r in rows:
 counts.update(r['semantic_disposition_counts']);qhist[f"{r['R3_quality_score']:.1f}"]+=1;newtypes.update(r['delta_criteria_kinds']);olds+=len(r['changed_R2_current'])
 for c in r['all_criterion_decisions']:status[c['current_R3']]+=1;repeated+=c['oracle_repeats_requirement_verbatim']
out={'schema':'A11-ledger-independent-r3-v1','reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'R3_sha256':hf(F/'A12_raport.json'),'rubric_sha256':hf(R/'A11_rubrica_control.json'),'population':len(rows),'full_cases_accepted':0,'criterions_and_audit_checks':sum(sum(r['semantic_disposition_counts'].values()) for r in rows),'forward_edges':len(edges),'inverse_edges':len(inverse),'bidirectional_anomaly_count':len(edges^inverse),'new_reused_oracles':repeated,'historical_current_updates_preserved':olds,'R3_new_criterion_kind':newtypes,'full_case_quality_scoring':'Puncte pe cele 50 de subcontroale ale aceleiași rubrici; un subcontrol dovedit aduce 0,2. Restul celor 50 are 0. Unele puncte pe citări, probe componente și proveniență se aplică fără să dovedească produsul.','case_score_distribution':qhist,'reported_status_counts':status,'independently_qualified_status_counts':counts,'cases':rows}
assert out['criterions_and_audit_checks']==2594 and sum(newtypes.values())==398 and len(rows)==652
f=E/'A11_ledger_652_R3.json';wr(f,out);print(hf(f),dict(status),dict(counts),dict(qhist),repeated)

