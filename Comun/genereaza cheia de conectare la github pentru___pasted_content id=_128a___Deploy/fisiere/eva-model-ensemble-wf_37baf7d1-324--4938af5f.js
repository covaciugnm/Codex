export const meta = {
  name: 'eva-model-ensemble',
  description: 'Toate modelele/codecurile/motoarele concurente + selector pornit/oprit in setari (site si aplicatie) + evaluator + ansambluri (detectie obiecte, segmentare, vocabular deschis, audio, voce) pe server, cu licente verificate si benchmark masurat; audit pana la 10/10',
  phases: [
    { title: 'Cercetare', detail: 'candidati pe domenii, licente, cerinte CPU/GPU' },
    { title: 'Arhitectura', detail: 'registru, interfata de inferenta, fuziune, recenzie independenta' },
    { title: 'Implementare', detail: 'echipe pe domenii in paralel' },
    { title: 'Benchmark', detail: 'masurare pe seturi publice, alegere ansamblu' },
    { title: 'Audit', detail: '3 auditori independenti' },
    { title: 'Remediere', detail: 'reluare pana la 10/10' },
  ],
}

const CTX = `
CONTEXT COMUN:
- Repo GitHub covaciugnm/3dscan.eva-org.com (privat), aplicatie iOS EVA 3D Scan + extindere robotica (documente in "Aplicație/Extindere-Robotica/": Plan_implementare_2026-10-06/ cu CONTRACTE_V2, EXECUTIE_TESTE_V2, rapoartele 03-modele-voce-llm.md si 04-candidati-research.md si vision-robotics.md — CITESTE-LE, contin deja comparatii de modele; nu relua cercetarea de la zero, actualizeaz-o si verifica-o).
- Esti pe laptop Windows; lucrezi pe server: ssh -o BatchMode=yes saga-server@192.168.100.151 '<comenzi>' (Docker fara sudo, fara sudo pe host — totul in containere). Server: i9-12900KF 24 fire, 125 GB RAM (~60 GB liberi), ~460 GB disc liber, 2x RTX 3060 12 GB DAR driver NVIDIA NEINCARCAT => totul pe CPU acum (ONNX Runtime / OpenVINO CPU), arhitectura cu profil GPU optional activabil ulterior fara schimbari de cod.
- NU atinge checkout-ul live ~/site-uri/3dscan.eva-org.com, containerele live sau DB-ul live; ~120 containere ale altor proiecte — nu le atinge, fara prune global; atentie la consumul de RAM/CPU (limiteaza containerele tale cu --cpus/--memory ca sa nu afectezi productia). Alte echipe in paralel: feat/scene-live (scene-gateway, scene-recon cu detectii proiectate 3D si obiecte, scene-audio cu clasificare sunete/VAD/transcriere/amprente echipamente, magazie; migrarea 013), feat/admin-live (012), feat/b05-sequencer (014), feat/b09-worldmodel (010), feat/b12-leases (011), feat/b15-ops (compose.robot.yaml cu profile si model-registry/evaluator propus), feat/model-export (D-FINE M Obj365 ONNX exportat, in volumul models al workerului live; Site/worker/MODEL_EXPORT.md). Tu: branch feat/models din origin/main, migrare Site/db/015-models.sql daca e nevoie. Integrarea cu scene-recon/scene-audio se face printr-o INTERFATA de inferenta pe care o definesti si o documentezi (Site/docs/MODELE_INTERFATA.md) — nu edita fisierele echipei de scena; ele o vor consuma.
- Clona ~/work/3dscan-models (git clone ~/site-uri/3dscan.eva-org.com; git remote set-url origin git@github-3dscan-eva:covaciugnm/3dscan.eva-org.com.git). Agentii lucreaza in aceeasi clona pe fisiere diferite, git pull --rebase inainte de push, fara force, niciodata main. Commit-uri cu linia finala: Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- Modele DOAR din surse oficiale (GitHub/HuggingFace al autorilor), cu licenta si hash notate; fara a comite greutati in git (volum models + manifest). Onestitate: ce n-ai rulat = not_run; acuratete si latenta DOAR masurate pe CPU-ul serverului.

CERINTA PROPRIETARULUI (trei mesaje): "daca sunt mai multe modele pe care le putem implementa pentru a obtine [rezultatul cel mai bun]"; "daca sunt mai multe modele / codecuri / versiuni de soft similare sau concurentiale pe care le putem implementa pentru a obtine - folosi in diverse sarcini - instaleaza toate si pune selector in setings - sa putem sa oprim din butoane"; "sau schimba aplicatia" (= comutarea trebuie posibila si din aplicatia iPhone) — adica: INSTALEAZA TOATE variantele concurente fezabile (nu doar 2-3) pentru fiecare sarcina — modele, codecuri, motoare software, backend-uri de inferenta si versiuni diferite ale aceluiasi soft side-by-side — fiecare pornit/oprit dintr-un SELECTOR IN SETARI cu butoane, pe site SI din aplicatia iOS; mai multe modele per sarcina, comparate masurat si combinate (ansamblu/fuziune) acolo unde combinatia bate cel mai bun model individual; plus rezolvarea problemei de licenta (D-FINE Obj365 poate fi necomercial) prin alternative cu licenta permisiva.

DOMENII:
A. Detectie obiecte pe cadre RGB (clase inchise COCO/Objects365/LVIS): ex. D-FINE (Apache-2.0 cod; atentie licenta greutati obj365), RT-DETR/RT-DETRv2 (Apache-2.0), DEIM, RF-DETR (Apache-2.0) — verifica; EXCLUDE sau marcheaza clar AGPL (Ultralytics YOLO) ca necomercial fara licenta platita.
B. Vocabular deschis / interogare text ("cana de langa monitor"): ex. OWLv2 (Apache-2.0), Grounding DINO (Apache-2.0), YOLO-World (verifica licenta), Florence-2 (MIT).
C. Segmentare instante: SAM 2 / SAM 2.1 (Apache-2.0), EfficientSAM/ MobileSAM — pentru masti precise ale obiectelor in 3D (decupaj nor de puncte per obiect). SAM 3 / SAM3D din rapoarte: verifica licenta si cerinta VRAM — probabil doar profil GPU.
D. Clasificare sunete: YAMNet (Apache-2.0), PANNs CNN14 (MIT), BEATs (MIT), AST (BSD-3), CLAP (LAION/Microsoft — verifica) pentru zero-shot si amprente de echipamente.
E. Voce: VAD (Silero, MIT), transcriere (faster-whisper / Whisper, MIT; variante large-v3-turbo vs small pe CPU), diarizare (pyannote — verifica licenta/gating; alternative).
G. CODECURI (pentru fluxurile scenei: inregistrare, transport, arhivare, previzualizare — calea bruta implicita ramane raw/necodificata, codecurile sunt OPTIUNI selectabile, iar cele cu pierderi sunt etichetate clar ca atare): video — raw YUV, FFV1 (lossless), H.264 (x264/openh264 — atentie licente/patente), HEVC/H.265 (x265), AV1 (SVT-AV1, libaom, dav1d), VP9; imagini — PNG, WebP lossless, JPEG XL lossless, JPEG; audio — PCM float32/int16, FLAC, WavPack, Opus, AAC; adancime — raw f32, zstd/lz4 lossless, RVL, PNG 16-bit; nor de puncte/mesh — PLY, Draco, glTF/GLB, meshoptimizer, LAS/LAZ. Toate prin ffmpeg/biblioteci in containere; transcodare la cerere din arhiva bruta (bruta nu se modifica); benchmark: raport de compresie, viteza, eroare (0 pentru lossless — verificat bit-exact).
H. MOTOARE SOFTWARE CONCURENTE: reconstructie 3D / fuziune — Open3D TSDF (ScalableTSDFVolume si VoxelBlockGrid), alternative CPU (ex. Voxblox / RTAB-Map / KinectFusion open-source — verifica licente si fezabilitate in container), GPU (nvblox — doar profil GPU, instalat dar dezactivat fara driver); backend-uri de inferenta — ONNX Runtime CPU, OpenVINO, (TensorRT/CUDA doar profil GPU); versiuni diferite ale aceluiasi model/soft instalate side-by-side cu selector (ex. D-FINE S/M/L, Whisper tiny/base/small/medium/large-v3-turbo, SAM 2.1 tiny/small/base/large).
F. (optional, daca timpul permite) Descriptori pentru re-identificarea aceluiasi obiect intre sesiuni/roboti (ex. DINOv2 Apache-2.0) — util magaziei.

SPECIFICATIE TINTA:
1. Registru de modele (model-registry): manifest per model (nume, versiune, sursa oficiala, licenta + uz comercial da/nu/neclar, sha256 greutati, format ONNX/OpenVINO, intrari/iesiri, cerinte CPU/RAM/VRAM, profil cpu|gpu), stocare in volum, descarcare/export reproductibil (scripturi), activare/dezactivare per model fara redeploy, versionare cu rollback.
2. Serviciu de inferenta (model-server, container nou, retea privata, fara porturi pe host): API intern uniform per domeniu (detect, detect_open_vocab, segment, classify_audio, vad, transcribe, embed), batching, limite de concurenta si memorie, warm-up, health/ready, rezultate cu model+versiune pe fiecare predictie (provenienta).
3. Ansambluri: detectie — Weighted Boxes Fusion / fuziune per clasa cu ponderi invatate pe setul de validare; audio — medie calibrata a probabilitatilor peste maparea comuna a claselor AudioSet; politica "cel mai bun per clasa"; ansamblul se activeaza DOAR daca benchmark-ul arata castig masurat fata de cel mai bun individual (altfel ramane individualul) — documentat cu cifre.
4. Evaluator: rulare automata pe seturi publice cu licenta verificata (ex. COCO val2017 subset pentru detectie, LVIS/ODinW mic pentru vocabular deschis, ESC-50 pentru audio, LibriSpeech test-clean subset pentru transcriere), metrici standard (mAP, AP50, recall, latenta p50/p95 pe CPU, RAM de varf), raport generat (Site/docs/MODELE_BENCHMARK.md + json) si tabel in registru; re-rulabil la fiecare model nou.
5. Matrice de licente (Site/docs/MODELE_LICENTE.md): per model cod vs greutati vs set de date, uz comercial, obligatii; recomandarea unui set implicit 100% permisiv pentru productie si a unui set "cercetare" separat, comutabil.
7. SELECTOR IN SETARI (obligatoriu), pe site SI in aplicatia iOS: API /api/admin/engines (listare cu stare, licenta, profil cpu/gpu, resurse, cifre de benchmark; PUT pentru pornit/oprit, alegere implicita per sarcina, ordine/ponderi in ansamblu, set productie vs cercetare) cu autorizare de admin — refoloseste mecanismul de rol al zonei admin (citeste Site/docs/ADMIN_ARHITECTURA.md pe origin/feat/admin-live; daca nu e inca disponibil, izoleaza verificarea intr-o singura functie usor de inlocuit la merge) si jurnal de audit al fiecarei comutari (cine, de unde: web sau aplicatie); aplicare LIVE fara redeploy (model-server si consumatorii reincarca configuratia; oprirea unui motor elibereaza memoria; un motor care nu poate porni — ex. GPU fara driver — apare dezactivat cu motivul); eveniment de schimbare propagat live (SSE/WebSocket) catre toti clientii, inclusiv aplicatia. Pagina web public/setari/ (fara inline, CSP, vendor local, responsive, tema intunecata): grupuri pe sarcini (Detectie, Vocabular deschis, Segmentare, Re-identificare, Sunete, Voce, Codecuri video/imagine/audio/adancime/3D, Reconstructie, Backend inferenta, Versiuni), fiecare intrare cu buton pornit/oprit, radio pentru implicit, badge licenta (comercial/cercetare/neclar), badge cpu/gpu, cifre benchmark, consum memorie live, stare (incarcat/oprit/eroare). Link din /admin/ fara a edita fisierele echipei admin. APLICATIA iOS: GET /api/app/settings (setarile pe care telefonul trebuie sa le respecte: codec de transport, ce fluxuri trimite, rezolutie/cadenta, motoare on-device vs server) + aceleasi operatii de comutare ca pe web pentru un utilizator admin autentificat din aplicatie (acelasi API, aceeasi autorizare), cu notificare live a schimbarilor; contract complet pentru ecranul de Setari din iOS in Site/docs/SETARI_MOTOARE.md (lista de controale, stari, erori, chei i18n propuse in cele 7 limbi).
6. Teste: fiecare adaptor de model produce iesiri in formatul interfetei, provenienta prezenta, model lipsa => eroare onesta (nu cade serviciul), limitele de memorie respectate, fuziunea testata pe cazuri construite, evaluatorul reproduce aceleasi cifre la re-rulare (toleranta declarata).
`

