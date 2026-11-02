# Plan de re-audit EVA-Mail — Agentul 1

Versiune: 1.2, 1 noiembrie 2026 (UTC+02). Statut: PROPUS, audit live neînceput de Agentul 1. Autor: Agentul 1. Reviewer independent: Agentul 2. Coordonatorul gestionează accesul la UI și aprobarea gate-urilor.

## 1. Obiectiv, limite și baza de lucru

Solicitarea este re-auditarea întregului proiect și verificarea funcțională a tuturor controalelor din Chrome și aplicația Windows, fără trasee fără ieșire, cu verificare independentă a planului și a auditului. Android și iOS rămân în scopul original. Un plan 10/10 dovedește că procedura satisface criteriile convenite, NU că produsul are calitatea 10/10 sau că nu există defecte. Nicio promisiune de absență absolută a erorilor: concluzia finală va avea numitor de acoperire, versiuni, medii, limitări și dovezi.

Bază istorică: audit-2026-10-30/findings.json (A01–A22), Raport-audit-EVA-2026-10-30.html, UI-20h-addendum.html (U01–U04), source/frontend/src/App.tsx și inventarul directoarelor sursei. Snapshotul istoric HEAD d7040dc21a64dfcfda660b7c8eda4a7ca9812e45 nu este presupus actual. Toate constatările vechi sunt ipoteze de retestat. Nu au fost găsite AGENTS.md în ascendenții partajării și snapshotului inspectat; se verifică iar pe sursa actuală înainte de execuție.

Inventar de planificare: frontend; backend/API/workers/MCP; database; Docker Compose/rețea/proxy; Redis/Celery; Ollama/ollama-qwen; meeting-bot; OCR/unlimited_ocr; eva-desktop; eva-android; chrome-extension; alibaba-desktop; wechat-desktop; novnc-sidecar; telegram-poc; rca-solver/yolo-solver; op-overlays/OpenProject; scripts; .github CI/release; docs/documentatie/skills. Componente noi descoperite intră în scope prin revizie. POC, utilitar și componentă abandonată nu sunt excluse tacit: se documentează dacă sunt livrate, pornite, accesibile sau excluse, cu justificare verificată de reviewer.

## 2. Responsabilități și gate-uri

Agentul 1 produce planul, inventarele, cazurile, execuția, registrul defectelor și raportul. Agentul 2 verifică independent acoperirea, corectitudinea dovezilor și concluziilor și reproduce cazurile cerute. Nu își autoaprobă Agentul 1 rezultatele. Control UI exclusiv: un singur agent la un moment dat; handoff prin coordonator și recitirea stării curente, fără identificatori UI vechi. Nu se creează agenți suplimentari. Toate interacțiunile UI folosesc cua_repl și API-urile documentate; fără Playwright extern, PowerShell UIA sau automatizare alternativă. Agentul 2 primește explicit controlul după eliberarea ferestrei de Agentul 1.

G0: plan 10/10 aprobat în scris de Agentul 2 și gate transmis de coordonator. Până atunci doar citire artefacte și planificare.
G1: inventar actual și baseline de versiuni; fiecare suprafață are acces confirmat sau BLOCKED. Agentul 2 semnează numitorul de inventar înainte de a raporta procente; auditul poate avansa pe suprafețele accesibile, dar nu poate declara scope complet.
G2: date sintetice, roluri și limite de efecte validate; testele care necesită mediu izolat nu se mută pe producție.
G3: execuție și dovezi pe toate cazurile aplicabile; orice componentă nouă redeschide inventarul și cazurile dependente.
G4: auditul auditului de Agentul 2; buclă de corecții până la 10/10 pentru fidelitatea/metodologia auditului. Produsul poate rămâne NO-GO cu audit metodologic 10/10.
G5: după remedieri autorizate separat, retest pe build nou, regresie și re-review. Această cerere autorizează auditul, nu modificarea/deploy-ul produsului.

