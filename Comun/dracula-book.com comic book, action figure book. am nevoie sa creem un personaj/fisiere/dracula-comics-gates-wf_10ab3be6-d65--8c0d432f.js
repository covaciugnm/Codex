export const meta = {
  name: 'dracula-comics-gates',
  description: 'DRACULA COMICS: audit „Poarta 9,50” cu arhivare completă (rapoarte auditori, planuri de măsuri, snapshot-uri, rezultate, registru)',
  whenToUse: 'Rulează porțile de audit ale proiectului DRACULA COMICS; args.gates = listă de porți (G0..G5), args.date = data',
  phases: [
    { title: 'G0 Canon & Studio', detail: 'audit canon + organizare' },
    { title: 'G1 Fundație', detail: 'research, personaje, lume, artă' },
    { title: 'G2 Arc sezon', detail: 'arcul Sezonului 1 + harta celor 20 de episoade' },
    { title: 'G3-4 Episoade', detail: 'plot → audit → povestire → audit, per episod' },
    { title: 'G4 Scenariu BD', detail: 'scenariul EP01 + șablon' },
    { title: 'G5 QA & Site', detail: 'continuitate + site local' },
    { title: 'Registru', detail: 'registrul central de audit + jurnal' },
  ],
}

const ROOT = String.raw`D:\00. Downloads\Dracula Book\DRACULA-COMICS`
const P = (rel) => ROOT + '\\' + rel.replace(/\//g, '\\')
const CANON = P('01_CANON/00_CANON_NUCLEU.md')
const STUDIO = P('00_STUDIO/01_ECHIPA_SI_ROADMAP.md')
const AUDIT_DIR = P('00_STUDIO/audit')
const DOSAR = (code) => P(`00_STUDIO/audit/${code}`)
const PASS = 9.5
const MAX_ROUNDS = 6
const gates = (args && args.gates) || ['G0']
const DATE = (args && args.date) || '24.09.2026'
const EXTRA = (args && args.extra) || {}

const LOCKED = `DECIZII BLOCATE ALE PRODUCĂTORULUI (nu se pot modifica, doar îmbunătăți în jurul lor):
1) Eroul este VLAD al III-lea Drăculea însuși (n. 1431 Sighișoara) — nu alt personaj.
2) Viața de om 1431–1476 respectă STRICT istoria reală (locuri, ani, evenimente).
3) BD-ul are continuitate proprie, DIFERITĂ de romanele editurii (nu preia personaje/evenimente din seria NOIR etc.).
4) După 1476 trăiește ca nemuritor prin capitale europene și mondiale, schimbând identitatea ca să nu se vadă că nu îmbătrânește; traseul se leagă de obiective universal cunoscute și de clișee Hollywood.
5) Personaj pozitiv, supererou: frumos, atletic, super-inteligent, sofisticat, simțuri supradezvoltate (tip The Mentalist), zboară, se transformă; familie de conți transilvăneni foarte bogați și puternici; inspirație Saga + supereroi pozitivi.
6) Totul în limba română cu diacritice corecte (ă â î ș ț), cu excepția prompturilor de ilustrație (EN).
7) Tot procesul de audit se ARHIVEAZĂ (rapoarte, planuri de măsuri, versiuni, rezultate) în ${AUDIT_DIR}.`

const LENSES = [
  { key: 'canon', name: 'Auditor de Canon & Istorie', focus: `coerența totală cu canonul (${CANON}) și deciziile blocate; EXACTITATEA ISTORICĂ (verifică datele, locurile, personajele reale — folosește WebSearch prin ToolSearch "select:WebSearch" când ai orice dubiu; o singură dată istorică greșită prezentată ca fapt = defect major); continuitate internă (nume, vârste, ani, reguli ale puterilor, cine știe ce și când); contradicții între fișiere.` },
  { key: 'craft', name: 'Auditor de Meșteșug & Piață', focus: `calitate profesională la nivelul celor mai buni din industrie (Image/Marvel/DC, Brian K. Vaughan – Saga, Bruno Heller – The Mentalist, serialele polițiste de top): suspans, ritm, originalitate (fără copiere de IP-uri), profunzime emoțională, eroul pozitiv care plătește un preț, stil și limbă română literară impecabilă, potențial comercial (cititorul vrea episodul următor?), utilitate reală pentru echipa care va folosi livrabilul; riscuri juridice (drepturi de imagine, mărci, IP protejat).` },
  { key: 'kpi', name: 'Auditor de KPI & Completitudine', focus: `verificare punct cu punct a KPI-urilor și cerințelor din brief (numără efectiv: elemente, cuvinte — folosește Python/wc prin Bash —, pagini, secțiuni); lipsuri, fișiere lipsă, secțiuni goale sau superficiale, placeholder-e, format, diacritice, fișierul de raport al echipei completat conform șablonului din ${STUDIO} §5.` },
]

const AUDIT_SCHEMA = {
  type: 'object',
  properties: {
    score: { type: 'number', description: 'Nota 0.00–10.00 cu două zecimale' },
    verdict: { type: 'string', enum: ['PASS', 'FAIL'] },
    strengths: { type: 'array', items: { type: 'string' } },
    defects: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          severity: { type: 'string', enum: ['critic', 'major', 'minor'] },
          location: { type: 'string' },
          problem: { type: 'string' },
          fix: { type: 'string' },
        },
        required: ['severity', 'location', 'problem', 'fix'],
      },
    },
    summary: { type: 'string' },
    report_path: { type: 'string', description: 'calea raportului de audit salvat' },
  },
  required: ['score', 'verdict', 'defects', 'summary', 'report_path'],
}