const PLAN = { type: 'object', properties: { contract_path: { type: 'string' }, summary: { type: 'string' }, candidates: { type: 'array', items: { type: 'object', properties: { domain: { type: 'string' }, model: { type: 'string' }, license: { type: 'string' }, commercial: { type: 'string' }, cpu_feasible: { type: 'string' } }, required: ['domain', 'model', 'license', 'commercial', 'cpu_feasible'] } }, tasks: { type: 'object', properties: { vision: { type: 'array', items: { type: 'string' } }, audio: { type: 'array', items: { type: 'string' } }, platform: { type: 'array', items: { type: 'string' } }, 'codecs-engines': { type: 'array', items: { type: 'string' } }, 'settings-ui': { type: 'array', items: { type: 'string' } } }, required: ['vision', 'audio', 'platform', 'codecs-engines', 'settings-ui'] } }, required: ['contract_path', 'summary', 'candidates', 'tasks'] }
const RESULT = { type: 'object', properties: { commit: { type: 'string' }, status: { type: 'string', enum: ['done', 'partial', 'blocked'] }, delivered: { type: 'array', items: { type: 'string' } }, tests: { type: 'array', items: { type: 'object', properties: { name: { type: 'string' }, result: { type: 'string', enum: ['pass', 'fail', 'not_run'] }, evidence: { type: 'string' } }, required: ['name', 'result', 'evidence'] } }, measurements: { type: 'array', items: { type: 'string' } }, open_issues: { type: 'array', items: { type: 'string' } }, decisions_for_user: { type: 'array', items: { type: 'string' } } }, required: ['commit', 'status', 'delivered', 'tests', 'measurements', 'open_issues', 'decisions_for_user'] }
const REVIEW = { type: 'object', properties: { approved: { type: 'boolean' }, score: { type: 'number' }, issues: { type: 'array', items: { type: 'string' } } }, required: ['approved', 'score', 'issues'] }
const AUDIT = { type: 'object', properties: { score: { type: 'number' }, tests_rerun: { type: 'array', items: { type: 'string' } }, findings: { type: 'array', items: { type: 'object', properties: { severity: { type: 'string', enum: ['blocant', 'major', 'minor'] }, description: { type: 'string' }, location: { type: 'string' } }, required: ['severity', 'description', 'location'] } }, merge_ready: { type: 'boolean' }, verdict: { type: 'string' } }, required: ['score', 'tests_rerun', 'findings', 'merge_ready', 'verdict'] }

