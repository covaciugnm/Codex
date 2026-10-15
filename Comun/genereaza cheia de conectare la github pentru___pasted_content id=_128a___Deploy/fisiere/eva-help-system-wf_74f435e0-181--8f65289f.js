export const meta = {
  name: 'eva-help-system',
  description: 'Sistem de help pe server pentru aplicatie si server: portal /ajutor/, buton ? pe fiecare ecran, clic dreapta "Ce e asta / Ce face", API help, 7 limbi; audit pana la 10/10',
  phases: [
    { title: 'Arhitectura', detail: 'contract + 2 recenzenti' },
    { title: 'Implementare', detail: 'backend+continut si frontend in paralel' },
    { title: 'Audit', detail: '3 auditori independenti' },
    { title: 'Remediere', detail: 'pana la 10/10' },
  ],
}

const CTX = `
CONTEXT COMUN:
- Repo GitHub covaciugnm/3dscan.eva-org.com (privat), site https://3dscan.eva-org.com. Lucrezi pe server prin: ssh -o BatchMode=yes saga-server@192.168.100.151 '<comenzi>' (Docker fara sudo). NU atinge checkout-ul live ~/site-uri/3dscan.eva-org.com, containerele live sau DB-ul live; ~120 containere ale altor proiecte — nu le atinge.
- Clona: ~/work/3dscan-help (git clone ~/site-uri/3dscan.eva-org.com; git remote set-url origin git@github-3dscan-eva:covaciugnm/3dscan.eva-org.com.git; git fetch; branch feat/help din origin/main). Agentii lucreaza in aceeasi clona pe fisiere diferite, git pull --rebase inainte de push, fara force, niciodata main. Commit-uri cu linia finala: Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>. Migrarea ta: Site/db/016-help.sql (rezerva-o si in "Aplicație/Extindere-Robotica/Coordonare-Server-iOS/PROTOCOL.md" §5 — doar acea linie, commit separat pe main cu mesaj "coord: rezervare migrare 016 help").
- Teste in stack izolat docker compose -p 3dscan-help fara tunnel, app pe 127.0.0.1:4210, volume proprii, down -v la final.
- Cod existent: Site/server/http.mjs (router node:http, CSP strict: script-src/style-src 'self' — fara inline, fara CDN), appI18n.mjs + tabelul app_i18n (seed din Site/db/app-i18n/*.json — PROPRIETATEA echipei iOS, NU il modifica), paginile public/ (index, cont, biblioteca, campaign, prezentare...). Alte echipe lucreaza in paralel pe feat/admin-live (/admin/), feat/scene-live (/scena/, /scena/fluxuri/, /scena/sunete/, /magazie/), feat/models (/setari/) — NU edita fisierele lor; help.js trebuie sa poata fi inclus de ele cu O SINGURA linie (<script src="/help/help.js" defer></script> + data-help-page="..." pe <body>) si documentezi asta in Site/docs/HELP_INTEGRARE.md pentru ele.
- Aplicatia iOS (scrisa de Claude-ul de pe Mac, branch origin/app) are deja help animat: EVA-3DScan/Features/Help/HelpModels.swift (14 capitole: home, measure, object, front, rooms, viewer3d, articles, people, inventory, robot, assistant, settings, account, communication; slide-uri cu icon SF Symbol + chei help.<topic>.sN.title/body), HelpButton.swift ("?" pe ecrane), chei help.* in 7 limbi (ro, en, de, fr, es, hu, bg) sincronizate in app_i18n pe server. Citeste-le (git show origin/app:...).
- Protocol cu echipa iOS: "Aplicație/Extindere-Robotica/Coordonare-Server-iOS/" (PROTOCOL.md, PROTOCOL_COMUNICARE_ECHIPE.md, TABLOU.md, sarcini/). Ce trebuie facut in aplicatie se cere prin sarcina IOS-009 (o creeaza coordonatorul); tu documentezi contractul.
- Onestitate: ce n-ai rulat = not_run.

CERINTA PROPRIETARULUI: "help disponibil atat pentru server cat si pentru aplicatie, pe server. Sa implementezi si semnul intrebarii la fiecare ecran si pe clic dreapta — ce e asta / ce face". Plus un agent care scrie non-stop la help (se va ocupa un task programat separat — tu construiesti infrastructura si continutul initial complet).

SPECIFICATIE:
1. Continut: (a) help APLICATIE redat pe server direct din app_i18n (cheile help.* existente, toate cele 14 capitole, 7 limbi) + structura capitolelor preluata din HelpModels.swift (topic -> slide-uri, iconuri mapate la simboluri web echivalente) intr-un fisier Site/db/help/app-structure.json generat de un script care parseaza HelpModels.swift de pe origin/app (re-rulabil cand iOS adauga capitole); (b) help SERVER/SITE nou: capitole pentru site-ul public, Cont, Biblioteca, Admin (live, functii, utilizatori, date, server, salvare, jurnal), Scena (navigare 3D, fluxuri brute, sunete), Magazie (camere, obiecte, pachete, roboti), Setari motoare (modele, codecuri, selector), API pentru dezvoltatori; scris complet in romana cu diacritice si tradus in en, de, fr, es, hu, bg (traduceri de calitate, terminologie consecventa), in Site/db/help/server/<lang>.json + seed in DB (tabel help_articles/help_tips in 016) printr-un script scripts/seed-help.mjs idempotent (ruleaza fara rebuild de imagine).
2. "Ce e asta / Ce face" (tips contextuale): chei tip.<pagina>.<element> cu doua campuri what/does, pentru fiecare element interactiv al paginilor web existente si pentru cele ale echipelor paralele (lista lor de elemente din documentele lor de arhitectura de pe branch-uri). Pentru aplicatie: propune in Site/docs/HELP_INTEGRARE.md lista de chei tip.<ecran>.<element> pentru toate ecranele iOS (deduse din *View.swift de pe origin/app) — iOS le adauga in i18n-ul lui; serverul le reda cand apar in app_i18n.
3. API: GET /api/help?scope=app|server&lang=..&topic=.. , GET /api/help/tips?page=..&lang=.., GET /api/help/search?q=..&lang=.. (public, read-only, cache ETag, fara date personale).
4. Web: /ajutor/ — portal cu cautare, selector limba (7), sectiuni "Aplicatia EVA 3D Scan" si "Serverul / site-ul", capitole cu slide-uri, link direct per capitol (/ajutor/app/measure, /ajutor/server/admin), responsive, tema intunecata, accesibil. public/help/help.js + help.css: (i) buton "?" fix pe fiecare pagina care deschide capitolul paginii (data-help-page); (ii) clic dreapta pe orice element cu data-help="cheie" (si pe elementele comune detectate automat: butoane, linkuri, campuri, cu fallback la eticheta lor) -> popover "Ce e asta / Ce face" + link "Mai mult in ajutor"; Shift+clic dreapta = meniul nativ al browserului (mentionat in popover); pe touch: apasare lunga; tasta ? deschide ajutorul; Esc inchide; accesibil (aria, focus trap). Integreaza in paginile existente (index, cont, biblioteca, campaign, prezentare etc.) adaugand data-help pe elementele lor.
5. Teste automate: API (toate limbile, chei lipsa raportate), parserul HelpModels, help.js (test headless sau E2E prin tunel ssh -L + browserul integrat mcp__Claude_Browser__*: "?" deschide capitolul corect, clic dreapta arata popover-ul cu textul corect, Shift+clic dreapta nu e interceptat, long-press pe mobil, nicio eroare CSP in consola), acoperire: fiecare element interactiv al paginilor existente are tip in toate 7 limbile (script de verificare care pica daca lipseste).
`