const PLAN_SCHEMA = {
  type: 'object',
  properties: {
    root_causes: { type: 'array', items: { type: 'string' } },
    tasks: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          task: { type: 'string' },
          acceptance: { type: 'string', description: 'criteriu verificabil de acceptare' },
          owner: { type: 'string' },
        },
        required: ['id', 'task', 'acceptance'],
      },
    },
    record_path: { type: 'string' },
  },
  required: ['root_causes', 'tasks', 'record_path'],
}

function auditPrompt(item, lens, round) {
  const rp = `${DOSAR(item.code)}\\R${round}_audit_${lens.key}.md`
  return `Ești ${lens.name} în completul de audit al DRACULA COMICS STUDIO (editura Dracula Book). Ești unul dintre cei mai severi auditori din industrie. Proiect: serie BD color + povestiri „DRACULA — Contele Nopții”.

LIVRABIL AUDITAT: [${item.code}] ${item.name} — runda ${round} — data ${DATE}.
FIȘIERE DE CITIT INTEGRAL (nu eșantionat; dacă e un folder, citește toate fișierele din el, recursiv):
${item.files.map(f => '- ' + f).join('\n')}
REFERINȚE: canonul ${CANON} (sursă unică de adevăr) și organizarea ${STUDIO} (fișa de post + KPI-urile rolului ${item.role}).
${LOCKED}

BRIEF / CERINȚE ALE LIVRABILULUI:
${item.brief}

LENTILA TA: ${lens.focus}

REGULI DE NOTARE (fii necruțător, dar corect):
- 9.50–10.00 = excepțional, l-ai semna pentru publicare la o editură de top FĂRĂ modificări substanțiale. Doar defecte minore cosmetice.
- Orice defect MAJOR plafonează nota la 9.20. Orice defect CRITIC plafonează la 8.50. Mai multe defecte minore acumulate scad nota.
- Nu da notă mare din politețe; nu penaliza gusturi personale fără argument. Fiecare defect: locație exactă (fișier + secțiune/rând), problema, corectura concretă.

ARHIVARE OBLIGATORIE: salvează RAPORTUL TĂU COMPLET DE AUDIT în ${rp} (creează folderul dacă lipsește; markdown, română) cu: antet (livrabil, cod, rundă, auditor/lentilă, data ${DATE}, fișiere verificate), NOTA și VERDICTUL (PASS dacă ≥ ${PASS}), metoda de verificare (ce ai citit, ce ai numărat, ce ai căutat pe web și sursele), punctele forte, tabelul defectelor (nr., gravitate, locație, problemă, corectură), concluzia. Acesta e SINGURUL fișier pe care ai voie să-l creezi/modifici.
Returnează evaluarea structurată (score, verdict, strengths, defects, summary în română, report_path = ${rp}).`
}

function managerPrompt(item, audits, round) {
  const rec = `${DOSAR(item.code)}\\R${round}_plan_masuri.md`
  return `Ești Managerul echipei ${item.role} (Showrunner delegat) la DRACULA COMICS STUDIO. Livrabilul [${item.code}] ${item.name} NU a trecut poarta de audit (minim ${PASS}/10 de la FIECARE auditor) în runda ${round}.

Convoci ședința echipei: citești cele 3 rapoarte de audit complete (${audits.map(a => a.report_path).join(' ; ')}) și rezumatul JSON de mai jos, identifici cauzele-rădăcină și emiți PLANUL DE MĂSURI: sarcini clare, numerotate (M${round}.1, M${round}.2 …), fiecare cu responsabil și criteriu verificabil de acceptare, astfel încât runda următoare să obțină ≥${PASS} de la toți. Acoperă TOATE defectele critice și majore și grupează minorele. Dacă auditorii se contrazic, arbitrează pe baza canonului ${CANON} și a deciziilor blocate (motivează arbitrajul). Poți adăuga îmbunătățiri proactive care ridică livrabilul la nivel de excepție.
${LOCKED}

FIȘIERELE LIVRABILULUI: ${item.files.join(' ; ')}

AUDITURILE (JSON):
${JSON.stringify(audits, null, 1)}

ARHIVARE OBLIGATORIE: scrie procesul-verbal al ședinței + planul de măsuri în ${rec} (markdown, română): antet (livrabil, rundă, data ${DATE}, participanți: autor ${item.role}, cei 3 auditori, manager), tabelul notelor celor 3 auditori + nota minimă + decizia „NU TRECE”, legături la cele 3 rapoarte de audit, sinteza defectelor, cauzele-rădăcină, arbitraje, PLANUL DE MĂSURI (tabel: cod, sarcină, responsabil, criteriu de acceptare, stare = „de executat”), și o secțiune goală „## Execuție” pe care o completează autorul. Nu modifica livrabilul. Returnează root_causes, tasks, record_path = ${rec}.`
}

