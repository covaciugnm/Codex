from pathlib import Path
import json,hashlib,datetime,shutil
B=Path(r'\\192.168.100.169\Comun\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01\executie\R12_fisiere')
S=B/'A09_Date_Masini_lot02';O=B/'A01_Peer_Masini_lot02';O.mkdir(exist_ok=True)
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();R=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
assert not (O/'Peer_A01_Masini_lot02.json').exists()
manifest=S/'MANIFEST_SHA256.json';assert H(manifest)=='ff071b46603712874805c53a024d5d4f8fccf7fedd5fb988dfb338d17f5059db'
m=R(manifest);verified=[]
for x in m['files']:
 p=S/x['path'];assert p.is_file() and H(p)==x['sha256'] and p.stat().st_size==x['bytes'];verified.append(x['path'])
for name,oid in [('WSagaMasiniForm.java','54a504e5f5cc1d536dae4c4f567d84f01703c2e5'),('WSagaCrudForm.java','d1364d45367f91cee732667fcbc57110216d8487')]:
 b=(S/name).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid
assert (S/'Git_WSagaMasiniForm.class').read_bytes()==(S/'Installed_WSagaMasiniForm.class').read_bytes()
cases=R(S/'Cases_normalized.json');counts=[]
for run in cases:
 lines=(S/(run['execution']+'.stdout.txt')).read_text('utf8').splitlines();raw=[l.split('\t') for l in lines if l.startswith('CASE\t')]
 assert len(raw)==len(run['cases'])==12
 for a,c in zip(raw,run['cases']):
  assert int(a[1])==c['case'] and a[2]==c['input'] and a[3]==c['expected'] and a[4]==c['actual'] and a[5]==c['jdk_uuuu_comparator'] and (a[6]=='true')==c['product_matches_expected']
 positive=[c for c in run['cases'] if c['expected']!='null'];negative=[c for c in run['cases'] if c['expected']=='null']
 assert len(positive)==5 and all(c['actual']=='null' and not c['product_matches_expected'] for c in positive)
 assert len(negative)==7 and all(c['actual']=='null' and c['product_matches_expected'] for c in negative)
 counts.append({'execution':run['execution'],'unique_inputs':12,'valid_rejected':5,'invalid_format_or_calendar':4,'empty_space_or_null':3})