Fiecare revizie păstrează versiunea precedentă și review-ul: finding reviewer, criteriu, dovadă lipsă, corecție, verificare. Nu se schimbă criteriile pentru a obține artificial 10/10. Dacă accesul lipsește, se raportează incomplet/BLOCKED; nu se umple cu PASS și nu se așteaptă inutil în buclă.

## 3. Precondiții și medii

La pornire se înregistrează timestamp, git HEAD/dirty state, hash bundle servit, versiuni API/container image digest, config relevantă redactată, DB schema/migration head, OS/Chrome/Electron, exe/APK hash și semnătură, domenii/tunnel/proxy, service worker/cache, matrice feature flags. Nu se presupune că aplicația instalată coincide cu sursa sau cu release-ul public. Diferențele produc rânduri separate de baseline și limite de concluzie.

Confirmare de la coordonator în sesiunea curentă: există fereastră Chrome Eva-Mail și fereastră EVA Windows. Accesul UI nativ este disponibil acum; Chrome autentificat este acum confirmat prin AX în Inbox /inbox?account_id=all, conform preflight-coordonator.json; drepturile și conturile disponibile se inventariază fără a salva conținut personal în dovezile generale. Autentificarea Windows se confirmă separat. Chrome nu se înlocuiește cu browserul integrat. Un cont real deja autentificat permite navigare/citire în scop, dar nu autorizează mesaje externe sau schimbări pe date reale.

Platforme obligatorii: Chrome Windows instalat (versiune exactă); EVA Windows instalat (versiune exactă); Android APK instalat pe dispozitiv/emulator identificat + versiune Android/Chrome; iPhone Safari/PWA sau aplicație nativă dacă există, cu model și versiune iOS. Device viewport în Chrome nu este test Android/iOS. Pentru desktop se testează fereastră normală/maximizată, zoom 100/200%, DPI disponibile; pentru mobil portrait/landscape, tastatură, safe areas și touch. Mobile momentan NEIDENTIFICAT, nu N/A. Ordinea actualizată prin instrucțiunea utilizatorului: întâi Chrome și EVA Windows, apoi telefoanele în faza finală. DEFERRED este etichetă de programare pentru mobile (cazurile rămân NOT_RUN până la faza finală), nu verdict de test și nu excludere de scope.

Date necesare: două tenants sintetice A/B și utilizator cu rol redus, un admin de test dacă există, două mailbox-uri controlate cu destinatari expliciți, conturi provider sandbox pentru OAuth/calendar/messaging, fixtures sintetice de email/atașamente/contacte/evenimente/facturi/proiecte, perechi de adrese pentru coliziuni și text prompt injection fără secrete. Coordonatorul a cerut utilizatorului conturi/destinatari și dispozitive; parolele nu se solicită în chat și nu se reutilizează parola SSH ca parolă EVA.

Mediu izolat pentru fault injection, MITM TLS de test, load, token/cross-tenant, update/install, backup restore, migrare și controale destructive. Disponibilitatea lui este un prerechizit verificat, nu o presupunere. Dacă nu există, cazurile dependente devin BLOCKED cu owner și cerință de deblocare, iar restul continuă.

## 4. Siguranță, efecte și fixture-uri

Clasa R: citire/inventar/navigare; permisă în scop. Clasa T: creare/editare de date sintetice într-un mediu de test identificat; permisă numai după stabilirea contului/fixture-ului și efectului. Clasa X: trimitere email/mesaj/invitație, apel, meeting bot, upload către terț, import/sync care poate publica, unsubscribe, plată, ștergere, modificări securitate și instalare; necesită autorizarea specifică aplicabilă și destinația de test. Nu se execută mesaj real către terți, nu se șterge producție, nu se acceptă termeni și nu se schimbă parole fără pașii de handoff/confirmare ceruți de instrumente. Testarea tuturor butoanelor NU este permisiune de a activa orbește efecte distructive.