function revisePrompt(item, plan, round) {
  const snap = `${DOSAR(item.code)}\\R${round}_versiune_inainte_de_revizie`
  const snapTargets = item.snap || item.files
  return `Ești autorul livrabilului [${item.code}] ${item.name} (rolul ${item.role}) la DRACULA COMICS STUDIO. Auditul rundei ${round} a dat sub ${PASS}/10. Managerul a stabilit planul de măsuri din ${plan.record_path} — execută-l INTEGRAL, direct în fișiere, la nivel de excepție (nu cosmetic).
${LOCKED}
Canon: ${CANON}. Organizare/KPI: ${STUDIO}.
FIȘIERELE LIVRABILULUI: ${item.files.join(' ; ')}
BRIEF ORIGINAL:
${item.brief}

PAS 1 — ARHIVARE ÎNAINTE DE MODIFICARE (obligatoriu): copiază versiunea actuală a fișierelor/folderelor ${snapTargets.join(' ; ')} în ${snap}\\ (păstrează numele fișierelor și structura subfolderelor; NU copia nimic din ${AUDIT_DIR}). Verifică copia.
PAS 2 — Execută sarcinile:
${JSON.stringify(plan.tasks, null, 1)}
Reguli: citește fișierele întâi; editează-le complet; păstrează diacriticele; nu șterge conținut bun, îmbunătățește-l; dacă o sarcină cere modificarea canonului și tu NU ești Showrunnerul, nu edita canonul — notează propunerea în raportul echipei (${P('00_STUDIO/rapoarte')}) la „Propuneri de modificare a canonului”.
PAS 3 — ARHIVARE DUPĂ: completează în ${plan.record_path} secțiunea „## Execuție”: pentru fiecare sarcină — stare (executat/parțial), ce s-a făcut concret, fișierele și secțiunile modificate; plus un rezumat al diferențelor față de ${snap}. Actualizează raportul echipei din 00_STUDIO/rapoarte/ (istoric revizii).
Returnează un rezumat de maximum 10 rânduri.`
}

async function gate(item, phaseName) {
  const history = []
  for (let round = 1; round <= MAX_ROUNDS; round++) {
    const audits = (await parallel(LENSES.map(lens => () =>
      agent(auditPrompt(item, lens, round), { label: `audit ${item.code} R${round} ${lens.key}`, phase: phaseName, schema: AUDIT_SCHEMA })
        .then(a => a ? { lens: lens.name, ...a } : null)
    ))).filter(Boolean)
    const scores = audits.map(a => a.score)
    const min = scores.length ? Math.min(...scores) : 0
    history.push({ round, scores: audits.map(a => ({ auditor: a.lens, score: a.score, report: a.report_path })), min })
    log(`[${item.code}] R${round}: ${audits.map(a => a.lens.split(' ').pop() + ' ' + a.score.toFixed(2)).join(' · ')} → min ${min.toFixed(2)}${min >= PASS && audits.length === 3 ? ' ✅ TRECE' : ' ❌'}`)
    const passed = audits.length === LENSES.length && min >= PASS
    if (passed || round === MAX_ROUNDS) {
      const status = passed ? 'PASS' : 'BLOCAT'
      await agent(`Ești grefierul de audit al DRACULA COMICS STUDIO. Arhivează REZULTATUL FINAL al porții pentru [${item.code}] ${item.name}.
1) Scrie ${DOSAR(item.code)}\\REZULTAT_FINAL.md (română, markdown): antet (livrabil, cod, rol ${item.role}, data ${DATE}), STATUS: ${status === 'PASS' ? '✅ TRECE POARTA 9,50' : '🔴 BLOCAT — necesită decizia Producătorului'}, runda finală ${round}, nota minimă finală ${min.toFixed(2)}; TABELUL ISTORIC al tuturor rundelor (rundă, nota fiecărui auditor, minimă, decizie, legătură la rapoarte și la planul de măsuri R<n>_plan_masuri.md unde există) din datele: ${JSON.stringify(history)}; punctele forte finale și defectele minore rămase (pentru finisare) din auditurile finale: ${JSON.stringify(audits.map(a => ({ auditor: a.lens, score: a.score, strengths: a.strengths, defects: a.defects })))}; ${status === 'BLOCAT' ? 'ce decizie trebuie să ia Producătorul și opțiunile.' : ''}
2) ${status === 'PASS' ? `Copiază versiunea APROBATĂ a fișierelor ${(item.snap || item.files).join(' ; ')} în ${DOSAR(item.code)}\\VERSIUNE_APROBATA\\ (fără nimic din ${AUDIT_DIR}).` : 'Nu copia nimic.'}
Returnează "ok".`, { label: `grefier ${item.code} ${status}`, phase: phaseName, effort: 'low' })
      return { code: item.code, name: item.name, status, rounds: round, min, history }
    }
    const plan = await agent(managerPrompt(item, audits, round), { label: `ședință ${item.code} R${round}`, phase: phaseName, schema: PLAN_SCHEMA })
    if (!plan) return { code: item.code, name: item.name, status: 'EROARE_MANAGER', rounds: round, min, history }
    await agent(revisePrompt(item, plan, round), { label: `revizie ${item.code} R${round}`, phase: phaseName })
  }
}

