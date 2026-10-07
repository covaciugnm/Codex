export const meta = {
  name: 'dracula-v4-pipeline',
  description: 'DRACULA (v4): canon → aliniere echipe → arc → 20 ploturi + 20 povestiri → scenariu → QA → site, fiecare livrabil prin Poarta 9,50 cu arhivare completă',
  whenToUse: 'Pipeline-ul complet al proiectului DRACULA COMICS după deciziile Producătorului 1–14; reluabil cu resumeFromRunId',
  phases: [
    { title: 'G0 Canon & Studio v4', detail: 'canon v4 + organizare v4, audit' },
    { title: 'G1 Aliniere & Fundație', detail: 'A/B/C/E aliniate la v4 și auditate' },
    { title: 'G2 Arc sezon', detail: 'arcul Sezonului 1 + harta episoadelor' },
    { title: 'G3 Episoade', detail: 'plot → audit → povestire → audit, per episod' },
    { title: 'G4 Scenariu BD', detail: 'scenariul EP01 + șablon' },
    { title: 'G5 QA & Site', detail: 'continuitate + site local' },
    { title: 'Registru', detail: 'registrul central de audit + jurnal' },
  ],
}

const ROOT = String.raw`D:\00. Downloads\Dracula Book\DRACULA-COMICS`
const P = (rel) => ROOT + '\\' + rel.replace(/\//g, '\\')
const CANON = P('01_CANON/00_CANON_NUCLEU.md')
const DECIZII = P('01_CANON/01_DECIZII_PRODUCATOR.md')
const STUDIO = P('00_STUDIO/01_ECHIPA_SI_ROADMAP.md')
const JURNAL = P('00_STUDIO/03_JURNAL_PROGRES.md')
const AUDIT_DIR = P('00_STUDIO/audit')
const DOSAR = (code) => P(`00_STUDIO/audit/${code}`)
const PASS = 9.5
const MAX_ROUNDS = 6
const DATE = (args && args.date) || '24.09.2026'
const ONLY = (args && args.only) || null   // opțional: listă de faze de rulat
const run = (g) => !ONLY || ONLY.includes(g)

const LOCKED = `DECIZIILE BLOCATE ALE PRODUCĂTORULUI — registrul complet: ${DECIZII} (CITEȘTE-L INTEGRAL; orice contradicție = defect CRITIC). Pe scurt:
1) Eroul = VLAD al III-lea Drăculea însuși (n. 1431 Sighișoara). 2) 1431–1476 = istorie reală STRICTĂ. 3) Continuitate proprie, diferită de romanele editurii. 4) Nemuritor prin capitalele lumii, identități schimbate; obiective universal cunoscute + clișee Hollywood. 5) Supererou pozitiv: frumos, atletic, super-inteligent, sofisticat, simțuri supradezvoltate (Mentalist), zboară, se transformă; familie de conți transilvăneni foarte bogați și puternici; Saga + supereroi pozitivi. 6) Română cu diacritice (prompturile de ilustrație în EN). 7) Poarta 9,50 + arhivare completă în ${AUDIT_DIR}. 8) Orice roman/scenariu/serial/BD/joc de succes e sursă; contează modul de prezentare. 9) TITLUL SERIEI = doar „DRACULA” + subtitlu pe arc (S1: „DRACULA — Sângele Dragonului”); „Contele Nopții” ELIMINAT peste tot. 10) NU e legat de noapte — acțiune și ZIUA („all day long”). 11) FASHION ICON în ton cu fiecare epocă. 12) STIL BOND: glamour, acțiune, cai, caleașca, trenuri de lux, mașini, avioane, iahturi, lux, femei la superlativ, success story. 13) FĂRĂ SOȚIE ÎN PREZENT: burlac glamour; Sânziana = marea iubire înstrăinată; o femeie spectaculoasă pe episod (aliată/rivală/femme fatale), 14+. 14) Adaptat cititorului tânăr de azi: fantezie aspirațională (succes, bani, libertate, lux, călătorii), succes prin MERIT, generozitate.`

const LENSES = [
  { key: 'canon', name: 'Auditor de Canon & Istorie', focus: `coerența totală cu canonul (${CANON}) și cu registrul deciziilor blocate (${DECIZII}); EXACTITATEA ISTORICĂ (verifică datele, locurile, personajele, obiectivele și anii lor de construcție — folosește WebSearch/WebFetch prin ToolSearch "select:WebSearch,WebFetch" când ai orice dubiu; o dată istorică greșită prezentată ca fapt = defect major; un anacronism = defect major); continuitate internă (nume, vârste, ani, reguli ale puterilor, cine știe ce și când); contradicții între fișiere.` },
  { key: 'craft', name: 'Auditor de Meșteșug & Piață', focus: `calitate profesională la nivelul celor mai buni din industrie (Image/Marvel/DC, Saga, The Mentalist, francizele Bond, bestselleruri): suspans, ritm, originalitate (fără copiere de IP), profunzime emoțională, eroul pozitiv care plătește un preț, glamour și aspirație pentru cititorul tânăr de azi (decizia 14), stil Bond și fashion icon (deciziile 11–12), acțiune și ziua (decizia 10), limbă română literară impecabilă, potențial comercial (cititorul vrea episodul următor?), utilitate reală pentru echipa care folosește livrabilul; riscuri juridice (drepturi de imagine, mărci — Bond, Universal/Lugosi, mărci auto/modă).` },
  { key: 'kpi', name: 'Auditor de KPI & Completitudine', focus: `verificare punct cu punct a KPI-urilor și cerințelor din brief și din fișa de post din ${STUDIO} (numără efectiv: elemente, cuvinte — folosește Python/wc prin Bash —, pagini, secțiuni); lipsuri, fișiere lipsă, secțiuni goale sau superficiale, placeholder-e, format, diacritice, urme ale canonului vechi („Valerian”, „Drakon”, „Contele Nopții”, Sânziana-soție-în-prezent), raportul echipei completat conform șablonului.` },
]

const AUDIT_SCHEMA = {
  type: 'object',
  properties: {
    score: { type: 'number', description: 'Nota 0.00–10.00 cu două zecimale' },
    verdict: { type: 'string', enum: ['PASS', 'FAIL'] },
    strengths: { type: 'array', items: { type: 'string' } },
    defects: { type: 'array', items: { type: 'object', properties: {
      severity: { type: 'string', enum: ['critic', 'major', 'minor'] }, location: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' },
    }, required: ['severity', 'location', 'problem', 'fix'] } },
    summary: { type: 'string' },
    report_path: { type: 'string' },
  },
  required: ['score', 'verdict', 'defects', 'summary', 'report_path'],
}
const PLAN_SCHEMA = {
  type: 'object',
  properties: {
    root_causes: { type: 'array', items: { type: 'string' } },
    tasks: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, task: { type: 'string' }, acceptance: { type: 'string' }, owner: { type: 'string' },
    }, required: ['id', 'task', 'acceptance'] } },
    record_path: { type: 'string' },
  },
  required: ['root_causes', 'tasks', 'record_path'],
}