refs=['Fisa_Masini_date.json','Sursa.json','Caller_source.json','WSagaMasiniForm.java','WSagaCrudForm.java','Cases_normalized.json','compiled_source.stdout.txt','git_jar.stdout.txt','Binding_instalat.json','Cleanup.json','Compile_receipt.json','Execution.json','MasiniParserWitness.java','Git_WSagaMasiniForm.class','Installed_WSagaMasiniForm.class']
report={
'schema':'A01_PEER_SEMANTIC_MASINI_LOT02_v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A01','owner':'A09 / executor root','head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','finding':'R12-MASINI-DATE-01','controls':['A01.C13','A09-C04'],'pipeline':'A09-P1 subset parser / legături statice CRUD','canonical_task':None,'task_mapping':'SHARED_NO_TASK_ASSIGNED; T240 este semnal/context, fără atribuire nominală sau închidere de task.',
'scope':'Peer semantic și de cod, strict citire a lotului sigilat. Nicio rerulare Java/produs, niciun PO/UI/SQL executat de A01; reproducerea independentă și recepția globală aparțin A11.',
'input_manifest':{'path':str(manifest),'sha256':H(manifest),'verified_file_count':len(verified),'all_hashes_and_sizes_match':True},
'references':[{'path':str(S/p),'sha256':H(S/p)} for p in refs],
'verdict':'ACCEPTAT_SEMANTIC_CU_PRECIZĂRI; fără notă de audit și fără recepție integrală a fișierului sau a funcției business.',
'checks':[
 {'id':'M01','result':'CONFIRMAT','observed':'OID-urile ambelor surse au fost recalculate din bytes, nu doar preluate din fișă; toate cele33 fișiere ale manifestului coincid ca hash și dimensiune.'},
 {'id':'M02','result':'CONFIRMAT_STATIC','anchors':['WSagaMasiniForm.java:24-26','WSagaMasiniForm.java:240-247'],'observed':'ofPattern dd.MM.yyyy produce YearOfEra; STRICT fără eră nu rezolvă LocalDate pentru datele pozitive consemnate. Catch-ul DateTimeParseException întoarce null. Explicația cauzală corespunde sursei și rezultatelor, fără a necesita un parser nou.'},
 {'id':'M03','result':'CONCORDANȚĂ_DOVEZI','observed':'Cases_normalized coincide câmp-cu-câmp cu stdout pentru fiecare din cele două execuții. 12 cazuri unice repetate în două contexte =24 evaluări;5 date valide refuzate în fiecare context;4 formate/date imposibile și3 absențe/blank/null conforme contractului parserului. Nu sunt7 date calendaristice invalide și nici24 scenarii independente.','counts':counts},
 {'id':'M04','result':'CONFIRMAT_STATIC','anchors':['WSagaMasiniForm.java:33-45','WSagaMasiniForm.java:217-227','WSagaCrudForm.java:964-976','WSagaCrudForm.java:1088-1096','WSagaCrudForm.java:1118-1134'],'observed':'Cele7 scadențe sunt Camp.TEXT; editorul pop-up întoarce text trim-uit, valoareCamp implicit îl păstrează, iar hook-ul inainteDeSalvare precede saveEx în ambele căi. Pentru text calendaristic valid nevid care ajunge în PO, parseData null produce excepție înaintea saveEx; acesta este efect static, nu salvare UI observată.'},
 {'id':'M05','result':'CONFIRMAT_STATIC','anchors':['WSagaMasiniForm.java:201-212','WSagaMasiniForm.java:234-237'],'observed':'stilCelula folosește același parser și revine fără clasă de culoare când acesta întoarce null. textColoana face trim: cazul direct cu un spațiu din harness nu probează că UI ar refuza câmpul opțional gol; hook-ul îl acceptă după normalizare.'},
 {'id':'M06','result':'CONFIRMAT_BYTES_LOCAL','observed':'Clasa extrasă din JAR Git și clasa extrasă din JAR instalat sunt byte-identical, SHA256090e6340dc6a817e68fee4ab5aae854033652ac0a4a71f738249134ac479f8de. JAR-urile complete au hashuri diferite; egalitatea clasei nu dovedește ce clasă este încărcată în JVM live, activarea formularului sau existența datelor reale afectate.'},
 {'id':'M07','result':'PRECIZARE_DE_NIVEL','observed':'Clasa recompilată din sursă are alt SHA256 decât clasa din JAR. Fișa nu trebuie interpretată ca egalitate binară recompilare/JAR; cele două execuții consemnate au rezultate funcționale identice pentru cele12 intrări. Codul sursă recompilat este verificat ca OID exact.'},
 {'id':'M08','result':'LIMITE_CORECTE','observed':'Harnessul invocă metoda statică privată prin reflecție, fără instanțiere PO. Exit0 înseamnă finalizarea experimentului; nu înseamnă că cele5 așteptări pozitive au trecut. SecurityManager are checkPermission permisiv; cele4 canari validați nu îl transformă în sandbox OS ori gardă rezistentă la cod ostil.'},
 {'id':'M09','result':'RESPECTAT','observed':'Cleanup.json consemnează refuzul automat al ștergerii, scratch păstrat și0 procese Java la acel moment. A01 nu a șters, nu a relansat procese și nu a încercat o cale alternativă de cleanup. Nu afirmăm că directorul este eliminat sau o verificare nouă a proceselor live.'}],
'severity_review':{'proposed':'P1_PROPUS','peer_position':'REZONABIL_CA_PRIORITATE_DE_REMEDIERE, CU_CALIFICARE','reason':'Parserul comun respinge inclusiv exemplul recomandat utilizatorului și este traversat de ambele căi normale de salvare pentru toate cele7 scadențe. Impactul nu este doar cosmetic: blocarea salvării este o implicație statică directă. P1 nu trebuie prezentat ca incident operațional observat sau defect de acces/tenant demonstrat.','not_demonstrated':['incident de producție','pierdere/corupere de date','ocolire de autorizare','expunere cross-tenant'],'independent_final_priority_owner':'A11/coordonator'},
'constructive_clarifications':[
'Hook-ul validează toate scadențele, nu numai câmpul editat. Din cod rezultă că și editarea altui câmp al unui rând care conține deja o scadență validă ar putea fi blocată; de confirmat ulterior prin PO/UI, fără a pretinde că s-a executat acum.',
'Cele7 cazuri conforme conțin4 intrări calendaristice/formate invalide și3 intrări goale/spațiu/null. Parserul acceptă absența prin null; validarea din caller permite explicit golul.',
'În Cases_normalized intrarea null este redată ca șirul "null". Harnessul sursă demonstrează că este valoarea Java null, nu literalul text "null"; păstrați această distincție în orice raport sintetic.',
'Corectarea cu uuuu este o propunere, nu o remediere aplicată. Stabiliți domeniul anilor: proleptic-year permite semantic anul0 și ani negativi; nu extindeți accidental domeniul business față de cerința zz.ll.aaaa.',
'Nu schimbați mecanic Camp.TEXT în Camp.DATA: editorul existent Datebox produce Timestamp, în timp ce textColoana/parsing și coloanele importate folosesc text. Reutilizarea editorului nativ cere conversie compatibilă și verificarea datelor existente.'
],
'native_first_recommendation':'Corectați formatterul JDK deja folosit păstrând STRICT; alternativ declarați explicit era dacă domeniul ales cere YearOfEra. Mențineți hook-urile CRUD existente, PO.saveEx și tranzacțiile iDempiere. Nu adăugați SQL paralel sau un nou mecanism de persistență. Pe clonă, verificați cele7 câmpuri în ambele editoare, text gol/valid/imposibil/importat, eroare lizibilă, păstrarea valorilor, rollback și marcajele trecut/azi/30zile/viitor.',
'coverage_limits':['A01.C13/A09-C04 primesc doar creditul semantic al acestui subset; nu este audit integral de IDOR/tenancy/roluri.','Nu există probe UI sau PO/DB create de A01 în această revizie.','Binding_instalat este recepționat ca dovadă de bytes extrasă anterior de executor; A01 nu a recitit serverul operațional.','Nici WSagaCrudForm și nici dependențele nu primesc verdict integral din lectura punctelor de apel.','A11 trebuie să consemneze separat reproducerea și recepția.'],
'mutation_summary':{'source_lot_modified':False,'product_execution_count':0,'production_access_count':0,'cleanup_attempt_count':0,'subagents_started':0,'tasks_closed':0}}
# Make spacing in explanatory prose explicit while preserving identifiers/hashes.
for item in report['checks']:item['observed']=item['observed'].replace('cele33','cele 33').replace('cele7','cele 7').replace('cele12','cele 12').replace('cele5','cele 5').replace('cele4','cele 4').replace('SHA256090','SHA256 090').replace('și0','și 0')
(O/'Peer_A01_Masini_lot02.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
shutil.copyfile(Path(__file__),O/'verificare_metadate_fara_rerulare.py')
files=[{'path':p.name,'sha256':H(p),'bytes':p.stat().st_size} for p in sorted(O.iterdir()) if p.is_file() and p.name!='MANIFEST_SHA256.json']
(O/'MANIFEST_SHA256.json').write_text(json.dumps({'head':report['head'],'reviewer':'A01','input_manifest_sha256':H(manifest),'files':files},indent=2),encoding='utf8')
assert all(H(O/x['path'])==x['sha256'] for x in files)
assert H(manifest)=='ff071b46603712874805c53a024d5d4f8fccf7fedd5fb988dfb338d17f5059db'
print(json.dumps({'report_sha256':H(O/'Peer_A01_Masini_lot02.json'),'manifest_sha256':H(O/'MANIFEST_SHA256.json'),'input_verified_files':len(verified),'verdict':report['verdict']},ensure_ascii=True))
