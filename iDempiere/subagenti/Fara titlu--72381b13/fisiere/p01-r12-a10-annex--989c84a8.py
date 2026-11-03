from pathlib import Path
import json, hashlib, datetime, html
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
P=R/'executie/R12_plan_delta'
M=json.loads((P/'Manifest_sources_lues.json').read_text(encoding='utf-8-sig'))
I=json.loads((P/'A12/Index_19_fise.json').read_text(encoding='utf-8-sig'))
C={x['file']:x for x in json.loads((P/'A12/Controale_audit_R12_I01_I19.json').read_text(encoding='utf-8-sig'))['rows']}
S={Path(x['path']).name:x for x in M['rows'] if Path(x['path']).suffix in ('.py','.sh')}
# Prose authored by A10. No candidate module is imported or executed here.
N={
'verifica_integrare_L1.sh':[
'Git/JAR/commituri istorice→gărzi și comparații ZIP→raport de integrare→A12/A11.',
'Repo sintetic complet, ref-uri fixate: mulțimile de căi/intrări ZIP și hashurile coincid cu comparatorul independent. Canarul este text și nu efectuează cererea HTTP.',
'Ref lipsă/shallow, JAR corupt, gardă rc nenul și export parțial. Nu accepta exit0 al ultimului echo ca succes; wc -l poate include linii goale. CRC/MD5 nu sunt singurele identificatoare de proveniență.',
'Scrie sn_*.jar și canar în scratch; merge-tree --write-tree poate crea obiecte Git. Numai copia Git izolată este permisă, nu checkout operațional.',
'Compară independent tree/OID și SHA256 pentru fiecare intrare ZIP; păstrează fiecare rc. Referințele istorice nu dovedesc starea runtime la df85.',
'Comentariul Read-only nu face întregul script readonly. Pentru fixarea master la candidat, comparatorul și patchul se declară separat.'
],
'foi_contact.py':[
'raport.tsv/capturi→miniaturi și foi.md→lectură vizuală peer.',
'21 rânduri cu două imagini valide fiecare produc trei foi în ordinea raportului. Absența justificată a panoului este vizibilă și păstrează eșecul de produs.',
'Captură lipsă, coruptă, goală, cale ../ ori absolută, rând duplicat și imagini lungi care devin ilizibile în miniatură.',
'Scrie numai foi derivate în dosar nou. Intrările și capturile originale rămân byte-identice.',
'Reconciliere independentă rând→pereche imagini→foaie, decodare reală și inspecție a originalelor când miniatura nu permite citirea.',
'rc0 atestă cel mult compunerea; nu dovedește că ecranele sunt corecte ori că testerul a deschis foile.'
],
'fragment_public.py':[
'Fraze sintetice de mască + JAR public + corpus→fragmente clasificate→recepție confidențialitate.',
'Un fragment public și unul sintetic nepublic sunt clasificate separat fără imprimarea valorilor; diacriticele sunt tratate prin comparator independent.',
'Resurse ZIP cu același basename, listă/corpus goale și frază privată al cărei bigram este comun în text public; extensii și binare excluse explicit.',
'Doar stdout și jurnal nou; corpusul/JAR nemodificate.',
'Comparator pe căi ZIP complete și fraze complete; canari sintetici cunoscuți și numitor real de fișiere.',
'Dict-ul public folosește basename și poate suprascrie o resursă omonimă. Bigram public nu certifică anonimizarea contextului întreg ori a imaginilor.'
],
'reteta_L6.sh':[
'Git ref→JAR/E/Manual→helper clonă→colector→judecător→mască→foi→cleanup.',
'Lot sintetic complet cu HTTP/OSGi/JAR/DB sănătoase verificate separat; toate etapele au bilanț și resursele proprii sunt închise.',
'Eșec injectat la fiecare pas, timeout, întrerupere, lipsă stare, gardă rc1, rețea neinternă și JAR nepotrivit. Orice cale operațională rămasă blochează execuția.',
'Originalul șterge și înlocuiește dovezi-80; se permite exclusiv copia nouă. Schimbarea limbii și operațiile de clonă/slot numai în laborator sintetic.',
'Manifest per etapă cu rc/input/output SHA și efect DB pe conexiune nouă. Cleanup verificat în afara trapului, inclusiv porturi, volume și slot.',
'Reutilizează pregateste_cabinet_help.sh cu seed pur sintetic; niciun dump operațional q31. Nu interpreta exit0 al helperului drept restore/readiness; comparatorul remapat nu este execuția originalului integral.'
],
'c8_lot.py':[
'Progres lot + jurnale refs istorice→constatari_lotK.tsv→construieste_lot.py.',
'Două ecrane și un supliment: fiecare constatare are cheia corectă; reluarea în propria copie nu adaugă dubluri.',
'Jurnal absent/stale la alt SHA, lot inexistent, rând fără delimitator și chei parțial identice. Ecranul normal și suplimentul nu se confundă.',
'Append în constatări numai în copia sintetică; livrarea auditului folosește dosare noi imuabile.',
'Mulțimea constatărilor extrasă independent din progres și jurnale coincide exact, nu doar totalul.',
'Jurnalele sunt fixate nominal la b71a3e085a6; nu se transferă automat la df85. Scriptul agregă, nu repară referințe.'
],
'citate_butoane.py':[
'Cadru lot + TSV + etichete/literali Java→citate negăsite→revizuire manuală.',
'Citat exact valid găsit și citat sintetic absent semnalat, cu numitor de rânduri reconciliat.',
'Root relativ greșit, lot gol, literal doar în comentariu sau într-o altă formă, subșir accidental și buton ascuns rolului.',
'Numai stdout; intrările rămân neschimbate.',
'Legătura explicită ecran→control→label în cod și apoi DOM/rol nativ; căutarea globală oferă candidați.',
'Nu impune exit nenul pentru citate negăsite. rc0 și existența unui literal oriunde nu sunt corectitudine UX.'
],
'clase_corpus.py':[
'Inventar E/Java/TSV/consultant→K1–K6→candidați și numitori pe lot.',
'Fixture cu butoane/câmpuri cunoscute, RO/EN echivalente și numere egale; martor separat pentru fiecare clasă.',
'Buton doar în dialog, EN gol, procent/termen schimbat, literal comun în altă formă, supliment cu extensie neprevăzută și input lipsă.',
'Rezultate statice numai; fără scrieri DB.',
'Inventar independent de seturi și revizuire bilingvă, cu sursă concretă pentru fiecare candidat. Legalitatea se verifică distinct față de cerința/versiunea aplicabilă.',
'K1/K5 sunt euristici declarate. Cifrele egale nu înseamnă sens identic; rc0 nu recepționează corpusul.'
],
'construieste_lot.py':[
'Progres + constatări + fisa/manual_cap + V→raport lot→A12/A11.',
'Progres explicit citit și probe complete produc exact rândurile/numitorii; capitol și supliment nu dublează constatările comune.',
'Progres necitit, V absent, subprocess eșuat ori stdout gol; eliminarea constatării nu justifică OK. Lot nevalid și delimitatori Markdown.',
'Suprascrie raportul lotului numai în copia sintetică; dovada finală este nouă și append-only.',
'Fiecare OK trebuie susținut de o dovadă pozitivă separată. Reconciliere cheie→lectură→sursă→contraexemplu, nu absența constatării.',
'Scriptul emite OK implicit și textul citit; aceste formulări nu constituie dovadă de lectură. subprocess stdout fără returncode nu confirmă execuția reușită.'
],
'fisa.py':[
'Help TSV/V/inventar E→eșantion și prima apariție→raport/numărători.',
'Rol, toate butoanele, câmpuri impare și rânduri legale selectate exact; supliment integral; legătură RO+EN identică verificabilă.',
'Câmp par cu condiție de business necuprinsă, V lipsă/trunchiat și prima apariție doar declarată, fără probă de citire.',
'Numai stdout; cache-urile de import sunt controlate în scratch.',
'Lista completă de chei independentă și diferența eșantion/complet publicată. Pentru mandatul integral se extinde lectura la rândurile omise.',
'Eșantionul nu dovedește citirea integrală a fișierului; texte identice pot avea contexte de utilizare/rol diferite.'
],
'garzi.sh':[
'Corpus copiat + index sintetic + canar→gărzi→bilanț independent.',
'Corpus curat și canar de text au rezultate distincte; Git index conține numai fixture și cleanup rămâne în scratchul propriu.',
'SP/R hardcodate operațional, cale cu spații, gardă eșuată urmată de rm reușit, index diferit de corpus: refuz recepție.',
'Șterge SP recursiv și poate scrie obiecte prin merge-tree --write-tree; numai copie Git/scratch sintetic, cu limite absolute validate.',
'Snapshot înainte/după al căilor și obiectelor, rc separat pentru fiecare gardă/canar și verificarea surselor intacte.',
'Nu este global readonly; canarul static nu demonstrează blocarea reală a rețelei. Nu se execută varianta cu scratch /tmp al altei sesiuni.'
],
'manual_cap.py':[
'ManualEvA/Reges + metadata/menu + etichete→capitol/titlu/citate→lectură manuală.',
'Capitol clasic, REGES, titlu prin etichetă și concatenări Java: linii/meniu/citate corespund surselor.',
'Clasă fără capitol, capitole multiple, formă moștenită, meniu inactiv ori inaccesibil rolului și etichetă omonimă.',
'Doar stdout; nicio modificare de metadate.',
'Citire independentă surse, apoi AD_Menu/AD_Form/AD_Role și traseu UI normal în clonă, fără meniu nou paralel.',
'Regex nu substituie parser Java sau drepturile native. NEGĂSIT ori FĂRĂ CAPITOL poate fi tipărit fără exit de eșec.'
],
'numara_lot.py':[
'Progres + TSV + fisa.esantion→numitori eșantion/total→raport lot.',
'Fixture cu număr cunoscut de chei; lotul gol păstrează explicit numitor zero, nu 100% acoperire.',
'Rând progres duplicat, aceeași formă în două loturi, supliment cu câmp par, cheie duplicată și import fisa eșuat.',
'Doar stdout; fișierele sursă sunt intacte.',
'Set independent de identități cale/cheie/linie/lot; diferențe de mulțimi, nu doar sume.',
'Numărătorul aplică esantion inclusiv suplimentelor, în timp ce fisa --supliment le citește integral; confruntarea este obligatorie. Numerele nu probează lectura.'
],
'refs_nemarcate.py':[
'Tabele V + index basename Java/TSV→referințe greșite/ambigue→C8 lot.',
'Identificator la linia citată trece; mutat în aceeași sursă este raportat, ambiguitatea de basename este păstrată.',
'Identificator eliminat complet, interval invalid, fișier omonim, regex neaplicabil și zero verificate cu zero probleme.',
'Numai stdout; fără efect DB/Git.',
'Resolver independent pe cale completă și interval, inclusiv identificatori inexistenți; ambiguitățile/excluderile au numitor explicit.',
'În cod, prob crește doar dacă ident există altundeva. Dispariția completă poate rămâne neraportată; este limită de verificat, nu verdict automat de produs.'
],
'mutanti_aud_b_r1.py':[
'SHA site separat→export→A00/A01–A23→runner B-r1→reconciliere.',
'A00 byte-identic, ceilalți exact o mutație intenționată compilabilă. Doi tenants sintetici și chei idempotente distincte.',
'Dest=sursă/repo/părinte ori symlink în afara scratch: wrapper refuză înainte de rmtree. Ancoră lipsă/dublă sau compilare eșuată=NERULAT, nu UCIS.',
'Copiază/șterge recursiv dest; numai scratch propriu verificat. Nicio anulare/rambursare ori apel partener real.',
'Diff independent per mutant, control A00 verde și aserțiune sensibilă demonstrată, cu efect DB/rol corespunzător.',
'Ținta este codul site-ului la commit separat; fără acel SHA proba rămâne neexecutată, nu primește credit doar pentru EVA df85.'
],
'rulare_aud_b_r1.sh':[
'SHA site + export + mutant + DB sintetică→pytest→UCIS/VIU/NERULAT→test_clasa.',
'A00 verde și mutant ucis de aserțiune concretă; fiecare caz are SHA și stare DB pe conexiune nouă. Fără contaminare între mutanți.',
'A00 roșu invalidează score; collection/import/setup/timeout nu se confundă cu mutant ucis doar pentru rc1. Export parțial, credential real și container permisiv blochează proba.',
'rsync --delete, scratch mutanți, loguri și scrieri DB numai în laborator. Niciun exec Docker pe sistemul operațional.',
'TestReport structurat și etapă, assertion exactă, snapshot DB/retry, docker inspect pentru rețea/mounturi și audit de ieșire.',
'Comentariul network none nu este izolare probată; toate env secret sunt sintetice și nu sunt tipărite. Comparatorul remapat rămâne etichetat distinct.'
],
'test_clasa_lot_b_r1.sh':[
'SHA EVA + SHA site→arhivă/gardă/canar→trei seturi runner→verdict CLASĂ.',
'Mulțimea completă a mutanților coincide cu rezultatele; control verde și canar detectat fără HTTP.',
'--fara-mutanti este parțial. Rapoarte vechi/trunchiate, A00 duplicat, runner întrerupt și set gol se resping. A02/A07 vii cer dovadă de echivalență, nu listă nominală.',
'Scratch/arhivă/loguri și efectele runnerului doar în laborator; cleanup confirmat extern.',
'Set așteptat↔raportat și legătura la execuția curentă; nu grep pe un fișier rămas din altă rundă.',
'Rădăcina hardcodată operațional face execuția ca atare interzisă. Dacă remaparea nu e sigură, originalul rămâne NERULAT.'
],
'proba_buton.py':[
'AD_Menu/AD_Form + JAR/E/Manual + helper T331→UI nativ→raport/capturi→judecător.',
'Pe clonă sintetică: meniu→formă→Ajutor→închidere; RO→EN→RO în UI și DB pe conexiune nouă. Separat partea pură cu JAR fixture cunoscut.',
'Rețea neinternă/JAR greșit, menu inaccesibil, tab ambiguu, erori ZK, imagine coruptă, timeout și abandon după EN. --doar incomplet nu reduce populația oficială. Canar nemascat blochează captura.',
'Scrie artefacte și limba în DB sintetică. Verifică utilizatorul/rolul explicit: ID 1000000 hardcodat nu este universal. Browserul și preferințele se restituie.',
'Peer compară DOM/capturi decodate și AD_* pe conexiune nouă. Așteptările din același JAR nu sunt singurul oracol; manifest pe aceeași execuție.',
'rc0 înseamnă colectare fără motiv tehnic, nu conformitate. Rețeaua internă Docker nu izolează browserul gazdă/redirecturile. Ajutorul ZK este separat de portal KB.'
],
'test_clasa_verifica_proba.py':[
'Judecător original + fixture temporare→cazuri R1–R11→mutanți→rezultate separate.',
'Control complet are 13 RO/10 EN TEXTE plus Perioade EN conform codului, nu 12 din docstring. Fiecare caz și mutant are identitate.',
'Modul mutant invalid/ancoră ambiguă=NERULAT. Original roșu invalidează mutation score. --fara-mutanti este parțial; probe independente cu E dublu, en-min negativ și tip MANUAL arbitrar.',
'Fișiere temporare și mutanți numai în scratch; finally cleanup verificat independent.',
'Comparator separat al cazurilor/așteptărilor și martori care nu folosesc aceleași funcții rand_texte.',
'Bytes jpg sunt sintetici și nu imagini reale. Trecerea suitei nu recepționează UI, imaginile sau securitatea colectorului. Cazul caz_fisier_nu creează un nume cu două puncte, invalid pe Windows: preflight OS obligatoriu. Preferă POSIX sintetic; selecția cazurilor compatibile ori adaptorul de nume rămân parțiale și declarate separat, fără verdict de defect al produsului din limita OS.'
],
'verifica_proba.py':[
'35 coloane raport + E + capturi→R1–R11/numitori→A12/A11.',
'Raport complet construit independent și fiecare regulă stricată separat; tipuri TEXTE/MANUAL/REGES și prag EN/Perioade.',
'Rând lipsă/dublu, limbă necunoscută, antet ilizibil, E gol/dublu, prag negativ și lipsă Perioade. Așteptat/afișat falsificate identic și captură nonempty falsă cer oracol suplimentar.',
'Citire raport/capturi și stdout nou; niciun efect business ori DB.',
'Proveniență independentă și reconstrucție a așteptărilor; decode imagini, containment cale, SHA și identitate de execuție. Raportul vechi cu alte capturi se respinge.',
'R10 verifică existență/mărime, nu autenticitate/decode. Căi absolute/../ trebuie blocate de preflight. rc0 este conformitate internă de raport, nu recepție nativă completă.'
]}
preflight=[
'Nicio execuție, import, compilare, --help, shell sau test de cod candidat înainte de planul R12 aprobat independent 10/10 pe SHA exact. Citirea și hasharea pentru plan sunt singurele operații deja realizate.',
'Inventariază cwd, căi hardcodate, interpolări shell, variabile, imports, subprocess, refs Git, containere, volumes și rețele; validează valorile efective înainte de execuție.',
'Orice destinație operațională rămasă, credential real ori symlink/junction care evadează din scratch blochează proba. Nu se execută rețete pe saga-server.',
'Păstrează originalul la OID și comparatorul remapat într-o cale nouă, cu patch și limită. Nu raporta comparatorul drept execuție originală integrală.',
'Mutații/ștergeri numai într-un scratch nou deținut, verificat absolut sub rădăcina laboratorului; nu pe repo, surse, arhive sau rapoarte sigilate.',
'Pentru nativ reutilizează cabinet_help/captureaza_ecrane și lifecycle existent, dar seed pur sintetic. Restore/HTTP/OSGi/JAR/DB sunt verificate independent; timeout epuizat și exit0 nu dovedesc readiness.',
'Fără trafic către parteneri: verifică separat containere, browser gazdă, DNS, redirecturi, subprocess și mounts. Audit hook Python sau comentariu network none nu constituie singur sandbox.',
'Dovezi append-only în dosar nou per rulare; stări înainte/după/retry, cleanup pe succes/eșec/timeout verificat în afara runnerului. Restituie toate resursele proprii.',
'Păstrează separat inventariere, lectură, execuție originală/comparator, persistență, peer și A11. OID egal nu transferă probe în context nou. Cele 17 contracte complete rămân deschise.'
]
items=[]
for x in I['rows']:
 f=R/x['path'];b=f.read_bytes();assert hashlib.sha256(b).hexdigest()==x['sha256']
 a=json.loads(b.decode('utf-8-sig'));name=Path(a['source']['path']).name;s=S[name];src=Path(s['local']).read_bytes()
 assert hashlib.sha256(src).hexdigest()==s['sha256']==a['source']['sha256']
 assert hashlib.sha1(('blob '+str(len(src))+'\0').encode()+src).hexdigest()==s['new_oid']==a['source']['git_object']
 n=N[name]
 control=C[a['source']['path']]
 assert a['assignment']['owner']==control['owner'] and a['assignment']['peer']==control['peer']
 items.append({'source':a['source'],'assignment':a['assignment'],'task':a['task'],'A12_file_plan':{'path':x['path'],'sha256':x['sha256']},'role':a['objective'],'actor':a['actor'],'normal_entry_and_fixture':a['fixture'],'native_reuse':a['native_reuse'],'pipeline_producer_consumer':n[0],'positive':n[1],'counterexamples':n[2],'persistent_effect':n[3],'independent_oracle':n[4],'limit':n[5],'cleanup':a['postcondition'],'result':None,'peer_receipt':None,'status':'LECTURĂ PENTRU PLAN; ZERO EXECUȚII CANDIDAT','lines_read':len(src.decode('utf-8-sig').splitlines()),'A12_dependencies':a['dependencies'],'A12_consumers':a['consumers']})
