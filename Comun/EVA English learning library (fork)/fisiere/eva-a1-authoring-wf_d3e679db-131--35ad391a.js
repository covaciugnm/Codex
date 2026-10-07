export const meta = {
  name: 'eva-a1-authoring',
  description: 'Autorare componenta scrisa (Stratul 1) pentru toate cele 12 unitati ale nivelului A1 EVA',
  phases: [
    { title: 'Autorare unitati A1', detail: '12 agenti, cate o unitate completa fiecare' },
  ],
}

phase('Autorare unitati A1')

const UNITS = [
  {n:1, mod:1, title:"Hello & Goodbye", theme:"salut, alfabet, spelling", func:"a saluta si a-si lua ramas-bun; a spune si a silabisi (spell) numele; a cere repetarea", gram:"pronume personale subiect (I/you/he/she/it/we/they); 'My name is...'; imperative de clasa (Listen, Repeat, Look)", vocab:"formule de salut (hello, hi, good morning/afternoon/evening, goodbye, bye, see you), alfabetul englez + spelling, politeturi de baza (please, thank you, sorry)", vN:40, phon:"/h/ aspirat in hello, hi, how (romanii il 'inghit'); intonatie de salut", obj:"silabiseste corect propriul nume si 3 cuvinte dictate (>=90% litere) si saluta/isi ia ramas-bun in >=8 schimburi de chat fara eroare"},
  {n:2, mod:1, title:"Who are you?", theme:"informatii personale, tari, nationalitati", func:"a se prezenta si a cere identitatea altcuiva; a spune de unde esti si ce nationalitate ai", gram:"verbul to be — afirmativ/negativ/interogativ (am/is/are; forme scurte I'm, you're, he's; isn't/aren't; Are you...? Yes I am/No I'm not)", vocab:"tari, nationalitati, intrebari personale de baza (What's your name? Where are you from? How are you?)", vN:55, phon:"/iː/ vs /ɪ/ in he/she/is/it/this (ship vs sheep intro); weak forms ale lui is/are", obj:"produce >=6 propozitii corecte cu to be (min 1 negativa + 1 interogativa) si completeaza o fisa de prezentare in chat cu >=80% acuratete"},
  {n:3, mod:1, title:"A, an or the?", theme:"obiecte, articole (drill contrastiv RO)", func:"a numi obiecte din jur si a spune 'este un/o...'; a distinge prima mentionare vs. cunoscut", gram:"a/an (vocala/consoana) vs the vs articol zero — CONTRAST EXPLICIT cu romana (articol hotarat enclitic -ul/-a; romanii omit a/an: 'I am student')", vocab:"obiecte de zi cu zi (pen, book, bag, table, chair, phone, key, door), culori", vN:35, phon:"schwa /ə/ in a; the = /ðə/ inainte de consoana vs /ðiː/ inainte de vocala, cu /ð/ corect (nu 'za/de')", obj:"la un test de 20 de spatii cu a/an/the/— obtine >=80% corect si explica o regula de contrast RO-EN"},
  {n:4, mod:1, title:"This, that & many things", theme:"demonstrative, plural", func:"a indica obiecte (acesta/acela) si a spune cate sunt; a forma pluralul", gram:"this/that/these/those; plural regulat (-s/-es) + neregulate frecvente (man->men, child->children, woman->women, foot->feet)", vocab:"extindere obiecte + scoala/casa, cantitati mici", vN:50, phon:"/ð/ in this/that/these/those; terminatii de plural /s/–/z/–/ɪz/ (books/pens/boxes)", obj:"transforma corect >=10 substantive la plural (inclusiv 2 neregulate) si clasifica terminatia fonetica /s z ɪz/ cu >=80% acuratete"},
  {n:5, mod:2, title:"My family", theme:"familie, posesie", func:"a prezenta membrii familiei si a spune ce/pe cine ai; a exprima posesia", gram:"have got / has got (afirmativ/negativ/interogativ: I've got, she hasn't got, Have you got...?); adjective posesive (my/your/his/her/our/their)", vocab:"membri ai familiei (mother, father, brother, sister, son, daughter, grandmother...), stare civila, animale de companie", vN:55, phon:"/ð/ in mother, father, brother, the; contrast cu /θ/", obj:"descrie propria familie in >=6 propozitii cu have got + posesive (min 4 corecte gramatical)"},
  {n:6, mod:2, title:"Numbers & Age", theme:"numere, varsta, preturi intro", func:"a numara, a spune si intreba varsta, a citi numere de telefon si preturi simple", gram:"numere cardinale 0–100; How old...? — I'm ... (years old); How many...?", vocab:"numere 0–100, varsta, telefon, preturi de baza (pound/euro/dollar)", vN:60, phon:"/θ/ in three, thirteen, thirty; contrast de accent thirTEEN vs THIRty", obj:"asculta si scrie corect >=8/10 numere dictate si distinge -teen/-ty prin accent cu >=80% acuratete"},
  {n:7, mod:2, title:"What time is it?", theme:"ora, zile, luni, data", func:"a spune si cere ora, ziua, luna si data; a vorbi despre program", gram:"prepozitii de timp at/on/in (at 7 o'clock, on Monday, in July); What time...? When...?", vocab:"ore (o'clock, half past, quarter past/to), zilele saptamanii, luni, momente ale zilei", vN:65, phon:"/θ/ in Thursday, month, three o'clock; /z/ final in days; reducerea vocalelor neaccentuate", obj:"spune corect >=8 ore diferite si completeaza un mini-orar cu prepozitiile at/on/in corecte in >=80% din cazuri"},
  {n:8, mod:3, title:"My daily routine", theme:"rutina zilnica (I/you/we)", func:"a descrie ce faci zilnic si cat de des; a vorbi despre programul tau", gram:"present simple (I/you/we/they) afirmativ/negativ (don't); adverbe de frecventa (always/usually/often/sometimes/never)", vocab:"verbe de rutina (get up, have breakfast, go to work, eat, sleep, watch TV...), parti ale zilei", vN:60, phon:"/w/ vs /v/ in wake, work, watch vs very (romanii confunda!); /w/ labial", obj:"produce >=8 propozitii despre rutina proprie (min 2 negative + 2 cu adverb de frecventa) cu >=75% acuratete gramaticala"},
  {n:9, mod:3, title:"He works, she plays", theme:"persoana a III-a, intrebari WH", func:"a descrie rutina altcuiva; a pune intrebari despre ce, unde, cand, cine", gram:"present simple persoana a III-a -s/-es; does/doesn't; intrebari WH (what/where/when/who) cu do/does", vocab:"verbe extinse + profesii (teacher, doctor, driver, cook...), cuvinte de intrebare", vN:45, phon:"terminatia -s la verbe: /s/–/z/–/ɪz/ (works/plays/watches); auxiliar does redus", obj:"adauga corect -s si terminatia fonetica la >=8/10 verbe si formeaza >=5 intrebari WH corecte cu do/does"},
  {n:10, mod:3, title:"My house", theme:"casa, camere, mobilier", func:"a descrie casa ta si a spune ce se afla unde", gram:"There is / There are (+ neg./interog. Is there...? Are there any...?); prepozitii de loc (in/on/under/next to/behind/between)", vocab:"camere (kitchen, bathroom, bedroom, living room), mobilier, obiecte casnice", vN:60, phon:"/ð/ in there; /θ/ in bathroom, three rooms; forme slabe ale prepozitiilor", obj:"descrie o camera in >=6 propozitii cu there is/are + >=4 prepozitii de loc corecte (>=80% potrivire pe imagine)"},
  {n:11, mod:3, title:"Food & drink", theme:"mancare, preferinte", func:"a numi alimente, a spune ce iti place/nu-ti place si ce poti sa faci", gram:"like/don't like + noun/-ing; countable vs uncountable (some/any) — introductiv; can (abilitate)", vocab:"alimente, bauturi, mese (breakfast/lunch/dinner), verbe 'a putea face' (cook, swim, drive)", vN:65, phon:"/æ/ vs /e/ in apple/cat vs bread/egg (romanii aud 'e' peste tot); /ɔː/ in water", obj:"exprima >=6 preferinte alimentare (I like / I don't like) si clasifica >=8 alimente in countable/uncountable cu >=75% acuratete"},
  {n:12, mod:3, title:"At the shop", theme:"cumparaturi simple (recapitulare)", func:"a cumpara lucruri simple: a cere un produs, a intreba pretul, a plati si a multumi", gram:"Can I have...? How much is/are...?; recapitulare integrata a/an/the, plural, numere, present simple", vocab:"magazin, produse, bani, formule de tranzactie (Here you are, How much, That's...)", vN:60, phon:"recapitulare /θ/ la preturi (three, thirty); /aʊ/ in how much; intonatie politicoasa", obj:"joaca un rol 'cumparaturi' cu EVA (min 8 replici), cere >=3 produse, intreaba corect pretul si incheie tranzactia cu >=80% inteligibilitate"},
]

