from pathlib import Path
import datetime,hashlib,json,re,shutil
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ref=lambda p:{'path':p.relative_to(R).as_posix(),'sha256':h(p),'bytes':p.stat().st_size}
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
verdict=R/'executie/R11_fisiere/A11/Verdict_A11_R11_val04_v1.json'
assert h(verdict)=='7133088b626b0abf1f3bf7161c9c05ceb62253a209e87bbd1daf045d950e99ff'
received=read(verdict)
P=R/'executie/R12_plan_delta'
plans=sorted(P.glob('Plan_delta_R12_v*.json'))
assert plans
plan=plans[-1]
gates=sorted(P.glob('A11_verdict_plan_delta_R12_v*.json'))
gate=gates[-1] if gates else None
gate_data=read(gate) if gate else None
gate_state=(gate_data.get('decision') or gate_data.get('state') or gate_data.get('verdict')) if gate_data else 'ÎN AȘTEPTAREA A11'
plan_html=plan.with_name(plan.stem+'_lectura.html')
if not plan_html.exists(): plan_html=plan.with_suffix('.html')
assert plan_html.exists()
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
snapshot=R/'executie/Publicare_Val04_R12'/stamp
snapshot.mkdir(parents=True,exist_ok=False)
for name in ['Raport_audit.html','Audit_C03.html','Audit_C10.html','Stare_continuare_audit.json','Runda_11_stare.json']:
 shutil.copyfile(R/name,snapshot/('anterior_'+name))
gate_link=('<a href="'+gate.relative_to(R).as_posix()+'">Verdictul independent al planului</a>') if gate else 'A11 verifică planul; testele pe noua revizie așteaptă aprobarea.'
section='''<section id="r11-val04"><h2>Recepția independentă Val_04 — codul 2fe90</h2>
<p><strong>A11 a recepționat registrul și probele limitate ale valului 04.</strong> Sunt 116 fișiere cu fragmente exercitate, față de 95 în valul 03. Există observații directe limitate pentru 20 de criterii din șase taskuri. Registrul păstrează 652 de fișe și 2.619 criterii. Acestea nu reprezintă fișiere sau taskuri validate integral.</p>
<p>Controlul a reconciliat 819 fișiere rehash-uite și 7.188 pointere: 31 verificări mecanice și 186 verificări ale unui peer separat. <strong>Toate cele 17 contracte complete rămân deschise.</strong> Nu este acordată o notă globală 10/10 pentru audit sau produs.</p>
<p><a href="executie/R11_fisiere/A11/Verdict_A11_R11_val04_v1.json">Verdict A11 Val_04</a> · <a href="executie/R11_fisiere/A12/Val_04/index.html">Fișele și dovezile Val_04</a> · <a href="executie/R11_fisiere/A11/Checklist_A11_dupa_val04_v1.json">Obligațiile rămase</a></p>
<table><thead><tr><th>Verificare</th><th>Rezultat și limită</th></tr></thead><tbody>
<tr><td>Frontend și ajutor</td><td>Configurațiile sintetice explică erori de pregătire ale testelor de teme, SAGA și proxy. Browserul confirmă ajutor general pentru 16 din 70 de rute statice fără articol dedicat. Completarea dicționarului existent rămâne necesară; ajutorul nativ ZK se verifică separat.</td></tr>
<tr><td>Backend</td><td>Opt suite originale suplimentare: 105 teste trecute. Limitele mock/SQLite sunt păstrate; acestea nu certifică posting, plăți sau integrare ERP completă. La T58, cele patru suite au rulat separat; aserțiunile care admit HTTP 500 nu certifică sănătatea rutei.</td></tr>
<tr><td>HR și drepturi</td><td>27 de cereri ASGI și controale pe PostgreSQL sintetic verifică izolarea și rollback. Politica member/read diferă între v1 și v2 în condițiile documentate. Nu este demonstrată o scurgere între firme; trebuie armonizată politica cu drepturile native și verificat mirror-ul real.</td></tr>
<tr><td>WMS nativ</td><td>Binding-ul instalat, sursele și metoda beforeSave au fost verificate suplimentar. Cursa BOM demonstrată la nivel componentă/JDBC nu este încă probată prin întregul PO/OSGi/Fact_Acct. Următorul pas este clona nativă sintetică, cu reutilizarea mecanismelor existente.</td></tr>
</tbody></table>
<p>Selecția celor 63 de surse de programe conține 1.259 de evenimente pytest: 1.206 trecute, două eșuate și 51 omise. Evenimentele includ subteste; nu sunt 1.259 de teste distincte. Două suite HR au doar trei cazuri reprobate, nu recepție integrală. Două evenimente eșuate nu înseamnă că produsul are doar două probleme.</p></section>'''
section+='''<section id="r12-plan"><h2>R12 — noua revizie GitHub și planul de continuare</h2>
<p>Revizia nouă este <code>df85d33c1648ce2b2df130a60a05ef696e2e5480</code>. Probele Val_04 aparțin exclusiv reviziei <code>2fe90ed3f128c33dff7cf9f8674e664a70679390</code>; nu au fost transferate automat.</p>
<p>Inventarul complet are 183.469 de căi. Delta cuprinde 557 adăugări și opt modificări. Cele 6.709 fișiere tehnice precedente sunt identice; 19 instrumente noi duc domeniul tehnic la 6.728. Dintre acestea, 16 au fost promovate din documentație. Auditul continuă și pentru fișierele neschimbate.</p>
<p>Planul împarte verificările în zece zone, păstrează A12 pentru fișele nominale și A11 pentru recepție, include oracole independente, martori negativi, efecte persistente și curățarea laboratoarelor. Scripturile care pot scrie obiecte Git, înlocui dovezi sau șterge scratch se probează numai pe copii sintetice proprii.</p>'''
section+='<p><a href="'+plan_html.relative_to(R).as_posix()+'">Planul detaliat R12</a> · <a href="executie/R12_plan_delta/Manifest_A12_receptie_R12_v2.json">Inventarul și indexul reconciliat</a> · '+gate_link+'</p>'
section+='<p><strong>Starea planului:</strong> '+str(gate_state)+'. Poarta independentă 10/10 este îndeplinită pentru planul v2 și hashul exact. Primul lot T240 se execută separat; rezultatele lui așteaptă recepția A11. Scorul planului nu închide auditul.</p><p>Populația observată rămâne 996 taskuri total, dintre care 693 P01, fără schimbări de membri sau stări. Numai observațiile și progresul T343 au fost actualizate. Datele exacte de închidere nedovedite rămân „dată exactă nedocumentată”. Stația hardware nu condiționează auditarea codului.</p><p>Pentru P01.C10.T0025 / T343, observația nouă afirmă că un criteriu ar accepta C_Order IP. Sursa fixată cere încă CO, iar amendamentul indicat nu apare în arborele verificat. Recepția acelui criteriu rămâne deschisă până la verificarea oracolului și a metodei native; celelalte loturi continuă. <a href="executie/R12_plan_delta/A12/Supliment_populatie_2315.json">Comparația nominală și limitele</a>.</p></section>'
for name in ['Raport_audit.html','Audit_C03.html','Audit_C10.html']:
 p=R/name;t=p.read_text(encoding='utf-8')
 t=re.sub(r'<!--r11-val03-progress-->.*?<!--end-r11-val03-progress-->','',t,flags=re.S)
 t=re.sub(r'<!--r11-val04-r12-progress-->.*?<!--end-r11-val04-r12-progress-->','',t,flags=re.S)
 marker='<!--end-r11-lot-curent-->' if name=='Raport_audit.html' else '<!--end-actualizare-r11-capitol-->'
 assert t.count(marker)==1
 t=t.replace(marker,marker+'<!--r11-val04-r12-progress-->'+section+'<!--end-r11-val04-r12-progress-->')
 p.write_text(t,encoding='utf-8')