function auditPrompt(item, lens, round) {
  const rp = `${DOSAR(item.code)}\\R${round}_audit_${lens.key}.md`
  return `Ești ${lens.name} în completul de audit al DRACULA COMICS STUDIO (editura Dracula Book). Ești unul dintre cei mai severi auditori din industrie. Proiect: serie BD color + povestiri „DRACULA” (S1: „DRACULA — Sângele Dragonului”).

LIVRABIL AUDITAT: [${item.code}] ${item.name} — runda ${round} — data ${DATE}.
FIȘIERE DE CITIT INTEGRAL (nu eșantionat; dacă e un folder, toate fișierele, recursiv):
${item.files.map(f => '- ' + f).join('\n')}
REFERINȚE: registrul deciziilor ${DECIZII}, canonul ${CANON}, organizarea ${STUDIO} (fișa de post + KPI-urile rolului ${item.role}).
${LOCKED}

BRIEF / CERINȚE:
${item.brief}

LENTILA TA: ${lens.focus}

REGULI DE NOTARE (necruțător, dar corect):
- 9.50–10.00 = excepțional, l-ai semna pentru publicare la o editură de top FĂRĂ modificări substanțiale; doar defecte minore cosmetice.
- Orice defect MAJOR plafonează nota la 9.20; orice defect CRITIC la 8.50; defectele minore acumulate scad nota.
- Nu da notă mare din politețe; nu penaliza gusturi fără argument. Fiecare defect: locație exactă, problema, corectura concretă.

ARHIVARE OBLIGATORIE: salvează RAPORTUL TĂU COMPLET în ${rp} (creează folderul; markdown, română): antet (livrabil, cod, rundă, lentilă, data, fișiere verificate), NOTA și VERDICTUL (PASS dacă ≥ ${PASS}), metoda de verificare (ce ai citit, numărat, căutat pe web + surse), puncte forte, tabelul defectelor (nr., gravitate, locație, problemă, corectură), concluzia. E SINGURUL fișier pe care ai voie să-l creezi/modifici.
Returnează evaluarea structurată (report_path = ${rp}).`
}

function managerPrompt(item, audits, round) {
  const rec = `${DOSAR(item.code)}\\R${round}_plan_masuri.md`
  return `Ești Managerul echipei ${item.role} (Showrunner delegat) la DRACULA COMICS STUDIO. Livrabilul [${item.code}] ${item.name} NU a trecut poarta (minim ${PASS}/10 de la FIECARE auditor) în runda ${round}.
Convoci ședința echipei: citești cele 3 rapoarte complete (${audits.map(a => a.report_path).join(' ; ')}) și rezumatul JSON de mai jos, identifici cauzele-rădăcină și emiți PLANUL DE MĂSURI: sarcini clare, numerotate (M${round}.1, M${round}.2 …), cu responsabil și criteriu verificabil de acceptare, astfel încât runda următoare să obțină ≥${PASS} de la toți. Acoperă TOATE defectele critice și majore; grupează minorele. Arbitrează contradicțiile dintre auditori pe baza registrului deciziilor și a canonului (motivează). Adaugă îmbunătățiri proactive spre nivel de excepție.
${LOCKED}
FIȘIERELE LIVRABILULUI: ${item.files.join(' ; ')}
AUDITURILE (JSON): ${JSON.stringify(audits)}
ARHIVARE: scrie procesul-verbal + planul de măsuri în ${rec} (markdown, română): antet (livrabil, rundă, data, participanți), tabelul notelor + nota minimă + decizia „NU TRECE”, legături la rapoarte, sinteza defectelor, cauze-rădăcină, arbitraje, PLANUL DE MĂSURI (cod, sarcină, responsabil, criteriu de acceptare, stare „de executat”) și o secțiune goală „## Execuție”. Nu modifica livrabilul. Returnează root_causes, tasks, record_path = ${rec}.`
}

function revisePrompt(item, plan, round) {
  const snap = `${DOSAR(item.code)}\\R${round}_versiune_inainte_de_revizie`
  const snapTargets = item.snap || item.files
  return `Ești autorul livrabilului [${item.code}] ${item.name} (rolul ${item.role}) la DRACULA COMICS STUDIO. Auditul rundei ${round} a dat sub ${PASS}/10. Execută INTEGRAL planul de măsuri din ${plan.record_path}, direct în fișiere, la nivel de excepție (nu cosmetic).
${LOCKED}
Registru decizii: ${DECIZII}. Canon: ${CANON}. Organizare/KPI: ${STUDIO}.
FIȘIERELE LIVRABILULUI: ${item.files.join(' ; ')}
BRIEF: ${item.brief}
PAS 1 — ARHIVARE ÎNAINTE: copiază ${snapTargets.join(' ; ')} în ${snap}\\ (păstrează structura; NU copia nimic din ${AUDIT_DIR}). Verifică copia.
PAS 2 — SARCINI: ${JSON.stringify(plan.tasks)}
Reguli: citește întâi; editează complet; păstrează diacriticele; nu șterge conținut bun; ${item.canCanon ? 'ești Showrunnerul delegat: poți edita canonul, dar NU registrul deciziilor Producătorului.' : 'nu edita canonul și nici registrul deciziilor — propunerile de canon le scrii în raportul echipei (00_STUDIO/rapoarte/) la „Propuneri de modificare a canonului”.'}
PAS 3 — ARHIVARE DUPĂ: completează „## Execuție” în ${plan.record_path} (pe fiecare sarcină: stare, ce s-a făcut, fișiere/secțiuni modificate) + rezumatul diferențelor față de ${snap}. Actualizează raportul echipei din 00_STUDIO/rapoarte/ (istoric revizii).
Returnează un rezumat de maximum 10 rânduri.`
}