Prefix fixture: EVA-AUDIT-20261101-<caseid>. Înainte/după se notează obiectele de test și proprietarul, fără conținut real. SMTP sink și API sandbox/conturi controlate pentru efecte. Cleanup numai pentru fixture-uri autorizate recuperabile, sau restore snapshot în sandbox; niciodată search-and-delete global. Duplicatul după retry și orice efect neașteptat se investighează înainte de continuare. Oprire imediată la amestec de tenants, exfiltrare, mesaje reale, degradare producție sau cererea utilizatorului; păstrare dovezi redactate și notificare coordonator.

## 5. Inventar exhaustiv UI și trasabilitate

Se construiesc inventory-routes.csv, inventory-controls.csv, inventory-states.csv, dependency-map.csv și cases.csv. Sursa/routerul oferă candidați, DOM/AX/UI runtime confirmă ce este livrat. Se includ taburi, meniuri, submeniuri, icon-only, context menus, popover/modal, shortcut, drag/drop, link extern, download, setări, pagination, empty/loading/error, disabled/hidden pentru rol, toolbar native/tray/updater. Componente partajate sunt inventariate și pe fiecare context unde acțiunea/permisiunea diferă.

ID control: platform/screen/container/semantic-action; nu index AX volatil. Se notează text, rol accesibil, selector/poziție semantică, precondiții, rol, stare, side-effect class, API/worker dependență, destinație așteptată și modalitate de ieșire. Funcțiile descoperite după freeze adaugă control și caz, versiunea numitorului crește și reviewer revalidează.

Pentru FIECARE control aplicabil × platformă obligatorie × rol care schimbă comportamentul × stare relevantă: caz normal, validare/refuz, cancel/back/close, eroare/retry și verificare persistență când controlul scrie. Liste dinamice au exemplare empty/1/many și pagina următoare/ultima, nu un click pe fiecare mesaj real. Se pot grupa exemplare echivalente numai dacă reviewer justifică aceeași implementare, aceleași permisiuni și aceeași tranziție; niciodată nu se extrapolează Chrome la Windows.

Rând cases.csv obligatoriu: case_id, requirement_id, risk_id, platform_build, screen, control_id, role, data_fixture, preconditions, steps, expected_ui, expected_server_effect, recovery_path, dependencies, side_effect_class, status, actual, evidence_ids, issue_id, executed_at, executor, reviewer, retest_build. Rând cu status PASS fără pași/expected/actual/dovadă este invalid.

Numitori: controale aplicabile, perechi control-stare-rol planificate și cazuri obligatorii per platformă. Raportăm separat executate=(PASS+FAIL), reușite=PASS, BLOCKED, NOT_RUN, N/A. N/A necesită motiv și acord Agent 2, fără a ascunde lipsa de acces. Nicio rată generală nu ascunde platforme cu 0 teste. „Toate butoanele” este îndeplinit doar când 100% inventar livrat aplicabil are caz executat și dovadă; „funcționează tot” cere și toate cazurile obligatorii PASS, zero blocaje, zero defecte funcționale deschise.

Rutele seed din snapshot: /, /help, /presentation, /privacy, /terms, /login, /register, /reset-password, /oauth/authorize, /upload/:token, /dashboard, /inbox, /contacts, /drafts, /calendar, /knowledge-base, /knowledge-base/chat, /meetings, /messenger, /whatsapp, /telegram, /alibaba, /projects, /asana, /openproject, /invoices, /settings, /audit. Include ruta necunoscută, deep-link expirat/invalid, navigare autentificat/neautentificat și add_account. Lista se reconciliază cu versiunea actuală; nu este inventarul final de butoane.

## 6. Graful de navigare și definiția dead end

Fiecare nod = ecran/modal/stare/rol; fiecare muchie = acțiune/control + rezultat. Din orice nod accesibil nefinal trebuie să existe traseu utilizabil spre ecran sigur (home/listă/login după expirare) fără închiderea forțată a aplicației și fără pierdere de date neanunțată. Nodurile finale intenționate (download, logout) au confirmare și cale clară de continuare. Disabled este corect doar dacă motivul și deblocarea sunt explicate.