phase('Cercetare')
const research = await parallel([
  ['viziune', 'domeniile A, B, C, F'],
  ['audio-voce', 'domeniile D, E'],
  ['codecuri-motoare', 'domeniile G, H (codecuri, motoare de reconstructie/SLAM, backend-uri de inferenta, versiuni)'],
].map(([k, d]) => () => agent(`${CTX}
ROL: CERCETATOR ${k} (${d}). Scopul e LISTA COMPLETA a variantelor concurente fezabile (proprietarul vrea sa le instalam pe toate cu selector), nu doar cele mai bune. Pornind de la rapoartele existente din repo (03-modele-voce-llm.md, 04-candidati-research.md, vision-robotics.md), verifica pe surse primare actuale (paginile oficiale GitHub/HuggingFace/paper; poti folosi WebSearch/WebFetch) fiecare candidat: licenta cod SI greutati SI set de antrenare, uz comercial, disponibilitate export ONNX/OpenVINO, acuratete publicata pe benchmark standard, fezabilitate CPU (dimensiune, latenta estimata — marcata estimare). Adauga candidati noi relevanti aparuti recent. Nu scrii in repo. Intoarce o lista structurata, cu link sursa pentru fiecare afirmatie de licenta.`, { label: `Cercetare ${k}`, phase: 'Cercetare' })))

