export const meta = {
  name: 'eva-curriculum-architecture',
  description: 'Cuprins/syllabus map pe 6 niveluri CEFR (A1-C2) + design test de validare A2-C2, pt curriculumul aplicatiei EVA (English Voice Assistant)',
  phases: [
    { title: 'Cuprins pe niveluri', detail: '6 agenti (A1-C2) + 1 agent test de validare' },
  ],
}

phase('Cuprins pe niveluri')

const CONTEXT = `PROIECT: "EVA — English Voice Assistant", o aplicatie chat-first (stil WhatsApp/Messenger) prin care un VORBITOR DE ROMANA invata engleza vorbind si scriind cu EVA (tutore AI). Curriculum pe 6 niveluri CEFR A1-C2. Alimentata de o biblioteca OER existenta: manuale de engleza (State Dept, OER), ~16.000 propozitii paralele RO-EN (Tatoeba), audio MP3, gramatici, dictionar RO-EN.`

const FLOW = `FLUXUL DE INVATARE AL FIECAREI UNITATI (obligatoriu, in 3 faze):
- FAZA 1 — PARTEA SCRISA (input & studiu): text/dialog de citit, explicatie de gramatica IN ROMANA (care se stinge la niveluri mari), prezentare vocabular, exercitii scrise, intelegere.
- FAZA 2 — PIPELINE (conversatie & voce cu EVA): ascultare, conversatie ghidata -> libera cu EVA pe tema unitatii, focus de PRONUNTIE specific romanilor (th, v/w, i:/ɪ, æ/e, accent), shadowing.
- FAZA 3 — CONSOLIDARE & EVALUARE (restul): carduri SRS (din vocabularul/propozitiile unitatii), scenariu task-based din viata reala, auto-verificare, test de unitate cu criterii MASURABILE.`

const TEMPLATE = `SABLON DE UNITATE (fiecare unitate din cuprins trebuie descrisa cu aceste campuri, TOTUL MASURABIL):
1. Cod + Titlu unitate + Tema
2. Functii comunicative (formulate ca descriptori CAN-DO)
3. Gramatica (punctele-cheie)
4. Vocabular (tema + numar tinta de cuvinte)
5. Fonetica (focus specific pt romani)
6. Obiectiv/Rezultat MASURABIL (criteriu observabil + prag: ex. "produce 6 propozitii corecte la present simple", "scor pronuntie >=80 pe cuvinte cu /θ/", ">=80% la testul de unitate", descriptor CEFR atins)`

const FORMAT = `FORMAT DE IESIRE (markdown curat, gata de inclus intr-un document):
## Nivel <X> — <denumire> (<descriptor CEFR scurt>)
**Obiectiv global de nivel (CAN-DO):** ...
**Prag de intrare / iesire:** vocabular cumulat, arii gramaticale.
**Rezumat test de validare la intrare:** (doar pt A2-C2) ce trebuie sa demonstreze.
### Module si Unitati (CUPRINS)
Grupeaza in 2-3 Module. Da un TABEL cu 10-12 unitati, coloane: # | Unitate (tema) | Functii comunicative | Gramatica | Vocabular (tema / nr) | Fonetica RO | Obiectiv masurabil.
**Checkpoint-uri si Test final de nivel:** criterii masurabile pt promovare la nivelul urmator.
**Resurse din biblioteca EVA:** ce manuale/audio/propozitii alimenteaza nivelul.`