async function auditRound(item, round, phaseName) {
  // reîncearcă auditorii căzuți (erori API) de până la 2 ori, fără a consuma runde
  let audits = []
  for (let attempt = 0; attempt < 3 && audits.length < LENSES.length; attempt++) {
    const missing = LENSES.filter(l => !audits.find(a => a.key === l.key))
    const got = (await parallel(missing.map(lens => () =>
      agent(auditPrompt(item, lens, round), { label: `audit ${item.code} R${round} ${lens.key}${attempt ? ' retry' + attempt : ''}`, phase: phaseName, schema: AUDIT_SCHEMA })
        .then(a => a ? { key: lens.key, lens: lens.name, ...a } : null)))).filter(Boolean)
    audits = audits.concat(got)
  }
  return audits
}

async function gate(item, phaseName) {
  const history = []
  for (let round = 1; round <= MAX_ROUNDS; round++) {
    const audits = await auditRound(item, round, phaseName)
    if (audits.length < LENSES.length) {
      log(`[${item.code}] R${round}: doar ${audits.length}/3 auditori au răspuns (erori API) — oprit, se reia ulterior`)
      return { code: item.code, name: item.name, status: 'EROARE_API', rounds: round, min: null, history }
    }
    const min = Math.min(...audits.map(a => a.score))
    history.push({ round, scores: audits.map(a => ({ auditor: a.lens, score: a.score, report: a.report_path })), min })
    const passed = min >= PASS
    log(`[${item.code}] R${round}: ${audits.map(a => a.key + ' ' + a.score.toFixed(2)).join(' · ')} → min ${min.toFixed(2)} ${passed ? '✅ TRECE' : '❌'}`)
    if (passed || round === MAX_ROUNDS) {
      const status = passed ? 'PASS' : 'BLOCAT'
      await agent(`Ești grefierul de audit al DRACULA COMICS STUDIO. Arhivează REZULTATUL FINAL al porții pentru [${item.code}] ${item.name}.
1) Scrie ${DOSAR(item.code)}\\REZULTAT_FINAL.md (română): antet (livrabil, cod, rol ${item.role}, data ${DATE}), STATUS: ${passed ? '✅ TRECE POARTA 9,50' : '🔴 BLOCAT — necesită decizia Producătorului'}, runda finală ${round}, nota minimă ${min.toFixed(2)}; TABELUL ISTORIC al rundelor (rundă, nota fiecărui auditor, minimă, decizie, link la rapoarte și la R<n>_plan_masuri.md) din: ${JSON.stringify(history)}; punctele forte finale și defectele minore rămase: ${JSON.stringify(audits.map(a => ({ auditor: a.lens, score: a.score, strengths: a.strengths, defects: a.defects })))}; ${passed ? '' : 'decizia necesară de la Producător și opțiunile.'}
2) ${passed ? `Copiază versiunea APROBATĂ a ${(item.snap || item.files).join(' ; ')} în ${DOSAR(item.code)}\\VERSIUNE_APROBATA\\ (fără nimic din ${AUDIT_DIR}).` : 'Nu copia nimic.'}
Returnează "ok".`, { label: `grefier ${item.code} ${status}`, phase: phaseName, effort: 'low' })
      return { code: item.code, name: item.name, status, rounds: round, min, history }
    }
    const plan = await agent(managerPrompt(item, audits, round), { label: `ședință ${item.code} R${round}`, phase: phaseName, schema: PLAN_SCHEMA })
    if (!plan) return { code: item.code, name: item.name, status: 'EROARE_API', rounds: round, min, history }
    const rev = await agent(revisePrompt(item, plan, round), { label: `revizie ${item.code} R${round}`, phase: phaseName })
    if (rev === null) return { code: item.code, name: item.name, status: 'EROARE_API', rounds: round, min, history }
  }
}

async function writeThen(item, writerPrompt, phaseName) {
  const w = await agent(writerPrompt + `\n\nARHIVARE: după ce scrii, salvează o copie a versiunii inițiale a fișierelor tale în ${DOSAR(item.code)}\\R0_versiune_initiala\\ (fără nimic din ${AUDIT_DIR}).`, { label: `scrie ${item.code}`, phase: phaseName })
  if (w === null) return { code: item.code, name: item.name, status: 'EROARE_API', rounds: 0, min: null, history: [] }
  return gate(item, phaseName)
}

const allPass = (rs) => rs.length > 0 && rs.every(r => r && r.status === 'PASS')
const results = []
let stopReason = null

// ========== G0: canon v4 + studio v4 ==========
const G0_CANON = { code: 'G0-CANON-v4', role: 'Showrunner', name: 'Canonul-nucleu v4', files: [CANON], canCanon: true,
  brief: `Canonul v4 = sursa unică pentru toate echipele, construit în jurul celor 14 decizii blocate (${DECIZII}). Complet, precis istoric (1431–1476 strict; toate obiectivele și evenimentele din traseu cad în anii popasului — ex. Podul Suspinelor 1600–1603, Walk of Fame 1958–60, Opera din Viena 1869, Chrysler 1930), fără contradicții interne, operațional pentru personaje/lume/ploturi/artă/proză: pitch aspirațional; eroul (aspect pe epoci: doar mustață 1448–1476, moda de vârf a fiecărei epoci; fashion icon; ochelarii de soare ai zilei), viața de om; noaptea transformării (26/27 dec. 1476); regula nemuririi (schimbarea identității la mijlocul popasurilor lungi); traseul de 24 de popasuri cu, pentru fiecare: obiectiv celebru, clișeu Hollywood, MODA epocii, VEHICULUL-semnătură (cal/caleașcă/tren/mașină/avion/iaht), luxul (cazinou, bal, Riviera…), IUBIREA epocii după 1794, succesul/afacerea familiei în acel oraș; puteri + limite care permit ACȚIUNE ZIUA (Inelul Zorilor, cele 7 inele, fără umbră în plin soare); Codul; familia (Sânziana înstrăinată din 1794 — nu soție în prezent; Ilinca = „Q”; Iosif = Alfred; Mihnea; Buna Dochia); aliații (Ioana — tensiune lentă, fără romantism S1); antagoniștii (Radu cel Frumos — mort istoric în Țara Românească, ian. 1475; Armistițiul fraților la 50 de ani din 1526; Omul Fără Umbră — doar profil public, identitatea în documentul confidențial); locuri; structura sezonului (titlul „DRACULA — Sângele Dragonului”; episod = 24 pagini BD + până la 8 pagini de backmatter; cold open tip Bond; femeia episodului; set-piece de zi; povestirea separată) ; identitatea vizuală (titlul DRACULA fără „Contele Nopții”); drepturi (fără Lugosi/Universal/mărci Bond/auto/modă pe coperți și produse); registrul deciziilor de canon și istoricul versiunilor (v1→v4). KPI Showrunner: 0 contradicții.` }