phase('Arhitectura')
let plan = await agent(`${CTX}
ROL: ARHITECT. Rezultatele cercetarii (date): ${JSON.stringify(research).slice(0, 14000)}
Creeaza clona si branch-ul feat/models; comite Site/docs/MODELE_ARHITECTURA.md (registru, model-server, interfata, fuziune, evaluator, profile cpu/gpu, limite resurse, compose), Site/docs/MODELE_INTERFATA.md (contractul exact consumat de scene-recon/scene-audio) si Site/docs/MODELE_LICENTE.md (matricea initiala). Include TOTI candidatii fezabili (pe CPU acum; cei doar-GPU instalati ca definitie si dezactivati cu motivul), cu set productie (licente comerciale) si set cercetare (necomercial/AGPL, oprit implicit, etichetat). Imparte pe 5 echipe care nu editeaza aceleasi fisiere: platform (registru, model-server, evaluator, fuziune generica, compose, API /api/admin/engines + /api/app/settings, aplicare si notificare live), vision (adaptoare A/B/C/F + exporturi + versiuni), audio (adaptoare D/E + versiuni), codecs-engines (G + H: codecuri, transcodare la cerere, motoare de reconstructie, backend-uri inferenta, benchmark bit-exact), settings-ui (public/setari/ + SETARI_MOTOARE.md pentru ecranul iOS). Push.`, { label: 'Arhitect modele', phase: 'Arhitectura', schema: PLAN })

