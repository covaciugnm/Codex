from pathlib import Path
import sys,json,hashlib,datetime,re,shutil
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
rd=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ref=lambda p:{'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
cfg=rd(Path(sys.argv[1]))
assert cfg['independent_lots_received'] and cfg['independent_register_received']
inputs={k:R/cfg[k] for k in ['verdict','lot_verdict','manifest','handoff','checklist','native_verdict','native_report','population_supplement']}
assert all(p.is_file() for p in inputs.values())
v=rd(inputs['verdict']);hd=rd(inputs['handoff'])
assert hd['head']=='df85d33c1648ce2b2df130a60a05ef696e2e5480'
assert cfg['component_files']==13 and cfg['open_contracts']==17 and cfg['remaining_new_tools']==7
assert hd['counts']['current_partial_source_files']==13 and hd['counts']['native_contracts_open']==17 and hd['counts']['full_task_verdicts']==0
utc=datetime.datetime.now(datetime.timezone.utc).isoformat();stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
out=R/'executie/Publicare_R12_Val02'/('Final_'+stamp);out.mkdir(parents=True,exist_ok=False)
names=['Raport_audit.html','Audit_C03.html','Audit_C10.html','Stare_continuare_audit.json','Runda_11_stare.json','Runda_12_stare.json']
for name in names:shutil.copyfile(R/name,out/('anterior_'+name))
block='''<section id="r12-lot02"><h2>R12 · lotul 02 — defect în aplicație, probe native și controlul dovezilor</h2>
<p><strong>Progres recepționat independent, auditul integral rămâne deschis.</strong> La candidatul <code>df85d33c</code>, registrul cuprinde 6.728 de fișiere tehnice; 13 au acum porțiuni exercitate în R12, față de 2 în checkpointul anterior. Cele 11 adăugate sunt zece instrumente de audit și o clasă a aplicației. Cele 116 fișiere exercitate parțial în R11 rămân evidență istorică separată. Niciun fișier, task sau contract de business nu primește recepție integrală.</p>
<h3>Mașini: date valide refuzate</h3>
<p>Parserul original respinge toate cele cinci date valide testate, inclusiv <strong>15.03.2027</strong>, chiar exemplul indicat utilizatorului. Rezultatul este identic în clasa compilată din sursa Git și în JAR-ul din Git; clasa extrasă din JAR-ul instalat este identică binar. Cele șapte intrări invalide/goale au rezultatul așteptat. Sunt 12 cazuri unice executate pe două artefacte, nu 24 de cazuri diferite.</p>
<p>Codul apelează acest parser înainte de <code>PO.saveEx</code> pentru cele șapte scadențe și pentru colorarea lor. Consecința rezultată din cod este refuzarea salvării datelor valide și lipsa marcării acelor scadențe. <strong>Interacțiunea ZK și salvarea acestui formular nu au fost executate în lot.</strong> Se propune corectarea formatterului existent, cu păstrarea validării stricte și a salvării native; comparatorul JDK cu <code>uuuu</code> este o pistă verificată pe aceste exemple, nu o remediere instalată.</p>
<p><a href="executie/R12_fisiere/A09_Date_Masini_lot02/Raport_Masini_date.html">Fișa detaliată Mașini, probe și checklist de remediere</a></p>
<h3>Zece instrumente: un rezultat „OK” trebuie susținut de probe</h3>
<p>A08 a executat 54 de cazuri în 58 de invocări principale; A09 a executat 67 de cazuri. A11 a adăugat separat 12 probe CLI ale instrumentelor și opt cazuri Mașini, cu alt oracol calendaristic, confirmând refuzul a încă trei date valide. Rezultatele includ defecte, contraexemple și limite, fără a fi prezentate drept teste de produs toate trecute. Cele 21 de grupe de constatări/limite ale executanților se consultă împreună cu dispozițiile A11.</p>
<table><thead><tr><th>Risc demonstrat</th><th>Adaptarea recomandată în instrumentele existente</th></tr></thead><tbody>
<tr><td>Raport cu „OK” și afirmație de lectură când dovada lipsește; copil eșuat, părinte cu succes</td><td>Stări explicite DOVEDIT / NEVERIFICAT / DEFECT; verificarea codului de ieșire, a erorilor, a populației așteptate și a probei nominale înainte de emiterea verdictului.</td></tr>
<tr><td>Identificator eliminat: zero probleme în validator, apoi șase „OK” în raport</td><td>Distincție între identificator prezent, mutat și absent; propagarea diagnosticului pe întregul flux. Absența diagnosticului nu dovedește conformitate.</td></tr>
<tr><td>Progres duplicat și selecție diferită a suplimentelor; intrare ambiguă cu două capitole pentru aceeași clasă</td><td>Unicitate și numitori expliciți; reutilizarea aceleiași selecții. A11 califică proba capitolelor duplicate: intrarea încalcă invariantul manualului, deci dovedește o limită de diagnostic, fără defect nativ sau P2 automat.</td></tr>
<tr><td>Nume identic în directoare ZIP diferite schimbă verdictul în funcție de ordine</td><td>Identificarea resursei prin calea completă și păstrarea ancorelor, nu prin numele simplu.</td></tr>
<tr><td>Potrivire textuală în comentariu/alt ecran, captură prea mică, corpus gol</td><td>Etichetarea rezultatelor ca indicii și limite; verificare distinctă a ecranului, rolului și contextului, citire la scară lizibilă și refuzul recepției pe numitor gol.</td></tr>
</tbody></table>
<p><a href="executie/R12_fisiere/A08_Helper_rapoarte_lot02/Raport_A08_lectura.html">A08 — rapoarte și pipeline</a> · <a href="executie/R12_fisiere/A09_Helper_corpus_lot02/Raport_A09_Helper_corpus_lot02_lectura.html">A09 — corpus, manual și capturi</a>. Copiile pentru lectură adaugă numai stiluri pentru mobil; rapoartele originale sigilate păstrează starea de la predare. Recepția ulterioară și calificările ei sunt în verdictul A11 legat mai jos.</p>
<h3>Clonă sintetică: modelul nativ iDempiere a executat persistența</h3>
<p>Bootstrapul real Equinox → Service.locator → furnizor PostgreSQL → model nativ a permis <code>MProduct.saveEx</code>, commit cu recitire, rollback fără rând persistent, refuzul unui duplicat și retry. Numele CPP/CPA din datele de test sunt etichete de fixture; două ID-uri distincte nu certifică încă identitatea permanentă, nereutilizarea codurilor, separarea SKU/EAN sau modelul G1/G2/G3.</p>
<p>Recepția este limitată la infrastructură și PO generic. Versiunea calendaristică a seedului corespunde nucleului, dar <code>LastBuildInfo</code> păstrează un placeholder; <code>DB.isBuildOK</code> acceptă diferența prin <code>FailOnBuildDiffer=N</code>. Nu se afirmă compatibilitate completă, validarea validatorilor EVA, DocAction, Fact_Acct ori a fluxurilor WMS.</p>
<h3>Ce rămâne și cum continuă auditul</h3>
<p>Rămân șapte instrumente noi fără execuție, axele neacoperite ale celor deja exercitate, fișierele neschimbate și cele 17 contracte complete. Probele native vor urmări rolul, tranzacția, efectul persistent și contraexemplul pentru fiecare flux. Nu se transferă automat un test de componentă în recepție frontend, backend sau business. <a href="executie/R12_fisiere/A09_Date_Masini_lot02/Scope_restant_Masini_v1.json">Controalele neexecutate încă în clasa Mașini</a> păstrează distinct ipotezele și defectul demonstrat.</p>
<p>Captura registrului de la 23:39 UTC păstrează 693 de taskuri P01 și 996 în total, fără modificări de membri sau stări față de captura anterioară. Observațiile și progresul T240 s-au schimbat; afirmațiile despre o ramură de implementare nu sunt dovezi de remediere în candidatul auditat. Conflictul documentar T343 privind oracolul CO/IP rămâne deschis. Datele de închidere fără dovadă exactă rămân „dată exactă nedocumentată”.</p>
<p>Planul R12 are aprobarea independentă 10/10. <strong>Aceasta nu este nota implementării.</strong> Nu s-au modificat codul aplicației, taskurile sau datele operaționale.</p>
<p>Directorul temporar Mașini a rămas păstrat, fără proces Java activ: ștergerea a fost respinsă de verificarea automată a comenzii cu „blocked by policy”. Limita este înregistrată; nu se declară restituire integrală a tuturor fișierelor temporare.</p>'''
block+='<p>'+ ' · '.join('<a href="'+cfg[k]+'">'+label+'</a>' for k,label in [('lot_verdict','A11 — verificarea loturilor'),('native_verdict','A11 — infrastructura nativă'),('verdict','A11 — recepția registrului'),('handoff','A12 — registrul Val02'),('checklist','Checklist pentru continuare')])+'</p></section>'
block=block.replace('<a href="'+cfg['handoff']+'">A12 — registrul Val02</a>','<a href="executie/R12_fisiere/A12/Val_02/index.html">A12 — registrul Val02</a>')
for name in names[:3]:
 p=R/name;s=p.read_text(encoding='utf-8');assert '<!--r12-lot02-->' not in s
 if name=='Raport_audit.html':s=s.replace('</header>','</header><!--r12-lot02-->'+block+'<!--end-r12-lot02-->',1)
 else:
  marker='<!--r12-lot01-->';assert marker in s;s=s.replace(marker,'<!--r12-lot02-->'+block+'<!--end-r12-lot02-->'+marker,1)
 s=s.replace('executie/delta/2026-11-02T23-15-23-444Z/Delta.json">Ultima captură a registrului','executie/delta/2026-11-02T23-39-09-646Z/Delta.json">Ultima captură a registrului')
 s=re.sub(r'<small>Actualizat [^<]*</small>','<small>Actualizat '+utc+' · candidat R12 df85d33c1648ce2b2df130a60a05ef696e2e5480 · Git și populație observate la 2026-11-02 23:39 UTC; versiunea instalată verificată separat, la nivel de clasă pentru Mașini.</small>',s)
 p.write_text(s,encoding='utf-8')
checkpoint={'utc':utc,'head':hd['head'],'verdict':cfg['verdict'],'verdict_sha256':sha(inputs['verdict']),'verdict_ref':ref(inputs['verdict']),'manifest':ref(inputs['manifest']),'handoff':ref(inputs['handoff']),'lot_verdict':ref(inputs['lot_verdict']),'native_verdict':ref(inputs['native_verdict']),'state':'RECEPȚIE R12 VAL02 PARȚIALĂ; AUDIT INTEGRAL DESCHIS','counts':hd['counts'],'whole_execution_grade':None,'product_grade':None,'open_full_contracts':17}
for name in names[3:]:
 p=R/name;d=rd(p);d['utc']=utc
 if name=='Runda_11_stare.json':d['next_candidate']={'head':hd['head'],'state':'Runda_12_stare.json','last_component_receipt':checkpoint}
 else:
  d.setdefault('previous_R12_checkpoints',[]).append(d['last_independent_checkpoint']);d['last_independent_checkpoint']=checkpoint
  d['current_nominal_handoff']=ref(inputs['handoff']);d['next_review_checklist']=ref(inputs['checklist']);d['component_execution_counts']=hd['counts'];d['execution_state']='VAL02 RECEPȚIONAT PARȚIAL; 13 FIȘIERE CU COMPONENTE EXERCITATE; 17 CONTRACTE DESCHISE'
  d['product_tests_executed_meaning']='12 instrumente și o clasă originală cu porțiuni executate în R12; bootstrap PO nativ generic separat, fără recepție integrală UI/ERP.'
  d['next']='Continuă 7 instrumente noi rămase și fișierele neschimbate; execută pe clona nativă sintetică metodele și contractele de business neacoperite după verificarea diferențelor și porții de plan. Păstrează T343 CO/IP separat; nicio închidere automată.'
  d['latest_resources']='A08/A09 helpers: laboratoare eliminate; Mașini: scratch păstrat după refuzul auto-review, zero procese Java; A05 conform recepției și cleanupului distinct.'
  d['active_resources']=d['latest_resources']
  d['external_dependency_indispensable']=False;d['latest_population_supplement']=ref(inputs['population_supplement']);d['native_infrastructure_receipt']=ref(inputs['native_verdict'])
  d['latest_population_delta']=ref(R/'executie/delta/2026-11-02T23-39-09-646Z/Comparatie_ultimul_checkpoint.json')
  d['publication_state']='R12 Val02 recepționat parțial; 13 surse cu componente exercitate, infrastructură PO nativă separată; audit integral deschis, fără notă globală nouă.'
  if name=='Stare_continuare_audit.json':
   d['generated_utc']=utc;d['registry']={**ref(inputs['handoff']),'file':cfg['handoff']}
   d['latest_tracker']='executie/delta/2026-11-02T23-39-09-646Z/Comparatie_ultimul_checkpoint.json'
   d['primary_hash_meaning']='Candidat congelat și testat parțial; nu reprezintă afirmația că master nu s-a schimbat după captura23:39UTC.'
   d['current_best_view']['R12_nominal']=cfg['handoff']
   d['next_candidate']['execution_state']=d['execution_state']
   d['next_review']='Reia din checklistul A11 Val02; verifică execuțiile active și diferențele de Git/populație înainte de noua rundă. Prioritate codului de aplicație și proceselor native WMS/DocAction/Fact_Acct, cu reconcilierea seedului. Cele7instrumente rămase se verifică separat. Păstrează limitele de identitate, rol și contabilizare G1/G2/G3.'
   d['next_round']={'round':12,'work_state':'Runda_12_stare.json','candidate_code':hd['head'],'plan_quality':10,'gate':d.get('gate'),'stage':d['execution_state'],'A12_current':cfg['handoff'],'full_execution_grade':None,'remaining_contracts':17}
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'Predare_publicare.json').write_text(json.dumps({'utc':utc,'received':checkpoint,'inputs':{k:ref(p) for k,p in inputs.items()},'files_pending_final_QA':[ref(R/n) for n in names],'previous_snapshots':[ref(p) for p in out.glob('anterior_*')]},ensure_ascii=False,indent=2),encoding='utf-8')
print(out)