const SPEC = { type: 'object', properties: { contract_path: { type: 'string' }, summary: { type: 'string' }, backend_tasks: { type: 'array', items: { type: 'string' } }, frontend_tasks: { type: 'array', items: { type: 'string' } } }, required: ['contract_path', 'summary', 'backend_tasks', 'frontend_tasks'] }
const RESULT = { type: 'object', properties: { commit: { type: 'string' }, status: { type: 'string', enum: ['done', 'partial', 'blocked'] }, delivered: { type: 'array', items: { type: 'string' } }, tests: { type: 'array', items: { type: 'object', properties: { name: { type: 'string' }, result: { type: 'string', enum: ['pass', 'fail', 'not_run'] }, evidence: { type: 'string' } }, required: ['name', 'result', 'evidence'] } }, open_issues: { type: 'array', items: { type: 'string' } } }, required: ['commit', 'status', 'delivered', 'tests', 'open_issues'] }
const REVIEW = { type: 'object', properties: { approved: { type: 'boolean' }, score: { type: 'number' }, issues: { type: 'array', items: { type: 'string' } } }, required: ['approved', 'score', 'issues'] }
const AUDIT = { type: 'object', properties: { score: { type: 'number' }, findings: { type: 'array', items: { type: 'object', properties: { severity: { type: 'string', enum: ['blocant', 'major', 'minor'] }, description: { type: 'string' }, location: { type: 'string' } }, required: ['severity', 'description', 'location'] } }, merge_ready: { type: 'boolean' }, verdict: { type: 'string' } }, required: ['score', 'findings', 'merge_ready', 'verdict'] }