Pentru fiecare formular/modal/operare async: Back, Cancel, X, Escape, click outside dacă proiectat; refresh; deep link și browser history; token expirat; offline apoi online; 401/403/404/409/422/429/5xx și timeout în sandbox; dublu click/retry; pagină lipsă/lazy chunk vechi; sursă externă deconectată; operare anulată. Timeout-ul cazului se consemnează înainte (30s navigare/listare, 120s job interactiv default, prag separat documentat pentru import/AI); peste prag fără progres/ieșire este FAIL UX, nu așteptare nelimitată. Aceste praguri sunt criterii de test propuse, nu SLA contractual.

Se verifică starea după revenire, draft neexpediat păstrat/avertizat, focus restituit, indicator loading terminat, retry fără dubluri, erroare clară cu acțiune. Se calculează noduri fără muchie de ieșire și controale fără handler/rezultat; reviewer reproduce toate dead-end-urile raportate.

## 7. Familii funcționale obligatorii

| ID | Modul | Scenarii minime; toate controalele runtime vor extinde cazurile |
|---|---|---|
| F01 | Public/onboarding | landing links/help/download/privacy/terms, register validări/activation în sandbox, login/logout/forgot/reset, 2FA, expirare, account switch/add, login return-to |
| F02 | Dashboard/layout | sidebar/topbar/help/theme/language/account, toate cardurile/links, empty/loading/error, search și refresh |
| F03 | Inbox | Team Inbox/sharing/revocare și mailbox/folder/category/sender filters, search/pagination/sort, message/thread view, attachments, read/unread/star, compose/reply/reply-all/forward/draft, recipients/CC/BCC, signatures, upload, send sink, bulk/undo/trash numai sandbox, sync întrerupt/deduplicare |
| F04 | Drafts | generare/editare/save/reopen/discard autorizat/send sink, conflict, cancel AI, schimbare cont și retry fără dubluri |
| F05 | Contacts/calendar | create/read/update fixture, import/export, validation, duplicate, timezone/DST/all-day/recurență dacă există, invites sink, external sync ownership/conflict |
| F06 | Knowledge/AI | index/upload/link/source/download, semantic search, scoped citations, widget AI global și chat/history/new/delete sandbox, stop/retry, model indisponibil, prompt injection, tool calls și autorizare independentă, fișiere invalide/mari |
| F07 | Meetings | calendar/source preview/join link, bot numai meeting de test, admission/rejection/leave, record/transcribe/summary/audio, participanți/permisiuni, întrerupere/finalizare și acces ulterior |
| F08 | Messaging | Messenger/WhatsApp/Telegram/Alibaba: cont/select/conectare QR/reconnect, conversații/search/filter/archived, text/media/voice/emoji, delivery states, send numai peers controlați, permission denied, disconnect |
| F09 | Projects/integrări | CRUD fixture, membership/roles/sharing, feed/search/AI/docs/import, Asana/OpenProject SSO și drepturi, sync conflict/retry, links externe, embed logout/expirare |
| F10 | Invoices | scan/OCR fixture, list/search/filter/sort, detail/edit/paid/undo sandbox, multi-currency/totals/rounding, duplicate/corrupt PDF/export/pagination |
| F11 | Settings/audit | fiecare tab/control, profile/signature, providers, sync, notifications, security sessions/2FA preview fără schimbări live, permissions/RBAC, audit filters/export/redaction |
| F12 | Public upload/OAuth | token valid/expirat/folosit/alt tenant, limite/extensii/magic, scopes/client/redirect/state/PKCE, approve/deny numai client de test autorizat |
| F13 | Chrome extension | manifest permissions, popup/options/content/background, login/storage, import/export/ChatGPT bridge, disconnected tab/token, context/isolation/duplicate submission; fără transmitere către terți |
| F14 | Native auxiliari | Alibaba/WeChat/noVNC, session ownership/auth/reconnect/viewport/clipboard/file transfer; capcha handoff, nu bypass; identificați ce e livrat vs POC |