for a in items:a['audit_control_id']=C[a['source']['path']]['id']
assert len(items)==len(N)==19
obj={'schema':'eva.audit.r12.A10.new-instruments.plan.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'author':'A10 · anexa instrumentelor noi','candidate':M['head'],'base':'2fe90ed3f128c33dff7cf9f8674e664a70679390','state':'PLAN NEAPROBAT; EXECUȚIA AȘTEAPTĂ POARTA A11 10/10','score':None,'input_anchors':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in ['executie/R12_plan_delta/Manifest_sources_lues.json','executie/R12_plan_delta/A12/Index_19_fise.json','executie/R11_fisiere/A11/Checklist_A11_dupa_val04_v1.json']},'scope':{'new_instruments':19,'tools':3,'promoted_Documentatie':16},'mandatory_preflight':preflight,'portal_boundary':'Ajutorul nativ ZK T240 este separat de portal eva-help-kb.json. Aceste instrumente nu închid constatarea R11 privind 16 rute fără articol dedicat.','receipt_rule':'Fiecare rezultat are cerință, actor, nativ, pozitiv, contraexemplu, persistență ori neaplicabilitate justificată, limită și peer. A11 decide separat asupra planului și execuției; exit0 sau absența constatării nu produc OK semantic.','items':items,'authoring_QA':{'sources_read_and_rehashed':19,'git_blob_ids_recomputed':19,'A12_sheets_rehashed':19,'candidate_executions':0,'results_assigned':0}}
j=P/'Plan_instrumente_noi_A10_v1.json';j.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
e=html.escape
out=['<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Plan R12 · 19 instrumente noi</title><style>body{font:16px/1.55 system-ui;max-width:1050px;margin:28px auto;padding:0 18px;color:#183044}code{overflow-wrap:anywhere}article{border-top:2px solid #b5cad5;margin-top:26px;padding-top:14px}dt{font-weight:700;margin-top:12px}dd{margin-left:0}li{margin:8px 0}.gate{background:#fff2cd;padding:18px}a{color:#08538f}</style><h1>Plan R12: cele 19 instrumente noi</h1><p class="gate"><b>Plan neaprobat. Zero execuții pe noul HEAD.</b> Sursele au fost citite și identitățile Git/SHA256 recalculate pentru plan. Execuția așteaptă recepția independentă 10/10.</p>',f'<p>Candidat: <code>{e(M["head"])}</code>. Bază: <code>{obj["base"]}</code>.</p><p>3 instrumente din tools/teste și 16 promovate din Documentatie. Repartizarea și taskurile canonice se păstrează din inventarul A12.</p><h2>Preflight obligatoriu</h2><ol>']
out += ['<li>'+e(p)+'</li>' for p in preflight];out+=['</ol><p>'+e(obj['portal_boundary'])+'</p>']
labels={'role':'Rol','actor':'Actor','normal_entry_and_fixture':'Intrare și fixture','native_reuse':'Reutilizare nativă','pipeline_producer_consumer':'Producător → consumator','positive':'Probe pozitive propuse','counterexamples':'Contraexemple propuse','persistent_effect':'Efect persistent','independent_oracle':'Oracol independent','limit':'Limită','cleanup':'Restituire resurse'}
for i,a in enumerate(items,1):
 out += [f'<article id="f{i}"><h2>{i}. {e(Path(a["source"]["path"]).name)}</h2><p><code>{e(a["source"]["path"])}</code><br>OID: <code>{a["source"]["git_object"]}</code><br>SHA256: <code>{a["source"]["sha256"]}</code></p><p><b>Task:</b> {e(a["task"]["canonical"])}; <b>responsabil:</b> {e(a["assignment"]["owner"])}; <b>peer:</b> {e(a["assignment"]["peer"])}. Control: {e(a["assignment"]["control"])}.</p><dl>']
 for k,label in labels.items():out+=['<dt>'+label+'</dt><dd>'+e(a[k])+'</dd>']
 out+=['</dl><p><b>Stare:</b> lectură pentru plan; rezultat și recepție neatribuite.</p></article>']
out+=['<p>'+e(obj['receipt_rule'])+'</p></html>']
h=P/'Plan_instrumente_noi_A10_v1.html';h.write_text('\n'.join(out),encoding='utf-8')
for p in [j,h]:print(p.name,hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size)
