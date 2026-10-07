export const meta = {
  name: 'eva-a1-pipeline-consolidare',
  description: 'Straturile 2 (pipeline conversatie/voce EVA) si 3 (SRS live + scenariu + evaluare automata) pentru cele 12 unitati A1 + testele de nivel',
  phases: [
    { title: 'Pipeline + Consolidare A1', detail: '12 agenti/unitate + 1 agent teste de nivel' },
  ],
}

phase('Pipeline + Consolidare A1')

const BASE = "Z:\\02. EVA - Learn English with EVA\\10. Curriculum EVA (A1-C2)\\Nivel A1 - Componenta scrisa\\"

const UNITS = [
  {n:1, title:"Hello & Goodbye", theme:"salut, alfabet, spelling", gram:"pronume personale subiect; My name is...; imperative de clasa", phon:"/h/ aspirat", file:"A1-U01 - Hello and Goodbye.md"},
  {n:2, title:"Who are you?", theme:"informatii personale, tari", gram:"verbul to be (afirmativ/negativ/interogativ)", phon:"/iː/ vs /ɪ/", file:"A1-U02 - Who are you.md"},
  {n:3, title:"A, an or the?", theme:"obiecte, articole (contrastiv RO)", gram:"a/an vs the vs articol zero", phon:"schwa /ə/; /ð/ in the", file:"A1-U03 - A, an or the.md"},
  {n:4, title:"This, that & many things", theme:"demonstrative, plural", gram:"this/that/these/those; plural -s/-es + neregulate", phon:"/ð/; terminatii plural /s z ɪz/", file:"A1-U04 - This, that and many things.md"},
  {n:5, title:"My family", theme:"familie, posesie", gram:"have got/has got; adjective posesive", phon:"/ð/ vs /θ/", file:"A1-U05 - My family.md"},
  {n:6, title:"Numbers & Age", theme:"numere, varsta, preturi", gram:"numere 0-100; How old...?; How many...?", phon:"/θ/ in three/thirteen/thirty; accent -teen/-ty", file:"A1-U06 - Numbers and Age.md"},
  {n:7, title:"What time is it?", theme:"ora, zile, luni, data", gram:"prepozitii de timp at/on/in; What time...? When...?", phon:"/θ/ Thursday; /z/ days", file:"A1-U07 - What time is it.md"},
  {n:8, title:"My daily routine", theme:"rutina (I/you/we)", gram:"present simple I/you/we/they + don't; adverbe de frecventa", phon:"/w/ vs /v/", file:"A1-U08 - My daily routine.md"},
  {n:9, title:"He works, she plays", theme:"persoana a III-a, WH", gram:"present simple pers. III -s/-es; does/doesn't; intrebari WH", phon:"terminatia -s /s z ɪz/", file:"A1-U09 - He works, she plays.md"},
  {n:10, title:"My house", theme:"casa, camere, mobilier", gram:"there is/are; prepozitii de loc", phon:"/ð/ there; /θ/ bathroom", file:"A1-U10 - My house.md"},
  {n:11, title:"Food & drink", theme:"mancare, preferinte", gram:"like/don't like + noun/-ing; some/any; can", phon:"/æ/ vs /e/; /ɔː/ water", file:"A1-U11 - Food and drink.md"},
  {n:12, title:"At the shop", theme:"cumparaturi (recapitulare)", gram:"Can I have...? How much is/are...?; recapitulare", phon:"/θ/ preturi; /aʊ/ how much", file:"A1-U12 - At the shop.md"},
]

const CTX = "PROIECT: EVA — English Voice Assistant, aplicatie chat-first (WhatsApp/Messenger) prin care un VORBITOR DE ROMANA invata engleza vorbind/scriind cu EVA (tutore AI prietenos, rabdator). NIVEL A1. Straturile de productie: Strat 1 = componenta scrisa (GATA). Acum construim Strat 2 (pipeline conversatie/voce) + Strat 3 (SRS live, scenariu, evaluare automata), COERENT cu Stratul 1 al unitatii. Control de nivel: doar A1, gramatica introdusa pana la aceasta unitate. Corectare prin RECAST (reformulare blanda, nu marcaj rosu). Sprijin in ROMANA la A1.";

