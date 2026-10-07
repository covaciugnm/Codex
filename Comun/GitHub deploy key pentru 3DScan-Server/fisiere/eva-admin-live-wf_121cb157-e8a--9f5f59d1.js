export const meta = {
  name: 'eva-admin-live',
  description: 'Zona /admin pe 3dscan.eva-org.com (live SSE, telemetrie iPhone, date, joburi, backup) cu verificare arhitectura si bucla audit-remediere pana la 10/10',
  phases: [
    { title: 'Arhitectura', detail: 'contract + 2 recenzenti independenti, revizie pana la aprobare' },
    { title: 'Implementare', detail: 'backend si frontend in paralel' },
    { title: 'Integrare', detail: 'E2E in stack izolat' },
    { title: 'Audit', detail: '3 auditori independenti (securitate, corectitudine, UX)' },
    { title: 'Remediere', detail: 'reluare pana la 10/10 la toti auditorii' },
  ],
}

const CTX = `
CONTEXT COMUN:
- Repo GitHub covaciugnm/3dscan.eva-org.com (privat), site public https://3dscan.eva-org.com, aplicatie iOS "EVA 3D Scan" (scris de un Claude pe Mac; clientul iOS NU se modifica de aici).
- Esti pe un laptop Windows; lucrezi pe server prin: ssh -o BatchMode=yes saga-server@192.168.100.151 '<comenzi>' (Docker fara sudo).
- Checkout LIVE: ~/site-uri/3dscan.eva-org.com (stack compose "eva-3d-scan-site": db postgres 17, app Node pe 127.0.0.1:4160, worker Python, tunnel). NU edita checkout-ul live, NU atinge containerele live, NU rula migrari pe DB-ul live. Pe server mai sunt ~120 containere ale altor proiecte — nu le atinge, fara prune global. In paralel ruleaza ALTE echipe pe branch-urile feat/b01-hardware, feat/model-export, feat/b05-sequencer, feat/b15-ops, feat/b09-worldmodel, feat/b12-leases (migrari rezervate 009/010/011) — nu le atinge branch-urile; tu folosesti migrarea Site/db/012-admin.sql (verifica conventia: migrarile sunt in Site/db/, aplicate de scripts/migrate.mjs / bootstrap.mjs; granturile runtime in scripts/provision-runtime.mjs).
- Clona ta: ~/work/3dscan-admin (git clone ~/site-uri/3dscan.eva-org.com, apoi git remote set-url origin git@github-3dscan-eva:covaciugnm/3dscan.eva-org.com.git, git fetch, branch feat/admin-live din origin/main). Agentii acestei echipe lucreaza in ACEEASI clona si acelasi branch pe fisiere diferite: inainte de commit fa git pull --rebase origin feat/admin-live, apoi push. Fara force, niciodata pe main. Commit-uri cu linia finala: Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- Teste in stack izolat: docker compose -p 3dscan-admin cu override care NU porneste tunnel si publica app pe 127.0.0.1:4190 (nu 4160), volume proprii; la final down -v doar pentru proiectul tau.
- Codul existent: Site/server/http.mjs (router manual node:http, SSE pe /api/events deja existent, CSP strict: script-src 'self', style-src 'self' — FARA scripturi/stiluri inline, fara CDN), auth.mjs (users, user_sessions, Bearer token, scrypt), library.mjs, inventory.mjs, projects.mjs, appI18n.mjs; paginile web existente public/cont/ si public/biblioteca/ (login cu token in browser) — refoloseste stilul si mecanismul lor de login. Rolul DB runtime eva_site_runtime e read-only implicit, scrierile cu BEGIN READ WRITE; workerul si migrate folosesc owner eva_site. Respecta stilul de cod existent.
- Fara secrete in commit. Onestitate: ce n-ai rulat = not_run; nu inventa rezultate.
- Text UI in romana (cu diacritice), si chei EN acolo unde mecanismul existent permite simplu.

CERINTA UTILIZATORULUI (proprietarul): "odata logat in zona de admin a aplicatiei sa intram in zona in care vedem paginile de administrare a aplicatiei 3dScan de pe iPhone - sa creezi pagini sa vedem in timp real ceea ce se intampla - sa apara detalii ale functiilor aplicate etc. sa fie un server cu toate functiile inclusiv salvare etc."

SPECIFICATIE TINTA:
1. Roluri: coloana role pe users (user|admin), admin initial = contul existent cesiro.horeca@gmail.com (prin env ADMIN_EMAILS la migrare/seed sau script scripts/grant-admin.mjs — nu hardcoda emailul in cod; documenteaza comanda). Toate /api/admin/* cer Bearer de admin (403 altfel, 401 fara token). Jurnal de audit al actiunilor admin.
2. Pagina /admin/ (login cu contul existent; non-admin vede "acces interzis"), cu sectiuni:
   a. Panou LIVE (SSE /api/admin/stream, autentificat — EventSource nu trimite header, deci foloseste un ticket scurt de stream obtinut cu Bearer, sau fetch streaming; NU pune tokenul de sesiune lung in URL): flux in timp real al tuturor cererilor API ale aplicatiei (metoda, ruta normalizata, status, durata ms, user, dispozitiv/user-agent, marime), evenimente de sync (proiect/biblioteca/inventar upsert/delete, asset upload, video upload), joburi worker (claimed/done/failed cu detectii), login/logout/inregistrari, erori. Contoare live (cereri/min, erori, utilizatori activi, dispozitive). Filtre pe user/tip/ruta.
   b. Telemetrie "functii aplicate" din iPhone: endpoint nou POST /api/telemetry/events (Bearer user, batch de evenimente: device_id, app_version, os, session_id, event (ex. scan_started, scan_finished, measure, object_detected, detector_engine_selected, export, sync, error), properties JSON marginit, ts client + received_at server), cu cote/rate limit si validare; afisate live si istoric in admin cu detalii per functie (parametri, durata, rezultat). Scrie Site/docs/ADMIN_TELEMETRIE.md = contractul exact pentru clientul iOS (Claude-ul de pe Mac va implementa trimiterea). Pana atunci panoul trebuie sa arate activitatea reala dedusa din cererile API existente.
   c. Utilizatori si dispozitive: lista, sesiuni active (revocare), ultima activitate, cote folosite (biblioteca/inventar/video), detalii per user.
   d. Date: proiecte, biblioteca, inventar (camere/obiecte/assets), videoclipuri si rezultatul reprocesarii (detectii cu clase/scor), cu vizualizare detalii JSON si preview imagini/asset-uri (servite prin admin API, autentificat).
   e. Server: health/readiness (app, db, worker heartbeat — workerul poate scrie un heartbeat in DB sau starea se deduce din joburi), versiune/commit, migrari aplicate, dimensiune DB si volume, starea modelului detectorului, statistici joburi.
   f. Salvare/backup: buton "Salvare acum" care pune o cerere in tabel admin_backup_jobs; executia o face un serviciu cu drepturi owner (extinde workerul existent sau un serviciu nou "backup" in compose, fara porturi publicate) cu pg_dump + arhiva volume (videos) + manifest sha256 intr-un volum backups; lista backup-urilor cu dimensiune/hash/stare, descarcare autentificata, retentie configurabila; restaurarea doar documentata (nu buton de restore pe productie). Coordonare: echipa feat/b15-ops face scripturi de backup in paralel — fa-l pe al tau autonom si mentioneaza in doc ca se pot unifica.
   g. Jurnal: cautare in evenimentele stocate (retentie limitata, ex. 30 zile, cu curatare).
3. Captura evenimentelor: middleware in http.mjs care inregistreaza fiecare cerere /api/* (fara body, fara tokenuri, fara parole; emailul doar ca user_id + email afisat doar adminului) intr-un bus in memorie (pentru SSE) + persistare asincrona batch in tabel admin_events (nu blocheaza cererea; esec de persistare nu strica API-ul). Hook-uri in library/inventory/projects/auth pentru evenimente semantice. Worker: evenimente prin tabel sau LISTEN/NOTIFY.
4. Performanta/securitate: fara impact vizibil pe API-urile existente; endpoint-urile vechi neschimbate ca semnatura; CSP pastrat; fara porturi noi pe host; grant-uri minime.
`