// ---------------- DEFINIȚII LIVRABILE ----------------
const G0_ITEMS = [
  { code: 'G0-CANON', role: 'Showrunner', name: 'Canonul-nucleu v3', files: [CANON],
    brief: `Documentul-sursă unic pentru toate echipele. Trebuie să fie complet, precis istoric, fără contradicții, suficient de detaliat încât personajele, lumea, ploturile, arta și proza să poată fi scrise coerent: pitch, erou (aspect, personalitate, alias), viața de om 1431–1476 strict istorică cu date verificate, regula nemuririi, traseul de 24 de popasuri (oraș, ani, alias, obiectiv celebru, clișeu Hollywood, nucleu de poveste — plauzibil istoric pentru anii dați: fiecare eveniment istoric menționat trebuie să cadă în intervalul popasului), puteri + limite + slăbiciuni, Codul, familia, aliații, antagoniștii, locurile, structura sezonului, identitatea vizuală. KPI Showrunner: 0 contradicții de canon.
INPUT DE LA ECHIPA A (research) de luat în calcul: propuneri — gradul în care „Privirea” funcționează pe Ioana; evoluția siluetei Omului Fără Umbră; „cadourile” prin care Radu se anunță înainte de Ep. 15; definirea „apelor curgătoare mari”; o dată fixă pentru transformarea din dec. 1476 (istoric: moartea între sfârșitul lui dec. 1476 și începutul lui ian. 1477). Risc juridic semnalat: chipul lui Bela Lugosi și designul filmului Dracula (1931, Universal) pot fi încă protejate (drept de imagine/mărci) — canonul trebuie să stabilească regula de folosire (ex.: fără chipul lui Lugosi/design Universal pe coperți până la verificare juridică). (Eroarea „Afacerea otrăvurilor” la popasul 6 a fost deja corectată în „Fronda 1648–1653”.) Autorul revizuirilor la canon este Showrunnerul delegat — poate edita canonul, dar NU deciziile blocate.` },
  { code: 'G0-STUDIO', role: 'Showrunner', name: 'Organizarea studioului: echipa, modul de gândire, sarcini, raportare, roadmap, sistem de audit și arhivare', files: [STUDIO, P('00_STUDIO/03_JURNAL_PROGRES.md')],
    brief: `Cerințele Producătorului: „descrie echipa și modul de gândire — sarcini — raportează progres — stabilește un roadmap cu obiective, activități și rezultate măsurabile pentru FIECARE membru al echipei” + „toți pașii trebuie auditați; fiecare agent are auditori; minimum 9,50/10 de la cei mai severi auditori; sub prag echipa se strânge, analizează, managerul stabilește sarcini clare de îmbunătățire; nimic nu trece fără punctaj de excepție” + „totul salvat, arhivat tot procesul pentru auditare — rapoarte de audit / planuri de măsuri / rezultate”. Documentul trebuie să reflecte canonul v3 (VLAD, nu Valerian/Drakon), să aibă pentru fiecare membru: mod de gândire, sarcini, livrabile cu căi, KPI numerici; roadmap cu obiective/activități/rezultate măsurabile PER MEMBRU și pe etape datate; sistemul de raportare cu șablon; sistemul de audit cu auditorii ca membri ai organigramei (fișe de post pentru auditori și grefier); SISTEMUL DE ARHIVARE: structura ${AUDIT_DIR}\\<COD>\\ (R<n>_audit_canon|craft|kpi.md, R<n>_plan_masuri.md cu secțiunea Execuție, R<n>_versiune_inainte_de_revizie\\, REZULTAT_FINAL.md, VERSIUNE_APROBATA\\) + registrul central ${AUDIT_DIR}\\00_REGISTRU_AUDIT.md. Jurnalul de progres coerent cu starea reală.` },
]

