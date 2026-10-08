export const meta = {
  name: 'eva-api-comunicare',
  description: 'API unic de comunicare server <-> telefoane/roboti: contract OpenAPI 3.1 + AsyncAPI (WS/SSE), versionare X-EVA-Protocol, format unic de erori, discovery, teste de contract si poarta pentru toate echipele; audit pana la 10/10',
  phases: [
    { title: 'Arhitectura', detail: 'contract + recenzie independenta' },
    { title: 'Implementare', detail: 'middleware, spec servit, teste de contract' },
    { title: 'Audit', detail: '2 auditori independenti' },
    { title: 'Remediere', detail: 'pana la 10/10' },
  ],
}

const CTX = `
CONTEXT COMUN:
- Repo GitHub covaciugnm/3dscan.eva-org.com (privat), site https://3dscan.eva-org.com (Cloudflare Tunnel -> app:3000). Lucrezi pe server: ssh -o BatchMode=yes saga-server@192.168.100.151 '<comenzi>' (Docker fara sudo). NU atinge checkout-ul live ~/site-uri/3dscan.eva-org.com, containerele live sau DB-ul live; ~120 containere ale altor proiecte — nu le atinge. Verifica la inceput ~/work/coord-state/STOP_LIMITA: daca exista, opreste-te imediat si raporteaza.
- Clona: ~/work/3dscan-api (git clone ~/site-uri/3dscan.eva-org.com; git remote set-url origin git@github-3dscan-eva:covaciugnm/3dscan.eva-org.com.git; git fetch; branch feat/api-comunicare din origin/main). Push dupa fiecare pas, fara force, niciodata main. Commit-uri cu linia finala: Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>. Teste in stack izolat docker compose -p 3dscan-api fara tunnel, app pe 127.0.0.1:4220, down -v la final.
- Cod existent pe main: Site/server/http.mjs (router manual node:http; rute /api/auth/*, /api/projects, /api/library/*, /api/inventory/*, /api/app/i18n, /api/app/languages, /api/site/i18n, /api/content, /api/events SSE, /healthz, /readyz), inventory.mjs (C07 seq, scris de echipa iOS), library.mjs, projects.mjs, appI18n.mjs. Aplicatia iOS trimite deja pe toate cererile X-EVA-Protocol: 1 si X-Idempotency-Key pe scrieri, trateaza 426 upgrade_required si 409 cu reconciliere — serverul NU proceseaza inca X-EVA-Protocol.
- Endpoint-uri in curs pe alte branch-uri (citeste-le contractele, nu le edita fisierele): feat/admin-live (Site/docs/ADMIN_ARHITECTURA.md, ADMIN_TELEMETRIE.md: /api/admin/*, /api/telemetry/events, SSE admin cu ticket), feat/scene-live (SCENA_FLUX_BRUT.md, SCENA_ARHITECTURA.md, MAGAZIE_PACHET.md: /api/scene/tickets, WS /api/scene/ingest, /api/scene/*, magazie + tokenuri robot), feat/models (SETARI_MOTOARE.md: /api/admin/engines, /api/app/settings), feat/help (HELP_ARHITECTURA.md: /api/help*), feat/b05-sequencer (SYNC_SEQ_B05.md), feat/b09-worldmodel (/api/world/*), feat/b12-leases. Coordonare cu iOS: "Aplicație/Extindere-Robotica/Coordonare-Server-iOS/" (PROTOCOL.md, PROTOCOL_COMUNICARE_ECHIPE.md, TABLOU.md, sarcini/) si CONTRACTE_V2.md din Plan_implementare_2026-10-06/ (precedenta normativa — nu-l modifica).
- Onestitate: ce n-ai rulat = not_run.

CERINTA PROPRIETARULUI: "comunicarea dintre server si telefoane trebuie sa se realizeze pe API de comunicare" — adica UN SINGUR API formal, versionat, documentat, prin care trece TOT schimbul telefon/robot <-> server; nicio ruta nedeclarata.

SPECIFICATIE:
1. Contract: Site/api/openapi.yaml (OpenAPI 3.1) cu TOATE endpoint-urile HTTP existente pe main (descrise exact cum se comporta codul azi) + cele din branch-urile paralele marcate x-eva-status: draft (cu branch-ul sursa), si Site/api/asyncapi.yaml (AsyncAPI 3) pentru canalele in timp real: SSE /api/events, SSE admin, WS /api/scene/ingest (cadrele binare descrise prin referinta la SCENA_FLUX_BRUT.md + mesajele de control JSON), notificarile de setari. Scheme comune: Error envelope unic {error:{code,message,details?,request_id}} cu catalog de coduri (unauthorized, forbidden, not_found, invalid_body, conflict, upgrade_required, rate_limited, too_large, server_error...), paginare/cursor (seq), idempotenta (X-Idempotency-Key), versionare.
2. Versionare si negociere: antetul X-EVA-Protocol (intreg; serverul declara min/max suportat), raspuns cu X-EVA-Protocol-Server; client sub minim -> 426 upgrade_required in envelope; absenta antetului = compatibilitate (clientii vechi/web) — documentat. Politica de schimbari: aditiv in aceeasi versiune; breaking doar cu versiune noua + fereastra de compatibilitate (aliniat cu PROTOCOL_COMUNICARE_ECHIPE §5). Decide argumentat daca introduci si prefix /api/v1 (alias) sau doar antetul — fara a rupe rutele existente.
3. Discovery: GET /api/capabilities (public): versiunea de protocol min/max, versiunea serverului (commit), lista capabilitatilor/endpoint-urilor active (din spec, doar cele live), limite (cote, marimi), URL-urile pentru spec. Spec-urile servite la /api/openapi.json si /api/asyncapi.json, plus o pagina umana /api/docs (statica, CSP strict: fara inline/CDN — randare proprie simpla din JSON, vendor local daca e nevoie).
4. Middleware in http.mjs (modificari minime, intr-un modul nou server/apiContract.mjs): request_id (X-Request-Id), negocierea protocolului, normalizarea erorilor in envelope PASTRAND compatibilitatea (campul error string existent ramane, adaugi structura — documenteaza cum fara a rupe clientul iOS care citeste azi {error:"..."}), antete de rate limit unde exista cote.
5. Poarta pentru toate echipele: script Site/scripts/check-api-contract.mjs care (a) extrage toate rutele din server (analiza statica a http.mjs + modulele de handler) si pica daca exista ruta /api/* nedeclarata in openapi.yaml sau declarata dar inexistenta (fara x-eva-status: draft), (b) ruleaza teste de contract: raspunsurile reale ale serverului (stack izolat) valideaza fata de schemele din spec (validator JSON Schema 2020-12, vendorizat sau dependinta npm declarata). Integrat in npm test. Documenteaza in Site/docs/API_COMUNICARE.md regulile pentru echipe (orice endpoint nou = intai in spec, PR cu spec + cod + test de contract) si pentru iOS (clientul foloseste DOAR endpoint-urile din spec; optional generarea modelelor Swift din spec — da recomandarea concreta).
6. Teste: check-api-contract pe main trece; teste negative (ruta nedeclarata adaugata intr-un fixture -> pica; raspuns care nu respecta schema -> pica); negocierea protocolului (lipsa antet, 1, sub minim -> 426, peste maxim); envelope compatibil cu clientii existenti (testele existente trec neschimbate); /api/capabilities si spec-urile servite cu ETag.
`