const levels = [
  { lvl: 'A1', label: 'Beginner', guide: 'Gramatica: verbul to be, present simple, articole a/an/the (drill contrastiv RO!), plural, this/that, can, have got, prepozitii de loc/timp, intrebari WH. Vocabular ~500-750. Teme: salut, informatii personale, familie, numere, ora/data, mancare, casa, rutina zilnica, cumparaturi simple.' },
  { lvl: 'A2', label: 'Elementary', guide: 'Gramatica: past simple (regulate/neregulate), present continuous, comparativ/superlativ, going to, adverbe de frecventa, countable/uncountable + some/any/much/many. Vocabular cumulat ~1500-2500. Teme: cumparaturi, calatorii, munca, sanatate, indicatii, evenimente trecute, planuri.' },
  { lvl: 'B1', label: 'Intermediate', guide: 'Gramatica: present perfect vs past simple, past continuous, will/first conditional, modale (should/must/have to), propozitii relative, discurs indirect (baza), introducere phrasal verbs. Vocabular cumulat ~2750-3250. Teme: experiente, povestiri, vise/sperante, opinii, situatii de calatorie.' },
  { lvl: 'B2', label: 'Upper-Intermediate', guide: 'Gramatica: present perfect continuous, second/third conditional, pasiv, mixed conditionals, phrasal verbs extinse, conectori de discurs, used to/would. Vocabular cumulat ~4000-5000. Teme: subiecte abstracte, media/film, argumentare, munca, mediu.' },
  { lvl: 'C1', label: 'Advanced', guide: 'Gramatica: inversiune, cleft sentences, conditionale avansate, structuri emfatice, colocatii, idiomuri, nuante de registru. Teme: academic, profesional, argumentare complexa, texte lungi/pretentioase.' },
  { lvl: 'C2', label: 'Proficiency', guide: 'Gramatica/stil: stapanire cvasi-nativa, subtilitati de conotatie, stilistica, umor/ironie, registre variate, idiomatic complet. Teme: orice subiect, precizie si naturalizare la nivel de nativ educat.' },
]

const specs = levels.map((L) => ({
  label: `nivel-${L.lvl}`,
  prompt: `${CONTEXT}\n\n${FLOW}\n\n${TEMPLATE}\n\n${FORMAT}\n\nSARCINA: Scrie CUPRINSUL (syllabus map) complet pentru NIVELUL ${L.lvl} (${L.label}). Ancoreaza-te pe scara globala CEFR (British Council reproduce descriptorii CEFR). Repere de continut pt acest nivel: ${L.guide}\nDa 10-12 unitati grupate in module, fiecare cu toate campurile din tabel, obiective MASURABILE, si progresie logica (spirala: reia si extinde). Pastreaza un ton prietenos, orientat pe conversatie. Livreaza DOAR blocul markdown in formatul cerut, nimic altceva.`,
}))

specs.push({
  label: 'test-validare',
  prompt: `${CONTEXT}\n\nSARCINA: Proiecteaza modelul de TEST DE VALIDARE / PLASARE pe nivel pentru aplicatia EVA, chat-first. Scop: un cursant care spune ca e la nivelul X (A2-C2, adica nivelurile 2-6) da un test care VALIDEAZA ca e la acel nivel si il lasa sa inceapa acel nivel; daca nu, e rutat la nivelul potrivit. A1 = intrare directa (incepator absolut, fara test).\n\nDescrie MASURABIL:\n1. Structura testului adaptiv, pe sectiuni: (a) test de marime a vocabularului yes/no (cuvinte reale vs pseudo-cuvinte) -> estimare banda CEFR; (b) use of English adaptiv (MCQ calibrate pe nivel, gramatica+vocabular); (c) intelegere dupa ascultare (clipuri scurte + intrebari); (d) intelegere text (citire); (e) validare PRODUCTIVA: vorbire cu EVA (scorata de LLM pe rubrica CEFR) + scriere scurta (scorata de LLM). \n2. Cum se administreaza chat-first (conversational, prietenos, ~15-20 min), cu adaptivitate (item response / oprire timpurie).\n3. SCORARE si MAPARE pe CEFR: cum se combina sectiunile, pragurile de promovare/validare per nivel tinta, ce inseamna "validat sa inceapa nivelul X".\n4. Rubrica de vorbire/scriere (criterii CEFR: range, accuracy, fluency, coherence, interaction, pronunciation) cu descriptori pe niveluri.\n5. Re-testare / checkpoint-uri periodice si test final de nivel (criterii de promovare).\nLivreaza markdown curat, structurat, gata de inclus intr-un document (titlu de sectiune: "## Testele de validare si plasare (A2-C2)").`,
})

const sections = await parallel(
  specs.map((s) => () =>
    agent(s.prompt, { label: s.label, phase: 'Cuprins pe niveluri' }).then((t) => ({ label: s.label, md: t || '' }))
  )
)

return { sections }