const SPEC = {
  type: 'object',
  properties: {
    contract_path: { type: 'string' },
    summary: { type: 'string' },
    backend_tasks: { type: 'array', items: { type: 'string' } },
    frontend_tasks: { type: 'array', items: { type: 'string' } },
  },
  required: ['contract_path', 'summary', 'backend_tasks', 'frontend_tasks'],
}
const RESULT = {
  type: 'object',
  properties: {
    commit: { type: 'string' },
    status: { type: 'string', enum: ['done', 'partial', 'blocked'] },
    delivered: { type: 'array', items: { type: 'string' } },
    tests: { type: 'array', items: { type: 'object', properties: { name: { type: 'string' }, result: { type: 'string', enum: ['pass', 'fail', 'not_run'] }, evidence: { type: 'string' } }, required: ['name', 'result', 'evidence'] } },
    open_issues: { type: 'array', items: { type: 'string' } },
    deploy_steps: { type: 'array', items: { type: 'string' } },
  },
  required: ['commit', 'status', 'delivered', 'tests', 'open_issues', 'deploy_steps'],
}
const AUDIT = {
  type: 'object',
  properties: {
    score: { type: 'number' },
    tests_rerun: { type: 'array', items: { type: 'string' } },
    findings: { type: 'array', items: { type: 'object', properties: { severity: { type: 'string', enum: ['blocant', 'major', 'minor'] }, description: { type: 'string' }, location: { type: 'string' } }, required: ['severity', 'description', 'location'] } },
    merge_ready: { type: 'boolean' },
    verdict: { type: 'string' },
  },
  required: ['score', 'tests_rerun', 'findings', 'merge_ready', 'verdict'],
}