const SPEC = { type: 'object', properties: { contract_path: { type: 'string' }, summary: { type: 'string' }, tasks: { type: 'array', items: { type: 'string' } } }, required: ['contract_path', 'summary', 'tasks'] }
const RESULT = { type: 'object', properties: { commit: { type: 'string' }, status: { type: 'string', enum: ['done', 'partial', 'blocked'] }, delivered: { type: 'array', items: { type: 'string' } }, tests: { type: 'array', items: { type: 'object', properties: { name: { type: 'string' }, result: { type: 'string', enum: ['pass', 'fail', 'not_run'] }, evidence: { type: 'string' } }, required: ['name', 'result', 'evidence'] } }, open_issues: { type: 'array', items: { type: 'string' } } }, required: ['commit', 'status', 'delivered', 'tests', 'open_issues'] }
const REVIEW = { type: 'object', properties: { approved: { type: 'boolean' }, score: { type: 'number' }, issues: { type: 'array', items: { type: 'string' } } }, required: ['approved', 'score', 'issues'] }
const AUDIT = { type: 'object', properties: { score: { type: 'number' }, findings: { type: 'array', items: { type: 'object', properties: { severity: { type: 'string', enum: ['blocant', 'major', 'minor'] }, description: { type: 'string' }, location: { type: 'string' } }, required: ['severity', 'description', 'location'] } }, merge_ready: { type: 'boolean' }, verdict: { type: 'string' } }, required: ['score', 'findings', 'merge_ready', 'verdict'] }