for (let r = 1; r <= 4; r++) {
  const lenses = ['licente si conformitate (cod/greutati/date, uz comercial, set implicit 100% permisiv), surse oficiale', 'fezabilitate tehnica pe CPU si izolarea resurselor de productie, interfata si provenienta, fuziune corecta statistic, evaluare reproductibila']
  const reviews = (await parallel(lenses.map((lens, i) => () => agent(`${CTX}
ROL: RECENZENT INDEPENDENT (runda ${r}, lentila: ${lens}). Citeste documentele de arhitectura pe origin/feat/models (clona proprie ~/work/3dscan-modrev${i}, stearsa la final). Nu scrii in repo. approved=true doar fara lipsuri pe lentila ta; score 0-10; issues concrete.`, { label: `Recenzie arh r${r}.${i + 1}`, phase: 'Arhitectura', schema: REVIEW })))).filter(Boolean)
  const issues = reviews.flatMap(v => v.issues)
  log(`Arhitectura modele r${r}: ${reviews.map(v => v.score).join('/')}, ${issues.length} probleme`)
  if (reviews.length === 2 && reviews.every(v => v.approved && v.score >= 10) && !issues.length) break
  if (r === 4) { log('Arhitectura modele: limita 4 runde — problemele ramase trec la implementare'); plan = { ...plan, summary: plan.summary + ' | PROBLEME RAMASE: ' + JSON.stringify(issues).slice(0, 4000) }; break }
  plan = await agent(`${CTX}
ROL: ARHITECT (revizie r${r}). Rezolva TOATE problemele in documentele de pe feat/models (clona ~/work/3dscan-models, git pull), commit + push: ${JSON.stringify(issues).slice(0, 9000)}`, { label: `Arhitect revizie r${r}`, phase: 'Arhitectura', schema: PLAN })
}

phase('Implementare')
const impl = await parallel(['platform', 'vision', 'audio', 'codecs-engines', 'settings-ui'].map(k => () => agent(`${CTX}
ROL: ECHIPA ${k.toUpperCase()}. Documente pe feat/models (git pull). Rezumat arhitect: ${plan.summary}
Candidati aprobati: ${JSON.stringify(plan.candidates).slice(0, 5000)}
Sarcinile tale: ${JSON.stringify(plan.tasks[k])}
Implementeaza complet cu teste; descarca/exporta modelele din surse oficiale in containere limitate (--cpus 8 --memory 16g maxim), verifica sha256, inregistreaza in manifest. Teste in stack izolat docker compose -p 3dscan-models (fara porturi pe host), down -v la final (NU sterge volumul cu greutati daca e partajat intre echipe — foloseste un volum denumit explicit pastrat, documentat). Commit + push (pull --rebase).`, { label: `Impl ${k}`, phase: 'Implementare', schema: RESULT })))