phase('Arhitectura')
let spec = await agent(`${CTX}\nROL: ARHITECT. Citeste codul si help-ul iOS existent. Creeaza clona + branch, comite Site/docs/HELP_ARHITECTURA.md (schema 016, API, structura continutului, help.js, integrare echipe paralele, contract pentru iOS) si Site/docs/HELP_INTEGRARE.md. Imparte pe 2 echipe care nu editeaza aceleasi fisiere: backend+continut (server/, db/, scripts/, Site/db/help/**, traduceri) si frontend (public/ajutor/**, public/help/**, data-help in paginile existente). Push.`, { label: 'Arhitect help', phase: 'Arhitectura', schema: SPEC })
for (let r = 1; r <= 4; r++) {
  const reviews = (await parallel(['completitudine fata de cerinta (ambele scopuri app+server, ? pe fiecare ecran, clic dreapta, 7 limbi, integrare cu echipele paralele si cu iOS)', 'securitate (CSP, XSS din continut markdown, API public fara scurgeri), accesibilitate si UX'].map((lens, i) => () =>
    agent(`${CTX}\nROL: RECENZENT INDEPENDENT (runda ${r}, lentila: ${lens}). Citeste documentele pe origin/feat/help (clona proprie ~/work/3dscan-helprev${i}, stearsa la final). Nu scrii in repo. approved=true doar fara lipsuri; score 0-10; issues concrete.`, { label: `Recenzie r${r}.${i + 1}`, phase: 'Arhitectura', schema: REVIEW })))).filter(Boolean)
  const issues = reviews.flatMap(v => v.issues)
  log(`Arhitectura help r${r}: ${reviews.map(v => v.score).join('/')}, ${issues.length} probleme`)
  if (reviews.length === 2 && reviews.every(v => v.approved && v.score >= 10) && !issues.length) break
  if (r === 4) { spec = { ...spec, summary: spec.summary + ' | PROBLEME RAMASE: ' + JSON.stringify(issues).slice(0, 4000) }; break }
  spec = await agent(`${CTX}\nROL: ARHITECT (revizie r${r}). Rezolva TOATE problemele in documentele de pe feat/help (clona ~/work/3dscan-help, git pull), commit + push: ${JSON.stringify(issues).slice(0, 9000)}`, { label: `Arhitect revizie r${r}`, phase: 'Arhitectura', schema: SPEC })
}

