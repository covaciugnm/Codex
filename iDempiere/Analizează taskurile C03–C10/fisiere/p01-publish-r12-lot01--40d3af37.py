from pathlib import Path
import sys,json,hashlib,datetime,re,shutil
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
rd=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ref=lambda p:{'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
verdict=R/sys.argv[1];manifest=R/sys.argv[2];handoff=R/sys.argv[3]
assert all(p.is_file() for p in [verdict,manifest,handoff])
v=rd(verdict);m=rd(manifest);hd=rd(handoff)
report=R/'executie/R12_fisiere/A08_T240/Lot_01_final_v1/Raport_A08_T240_R12_lot01_v1.json'
assert sha(report)=='b787ebbacdbed52aa5dfb3ac8b61d4e2ad331d043b489306b110986afbe5aa69'
ar=rd(report);assert ar['counts']['original_cases_passed']==46 and ar['counts']['mutants_by_status']=={'UCIS':33}
utc=datetime.datetime.now(datetime.timezone.utc).isoformat();stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
out=R/'executie/Publicare_Val04_R12'/('Final_'+stamp);out.mkdir(parents=True,exist_ok=False)
names=['Raport_audit.html','Audit_C03.html','Audit_C10.html','Stare_continuare_audit.json','Runda_11_stare.json','Runda_12_stare.json']
for name in names:shutil.copyfile(R/name,out/('anterior_'+name))
block='''<section id="r12-lot01"><h2>Primul lot R12 — control transversal al dovezilor de ajutor</h2>
<p><strong>A11 a recepționat probele de componentă pentru două instrumente T240 / P01.C14.T0001.</strong> Au trecut 46 din 46 de cazuri originale, fără modificarea surselor și fără omisiuni. Cei 33 de mutanți au fost detectați în șapte loturi separate. Încercarea programului integral cu mutanți a expirat la 60 de secunde și rămâne consemnată; loturile nu sunt prezentate drept succes al acelei încercări.</p>
<p>Au fost păstrați separat cei 20 de martori proprii A08, cazul CLI pentru UTF8 și cei 19 martori independenți A11. Cele 1.518 evaluări ale mutanților reutilizează aceleași 46 de cazuri; nu reprezintă 1.518 teste distincte. Testarea la 1.000 și 10.000 de rânduri privește parserul pe date sintetice, nu performanța iDempiere.</p>
<table><thead><tr><th>Constatare</th><th>Ce a fost demonstrat și ce se recomandă</th></tr></thead><tbody>
<tr><td>Titlul nu este confruntat cu inventarul</td><td>Judecătorul poate afișa <strong>13/13 conforme</strong> pentru un raport al cărui titlu contrazice coloana 2 din inventarul E. Cititorul elimină acea coloană și compară valori din același raport. Se propune adaptarea judecătorului existent pentru a folosi inventarul ca sursă independentă, cu excepția REGES verificată separat.</td></tr>
<tr><td>Inventar cu identificatori repetați</td><td>Același ecran introdus de două ori în inventarul E poate conduce la 14/14 pentru numai 13 identități. Se verifică unicitatea în cititorul existent. Această probă nu dovedește că lipsește un ecran real.</td></tr>
<tr><td>Raport cu codificare UTF8 invalidă</td><td>Intrarea CLI produce traceback și cod 1, în locul răspunsului controlat pentru raport ilizibil. Intrarea este refuzată; nu există acceptare falsă în acest caz. Se propune tratarea erorii în parserul existent.</td></tr>
<tr><td>Limite ale dovezilor</td><td>Fișierul de captură nevid și acordul dintre coloanele „așteptat” și „afișat” nu dovedesc proveniența sau aspectul UI. Configurația pragului EN și familia MANUAL se judecă după contractul consumatorului, fără severități automate.</td></tr>
</tbody></table>
<p><strong>Limita recepției:</strong> cele două fișiere sunt exercitate la nivel de componentă. Colectorul din buton, interfața ZK, rolurile și efectele ERP nu au fost probate în acest lot. Nu se închide T240 și nu se acordă credit nou taskurilor C03/C10. Cele 116 fișiere cu exerciții parțiale din R11 rămân evidență istorică separată; cele 17 contracte complete rămân deschise.</p>
<p>Ipoteza inițială despre incompatibilitatea unui nume de fișier cu Windows a fost infirmată prin probă: originalul a funcționat, iar A11 a confirmat fluxul NTFS. Nu a fost aplicat un adaptor preventiv și nu a fost imputat aplicației un defect de mediu presupus.</p>'''
block+='<p><a href="executie/R12_fisiere/A08_T240/Lot_01_final_v1/Raport_A08_T240_R12_lot01_v1.html">Raportul detaliat T240</a> · <a href="'+verdict.relative_to(R).as_posix()+'">Recepția independentă A11</a> · <a href="'+handoff.relative_to(R).as_posix()+'">Registrul A12 al primului lot</a></p></section>'
for name in names[:3]:
 p=R/name;s=p.read_text(encoding='utf-8');s=re.sub(r'<!--r12-lot01-->.*?<!--end-r12-lot01-->','',s,flags=re.S)
 marker='<!--end-r11-val04-r12-progress-->';assert s.count(marker)==1
 s=s.replace(marker,marker+'<!--r12-lot01-->'+block+'<!--end-r12-lot01-->')
 s=s.replace('Primul lot T240 se execută separat; rezultatele lui așteaptă recepția A11.', 'Primul lot T240 a fost recepționat separat la nivel de componentă; rezultatele și limitele sunt prezentate mai jos.')
 if name=='Raport_audit.html':
  current_blocks=[]
  for tag in ['r12-lot01','r11-val04-r12-progress']:
   pattern=r'<!--'+tag+r'-->.*?<!--end-'+tag+r'-->'
   found=re.search(pattern,s,flags=re.S);assert found
   current_blocks.append(found.group(0));s=s[:found.start()]+s[found.end():]
  s=s.replace('</header>','</header>'+''.join(current_blocks),1)
  s=s.replace('Plan aprobat independent cu 10/10. Auditul implementării este deschis.', 'Plan R12 v2 aprobat independent cu 10/10. Auditul implementării este deschis.')
  s=s.replace('<a href="Plan_audit_P01.html">Plan și atribuții</a>', '<a href="executie/R12_plan_delta/Plan_delta_R12_v2_receptionat.html">Plan R12 și atribuții</a> · <a href="Plan_audit_P01.html">Plan inițial</a>')
  s=s.replace('executie/delta/2026-11-02T20-46-47-993Z/Delta.json">Ultima captură a registrului', 'executie/delta/2026-11-02T23-15-23-444Z/Delta.json">Ultima captură a registrului')
  s=s.replace('Verificări fișier cu fișier la commitul 2fe90ed3','Istoric R11 — verificări fișier cu fișier la commitul 2fe90ed3')
  s=re.sub(r'<small>Actualizat [^<]*</small>','<small>Actualizat '+utc+' UTC · candidat R12 df85d33c1648ce2b2df130a60a05ef696e2e5480 · Git și populație observate la 2026-11-02 23:15 UTC; versiunea instalată se verifică separat.</small>',s)
 p.write_text(s,encoding='utf-8')

checkpoint={'utc':utc,'head':ar['head'],'verdict':verdict.relative_to(R).as_posix(),'verdict_sha256':sha(verdict),'verdict_ref':ref(verdict),'manifest':ref(manifest),'handoff':ref(handoff),'state':'RECEPȚIE LOT R12 COMPONENTĂ; AUDIT INTEGRAL DESCHIS','counts':ar['counts'],'whole_execution_grade':None,'product_grade':None,'open_full_contracts':17}
for name in names[3:]:
 p=R/name;d=rd(p);d['utc']=utc
 if name=='Runda_11_stare.json':
  old=d['last_independent_checkpoint']
  if isinstance(old.get('verdict'),dict):
   old['verdict_ref']=old['verdict'];old['verdict_sha256']=old['verdict']['sha256'];old['verdict']=old['verdict']['path']
  d['next_candidate']={'head':ar['head'],'state':'Runda_12_stare.json','last_component_receipt':checkpoint}
 else:
  d['previous_R11_checkpoint']=d.get('last_independent_checkpoint');d['last_independent_checkpoint']=checkpoint
  d['current_nominal_handoff']=ref(handoff);d['component_execution_counts']=ar['counts'];d['execution_state']='LOT T240 RECEPȚIONAT PARȚIAL; CONTINUARE NECESARĂ'
  d['product_tests_executed']=True;d['product_tests_executed_meaning']='Există execuții ale celor două instrumente la df85, fără numitor agregat de teste distincte și fără UI/ERP.'
  d['plan_quality']=10;d['gate']='executie/R12_plan_delta/A11_verdict_plan_delta_R12_v2.json';d['gate_sha256']='84e3735906d868f2153bc6b71c8f0e0e7a0211367ba4d3df5f8509d008d1f2a4'
  d['next']='Continuă cele 17 instrumente noi fără execuție și axele rămase la cele două exercitate, fișierele neschimbate și clona nativă sintetică. Urmărește separat oracolul C-2.2 T343; nicio închidere automată.'
  d['latest_resources']='A08 și A11 declară cleanup verificat; înainte de reluare se recitesc recepțiile și execuțiile active.'
  if name=='Stare_continuare_audit.json':
   d['generated_utc']=utc;d['registry']={**ref(handoff),'file':handoff.relative_to(R).as_posix()}
   d['next_round']={'round':12,'work_state':'Runda_12_stare.json','candidate_code':ar['head'],'plan_quality':10,'gate':d['gate'],'gate_sha256':d['gate_sha256'],'stage':d['execution_state'],'A12_current':handoff.relative_to(R).as_posix(),'full_execution_grade':None,'remaining_contracts':17}
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'Predare_publicare.json').write_text(json.dumps({'utc':utc,'received':checkpoint,'files_pending_final_QA':[ref(R/n) for n in names],'previous_snapshots':[ref(p) for p in out.glob('anterior_*')]},ensure_ascii=False,indent=2),encoding='utf-8')
print(str(out))