## 8. Platforme desktop/mobile și accesibilitate

Chrome: profil/versiune documentat, route-by-route, dev console/network unde instrumentele suportă, reload/back/forward/open new tab, download/open file autorizat, keyboard Tab/Enter/Escape și focus, contrast/zoom, language, permisiuni denied/granted doar cu autorizație, offline/online pe cont de test. Nu se închide browserul utilizatorului pentru test.

Windows: aceeași matrice funcțională se execută separat; meniuri/tab create/switch/rename/close/reload, tray/minimize/restore/quit, notificări/deep links, external protocols, settings URL, saved credentials origin, offline fallback, crash/restart într-o instanță de test, multiple windows, DPI, installer/update/cancel/corrupt package/downgrade și semnătură. Install/update pe VM sau instanță de test; nu se alterează sesiunea reală pentru repro de securitate.

Android: APK semnătură/versionCode, domeniu/TWA/DAL, install/update, back gesture, keyboard/orientation, file picker/camera/mic, notification permission, offline/background/resume, external intents/share, account isolation și fluxurile F01–F14 aplicabile. iOS: Safari și PWA instalată distincte, install/add-to-home, safe area, upload/download/share, keyboard, back, session persistence, background/relaunch și notificări conform capabilităților reale; aplicație nativă dacă livrată. Fără dispozitiv, BLOCKED; nici emularea viewportului, nici source review nu înlocuiesc testul device.

Accesibilitate: nume/rol/stare pentru toate controalele, label și error association, ordine/focus trap/restoration, tastatură, 200% zoom și contrast, mesaje loading/erroare anunțabile. Test real screen reader dacă disponibil; lipsa lui se notează distinct de inspecția AX.

## 9. Backend, securitate, date și AI

Inventar OpenAPI/rute din sursă+runtime, auth deps, roluri/tenants, background workers, webhooks, WS/SSE, fișiere/public shares, integrarea MCP/OAuth. Pentru fiecare endpoint/mutator: autentificare lipsă/expirată, rol greșit, alt tenant, input invalid/limite, idempotency, concurrent update, rate limits, timeout/error leak, DB efect versus UI. Nu se citesc rânduri reale ale altui client; dovezile cross-tenant folosesc fixtures.

Priorități A01–A22: tenant schema collisions și filtre; AI SQL table/function authorization cu least privilege; access vs refresh; revocare când Redis cade; certificat IMAP invalid; Electron sender/origin; Docker socket/root; backup full/schema rotation; clean install; coverage real; dependency reachability/release gating; HTML sanitization exception/XSS; public issue mutations; token storage; OOM/resource budgets; Ollama network exposure; trusted proxy/rate limit; camera/mic policies; currency totals; startup DDL; signatures/updater; teste reale vs mock tautologic. U01–U04: labels, promisiuni procesare locală/cloud, traduceri, criptare vs text public.

Suplimentar: SQLi/path traversal/SSRF/command injection/IDOR, upload/download ownership, secret storage/log redaction, OAuth scopes/redirect/PKCE/state, cookie/CSRF/CORS/CSP, webhook auth/replay, JWT exp/aud/iss/alg, password reset enumeration/rate limits, sharing/revocation și cache multi-cont, encrypted transport/at-rest claims, retention/export/delete workflow fără ștergere reală. AI: răspuns greșit/hallucination, citări verificabile, date lipsă, prompt injection din email/docs, memory scope, tool permission, anulare/cost/concurrency; un prompt nu este barieră de autorizare.

Contract DB: constrângeri/FK/uniqueness/tranzacții, concurență/idempotency, migrare forward/rollback pe copie, timezone și Decimal/currency, retention și audit. Pentru fiecare afirmație se diferențiază code review, test izolat, integrare și exploatare end-to-end; nu se deduce exploatare din simpla prezență a unei librării.

## 10. Dependențe, operare și continuitate