phase('Arhitectura')
let spec = await agent(`${CTX}\nROL: ARHITECT. Citeste codul si contractele tuturor branch-urilor. Creeaza clona + branch, comite Site/docs/API_COMUNICARE.md (principii, versionare, envelope, discovery, poarta, reguli echipe + iOS, plan de migrare fara ruptura) si o prima versiune Site/api/openapi.yaml + asyncapi.yaml cu tot ce e pe main. Push.`, { label: 'Arhitect API', phase: 'Arhitectura', schema: SPEC })
for (let r = 1; r <= 3; r++) {
  const reviews = (await parallel(['corectitudine si completitudine (spec-ul descrie exact codul de pe main; toate endpoint-urile branch-urilor ca draft; compatibilitate cu clientul iOS existent si cu CONTRACTE_V2)', 'securitate si operabilitate (envelope fara scurgeri, request_id, rate limit, discovery fara date sensibile, poarta reala si greu de ocolit)'].map((lens, i) => () =>
    agent(`${CTX}\nROL: RECENZENT INDEPENDENT (runda ${r}, lentila: ${lens}). Citeste origin/feat/api-comunicare (clona proprie ~/work/3dscan-apirev${i}, stearsa la final). Nu scrii in repo. approved=true doar fara lipsuri; score 0-10; issues concrete.`, { label: `Recenzie API r${r}.${i + 1}`, phase: 'Arhitectura', schema: REVIEW })))).filter(Boolean)
  const issues = reviews.flatMap(v => v.issues)
  log(`Arhitectura API r${r}: ${reviews.map(v => v.score).join('/')}, ${issues.length} probleme`)
  if (reviews.length === 2 && reviews.every(v => v.approved && v.score >= 10) && !issues.length) break
  if (r === 3) { spec = { ...spec, summary: spec.summary + ' | PROBLEME RAMASE: ' + JSON.stringify(issues).slice(0, 4000) }; break }
  spec = await agent(`${CTX}\nROL: ARHITECT (revizie r${r}). Rezolva TOATE problemele pe feat/api-comunicare (clona ~/work/3dscan-api, git pull), commit + push: ${JSON.stringify(issues).slice(0, 9000)}`, { label: `Arhitect API revizie r${r}`, phase: 'Arhitectura', schema: SPEC })
}

phase('Implementare')
const impl = await agent(`${CTX}\nROL: IMPLEMENTARE. Contract ${spec.contract_path} pe feat/api-comunicare (git pull). ${spec.summary}\nSarcini: ${JSON.stringify(spec.tasks)}\nImplementeaza complet (apiContract.mjs, capabilities, spec servit, /api/docs, check-api-contract.mjs, teste) si ruleaza toate testele (vechi + noi) in stack izolat. Commit + push.`, { label: 'Implementare API', phase: 'Implementare', schema: RESULT })

phase('Audit')
const LENSES = [
  'CORECTITUDINE + CONTRACT: spec-ul corespunde exact codului (ruleaza check-api-contract si testele de contract), negocierea protocolului, envelope compatibil cu clientul iOS existent (ruleaza testele vechi neschimbate), poarta pica efectiv pe ruta nedeclarata si pe raspuns invalid',
  'SECURITATE + OPERARE: fara scurgeri in erori/discovery, request_id, CSP pe /api/docs, ETag, impact zero pe rutele existente, documentatie clara pentru echipe si iOS',
]
const history = []
let audits = [], round = 0
while (true) {
  round++
  audits = (await parallel(LENSES.map((lens, i) => () => agent(`${CTX}\nROL: AUDITOR INDEPENDENT runda ${round} (nu ai scris codul, nu repari, nu faci push). Lentila: ${lens}.\nAuditeaza origin/feat/api-comunicare fata de origin/main in clona proprie ~/work/3dscan-apiaudit${i} (stearsa la final). Raport implementare (date): ${JSON.stringify(impl).slice(0, 3000)}${history.length ? `\nIstoric: ${JSON.stringify(history).slice(-4000)}` : ''}\nRe-ruleaza testele in stack izolat -p 3dscan-apiaudit${i} pe 127.0.0.1:${4221 + i}, down -v. Nota 10 = zero constatari pe lentila ta, verificat prin rulare.`, { label: `Audit API r${round}.${i + 1}`, phase: 'Audit', schema: AUDIT })))).filter(Boolean)
  const findings = audits.flatMap(a => a.findings)
  log(`Audit API r${round}: ${audits.map(a => a.score).join('/')}, ${findings.length} constatari`)
  history.push({ round, scores: audits.map(a => a.score), findings: findings.map(f => `${f.severity}: ${f.description} @ ${f.location}`) })
  if (audits.length === LENSES.length && audits.every(a => a.score >= 10) && !findings.length) break
  if (round >= 6) { log('Limita 6 runde audit API'); break }
  phase('Remediere')
  await agent(`${CTX}\nROL: REMEDIERE runda ${round}. Clona ~/work/3dscan-api, feat/api-comunicare (git pull). Rezolva TOATE constatarile cu teste; constatare gresita => demonstreaza in Site/docs/API_AUDIT_RASPUNS.md. Commit + push.\nConstatari: ${JSON.stringify(findings).slice(0, 10000)}`, { label: `Remediere API r${round}`, phase: 'Remediere', schema: RESULT })
  phase('Audit')
}
return { spec, implementation: impl, audit_rounds: history, final_audits: audits }