const G0_STUDIO = { code: 'G0-STUDIO-v4', role: 'Showrunner', name: 'Organizarea studioului v4 (echipa, mod de gândire, sarcini, raportare, roadmap per membru, Poarta 9,50, arhivare)', files: [STUDIO, JURNAL], canCanon: true,
  brief: `Cerințele Producătorului: echipa și modul de gândire, sarcini, raportare de progres, roadmap cu obiective/activități/rezultate MĂSURABILE pentru FIECARE membru (inclusiv auditorii, managerii, grefierul); „toți pașii auditați; fiecare agent are auditori; minim 9,50 de la cei mai severi; sub prag ședință + manager cu sarcini clare; nimic nu trece fără punctaj de excepție”; „totul salvat, arhivat — rapoarte de audit / planuri de măsuri / rezultate”. Documentul trebuie aliniat la cele 14 decizii (titlul DRACULA, stil Bond, fashion, zi, aspirațional, research extins): fișe de post cu KPI numerici și căi de livrabile, roadmap datat (Etapa I sprint, II pre-producție vizuală până la 30.11.2026, III lansare de la 01.12.2026, figurine 31.03.2027), sistemul de raportare cu șablon, sistemul Poarta 9,50, sistemul de arhivare (${AUDIT_DIR}\\<COD>\\ cu R0_versiune_initiala, R<n>_audit_canon|craft|kpi.md, R<n>_plan_masuri.md + Execuție, R<n>_versiune_inainte_de_revizie, REZULTAT_FINAL.md, VERSIUNE_APROBATA; registrul 00_REGISTRU_AUDIT.md), principiul independenței auditului (Producătorul contrasemnează planurile pentru livrabilele Showrunnerului — marcat „în așteptarea contrasemnării” până atunci). Jurnalul de progres coerent cu starea reală (inclusiv oprirea G0 v3 și motivele).` }

if (run('G0')) {
  phase('G0 Canon & Studio v4')
  const r = await parallel([
    () => writeThen(G0_CANON, `Ești Showrunnerul delegat (Director de Creație) al DRACULA COMICS STUDIO. Transformi canonul actual v3.1 (${CANON}, ~13.000 de cuvinte, deja revizuit prin audit) în **canonul v4**.
Citește INTEGRAL: registrul deciziilor Producătorului ${DECIZII} (14 decizii BLOCATE — mai ales 9–14, noi), jurnalul ${JURNAL} (secțiunea „DECIZII SHOWRUNNER asupra propunerilor A/B/C” — aplică tot ce e aprobat acolo), rapoartele auditului anterior al canonului: ${DOSAR('G0-CANON')}\\R2_audit_canon.md, R2_audit_craft.md, R2_audit_kpi.md (închide TOATE defectele semnalate care rămân valabile), propunerile echipelor din ${P('00_STUDIO/rapoarte')} (A_research.md — inclusiv R24 „Armistițiul fraților” la 50 de ani din 1526 = APROBAT și R32 corectura despre pamfletele tipărite 1488–1500 vs poemul lui Beheim 1463 = APROBAT; B_personaje.md; C_lume.md), plus ${P('02_RESEARCH/05_MODURI_DE_PREZENTARE.md')} (formula de prezentare — adoptă ce se potrivește).
${LOCKED}
Rescrie ${CANON} ca v4 (păstrează numerotarea §1–§13 stabilă, secțiunile noi la final): ${G0_CANON.brief}
La final numără cuvintele și verifică automat (Python) că nu mai apar „Contele Nopții”, „Valerian”, „Drakon”, „soția lui” în prezent. Actualizează raportul ${P('00_STUDIO/rapoarte/S_showrunner.md')}. Returnează rezumat ≤10 rânduri.`, 'G0 Canon & Studio v4'),
    () => writeThen(G0_STUDIO, `Ești Showrunnerul delegat al DRACULA COMICS STUDIO. Aduci documentul de organizare ${STUDIO} și jurnalul ${JURNAL} la versiunea v4. Atenție: o revizie anterioară a documentului a fost întreruptă la jumătate (vezi ${DOSAR('G0-STUDIO')}\\R1_plan_masuri.md și R1_audit_*.md — închide toate defectele valabile). Citește registrul ${DECIZII} (14 decizii blocate) și jurnalul.
${LOCKED}
Cerințe: ${G0_STUDIO.brief}
Nu crea documente contradictorii; dacă există 00_STUDIO/02_BRIEFURI, aliniază-le și pe ele. Returnează rezumat ≤10 rânduri.`, 'G0 Canon & Studio v4'),
  ])
  results.push(...r.filter(Boolean))
  if (!allPass(r)) stopReason = 'G0 nu a trecut integral Poarta 9,50'
}

