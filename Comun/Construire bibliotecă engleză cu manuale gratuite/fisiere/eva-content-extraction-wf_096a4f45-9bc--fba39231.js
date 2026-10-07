export const meta = {
  name: 'eva-content-extraction',
  description: 'Extrage cele 12 unitati A1 (Strat 1 + Strat 2-3) si testele de nivel in JSON structurat pentru aplicatia EVA',
  phases: [
    { title: 'Extractie continut', detail: '12 agenti/unitate + 1 teste de nivel' },
  ],
}

phase('Extractie continut')

const S1 = "Z:\\02. EVA - Learn English with EVA\\10. Curriculum EVA (A1-C2)\\Nivel A1 - Componenta scrisa\\"
const S23 = "Z:\\02. EVA - Learn English with EVA\\10. Curriculum EVA (A1-C2)\\Nivel A1 - Pipeline si Consolidare (Straturile 2-3)\\"

const UNITS = [
  {n:1,  title:"Hello & Goodbye",            f1:"A1-U01 - Hello and Goodbye.md",            f2:"A1-U01 - Hello and Goodbye (Straturile 2-3).md"},
  {n:2,  title:"Who are you?",               f1:"A1-U02 - Who are you.md",                  f2:"A1-U02 - Who are you (Straturile 2-3).md"},
  {n:3,  title:"A, an or the?",              f1:"A1-U03 - A, an or the.md",                 f2:"A1-U03 - A, an or the (Straturile 2-3).md"},
  {n:4,  title:"This, that & many things",   f1:"A1-U04 - This, that and many things.md",   f2:"A1-U04 - This, that and many things (Straturile 2-3).md"},
  {n:5,  title:"My family",                  f1:"A1-U05 - My family.md",                    f2:"A1-U05 - My family (Straturile 2-3).md"},
  {n:6,  title:"Numbers & Age",              f1:"A1-U06 - Numbers and Age.md",              f2:"A1-U06 - Numbers and Age (Straturile 2-3).md"},
  {n:7,  title:"What time is it?",           f1:"A1-U07 - What time is it.md",              f2:"A1-U07 - What time is it (Straturile 2-3).md"},
  {n:8,  title:"My daily routine",           f1:"A1-U08 - My daily routine.md",             f2:"A1-U08 - My daily routine (Straturile 2-3).md"},
  {n:9,  title:"He works, she plays",        f1:"A1-U09 - He works, she plays.md",          f2:"A1-U09 - He works, she plays (Straturile 2-3).md"},
  {n:10, title:"My house",                   f1:"A1-U10 - My house.md",                     f2:"A1-U10 - My house (Straturile 2-3).md"},
  {n:11, title:"Food & drink",               f1:"A1-U11 - Food and drink.md",               f2:"A1-U11 - Food and drink (Straturile 2-3).md"},
  {n:12, title:"At the shop",                f1:"A1-U12 - At the shop.md",                  f2:"A1-U12 - At the shop (Straturile 2-3).md"},
]

