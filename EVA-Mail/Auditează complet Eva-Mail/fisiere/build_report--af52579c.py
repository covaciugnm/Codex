import pathlib,json,html,hashlib
r=pathlib.Path(__file__).resolve().parent
findings=[]
def add(id,sev,title,proof,impact,fix,accept,refs):
 findings.append(dict(id=id,severity=sev,title=title,evidence=proof,impact=impact,remediation=fix,acceptance=accept,references=refs))
add('A01','P0','Izolarea utilizatorilor permite coliziuni de schemă',
'Funcția reală get_schema_name a fost executată izolat: a.b@example.com și a-b@example.com produc aceeași schemă; ab@example.com și a+b@example.com de asemenea. Trunchierea produce o a treia coliziune pentru adrese lungi. Înregistrarea folosește CREATE SCHEMA IF NOT EXISTS, iar listarea contactelor selectează Contact fără filtru user_id.',
'Două identități diferite pot ajunge în același spațiu de date. Demonstrația verifică funcțiile reale și traseul din cod; nu am creat conturi în producție și nu am citit datele altui utilizator. Înregistrarea efectivă a perechilor trebuie verificată într-un mediu de test.',
'Identificator tenant UUID imuabil, registru cu unicitate, autorizare explicită și ideal RLS. Inventariere controlată a coliziunilor existente înainte de migrare; nu redenumiți schemele automat fără maparea proprietarilor.',
'Două conturi cu fiecare pereche de adrese au scheme distincte și nu pot citi/modifica contacte, emailuri, proiecte sau facturi reciproc; testare inclusiv după schimbarea adresei.',
['source/backend/app/api/deps.py:19','source/backend/app/api/v1/endpoints/auth.py:57','source/backend/app/api/v1/endpoints/auth.py:137','source/backend/app/api/v1/endpoints/contacts.py:38','security-reproductions.json'])
add('A02','P0','SQL generat de AI poate depăși datele autorizate',
'Validatorul real acceptă SELECT email, hashed_password FROM public.users și SELECT pg_read_file(...); respinge DELETE. Interogările au fost validate offline, NU executate. Codul concatenează un CTE all_emails, însă nu obligă SELECT-ul să folosească acel CTE. Backendul are utilizator DB openfyxer; rolul este superuser.',
'Tranzacția read-only previne scrierea, dar nu citirea altor scheme sau apelarea funcțiilor privilegiate. Un SQL greșit sau indus prin prompt poate accesa date în afara utilizatorului. Nu s-a demonstrat un atac complet prin interfața AI.',
'Eliminați superuser din aplicație. Executor separat cu rol read-only restrâns la vederi autorizate; parser SQL cu allowlist de relații și funcții, buget de rânduri/timp, fără acces la public.users sau fișiere. Autorizarea trebuie impusă în DB, independent de prompt.',
'Teste negative pentru scheme străine, public.users, pg_catalog sensibil, funcții de fișiere, CTE/subquery și prompt injection; fiecare este refuzat chiar dacă modelul îl generează.',
['source/backend/app/api/v1/endpoints/eva_chat.py:774','source/backend/app/api/v1/endpoints/eva_chat.py:1057','extended-checks.json','db-role-check.json','runtime-audit.json'])
add('A03','P1','Refresh token acceptat ca access token',
'get_current_user nu impune payload.type == access. Harness-ul cu payload refresh valid sintetic, user activ și sesiune validă este acceptat de funcția reală. Semnătura JWT a fost simulată în test; nu afirm că un JWT nesemnat este acceptat.',
'Separarea dintre tokenurile de acces și reînnoire este încălcată; un refresh token poate fi utilizat direct la rutele protejate.',
'Validare explicită tip, issuer, audience și scop; separarea cheilor/audiențelor unde este justificată; rotație refresh cu detectarea reutilizării.',
'Toate rutele protejate refuză refresh tokens; access valid funcționează; token expirat, revocat, cu tip/issuer/audience greșit este refuzat.',
['source/backend/app/api/deps.py:29','source/backend/app/api/v1/endpoints/auth.py:1229','security-reproductions.json'])
add('A04','P1','Revocarea sesiunii nu este impusă când Redis nu răspunde',
'session_exists returnând None este acceptat de get_current_user în testul izolat; este respins doar False. Endpointul refresh folosește o verificare similară.',
'În timpul indisponibilității Redis, verificarea revocării devine permisivă. Nu este dovadă că Redis a fost indisponibil la audit.',
'Refuz controlat cu 503 sau verificare într-un depozit durabil; documentați explicit compromisul de disponibilitate. Nu tratați o eroare de infrastructură drept sesiune validă.',
'Cu Redis indisponibil, tokenul revocat nu primește acces; răspuns predictibil și alertă, fără valuri de retry.',
['source/backend/app/api/deps.py:81','source/backend/app/api/v1/endpoints/auth.py:1254','security-reproductions.json'])
add('A05','P1','Verificarea certificatului IMAP este dezactivată',
'Listenerul setează check_hostname=False și verify_mode=CERT_NONE atât pe ramura autentificării clasice, cât și OAuth; există configurații similare în email_service.',
'Conexiunea criptată nu autentifică serverul de email. Un intermediar cu acces la traseul de rețea poate intercepta autentificarea sau mesajele. Nu s-a efectuat MITM.',
'Verificare TLS obligatorie; CA intern explicit pentru servere private, fără fallback global CERT_NONE; erori clare pentru certificat expirat/nume diferit.',
'Serverul de test cu certificat expirat, self-signed neaprobat sau hostname greșit este refuzat; CA aprobat funcționează.',
['source/backend/app/workers/imap_listener.py:97','source/backend/app/workers/imap_listener.py:114','source/backend/app/services/email_service.py:4251'])
add('A06','P1','Electron permite schimbarea originii fără validarea expeditorului IPC',
'Preload expune setUrl; eva:set-url acceptă orice http(s), ignoră event/sender și reîncarcă taburile. Datele de autentificare sunt legate de partiție, nu de origine. Preload completează câmpurile email/password folosind parola salvată.',
'O pagină compromisă care poate utiliza bridge-ul poate redirecționa taburile către o origine controlată și poate provoca completarea parolei. Este un lanț dedus din cod, netestat cu parole reale.',
'Permiteți schimbarea serverului doar din fereastra locală de setări verificată prin senderFrame și URL exact; HTTPS și allowlist de origini; secrete legate de origine și cont; nu completați parole pe o origine schimbată.',
'Un renderer web și un iframe neautorizat nu pot schimba serverul; pagina externă cu câmpuri email/password nu primește secrete; migrarea serverului cere un flux explicit de reconectare.',
['main.js:853','main.js:811','preload.js:59','preload.js:207'])
add('A07','P1','Suprafață mare de compromitere a gazdei prin backend',
'Backendul rulează uid 0 și are /var/run/docker.sock montat RW; codul sursă este montat de pe gazdă. Și deerflow are socket RW. Containerele inspectate nu erau privileged, ceea ce nu neutralizează accesul la daemon.',
'O vulnerabilitate de execuție în backend poate permite controlul daemonului Docker și implicit al gazdei. Acesta este impact potențial, nu dovadă de compromitere.',
'Eliminați socketul din backend; serviciu de orchestrare separat cu operații strict permise. Utilizator fără privilegii, filesystem read-only unde posibil, cap_drop și no-new-privileges; secrete și volume minime.',
'Backendul nu poate lista/crea containere și nu poate scrie sursa gazdei; funcțiile legitime de orchestrare funcționează prin API limitat.',
['server-baseline.json','db-role-check.json'])
add('A08','P1','Rotația backupurilor poate păstra doar un dump de schemă',
'Scriptul aplică rotația tuturor openfyxer_*.sql.gz.enc inclusiv când MODE=schema. La pragul 4 șterge tot în afară de fișierul curent. Logul zilei confirmă că după backupul full curent au fost șterse cele trei full precedente.',
'Un backup schema-only executat la prag poate elimina copiile full din această serie. Chiar fără acest scenariu, retenția scade periodic la un singur punct de restaurare. Nu s-a executat scriptul și nu s-a șters nimic în audit.',
'Retenție separată full/schema, păstrare zilnică/săptămânală/lunară, fișier temporar și rename atomic după validare; restaurare verificată înainte de expirarea copiilor; copie offsite și cheie recuperabilă separat.',
'Test într-un director temporar cu 3 full + 1 schema păstrează full-urile conform politicii. Restaurare integrală pe server separat și măsurare RPO/RTO.',
['source/scripts/backup_db_encrypted.sh','runtime-audit.json','ops-checks.json'])
add('A09','P1','Instalarea reproductibilă a frontendului eșuează',
'npm ci --ignore-scripts --no-audit --no-fund pe copia sursei eșuează EUSAGE: manifestul și lockfile-ul nu sunt sincronizate; lipsesc inclusiv docx-preview, dompurify, xlsx și dependențe tranzitive.',
'Un build curat nu poate fi reprodus prin fluxul standard. O instanță deja pornită nu dovedește că release-ul poate fi reconstruit sau recuperat.',
'Regenerați lockfile în mediu controlat cu versiuni Node/npm fixate; revizuiți schimbările; build de la zero și publicare de artefacte imuabile cu commit și digest.',
'Checkout curat → npm ci → test → build fără modificarea lockfile și fără dependență de node_modules existent.',
['npm-ci.log','source/frontend/package.json','source/frontend/package-lock.json'])
add('A10','P1','Providerul de coverage este un stub fără măsurare',
'@vitest/coverage-v8 este rezolvat la vendor/coverage-v8; provider.name este local-v8-stub, iar initialize, takeCoverage și reportCoverage nu colectează sau emit acoperire.',
'Un job care cere coverage poate trece fără a demonstra acoperirea. Nu presupun că un procent concret raportat anterior este fals; mecanismul prezent nu îl poate justifica.',
'Înlocuiți cu provider oficial compatibil cu Vitest; praguri relevante și upload obligatoriu de raport nevid; test că încălcarea pragului face jobul să eșueze.',
'Raportul conține fișiere și linii reale; eliminarea unui test relevant reduce acoperirea și poate bloca CI.',
['source/frontend/vendor/coverage-v8/index.js','source/frontend/package.json'])
add('A11','P1','Dependențe semnalate și release fără gate de teste în workflow',
'npm audit pe lockfile raportează 32 noduri de pachete afectate: 2 critical, 23 high, 6 moderate, 1 low. Include unelte de dezvoltare, precum Vitest/tinypool. release.yml construiește și publică la tag v* fără job de teste de care să depindă.',
'Numărul nu înseamnă 32 exploatări în browser și nu reprezintă un scan complet al imaginilor/backendului. Workflow-ul poate publica independent de validarea CI; regulile externe GitHub nu au putut fi verificate, repository-ul returnând 404.',
'Triage runtime/dev și reachability; actualizări țintite, fără npm audit fix --force automat. SBOM frontend/backend/imagine; release pe commit verificat, required checks și digest; verificați și dependențele Python și imaginea NVIDIA.',
'Build curat, scan documentat, zero constatări critice exploatabile neacceptate; tagul unui commit cu teste eșuate nu publică release.',
['npm-audit.json','source/.github/workflows/release.yml','source/.github/workflows/ci.yml'])
add('A12','P1','Sanitizarea emailului are fallback nesigur',
'sanitizeEmailHtml folosește DOMPurify normal, dar în catch elimină doar tagurile script și returnează restul HTML. Atribute precum onerror rămân. HTML este introdus cu innerHTML în Shadow DOM. Răspunsul HTML live nu are CSP.',
'Dacă sanitizatorul aruncă o excepție, conținutul neîncredere poate ajunge activ în DOM. Excepția nu a fost provocată în producție; Shadow DOM nu izolează execuția JavaScript.',
'La eroare afișați text escapate sau mesaj de eroare, niciodată HTML brut; CSP compatibilă cu produsul și teste pentru toate locurile care afișează emailuri.',
'Mock DOMPurify care aruncă: payload cu img/onerror este afișat inert; teste XSS pentru Inbox și Projects, linkuri și SVG.',
['source/frontend/src/components/email/SafeEmailContent.tsx:7','http-probes.json'])
add('A13','P1','Registrul de probleme este accesibil public',
'GET /api/v1/probleme fără autentificare returnează 200 cu 48 de înregistrări și aproximativ 81 KB. Codul PUT/POST nu are dependență de autentificare. Comentariile indică o alegere intenționată anterioară.',
'Expunere publică de detalii interne și posibilitate de alterare/creare conform codului. Nu am apelat PUT/POST și nu am modificat registrul.',
'Decideți explicit dacă este pagină publică de status. Separați datele publicabile de registrul intern; toate mutațiile necesită rol autorizat, audit și rate limit.',
'Anonim vede doar rezumatul public aprobat; POST/PUT anonim sunt 401/403, utilizator fără rol este refuzat.',
['source/backend/app/api/v1/endpoints/probleme.py:522','source/backend/app/api/v1/endpoints/probleme.py:533','source/backend/app/api/v1/endpoints/probleme.py:564','http-probes.json'])
add('A14','P2','Tokenurile tuturor conturilor sunt persistate în localStorage',
'authStore folosește persist și păstrează token/refreshToken în lista conturilor.',
'Un XSS pe aceeași origine poate afecta mai multe conturi și tokenuri de durată lungă. Stocarea este o alegere arhitecturală cu impact amplificat de A12, nu dovada unui furt.',
'Refresh în cookie HttpOnly/Secure/SameSite adecvat și protecție CSRF; access în memorie; revocare/rotație, expirare și curățare la logout pentru toate conturile.',
'JavaScript din pagină nu poate citi refresh token; logout revocă efectiv sesiunea, iar schimbarea contului nu amestecă date/cache.',
['source/frontend/src/store/authStore.ts:89'])
add('A15','P1','Memorie foarte aproape de capacitatea gazdei',
'Gazda are aproximativ 122 GiB RAM, 5,7–6,9 GiB disponibili în instantaneele auditului și fără swap. Backend/frontend/worker nu au limite Docker de memorie; Redis maxmemory=0. Nu am rulat teste de încărcare pe producție.',
'Modelele AI și taskurile concurente pot epuiza memoria, cu efect asupra emailului și DB pe aceeași gazdă. Nu s-a observat sau demonstrat un OOM în această verificare.',
'Bugete pentru modele/workeri, limite validate prin test de sarcină, backpressure și cozi separate; protecția DB; alertare pe available memory, OOM, latență și backlog. Swap se decide conform platformei, nu ca substitut pentru capacity planning.',
'Test de sarcină pe staging cu volum realist, p95/p99 și SLO convenite, fără OOM și fără creștere necontrolată a cozilor.',
['server-baseline.json','ops-checks.json','runtime-audit.json'])
add('A16','P2','Servicii de modele accesibile fără autentificare în LAN',
'Porturile 11435 și 11436 ascultă pe 0.0.0.0; /api/tags răspunde fără autentificare cu 8 modele pe fiecare. Nu am generat inferențe și nu am probat expunerea din internet.',
'Clienții LAN care ajung la porturi pot cel puțin inventaria modelele; alte operații necesită verificare separată. Suprafața de acces depășește backendul.',
'Bind pe loopback/rețea internă Docker sau firewall restrictiv; autentificare dacă serviciul trebuie accesat din rețea; cote pentru operații costisitoare.',
'Client LAN neautorizat nu poate accesa API-ul; backendul autorizat continuă să funcționeze.',
['http-probes.json','server-baseline.json'])
add('A17','P2','Limitarea pe IP are încredere în headere neverificate',
'Funcția reală get_client_ip întoarce CF-Connecting-IP furnizat de client fără verificarea proxy-ului. Intrarea directă LAN pe portul 3000 ajunge la API.',
'Cheia de rate limit pe IP poate fi influențată de apelant pe traseele directe. Există și limitare pe email, deci nu afirm ocolirea tuturor controalelor anti-bruteforce.',
'Acceptați headerele doar de la proxy-uri de încredere; eliminați accesul direct sau normalizați headerele la primul proxy; păstrați limitarea pe cont și sesiune.',
'Headere falsificate de un peer neautorizat nu schimbă identitatea IP folosită de limitator.',
['source/backend/app/api/deps.py:155','security-reproductions.json','http-probes.json'])
add('A18','P2','Politica browserului interzice camera și microfonul folosite de produs',
'Răspunsul live are Permissions-Policy microphone=(), camera=(). WhatsAppPage utilizează getUserMedia pentru audio/video; allowlist-ul Electron nu include media.',
'Funcțiile de înregistrare au o incompatibilitate de configurație. Simptomul exact pe fiecare platformă urmează să fie verificat în sesiunea UI după ora 20.',
'Permiteți doar funcțiile necesare pe originea de încredere și implementați cerere de permisiune contextuală, cu erori clare/refuz/retry.',
'Audio/video funcționează cu acord, refuzul nu blochează pagina, iar origini externe/iframe-uri neautorizate rămân refuzate.',
['http-probes.json','main.js:215','source/frontend/src/pages/WhatsAppPage.tsx:121'])
add('A19','P2','Totalurile facturilor amestecă monedele',
'Endpointul /totals calculează SUM(amount) fără filtrare/grupare pe currency. Alte endpointuri au deja unpaid_sum_by_currency, deci comportamentul nu este uniform.',
'100 RON + 100 EUR ar produce numeric 200 fără o monedă comună justificată. Analiză a SQL, nu verificare a facturilor reale și nici confirmare că toate ecranele folosesc acest endpoint.',
'Totaluri separate pe monedă; dacă se cere total convertit, curs, sursă și dată explicite; Decimal pentru operații financiare.',
'Set sintetic RON/EUR/USD returnează totaluri separate corecte; frontendul nu afișează o sumă mixtă ca RON.',
['source/backend/app/api/v1/endpoints/invoices.py:933'])
add('A20','P2','Migrație distructivă în startup',
'main.py execută DROP TABLE IF EXISTS public.project_chat_imports la pornire, într-un bloc de migrare. Nu s-a repornit aplicația în audit.',
'Poate distruge date reintroduse prin restore/rollback în acea tabelă; nu afirm că tabela conține date în prezent sau că s-au pierdut date.',
'Migrații versionate, executate o singură dată, cu precondiții și strategie de rollback; scoaterea DDL distructiv din startup normal.',
'Restart repetat nu schimbă schema; restaurarea unei versiuni suportate trece prin migrare controlată și verificată.',
['source/backend/app/main.py:1169'])
add('A21','P2','Distribuția Windows nu oferă încă încredere de publisher verificată',
'Executabilul instalat 1.5.6 a fost identificat NotSigned. Updaterul verifică hash din metadatele de distribuție; confirmarea utilizatorului există. Nu s-a instalat sau executat un update în audit.',
'Hash-ul din același canal nu înlocuiește o semnătură independentă a publisherului. Compatibilitatea SmartScreen, upgrade/downgrade și recuperarea după update rămân de testat.',
'Semnare Authenticode a binarului/installerului, metadate de update semnate, HTTPS strict și verificare publisher înainte de execuție; protecție downgrade.',
'Binarele release au semnătură validă; artefact alterat sau publisher diferit este respins; upgrade păstrează conturile și permite recuperare.',
['main.js','package.json'])
add('A22','P2','Testele care trec nu demonstrează încă securitatea produsului',
'139 teste colectate. Subsetul unit: 58 passed, 1 skipped, 130 warnings. Unele teste security verifică implementări locale de SHA/base64/XOR/limiter în locul funcțiilor produsului; unele teste AI verifică răspunsul propriului mock. 127 fișiere Python din app se parsează fără SyntaxError.',
'Rezultatul verde trebuie interpretat strict pentru subsetul rulat. Nu am rulat suita completă/integrările pe DB de producție; acestea nu sunt validate.',
'Teste de contract pe funcțiile reale, integrare pe DB/Redis efemere, teste negative multi-tenant și fault injection; eliminarea testelor tautologice; raportarea explicită a skip-urilor.',
'Regresiile A01–A06 fac testele să eșueze înainte de remediere și să treacă după, fără date reale și fără mocks care înlocuiesc controlul testat.',
['unit-tests.json','pytest-collection.json','source/backend/tests/unit/test_security.py','extended-checks.json'])