dependency-map.csv leagă UI→API→DB/Redis/worker→provider și image/package/version. Enumerare manifests+lock+runtime pentru Python/npm/Gradle/Electron/extensie/bots/OCR/imaginile OS; SBOM și licențe la nivel tehnic, advisories actuale din surse oficiale, runtime/dev și reachable/not demonstrated separate. Pin/digest, proveniență/semnături, build curat, checksum artefact, teste/coverage/CI gates și secrets în repo. Vulnerability count pe package/advisory nu este număr de exploatări.

Operații: porturi/firewall/proxy/TLS, secret permissions, user/capabilities/socket/mount/resource limits/health checks, updates suportate Jetson, storage și DB pool, idle transactions, queues/dead letters, retry/backoff, provider quotas și failure isolation. Backup: full/schema/key/offsite/retention plus restore pe gazdă izolată; verificare checksum, row/object counts și login/attachments după restore; RPO/RTO măsurate, nu presupuse din existența dumpului. Runbook incident/rollback/on-call și verificare alerte într-un sink.

Performanță pe staging: baseline + 1/5/10 utilizatori concurenți și 10k/100k mesaje sintetice dacă resursele permit, soak 60 minute, scenarii search/sync/OCR/AI mix și provider lent; p50/p95/p99, error rate, RAM/VRAM/disk/DB/queue backlog, idempotency. Volumele maxime reale și SLO business sunt prerechizite de confirmat; fără ele rezultatul e limitat la profilul măsurat. Gate obligatoriu înainte de load/fault: coordonatorul și ownerul mediului aprobă profilul, plafonul de concurență, durata, bugetul și pragurile de oprire în load-gate.json. Propuneri conservative pentru staging: oprire la available RAM <15%, disk free <20%, orice OOM, error rate >5% timp de 60s, p95 >2×baseline timp de 120s sau backlog crescând fără drenare 5min; praguri VRAM/GPU/DB se fixează după baseline. Orice semn de afectare producție oprește imediat testul. Fără acest gate cazurile sunt BLOCKED. Fără load/fault injection pe producție. Datele de business și costurile externe nu sunt generate automat.

## 11. Dovezi, rezultate și clasificare

Structură: baseline/, inventories/, cases/, evidence/<platform>/<case-id>/, issues/, reviews/, report/. Dovezi: screenshot înainte/după la UI relevant, AX/DOM snapshot pentru nume/stare, log/rețea/status/corelation ID când disponibil, efect server în sandbox, timestamp și build. Capturile/logurile redactează tokenuri/parole/mesaje reale, pot păstra fixture IDs. Dacă instrumentul nu poate captura/inspecta, notați limita; nu fabricați dovadă și nu promovați testul la PASS dacă oracle-ul necesar lipsește. Manifest SHA256 pentru fișiere, fără includerea secretelor.

PASS: pași executați pe build dat, rezultat UI și efect server cerut corespund, recovery verificat. FAIL: diferență observată/reproductibilă; păstrați condițiile și frecvența dacă intermitent. BLOCKED: precondiție externă/access/autorizare/mediu lipsește, cu owner și next action. NOT_RUN: planificat dar neexecutat. N/A: funcție demonstrat nelivrată/neaplicabilă, justificare + semnătură reviewer. Code-only și test-isolated sunt tipuri de dovezi, nu substitute PASS UI.

Defect: issue_id, cerință/caz/control, severity P0 critic date/host; P1 flux esențial/security indisponibil; P2 funcție secundară/UX/accesibilitate/material inconsistency; P3 cosmetic; confidence, prerequisites, steps, expected/actual, impact, scope platforms, evidence, owner, recommendation, fix commit și retest. Prioritățile pot fi corectate de reviewer cu motiv. Nu se declară GDPR/compliance certificat; procesele și afirmațiile produsului se verifică factual, evaluarea legală separată.

## 12. Auditarea auditului și criterii finale