const UNIT_SCHEMA = {
  type: 'object',
  properties: {
    code: { type: 'string', description: 'ex: A1-U01' },
    title: { type: 'string' },
    titleRo: { type: 'string', description: 'tema in romana' },
    module: { type: 'integer' },
    durationMin: { type: 'integer' },
    objectives: { type: 'array', items: { type: 'object', properties: { canDo: {type:'string'}, criterion: {type:'string'} }, required: ['canDo','criterion'] } },
    grammar: { type: 'array', items: { type: 'string' } },
    functions: { type: 'array', items: { type: 'string' } },
    vocab: { type: 'array', items: { type: 'object', properties: { en: {type:'string'}, ipa: {type:'string'}, ro: {type:'string'} }, required: ['en','ro'] } },
    dialogue: { type: 'object', properties: { lines: { type: 'array', items: { type: 'object', properties: { speaker: {type:'string'}, text: {type:'string'} }, required: ['speaker','text'] } }, gloss: { type: 'array', items: { type: 'object', properties: { en: {type:'string'}, ro: {type:'string'} }, required: ['en','ro'] } } }, required: ['lines'] },
    grammarNoteRo: { type: 'string', description: 'nota de gramatica in romana, markdown, VERBATIM din sectiunea 4' },
    exercisesMd: { type: 'string', description: 'exercitiile scrise + raspunsuri, markdown verbatim din sectiunea 5' },
    comprehension: { type: 'array', items: { type: 'object', properties: { q: {type:'string'}, a: {type:'string'} }, required: ['q','a'] } },
    systemPrompt: { type: 'string', description: 'system promptul EVA VERBATIM din Stratul 2 sectiunea A (fara gardurile de cod)' },
    flow: { type: 'object', properties: {
      guided: { type: 'array', items: { type: 'object', properties: { eva: {type:'string'}, model: {type:'string'}, target: {type:'string'} }, required: ['eva'] } },
      semiGuided: { type: 'array', items: { type: 'object', properties: { eva: {type:'string'}, hint: {type:'string'} }, required: ['eva'] } },
      free: { type: 'object', properties: { scenario: {type:'string'}, objective: {type:'string'} }, required: ['scenario'] },
      branchingMd: { type: 'string' },
    }, required: ['guided','semiGuided','free'] },
    listening: { type: 'object', properties: { script: { type: 'string', description: 'scriptul audio CURAT pt TTS: doar replici "Speaker: text" pe linii, fara adnotari' }, settings: { type: 'string' }, items: { type: 'array', items: { type: 'object', properties: { q: {type:'string'}, a: {type:'string'} }, required: ['q','a'] } } }, required: ['script','items'] },
    pronunciation: { type: 'object', properties: {
      targets: { type: 'array', items: { type: 'object', properties: { sound: {type:'string'}, issue: {type:'string'}, words: { type: 'array', items: {type:'string'} }, tip: {type:'string'} }, required: ['sound','words'] } },
      drillSentences: { type: 'array', items: { type: 'string' } },
      shadowing: { type: 'array', items: { type: 'string' } },
      threshold: { type: 'integer' },
    }, required: ['targets','drillSentences','shadowing'] },
    srs: { type: 'array', items: { type: 'object', properties: { front: {type:'string'}, back: {type:'string'}, type: { type: 'string', enum: ['en-ro','ro-en','cloze'] }, note: {type:'string'} }, required: ['front','back','type'] } },
    scenario: { type: 'object', properties: { situation: {type:'string'}, objective: {type:'string'}, criteriaMd: {type:'string'}, rubricMd: {type:'string'} }, required: ['situation','objective'] },
    test: { type: 'object', properties: {
      items: { type: 'array', items: { type: 'object', properties: {
        type: { type: 'string', enum: ['mcq','cloze','translate','reorder','short'] },
        question: { type: 'string' },
        options: { type: 'array', items: {type:'string'} },
        answer: { type: 'string', description: 'raspunsul corect; alternative acceptate separate cu " | "' },
        points: { type: 'integer' },
      }, required: ['type','question','answer','points'] } },
      passThreshold: { type: 'integer', description: 'procent, ex 80' },
      productionRubricMd: { type: 'string' },
    }, required: ['items','passThreshold'] },
  },
  required: ['code','title','titleRo','module','objectives','vocab','dialogue','grammarNoteRo','exercisesMd','comprehension','systemPrompt','flow','listening','pronunciation','srs','scenario','test'],
}