const PROGRESSION = UNITS.map(u => `U${u.n} ${u.title}: ${u.gram}`).join('\n')

const CONTEXT = `PROIECT: EVA — English Voice Assistant, aplicatie chat-first (stil WhatsApp/Messenger) prin care un VORBITOR DE ROMANA invata engleza vorbind/scriind cu EVA (tutore AI prietenos, rabdator).
NIVEL: A1 (Beginner, CEFR). Obiectiv global A1: cursantul poate sa se prezinte, sa dea/ceara date personale simple, sa faca tranzactii cotidiene foarte simple (salut, ora, cumparaturi, mancare), in propozitii scurte, cu sprijin.
CONTROL DE NIVEL (obligatoriu): foloseste DOAR vocabular si structuri A1, si DOAR gramatica introdusa pana la unitatea curenta inclusiv (nu folosi timpuri/structuri din unitati viitoare). Propozitii scurte, frecvente. Sprijin/explicatii in ROMANA (A1 = sprijin maxim in romana).
PROGRESIA GRAMATICALA A NIVELULUI (ca sa stii ce e disponibil inainte/dupa):
${PROGRESSION}
RESURSE (foloseste-le ca ancora, nu inventa continut nefondat): manuale OER din biblioteca EVA (Everyday Conversations, A Digital Workbook for Beginning ESOL, BC Reads) pt texte/dialoguri; ~16.000 propozitii paralele RO-EN (Tatoeba) pt banca SRS si drill-uri; audio MP3 pt ascultare/pronuntie; gramatici RO-EN pt notele contrastive; dictionar RO-EN pt liste de vocabular.`

