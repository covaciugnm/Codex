export const meta = {
  name: 'eva-intro-bilingv',
  description: 'Genereaza introducere bilingva (RO persoana a II-a + EN + scop) pentru cele 12 unitati A1',
  phases: [{ title: 'Intro bilingv', detail: '12 unitati' }],
}
phase('Intro bilingv')

const DIR = "Z:\\02. EVA - Learn English with EVA\\11. Prototip EVA (App)\\content\\units\\"
const CODES = ['a1-u01','a1-u02','a1-u03','a1-u04','a1-u05','a1-u06','a1-u07','a1-u08','a1-u09','a1-u10','a1-u11','a1-u12']

const SCHEMA = {
  type: 'object',
  properties: {
    code: { type: 'string' },
    intro: {
      type: 'object',
      properties: {
        ro: { type: 'string', description: 'Adresare DIRECTA la persoana a II-a (tu). 1-2 propozitii: ce vei invata + DE CE iti foloseste in viata reala. Cald, simplu.' },
        en: { type: 'string', description: 'Aceeasi idee in engleza foarte simpla (A1), pers. a II-a (you).' },
        goals: {
          type: 'array',
          description: '3-5 obiective, reformulate la persoana a II-a (tu), scurte si concrete',
          items: {
            type: 'object',
            properties: {
              ro: { type: 'string', description: 'ex: "sa te prezinti (spui cum te cheama)"' },
              en: { type: 'string', description: 'engleza A1 simpla, ex: "introduce yourself (say your name)"' },
            },
            required: ['ro', 'en'],
          },
        },
      },
      required: ['ro', 'en', 'goals'],
    },
  },
  required: ['code', 'intro'],
}

const jobs = CODES.map((code) => () =>
  agent(
    `Citeste fisierul JSON al unitatii: "${DIR}${code}.json". Uita-te la campurile title, titleRo, objectives (canDo).\n\n` +
    `Genereaza un obiect "intro" BILINGV pentru ecranul de start al lectiei intr-o aplicatie de invatat engleza pentru un ADULT roman incepator (A1).\n` +
    `REGULI:\n` +
    `- Adresare DIRECTA, la persoana a II-a ("tu"): NU "cursantul poate", ci "vei invata sa...", "vei putea sa...".\n` +
    `- "ro" si "en": 1-2 propozitii scurte = ce inveti + DE CE iti foloseste in viata reala (ex. sa te descurci intr-o calatorie / la magazin / cand cunosti pe cineva).\n` +
    `- "goals": 3-5 obiective scurte, concrete, la persoana a II-a, derivate din objectives.canDo. RO natural; EN foarte simplu (A1).\n` +
    `- Ton cald, prietenos, incurajator. code = "${code.toUpperCase().replace('A1-U','A1-U')}" (ex A1-U01 -> "A1-U01").\n` +
    `Returneaza DOAR obiectul JSON {code, intro}.`,
    { label: code, phase: 'Intro bilingv', schema: SCHEMA, effort: 'low' }
  ).then((r) => r)
)

const results = await parallel(jobs)
return { results: results.filter(Boolean) }