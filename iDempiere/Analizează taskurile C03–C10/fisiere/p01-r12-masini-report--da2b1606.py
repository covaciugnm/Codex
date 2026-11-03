from pathlib import Path
import hashlib,json,datetime,html,shutil
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
O=R/'executie/R12_fisiere/A09_Date_Masini_lot02'
L=Path('D:/CodexWork/p01-r12-masini-dates')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,x): (O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
src=json.loads((O/'Sursa.json').read_text(encoding='utf-8-sig'))
binding=json.loads((O/'Binding_instalat.json').read_text(encoding='utf-8-sig'))
cp=[]
for p in [Path('D:/CodexWork/a12-r11-p01/repo/idempiere/plugins/com.eva.ro.contab/com.eva.ro.contab_13.0.0.jar'),*sorted(Path('D:/CodexWork/a12-r5-classes/all_deps').glob('*.jar')),*sorted(Path('D:/CodexWork/a05-support-jars').glob('*.jar'))]:
    cp.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
put('Classpath_provenance.json',{'utc':utc,'classpath_order':'classes OR harness_only; Git EVA jar; all_deps/*; a05-support-jars/*','jars':cp,'limit':'Classpath dependencies are test inputs. Only WSagaMasiniForm has execution credit; no credit for all dependency files.'})
for p in L.rglob('*.class'):
    dest=O/'compiled_artifacts'/p.relative_to(L);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
for n in ['logging.properties','classpath.txt']:
    if (L/n).exists():shutil.copyfile(L/n,O/n)
cases=[]
for label in ['compiled_source','git_jar']:
    rows=[]
    for line in (O/(label+'.stdout.txt')).read_text(encoding='utf-8-sig').splitlines():
        if line.startswith('CASE\t'):
            _,i,inp,exp,actual,cmp,same=line.split('\t')
            rows.append({'case':int(i),'input':inp,'expected':exp,'actual':actual,'jdk_uuuu_comparator':cmp,'product_matches_expected':same=='true'})
    assert len(rows)==12 and sum(x['product_matches_expected'] for x in rows)==7
    cases.append({'execution':label,'cases':rows,'valid_rejected':5,'invalid_or_empty_as_expected':7})
put('Cases_normalized.json',cases)
f={
 'schema':'P01_R12_partial_file_audit_v1','utc':utc,'head':src['head'],'plan':'../../R12_plan_delta/Plan_delta_R12_v2.json','plan_sha256':'4aeeaf61d73efa1a1155e9eecbbcc5564ddfeee4cda918fa5fa04c97f2ef7276',
 'plan_gate':'A11 10/10 before product execution; exact df85 revision',
 'file':src['path'],'oid':src['oid'],'sha256':src['sha256'],'dispatch_id':'Ffb5d87dce38b5c049467','owner':'A09','executor':'root (lot A09)','peer_nominal':'A01','independent_reviewer':'A11_PENDING',
 'role':'Formular ZK Mașini: nomenclator și scadențe auto; validarea Java este comună salvării și marcării scadențelor.',
 'canonical_task':None,'task_mapping':'SHARED_NO_TASK_ASSIGNED; observația T240 (P01.C14.T0001) este semnal de investigație, nu atribuire/închidere a taskului Mașini.',
 'requirement':'O dată calendaristică validă zz.ll.aaaa trebuie acceptată, inclusiv exemplul 15.03.2027 afișat de produs. Datele imposibile se refuză, câmpurile opționale goale se permit.',
 'actor':'Utilizator cu acces la nomenclatorul Mașini; drepturile efective nu au fost exercitate.',
 'control':'A09-C04 / A01.C13; A09-P1; ZK_UI; subset parser și legătura statică a salvării.',
 'normal_path':[{'step':'Editor pop-up → valoareEditor/valoareCamp → inainteDeSalvare → PO.saveEx','evidence':'WSagaCrudForm.java:1088-1096','mode':'STATIC_ONLY'},{'step':'Editare celule → inainteDeSalvare → PO.saveEx → commit','evidence':'WSagaCrudForm.java:964-976','mode':'STATIC_ONLY'},{'step':'inainteDeSalvare și stilCelula folosesc parseData','evidence':'WSagaMasiniForm.java:201-247','mode':'STATIC_CALLERS; parser EXECUTED'}],
 'native_method':'Se păstrează stratul iDempiere PO.saveEx și mecanismul existent CRUD; repararea formatului se poate face în DateTimeFormatter din JDK, fără motor nou de date/salvare SQL paralelă.',
 'positive':'5 date valide, inclusiv ani bisecți 2000/2024: toate returnează null în sursa compilată și în JAR Git.',
 'counterexample':'7 date invalide/goale/null returnează null conform contractului parserului; comparatorul JDK uuuu separă cele 5 date valide.',
 'result':'DEFECT REPRODUS ÎN COMPONENTA ORIGINALĂ: yyyy (YearOfEra) cu STRICT fără eră nu rezolvă LocalDate pentru exemplele valide.',
 'finding_id':'R12-MASINI-DATE-01','priority':'P1_PROPUS (funcție de salvare blocată pentru date valide; efectul UI/persistența încă de confirmat pe clonă)',
 'affected_columns':['ITP','ASIG_O','CASCO','ROVIGNETA','REVIZIE','LICENTA','TAHOGRAF'],
 'persistent_effect':{'observed':'NONE; no PO object, SQL, transaction or operational mutation','static_implication':'Pentru scadențe text nenule valide, înainteDeSalvare aruncă înainte de saveEx. stilCelula nu colorează scadențele al căror parser întoarce null. Nu este o demonstrație a interacțiunii ZK complete.'},
 'installed_binding':binding,'coverage':{'inventoried':True,'full_file_read':True,'compiled_original':True,'component_executed':True,'normal_ui_executed':False,'persistence_executed':False,'independent_receipt':False,'unique_cases':12,'executions':2,'case_evaluations':24,'entire_file_pass':False},
 'limits':['Nu s-a instanțiat/ocolit PO.get_Value final; niciun mock PO nu este prezentat drept iDempiere nativ.','Byte equality a clasei instalate este dovadă de cod, nu de clasă încărcată în procesul serverului ori de UI live.','Comparatorul uuuu nu modifică produsul și nu reprezintă remediere recepționată.','SecurityManager JDK21 este o gardă locală pentru componenta cunoscută, nu sandbox OS general; checkPermission nu interzice demontarea gărzii. Patru canari au fost refuzați înainte de încărcarea clasei.','Dependențele/JAR-ul/callerul nu primesc automat verdict integral sau credit de execuție pentru toate fișierele lor.'],
 'recommendation':'Corectați formatterul existent (de exemplu dd.MM.uuuu STRICT, după verificarea domeniului anilor permis); păstrați validarea strictă și PO.saveEx. Refaceți pe clonă cele 7 câmpuri prin pop-up și editare în tabel, gol/valid/imposibil, colorare expirat/30 zile/viitor, eroare lizibilă și rollback. Dacă se introduce un editor de dată, reutilizați componenta nativă ZK/iDempiere și migrarea compatibilă a valorilor text.',
 'closure_checklist':['Cerință aprobată și atribuire canonică, fără inventarea unui task.','Pozitiv/negativ pentru toate cele 7 câmpuri în editorii existenți.','Persistență PO.saveEx și rollback verificate pe clonă nativă.','Colorare scadențe trecut/azi/30 zile/viitor.','Citire și editare date existente importate, spații, format invalid, ani permiși.','JAR nou corelat cu sursa; probe de rol/cabinet și regresie; recepție A11.'],
 'closed_tasks':0,'full_business_contracts_closed':0,
 'evidence':['Sursa.json','Caller_source.json','WSagaMasiniForm.java','WSagaCrudForm.java','Compile_receipt.json','Execution.json','compiled_source.stdout.txt','git_jar.stdout.txt','Cases_normalized.json','Binding_instalat.json','Classpath_provenance.json','MasiniParserWitness.java']}
put('Fisa_Masini_date.json',f)
esc=html.escape
trs=''.join('<tr><td>'+esc(x['input'])+'</td><td>'+esc(x['expected'])+'</td><td>'+esc(x['actual'])+'</td><td>'+('Conform' if x['product_matches_expected'] else 'DEFECT')+'</td></tr>' for x in cases[0]['cases'])
doc=f'''<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>R12 · Mașini · date valide respinse</title><style>body{{font:17px/1.55 system-ui,sans-serif;max-width:1050px;margin:auto;padding:24px;color:#172c3e}}h1{{font-size:30px}}a{{color:#075b94}}code{{overflow-wrap:anywhere}}table{{border-collapse:collapse;width:100%}}td,th{{padding:8px;border:1px solid #ccd6dd;text-align:left}}.notice{{background:#fff0db;border-left:5px solid #c57d12;padding:16px}}.scroll{{overflow-x:auto}}li{{margin:8px 0}}</style>
<p>Audit P01 · R12 · lot 02 · {esc(utc)}</p><h1>Mașini: parserul respinge chiar exemplul de dată afișat utilizatorului</h1>
<p class="notice"><b>Defect de componentă reprodus.</b> Toate cele 5 date valide testate sunt refuzate în sursa originală compilată și în JAR-ul din Git. Clasa extrasă din JAR-ul instalat este identică binar. Nu am exercitat interfața ZK sau salvarea PO; recepția independentă A11 urmează.</p>
<p>Fișier <code>{esc(src['path'])}</code><br>HEAD <code>{src['head']}</code><br>OID <code>{src['oid']}</code>. Responsabil A09; peer nominal A01; executor root; verificator independent A11.</p>
<h2>Cerința și traseul normal</h2><p>{esc(f['requirement'])}</p><p>Atât salvarea din pop-up, cât și editarea în tabel apelează <code>inainteDeSalvare</code> înainte de <code>PO.saveEx</code>. Aceasta verifică cele șapte scadențe prin <code>parseData</code>. Aceeași funcție este folosită pentru culoarea scadențelor. Legătura a fost citită în cod; testul execută doar parserul original.</p>
<h2>Dovada executată</h2><p>12 cazuri unice, repetate pe două artefacte (24 evaluări). Cele 7 cazuri invalide/goale sunt tratate conform contractului; cele 5 valide eșuează. Codul de ieșire 0 al harnessului înseamnă executare terminată, nu produs conform.</p><div class="scroll"><table><thead><tr><th>Intrare</th><th>Așteptat</th><th>Original</th><th>Rezultat</th></tr></thead><tbody>{trs}</tbody></table></div>
<p><code>dd.MM.yyyy + STRICT</code> folosește anul erei fără rezolvarea erei pentru <code>LocalDate</code>. Comparatorul separat JDK <code>dd.MM.uuuu + STRICT</code> acceptă datele valide și refuză contraexemplele. Comparatorul este o pistă de remediere, nu o schimbare a aplicației.</p>
<h2>Efectul și limitele</h2><p>{esc(f['persistent_effect']['static_implication'])}</p><ul>{''.join('<li>'+esc(x)+'</li>' for x in f['limits'])}</ul>
<h2>Remediere cu reutilizarea mecanismelor existente</h2><p>{esc(f['recommendation'])}</p><ul>{''.join('<li>'+esc(x)+'</li>' for x in f['closure_checklist'])}</ul>
<p>Constatare <b>{f['finding_id']}</b>, prioritate P1 propusă, fără task închis și fără notă de conformitate integrală. Observația T240/P01.C14.T0001 a declanșat investigația; nu stabilește identitatea taskului Mașini.</p>
<p><a href="Fisa_Masini_date.json">Fișă completă</a> · <a href="Cases_normalized.json">Cazuri</a> · <a href="Binding_instalat.json">Legătura cu JAR-ul instalat</a> · <a href="WSagaMasiniForm.java">Sursa originală</a> · <a href="MasiniParserWitness.java">Harness</a> · <a href="Execution.json">Execuții</a></p></html>'''
(O/'Raport_Masini_date.html').write_text(doc,encoding='utf-8')
print(json.dumps({'output':str(O),'fisa_sha256':sha(O/'Fisa_Masini_date.json'),'classpath_jars':len(cp),'unique_cases':12,'evaluations':24},ensure_ascii=False))