const G1_ITEMS = [
  { code: 'A-RESEARCH', role: 'A. Analist de narațiune și surse de inspirație', name: 'Research: seriale/filme polițiste + surse extinse (romane, scenarii, francize, seriale, BD/manga, jocuri) + moduri de prezentare + banca de mecanisme + recomandări',
    files: [P('02_RESEARCH'), P('00_STUDIO/rapoarte/A_research.md')],
    brief: `Principiul Producătorului: „ORICE scenariu sau roman de succes poate fi sursă de inspirație — nu doar serialele polițiste; lumea este ceea ce este, MODUL în care o prezentăm e important.” Cerințe: ≥25 seriale și ≥20 filme polițiste/suspans de top, cu rating și sursă; ≥60 de opere de succes din afara genului polițist (≥15 romane clasice și bestselleruri, ≥15 filme/scenarii/francize, ≥10 seriale de prestigiu, ≥10 BD/manga/jocuri narative) cu: de ce au succes, ce mecanism/arhetip transferăm, cum îl aplicăm la DRACULA (ex. arhetipul aristocratului bogat cu identitate secretă: Monte Cristo, Zorro, Pimpernelul Stacojiu, Batman, Lupin); ≥50 de mecanisme de plot (M01..) cu definiție, 2 exemple, aplicare cu puterile/limitele lui Vlad, risc de clișeu; 05_MODURI_DE_PREZENTARE.md cu ≥30 de moduri de prezentare (încadrare narativă, epistolar/documente găsite ca la Stoker, timeline dublu, narator nesigur, antologie, backmatter tip Watchmen, pagini de recapitulare, coperți variante, webtoon/vertical scroll etc.) aplicate concret la seria DRACULA (BD + povestiri + site), cu recomandarea „formulei de prezentare” a seriei; ≥10 recomandări + ≥45 semințe de plot (cu epoca de flashback dintr-un popas din canon §3/§5); secțiune despre clișeele vampirilor/nemuritorilor și cum le răsturnăm pozitiv. Canonul v3 (VLAD). Fără copiere de IP — doar mecanisme.` },
  { code: 'B-PERSONAJE', role: 'B. Arhitect personaje', name: 'Biblia personajelor + figurine de acțiune',
    files: [P('03_PERSONAJE'), P('00_STUDIO/rapoarte/B_personaje.md')],
    brief: `Toate fișierele din 03_PERSONAJE: 01_VLAD_DRACULEA.md (≥15 momente istorice reale 1431–1476 cu personaje reale + paragraf pentru FIECARE din cele 24 de popasuri ale traseului + psihologie, metoda de deducție tip Mentalist, voce, reguli „ce nu face niciodată”, costume pe epoci, fișa puterilor), 02_FAMILIA_DRACULESTI.md, 03_ALIATI.md, 04_ANTAGONISTI.md, 05_FIGURINE_ACTIUNE.md (≥5 figurine cu scară, articulații, accesorii, ambalaj, SKU). ≥12 personaje cu dorință/frică/secret/contradicție/voce (3 replici)/aspect precis. Fără urme de „Valerian/Drakon/Matei/Morvan/Radu Drakon” (canon vechi).` },
  { code: 'C-LUME', role: 'C. Arhitect lume & istoric', name: 'Worldbuilding: cronologie, regulile nopții, facțiuni, locuri, traseul capitalelor, misterul antagonistului',
    files: [P('04_LUME'), P('00_STUDIO/rapoarte/C_lume.md')],
    brief: `01_CRONOLOGIE_SECOLE.md (≥40 intrări, ≥20 ancorate în istorie reală verificată), 02_REGULILE_NOPTII.md (FAQ se poate/nu se poate + clișee Hollywood vs adevăr), 03_FACTIUNI.md (≥3), 04_LOCURI.md (≥15 locuri cu descriere vizuală pentru desenatori), 05_MISTERUL_OMULUI_FARA_UMBRA.md (3 ipoteze + indicii de plantat pe episoade + recomandare), 06_TRASEUL_CAPITALELOR.md (cele 24 de popasuri dezvoltate: date, alias, locuință, obiectiv celebru descris vizual, clișeu Hollywood cu filme de referință, 3–5 evenimente istorice reale, personaje reale întâlnite plauzibil, familia prezentă, cazul rezolvat = sămânță de flashback, motivul plecării/dispariției înscenate, suvenirul păstrat). Canon v3, fără urme de canon vechi (Drakonstein, Radu Drakon etc.). Exactitate istorică strictă.` },
  { code: 'E-ARTA', role: 'E. Director artistic', name: 'Identitate vizuală: sigle, paletă, schițe, layout-uri, ghid de stil, prompturi',
    files: [P('05_ART'), P('00_STUDIO/rapoarte/E_arta.md')],
    brief: `≥3 variante de siglă SVG (emblemă dragon încolăcit în jurul lui D cu ecou Ordinul Dragonului, logotip „DRACULA — Contele Nopții”, monogramă), paleta principală + palete pe epoci/orașe din traseu, ≥6 schițe SVG de personaj (Vlad turnaround, Vlad 1462, Vlad în formă de lup/lilieci, Sânziana, familia lineup, Radu cel Frumos, silueta Omului Fără Umbră, Conacul Făgăraș/Poenari), ≥4 șabloane de pagină BD SVG + 3 machete de copertă, ghid de stil vizual complet, ≥20 prompturi de ilustrație EN cu ancoră de personaj consecventă. SVG-uri valide XML, calitate profesională (nu desene copilărești), paleta canon. Auditorii trebuie să DESCHIDĂ SVG-urile (citește codul; dacă poți, randează în PNG cu Python cairosvg/Pillow sau prin browser și inspectează vizual). Fără urme de „DRAKON/Valerian”.` },
]

const ARC = P('06_EPISOADE/00_ARC_SEZON_1.md')
const ARC_ITEM = { code: 'D1-ARC', role: 'D1. Plot Architect', name: 'Arcul Sezonului 1 + harta celor 20 de episoade', files: [ARC, P('00_STUDIO/rapoarte/D1_plot.md')], snap: [ARC],
  brief: `Arcul Sezonului 1 „Sângele Dragonului”: tema, arcul lui Vlad, al Ioanei, al familiei, al lui Radu și al Omului Fără Umbră; HARTA celor 20 de episoade (tabel): nr., titlu RO (+ titlu EN), logline, cazul modern (oraș românesc/european), popasul de flashback (din canon §3/§5 — minimum 15 popasuri DIFERITE în sezon, toate pivoturile: Ep1 mormântul gol Snagov, Ep5 prima siluetă neagră, Ep10 Ioana află adevărul, Ep15 Radu reapare, Ep20 cliffhanger), cele 3 surse-mecanisme din banca de research (coduri M..), indiciul plantat și episodul plății. Plan de indicii (setup→payoff) pe tot sezonul. Varietate de tipuri de caz (cameră încuiată, răpire, fals de artă, crimă în serie, cold case, jaf, otrăvire, dispariție, șantaj etc.). Suspans maxim, originalitate, erou pozitiv care plătește un preț.` }