checkpoint={'utc':received['utc'],'head':received['head'],'verdict':ref(verdict),'state':'RECEPȚIE VAL_04 PARȚIALĂ; AUDIT INTEGRAL DESCHIS','counts':received['counts'],'whole_execution_grade':None,'product_grade':None}
handoff=ref(R/'executie/R11_fisiere/A12/Val_04/Handoff_val_04.json')
r12={'utc':utc,'round':12,'head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','base':received['head'],'plan':ref(plan),'plan_gate':ref(gate) if gate else None,'plan_gate_state':gate_state,'product_tests_executed':None,'execution_state':'LOT A08 T240 ÎN CURS; REZULTATELE AȘTEAPTĂ RECEPȚIE A11','whole_execution_grade':None,'product_grade':None,'inventory':ref(P/'Manifest_A12_receptie_R12_v2.json'),'last_independent_checkpoint':checkpoint,'next':'După poarta A11 10/10: instrumente pure T240 și contraexemple; continuarea fișierelor neschimbate și pregătirea clonei native sintetice.','active_resources':'Nicio resursă nouă de produs creată la pregătirea R12; verificați agenții/procesele și registrele înaintea fiecărei reluări.'}
(R/'Runda_12_stare.json').write_text(json.dumps(r12,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ['Stare_continuare_audit.json','Runda_11_stare.json']:
 p=R/name;d=read(p);d['utc']=utc;d['last_independent_checkpoint']=checkpoint;d['current_nominal_handoff']=handoff
 d['latest_population_delta']=ref(R/'executie/delta/2026-11-02T23-15-23-444Z/Comparatie_ultimul_checkpoint.json')
 d['supplements_pending_independent_or_nominal_reception']=[]
 d['next_candidate']={'head':r12['head'],'state':'Runda_12_stare.json','plan':ref(plan),'gate':ref(gate) if gate else None,'execution_state':'Lot A08 T240 în curs după poarta A11; recepția urmează separat'}
 if name=='Stare_continuare_audit.json':
  d['history_before_R12']={k:d[k] for k in ['primary_hash','round','current_population','remaining','registry','next_round'] if k in d}
  d['primary_hash']=r12['head'];d['primary_hash_meaning']='Candidat de plan; ultimul testat este last_independent_checkpoint.head'
  d['round']=12;d['current_population']=693;d['historic_nominal_population']=652;d['remaining']=None
  d['remaining_meaning']='Vezi checklist A11 și cele 17 contracte; 1140 era indicatorul istoric R10, nu total curent.'
  d['registry']=handoff;d['next_round']=r12;d['generated_utc']=utc;d['latest_tracker']=d['latest_population_delta']['path']
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
manifest={'utc':utc,'kind':'publicare Val_04 și plan R12, înainte de QA vizual separat','files':[ref(R/n) for n in ['Raport_audit.html','Audit_C03.html','Audit_C10.html','Stare_continuare_audit.json','Runda_11_stare.json','Runda_12_stare.json']], 'previous_snapshots':[ref(p) for p in snapshot.glob('anterior_*')],'received_verdict':ref(verdict),'plan':ref(plan),'gate':ref(gate) if gate else None}
(snapshot/'Manifest_publicare.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(str(snapshot))