const TESTS_SCHEMA = {
  type: 'object',
  properties: {
    checkpoints: { type: 'array', items: { type: 'object', properties: {
      afterUnit: { type: 'integer' },
      scope: { type: 'string' },
      items: { type: 'array', items: { type: 'object', properties: {
        type: { type: 'string', enum: ['mcq','cloze','translate','reorder','short'] },
        question: { type: 'string' }, options: { type: 'array', items: {type:'string'} },
        answer: { type: 'string' }, points: { type: 'integer' },
      }, required: ['type','question','answer','points'] } },
      passThreshold: { type: 'integer' },
      oralTaskMd: { type: 'string' },
    }, required: ['afterUnit','scope','items','passThreshold'] } },
    finalTest: { type: 'object', properties: {
      blueprintMd: { type: 'string' },
      items: { type: 'array', items: { type: 'object', properties: {
        type: { type: 'string', enum: ['mcq','cloze','translate','reorder','short'] },
        question: { type: 'string' }, options: { type: 'array', items: {type:'string'} },
        answer: { type: 'string' }, points: { type: 'integer' },
      }, required: ['type','question','answer','points'] } },
      passThreshold: { type: 'integer' },
      gatesMd: { type: 'string', description: 'cele 6 porti conjunctive de promovare' },
      rubricsMd: { type: 'string' },
    }, required: ['items','passThreshold','gatesMd'] },
  },
  required: ['checkpoints','finalTest'],
}

const RULES = `REGULI DE EXTRACTIE:
- Citeste AMBELE fisiere markdown indicate (Read tool), apoi returneaza JSON-ul structurat.
- Continutul EN/RO se preia FIDEL (verbatim unde e ceruta) — nu rescrie, nu rezuma, nu inventa.
- systemPrompt: textul complet al system promptului EVA din Stratul 2 sectiunea A, fara \`\`\`-uri.
- listening.script: transforma scriptul audio in linii simple "EVA: text" / "Tom: text" (fara [VOICE A], fara indicatii de regie — acelea merg in "settings").
- test.items: converteste itemii structurati din Stratul 3 sectiunea G in tipurile permise. "match"/potrivire → transforma in mcq sau cloze per pereche. Alternative de raspuns acceptate → separa cu " | ". Punctele: intregi (default 1).
- reorder: question = cuvintele amestecate separate cu " / ", answer = propozitia corecta.
- srs: preia cardurile din Stratul 3 sectiunea E (15-20). type: en-ro (front EN, back RO), ro-en (front RO, back EN) sau cloze.
- vocab: TOATE cuvintele din tabelul de vocabular al unitatii (Strat 1 sectiunea 2).
- Texte markdown (grammarNoteRo, exercisesMd, branchingMd etc.): pastreaza formatarea markdown.`

const jobs = UNITS.map((u) => ({
  label: `extract-U${String(u.n).padStart(2,'0')}`,
  prompt: `Extrage continutul unitatii A1-U${u.n} ("${u.title}") in JSON pentru aplicatia EVA (English Voice Assistant).\n\nFISIERE DE CITIT:\n1. "${S1}${u.f1}"  (Stratul 1 — componenta scrisa)\n2. "${S23}${u.f2}"  (Straturile 2-3 — pipeline + consolidare)\n\n${RULES}\n\ncode = "A1-U${String(u.n).padStart(2,'0')}". Returneaza DOAR obiectul JSON structurat.`,
  schema: UNIT_SCHEMA,
}))

jobs.push({
  label: 'extract-tests',
  prompt: `Extrage testele de nivel A1 in JSON pentru aplicatia EVA.\n\nFISIER DE CITIT:\n"${S23}A1 - Teste de nivel (Checkpoints + Test final).md"\n\n${RULES}\n\nExtrage cele 3 checkpoint-uri (dupa U4, U7, U10) cu itemii lor structurati + testul final A1 (esantionul de itemi + blueprint + cele 6 porti + rubrici). Returneaza DOAR obiectul JSON structurat.`,
  schema: TESTS_SCHEMA,
})

const results = await parallel(
  jobs.map((j) => () =>
    agent(j.prompt, { label: j.label, phase: 'Extractie continut', schema: j.schema, effort: 'low' })
      .then((r) => ({ label: j.label, data: r }))
  )
)

return { results }