function epFile(n) { return P(`06_EPISOADE/EP${String(n).padStart(2, '0')}_PLOT.md`) }
function storyFile(n) { return P(`07_POVESTIRI/EP${String(n).padStart(2, '0')}_POVESTIRE.md`) }
const PROZATOR = (n) => ['D3', 'D4', 'D5', 'D6'][Math.floor((n - 1) / 5)]

const STYLE = `GHID DE VOCE PENTRU PROZĂ (comun celor 4 prozatori): narator la persoana a III-a, focalizat pe Vlad (cu scurte secțiuni din perspectiva Ioanei Mureșan când ajută suspansul); timpul trecut (perfect simplu/imperfect literar românesc, cu dialog vioi, actual); simțurile lui Vlad redate concret și precis (bătăi de inimă, mirosuri, sunete) — scena de „citire” a suspectului tip Mentalist obligatorie; flashback-ul marcat vizual cu titlu de loc și an în italic (ex. *Londra, noiembrie 1888*), cu obiectivul celebru al orașului în prim-plan; umor fin și ironie aristocratică; eroul pozitiv — Codul Dragonului e respectat; clișeele Hollywood pot fi comentate ironic; fără gore explicit (14+); final cu cârlig. Română literară impecabilă, cu diacritice.`

function plotItem(n) {
  return { code: `D1-EP${String(n).padStart(2, '0')}`, role: 'D1. Plot Architect', name: `Plotul Episodului ${n}`, files: [epFile(n)],
    brief: `Plotul Episodului ${n} conform hărții din ${ARC} (respectă titlul, popasul de flashback, pivotul și planul de indicii de acolo). Structura obligatorie: titlu RO + EN; logline; rezumat în 3 acte (caz modern 2026); flashback-ul (popasul, anul, obiectivul celebru, clișeul Hollywood jucat/răsturnat, cum oglindește tematic cazul); scena-cheie de deducție „Mentalist” a lui Vlad (ce observă, cum demonstrează); mecanismele de suspans folosite (≥3 coduri M.. din ${P('02_RESEARCH/02_BANCA_MECANISME_PLOT.md')} cu explicația aplicării) + cele 3 ploturi-sursă celebre combinate (declarate, fără copiere); limitele puterilor/Codul care îi îngreunează victoria; twist; piesa din arcul lung; indiciul plantat + unde se plătește; cliffhanger; distribuția episodului; defalcarea pe 24 de pagini BD (pagină → beat); 3 idei de copertă. Exactitate istorică pentru flashback. ~1.500–2.500 de cuvinte.` }
}
function storyItem(n) {
  return { code: `${PROZATOR(n)}-EP${String(n).padStart(2, '0')}`, role: `${PROZATOR(n)}. Prozator`, name: `Povestirea Episodului ${n}`, files: [storyFile(n)],
    brief: `Povestire scurtă în română, între 3.000 și 4.000 de cuvinte (KPI strict — numără), după plotul aprobat ${epFile(n)} (respectă-l: caz, flashback, deducție, twist, cliffhanger). ${STYLE} Titlul povestirii = titlul episodului. Nivel de excepție literară: să poată fi publicată ca atare.` }
}

const SCRIPT_ITEM = { code: 'D2-SCENARIU', role: 'D2. Scenarist BD', name: 'Scenariul BD complet Episodul 1 + șablonul de scenariu',
  files: [P('08_SCENARII/EP01_SCENARIU_BD.md'), P('08_SCENARII/00_SABLON_SCENARIU.md')],
  brief: `Scenariu BD profesional (format full-script tip Image/Marvel) pentru Episodul 1, după plotul aprobat ${epFile(1)} și ghidul vizual ${P('05_ART/00_GHID_STIL_VIZUAL.md')}: 24 de pagini, 4–6 panouri/pagină (splash și double-spread excepții), pentru fiecare panou: descriere vizuală pentru desenator (unghi, încadrare, lumină, paletă), baloane (≤25 cuvinte/balon), casete de narațiune (flashback sepia cu margine aurie; casete senzoriale argintii ale lui Vlad), SFX; marcarea celor 12 „întoarceri de pagină” (ultimul panou al paginilor impare); 1 splash page; 1 double-spread. Plus șablonul standard reutilizabil. Română, diacritice.` }

async function writeThen(item, writerPrompt, phaseName) {
  await agent(writerPrompt + `\nARHIVARE: după ce scrii, salvează o copie a versiunii inițiale (R0) a fișierelor tale în ${DOSAR(item.code)}\\R0_versiune_initiala\\.`, { label: `scrie ${item.code}`, phase: phaseName })
  return gate(item, phaseName)
}

const results = []

if (gates.includes('G0')) {
  phase('G0 Canon & Studio')
  const r = await parallel(G0_ITEMS.map(it => () => gate(it, 'G0 Canon & Studio')))
  results.push(...r.filter(Boolean))
}