phase('Arhitectura')
const spec = await agent(`${CTX}
ROL: ARHITECT. Citeste codul existent (Site/server/*.mjs, Site/db/*.sql, scripts/migrate.mjs, bootstrap.mjs, provision-runtime.mjs, compose.yaml, worker/process_videos.py, public/cont, public/biblioteca). Creeaza clona si branch-ul feat/admin-live (din origin/main) si comite Site/docs/ADMIN_ARHITECTURA.md: schema exacta 012-admin.sql (tabele users.role, admin_events, admin_audit, app_telemetry_events, admin_backup_jobs, worker heartbeat, indexuri, retentie, grant-uri pe rol), lista exacta a endpoint-urilor /api/admin/* si /api/telemetry/events (request/response JSON, coduri de eroare), formatul evenimentelor SSE, mecanismul de ticket pentru stream, structura fisierelor (server/admin.mjs, server/events.mjs, public/admin/*, worker/serviciu backup), si impartirea pe doua echipe care NU editeaza aceleasi fisiere: backend (server/, db/, scripts/, worker/, compose.yaml, docs/ADMIN_TELEMETRIE.md) si frontend (public/admin/* doar). Push. Intoarce caile si listele de sarcini.`, { label: 'Arhitect admin', phase: 'Arhitectura', schema: SPEC })

// Verificare arhitectura: 2 recenzenti independenti (securitate/date, functional/UX), revizie pana la aprobare
const REVIEW = { type: 'object', properties: { approved: { type: 'boolean' }, score: { type: 'number' }, issues: { type: 'array', items: { type: 'string' } } }, required: ['approved', 'score', 'issues'] }
let specCur = spec
for (let r = 1; r <= 4; r++) {
  const reviews = (await parallel(['securitate, autorizare, scurgeri de date, grant-uri DB, retentie, performanta middleware', 'acoperirea completa a cerintei utilizatorului (live, functii aplicate, utilizatori, date, server, salvare, jurnal), contract iOS telemetrie clar si implementabil, UX admin'].map((lens, i) => () =>
    agent(`${CTX}\nROL: RECENZENT INDEPENDENT DE ARHITECTURA (runda ${r}, lentila: ${lens}). Citeste ${specCur.contract_path} pe origin/feat/admin-live (clona proprie ~/work/3dscan-arhrev${i}, stearsa la final) si codul existent relevant. Nu scrii nimic in repo. approved=true doar daca arhitectura e completa si corecta pe lentila ta, fara lipsuri; score 0-10; issues = lista concreta a ce trebuie schimbat.`, { label: `Recenzie arh r${r}.${i + 1}`, phase: 'Arhitectura', schema: REVIEW })))).filter(Boolean)
  const issues = reviews.flatMap(v => v.issues)
  log(`Arhitectura runda ${r}: scoruri ${reviews.map(v => v.score).join('/')}, ${issues.length} probleme`)
  if (reviews.length === 2 && reviews.every(v => v.approved && v.score >= 10) && !issues.length) break
  if (r === 4) { log('Arhitectura: limita de 4 runde atinsa — continui cu problemele ramase transmise implementarii'); specCur = { ...specCur, summary: specCur.summary + ' | PROBLEME ARHITECTURALE RAMASE DE REZOLVAT IN IMPLEMENTARE: ' + JSON.stringify(issues).slice(0, 4000) }; break }
  specCur = await agent(`${CTX}\nROL: ARHITECT (revizie runda ${r}). Reviseaza ${specCur.contract_path} pe feat/admin-live (clona ~/work/3dscan-admin, git pull) rezolvand TOATE problemele recenzentilor: ${JSON.stringify(issues).slice(0, 8000)}. Commit + push. Intoarce caile si listele de sarcini actualizate.`, { label: `Arhitect revizie r${r}`, phase: 'Arhitectura', schema: SPEC })
}