phase('Benchmark')
const bench = await agent(`${CTX}
ROL: EVALUATOR. feat/models (git pull). Rapoarte (date): ${JSON.stringify(impl).slice(0, 8000)}
Ruleaza evaluatorul pe toate modelele active pe seturile publice (descarca seturile cu licenta verificata, subset documentat ca dimensiune daca e nevoie pentru timp CPU — raporteaza dimensiunea exacta, fara a pretinde set complet). Masoara acuratete + latenta p50/p95 + RAM de varf pe CPU-ul serverului, cu limita de resurse declarata. Calibreaza/invata ponderile de fuziune pe o impartire validare, raporteaza pe o impartire test separata; activeaza ansamblul doar unde bate masurat cel mai bun individual. Genereaza Site/docs/MODELE_BENCHMARK.md + json, actualizeaza registrul cu setul implicit de productie (doar licente permisive) si setul de cercetare. Commit + push.`, { label: 'Benchmark si ansambluri', phase: 'Benchmark', schema: RESULT })

phase('Audit')
const LENSES = [
  'LICENTE SI SURSE: fiecare model din setul implicit are licenta cod+greutati+date compatibila comercial, link oficial, sha256 verificat (recalculeaza), nimic AGPL/necomercial in setul implicit',
  'CORECTITUDINE SI REPRODUCTIBILITATE: re-ruleaza evaluatorul pe un subset si compara cifrele (toleranta declarata), verifica fuziunea (separare validare/test, fara scurgere), interfata respectata de toate adaptoarele, provenienta pe fiecare predictie, erori oneste la model lipsa',
  'SELECTOR SI OPERARE: E2E prin tunel ssh -L + browserul integrat (mcp__Claude_Browser__*) pe pagina /setari/: fiecare buton porneste/opreste efectiv motorul (verifica in model-server si memoria eliberata), implicitul per sarcina se aplica live, /api/app/settings reflecta schimbarea si comutarea prin API ca din aplicatie (admin) functioneaza identic, notificare live, autorizare admin + jurnal de audit, codecurile lossless verificate bit-exact, SETARI_MOTOARE.md complet pentru iOS; limite CPU/RAM respectate (masoara), fara porturi pe host, fara impact pe productie, activare/dezactivare/rollback model fara redeploy, health/ready, profil GPU documentat si inofensiv fara driver, documentatie completa pentru integrarea echipei de scena',
]
const history = []
let audits = [], round = 0
while (true) {
  round++
  audits = (await parallel(LENSES.map((lens, i) => () => agent(`${CTX}
ROL: AUDITOR INDEPENDENT runda ${round} (nu ai scris codul, nu repari, nu faci push). Lentila: ${lens}.
Auditeaza origin/feat/models fata de origin/main in clona proprie ~/work/3dscan-modaudit${i} (stearsa la final). Benchmark (date): ${JSON.stringify(bench).slice(0, 3000)}${history.length ? `\nIstoric (date; verifica remedierile declarate): ${JSON.stringify(history).slice(-6000)}` : ''}
Re-ruleaza testele in stack izolat -p 3dscan-modaudit${i} (fara porturi pe host, limite de resurse), apoi down -v (pastreaza volumul partajat de greutati). Nota 10 = zero constatari pe lentila ta, verificat prin rulare. Orice constatare => < 10. Ce cere GPU, declarat onest not_run, NU scade nota.`, { label: `Audit modele r${round}.${i + 1}`, phase: 'Audit', schema: AUDIT })))).filter(Boolean)
  const findings = audits.flatMap(a => a.findings)
  const scores = audits.map(a => a.score)
  log(`Audit modele r${round}: ${scores.join('/')}, ${findings.length} constatari`)
  history.push({ round, scores, findings: findings.map(f => `${f.severity}: ${f.description} @ ${f.location}`) })
  if (audits.length === LENSES.length && scores.every(s => s >= 10) && !findings.length) break
  if (round >= 8) { log('Limita 8 runde audit modele fara 10/10 — raportez constatarile ramase'); break }
  phase('Remediere')
  await agent(`${CTX}
ROL: ECHIPA DE REMEDIERE runda ${round}. Clona ~/work/3dscan-models, feat/models (git pull). Rezolva TOATE constatarile (blocante, majore, minore) cu teste/masuratori care dovedesc remedierea; nu slabi testele. Constatare gresita => demonstreaza prin rulare in Site/docs/MODELE_AUDIT_RASPUNS.md (runda ${round}). Commit + push.
Constatari: ${JSON.stringify(findings).slice(0, 12000)}`, { label: `Remediere modele r${round}`, phase: 'Remediere', schema: RESULT })
  phase('Audit')
}
return { research, plan, implementation: impl, benchmark: bench, audit_rounds: history, final_audits: audits }