const FMT = `FORMAT DE IESIRE (markdown curat; instructiuni in ROMANA, continut-tinta in ENGLEZA). Incepe EXACT cu:

### A1-U<n> — <Titlu> · Straturile 2 & 3 (Pipeline + Consolidare)

## STRATUL 2 — Pipeline (conversatie & voce cu EVA)

### A. Configuratia EVA (system prompt pt unitate)
Un system prompt CONCRET, gata de folosit, pt EVA pe aceasta unitate: rol/persona, nivel A1, tema, structurile si vocabularul-tinta de ELICITAT, reguli de corectare prin recast, proportia RO/EN, ce sa ceara cursantului, cum reactioneaza la tacere/greseala. (bloc de prompt)

### B. Fluxul conversatiei (3 etape)
- Etapa 1 GHIDAT: 4-6 replici EVA de pornire + raspunsuri MODEL + structura de elicitat.
- Etapa 2 SEMI-GHIDAT: intrebari deschise + indicii ("prompts").
- Etapa 3 LIBER: scenariul + obiectiv. Include ce face EVA daca userul greseste sau tace (branching).

### C. Ascultare (script audio pt TTS + itemi)
- Scriptul audio scurt A1 (dialog/monolog) de generat cu TTS.
- 4-5 itemi de comprehensiune + Raspunsuri.

### D. Pronuntie (drill + scorare)
- Sunete-tinta RO-focus + minimal pairs (perechi).
- Lista de cuvinte + 3-5 propozitii de drill.
- Config de scorare: ce foneme se evalueaza, prag (ex. >=80), feedback tipic pt romani.
- Set de shadowing (3-5 propozitii).

## STRATUL 3 — Consolidare & evaluare

### E. Pachet SRS (carduri live)
Tabel: | Front | Back | Tip (EN→RO / RO→EN / cloze) | Nota |. ~15-20 carduri bazate pe banca de propozitii (⑨) si vocabularul unitatii din Stratul 1. Config FSRS pe scurt (tag-uri, moment de introducere).

### F. Scenariu task-based
Situatia reala, obiectivul, criterii de succes MASURABILE, rubrica de scorare LLM (task completion / accuracy / fluency, cu descriptori A1), variante.

### G. Evaluare automata (test de unitate)
- Itemi in format STRUCTURAT pt corectare automata: pentru fiecare item o linie [tip | intrebare | (optiuni) | raspuns_corect | puncte] (MCQ, cloze, matching, reorder, traducere-check).
- Logica de scorare + prag de promovare (>=80%).
- Pt productie (vorbire/scriere): rubrica LLM (criterii + descriptori A1 + prag).
- MAPARE: fiecare obiectiv ① din Stratul 1 → item(i) care il testeaza.

Livreaza DOAR acest bloc markdown, complet.`;

const specs = UNITS.map((u) => ({
  label: `A1-U${String(u.n).padStart(2,'0')}-s23`,
  prompt: `${CTX}\n\nUNITATEA: A1-U${u.n} — "${u.title}" (tema: ${u.theme}; gramatica: ${u.gram}; fonetica RO: ${u.phon}).\n\nPAS OBLIGATORIU: citeste mai intai fisierul cu Stratul 1 al acestei unitati, ca sa fii COERENT cu textul, vocabularul exact, task-ul (⑧) si banca SRS (⑨) deja scrise:\n"${BASE}${u.file}"\n\nApoi produce Straturile 2 si 3 pentru aceasta unitate.\n\n${FMT}`,
}));

specs.push({
  label: 'A1-teste-nivel',
  prompt: `${CTX}\n\nSARCINA: Proiecteaza TESTELE DE NIVEL pentru A1 (nu per unitate, ci la nivel): 3 checkpoint-uri + testul final A1 (promovare la A2). Cele 12 unitati: U1 Hello&Goodbye, U2 Who are you (to be), U3 articole a/an/the, U4 this/that+plural, U5 have got+familie, U6 numere/varsta, U7 ora/prepozitii timp, U8 present simple I/you/we+rutina, U9 pers.III+WH, U10 there is/are+casa, U11 like+mancare+some/any, U12 cumparaturi (recap).\n\nCriterii de iesire A1 (de respectat in testul final, TOATE): (1) Scris/gramatica >=80% la test integrat (~60 itemi, toate unitatile); (2) Vocabular: >=80% din ~600 cuvinte (SRS >=480 carduri stiute); (3) Vorbire task cu EVA: dialog de rutina min 10 replici, >=75% acuratete pe structurile A1; (4) Pronuntie: scor >=80 pe /θ ð/ si /w v/; distinge auditiv /iː ɪ/ si /æ e/ >=75%; (5) Ascultare: >=80% la 3 dialoguri scurte lente; (6) Descriptor CEFR A1 confirmat.\n\nProduce markdown (incepe cu '## Testele de nivel A1 (Checkpoints + Test final)'):\n- Checkpoint 1 (dupa U4), Checkpoint 2 (dupa U7), Checkpoint 3 (dupa U10): scope, ~10-15 itemi structurati fiecare (cu raspunsuri), prag, + o sarcina orala scurta cu EVA + criteriu.\n- TEST FINAL A1: un BLUEPRINT de acoperire (cate itemi per unitate si per competenta, total ~60), un ESANTION de ~20 itemi structurati reprezentativi (cu raspunsuri), rubrica de vorbire + scriere (descriptori A1, praguri), logica de scorare cumulativa si maparea pe cele 6 criterii de iesire de mai sus, cu decizia de promovare la A2.\nTotul MASURABIL. Livreaza doar blocul markdown.`,
});

const sections = await parallel(
  specs.map((s) => () =>
    agent(s.prompt, { label: s.label, phase: 'Pipeline + Consolidare A1', agentType: 'general-purpose' })
      .then((t) => ({ label: s.label, md: t || '' }))
  )
)

return { sections }