phase('Implementare')
const [be, fe] = await parallel([
  () => agent(`${CTX}
ROL: ECHIPA BACKEND. Contractul: ${specCur.contract_path} pe branch feat/admin-live (git pull mai intai). Rezumat arhitect: ${specCur.summary}
Sarcinile tale: ${JSON.stringify(spec.backend_tasks)}
Implementeaza complet + teste automate in Site/tests (conventia existenta): roluri/403/401, ticket stream, SSE primeste evenimentul unei cereri API in <1 s, persistare batch, telemetrie (validare, cote, rate limit), revocare sesiune, job backup executat cap-coada in stack izolat (fisier creat, sha256 corect, descarcare autentificata), endpoint-urile vechi neschimbate (ruleaza testele existente). Scrie Site/docs/ADMIN_TELEMETRIE.md. Commit + push pe feat/admin-live. deploy_steps = pasii exacti pentru productie (build, migrare, env ADMIN_EMAILS, servicii noi).`, { label: 'Backend admin', phase: 'Implementare', schema: RESULT }),
  () => agent(`${CTX}
ROL: ECHIPA FRONTEND. Contractul: ${specCur.contract_path} pe branch feat/admin-live (git pull mai intai). Rezumat arhitect: ${specCur.summary}
Sarcinile tale: ${JSON.stringify(spec.frontend_tasks)}
Construieste public/admin/ (index.html + admin.css + admin.js, eventual module separate), fara inline script/style (CSP), fara CDN, fara framework greu: navigare pe sectiuni (Live, Functii aplicate, Utilizatori, Date, Server, Salvare, Jurnal), panou live cu flux care se actualizeaza in timp real, contoare, filtre, pauza/reluare, detalii expandabile per eveniment (JSON formatat), preview imagini, buton Salvare acum + lista backup-uri + descarcare, stari loading/eroare/gol, responsive (merge si pe telefon), tema luminoasa si intunecata, accesibil. Vizual coerent cu public/cont si public/biblioteca. Testeaza contra backend-ului cand apare pe branch (poti folosi date mock doar in timpul dezvoltarii; in versiunea comisa fara mock). Commit + push pe feat/admin-live.`, { label: 'Frontend admin', phase: 'Implementare', schema: RESULT }),
])

phase('Integrare')
const integ = await agent(`${CTX}
ROL: INTEGRARE/QA. Branch feat/admin-live (git pull). Rapoarte (date): backend=${JSON.stringify(be).slice(0, 4000)} frontend=${JSON.stringify(fe).slice(0, 3000)}
Porneste stack-ul izolat complet (inclusiv worker si serviciul de backup) pe 127.0.0.1:4190, ruleaza migrarile, creeaza un admin de test si un user de test (credentiale generate, nescrise in chat sau commit). Verifica E2E: login admin in /admin/ (foloseste browserul integrat mcp__Claude_Browser__* nu se poate catre server; deci verifica prin curl + un script node headless sau prin tunel ssh -L 4190:127.0.0.1:4190 si apoi browserul integrat pe http://localhost:4190/admin/ — fa screenshot-uri ale fiecarei sectiuni), genereaza trafic ca un iPhone (login user, upsert proiect/biblioteca/inventar, upload video mic, telemetrie batch) si confirma ca apare live in panou; Salvare acum -> backup terminat si descarcabil; non-admin -> 403. Repara bug-urile de integrare gasite (commit-uri mici, pull --rebase). Ruleaza toate testele. La final down -v si inchide tunelul.`, { label: 'Integrare E2E', phase: 'Integrare', schema: RESULT })