// ========== G1: aliniere + fundație ==========
const G1 = [
  { code: 'A-RESEARCH-v4', role: 'A. Analist de narațiune și surse de inspirație', name: 'Research complet (polițist + surse extinse + moduri de prezentare + Bond/aspirațional)', files: [P('02_RESEARCH'), P('00_STUDIO/rapoarte/A_research.md')], snap: [P('02_RESEARCH'), P('00_STUDIO/rapoarte/A_research.md')],
    brief: `Toate fișierele din 02_RESEARCH (exclusiv subfolderul _lucru_research_extins = notițe brute): ≥25 seriale + ≥20 filme polițiste; ≥60 opere din afara genului (≥15 romane, ≥15 filme/francize, ≥10 seriale, ≥10 BD/manga/jocuri); ≥50 mecanisme; ≥30 moduri de prezentare + formula de prezentare a seriei; ≥10 recomandări; ≥45 semințe de plot cu popas de flashback din canon v4. NOU (decizii 9–14): secțiune „Formula Bond” (ce face francizele Bond să funcționeze de 60 de ani: cold open, locații de lux, vehicule, femeia Bond modernă, gadgeturi, stil, antagoniști) + „Cititorul tânăr de azi” (profil demografic și de consum al cititorilor de BD/manga/webtoon 2024–2026 cu surse, ce aspirații îi mișcă — succes, bani, libertate, lux, călătorii — și cum le servim responsabil: succes prin merit) + semințe noi cu acțiune de zi, glamour și femeia episodului. Totul coerent cu canonul v4 (titlul DRACULA, Sânziana înstrăinată).`,
    align: `Ești Analistul-șef A. Aliniază research-ul la canonul v4 (${CANON}) și la deciziile 9–14 (${DECIZII}). Citește tot 02_RESEARCH. Criticul de completitudine al rulării anterioare a căzut (eroare API): fă TU verificarea de completitudine (numără KPI-urile cu Python; adaugă opere majore lipsă, inclusiv literatură română/est-europeană și anime). Adaugă secțiunile noi cerute în brief. Elimină/actualizează orice referință la „Contele Nopții” sau la Sânziana-soție. Actualizează raportul ${P('00_STUDIO/rapoarte/A_research.md')}.` },
  { code: 'B-PERSONAJE-v4', role: 'B. Arhitect personaje', name: 'Biblia personajelor + femeile epocilor + figurine (v4)', files: [P('03_PERSONAJE'), P('00_STUDIO/rapoarte/B_personaje.md')], snap: [P('03_PERSONAJE'), P('00_STUDIO/rapoarte/B_personaje.md')],
    brief: `Toate fișierele din 03_PERSONAJE aliniate la canonul v4: 01_VLAD_DRACULEA.md (≥15 momente istorice reale 1431–1476; paragraf pentru FIECARE din cele 24 de popasuri cu moda epocii/ținuta-semnătură, vehiculul, luxul, iubirea epocii după 1794, succesul/afacerea; psihologie; Metoda Ostaticului; voce; ce nu face niciodată; FASHION ICON pe epoci; cum trăiește ZIUA; parcursul de „self-made” al imperiului — lecții de succes prin merit); 02_FAMILIA_DRACULESTI.md (Sânziana înstrăinată din 1794, NU soție în prezent; Ilinca = Q; Iosif = Alfred/Moneypenny; Mihnea; Buna Dochia; Brutus); 03_ALIATI.md (Ioana — tensiune lentă, fără romantism S1); 04_ANTAGONISTI.md (Radu, Casa Strigoi, Ordinul Cenușii, Omul Fără Umbră — profil public, răufăcători ai săptămânii în stil Bond: magnați, colecționari, femei fatale); 05_FIGURINE_ACTIUNE.md (≥5 figurine incl. ținute fashion-icon și un vehicul/accesoriu de colecție); NOU 06_FEMEILE_EPOCILOR_SI_ALE_EPISOADELOR.md: ≥12 femei „la superlativ” (iubirile epocilor după 1794 + femei recurente ale prezentului: aliate, rivale, femei fatale) — fiecare puternică, cu agenda proprie, niciodată decor, 14+. ≥12 personaje cu dorință/frică/secret/contradicție/voce (3 replici)/aspect precis.`,
    align: `Ești Arhitectul de personaje B. Aliniază biblia personajelor la canonul v4 (${CANON}) și la deciziile 9–14 (${DECIZII}): Sânziana nu mai e soție în prezent (înstrăinare din 1794), Vlad burlac glamour, fashion icon pe epoci, stil Bond (vehicule, lux), acțiune ziua, aspirațional (succes prin merit), Ilinca = Q. Creează 06_FEMEILE_EPOCILOR_SI_ALE_EPISOADELOR.md. Actualizează raportul ${P('00_STUDIO/rapoarte/B_personaje.md')}.` },
  { code: 'C-LUME-v4', role: 'C. Arhitect lume & istoric', name: 'Worldbuilding v4 (cronologie, regulile zilei și nopții, facțiuni, locuri, traseu, imperiu, mister)', files: [P('04_LUME'), P('00_STUDIO/rapoarte/C_lume.md')], snap: [P('04_LUME'), P('00_STUDIO/rapoarte/C_lume.md')],
    brief: `Toate fișierele din 04_LUME aliniate la canonul v4: 01_CRONOLOGIE_SECOLE.md (≥40 intrări, ≥20 istorice verificate); 02_REGULILE_NOPTII.md → regulile ZILEI și NOPȚII (ce poate Vlad în plină zi cu Inelul, spectaculos; limitele; FAQ; clișee Hollywood vs adevăr); 03_FACTIUNI.md (≥3); 04_LOCURI.md (≥15 locuri descrise vizual, incl. locații de lux: cazinouri, hoteluri, Riviera, Alpi); 05_MISTERUL_OMULUI_FARA_UMBRA.md (confidențial; aliniat la Sânziana 1794); 06_TRASEUL_CAPITALELOR.md (24 de popasuri cu toate câmpurile + MODA epocii, VEHICULUL-semnătură, LUXUL, IUBIREA epocii după 1794, AFACEREA/succesul familiei; toate obiectivele cad în anii popasului); NOU 07_IMPERIUL_DRACULESTILOR.md: success story-ul familiei pe 550 de ani (cum s-a construit averea prin merit: comerț, bănci, artă, investiții pe termen lung, dobânda compusă a secolelor; companiile de azi; Fundația Sânziana; garajul, hangarul și grajdurile familiei — vehicule pe epoci descrise generic, fără mărci). Exactitate istorică strictă.`,
    align: `Ești Arhitectul lumii C. Aliniază worldbuilding-ul la canonul v4 (${CANON}) și la deciziile 9–14 (${DECIZII}): acțiune ziua (regulile Inelului), fashion/vehicule/lux/iubiri pe popasuri, Sânziana înstrăinată din 1794, imperiul familiei (07_IMPERIUL_DRACULESTILOR.md nou), titlul DRACULA. Corectează orice anacronism. Actualizează raportul ${P('00_STUDIO/rapoarte/C_lume.md')}.` },
  { code: 'E-ARTA-v4', role: 'E. Director artistic', name: 'Identitate vizuală v4: sigle DRACULA, paletă, schițe (fashion icon, vehicule, femei), layout-uri, coperți, ghid, prompturi', files: [P('05_ART'), P('00_STUDIO/rapoarte/E_arta.md')], snap: [P('05_ART'), P('00_STUDIO/rapoarte/E_arta.md')],
    brief: `05_ART complet la v4: ≥3 variante de siglă SVG cu titlul „DRACULA” (FĂRĂ „Contele Nopții”) + lock-up cu subtitlul S1 „Sângele Dragonului” (emblemă dragon în jurul lui D cu ecou Ordinul Dragonului, logotip, monogramă/favicon); paleta + palete pe epoci/orașe; ≥8 schițe SVG: Vlad turnaround (fashion icon 2026, ochelari de soare de zi), Vlad pe epoci (moda de vârf a fiecărei epoci — planșă de costume pentru ≥8 popasuri, doar mustață 1448–1476), transformări, familia (Sânziana ca figură separată/înstrăinată), Radu, Ioana, silueta Omului Fără Umbră, NOU planșa de vehicule-semnătură pe epoci (cal, caleașcă, tren de lux, automobil anii ’20, grand tourer anii ’60, hypercar 2026, biplan, avion privat, iaht — design generic, fără mărci), NOU planșa „femeile epocilor” (siluete elegante); ≥4 șabloane de pagină + 3 machete de copertă (cel puțin una în plină zi, stil afiș de film Bond, cu titlul DRACULA); 00_GHID_STIL_VIZUAL.md (fashion icon, glamour, zi/noapte, vehicule, lettering); 01_PROMPTURI_ILUSTRATIE.md (≥20 prompturi EN cu ancoră consecventă, scene de zi, glamour; fără nume de mărci/actori). SVG-uri valide XML, calitate profesională. Auditorii deschid/randează SVG-urile (cairosvg/Pillow sau browser) și inspectează vizual.`,
    align: `Ești Directorul artistic E. Lucrul tău anterior a fost întrerupt de o eroare API (planșa lui Radu era în lucru). Inventariază 05_ART, termină ce lipsește și aliniază totul la canonul v4 (${CANON}), la ghidul personajelor ${P('03_PERSONAJE')} și la deciziile 9–14 (${DECIZII}): titlul DRACULA (elimină „Contele Nopții” din toate siglele, coperțile și textele), fashion icon, stil Bond (planșa de vehicule), scene de zi, Sânziana înstrăinată, femeile epocilor. Validează fiecare SVG ca XML (Python) și, dacă poți, randează-le în PNG de previzualizare în 05_ART/_preview/. Scrie/actualizează raportul ${P('00_STUDIO/rapoarte/E_arta.md')}.` },
]