if (gates.includes('G1')) {
  phase('G1 Fundație')
  const r = await parallel(G1_ITEMS.map(it => () => gate(it, 'G1 Fundație')))
  results.push(...r.filter(Boolean))
}

if (gates.includes('G2')) {
  phase('G2 Arc sezon')
  const r = await writeThen(ARC_ITEM, `Ești D1 „Plot Architect”, șeful Writers' Room la DRACULA COMICS STUDIO. Mod de gândire: „Suspansul înseamnă informație dozată.” Citește integral: canonul ${CANON}, organizarea ${STUDIO} (§4.4), research-ul din ${P('02_RESEARCH')} (toate fișierele — banca de mecanisme și semințele de plot), personajele ${P('03_PERSONAJE')} și lumea ${P('04_LUME')} (în special 06_TRASEUL_CAPITALELOR.md și 05_MISTERUL_OMULUI_FARA_UMBRA.md).
${LOCKED}
Scrie ${ARC}. Cerințe: ${ARC_ITEM.brief}
Scrie și raportul ${P('00_STUDIO/rapoarte/D1_plot.md')} după șablonul din organizare §5. Returnează rezumat ≤10 rânduri.`, 'G2 Arc sezon')
  results.push(r)
}

if (gates.includes('G3')) {
  phase('G3-4 Episoade')
  const eps = (EXTRA.episodes) || Array.from({ length: 20 }, (_, i) => i + 1)
  const epResults = await pipeline(eps,
    n => writeThen(plotItem(n), `Ești D1 „Plot Architect” la DRACULA COMICS STUDIO. Citește: canonul ${CANON}, arcul aprobat ${ARC} (harta episoadelor și planul de indicii — respectă-le strict), banca de mecanisme ${P('02_RESEARCH/02_BANCA_MECANISME_PLOT.md')}, recomandările ${P('02_RESEARCH/03_RECOMANDARI_DRACULA.md')}, personajele ${P('03_PERSONAJE')}, lumea ${P('04_LUME')} (06_TRASEUL_CAPITALELOR.md pentru popasul episodului; 05_MISTERUL... pentru indiciile arcului lung).
${LOCKED}
Scrie ${epFile(n)}. ${plotItem(n).brief}
Returnează rezumat ≤5 rânduri.`, 'G3-4 Episoade'),
    (plotRes, n) => {
      if (!plotRes || plotRes.status !== 'PASS') return { plot: plotRes, story: null }
      return writeThen(storyItem(n), `Ești prozatorul ${PROZATOR(n)} la DRACULA COMICS STUDIO. Mod de gândire: „Aceeași poveste, alt instrument” — proza dă interioritate și simțurile lui Vlad din interior. Citește: canonul ${CANON}, plotul aprobat ${epFile(n)}, arcul ${ARC}, personajele ${P('03_PERSONAJE')} (voci, replici), lumea ${P('04_LUME')} (popasul flashback-ului în 06_TRASEUL_CAPITALELOR.md, locurile în 04_LOCURI.md).
${LOCKED}
Scrie ${storyFile(n)}: ${storyItem(n).brief}
După scriere numără cuvintele (Python) și ajustează până intri în 3.000–4.000. Returnează titlul și numărul de cuvinte.`, 'G3-4 Episoade').then(s => ({ plot: plotRes, story: s }))
    })
  for (const e of epResults) { if (e) { if (e.plot) results.push(e.plot); if (e.story) results.push(e.story) } }
}

if (gates.includes('G4')) {
  phase('G4 Scenariu BD')
  const r = await writeThen(SCRIPT_ITEM, `Ești D2 „Scenarist BD” la DRACULA COMICS STUDIO. Mod de gândire: „Gândesc în panouri, nu în paragrafe.” Citește: canonul ${CANON}, plotul aprobat ${epFile(1)}, povestirea ${storyFile(1)} (dacă există), arcul ${ARC}, ghidul vizual ${P('05_ART/00_GHID_STIL_VIZUAL.md')}, personajele ${P('03_PERSONAJE')}, locurile ${P('04_LUME/04_LOCURI.md')}.
${LOCKED}
Scrie ${SCRIPT_ITEM.files.join(' și ')}. ${SCRIPT_ITEM.brief}
Scrie și raportul ${P('00_STUDIO/rapoarte/D2_scenariu.md')}. Returnează rezumat ≤5 rânduri.`, 'G4 Scenariu BD')
  results.push(r)
}