phase('Audit')
const LENSES = [
  'SECURITATE: autorizare pe FIECARE endpoint admin (fara token, user non-admin, token expirat/revocat), ticket stream (expirare, reutilizare), scurgeri de date (tokenuri/parole/body in admin_events sau loguri), CSP pastrat, path traversal la descarcarea backup-urilor si asset-urilor, grant-uri DB minime, rate limit telemetrie',
  'CORECTITUDINE SI COMPLETITUDINE: conformitate cu ADMIN_ARHITECTURA.md si cu cerinta utilizatorului (toate sectiunile functioneaza cu date reale), migrarea 012 idempotenta si fara coliziune cu 009-011, impactul middleware-ului pe API-urile existente (re-ruleaza TOATE testele vechi si noi), backup cap-coada cu sha256, retentie/curatare, contract ADMIN_TELEMETRIE.md complet si implementabil pe iOS',
  'UX SI OPERARE: E2E prin tunel ssh -L catre stack-ul izolat + browserul integrat (mcp__Claude_Browser__*) pe localhost: fiecare sectiune /admin/ arata date reale, live se actualizeaza in timp real, stari gol/eroare/loading, mobil (resize_window mobile) si tema intunecata, accesibilitate de baza, consola fara erori; documentatia de deploy corecta si completa',
]
const history = []
let audits = [], round = 0
while (true) {
  round++
  audits = (await parallel(LENSES.map((lens, i) => () => agent(`${CTX}
ROL: AUDITOR INDEPENDENT runda ${round} (nu ai scris codul, nu repari, nu faci push). Lentila ta: ${lens}.
Auditeaza origin/feat/admin-live fata de origin/main, in clona proprie ~/work/3dscan-audit${i} (stearsa la final). Raport integrare (date): ${JSON.stringify(integ).slice(0, 3000)}${history.length ? `\nIstoric runde anterioare (date; verifica si ca remedierile declarate chiar exista): ${JSON.stringify(history).slice(-6000)}` : ''}
Re-ruleaza testele in stack izolat -p 3dscan-audit${i} pe 127.0.0.1:${4191 + i}, apoi down -v. Nota 10 = zero constatari de orice severitate pe lentila ta, totul verificat prin rulare, nu prin citire. Orice constatare (inclusiv minora) => nota < 10. merge_ready=true doar fara constatari blocante/majore.`, { label: `Audit r${round}.${i + 1}`, phase: 'Audit', schema: AUDIT })))).filter(Boolean)
  const findings = audits.flatMap(a => a.findings)
  const scores = audits.map(a => a.score)
  log(`Audit runda ${round}: note ${scores.join('/')}, ${findings.length} constatari`)
  history.push({ round, scores, findings: findings.map(f => `${f.severity}: ${f.description} @ ${f.location}`) })
  if (audits.length === LENSES.length && scores.every(s => s >= 10) && !findings.length) break
  if (round >= 8) { log('Limita de 8 runde de audit atinsa fara 10/10 — raportez constatarile ramase'); break }
  phase('Remediere')
  await agent(`${CTX}
ROL: ECHIPA DE REMEDIERE runda ${round}. Clona ~/work/3dscan-admin, branch feat/admin-live (git pull). Rezolva TOATE constatarile auditului (blocante, majore SI minore), cu teste care dovedesc fiecare remediere; nu ascunde constatari, nu slabi testele. Daca o constatare e gresita, demonstreaza prin rulare si explica in Site/docs/ADMIN_AUDIT_RASPUNS.md (sectiunea runda ${round}). Ruleaza toate testele in stack izolat pe 127.0.0.1:4190 (down -v la final). Commit + push.
Constatari: ${JSON.stringify(findings).slice(0, 12000)}`, { label: `Remediere r${round}`, phase: 'Remediere', schema: RESULT })
  phase('Audit')
}

return { spec: specCur, backend: be, frontend: fe, integration: integ, audit_rounds: history, final_audits: audits }