if (!stopReason && run('G1')) {
  phase('G1 Aliniere & Fundație')
  const r = await pipeline(G1, it => writeThen(it, `${it.align}
${LOCKED}
Cerințele complete pe care le va verifica auditul: ${it.brief}
Returnează rezumat ≤10 rânduri.`, 'G1 Aliniere & Fundație'))
  results.push(...r.filter(Boolean))
  if (!allPass(r)) stopReason = 'G1 nu a trecut integral Poarta 9,50'
}

// ========== G2: arc ==========
const ARC = P('06_EPISOADE/00_ARC_SEZON_1.md')
const ARC_ITEM = { code: 'D1-ARC', role: 'D1. Plot Architect', name: 'Arcul Sezonului 1 „DRACULA — Sângele Dragonului” + harta celor 20 de episoade', files: [ARC, P('00_STUDIO/rapoarte/D1_plot.md')], snap: [ARC],
  brief: `Arcul Sezonului 1: tema, arcurile lui Vlad, Ioanei, familiei (Sânziana înstrăinată), lui Radu (Armistițiul fraților), Omului Fără Umbră; HARTA celor 20 de episoade (tabel): nr., titlu RO + EN, logline, cazul modern (oraș românesc/european/mondial de lux), popasul de flashback (≥15 popasuri DIFERITE; pivoturile: Ep1 mormântul gol Snagov, Ep5 prima siluetă neagră, Ep10 Ioana află adevărul, Ep15 Radu reapare, Ep20 cliffhanger), COLD OPEN-ul Bond (zi sau noapte), set-piece-ul de ZI, femeia episodului, vehiculul/locația de lux, momentul fashion, mecanismele (coduri M..), indiciul plantat + episodul plății, modul de prezentare folosit (coduri PR..). Plan de indicii setup→payoff pe tot sezonul. Varietate de tipuri de caz. Suspans maxim, glamour aspirațional (decizia 14), erou pozitiv care plătește un preț, 14+.` }

if (!stopReason && run('G2')) {
  phase('G2 Arc sezon')
  const r = await writeThen(ARC_ITEM, `Ești D1 „Plot Architect”, șeful Writers' Room. Mod de gândire: „Suspansul înseamnă informație dozată.” Citește integral: registrul ${DECIZII}, canonul ${CANON}, organizarea ${STUDIO}, tot 02_RESEARCH (${P('02_RESEARCH')}: bancă de mecanisme M.., moduri de prezentare PR.., semințe S.., formula Bond, cititorul tânăr), 03_PERSONAJE (inclusiv femeile epocilor), 04_LUME (traseul, imperiul, regulile zilei/nopții, misterul confidențial).
${LOCKED}
Scrie ${ARC}. ${ARC_ITEM.brief}
Scrie raportul ${P('00_STUDIO/rapoarte/D1_plot.md')}. Returnează rezumat ≤10 rânduri.`, 'G2 Arc sezon')
  results.push(r)
  if (!r || r.status !== 'PASS') stopReason = 'G2 (arcul) nu a trecut Poarta 9,50'
}

// ========== G3: episoade ==========
const pad = (n) => String(n).padStart(2, '0')
const epFile = (n) => P(`06_EPISOADE/EP${pad(n)}_PLOT.md`)
const storyFile = (n) => P(`07_POVESTIRI/EP${pad(n)}_POVESTIRE.md`)
const PROZATOR = (n) => ['D3', 'D4', 'D5', 'D6'][Math.floor((n - 1) / 5)]
const STYLE = `GHID DE VOCE (comun celor 4 prozatori): persoana a III-a focalizată pe Vlad (scurte secțiuni din perspectiva Ioanei sau a femeii episodului când servesc suspansul); timpul trecut literar românesc, dialog viu și actual; deschidere tip cold open Bond; simțurile lui Vlad concrete și precise; scena de „citire” a suspectului (Metoda Ostaticului) obligatorie; cel puțin o scenă de acțiune ZIUA; glamour aspirațional (ținute descrise cu ochi de fashion editor, vehicule, locuri de lux — fără mărci reale); femeia episodului puternică, cu agenda ei, seducție 14+ fără conținut explicit; flashback-ul marcat cu loc și an în italic (ex. *Londra, noiembrie 1888*), cu obiectivul celebru al orașului în prim-plan; umor fin, ironie aristocratică; Codul Dragonului respectat; clișeele Hollywood comentate ironic; succes prin merit; final cu cârlig. Română literară impecabilă, cu diacritice.`