e=html.escape
head='''<!doctype html><html lang="ro"><meta charset="utf-8"><title>Audit EVA — 30 octombrie 2026</title><style>body{font:16px/1.6 system-ui;max-width:1120px;margin:40px auto;padding:0 24px;color:#182638;background:#f8fafc}h1,h2,h3{line-height:1.2}h1{font-size:38px}h2{margin-top:48px}article{background:white;border:1px solid #d6dfe8;border-radius:10px;padding:24px;margin:20px 0}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd6df;padding:10px;text-align:left;vertical-align:top}a{color:#075d99}.badge{background:#8b1c28;color:white;padding:4px 10px;border-radius:5px}.muted{color:#526475}code{overflow-wrap:anywhere}li{margin:8px 0}@media print{body{font-size:11px;background:white;margin:0}article{break-inside:avoid}h2{break-before:auto}a{color:inherit}}</style>'''
body='''<h1>EVA-Mail: audit înainte de lansare</h1><p class="badge">Verdict pentru etapa server/cod: NU recomand lansarea comercială</p>
<p>30 octombrie 2026 · Raport tehnic de etapă · 22 constatări prioritizate · Interfețele complete rămân de verificat după ora 20:00.</p>
<p>Problemele decisive sunt izolarea utilizatorilor, executorul SQL al AI și suprafața de privilegii a backendului. Acestea pot afecta confidențialitatea datelor clienților. Verdictul nu depinde de un scor estetic sau de numărul de butoane funcționale.</p>
<h2>Ce a fost verificat și cu ce limite</h2>
<p>Sursa a fost preluată prin SSH din /home/cesirothor/openfyxer: 592 fișiere urmărite de Git, cu excluderea fișierelor de mediu și a unor binare/fișiere mari. HEAD d7040dc21a64dfcfda660b7c8eda4a7ca9812e45. Un fișier urmărit, alibaba_chat_service.py, avea modificări locale; au existat și fișiere neurmărite. Analiza se referă la snapshotul de pe server, nu la o reproducere garantată a întregului repository GitHub. Accesul GitHub a returnat 404.</p>
<p>Au fost folosite comenzi de inventariere, probe HTTP fără autentificare și fără mutații, testele unitare izolate de DB/Redis reale și reproduceri pe funcții extrase din cod. Nu s-au creat conturi de atac, citit date ale altor utilizatori, trimis emailuri/mesaje, executat SQL de exfiltrare, rulat load test, șters backupuri sau schimbat configurația live. Copia locală a primit fișiere de audit și încercarea de instalare frontend; serverul nu a primit remedieri.</p>
<p>P0 = blocaj de lansare cu impact critic potențial; P1 = prioritate mare, de închis înaintea lansării; P2 = risc/defect care cere remediere sau decizie explicită. Prioritățile sunt evaluări inginerești, nu scoruri CVSS. „Confirmat în cod” nu înseamnă exploatare completă demonstrată.</p>
<table><tr><th>Suprafață</th><th>Acoperire reală</th><th>Ce lipsește</th></tr><tr><td>Server/backend</td><td>SSH, containere, DB rol/config, Redis, resurse, backup, cod și teste izolate</td><td>Restore real, sarcină, failover, pentest complet, scan complet imagini/Python</td></tr><tr><td>Web</td><td>13 probe HTTP; cod frontend și configurație</td><td>Parcurgerea tuturor ecranelor și butoanelor după ora 20</td></tr><tr><td>Windows 1.5.6</td><td>Inspecție preliminară și cod main/preload; semnătură executabil</td><td>Fluxuri complete, update, offline, crash/recovery, permisiuni</td></tr><tr><td>Android</td><td>Cod TWA și metadate APK 1.0.0; assetlinks răspunde 200</td><td>Instalare/rulare pe dispozitiv, semnătura APK distribuit, domain verification reală</td></tr><tr><td>iPhone/iOS</td><td>Indicii PWA; nu am identificat proiect nativ iOS în snapshot</td><td>Dispozitiv/Safari/PWA, instalare, fundal, notificări, upload/download. Nu afirm că o aplicație nativă externă snapshotului nu există.</td></tr></table>
<h2>Rezultate de verificare</h2><ul><li>58 teste unitare trecute, 1 omis; 139 colectate; 127 fișiere Python parsează fără erori de sintaxă.</li><li>Coliziuni tenant, refresh folosit ca access, fail-open Redis și IP falsificabil: reproduse în harness cu funcțiile reale, fără conturi reale.</li><li>Validator SQL: acceptă citiri neautorizate ca structură; interogările nu au fost executate.</li><li>npm ci eșuează; npm audit raportează 32 noduri de pachete afectate, cu distincția runtime/dev încă necesară.</li><li>Auth/me, contacts și status AI refuză anonimul cu 401; tts-lab și OpenAPI-ul său au 401, iar OpenAPI backend are 404. Aceste protecții au fost observate și nu sunt raportate ca defecte.</li></ul>
<h2>Constatări și criterii de închidere</h2>'''
for f in findings:
 body+=f'<article id="{f["id"]}"><h3>{f["id"]} · {f["severity"]} · {e(f["title"])}</h3>'
 for key,label in [('evidence','Dovadă și reproducere'),('impact','Impact și limite'),('remediation','Remediere propusă'),('acceptance','Criteriu de acceptare')]: body+=f'<p><b>{label}.</b> {e(f[key])}</p>'
 body+='<p class="muted"><b>Referințe locale:</b> '+', '.join(e(x) for x in f['references'])+'</p></article>'