const FORMAT = `FORMAT DE IESIRE (markdown curat, in ROMANA pentru instructiuni, ENGLEZA pentru continutul-tinta). Incepe EXACT cu titlul si respecta sectiunile:

### A1-U<n> — <Titlu EN> · Tema: <tema RO>
**Modul <m> · Durata ~25 min · Prerechizite: <unitati anterioare sau 'niciuna'>**

#### ① Obiective (CAN-DO, masurabile)
3–5 obiective, fiecare: "La final, cursantul poate <can-do>." + **Criteriu:** <observabil + prag numeric>.

#### ② Continut lingvistic
- **Gramatica:** punctele-cheie.
- **Vocabular-tinta (<N> cuvinte):** un TABEL cu coloane | Engleza | Pronuntie (IPA simpla) | Romana | — listeaza efectiv ~<N> cuvinte reale, tematice.
- **Functii comunicative:** actele de vorbire.
- **Fonetica (focus romani):** sunetele-tinta + 4–6 cuvinte-exemplu.

#### ③ Text / Dialog (Faza 1 — de citit)
Un dialog SAU text SCURT, autentic A1 (60–140 cuvinte), cu EVA ca personaj unde e firesc. Sub text, o mica glosa RO pentru 3–5 expresii-cheie.

#### ④ Nota de gramatica (in romana)
Explicatie clara IN ROMANA, CONTRASTIVA cu romana (ce e diferit), cu 3–5 exemple EN + un mini-tabel de forme. Semnaleaza greseala tipica a romanilor.

#### ⑤ Exercitii scrise (cu raspunsuri)
6–8 exercitii VARIATE (completare de spatii, potrivire, ordonare cuvinte, transformare, alegere multipla, traducere RO->EN) cu enunturi clare. Apoi **Raspunsuri:** cheia completa.

#### ⑥ Verificare de intelegere
3–5 intrebari despre text/dialog + **Raspunsuri**.

#### ⑦ Rezultate masurabile (Definition of Done) + Evaluare
- Praguri numerice (intelegere %, productie N, pronuntie scor, vocabular retentie %).
- Itemi de test (scurt) + **barem**.

#### ⑧ Sarcina comunicativa finala cu EVA (task)
Descrierea sarcinii (situatie reala) + o **schita de dialog EVA** de 8–12 replici (cu glose RO ocazionale), care demonstreaza obiectivele.

#### ⑨ Banca de propozitii pentru SRS (12–15 perechi EN | RO)
Un tabel EN | RO cu propozitii scurte din/pentru unitate (stil Tatoeba), pentru repetitie spatiata.

#### Resurse din biblioteca EVA
Ce anume alimenteaza unitatea (manual/tema, propozitii, audio).

Livreaza DOAR acest bloc markdown, complet, nimic in plus.`

const sections = await parallel(
  UNITS.map((u) => () => {
    const spec = `UNITATEA DE AUTORAT: A1-U${u.n} — "${u.title}" (Modul ${u.mod})
- Tema: ${u.theme}
- Functii comunicative: ${u.func}
- Gramatica: ${u.gram}
- Vocabular: ${u.vocab} (tinta ~${u.vN} cuvinte)
- Fonetica (focus RO): ${u.phon}
- Obiectiv masurabil (din cuprins): ${u.obj}
- Prerechizite: ${u.n === 1 ? 'niciuna (unitate de start)' : 'unitatile A1-U1 ... A1-U' + (u.n-1)}`
    return agent(`${CONTEXT}\n\n${spec}\n\n${FORMAT}`, { label: `A1-U${String(u.n).padStart(2,'0')}`, phase: 'Autorare unitati A1' })
      .then((t) => ({ n: u.n, md: t || '' }))
  })
)

return { sections }