if (gates.includes('G5')) {
  phase('G5 QA & Site')
  const qaItem = { code: 'F2-QA', role: 'F2. Editor de continuitate', name: 'Raportul de continuitate + corecturile aplicate pe tot proiectul', files: [P('00_STUDIO/04_RAPORT_CONTINUITATE.md'), ROOT], snap: [P('00_STUDIO/04_RAPORT_CONTINUITATE.md')],
    brief: `Verificare 100% a episoadelor, povestirilor, scenariului, personajelor și lumii față de canon: nume, date, vârste, puteri, reguli, cine știe ce și când (Ioana află în Ep10!), traseul capitalelor, planul de indicii setup→payoff (fiecare indiciu plătit, fiecare plată plantată). Raportul listează fiecare eroare (locație, gravitate, corectură) ȘI confirmă că a fost corectată în fișiere. La final: 0 erori critice/majore rămase. (Nu audita conținutul din ${AUDIT_DIR} — e arhivă.)` }
  const qa = await writeThen(qaItem, `Ești F2 „Editor de continuitate” la DRACULA COMICS STUDIO. Mod de gândire: „Cititorul fan va observa. Eu observ primul.” Citește TOT proiectul din ${ROOT} (canon, personaje, lume, arc, 20 de ploturi, 20 de povestiri, scenariul; ignoră arhiva ${AUDIT_DIR}). ${LOCKED}
Găsește toate erorile de continuitate și CORECTEAZĂ-LE direct în fișierele afectate (fără a schimba canonul; propunerile de canon le scrii în raport). Scrie ${P('00_STUDIO/04_RAPORT_CONTINUITATE.md')}: ${qaItem.brief} Scrie și ${P('00_STUDIO/rapoarte/F2_qa.md')}. Returnează rezumat ≤8 rânduri.`, 'G5 QA & Site')
  results.push(qa)
  const siteItem = { code: 'F1-SITE', role: 'F1. Web Studio', name: 'Site-ul local unitar al proiectului', files: [P('09_SITE/build_site.py'), P('09_SITE/index.html'), P('09_SITE/RECONSTRUIESTE_SITE.bat')],
    brief: `Site local HTML (un singur index.html, funcționează prin dublu-clic, offline + Google Fonts) generat de build_site.py din toate folderele: Acasă (pitch + statistici), Studio & Roadmap, Progres (rapoarte + jurnal), **AUDIT** (registrul central ${AUDIT_DIR}\\00_REGISTRU_AUDIT.md + pentru fiecare livrabil dosarul complet: rapoartele celor 3 auditori pe runde, planurile de măsuri cu execuția, rezultatul final, grafic al evoluției notelor pe runde, tablou „Poarta 9,50” cu status PASS/BLOCAT), Canon, Personaje, Lume, Traseul secolelor (timeline + hartă SVG a popasurilor), Artă (galerie SVG cu lightbox), Episoade (20 carduri cu titlu + logline, legături la povestire/scenariu), Povestiri (cititor cu nr. cuvinte + indicator KPI), Scenarii, Research; secțiune confidențială ascunsă pentru misterul antagonistului; căutare full-text; responsive (telefon 16px gutter, fără scroll orizontal); design gotic-premium cu paleta canon și sigla din 05_ART/logo. 100% din fișierele .md/.svg ale proiectului prezente (copiile din folderele de versiuni ale arhivei pot fi doar listate cu link, nu randate integral). Build <10s, UTF-8, diacritice corecte. Auditorii trebuie să ruleze build-ul și să deschidă index.html în browser (mcp__Claude_Browser__preview_start cu url file:///...) și să verifice vizual desktop + mobil.` }
  const site = await writeThen(siteItem, `Ești F1 „Web Studio” la DRACULA COMICS STUDIO. Actualizează ${P('09_SITE/build_site.py')} astfel încât să îndeplinească: ${siteItem.brief} Rulează build-ul, verifică rezultatul în browser (dacă poți) și scrie raportul ${P('00_STUDIO/rapoarte/F1_web.md')}. Returnează rezumat ≤8 rânduri.`, 'G5 QA & Site')
  results.push(site)
}

phase('Registru')
await agent(`Ești grefierul-șef de audit al DRACULA COMICS STUDIO. Actualizează REGISTRUL CENTRAL ${AUDIT_DIR}\\00_REGISTRU_AUDIT.md (română, markdown): dacă există, păstrează toate intrările anterioare și adaugă/actualizează; dacă nu, creează-l. Conținut: explicația sistemului „Poarta 9,50” (3 auditori, nota minimă ≥ 9,50, ședință + plan de măsuri + revizie, max ${MAX_ROUNDS} runde) și a structurii arhivei; TABELUL MASTER cu toate livrabilele auditate vreodată (cod, livrabil, poartă, nr. runde, notele finale per auditor, nota minimă, status ✅/🔴, dată, link la dosar și la REZULTAT_FINAL.md); statistici (total runde, total defecte, nota medie finală); lista deciziilor necesare de la Producător (BLOCAT). Sursa: scanează toate dosarele din ${AUDIT_DIR} (REZULTAT_FINAL.md, R<n>_*.md) + rezultatele acestei rulări: ${JSON.stringify(results.map(r => ({ code: r.code, name: r.name, status: r.status, rounds: r.rounds, min: r.min, history: r.history })))} (data ${DATE}).
Apoi actualizează ${P('00_STUDIO/03_JURNAL_PROGRES.md')}: tabelul de faze (stare reală a porților rulate: ${gates.join(', ')}) și o intrare nouă datată cu rezultatele. Returnează "ok".`, { label: 'registru central audit', phase: 'Registru', effort: 'low' })

log(`Rezultat porți: ${results.map(r => `${r.code}:${r.status}(R${r.rounds}, min ${typeof r.min === 'number' ? r.min.toFixed(2) : r.min})`).join(' | ')}`)
return results.map(r => ({ code: r.code, status: r.status, rounds: r.rounds, min: r.min }))