const plotItem = (n) => ({ code: `D1-EP${pad(n)}`, role: 'D1. Plot Architect', name: `Plotul Episodului ${n}`, files: [epFile(n)],
  brief: `Plotul Episodului ${n}, conform hărții din ${ARC} (titlu, popas, pivot, plan de indicii). Structură obligatorie: titlu RO + EN; logline; COLD OPEN Bond; rezumat în 3 acte (caz modern 2026); set-piece de ZI; femeia episodului (cine e, agenda ei, dinamica cu Vlad, 14+); vehicul/locație de lux/moment fashion; flashback-ul (popasul, anul, obiectivul celebru, clișeul Hollywood jucat/răsturnat, moda și vehiculul epocii, cum oglindește tematic cazul); scena de deducție „Mentalist”/Metoda Ostaticului (ce observă, cum demonstrează); ≥3 mecanisme (coduri M.. cu aplicarea) + modul de prezentare (PR..) + 3 surse de inspirație declarate (fără copiere); limitele puterilor/Codul care îi îngreunează victoria; twist; piesa din arcul lung; indiciul plantat + plata; cliffhanger; distribuția; defalcarea pe 24 de pagini BD + ideea de backmatter; 3 idei de copertă (una de zi). Exactitate istorică. ~1.800–2.800 de cuvinte.` })
const storyItem = (n) => ({ code: `${PROZATOR(n)}-EP${pad(n)}`, role: `${PROZATOR(n)}. Prozator`, name: `Povestirea Episodului ${n}`, files: [storyFile(n)],
  brief: `Povestire în română, între 3.000 și 4.000 de cuvinte (KPI strict — numără), după plotul aprobat ${epFile(n)} (caz, cold open, set-piece de zi, femeia episodului, flashback, deducție, twist, cliffhanger). ${STYLE} Titlul = titlul episodului. Nivel de excepție literară: publicabilă ca atare.` })

if (!stopReason && run('G3')) {
  phase('G3 Episoade')
  const eps = (args && args.episodes) || Array.from({ length: 20 }, (_, i) => i + 1)
  const epResults = await pipeline(eps,
    n => writeThen(plotItem(n), `Ești D1 „Plot Architect”. Citește: ${DECIZII}, ${CANON}, arcul aprobat ${ARC} (respectă-l strict), ${P('02_RESEARCH')} (mecanisme, moduri de prezentare, formula Bond), ${P('03_PERSONAJE')}, ${P('04_LUME')} (popasul episodului în 06_TRASEUL_CAPITALELOR.md; regulile zilei/nopții; indiciile arcului lung din 05_MISTERUL...).
${LOCKED}
Scrie ${epFile(n)}. ${plotItem(n).brief}
Returnează rezumat ≤5 rânduri.`, 'G3 Episoade'),
    (plotRes, n) => {
      if (!plotRes || plotRes.status !== 'PASS') return { plot: plotRes, story: null }
      return writeThen(storyItem(n), `Ești prozatorul ${PROZATOR(n)}. Mod de gândire: „Aceeași poveste, alt instrument” — proza dă interioritate și simțurile lui Vlad din interior. Citește: ${DECIZII}, ${CANON}, plotul aprobat ${epFile(n)}, arcul ${ARC}, ${P('03_PERSONAJE')} (voci, replici, femeile epocilor), ${P('04_LUME')} (popasul flashback-ului, locurile), ${P('02_RESEARCH/05_MODURI_DE_PREZENTARE.md')} (structura povestirii).
${LOCKED}
Scrie ${storyFile(n)}: ${storyItem(n).brief}
Numără cuvintele (Python) și ajustează până intri în 3.000–4.000. Returnează titlul și numărul de cuvinte.`, 'G3 Episoade').then(s => ({ plot: plotRes, story: s }))
    })
  let ok = true
  for (const e of epResults) {
    if (!e) { ok = false; continue }
    if (e.plot) results.push(e.plot); if (e.story) results.push(e.story)
    if (!e.plot || e.plot.status !== 'PASS' || !e.story || e.story.status !== 'PASS') ok = false
  }
  if (!ok) stopReason = 'G3: nu toate ploturile/povestirile au trecut Poarta 9,50'
}

// ========== G4: scenariu ==========
const SCRIPT_ITEM = { code: 'D2-SCENARIU', role: 'D2. Scenarist BD', name: 'Scenariul BD complet Episodul 1 + șablonul de scenariu', files: [P('08_SCENARII/EP01_SCENARIU_BD.md'), P('08_SCENARII/00_SABLON_SCENARIU.md')],
  brief: `Full-script profesional (tip Image/Marvel) pentru Episodul 1, după plotul aprobat ${epFile(1)} și ghidul vizual ${P('05_ART/00_GHID_STIL_VIZUAL.md')}: 24 de pagini (cold open Bond în primele pagini, set-piece de zi, femeia episodului, flashback cu paletă de epocă), 4–6 panouri/pagină (splash și double-spread excepții); per panou: descriere vizuală pentru desenator (unghi, încadrare, lumină, paletă, ținute fashion, vehicule), baloane (≤25 cuvinte/balon), casete (flashback sepia cu margine aurie; casete senzoriale argintii), SFX; cele 12 „întoarceri de pagină” marcate; 1 splash; 1 double-spread; + schița backmatter-ului (≤8 pagini) + șablonul reutilizabil. Titlul DRACULA — Sângele Dragonului.` }
if (!stopReason && run('G4')) {
  phase('G4 Scenariu BD')
  const r = await writeThen(SCRIPT_ITEM, `Ești D2 „Scenarist BD”. „Gândesc în panouri, nu în paragrafe.” Citește: ${DECIZII}, ${CANON}, ${epFile(1)}, ${storyFile(1)}, ${ARC}, ${P('05_ART/00_GHID_STIL_VIZUAL.md')}, ${P('03_PERSONAJE')}, ${P('04_LUME/04_LOCURI.md')}, ${P('02_RESEARCH/05_MODURI_DE_PREZENTARE.md')}.
${LOCKED}
Scrie ${SCRIPT_ITEM.files.join(' și ')}. ${SCRIPT_ITEM.brief}
Scrie raportul ${P('00_STUDIO/rapoarte/D2_scenariu.md')}. Returnează rezumat ≤5 rânduri.`, 'G4 Scenariu BD')
  results.push(r)
  if (!r || r.status !== 'PASS') stopReason = 'G4 (scenariul) nu a trecut Poarta 9,50'
}