Agentul 2 verifică 100% din inventar→cazuri→dovezi (integritate/traseu), reproduce independent toate P0/P1 și toate dead-end-uri, plus un eșantion stratificat de minimum 20% din celelalte cazuri executate pe fiecare platformă și modul (rotunjit în sus, minimum un caz pe modul/stare error/role critic). Dacă nu poate reproduce, statusul independent este BLOCKED/NOT_REPRODUCED, nu confirmat. Selecție deterministă: în fiecare strat platformă × modul × rol × tip stare (normal/error/recovery), sortați case_id lexical și selectați primele ceil(0.20*n) poziții distribuite uniform prin index floor(j*n/k), j=0..k-1, k=ceil(0.20*n), minimum 1. Se salvează lista înainte de reexecuție; include atât PASS cât și FAIL prin stratificare suplimentară pe status. Nu se alege după ușurința cazului. Eșantionul include PASS pentru a detecta false positives. Orice dovadă nevalidă extinde eșantionul la 100% din clasa afectată și returnează auditul la Agent 1.

Metodologia poate fi evaluată 10/10 numai cu matrice completă, fără afirmații fără dovezi și blocaje expuse. Audit funcțional COMPLET: zero NOT_RUN/BLOCKED în scope obligatoriu, toate controalele aplicabile executate și dovadă verificată, fiecare procedură cerută aplicată, review închis. Produs READY: toate cazurile obligatorii PASS, zero P0/P1 și zero dead-end deschis; defecte P2/P3 rămase enumerate cu decizie explicită, fără formula „totul funcționează” dacă există defecte funcționale. READY limitat sau NO-GO nu se ascunde sub nota auditului.

Retest: fiecare fix pe build nou reproduce cazul original, caz negativ vecin și recovery; regresie a dependenților din dependency-map, întregul modul și fiecare platformă afectată. Modificări auth/tenant/storage/shared renderer implică regresie pe toate modulele/conturile/platformele, nu doar ecranul inițial. Raportul vechi rămâne istoric, nu se rescrie pentru a părea că defectul n-a existat.

Livrare: plan+review versiuni, inventar și numitori, cazuri/status, dependency map, registru probleme cu dovezi și remediere, raport românesc cu verdict separat pe platformă/server, limite și prerechizite de deblocare. Verificarea finală confruntă fiecare solicitare a utilizatorului cu un ID de cerință și rezultat explicit.

## 13. Grilă binară 10/10 pentru plan și aplicarea ei la audit

| Punct | Criteriu verificabil | Dovadă pentru plan | Dovadă cerută la audit |
|---|---|---|---|
| 1 | Scope și proveniență complete, inclusiv auxiliari | §1/3, lista subsistemelor | baseline actual + reconciliere inventar |
| 2 | Trasabilitate solicitări/riscuri/istoric | §5/7/9, requirements.csv | fiecare cerință și A/U mapate la caz/dovadă |
| 3 | Control×stare×rol și numitor per platformă | §5/8 | inventar runtime semnat, acoperire calculată |
| 4 | Dead-end definit și verificabil | §6 | graf, recovery cases, zero nod ignorat |
| 5 | Acces și platforme reale, blocaje oneste | §3/8 | medii/device exact, BLOCKED unde lipsesc |
| 6 | Date/autorizații/izolare/cleanup | §4 | fixture manifest, efecte și cleanup trasabile |
| 7 | Backend/date/AI teste negative | §9 | rezultate integrate și limite de probă |
| 8 | Dependențe/build/operare/restore/perf | §10 | dependency map, scan/build/restore/load dovezi |
| 9 | Dovezi/reproducere independentă/status corect | §11/12 | review 100% trasabilitate + eșantion/repro |
| 10 | Gateuri/revizii/retest/acceptare distincte | §2/12 | jurnal gate, corecții închise, verdict distinct |

Fiecare punct este 0 sau 1; nu se acordă jumătăți pentru promisiuni vagi. Agentul 2 indică exact paragraful și lipsa dacă respinge. Nota 10/10 a planului autorizează trecerea metodologică la audit, nu ocolirea precondițiilor sau aprobarea lansării.