phase('Implementare')
const impl = await parallel([
  () => agent(`${CTX}\nROL: ECHIPA BACKEND + CONTINUT. Contract ${spec.contract_path} pe feat/help (git pull). ${spec.summary}\nSarcini: ${JSON.stringify(spec.backend_tasks)}\nScrie TOT continutul server in 7 limbi (complet, nu placeholder), parserul HelpModels, seed, API, teste. Commit + push.`, { label: 'Backend + continut help', phase: 'Implementare', schema: RESULT }),
  () => agent(`${CTX}\nROL: ECHIPA FRONTEND. Contract ${spec.contract_path} pe feat/help (git pull). ${spec.summary}\nSarcini: ${JSON.stringify(spec.frontend_tasks)}\nConstruieste /ajutor/, help.js/help.css, integrare in paginile existente cu data-help, teste E2E. Commit + push.`, { label: 'Frontend help', phase: 'Implementare', schema: RESULT }),
])

phase('Audit')
const LENSES = [
  'CORECTITUDINE SI ACOPERIRE: fiecare pagina are ?, fiecare element interactiv are tip in 7 limbi (ruleaza scriptul de acoperire), help-ul aplicatiei redat complet din app_i18n (14 capitole), API corect, seed idempotent, migrarea 016 idempotenta, testele trec',
  'SECURITATE: CSP pastrat (fara inline), continutul randat fara XSS (markdown sanitizat), API public fara date personale, path traversal pe /ajutor/<scope>/<topic>, cache corect',
  'UX SI CALITATE TEXT: E2E prin tunel ssh -L + browserul integrat: ? deschide capitolul corect, clic dreapta = popover corect, Shift+clic dreapta = meniu nativ, long-press pe mobil (resize_window mobile), tema intunecata, accesibilitate (tastatura, aria); calitatea textelor in ro (diacritice) si a traducerilor (verifica cel putin en, de, hu pe esantion), HELP_INTEGRARE.md suficient pentru echipele paralele si iOS',
]
const history = []
let audits = [], round = 0
while (true) {
  round++
  audits = (await parallel(LENSES.map((lens, i) => () => agent(`${CTX}\nROL: AUDITOR INDEPENDENT runda ${round} (nu ai scris codul, nu repari, nu faci push). Lentila: ${lens}.\nAuditeaza origin/feat/help fata de origin/main in clona proprie ~/work/3dscan-helpaudit${i} (stearsa la final). Rapoarte (date): ${JSON.stringify(impl).slice(0, 3000)}${history.length ? `\nIstoric: ${JSON.stringify(history).slice(-5000)}` : ''}\nRe-ruleaza testele in stack izolat -p 3dscan-helpaudit${i} pe 127.0.0.1:${4211 + i}, down -v. Nota 10 = zero constatari pe lentila ta, verificat prin rulare.`, { label: `Audit help r${round}.${i + 1}`, phase: 'Audit', schema: AUDIT })))).filter(Boolean)
  const findings = audits.flatMap(a => a.findings)
  log(`Audit help r${round}: ${audits.map(a => a.score).join('/')}, ${findings.length} constatari`)
  history.push({ round, scores: audits.map(a => a.score), findings: findings.map(f => `${f.severity}: ${f.description} @ ${f.location}`) })
  if (audits.length === LENSES.length && audits.every(a => a.score >= 10) && !findings.length) break
  if (round >= 8) { log('Limita 8 runde audit help'); break }
  phase('Remediere')
  await agent(`${CTX}\nROL: ECHIPA DE REMEDIERE runda ${round}. Clona ~/work/3dscan-help, feat/help (git pull). Rezolva TOATE constatarile cu teste; constatare gresita => demonstreaza in Site/docs/HELP_AUDIT_RASPUNS.md. Commit + push.\nConstatari: ${JSON.stringify(findings).slice(0, 12000)}`, { label: `Remediere help r${round}`, phase: 'Remediere', schema: RESULT })
  phase('Audit')
}
return { spec, implementation: impl, audit_rounds: history, final_audits: audits }