body+='''<h2>Operațiuni și recuperare</h2><p>Ubuntu 24.04.4 LTS aarch64, kernel tegra, aproximativ 18 zile uptime. Discul principal avea aproximativ 69% utilizare și 278 GB disponibili; baza de date aproximativ 69 GB. Backupul full din 30 octombrie are 53.210.619.056 bytes și log de finalizare. Acestea demonstrează existența unui fișier, nu restaurabilitatea sa. Copia și cheia sunt pe aceeași gazdă; nu s-a găsit dovadă suficientă de offsite sau exercițiu de restore în materialul inspectat.</p>
<p>Bannerul sistemului indică 542 actualizări, dintre care 416 de securitate; este un contor local posibil neactualizat, nu un inventar CVE validat. Planificați patching cu suportul NVIDIA/Jetson și rollback verificat. Serviciile dnsmasq, isc-dhcp și nvidia-cdi-refresh apăreau failed; relevanța lor pentru fluxul productiv trebuie stabilită înainte de a le considera incidente EVA.</p>
<p>Fișierele .env și copii .env.bak au mod 664, într-un home cu mod 750. Riscul este accesul grupului și multiplicarea secretelor, nu acces universal garantat. Restrângeți permisiunile, eliminați copiile inutile printr-o procedură controlată și gestionați rotația secretelor fără a le include în loguri/raport.</p>
<p>Backendul, workerul și frontendul nu au healthcheck Docker în inventarul inspectat. Conexiunile DB aveau 51 idle, una idle in transaction și trei active în instantaneu; nu demonstrează un leak. Poolurile și numărul de procese trebuie bugetate împreună cu limita PostgreSQL de 500. Observabilitatea ar trebui să urmărească vârsta ultimei sincronizări per cont, taskuri blocate, latențe, erori pe furnizor și backlog pe fiecare coadă, nu doar procesul pornit.</p>
<h2>Plan propus înainte de comercializare</h2><table><tr><th>Ordine</th><th>Livrabil</th><th>Dovadă necesară</th></tr><tr><td>1. Contenție și confidențialitate</td><td>A01/A02; roluri DB minime; reducerea Docker socket; autentificare/IMAP/IPC</td><td>Teste negative cu doi tenants și executor AI restrâns; validare independentă</td></tr><tr><td>2. Recuperare</td><td>Retenție backup sigură, copie offsite, cheie separată, restaurare pe gazdă izolată</td><td>Restore integral măsurat, verificarea numărului de obiecte și a fluxurilor aplicației; RPO/RTO aprobate</td></tr><tr><td>3. Release reproductibil</td><td>Lockfile reparat, coverage real, teste de produs, scanuri, artefacte semnate</td><td>Build curat de la commit până la digest; release blocat de teste eșuate</td></tr><tr><td>4. Capacitate și UX</td><td>Resurse/cote/cozi, fluxurile fiecărei platforme, permisiuni și totaluri financiare</td><td>Scenarii de sarcină și regresie; matrice UI cu pass/fail și capturi</td></tr><tr><td>5. Lansare controlată</td><td>Pilot cu clienți de test, suport, procedură de incident și rollback</td><td>Fără P0/P1 deschise; riscuri P2 acceptate explicit, owner și termen</td></tr></table>
<p>Nu estimez o dată responsabilă de lansare înaintea evaluării migrării tenant și a restaurării. Migrarea datelor este partea cu cel mai mare risc de implementare; necesită backup verificat și repetiție pe copie izolată.</p>
<h2>Matrice pentru sesiunea de interfață de după ora 20</h2><p>Reluarea a fost programată pentru 20:05. Este o continuare a auditului, nu o confirmare că toate dispozitivele sunt disponibile. Testele cu efect extern necesită destinatari de test aprobați; nu vor fi trimise mesaje către clienți reali.</p>
<table><tr><th>Modul</th><th>Scenarii obligatorii</th></tr><tr><td>Autentificare și conturi</td><td>Login corect/greșit, 2FA, expirare, refresh, logout/revocare, schimbare cont, sesiuni concurente, parolă uitată, acces după restart</td></tr><tr><td>Email</td><td>Sincronizare IMAP/OAuth, foldere, paginare, căutare, citit/necitit, atașamente, HTML adversarial, draft/reply/forward, trimitere doar către conturi de test, erori SMTP și retry fără dubluri</td></tr><tr><td>AI</td><td>Răspuns ancorat în date autorizate, citări, oprire, timeout, context multi-cont, prompt injection din email, lipsă date, model indisponibil, conversații simultane</td></tr><tr><td>Contacte/calendar/proiecte</td><td>CRUD pe date sintetice, validare, timezone/DST, invitații controlate, import/export, drepturi și schimbarea tenantului</td></tr><tr><td>Facturi</td><td>OCR document test, deduplicare, totaluri pe monedă, scadență, plată/undo, filtru/export, erori și document corupt</td></tr><tr><td>WhatsApp/Alibaba și integrări</td><td>Conectare/deconectare, reconectare, permisiuni audio/video, atașamente, notificări, identitate destinatar, stări eroare; fără mesaje reale</td></tr><tr><td>Windows</td><td>Instalare/upgrade, taburi, tray, notificări, linkuri externe, download, parole pe origine, offline, restart/crash și DPI</td></tr><tr><td>Android/iPhone</td><td>Dispozitiv real, viewport/tastatură, orientare, safe areas, instalare TWA/PWA, linkuri, fișiere/cameră, rețea slabă, fundal/revenire, notificări conform capabilităților livrate</td></tr><tr><td>Accesibilitate</td><td>Tastatură, focus vizibil, etichete screen reader, contrast, zoom, confirmări pentru acțiuni distructive și mesaje de eroare utile</td></tr></table>
<p>Pe Android proiectul inspectat este TWA și conține domeniul eva.alba-vision.ro, în timp ce desktop folosește mail.eva-org.com. Trebuie verificată asocierea exactă a APK-ului distribuit, redirecturile și Digital Asset Links pe dispozitiv. Pentru iOS nu se poate echivala un test în browser desktop cu un test Safari/PWA pe iPhone. Service worker-ul inspectat nu are listener push; notificările cu aplicația închisă nu trebuie promise fără implementare și validare separată.</p>
<h2>Îmbunătățiri de produs și arhitectură</h2><ul><li>Registru unic de tenant și cont, folosit de toate modulele; eliminarea copiilor de funcții de schemă.</li><li>Stare de sincronizare vizibilă: ultima sincronizare, progres, eroare remediabilă și retry. Operațiile lungi au anulare și rezultat persistent.</li><li>Acțiuni AI cu preview al țintei, autorizare pe server și confirmare pentru efecte externe; citări și delimitarea faptelor de inferențe.</li><li>Idempotency pentru trimitere/import/plată și retry; evitarea dublurilor după refresh sau reconectare.</li><li>Feature flags pentru funcții neterminate; inventar de capabilități separat pentru web, Windows, TWA și iOS PWA.</li><li>Politică de retenție și ștergere/export a datelor, audit trail fără conținut sensibil inutil, separarea logurilor de diagnostic de mesajele utilizatorilor. Acest raport nu certifică conformitatea juridică/GDPR.</li><li>Runbookuri pentru furnizor email indisponibil, model AI blocat, spațiu insuficient, Redis căzut, restaurare și rollback; alerte testate și responsabil de incident.</li></ul>
<h2>Dovezi și reproducibilitate</h2><p>Fișierele JSON păstrează rezultatele tehnice; scripturile reproduce_security.py și extended_checks.py reproduc verificările offline. npm-ci.log păstrează eroarea instalării. Sursa din source/ este snapshotul analizat. Dovezile pot conține nume interne de servicii și căi; păstrați pachetul intern. Nu conține intenționat parola SSH sau fișierele .env.</p>
<p>Raportul se bazează pe starea observată în această sesiune. Nu este o certificare de securitate și nu justifică formularea „toate funcțiile testate”. Pentru fiecare defect reparat sunt necesare retestarea criteriului de acceptare și regresia modulelor afectate.</p>'''
(r/'findings.json').write_text(json.dumps(findings,ensure_ascii=False,indent=2),encoding='utf-8')
(r/'Raport-audit-EVA-2026-10-30.html').write_text(head+body+'</html>',encoding='utf-8')
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in r.glob('*') if p.is_file() and p.name!='evidence-sha256.json'}
(r/'evidence-sha256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'findings':len(findings),'report_bytes':(r/'Raport-audit-EVA-2026-10-30.html').stat().st_size,'priorities':{s:sum(f['severity']==s for f in findings) for s in ['P0','P1','P2']}},indent=2))