// ========== G5: QA + site ==========
if (!stopReason && run('G5')) {
  phase('G5 QA & Site')
  const qaItem = { code: 'F2-QA', role: 'F2. Editor de continuitate', name: 'Raportul de continuitate + corecturile aplicate pe tot proiectul', files: [P('00_STUDIO/04_RAPORT_CONTINUITATE.md'), ROOT], snap: [P('00_STUDIO/04_RAPORT_CONTINUITATE.md')],
    brief: `Verificare 100% a episoadelor, povestirilor, scenariului, personajelor, lumii, artei față de registrul deciziilor și canonul v4: nume, date, vârste, puteri (zi/noapte), reguli, cine știe ce și când (Ioana află în Ep10), traseul capitalelor, Sânziana înstrăinată, titlul DRACULA, planul de indicii setup→payoff (fiecare indiciu plătit, fiecare plată plantată), femeile episoadelor necontradictorii. Raportul listează fiecare eroare (locație, gravitate, corectură) ȘI confirmă corectarea în fișiere. La final: 0 erori critice/majore. (Nu audita arhiva ${AUDIT_DIR}.)` }
  const qa = await writeThen(qaItem, `Ești F2 „Editor de continuitate”. „Cititorul fan va observa. Eu observ primul.” Citește TOT proiectul din ${ROOT} (fără arhiva ${AUDIT_DIR}).
${LOCKED}
Găsește toate erorile de continuitate și CORECTEAZĂ-LE în fișiere (canonul nu îl schimbi; propunerile în raport). Scrie ${P('00_STUDIO/04_RAPORT_CONTINUITATE.md')}: ${qaItem.brief} Scrie ${P('00_STUDIO/rapoarte/F2_qa.md')}. Returnează rezumat ≤8 rânduri.`, 'G5 QA & Site')
  results.push(qa)
  if (qa && qa.status === 'PASS') {
    const siteItem = { code: 'F1-SITE', role: 'F1. Web Studio', name: 'Site-ul local unitar al proiectului', files: [P('09_SITE/build_site.py'), P('09_SITE/index.html'), P('09_SITE/RECONSTRUIESTE_SITE.bat')],
      brief: `Site local HTML (un singur index.html, dublu-clic, offline + Google Fonts) generat de build_site.py din toate folderele. Titlul DRACULA (S1: Sângele Dragonului), fără „Contele Nopții”. Secțiuni: Acasă (pitch + statistici), Deciziile Producătorului, Studio & Roadmap, Progres (rapoarte + jurnal), AUDIT (registrul central + dosarul fiecărui livrabil: rapoartele celor 3 auditori pe runde, planurile de măsuri cu execuția, rezultatul final, graficul evoluției notelor, tabloul „Poarta 9,50”), Canon, Personaje (incl. femeile epocilor), Lume (incl. imperiul), Traseul secolelor (timeline + hartă SVG a popasurilor cu moda și vehiculul fiecărei epoci), Artă (galerie SVG cu lightbox), Episoade (20 de carduri cu titlu + logline + link la povestire/scenariu), Povestiri (cititor cu nr. cuvinte + indicator KPI), Scenarii, Research; secțiune confidențială ascunsă pentru misterul antagonistului; căutare full-text; responsive (16px gutter pe telefon, fără scroll orizontal); design premium glamour-gotic cu paleta canon și sigla din 05_ART/logo. 100% din fișierele .md/.svg ale proiectului prezente (copiile de versiuni din arhivă doar listate cu link). Build <10s, UTF-8. Auditorii rulează build-ul și deschid index.html în browser (mcp__Claude_Browser__preview_start cu url file:///...), verifică desktop + mobil.` }
    const site = await writeThen(siteItem, `Ești F1 „Web Studio”. Lucrul anterior la site a fost întrerupt de o eroare API: inventariază ${P('09_SITE')} și actualizează build_site.py ca să îndeplinească: ${siteItem.brief} Rulează build-ul, verifică în browser, scrie raportul ${P('00_STUDIO/rapoarte/F1_web.md')}. Returnează rezumat ≤8 rânduri.`, 'G5 QA & Site')
    results.push(site)
    if (!site || site.status !== 'PASS') stopReason = 'G5 (site) nu a trecut Poarta 9,50'
  } else stopReason = 'G5 (QA) nu a trecut Poarta 9,50'
}

if (stopReason) log(`⛔ OPRIT: ${stopReason}. Nimic nu trece mai departe fără 9,50.`)

phase('Registru')
await agent(`Ești grefierul-șef de audit al DRACULA COMICS STUDIO. Actualizează REGISTRUL CENTRAL ${AUDIT_DIR}\\00_REGISTRU_AUDIT.md (română): păstrează intrările anterioare (inclusiv G0-CANON și G0-STUDIO v3, oprite de Showrunner după deciziile 9–14) și adaugă/actualizează. Conținut: sistemul „Poarta 9,50” și structura arhivei; TABELUL MASTER (cod, livrabil, poartă, runde, note finale per auditor, nota minimă, status ✅/🔴/⚠️ EROARE_API, dată, link la dosar și REZULTAT_FINAL.md); statistici (runde, defecte, media notelor finale); deciziile necesare de la Producător; motivul opririi (dacă e cazul): ${stopReason || 'niciunul'}. Sursa: toate dosarele din ${AUDIT_DIR} + rezultatele acestei rulări: ${JSON.stringify(results.map(r => r && ({ code: r.code, name: r.name, status: r.status, rounds: r.rounds, min: r.min, history: r.history })))} (data ${DATE}).
Apoi actualizează ${JURNAL}: tabelul de faze (starea reală) + o intrare datată cu rezultatele. Returnează "ok".`, { label: 'registru central audit', phase: 'Registru', effort: 'low' })

return { stopReason, results: results.filter(Boolean).map(r => ({ code: r.code, status: r.status, rounds: r.rounds, min: r.min })) }
