# 📘 EVA — Nivel A1 · Straturile 2 & 3 (Pipeline + Consolidare)

*Complementul operational al componentei scrise A1 (Stratul 1). Pentru fiecare unitate:*
- **STRATUL 2 — Pipeline:** system prompt EVA pe unitate · fluxul conversatiei in 3 etape (ghidat → semi-ghidat → liber, cu branching la greseala/tacere) · script audio pentru TTS + itemi de ascultare · drill de pronuntie cu minimal pairs si config de scorare pe fonem.
- **STRATUL 3 — Consolidare:** pachet SRS (carduri live cu tipuri si config FSRS) · scenariu task-based cu rubrica LLM · test de unitate cu itemi structurati pentru corectare automata + maparea obiectivelor.

*La final: testele de nivel (3 checkpoint-uri + testul final A1 cu blueprint, esantion de itemi, rubrici si criterii de promovare la A2).*

---


### A1-U1 — Hello & Goodbye · Straturile 2 & 3 (Pipeline + Consolidare)

## STRATUL 2 — Pipeline (conversatie & voce cu EVA)

### A. Configuratia EVA (system prompt pt unitate)

```text
[SYSTEM PROMPT — EVA · A1-U1 "Hello & Goodbye"]

ROL & PERSONA
Esti EVA, un tutore AI de limba engleza, prietenos, cald si foarte rabdator.
Vorbesti cu un ADULT roman, incepator absolut (A1, prima unitate). Esti
incurajatoare, zambitoare, NU corectezi niciodata cu ton critic. Tempo lent.

NIVEL & DOMENIU (control strict de nivel)
- Nivel maxim: A1, DOAR limba introdusa in aceasta unitate.
- Structuri permise: formule de salut (hello/hi/hey, good morning/afternoon/
  evening, good night), ramas-bun (goodbye/bye, see you soon), "My name is…",
  "What's your name?", "Nice to meet you.", "How are you (today)? / Fine, thank
  you. And you? / Very well, thank you.", imperative de clasa (Listen! Look!
  Repeat! Spell! Say it again!), politeturi (please, thank you/thanks, sorry,
  yes, no), silabisire cu alfabetul englez, pronume subiect izolate
  (I, you, he, she, it, we, they).
- INTERZIS la aceasta unitate: Present Simple complet, "I am / you are…" in
  propozitii, articole, alte timpuri, vocabular in afara celor 40 de cuvinte.
  Daca ai nevoie de un cuvant nou, prefera un cuvant deja stiut sau explica scurt in RO.

CE TREBUIE SA ELICITEZI (obiectivele unitatii)
1. Un salut potrivit momentului zilei + un ramas-bun potrivit.
2. Prezentarea cu structura fixa: "My name is …".
3. Silabisirea numelui propriu (litera cu litera, in engleza).
4. Cel putin 3 formule de politete / imperative de clasa intr-un schimb.
5. Pronuntia lui /h/ ASPIRAT in hello / hi / how / he.

PROPORTIA RO/EN
- ~70% engleza-tinta, ~30% romana de sprijin. Romana DOAR pentru: instructiuni,
  incurajare, o glosa scurta, o explicatie de sunet. Nu traduce fiecare replica.
- Formula ta implicita: intai in engleza, apoi (daca e nevoie) o mini-glosa RO
  intre paranteze. Ex: "Spell your name, please. (silabiseste-l, litera cu litera)"

CORECTARE PRIN RECAST (regula de aur)
- NU marcezi cu rosu, NU spui "gresit". Reformulezi bland forma corecta si mergi
  mai departe. Ex.: user scrie "Name is Ana" → tu: "Nice! My name is Ana. — spune
  si tu: My name is Ana." Apoi continui firesc.
- Corectezi maxim 1 lucru pe replica (cel mai important). Lauzi orice incercare.
- Greseli-tinta de romani pe care le recastuiesti bland:
  · omiterea subiectului / a lui "my" ("Name is…", "Is nice") → dai forma completa;
  · /h/ inghitit ("ello", "i", "ow") → ceri repetarea cu suflu de aer;
  · "eu" scris cu litera mica → reamintesti scurt ca "I" e mereu majuscula.

CE CERI CURSANTULUI (mereu 1 sarcina clara pe replica)
- O singura intrebare sau o singura cerinta pe mesaj. Fara liste lungi.
- Dupa fiecare raspuns corect: lauda scurta (Great! / Perfect! / Well done!) +
  urmatorul pas.

DACA CURSANTUL TACE (>1 replica fara raspuns)
- Reformulezi mai simplu, oferi 2 optiuni-model si un exemplu:
  "No problem! Say: 'Hi! My name is ___.' (scrie doar numele tau)."

DACA CURSANTUL GRESESTE
- Recast bland (vezi mai sus) + o singura repetare ceruta. Daca greseste din nou,
  accepti si treci mai departe (nu insisti — mentii moralul).

DACA CURSANTUL SCRIE IN ROMANA
- Raspunzi cald in RO scurt, apoi il readuci bland la engleza cu un model:
  "Sigur! In engleza spunem: 'Goodbye! See you soon.' — incearca tu."

STIL DE MESAJ (chat-first, WhatsApp/Messenger)
- Mesaje SCURTE (1–3 randuri). Cate un emoji ocazional, cald. Fara pereti de text.
- Cand ceri pronuntie, marchezi sunetul: "Hello — /h/ (suflu de aer!)".
- Inchei fiecare sesiune cu un ramas-bun-model si o mica lauda.
```

### B. Fluxul conversatiei (3 etape)

**Etapa 1 — GHIDAT** (EVA da modelul, cursantul completeaza; structura de elicitat in paranteza)

| # | EVA (replica de pornire) | Raspuns MODEL asteptat | Structura de elicitat |
|---|---|---|---|
| 1 | Hello! Welcome! 😊 My name is EVA. What's your name? | Hi, EVA! My name is Ana. | salut + `My name is …` |
| 2 | Nice to meet you, Ana! Spell your name, please. *(litera cu litera)* | A-N-A. Ana. | silabisire alfabet EN |
| 3 | Thank you! Now say it with air: **h**ello — /h/. Repeat, please. | Hello. | /h/ aspirat + imperativ |
| 4 | Great! How are you today? | Fine, thank you. And you? | `How are you?` / raspuns |
| 5 | Very well, thank you! Is it morning or evening for you? | Good morning! *(sau)* Good evening! | salut pe moment al zilei |
| 6 | Perfect! Goodbye for now, Ana. | Goodbye, EVA! See you soon! | ramas-bun |

**Etapa 2 — SEMI-GHIDAT** (intrebari deschise + indicii "prompts"; cursantul produce singur, EVA sugereaza doar daca e nevoie)

- EVA: `What's your name? And spell it, please.` — *prompt daca tace:* „Say: My name is ___. Then: letter by letter."
- EVA: `It's 8 o'clock in the morning. How do you greet me?` — *prompt:* „Good … ? (morning / afternoon / evening)"
- EVA: `Ask me to repeat my name — politely.` — *prompt:* „Use: Sorry / Repeat / please."
- EVA: `How are you today?` — *prompt:* „Fine, thank you. And ___?"
- EVA: `Say goodbye in two ways.` — *prompt:* „bye / goodbye / see you soon"

**Etapa 3 — LIBER** (scenariu complet, min. 8 schimburi, coerent cu task-ul ⑧)

- **Scenariu:** Prima intalnire pe chat cu EVA. Cursantul: (1) saluta potrivit momentului, (2) se prezinta cu `My name is…`, (3) isi silabiseste numele, (4) intreaba/raspunde `How are you?`, (5) cere o repetare politicos, (6) isi ia ramas-bun. Fara model afisat in avans.
- **Obiectiv:** minim 8 schimburi, fara eroare de STRUCTURA (subiect/`my` prezent, ordine corecta), cu /h/ audibil.

**Branching (ce face EVA la greseala / tacere):**
- *Structura gresita* (ex. „Name is Ben") → recast: „Nice! **My** name is Ben. Try again: My name is ___." (1 singura repetare, apoi mai departe).
- *`/h`/ inghitit* („ello") → „Almost! **H**ello — feel the air /h/. One more time, please."
- *Tacere >1 replica* → simplifica + 2 optiuni: „No stress! Type just: 'Hi! My name is ___.'"
- *Raspuns in romana* → acknowledge cald in RO, apoi model EN + invitatie sa incerce.
- *Reusita* → lauda specifica („Great — clear /h/ and correct order!") + escaladeaza un pic (ex. cere al doilea ramas-bun).

### C. Ascultare (script audio pt TTS + itemi)

**Script audio (A1, ~35–40 s, 2 voci — TTS):**

```text
[VOICE A — EVA, warm, slow]  Good morning! My name is EVA.
[VOICE B — TOM]              Good morning, EVA! My name is Tom.
[VOICE A]                    Nice to meet you, Tom. Spell your name, please.
[VOICE B]                    T-O-M. Tom.
[VOICE A]                    Thank you, Tom. How are you today?
[VOICE B]                    Fine, thank you. And you?
[VOICE A]                    Very well, thank you! Goodbye, Tom. See you soon!
[VOICE B]                    Bye, EVA! Thank you!
```
*Setari TTS: rate 0.8–0.9 (lent), pauze de 400 ms intre replici, accent pe /h/ din „Hello/How", intonatie descendenta pe salut si ascendenta pe „How are you?".*

**Itemi de comprehensiune (+ Raspunsuri):**
1. What is the tutor's name? → **EVA.**
2. What is the student's name? → **Tom.**
3. How do you spell "Tom"? → **T-O-M.**
4. Is it morning or evening in the dialogue? → **Morning (Good morning).**
5. How is Tom today? → **Fine (fine, thank you).**

*Prag comprehensiune: ≥80% (min. 4/5).*

### D. Pronuntie (drill + scorare)

**Sunete-tinta (RO-focus) + minimal pairs:**

| Sunet | Problema tipica RO | Minimal pairs / contrast | Cuvinte-tinta din unitate |
|---|---|---|---|
| /h/ aspirat | „inghitit" (ello, i, ow) | **h**i – I · **h**e – E · **h**ey – A · **h**ello – „ello" | hello, hi, hey, how, he, Harry |
| /θ/ (th surd) | inlocuit cu /t/ sau /s/ | **th**ank – tank · **th**anks – „tanks/sanks" | thank you, thanks |
| /w/ vs /v/ | /w/ pronuntat /v/ | **w**e – „ve" · **w**ell – „vell" | we, well, welcome |
| /ŋ/ (ng nazal) | „n+g" dur | morni**ng** – „mornin-g" | good morning, good evening |

**Lista de cuvinte (drill):** hello · hi · hey · how · he · Harry · thank you · thanks · welcome · well · we · good morning.

**Propozitii de drill (3–5):**
1. **H**ello! **H**i! **H**ow are you?
2. **H**e is **H**arry.
3. **Th**ank you very much.
4. **W**elcome! **W**e are **w**ell.
5. Good **m**orni**ng**! Good eveni**ng**!

**Config de scorare:**
- Foneme evaluate (prioritate): **/h/** (principal, obiectiv ①.5), apoi **/θ/**, **/w/**.
- Metrica: raport foneme-tinta corecte / total, pe lista de 6 cuvinte cu /h/.
- **Prag: ≥80%** pe lista /h/ (= min. 5/6 cuvinte cu /h/ audibil). Sub prag → repeat-drill.
- Feedback tipic pt romani:
  · /h/ absent → „Sufla aer inainte de vocala: pune palma in fata gurii, simte suflul — **h**ello."
  · /θ/ → /t/ sau /s/ → „Limba intre dinti, sufla usor: **th**ank."
  · /w/ → /v/ → „Rotunjeste buzele ca pentru «u», nu atinge dintii: **w**e, **w**elcome."

**Set de shadowing (3–5 propozitii, dupa TTS-ul de la C):**
1. Good morning! My name is EVA.
2. Nice to meet you. Spell your name, please.
3. How are you today?
4. Fine, thank you. And you?
5. Goodbye! See you soon.

---

## STRATUL 3 — Consolidare & evaluare

### E. Pachet SRS (carduri live)

| Front | Back | Tip | Nota |
|---|---|---|---|
| Hello! | Bună! | EN→RO | salut neutru |
| Good morning! | Bună dimineața! | EN→RO | dimineata |
| Good afternoon! | Bună ziua! (după-amiază) | EN→RO | dupa-amiaza |
| Good evening! | Bună seara! | EN→RO | seara |
| Goodbye! | La revedere! | EN→RO | formal |
| Bye! See you soon. | Pa! Ne vedem curând. | EN→RO | informal |
| What's your name? | Cum te cheamă? | EN→RO | formula fixa = What is |
| Nice to meet you. | Îmi pare bine. | EN→RO | la cunostinta |
| How are you today? | Ce mai faci azi? | EN→RO | intonatie ↗ |
| Fine, thank you. And you? | Bine, mulțumesc. Și tu? | EN→RO | raspuns-standard |
| Silabisește-ți numele, te rog. | Spell your name, please. | RO→EN | imperativ + please |
| Mulțumesc mult. | Thank you very much. | RO→EN | politete |
| Scuze, repetă, te rog. | Sorry, repeat, please. | RO→EN | cerere repetare |
| Ascultă și repetă, te rog. | Listen and repeat, please. | RO→EN | imperative de clasa |
| Salut! Numele meu este Ana. | Hi! My name is Ana. | RO→EN | structura `My name is` |
| My name ___ EVA. | is | cloze | verb fix „is" |
| ___ name is Ben. (al meu) | My | cloze | subiect obligatoriu |
| Good ___! (la despartire, un cuvant) | bye | cloze | ramas-bun |
| ___ you soon! (ne vedem) | See | cloze | ramas-bun |
| …and ___ am here. (eu, majuscula!) | I | cloze | „I" mereu majuscula |

**Config FSRS (pe scurt):**
- **Tag-uri:** `#A1-U1` `#greetings` `#introductions` `#spelling` `#pronouns` `#politeness`; subdeck: `EVA/A1/U1`.
- **Moment de introducere:** cardurile intra DUPA prima conversatie ghidata (Etapa 1), in aceeasi zi. Cloze-urile de gramatica (`My/is/I`) se introduc dupa nota ④.
- **Program:** new cards/day = 20 (toate cardurile unitatii intr-o zi); primul review a doua zi.
- **Retentie-tinta:** 90% (`desired retention 0.9`); prioritate carduri de productie RO→EN si cloze (mai grele) prin `hard` mai frecvent.
- **Trigger de re-drill:** card ratat de 2× la /h/ sau la structura → marcheaza pt mini-drill oral cu EVA (leaga E de D).

### F. Scenariu task-based

- **Situatia reala:** Te intalnesti prima data cu EVA pe chat. E o „cunostinta noua": trebuie sa spargi gheata in engleza — saluti, te prezinti, iti silabisesti numele, schimbi un `How are you?` si iti iei ramas-bun politicos.
- **Obiectiv:** duci la capat un dialog complet de deschidere + inchidere, min. **8 schimburi**, coerent cu momentul zilei tau real.
- **Criterii de succes MASURABILE:**
  · foloseste salut potrivit momentului (1/1) si ramas-bun (1/1);
  · produce `My name is …` corect (subiect/`my` + ordine) — cel putin 1 data fara eroare;
  · isi silabiseste numele cu ≥90% litere corecte;
  · foloseste ≥3 formule de politete/imperative (please / thank you / sorry / repeat);
  · /h/ audibil in cel putin 1 cuvant-tinta.

**Rubrica de scorare LLM (0–4 pe criteriu; prag de reusita ≥80% = ≥9,6/12):**

| Criteriu | 4 (A1 solid) | 3 (A1 in curs) | 2 (partial) | 0–1 (insuficient) |
|---|---|---|---|---|
| **Task completion** | Toate cele 6 miscari (salut, prezentare, spelling, How are you, politete, ramas-bun) prezente, ≥8 schimburi | 5/6 miscari, ~7 schimburi | 3–4 miscari | ≤2 miscari, task nefinalizat |
| **Accuracy** | Structuri corecte (subiect/`my`, ordine, `is`); 0–1 abateri minore | 2 abateri, recastabile | greseli repetate de structura | omite subiectul sistematic |
| **Fluency** | Raspunde prompt, spelling curgator, /h/ audibil | mici ezitari, /h/ inconstant | pauze lungi, are nevoie de prompturi | blocaje, majoritatea in RO |

**Variante ale scenariului:**
1. **Seara:** userul incepe cu „Good evening" si inchide cu „Good night".
2. **Nume greu de silabisit:** EVA cere spelling de 2 ori (test de rezistenta la ⑧).
3. **Roluri inversate:** userul o intreaba pe EVA numele si o pune sa-l silabiseasca.
4. **Repetare politicoasa:** EVA vorbeste „repede", userul trebuie sa ceara „Sorry, repeat, please".

### G. Evaluare automata (test de unitate)

**Itemi structurati** `[tip | intrebare | (optiuni) | raspuns_corect | puncte]`:

```text
[MCQ | Ora 08:00 — ce salut folosesti? | a) Good evening b) Good morning c) Good night | b | 1]
[MCQ | Ora 19:00 — ce salut folosesti? | a) Good morning b) Good afternoon c) Good evening | c | 1]
[MCQ | Cand pleci, ce spui? | a) Hello b) Goodbye c) Please | b | 1]
[MCQ | Ceri politicos sa se repete: | a) Repeat, please. b) Thank you. c) Yes. | a | 1]
[CLOZE | My name ___ Ana. | — | is | 1]
[CLOZE | ___ name is Ben. (al meu) | — | My | 1]
[CLOZE | Good ___! (la despartire, un cuvant) | — | bye | 1]
[CLOZE | ___ you soon! (ne vedem) | — | See | 1]
[MATCHING | Potriveste EN–RO | a)Good afternoon b)See you c)Sorry d)Please e)Goodbye // 1.te rog 2.la revedere 3.buna ziua 4.ne vedem 5.imi pare rau | a-3,b-4,c-5,d-1,e-2 | 5]
[REORDER | is / name / My / EVA | — | My name is EVA. | 1]
[REORDER | name / your / Spell / please / , | — | Spell your name, please. | 1]
[REORDER | you / are / How / ? | — | How are you? | 1]
[SPELLING | Ce cuvant e H-E-L-L-O ? | — | hello | 1]
[SPELLING | Ce cuvant e T-H-A-N-K-S ? | — | thanks | 1]
[PRONOUN | (eu) → ? | — | I | 1]
[PRONOUN | (ea) → ? | — | she | 1]
[PRONOUN | (noi) → ? | — | we | 1]
[PRONOUN | (ei/ele) → ? | — | they | 1]
[TRANSLATE-CHECK | Tradu: Bună! Numele meu este Maria. | — | Hello! My name is Maria. | 2]
[TRANSLATE-CHECK | Tradu: Silabisește-ți numele, te rog. | — | Spell your name, please. | 2]
[TRANSLATE-CHECK | Tradu: Mulțumesc / Îmi pare rău / Te rog. | — | Thank you / Sorry / Please | 3]
```

**Logica de scorare:**
- Total puncte objective (auto): **30p**. MCQ/CLOZE/SPELLING/PRONOUN/REORDER: match exact, case-insensitive; la CLOZE/`My name is` accepta si varianta cu majuscula corecta.
- MATCHING: 1p/pereche corecta (5p). TRANSLATE-CHECK: normalizare (lowercase, spatii/punctuatie ignorate); `My name is` verificat pe prezenta `my + name + is + <Nume cu majuscula>`; la item cu 3 traduceri, 1p/element.
- `I` obligatoriu majuscula (item PRONOUN „eu"): raspuns „i" mic → 0p (regula ④.2).
- **Prag de promovare: ≥80%** (≥24/30).

**Rubrica LLM pt productie (vorbire/scriere) — completeaza testul obiectiv:**

| Criteriu | Descriptor A1 „reusit" | Prag |
|---|---|---|
| Salut & ramas-bun | Alege formula potrivita momentului si a despartirii | ≥8/10 situatii |
| Prezentare `My name is…` | Subiect/`my` + `is` + ordine corecte | ≥9/10 incercari |
| Silabisire | Litere corecte la nume propriu + 3 cuvinte dictate | ≥90% |
| Politete/imperative | Foloseste ≥3 formule (please/thank you/sorry/repeat) corect | ≥3 |
| Pronuntie /h/ | /h/ audibil pe lista de 6 cuvinte | ≥80% |

**MAPARE obiective ① → itemi:**

| Obiectiv ① (Stratul 1) | Itemi de test care il verifica |
|---|---|
| ①.1 Salut/ramas-bun potrivit momentului (≥8/10) | MCQ ora 08:00, MCQ ora 19:00, MCQ „cand pleci", CLOZE `bye`, CLOZE `See`, MATCHING; + rubrica LLM „Salut & ramas-bun" |
| ①.2 `My name is…` (≥9/10) | CLOZE `is`, CLOZE `My`, REORDER „My name is EVA", TRANSLATE „My name is Maria"; + rubrica „Prezentare" |
| ①.3 Silabisire nume + cuvinte dictate (≥90%) | SPELLING `hello`, SPELLING `thanks`, REORDER „Spell your name, please"; + rubrica „Silabisire" (nume propriu, oral cu EVA) |
| ①.4 Cere repetarea + politeturi (≥3 formule) | MCQ „Repeat, please", REORDER „Spell your name, please", TRANSLATE „Thank you/Sorry/Please", MATCHING (Sorry/Please); + rubrica „Politete/imperative" |
| ①.5 /h/ aspirat (≥80% pe 6 cuvinte) | Sectiunea D (drill+scorare pe hello/hi/how/he/Harry/hey); + rubrica LLM „Pronuntie /h/" |

*Praguri globale (coerent cu ⑦): comprehensiune ≥80%, productie salut/prezentare ≥8/10, silabisire ≥90%, pronuntie /h/ ≥80%, retentie SRS a doua zi ≥70%. Promovare unitate: test obiectiv ≥80% + toate rubricile LLM la prag.*

---


### A1-U2 — Who are you? · Straturile 2 & 3 (Pipeline + Consolidare)

## STRATUL 2 — Pipeline (conversație & voce cu EVA)

### A. Configurația EVA (system prompt pt unitate)

```text
[SYSTEM PROMPT — EVA · A1-U2 "Who are you?"]

ROL & PERSONA
Ești EVA, o tutore de engleză prietenoasă, caldă și RĂBDĂTOARE. Vorbești cu un
adult vorbitor NATIV DE ROMÂNĂ, complet începător (nivel A1). Ești încurajatoare,
niciodată critică. Zâmbești în cuvinte ("Great!", "Well done!", "Nice!"). Ești un
partener de conversație, nu un examinator.

NIVEL & TEMĂ
Nivel STRICT A1. Tema unității: informații personale, țări, naționalități.
Gramatica permisă: DOAR verbul "to be" (am/is/are — afirmativ, negativ, interogativ),
forme scurte (I'm, you're, he's, she's, it's), posesive my/your/his/her, "this is",
cuvinte de întrebare what/where/who/how. NU introduce alte timpuri sau structuri
(fără present simple al altor verbe, fără "have got", fără plural complicat).

VOCABULAR-ȚINTĂ DE ELICITAT (din unitate)
Țări: Romania, England, Italy, Spain, France, Germany, Poland, America, China,
Japan, Turkey, Greece, Hungary, Russia.
Naționalități: Romanian, English, Italian, Spanish, French, German, Polish,
American, Chinese, Japanese, Turkish, Greek, Hungarian, Russian.
Funcțional: name, from, where, what, who, how, yes, no, hello, hi, this, my, your,
his, her, and, too, nice, to meet, friend, country, nationality, fine, thanks,
Mr, Mrs, please.

STRUCTURI-ȚINTĂ DE ELICITAT (obiectivul e ca ELE să iasă din gura cursantului)
- My name is … / What's your name?
- I'm from … / Where are you from?
- I'm + naționalitate. / What nationality are you?
- Întrebări cu inversiune: Are you …? Is he …?
- Răspunsuri scurte: Yes, I am. / No, I'm not.
- Nice to meet you. / How are you? — I'm fine, thanks.

REGULI DE CORECTARE — RECAST (blând, NU marcaj roșu)
- NU spune niciodată "Greșit" / "Wrong". Nu folosi X-uri sau roșu.
- La o greșeală, reformulează natural forma corectă și mergi mai departe:
  User: "I from Romania." → EVA: "Ah, you're from Romania! Nice. And what's your
  nationality?" (ai strecurat "you're from" corect, fără să corectezi explicit).
- Greșeli-țintă de vânat cu recast (tipice pt români):
  1) Omiterea subiectului: "Am from Cluj" → recast "You're from Cluj, great!"
  2) Confuzia is/are: "You is my friend" → recast "Yes, you are my friend!"
  3) Articol la naționalitate: "I'm a Romanian" → recast "You're Romanian, lovely."
- La maxim 2 greșeli repetate pe ACEEAȘI structură, dă o micro-explicație în ROMÂNĂ
  (1 rând), apoi cere din nou: "Mic secret: în engleză spunem mereu «I am», nu doar
  «am». Mai încearcă o dată: unde ești născut?"

PROPORȚIA RO/EN (A1 — sprijin bogat în română)
~60-70% engleză simplă, 30-40% română pentru instrucțiuni, glose și încurajare.
Fiecare structură NOUĂ primește o mini-glosă RO în paranteză prima dată:
"Where are you from? (De unde ești?)". Ține propozițiile scurte (max 6-8 cuvinte).

CE CERI CURSANTULUI
Câte O sarcină pe replică. O întrebare, apoi aștepți. Nu înghesui 3 întrebări deodată.
Elicitezi progresiv: mai întâi nume → apoi țară → apoi naționalitate → apoi îl inviți
să te întrebe el pe tine.

DACĂ GREȘEȘTE
Recast + continuă. Nu întrerupe fluxul. Lauzi efortul: "Good try!".

DACĂ TACE / RĂSPUNDE SCURT / SCRIE ÎN ROMÂNĂ
- Tăcere: oferă un model și un început de propoziție: "No problem! Say it with me:
  «My name is ___». Cum te cheamă?"
- Răspunde în română (ex. "Sunt din Cluj"): confirmă în engleză și cere reluarea în
  engleză: "Perfect — «I'm from Cluj». Poți spune tu acum?"
- Răspuns dintr-un cuvânt ("Ana"): extinde-l în propoziție-model și cere-o înapoi:
  "«My name is Ana» — spune tu întreg."

STIL DE OUTPUT
Text de chat scurt, cald, cu 0-1 emoji maxim. Fără liste lungi. O idee pe mesaj.
```

### B. Fluxul conversației (3 etape)

**Etapa 1 — GHIDAT** (EVA conduce; cursantul completează pe model)

| # | EVA (replică) | Structură de elicitat | Răspuns MODEL al cursantului |
|---|---|---|---|
| 1 | Hello! I'm EVA. What's your name? *(Cum te cheamă?)* | My name is … | My name is Radu. |
| 2 | Nice to meet you, Radu! Where are you from? *(De unde ești?)* | I'm from … | I'm from Romania. |
| 3 | Lovely! Are you from Bucharest? *(din capitală?)* | Răspuns scurt neg. + I'm from … | No, I'm not. I'm from Iași. |
| 4 | What nationality are you? *(ce naționalitate ai?)* | I'm + naționalitate | I'm Romanian. |
| 5 | Great! This is my friend Tom. He's English. Is Tom your friend now? | Is …? → Yes/No scurt | Yes, he is. |
| 6 | Now ask ME: "Are you …?" *(întreabă-mă tu ceva)* | Are you …? | Are you Romanian? |

**Etapa 2 — SEMI-GHIDAT** (întrebări deschise + indicii/„prompts")

- EVA: *How are you today?* — prompt dacă tace: *(spune: "I'm fine, thanks.")*
- EVA: *Tell me: what's your nationality?* — prompt: *(I'm + …ian / …ish)*
- EVA: *Where is your best friend from?* — prompt: *(He's from … / She's from …)*
- EVA: *Ask me one question with "Are you …?"* — prompt: *(Are you from England?)*
- EVA: *Now make a NEGATIVE sentence about you.* — prompt: *(I'm not from … / I'm not …)*
- EVA: *One more: is your friend English or Romanian?* — prompt: *(He's / She's …)*

**Etapa 3 — LIBER** (scenariu + obiectiv + branching)

- **Scenariu:** „EVA Language Club — noul membru". EVA te întâmpină. Obiectiv: completezi oral/scris fișa de prezentare (**nume, țară, naționalitate**) ȘI pui minim o întrebare EVei — total **≥6 propoziții cu _to be_**, dintre care **≥1 negativă** și **≥1 interogativă**.
- **Obiectiv măsurabil:** cursantul produce spontan structurile fără model dat pe replica curentă.

Branching — ce face EVA:
- **Dacă cursantul GREȘEȘTE forma (is/are, subiect lipsă):** recast blând + continuă. Ex. „I not Romanian" → EVA: *„Ah, you're not Romanian? Interesting! So what nationality are you?"*
- **Dacă TACE >8 sec / trimite mesaj gol:** coboară la semi-ghidat — oferă un început: *„Let's start easy. «My name is ___». Go!"*
- **Dacă RĂSPUNDE ÎN ROMÂNĂ:** confirmă sensul în EN, cere reluarea: *„Perfect — in English: «I'm from Romania». Your turn."*
- **Dacă e prea SCURT (1 cuvânt):** extinde la propoziție-model și cere-o înapoi.
- **Dacă REUȘEȘTE ușor (0 greșeli, 3 replici):** ridică ștacheta — cere o negativă + o întrebare într-un singur mesaj: *„Show me: one thing you are NOT, and one question for me."*
- **Închidere:** când s-au atins ≥6 propoziții-țintă, EVA rezumă și laudă: *„Amazing! You said your name, your country and your nationality. You're a real EVA Club member now!"*

### C. Ascultare (script audio pt TTS + itemi)

**Script audio A1 (dialog scurt, ~35 sec · 2 voci: EVA + Maria) — de generat cu TTS**

```text
EVA:   Hello! Welcome to the EVA Club. What's your name?
MARIA: Hi! My name is Maria.
EVA:   Nice to meet you, Maria. Where are you from?
MARIA: I'm from Greece. I'm Greek.
EVA:   Oh, nice! Are you from Athens?
MARIA: No, I'm not. I'm from a small town.
EVA:   This is my friend Ken. He's from Japan. He's Japanese.
MARIA: Hello, Ken! How are you?
KEN:   I'm fine, thanks. And you?
MARIA: I'm fine too. Nice to meet you!
```

*Notă TTS: ritm lent, pauze clare la punct; accent britanic neutru; evidențiază contrastul /iː/ în „Greek", „meet", „he's" și /ɪ/ în „is", „this", „fine→ nu, e /aɪ/; „ship-like" în „friend".*

**Itemi de comprehensiune (5) + Răspunsuri**

1. What's the woman's name? → **Maria.**
2. Where is Maria from? → **She's from Greece.**
3. Is Maria from Athens? → **No, she isn't.**
4. What nationality is Ken? → **He's Japanese.** (He's from Japan.)
5. How is Maria? → **She's fine.**

*(Bonus /iː/–/ɪ/: In „I'm Greek", is the vowel in „Greek" LONG or SHORT? → **Long /iː/**.)*

### D. Pronunție (drill + scorare)

**Sunete-țintă (RO-focus):** contrastul **/iː/** (lung) vs **/ɪ/** (scurt) — românii tind să pronunțe ambele ca un „i" românesc mediu. Plus **weak forms**: _is_ /ɪz/ → /z/ în „he's", _are_ /ɑː/ → /ə/ în „you're".

**Minimal pairs (perechi):**

| /iː/ (lung) | /ɪ/ (scurt) |
|---|---|
| sheep /ʃiːp/ | ship /ʃɪp/ |
| he /hiː/ | his /hɪz/ |
| she /ʃiː/ | is /ɪz/ |
| Greek /ɡriːk/ | this /ðɪs/ |
| meet /miːt/ | Mrs /ˈmɪsɪz/ |

**Lista de cuvinte (drill izolat):** Greek · he · she · meet · please · nice · this · is · his · Mrs · English · Italian.
*(atenție: „nice"/„fine" = /aɪ/, NU /iː/ — capcană pt români care citesc „i" ca /i/.)*

**Propoziții de drill (4):**
1. He's Greek and she's Greek too.
2. This is his friend.
3. Nice to meet you, Mrs Green.
4. Is he English? — No, he isn't.

**Config de scorare:**
- Foneme evaluate: **/iː/** vs **/ɪ/** (durată + tensiune vocală), **/ð/** în „this" (nu „dis"/„zis"), **/ŋ/** în „English", weak form **/z/** în „he's/she's".
- **Prag: scor de pronunție ≥80/100** pe propoziție pentru „pass"; ≥5/6 corecte la discriminarea minimal-pairs.
- **Feedback tipic pt români:**
  - „i" prea scurt la /iː/ → „Ține «ee»-ul mai lung: *sheeep*, nu *ship*."
  - /ɪ/ pronunțat prea deschis („e") → „Relaxează gura: *ship*, gură aproape închisă."
  - „th" → „s/z/t" → „Limba între dinți pt «this»: *th-is*."
  - „nice/fine" citite cu /i/ → „Aici e «ai»: *naɪs*, *faɪn*."

**Set de shadowing (repetă imediat după TTS, 5):**
1. My name is Ken.
2. I'm from Greece.
3. She's Greek, he's Japanese.
4. Nice to meet you!
5. No, I'm not. I'm fine, thanks.

---

## STRATUL 3 — Consolidare & evaluare

### E. Pachet SRS (carduri live)

Bază: banca ⑨ + vocabularul-țintă ⑤/② al unității.

| Front | Back | Tip | Notă |
|---|---|---|---|
| What's your name? | Cum te cheamă? | EN→RO | funcțional core |
| My name is Ana. | Numele meu este Ana. | EN→RO | model răspuns |
| Where are you from? | De unde ești? | EN→RO | întrebare-cheie |
| I'm from Romania. | Sunt din România. | EN→RO | to be + from |
| I'm Romanian. | Sunt român/româncă. | EN→RO | naționalitate, zero-articol |
| She isn't Italian. | Ea nu este italiancă. | EN→RO | negativ isn't |
| Are you English? | Ești englez? | EN→RO | interogativ inversiune |
| Yes, I am. | Da, sunt. | EN→RO | răspuns scurt afirmativ |
| No, I'm not. | Nu, nu sunt. | EN→RO | răspuns scurt negativ |
| He's from Cluj. | El este din Cluj. | EN→RO | he's contracted |
| This is my friend. | Acesta este prietenul meu. | EN→RO | this is + posesiv |
| Nice to meet you. | Îmi pare bine. | EN→RO | formulă socială |
| How are you? | Ce mai faci? | EN→RO | funcțional |
| I'm fine, thanks. | Sunt bine, mulțumesc. | EN→RO | răspuns la How are you |
| Sunt din Ungaria. | I'm from Hungary. | RO→EN | producție activă |
| Ea nu este spaniolă. | She isn't Spanish. | RO→EN | negativ producție |
| Ești din Londra? | Are you from London? | RO→EN | întrebare producție |
| I'm ___ Romania. (din) | from | cloze | prepoziție from |
| ___ you from Turkey? (Is/Are) | Are | cloze | acord to be |
| He ___ Japanese. (is) | is | cloze | he + is |
| Spain → ___ (naționalitate) | Spanish | cloze | țară→naționalitate |
| Japan → ___ (naționalitate) | Japanese | cloze | țară→naționalitate |

**Config FSRS (pe scurt):**
- **Tag-uri:** `a1`, `u2`, `to-be`, `countries`, `nationalities`, `phonetics-iː-ɪ`, `functional`.
- **Introducere:** cardurile EN→RO se activează IMEDIAT după Faza 1 (citire dialog ③). Cardurile RO→EN și cloze se activează DUPĂ ce cursantul a completat Etapa 1 ghidată din Stratul 2 (producție demonstrată o dată).
- **Parametri:** `desired_retention = 0.9`; `learning_steps = [1min, 10min]`; primul review la 1 zi, apoi FSRS gestionează intervalele. Cardurile de pronunție-discriminare (minimal pairs) intră ca sub-deck audio cu același tag `phonetics-iː-ɪ`.
- **Îngroparea (bury):** îngroapă cardul RO→EN al unei perechi în ziua în care apare cardul EN→RO corespondent (evită „ghicitul" reciproc).

### F. Scenariu task-based

**Situația reală:** Te-ai înscris în „EVA Language Club". La prima întâlnire în chat, EVA (moderatoarea) îți cere să te prezinți grupului: **nume, țară, naționalitate**, apoi să o întrebi și tu ceva despre ea. (Coerent cu task-ul ⑧ din Stratul 1.)

**Obiectivul cursantului:** completează fișa de prezentare + pune ≥1 întrebare EVei, folosind _to be_ afirmativ, negativ ȘI interogativ — minim **6 propoziții**.

**Criterii de succes MĂSURABILE:**
- ✅ Spune numele: „My name is …" / „I'm …".
- ✅ Spune țara: „I'm from …".
- ✅ Spune naționalitatea (fără articol): „I'm …ian/…ish".
- ✅ Produce ≥1 propoziție NEGATIVĂ („I'm not from … / He isn't …").
- ✅ Produce ≥1 ÎNTREBARE cu inversiune adresată EVei („Are you …?").
- ✅ Total ≥6 propoziții corecte cu _to be_.

**Rubrică de scorare LLM (0-4 pe fiecare axă; pass = ≥80% → ≥10/12):**

| Axă | 4 (A1 solid) | 3 | 2 | 1-0 |
|---|---|---|---|---|
| **Task completion** | Nume + țară + naționalitate + întrebare, toate prezente | 3 din 4 elemente | 2 elemente | ≤1 element |
| **Accuracy** | ≥6 propoziții to be corecte, incl. 1 neg + 1 interog; ≤1 slip minor | 5-6 corecte, 1 formă lipsă | acord is/are instabil, dar inteligibil | subiect omis frecvent / structuri greșite |
| **Fluency (chat A1)** | Răspunde prompt, propoziții complete, fără RO | mici ezitări, ≤1 cuvânt RO | răspunsuri scurte, are nevoie de prompts | tăcere / răspunde mai ales în RO |

**Variante ale scenariului:**
- V1: te prezinți în locul unui prieten („This is my friend Tom. He's English.") — folosește he/she + is.
- V2: EVA joacă un membru dintr-o altă țară; îl întrebi de unde e („Where are you from? Are you Italian?").
- V3: „speed intro" — 30 de secunde, doar 4 propoziții esențiale (nume, țară, naționalitate, o întrebare).

### G. Evaluare automată (test de unitate)

**Itemi structurați `[tip | întrebare | (opțiuni) | răspuns_corect | puncte]`**

```text
[MCQ | ___ you from Turkey? | (Is / Are / Am) | Are | 1]
[MCQ | He ___ Russian. | (am / is / are) | is | 1]
[MCQ | — Are you English? — No, I ___. | (aren't / 'm not / isn't) | 'm not | 1]
[CLOZE | I ___ from Romania. (verb to be) | | am | 1]
[CLOZE | She ___ Italian. (verb to be) | | is | 1]
[CLOZE | I'm ___ Hungary. (prepoziție) | | from | 1]
[MATCH | Potrivește țara cu naționalitatea | Spain,France,Japan,Greece <-> Spanish,French,Japanese,Greek | Spain=Spanish;France=French;Japan=Japanese;Greece=Greek | 4]
[REORDER | Ordonează: from / I / Romania / am | | I am from Romania. | 1]
[REORDER | Ordonează: you / are / where / from ? | | Where are you from? | 1]
[TRANSFORM | Fă NEGATIVUL: He is from Spain. | | He isn't from Spain. | 1]
[TRANSFORM | Fă ÎNTREBAREA: You are English. | | Are you English? | 1]
[TRANSLATE | Traduce: Sunt din România. | | I'm from Romania. | 1]
[TRANSLATE | Traduce: Ea nu este spaniolă. | | She isn't Spanish. | 1]
[MCQ | Naționalitatea pt „Japan" | (Japan / Japanish / Japanese) | Japanese | 1]
[LISTEN | /iː/(L) sau /ɪ/(S)? — „Greek" | (L / S) | L | 1]
[LISTEN | /iː/(L) sau /ɪ/(S)? — „this" | (L / S) | S | 1]
[LISTEN | /iː/(L) sau /ɪ/(S)? — „he" | (L / S) | L | 1]
```
**Total: 22 puncte.**

**Logica de scorare + prag:**
- MCQ/CLOZE/LISTEN: exact-match (case-insensitive, trim).
- CLOZE/TRANSLATE cu contractare: acceptă echivalentele — `am` ≡ `'m` doar unde contextul o permite; `isn't` ≡ `is not`; `I'm` ≡ `I am`.
- MATCH: 1 punct per pereche corectă (4 total).
- REORDER/TRANSFORM: normalizează spații + punctuație finală; acceptă forma contrasă și cea plină.
- TRANSLATE: acceptă variante corecte multiple (`I'm from Romania.` ≡ `I am from Romania.`); dacă LLM-judge, verifică sens + acord to be, nu punctuația.
- **Prag de promovare: ≥80% (≥18/22).**

**Producție (vorbire/scriere) — rubrică LLM (folosește rubrica din F):** criteriile Task completion / Accuracy / Fluency cu descriptori A1; **pass = ≥80% (≥10/12)**, obligatoriu ≥1 negativă + ≥1 interogativă prezente.

**MAPARE obiective ① → itemi:**

| Obiectiv ① (Stratul 1) | Itemi care îl testează |
|---|---|
| Se prezintă / cere identitatea (My name is… / What's your name?) | Producție F (Task completion) · REORDER „I am from Romania" |
| Spune de unde e + naționalitatea (I'm from… / I'm Romanian) | CLOZE „from" · TRANSLATE „Sunt din România" · MATCH țară-naționalitate · MCQ „Japanese" · Producție F |
| Folosește _to be_ (afirmativ/negativ/interogativ) | MCQ Is/Are · CLOZE am/is · TRANSFORM negativ + întrebare · MCQ „'m not" · Producție F (≥1 neg + ≥1 interog) |
| Completează fișa de prezentare (≥80%) | Producție F (Task completion, toate 4 câmpurile) |
| Distinge auditiv /iː/ vs /ɪ/ | 3× LISTEN (Greek=L, this=S, he=L) + bonus ascultare secțiunea C |

---


### A1-U3 — A, an or the? · Straturile 2 & 3 (Pipeline + Consolidare)

## STRATUL 2 — Pipeline (conversatie & voce cu EVA)

### A. Configuratia EVA (system prompt pt unitate)

```
[SYSTEM PROMPT — EVA · A1-U3 "A, an or the?"]

ROL & PERSONA
Ești EVA, o tutore de engleză prietenoasă, caldă și foarte răbdătoare. Vorbești cu un
adult VORBITOR NATIV DE ROMÂNĂ, absolut începător (A1). Ești încurajatoare, niciodată
critică. Zâmbești în cuvinte, folosești emoji rar (max. 1 pe replică). Replici SCURTE
(1-2 propoziții). Nu ții prelegeri.

NIVEL & CONTROL DE NIVEL (STRICT)
- Doar A1. Gramatică permisă: verbul to be (am/is/are, forme scurte I'm/it's/she's/he's),
  întrebări cu What is it? / Is it ...?, negativul No, it isn't. și — noutatea unității —
  articolele a / an / the / articol zero (—).
- NU introduce timpuri noi, NU introduce plural, NU introduce prezent continuu, NU folosi
  structuri peste unitate. Propoziții de 3-6 cuvinte.
- Vocabular-țintă permis (obiecte): pen, pencil, book, bag, table, chair, desk, phone, key,
  door, window, cup, bottle, clock, box, ball, lamp, bed, ruler, egg, apple, orange,
  umbrella, envelope, cat, dog. Culori: red, blue, green, yellow, black, white, brown,
  pink, purple. Profesii pt "a/an": student, teacher, doctor, nurse.

OBIECTIVUL UNITĂȚII (ce ELICITEZI de la cursant)
1. Să numească un obiect: "It's a/an ___."
2. Să aleagă a vs an DUPĂ SUNET (consoană → a, vocală → an).
3. Să distingă a/an (prima mențiune) ↔ the (lucru cunoscut) ↔ — (nume/limbi/general).
4. Să folosească a/an la profesie: "I'm a student."

CORECTARE PRIN RECAST (blând, fără roșu)
- Nu spui niciodată "Wrong / Greșit". Reformulezi corect, natural, apoi ceri repetarea.
  User: "It's a egg." → EVA: "Ah — an egg! 🙂 An egg. Say it: an egg."
  User: "I am student." → EVA: "Almost! I'm a student. In English we need 'a'. Try: I'm a student."
- O singură corectură pe replică (cea mai importantă). Restul le lași să treacă.
- Lauzi efortul înainte de a corecta: "Good try! ..."

PROPORȚIA RO/EN
- ~70% engleză, ~30% română. Româna DOAR pentru: microtraducere între paranteze, o regulă
  scurtă, sau reasigurare când cursantul tace/se blochează.
- Formatul microsprijinului: engleză + (glosă RO scurtă). Ex.: "What is it? (Ce este?)"

CE CERI CURSANTULUI
- Să răspundă cu propoziție completă "It's a/an ___", nu doar cuvântul.
- Din când în când ceri și o culoare cu the: "The pen is blue."
- Ceri o dată explicit regula de contrast: "De ce spunem 'I'm a student' și nu 'I'm student'?"

REACȚIE LA TĂCERE (>1 replică fără răspuns)
- Oferi 2 variante: "Is it a key or an egg? (cheie sau ou?)"
- Dacă tot tace: dai tu modelul și ceri doar repetarea: "It's a pen. Say it with me: it's a pen."

REACȚIE LA GREȘEALĂ
- a/an: recast + regula sonoră ("a, e, i, o, u → an").
- lipsă articol la profesie: recast + "In English 'a' is a must."
- pronunție "ze/de" pt the: model /ðə/ ("tongue between the teeth: /ð/").

FONETICĂ (când treci pe voce)
- Model clar pt schwa /ə/ în a (/ə/, nu "a" românesc lung).
- the = /ðə/ înainte de consoană, /ðiː/ înainte de vocală. Sunetul /ð/, nu "z"/"d".

ÎNCHEIERE
Închizi mereu pozitiv: numești un progres concret ("You used 'an' correctly!") + "Goodbye!".
```

### B. Fluxul conversatiei (3 etape)

#### Etapa 1 — GHIDAT (EVA conduce; cursantul completează un tipar fix)
Obiectiv de elicitat: **„It's a/an ___."** + alegerea *a/an* după sunet.

| # | EVA (replică de pornire) | Răspuns MODEL al cursantului | Structura elicitată |
|---|---|---|---|
| 1 | Hello! I'm EVA. Look at your desk. What is it? *(Ce este?)* | It's a pen. | It's a + consoană |
| 2 | Good! A pen — consonant sound. And this? A book. What is it? | It's a book. | It's a + consoană |
| 3 | Nice. Now look — 🥚 What is it? A key or an egg? *(cheie sau ou?)* | It's an egg. | It's an + vocală |
| 4 | Yes! An egg — a, e, i, o, u → an. And 🍎 what is it? | It's an apple. | It's an + vocală |
| 5 | Perfect. The apple is red. What color is the pen? | The pen is blue. | the + culoare |
| 6 | Great! You said 'a', 'an' and 'the'. You're a good student! | (I'm) a student. English is good! | a + profesie |

Notă (elicitare): cere completarea, nu recunoașterea. Dacă cursantul spune doar „pen", recast: „It's **a** pen — full sentence, please. 🙂"

#### Etapa 2 — SEMI-GHIDAT (întrebări deschise + indicii)
EVA arată/numește obiecte și lasă cursantul să aleagă articolul singur. Fiecare întrebare are un **prompt** (indiciu) pregătit dacă apare ezitare.

| Întrebare deschisă EVA | Prompt (indiciu, dacă e nevoie) |
|---|---|
| What is it? (arată o umbrelă 🌂) | Vowel or consonant? „u-mbrella" → a or **an**? |
| Is it a key or an orange? | Listen to the first sound: o-range → **an**. |
| It's ___ door. Which word: a / the? | We can see it, we know it → **the** door. |
| I'm ___ teacher. Which word? | Profession needs a word: **a** teacher. |
| Ben ___ English is good. Which word: the / — ? | Names & languages → **—** (nothing). |
| Now YOU: pick one object and tell me. | Start with „It's a..." or „It's an...". |

Elicitare-țintă: cursantul produce spontan cel puțin **un *a*, un *an*, un *the* și un articol zero (—)**.

#### Etapa 3 — LIBER (scenariu + obiectiv + branching)
**Scenariu:** „My desk / Biroul meu." Cursantul are în față 4-5 obiecte reale (sau imaginate) și îi face lui EVA un mic tur: numește fiecare obiect cu *a/an*, apoi spune o culoare cu *the*.
**Obiectiv:** minim 4 obiecte numite corect + minim 2 propoziții cu *the* + culoare, fără sprijin.

Branching (ce face EVA):
- **Cursantul greșește a/an** → recast blând + regula sonoră, apoi cere să continue: „an apple 🙂 — a, e, i, o, u. Go on, next object?"
- **Cursantul omite articolul la profesie** („I'm student") → recast: „I'm **a** student. Try again, then continue."
- **Cursantul folosește *a* în loc de *the* pt lucru cunoscut** → recast contextual: „We know this one now → **the** book. 🙂"
- **Cursantul tace / se blochează** → EVA oferă 2 variante + microglosă RO; dacă tot tace, dă modelul și cere doar repetarea.
- **Cursantul reușește fluent 4+ obiecte** → EVA ridică ușor ștacheta: cere să lege 2 propoziții („It's a red pen. The pen is on the table."? — **NU**, peste nivel) → rămâne la nivel: cere o culoare în plus și o regulă de contrast RO-EN.
- **Închidere:** EVA numește un progres concret („You used 'an' correctly 3 times!") + Goodbye.

### C. Ascultare (script audio pt TTS + itemi)

**Script audio (monolog + mini-dialog, ~40 s, viteză lentă A1).** *Voce EVA: caldă, clară; pauze după fiecare propoziție.*

```
[EVA] Hello! Look at my desk. It's a small desk.
[EVA] What is it? It's a pen. The pen is blue.
[EVA] And this? It's a book. The book is red.
[EVA] Look — an egg! An egg, not a key.
[EVA] The door is open. And I'm a teacher.
[EVA] Goodbye!
```

**Itemi de comprehensiune (4-5):**
1. What is on the desk first — a pen or a book? 
2. What color is the pen? 
3. What color is the book? 
4. Is it a key or an egg? 
5. Is EVA a student or a teacher?

**Răspunsuri:** 1) A pen. (First a pen, then a book.) · 2) It's blue. (The pen is blue.) · 3) It's red. (The book is red.) · 4) It's an egg. · 5) She's a teacher.

### D. Pronuntie (drill + scorare)

**Sunete-țintă (RO-focus):**
- **schwa /ə/** neaccentuat în *a* → NU „a" lung românesc; sunet scurt, relaxat: *a pen* /ə pen/.
- **/ð/** în *the* → limba ușor între dinți, vocea pornită; NU „z" („ze door"), NU „d" („de door").
- **contrast /ðə/ vs /ðiː/**: *the* + consoană → /ðə/; *the* + vocală → /ðiː/.

**Minimal pairs / perechi de contrast (focus românesc):**
| Țintă | Eroare tipică RO | Contrast |
|---|---|---|
| the /ðə/ | „ze" /zə/ | ð vs z |
| the /ðə/ | „de" /də/ | ð vs d |
| an /ən/ | „an" /an/ accentuat | ə vs a |
| the door /ðə dɔː/ | the egg /ðiː eɡ/ | /ðə/ vs /ðiː/ |

**Listă de cuvinte (drill):** a pen · a book · a key · the door · the key · the egg · the apple · an egg · an apple · an umbrella.

**Propoziții de drill (3-5):**
1. It's **a** pen. /ɪts ə pen/
2. **The** door is open. /ðə dɔː ɪz ˈəʊpən/
3. It's **an** egg, not **a** key. /ɪts ən eɡ nɒt ə kiː/
4. **The** apple is red. /ðiː ˈæpl ɪz red/
5. I'm **a** student. /aɪm ə ˈstjuːdnt/

**Config de scorare (pronunție):**
- Foneme evaluate: **/ə/** (în *a*, *an*, silabele neaccentuate), **/ð/** (în *the*), și distincția **/ðə/ vs /ðiː/**.
- Cuvinte-țintă de scorat (aliniate cu ⑦): *a pen, a book, the door, the key, the egg, the apple*.
- Prag: **≥70%** medie pe cele 6 cuvinte-țintă (coerent cu ⑦). Prag „excelent" ≥80% pt confirmare fără reluare.
- Metodă: forced-alignment + scor fonem-cu-fonem; penalizează substituția /ð/→/z/ sau /ð/→/d/ și /ə/→/a/ accentuat.
- Feedback tipic pt români: „Not 'ze door' — put your tongue between your teeth: /ðə/." · „'a' is short and soft: /ə/, not a strong 'a'." · „the egg → /ðiː/ (vowel!), the door → /ðə/ (consonant)."

**Set de shadowing (repetă imediat după model, 3-5):**
1. It's a pen. 
2. The book is red. 
3. It's an egg. 
4. The door is open. 
5. I'm a student.

## STRATUL 3 — Consolidare & evaluare

### E. Pachet SRS (carduri live)

| Front | Back | Tip | Notă |
|---|---|---|---|
| It's a pen. | Este un stilou. | EN→RO | a + consoană |
| Este un ou. | It's an egg. | RO→EN | an + vocală |
| It's ___ apple. | an | cloze | vocală → an |
| Is it a key? | Este o cheie? | EN→RO | întrebare *Is it...?* |
| No, it isn't. | Nu, nu este. | EN→RO | negativ scurt |
| The book is red. | Cartea este roșie. | EN→RO | the + culoare |
| Sunt student. | I'm a student. | RO→EN | a la profesie (greșeală tipică) |
| I'm ___ student. | a | cloze | profesie cere a |
| She's a teacher. | Ea este profesoară. | EN→RO | a la profesie |
| He's a doctor. | El este doctor. | EN→RO | a la profesie |
| The door is open. | Ușa este deschisă. | EN→RO | the (lucru cunoscut) |
| ___ door is open. | The | cloze | lucru cunoscut → the |
| It's a blue bag. | Este o geantă albastră. | EN→RO | culoare + substantiv |
| What is it? | Ce este? | EN→RO | întrebare-cheie |
| It's an umbrella. | Este o umbrelă. | EN→RO | an + vocală (u-) |
| It's ___ umbrella. | an | cloze | „u" = sunet vocalic |
| The chair is brown. | Scaunul este maro. | EN→RO | the + culoare |
| ___ English is good. | — (nimic) | cloze | limbă → articol zero |
| English is good. | Engleza este bună. | EN→RO | articol zero |
| Este un măr. | It's an apple. | RO→EN | an + vocală |

**Config FSRS (pe scurt):**
- Tag-uri: `A1-U3`, `articles`, `a-an`, `the`, `zero-article`, `to-be`, `objects`, `colors`.
- Introducere: cardurile EN→RO și RO→EN se introduc **la finalul lecției** (după Etapa 2), max. 8-10 carduri noi/zi; cloze-urile intră a **doua zi** (după prima expunere).
- Deck: `EVA::A1::U3-articles`. Retention target ~0.9; carduri „profesie fără articol" (I'm a student) și „u→an" primesc prioritate (dificultate inițială ușor mai mare, apar mai des).
- Legătură cu ⑨: cele 15 perechi din banca Stratului 1 sunt seed-ul; cele 5 cloze suplimentare derivă din aceleași propoziții pt varietate de recall.

### F. Scenariu task-based

**Situația reală:** „**Show me your desk / Arată-mi biroul tău.**" Cursantul are 4-5 obiecte în față (sau pe un card imagine): un stilou, o carte, o cheie, un telefon, o portocală. Îi prezintă lui EVA fiecare obiect.

**Obiectivul:** numește fiecare obiect cu *a/an* corect + spune culoarea a cel puțin 2 obiecte cu *the*, plus se autoprezintă cu o profesie („I'm a student.").

**Criterii de succes MĂSURABILE:**
- ≥4/5 obiecte numite cu articol corect (*a/an* după sunet).
- ≥2 propoziții *the* + culoare corecte.
- ≥1 propoziție de profesie cu *a* („I'm a student.").
- ≤2 recast-uri necesare pentru a finaliza (autonomie).

**Rubrică de scorare LLM (0-3 pe fiecare criteriu, descriptori A1):**

| Criteriu | 3 (foarte bine) | 2 (bine) | 1 (parțial) | 0 |
|---|---|---|---|---|
| **Task completion** | Prezintă 5 obiecte + 2 culori + profesie, coerent | 4 obiecte + 1-2 culori | 2-3 obiecte, incomplet | Nu îndeplinește sarcina |
| **Accuracy (articole)** | a/an/the/— corecte peste tot | 1 eroare de articol | 2-3 erori | ≥4 erori / omite articolele |
| **Fluency** | Propoziții complete, ritm firesc, pauze scurte | Complete, cu ezitări | Cuvinte izolate, cere ajutor des | Tace / doar RO |

**Prag task:** ≥ **7/9** (≈78%, aliniat la spiritul „≥80%" din ⑦) ȘI accuracy ≥2.

**Variante:**
- *Ușor (sprijin sporit):* EVA oferă mereu 2 opțiuni („a or an?") și glosă RO.
- *Standard:* întrebări deschise „What is it?", fără opțiuni.
- *Provocare:* cursantul descrie 6 obiecte + adaugă „first mention → the" (prima mențiune *a*, apoi *the* pt același obiect).

### G. Evaluare automata (test de unitate)

**Itemi structurați** `[tip | întrebare | (opțiuni) | răspuns_corect | puncte]`:

```
[MCQ | She's ___ teacher. | a / an / the | a | 1]
[MCQ | It's ___ umbrella. | a / an / — | an | 1]
[MCQ | ___ door is open. | A / An / The | The | 1]
[MCQ | ___ English is good. | The / An / — | — | 1]
[MCQ | It's ___ egg. | a / an / the | an | 1]
[CLOZE | It's ___ pen. | | a | 1]
[CLOZE | It's ___ apple. | | an | 1]
[CLOZE | I'm ___ student. | | a | 1]
[CLOZE | ___ book is red. | | The | 1]
[CLOZE | ___ Ben is a boy. | | — | 1]
[MATCHING | Potrivește obiectul cu articolul corect | pen→? ; egg→? ; orange→? ; key→? | pen=a; egg=an; orange=an; key=a | 2]
[MATCHING | Potrivește obiectul cu culoarea din dialog | pen ; book ; egg → red ; blue ; white | pen=red; book=blue; egg=white | 2]
[REORDER | it / a / is / pen | | It is a pen. | 1]
[REORDER | an / it / egg / is | | It is an egg. | 1]
[REORDER | blue / the / is / book | | The book is blue. | 1]
[TRANSLATE-CHECK | Traduceți: „Este un ou." | | It's an egg. | 1]
[TRANSLATE-CHECK | Traduceți: „Sunt student." | | I'm a student. | 1]
[TRANSLATE-CHECK | Traduceți: „Ușa este albastră." | | The door is blue. | 1]
[ERROR-FIX | Corectați: „It's a apple." | | It's an apple. | 1]
[ERROR-FIX | Corectați: „He is doctor." | | He is a doctor. | 1]
```

**Logica de scorare:**
- Total puncte: **22** (2×2 la matching + 18×1).
- MCQ/CLOZE/REORDER: match exact (case-insensitive, spații normalizate); pt cloze articolul zero se acceptă răspuns gol / „—" / „nimic".
- MATCHING: punctaj parțial — 0,5 pt fiecare pereche corectă (rotunjit la item).
- TRANSLATE-CHECK & ERROR-FIX: normalizare (lowercasing, *it's ↔ it is*, *I'm ↔ I am* echivalente); corect dacă articolul-țintă e prezent și corect + fără cuvinte în plus semnificative. Ambiguu → trece la rubrica LLM.
- **Prag de promovare: ≥80% (≥18/22).** Sub prag → reluare țintită pe tipul de item ratat (ex.: multe erori *a/an* → drill fonetic D).

**Evaluare producție (vorbire/scriere) — rubrică LLM:**

| Criteriu | Descriptor A1 „PROMOVAT" | Sub prag |
|---|---|---|
| **Task completion** | Numește ≥8/10 obiecte cu articol + ≥2 propoziții *the*+culoare | <8 obiecte sau lipsă *the* |
| **Accuracy** | ≥80% articole corecte (*a/an/the/—*); *to be* corect | erori sistematice de articol |
| **Fluency** | Propoziții complete „It's a/an ___", ezitări acceptabile A1 | doar cuvinte izolate |
| **Pronunție** | /ə/ și /ð/ inteligibile; scor ≥70% pe cele 6 cuvinte-țintă | „ze/de" persistent; /a/ accentuat |

**Prag producție:** toate criteriile la nivel „PROMOVAT"; accuracy este eliminatoriu (<80% → reluare).

**MAPARE obiective ① → itemi:**

| Obiectiv ① (Stratul 1) | Itemi care îl testează |
|---|---|
| ① Numește obiect „It's a/an ___" (≥8/10) | CLOZE „It's ___ pen/apple"; REORDER „it/a/is/pen", „an/it/egg/is"; TRANSLATE „Este un ou"; producție (rubrică Task completion) |
| ② Alege *a* vs *an* după sunet (≥8/10) | MCQ „___ umbrella", „___ egg"; CLOZE „It's ___ apple"; MATCHING pen/egg/orange/key; ERROR-FIX „a apple" |
| ③ Distinge *a/an* ↔ *the* ↔ — (≥16/20) | MCQ „___ door", „___ English"; CLOZE „___ book is red", „___ Ben is a boy"; REORDER „blue/the/is/book"; TRANSLATE „Ușa este albastră" |
| ④ Explică o regulă de contrast RO-EN | ERROR-FIX „He is doctor" → „He is **a** doctor"; TRANSLATE „Sunt student"; MCQ „She's ___ teacher"; prompt oral „De ce spunem 'I'm a student'?" (rubrică LLM) |
| ⑤ Pronunță schwa /ə/ + /ðə/ vs /ðiː/ cu /ð/ (≥70%) | Secțiunea D: scorare pronunție pe *a pen, a book, the door, the key, the egg, the apple*; shadowing (rubrică Pronunție) |

---


### A1-U4 — This, that & many things · Straturile 2 & 3 (Pipeline + Consolidare)

## STRATUL 2 — Pipeline (conversație & voce cu EVA)

### A. Configurația EVA (system prompt pt unitate)

```
[SYSTEM PROMPT — EVA · A1-U4 "This, that & many things"]

ROL & PERSONA
Ești EVA, o tutore de engleză prietenoasă, caldă și foarte răbdătoare. Vorbești
cu un ADULT vorbitor nativ de ROMÂNĂ, aflat la nivel A1 (foarte începător).
Ești încurajatoare, niciodată critică. Zâmbești prin cuvinte, folosești laude
scurte („Good!", „Perfect!", „Well done!"). Vorbești rar și clar.

NIVEL & CONTROL DE NIVEL (STRICT)
- Doar A1. Gramatica permisă: verbul to be (am/is/are), a/an/the (U3),
  și NOU în această unitate: this/that/these/those + pluralul substantivelor.
- Propoziții scurte (3-6 cuvinte). Un singur concept nou pe replică.
- NU introduce timpuri verbale noi, NU present continuous, NU past, NU modale.
- NU folosi vocabular în afara listei unității + vocabularul din U1-U3.

TEMA & STRUCTURILE-ȚINTĂ DE ELICITAT
- Demonstrative: this (aproape/sg), that (departe/sg), these (aproape/pl),
  those (departe/pl). O singură formă per poziție, FĂRĂ gen.
- Întrebări-cadru: "What's this?" / "What's that?" / "What are these?" /
  "What are those?" și "Is this a/an ___?" → "Yes, it is." / "No, it isn't."
- Plural: +s / +es (box→boxes, orange→oranges) / -ies (baby→babies) /
  neregulate (man→men, woman→women, child→children, foot→feet).
- Răspunsuri model așteptate: "It's a ___." / "They're ___." / "These are ___." /
  "Those are ___."

VOCABULAR-ȚINTĂ (folosește DOAR de aici pt obiecte)
book, pen, pencil, ruler, bag, desk, chair, board, eraser, notebook, table,
cup, plate, spoon, fork, knife, key, phone, clock, door, window, box, apple,
orange, egg, banana, man/men, woman/women, child/children, boy, girl, teacher,
student, friend, foot/feet, thing/things, here, there, one, two, three.

CORECTARE PRIN RECAST (fără marcaj roșu)
- Nu spui niciodată „Greșit". Reformulezi blând forma corectă și inviți la
  repetare. Ex.: User: "Three book." → EVA: "Ah, three books! Say it: three books."
- Corectezi MAXIM un lucru pe replică (cel mai important). Restul îl lași.
- Ținte prioritare de recast: (1) -s lipsă la plural; (2) this↔these / that↔those;
  (3) pronunția /ð/ ("dis" → "this /ð/").
- După recast, laudă imediat prima încercare bună.

PROPORȚIA RO/EN (A1 = mult sprijin în română)
- ~60% engleză, ~40% română. Sarcinile-țintă și modelele sunt în engleză;
  explicațiile, încurajările și ajutorul sunt în română.
- Orice cuvânt nou primește glosă scurtă în paranteză: "these (aceștia/acestea)".

CE CERI CURSANTULUI
- Să indice obiecte aproape/departe și să spună ce sunt (sg + pl).
- Să întrebe și să răspundă „What's this? / What are these?".
- Să formeze pluralul, inclusiv 2-3 neregulate.

DACĂ USERUL TACE (>6-8 sec)
- Oferi un indiciu în română + jumătate de model: „Poți începe cu «It's a…».
  Ce vezi aproape de tine?" Apoi, dacă tot tace, dai modelul complet și ceri doar
  repetarea: „Spune după mine: It's a pen."

DACĂ USERUL GREȘEȘTE
- Recast blând (vezi mai sus) → repetare → laudă. Fără explicații gramaticale lungi;
  maxim o propoziție de regulă în română dacă e chiar necesar.

REGULI DE ÎNCHEIERE A REPLICII
- Termină aproape fiecare replică cu O SINGURĂ întrebare clară, ca userul să știe
  exact ce să spună. Nu pune două întrebări deodată.
```

### B. Fluxul conversației (3 etape)

#### Etapa 1 — GHIDAT (EVA conduce; user completează)
Structura de elicitat: `It's a ___.` / `They're ___.` + `this/that/these/those`.

| # | EVA (replică de pornire) | Structură țintă | Răspuns MODEL (user) |
|---|---|---|---|
| 1 | "Hello! Look here, near you. What's **this**?" *(arată o carte)* | this + It's a ___ | "It's a book." |
| 2 | "Yes! And what are **these**?" *(două cărți)* | these + They're ___ | "They're books." |
| 3 | "Good. Now look over **there**. What's **that**?" *(un stilou departe)* | that + It's a ___ | "It's a pen." |
| 4 | "And **those** over there?" *(mai multe stilouri)* | those + They're ___ | "They're pens." / "Those are pens." |
| 5 | "**Is this** an apple?" *(arată o portocală aproape)* | Is this…? → No, it isn't | "No, it isn't. It's an orange." |
| 6 | "Perfect! And **these** — who are they?" *(arată copii)* | plural neregulat | "They're children." |

Notă pt EVA: după fiecare răspuns corect → laudă scurtă + treci la următorul. Dacă lipsește **-s** la plural (rep. 2, 4) → recast: „Ah, book**s**! Say it again."

#### Etapa 2 — SEMI-GHIDAT (întrebări deschise + indicii)
EVA pune întrebarea, oferă un „prompt" scurt, dar userul construiește singur.

- "Look around you. Name one thing **near** you. Start with «This is a…»." *(indiciu RO: alege ceva de pe masă)*
- "Now name **two** things near you. «These are…»." *(indiciu: nu uita **-s** la plural!)*
- "What can you see **far** from you? «That is a…»." *(indiciu RO: fereastră? ușă? tablă?)*
- "Ask **me** a question about this object." *(indiciu: folosește «What's this?» sau «Is this a…?»)*
- "Say the plural: one man → …? one child → …? one foot → …?" *(indiciu RO: sunt neregulate!)*

Branching indiciu: dacă userul dă o formă regulată la neregulat (ex. „childs") → recast: „Almost! Not «childs» — **children**. Say it: children."

#### Etapa 3 — LIBER (scenariu + obiectiv)
**Scenariul:** „My desk and the shelf." Userul are pe masa lui (aproape) câteva obiecte reale și, la distanță, o poliță/un raft cu alte obiecte. EVA joacă un prieten curios care întreabă ce e pe masă și ce e pe raft.

**Obiectiv (userul):** să descrie ≥6 obiecte folosind corect **this/that/these/those** + să producă ≥2 forme de plural, dintre care ≥1 neregulat, și să pună ≥1 întrebare („What's that?" / „Is this a…?").

**Branching EVA:**
- *User corect* → laudă + escaladează: „Nice! Now tell me about **two** of them." (împinge spre plural).
- *User greșește forma demonstrativului* (this↔these etc.) → recast punctual: „One book → **this**. Two books → **these**. Try again."
- *User uită -s la plural* → recast + repetare, apoi continuă.
- *User tace >8 sec* → indiciu RO + jumătate de model: „Poți spune «On my desk, this is a…». Ce e cel mai aproape de mâna ta?"
- *User iese din vocabular* (obiect necunoscut) → EVA oferă cuvântul în engleză cu glosă: „That's a «cup» (cană). Say: this is a cup."
- *Închidere*: „Great job, [nume]! You used this, that, these and those. Bye for now!"

### C. Ascultare (script audio pt TTS + itemi)

**Script audio — „In the classroom" (~40 sec, 2 voci: TEACHER + LILA).** *De generat cu TTS, ritm lent, pauze după fiecare replică.*

> **TEACHER:** Good morning, Lila. Look at the desk. What's this?
> **LILA:** It's a pen.
> **TEACHER:** Yes. And what are these?
> **LILA:** They're pencils. Three pencils.
> **TEACHER:** Good! Is this a book?
> **LILA:** No, it isn't. It's a notebook.
> **TEACHER:** And those things over there — on the table?
> **LILA:** Those are cups. Two cups.
> **TEACHER:** Very good, Lila! And who are these children?
> **LILA:** They're my friends. This is Tom, and that is Ben.

**Itemi de comprehensiune (5):**
1. What's on the desk first — a pen or a book? *(alege)*
2. How many pencils are there?
3. Is the second object a book?
4. What are the things on the table? Are they near or far?
5. Who are Tom and Ben?

**Răspunsuri:** 1. A pen. 2. Three (pencils). 3. No, it isn't — it's a notebook. 4. They're cups (two cups); far / over there → „those". 5. They're Lila's friends (children).

### D. Pronunție (drill + scorare)

**Sunete-țintă (RO-focus):**
- **/ð/** (th sonor) — românii tind să spună „d" sau „z". Limba atinge ușor dinții de sus, coardele vibrează.
- **Terminații de plural**: /s/ (surd), /z/ (sonor), /ɪz/ (silabă în plus).

**Minimal pairs (perechi de contrast):**
- /ð/ vs /d/: **they /ð/** – day /d/ · **there /ð/** – dare /d/ · **those /ð/** – doze /d/
- /ð/ vs /z/: **these /ð/** – Z's /z/ · **then /ð/** – Zen /z/
- plural /s/ vs /z/: desks /s/ – pens /z/ · books /s/ – keys /z/

**Listă de cuvinte (drill /ð/ — 6 cuvinte-țintă, cf. obiectiv ⑤):**
`this · that · these · those · the · they`

**Propoziții de drill (5):**
1. **This** is a book.
2. **These** are **the** pens.
3. **That** is a chair; **those** are chairs.
4. **They** are **there**, over **there**.
5. **These** children are here; **those** men are **there**.

**Config de scorare (pronunție):**
- Foneme evaluate: **/ð/** (obligatoriu, prioritar) + **terminația de plural /s z ɪz/** pe cuvintele: books, desks, cups (/s/); pens, keys, chairs (/z/); boxes, oranges (/ɪz/).
- Prag: scor **≥80** (echiv. ≥7/10 pe cele 6 cuvinte /ð/, cf. obiectiv ⑤). Sub 80 → un ciclu de shadowing + reîncercare.
- Feedback tipic pt români:
  - `/ð/` realizat ca [d] („dis") → „Nu «dis», ci «this»: pune vârful limbii ușor între dinți și lasă vocea să vibreze."
  - `/ð/` realizat ca [z] („zis") → „Nu «zis» — «this». Limba atinge dinții de sus, nu fluieră."
  - `-s` omis la plural („three book") → „Adaugă sunetul final: book**s** /s/."
  - `/ɪz/` redus („box" în loc de „boxes") → „boxes = box + **iz**, o silabă în plus."

**Set de shadowing (repetă după TTS, 5 propoziții):**
1. This is a pen.
2. These are books.
3. That is an apple.
4. Those are oranges.
5. These children are my friends.

## STRATUL 3 — Consolidare & evaluare

### E. Pachet SRS (carduri live)

| Front | Back | Tip | Notă |
|---|---|---|---|
| This is a book. | Aceasta este o carte. | EN→RO | din ⑨ · demonstrativ sg aproape |
| Aceasta este o carte. | This is a book. | RO→EN | din ⑨ · producție |
| That is a pen. | Acela este un stilou. | EN→RO | din ⑨ · sg departe |
| These are apples. | Acestea sunt mere. | EN→RO | din ⑨ · pl aproape |
| Acestea sunt mere. | These are apples. | RO→EN | din ⑨ · atenție -s |
| Those are oranges. | Acelea sunt portocale. | EN→RO | din ⑨ · pl departe + /ɪz/ |
| What's this? | Ce este acesta? | EN→RO | din ⑨ · întrebare-cadru |
| Ce sunt acestea? | What are these? | RO→EN | din ⑨ · are + these |
| Is this an egg? | Este acesta un ou? | EN→RO | din ⑨ · Yes/No + an |
| No, it isn't. | Nu, nu este. | EN→RO | din ⑨ · răspuns scurt |
| This man is a teacher. | Acest bărbat este profesor. | EN→RO | din ⑨ · this + man |
| These children are here. | Acești copii sunt aici. | EN→RO | din ⑨ · pl neregulat |
| Those women are teachers. | Acele femei sunt profesoare. | EN→RO | din ⑨ · woman→women |
| Look at these keys. | Uită-te la aceste chei. | EN→RO | din ⑨ · keys /z/ |
| Two feet, one foot. | Două picioare, un picior. | EN→RO | din ⑨ · foot→feet |
| These are my friends. | Aceștia sunt prietenii mei. | EN→RO | din ⑨ · producție pl |
| One man → two ___. | men | cloze | plural neregulat |
| One child → two ___. | children | cloze | plural neregulat |
| One box → two ___. | boxes | cloze | +es · /ɪz/ |
| This is a chair. ___ are chairs. | These | cloze | sg→pl aproape |
| That is a pen. ___ are pens. | Those | cloze | sg→pl departe |
| ___ this an apple? — No, it isn't. | Is | cloze | întrebare to be |

**Config FSRS (pe scurt):**
- Tag-uri: `A1`, `U4`, `demonstratives`, `plural`, `plural-irregular`, `phon-/ð/`, `phon-/s z ɪz/`.
- Moment de introducere: cardurile EN→RO se introduc imediat după lecție (Faza 1). Cardurile RO→EN și cloze se activează după ce cursantul a trecut o dată prin task-ul ⑧ (producție ghidată).
- Ordine: întâi demonstrative sg (this/that), apoi pl (these/those), apoi plural neregulat.
- Interval inițial: 1 zi; ease standard. Cardurile marcate „lapse" (ex. -s omis la plural, this↔these) reintră la interval scurt + se leagă de un drill de pronunție (D).
- Reactivare vocabular: extrage 5-8 cuvinte din cele 50 la fiecare sesiune de review (țintă retenție ≥70%, cf. ⑦).

### F. Scenariu task-based

**Situația reală:** „Show me your desk." Cursantul stă la biroul/masa lui reală. Aproape are câteva obiecte (pe masă), iar la distanță — un raft, o fereastră sau o ușă. EVA (prieten curios prin chat/voce) îi cere un mic tur al lucrurilor din jur.

**Obiectivul cursantului:** să descrie lucrurile aproape și departe, la singular și plural, și să poarte un mini-schimb de întrebări/răspunsuri cu EVA.

**Criterii de succes (măsurabile):**
- Folosește corect **cele 4 demonstrative** (this, that, these, those) — cel puțin 1 dată fiecare.
- Produce **≥3 forme de plural** corecte, dintre care **≥1 neregulat** (men/women/children/feet).
- Pune **≥1 întrebare** validă („What's that?" / „Is this a…?").
- Menține structura *to be* (It's / They're / These are / Those are) fără erori de acord în ≥80% din replici.

**Rubrică de scorare LLM (0-4 per criteriu; prag total ≥80% = ≥9.6/12):**

| Criteriu | Descriptor A1 (4 = țintă) | 2 (parțial) | 0 |
|---|---|---|---|
| **Task completion** | Descrie ≥6 obiecte aproape/departe și duce turul la capăt | Descrie 3-5 obiecte, tur incomplet | <3 obiecte / abandon |
| **Accuracy** | Demonstrative + plural (incl. 1 neregulat) corecte; acord to be corect | Câteva erori (-s omis sau this↔these) dar mesajul e clar | Erori sistematice care blochează sensul |
| **Fluency** | Răspunde prompt, propoziții scurte legate, ezitări mici | Pauze dese, are nevoie de indicii | Tăceri lungi, doar cuvinte izolate |

**Variante ale scenariului:**
- V1 „In the kitchen" — cup, plate, spoon, fork, knife, apple, banana, egg.
- V2 „In my bag" — book, pen, pencil, key, phone, notebook.
- V3 „People here and there" — boy, girl, man/men, woman/women, child/children, teacher, student, friend.

### G. Evaluare automată (test de unitate)

**Itemi structurați** — format: `[tip | întrebare | (opțiuni) | răspuns_corect | puncte]`

```
[MCQ | Near you, singular: "___ is a book." | this/that/these/those | this | 1]
[MCQ | Far, plural: "___ are pens over there." | this/that/these/those | those | 1]
[MCQ | "This is (a/an) orange." | a/an | an | 1]
[cloze | Plural: one child → two ___ | | children | 1]
[cloze | Plural: one foot → two ___ | | feet | 1]
[cloze | Plural: one box → two ___ | | boxes | 1]
[cloze | Question word + be: "___ these your friends?" | | Are | 1]
[cloze | Near, plural: "This is a chair. ___ are chairs." | | These | 1]
[matching | Potrivește sg cu pl | man;woman;child;foot;box → men;women;children;feet;boxes | man=men, woman=women, child=children, foot=feet, box=boxes | 5]
[matching | Clasifică terminația de plural | books;pens;boxes;desks;keys;oranges → /s/;/z/;/ɪz/ | books=/s/, pens=/z/, boxes=/ɪz/, desks=/s/, keys=/z/, oranges=/ɪz/ | 6]
[reorder | these / books / are | | These are books. | 1]
[reorder | that / is / a / pen | | That is a pen. | 1]
[reorder | what / are / those | | What are those? | 1]
[translate-check | Traduce: "Ce sunt acestea?" | | What are these? | 2]
[translate-check | Traduce: "Aceștia sunt bărbați." | | These are men. | 2]
[translate-check | Traduce: "Acela este un stilou." | | That is a pen. | 2]
[MCQ | "Is this an egg?" — răspuns scurt negativ corect | "No, it isn't."/"No, it doesn't."/"No, they aren't." | No, it isn't. | 1]
```

**Logica de scorare & prag:**
- Punctaj total = **30 p**. **Prag de promovare: ≥80% = ≥24/30.**
- MCQ / cloze / reorder: potrivire exactă (case-insensitive, spații normalizate, punctuația finală ignorată).
- matching: punctaj parțial, 1 p per pereche corectă.
- translate-check: acceptă variante echivalente A1 (ex. contracție „That's" ≈ „That is"; „These are men" acceptat; formă cu -s obligatorie la plural — „These are man" = 0).
- Sub prag → reia drill-ul demonstrative + plural (B/D) și cardurile SRS marcate lapse.

**Producție (vorbire/scriere) — rubrică LLM (prag ≥80%):** se aplică rubrica din secțiunea F (task completion / accuracy / fluency, descriptori A1). Pentru pronunție, prag ≥80 pe /ð/ + terminații plural (config din D).

**MAPARE obiective ① → itemi de test:**

| Obiectiv ① (Strat 1) | Itemi care îl testează |
|---|---|
| **① Ob.1** — this/that/these/those (≥8/10) | MCQ 1, MCQ 2, cloze „These are chairs", reorder 1 & 3, translate-check „Acela este un stilou" + task F (folosire toate 4) |
| **① Ob.2** — plural sg→pl, regulat+neregulat (≥10, ≥2 nereg.) | cloze children/feet/boxes, matching sg-pl (5 perechi), translate-check „Aceștia sunt bărbați" |
| **① Ob.3** — clasificare /s z ɪz/ (≥80% din 8) | matching „Clasifică terminația" (6 cuvinte) + drill-scoring D |
| **① Ob.4** — What's this? / What are these? cu to be (schimb 4 replici) | cloze „Are these…", reorder „what are those", MCQ „No, it isn't." + Etapa 1/task F (mini-schimb) |
| **① Ob.5** — pronunție /ð/ (≥7/10 pe 6 cuvinte) | Secțiunea D: drill /ð/ pe this/that/these/those/the/they + shadowing, scorare ≥80 |

---


I have everything I need from Layer 1. Producing Layers 2 & 3 now, coherent with the exact text, vocabulary, task ⑧ and SRS bank ⑨.

### A1-U5 — My family · Straturile 2 & 3 (Pipeline + Consolidare)

## STRATUL 2 — Pipeline (conversatie & voce cu EVA)

### A. Configuratia EVA (system prompt pt unitate)

```
SYSTEM PROMPT — EVA · A1-U5 "My family"

ROL & PERSONA
Esti EVA, o tutore AI de engleza: calda, rabdatoare, incurajatoare, prietena. Vorbesti cu un ADULT vorbitor de romana, nivel A1. Chat-first (WhatsApp/Messenger): mesaje SCURTE (1-3 propozitii), emoji ocazional (😊), 1 singura intrebare pe replica.

NIVEL & LIMBAJ
- Doar A1. Propozitii scurte, prezent simplu, vocabular din U1-U5.
- Gramatica permisa pana aici: to be; a/an/the; this/that/these/those; plurale; have got/has got; adjective posesive (my/your/his/her/its/our/their). NU folosi alte timpuri, modale sau structuri.
- Foloseste EXCLUSIV vocabularul-tinta al unitatii (family, mother, father, brother, sister, son, daughter, child/children, grandmother/grandfather, husband/wife, uncle/aunt, cousin, nephew/niece, pet, dog, cat, fish, bird, rabbit, hamster, horse, married/single/divorced, twins, baby...).

PROPORTIA RO/EN (A1)
- ~70% engleza / ~30% romana. Engleza = continutul-tinta. Romana = doar sprijin: traducere intre paranteze pt intrebari noi, o incurajare, sau o mini-explicatie de 1 rand cand userul se blocheaza.
- Format tipic: "English sentence? (traducere RO scurta)".

STRUCTURI DE ELICITAT (obiectivul conversatiei)
1. have got / has got — afirmativ, negativ, interogativ ("I've got...", "She's got...", "I haven't got...", "Have you got...?", "Yes, I have. / No, I haven't.").
2. Adjective posesive inaintea substantivului (my brother, her cat, their dog).
3. Vocabular de familie + animale de companie.
Provoaca userul sa PRODUCA aceste structuri, nu doar sa le recunoasca.

REGULI DE CORECTARE — RECAST (bland, fara rosu)
- NU spune "gresit". Reformuleaza corect natural, apoi mergi mai departe cu o intrebare.
  User: "She have got a cat." → EVA: "Ah, she HAS got a cat! 🐱 What's her cat's name?"
  User: "His sister" (pt o fata) → EVA: "Yes — HER sister. (fata → her) And has she got a pet?"
- Corecteaza MAXIM 1 lucru pe replica (cel mai important). Restul le lasi.
- Confirma continutul inainte de forma: intai "Nice!", apoi recast.

GRESELI TIPICE ROMANI (de urmarit)
- "She have got" → has got.
- his/her dupa OBIECT in loc de POSESOR → fata=her, baiat=his, indiferent ce urmeaza.
- lipsa articolului: "I've got brother" → "I've got A brother".
- /ð/ pronuntat "d"/"z" (mother, father) — la nevoie da un mic indiciu fonetic.

REACTIE LA TACERE / BLOCAJ
- Dupa ~1 replica fara raspuns: ofera 2 optiuni sau un model. "You can say: 'I've got a brother.' Now you try 😊 (Ai un frate sau o sora?)"
- Daca userul scrie in romana: accepta, apoi ofera varianta EN si cere-i sa o repete.
- Nu incarca: o intrebare, un pas, mult sprijin pozitiv.

OBIECTIV DE SESIUNE
Userul sa prezinte 3-4 membri ai familiei si sa spuna ce/pe cine are (have got + posesive) + daca are un animal. Inchei cu un rezumat cald + o mini-lauda concreta.
```

### B. Fluxul conversatiei (3 etape)

#### Etapa 1 — GHIDAT (EVA porneste, user completeaza pe model)

Fiecare replica EVA elic o structura tinta. Raspunsul MODEL = ce vrem sa iasa.

| # | EVA (replica de pornire) | Raspuns MODEL (user) | Structura de elicitat |
|---|---|---|---|
| 1 | Hi! I'm EVA. 😊 Have you got a big family? *(Ai o familie mare?)* | Yes, I've got a big family. | `have got` afirmativ (I) |
| 2 | Nice! Have you got any brothers or sisters? | I've got one brother and two sisters. | `have got` + vocabular familie |
| 3 | Great! What are their names? *(Cum ii cheama?)* | My brother is Andrei. My sisters are Ana and Ioana. | posesiv `my` + `their` inteles |
| 4 | Lovely! Has your mother got a pet? *(Mama ta are un animal?)* | Yes, she's got a cat. / No, she hasn't. | `has got` pers. III + raspuns scurt |
| 5 | And you — have you got a pet at home? | Yes, I've got a dog. / No, I haven't got a pet. | `have got` afirm./neg. |
| 6 | What's your dog's name? Tell me about it! 🐶 | His name is Max. My dog is big. | posesiv `his/its` + descriere |

**Structura tinta de iesire (Etapa 1):** min. 4 propozitii cu have/has got + min. 2 posesive corecte.

#### Etapa 2 — SEMI-GHIDAT (intrebari deschise + indicii)

EVA pune intrebari mai largi; ofera "prompts" doar daca userul ezita.

- **EVA:** Tell me about your family. Who is in your family? *(Cine e in familia ta?)*
  - *prompt:* You can start with "I've got..." (mother? father? brothers?)
- **EVA:** Have your grandparents got any pets?
  - *prompt:* "My grandmother has got..." / "They haven't got..."
- **EVA:** Who is your favourite person in the family? What has he or she got?
  - *prompt:* fata → "She's got... / Her..." · baiat → "He's got... / His..."
- **EVA:** Have you got cousins? How many? *(Ai verisori? Cati?)*
  - *prompt:* "I've got two cousins. Their names are..."

**Iesire asteptata:** 5-6 propozitii, userul alege continutul, EVA face recast la 1 greseala/replica.

#### Etapa 3 — LIBER (scenariu + obiectiv, cu branching)

**Scenariul:** *„The family photo"* — Userul „ii arata" lui EVA o poza cu familia (real sau imaginat) si o prezinta.

**Obiectiv:** prezinta **3-4 membri**, spune **ce/pe cine are** (have got + posesive) si daca are **un animal de companie** — coerent cu sarcina ⑧ din Stratul 1.

**Deschidere EVA:** "Show me your family photo! 📸 Who is this? Tell me about 3 or 4 people. *(Prezinta-mi 3-4 persoane.)*"

**Branching — ce face EVA:**

| Situatie | Reactia EVA |
|---|---|
| User produce corect | "Wonderful! 😊" + intrebare de aprofundare ("Has he got a pet, too?"). |
| Greseala de forma (have/has, his/her, articol) | RECAST natural + continua: "Ah, she HAS got a sister! And her sister — is she married?" |
| User da raspuns f. scurt (1 cuvant) | Cere extindere cu model: "Tell me more — 'This is my ___. She's got ___.'" |
| User tace (>1 replica) | Ofera 2 optiuni + traducere: "Have you got a brother or a sister? (frate sau sora?)" |
| User scrie in romana | Accepta continutul, ofera EN si cere repetare: "In English: 'Am o sora' = 'I've got a sister.' Try it 😊" |
| User cere ajutor / "I don't know" | Da un mini-model + reia: "No problem. Say: 'This is my mother. Her name is Maria.' Now you 😊" |

**Inchidere EVA:** rezumat cald + 1 lauda concreta: "Great job! You told me about your brother and your dog Max. You used 'have got' really well! 🌟"

### C. Ascultare (script audio pt TTS + itemi)

**Script audio (monolog scurt A1, ~45-55 s, voce feminina calma, ~0.9x viteza):**

```
[TITLU: Anna's family]

Hello! My name is Anna. I've got a big family.
I've got a mother, a father, and two brothers.
Their names are Paul and Mark.
I haven't got a sister.
My mother has got a cat. Her cat is small and white.
My father has got a dog. His name is Rex.
Rex is big and brown.
My grandmother has got a pet, too — a little bird!
I love my family. 😊
```

**Note TTS:** accentueaza usor /ð/ in *mother, father, brother, their*; pauza scurta dupa fiecare propozitie; nume proprii clare (Paul, Mark, Rex, Anna).

**Itemi de comprehensiune:**

1. Has Anna got a big family? *(Da/Nu)*
2. How many brothers has Anna got? (one / two / three)
3. Has Anna got a sister?
4. What is the dog's name?
5. What pet has Anna's grandmother got?

**Raspunsuri:**
1. Yes, she has. 2. Two. 3. No, she hasn't. 4. His name is Rex. 5. A (little) bird.

### D. Pronuntie (drill + scorare)

**Sunete-tinta (RO-focus):** /ð/ (sonor, „d" moale intre limba si dinti) vs /θ/ (surd). Romanii tind sa spuna „d"/„z" in loc de /ð/ si „t"/„s" in loc de /θ/.

**Minimal pairs (perechi de contrast):**

| /ð/ (sonor) | /θ/ (surd) |
|---|---|
| they /ðeɪ/ | thay/think (θ) — *think* /θɪŋk/ |
| father /ˈfɑː.ðə/ | (contrast: *thin* /θɪn/) |
| then /ðen/ | thin /θɪn/ |
| breathe /briːð/ | breath /breθ/ |
| the /ðə/ | three /θriː/ |

**Lista de cuvinte (drill):** mother · father · brother · the · they · their *(/ð/)* — vs — think · three · thank you · mouth *(/θ/)*.

**Propozitii de drill:**
1. My **mother** and **father** are **the**re.
2. **They**'ve got **the**ir dog.
3. **Th**is is my **br**o**th**er.  *(atentie: /ð/ in brother)*
4. **Th**ank you — **th**ree **th**ings. *(/θ/ de contrast)*
5. My **grandmother** and **grandfather** love **the**ir cat.

**Config de scorare (pronuntie):**
- Foneme evaluate: **/ð/** (prioritar) si **/θ/** (contrast), pe cuvintele-model: *mother, father, brother, the, they, their*.
- Prag de trecere: **≥70%** (coerent cu DoD din ⑦). Scor per cuvant = corect (/ð/ produs, nu „d/z") sau incorect.
- Feedback tipic pt romani:
  - Detectat „d" in loc de /ð/ → "Aproape! Pune varful limbii intre dinti si sufla usor cu voce: mo-**th**-er, nu 'mo-**d**-er'. 😊"
  - Detectat „z" in loc de /ð/ → "Fara suierat — /ð/ e moale, cu limba intre dinti: **the**, nu 'ze'."
  - Confuzie /ð/↔/θ/ → "**They** are voiced (cu voce), **three** is quiet (fara voce). Simte gatul: la 'they' vibreaza."

**Set de shadowing (repeta dupa model, 3-5):**
1. This is my mother.
2. They've got their dog.
3. My brother has got a cat.
4. Her father and grandfather are nice.
5. Thank you — this is the truth. *(mix /ð/+/θ/)*

## STRATUL 3 — Consolidare & evaluare

### E. Pachet SRS (carduri live)

Bazate pe banca ⑨ + vocabularul ② al unitatii.

| Front | Back | Tip | Nota |
|---|---|---|---|
| I've got a big family. | Am o familie mare. | EN→RO | have got afirm. |
| I've got a brother and a sister. | Am un frate si o sora. | EN→RO | vocab + have got |
| She's got two children. | Ea are doi copii. | EN→RO | has got + plural neregulat |
| He hasn't got a pet. | El nu are animal de companie. | EN→RO | have got negativ |
| Have you got any brothers? | Ai (vreun) frate? | EN→RO | interogativ + any |
| Yes, I have. / No, I haven't. | Da, am. / Nu, n-am. | EN→RO | raspunsuri scurte |
| This is my mother. | Aceasta este mama mea. | RO→EN | posesiv my |
| Her name is Ana. | Numele ei este Ana. | RO→EN | posesiv her |
| His father is a teacher. | Tatal lui este profesor. | EN→RO | posesiv his |
| Our grandparents are nice. | Bunicii nostri sunt draguti. | EN→RO | posesiv our |
| Their dog is small. | Cainele lor este mic. | RO→EN | posesiv their |
| My sister has got a cat. | Sora mea are o pisica. | RO→EN | my + has got |
| We haven't got a dog. | Nu avem caine. | EN→RO | have got negativ (we) |
| Has she got a brother? | Ea are un frate? | RO→EN | interogativ has |
| I've got a grandmother and a grandfather. | Am o bunica si un bunic. | EN→RO | vocab bunici |
| She ____ got a cat. (has/have) | has | cloze | pers. III = has |
| Tom has got a dog. ____ dog is big. (posesiv) | His | cloze | baiat → his |
| Maria has got a brother. ____ brother is tall. | Her | cloze | fata → her |
| I've got ____ brother. (articol) | a | cloze | articol obligatoriu |
| mother /ˈmʌð.ə/ | mama | EN→RO | /ð/ focus |

**Config FSRS (pe scurt):**
- **Tag-uri:** `A1-U5`, `have_got`, `possessives`, `family_vocab`, `phonics_th`.
- **Moment de introducere:** carduri de recunoastere (EN→RO) imediat dupa lectura ③; cloze (has/have, his/her, articol) dupa nota de gramatica ④; RO→EN (productie) dupa Etapa 1-2 din conversatie.
- **Intervale:** default FSRS; carduri de tip cloze (his/her, has/have) marcate ca „leech-prone" → repetare mai frecventa la esec. Retention target 0.9.
- **Prioritate zilnica:** intai cloze-gramatica, apoi RO→EN productie, apoi EN→RO recunoastere.

### F. Scenariu task-based

**Situatia reala:** Userul primeste (in chat) o „poza de familie" si o prezinta lui EVA — coerent cu sarcina ⑧. Context: se pregateste sa vorbeasca despre familie cu un prieten strain.

**Obiectiv:** prezinta **3-4 membri** ai familiei, spune **ce/pe cine are** (have got + posesive) si daca are **un animal de companie**; raspunde la 2-3 intrebari de la EVA.

**Criterii de succes MASURABILE:**
- ≥ **6 propozitii** produse despre familie.
- **have got / has got** folosit corect in ≥ **4** propozitii.
- ≥ **2** adjective posesive corecte (inclusiv his/her dupa posesor).
- ≥ **1** raspuns corect la o intrebare a EVA (Yes, I have. / No, she hasn't.).
- Prezinta **3-4 membri** distincti + mentioneaza (ai/nu ai) un animal.

**Rubrica de scorare LLM (0-4 per criteriu, descriptori A1):**

| Criteriu | 4 (foarte bine) | 3 (bine) | 2 (in curs) | 1 (insuficient) |
|---|---|---|---|---|
| **Task completion** | 4 membri + animal + raspunde la intrebari | 3 membri + animal | 2-3 membri, incomplet | <2 membri / off-task |
| **Accuracy** (have got + posesive) | ≥4 have/has got corecte, posesive corecte | 1-2 greseli minore | 3-4 greseli, sens clar | forme gresite sistematic |
| **Fluency** (A1) | propozitii scurte fluente, fara blocaje mari | mici ezitari, se recupereaza | pauze dese, are nevoie de prompts | depinde total de sprijin RO |

**Prag:** promovare task la **≥ 8/12** (si min. „2" la fiecare criteriu).

**Variante:**
- V1 „My best friend's family" (posesive his/her intensiv).
- V2 „My grandparents" (grandmother/grandfather/grandparents + has got).
- V3 „My pets" (pet vocab + have got afirm./neg.).

### G. Evaluare automata (test de unitate)

**Itemi structurati** `[tip | intrebare | (optiuni) | raspuns_corect | puncte]`:

```
[MCQ | She ___ got two sisters. | have / has / haves | has | 1]
[MCQ | ___ you got a pet? | Have / Has / Do | Have | 1]
[MCQ | Tom has got a dog. ___ dog is big. | His / Her / Their | His | 1]
[MCQ | Maria has got a cat. ___ cat is white. | His / Her / Its | Her | 1]
[MCQ | Tom and Ana have got a cat. ___ cat is small. | His / Her / Their | Their | 1]
[CLOZE | I've got ___ brother. (articol) | — | a | 1]
[CLOZE | We ___ got a dog. (negativ, have) | — | haven't | 1]
[CLOZE | ___ she got a brother? (interogativ) | — | Has | 1]
[REORDER | got / I / a / brother / 've | — | I've got a brother. | 1]
[REORDER | she / got / a / has / cat / ? | — | Has she got a cat? | 1]
[MATCHING | I·you·he·she·we·they → posesive | my/your/his/her/our/their | I-my, you-your, he-his, she-her, we-our, they-their | 3]
[TRANSLATE | Am o sora. (RO→EN, have got) | — | I've got a sister. | 1]
[TRANSLATE | Ea are un caine. | — | She's got a dog. | 1]
[TRANSLATE | Aceasta este mama mea. | — | This is my mother. | 1]
[TRANSLATE | Bunica mea are o pisica. | — | My grandmother has got a cat. | 1]
[LISTEN | (audio C) How many brothers has Anna got? | one / two / three | two | 1]
[LISTEN | (audio C) Has Anna got a sister? | Yes / No | No | 1]
```

**Logica de scorare:**
- MCQ / LISTEN: match exact al optiunii → puncte.
- CLOZE: normalizare (lowercase, trim, accepta forme contrase: `haven't` = `have not`).
- REORDER: match pe secventa corecta (ignora capitalizare/spatii; accepta variante de punctuatie finala).
- MATCHING: 0.5p per pereche corecta (6 perechi = 3p).
- TRANSLATE-check: acceptare fuzzy — corect daca (a) structura have/has got prezenta unde e ceruta, (b) posesivul corect, (c) lexicul-tinta corect; accepta `I've got`=`I have got`, `She's got`=`She has got`. Greseli de scriere minore neignifiante nu penalizeaza daca cuvantul-cheie e recognoscibil.
- **Total: 20 puncte. Prag de promovare: ≥ 80% (≥ 16/20).**

**Pt productie (vorbire/scriere) — rubrica LLM (descriptori A1):**

| Criteriu | Descriptor A1 | Prag |
|---|---|---|
| Task completion | descrie ≥6 propozitii despre familie, 3-4 membri + animal | atins daca ≥6 propozitii on-task |
| Accuracy | have/has got + posesive corecte in majoritate (≥4/6) | ≥ 4 corecte din 6 |
| Fluency | propozitii scurte inteligibile, minim sprijin RO | fara blocaje care opresc comunicarea |
| Pronuntie /ð/ | *mother, father, brother, the, they, their* | scor ≥ 70% |

**Prag global productie:** „atins" la Task completion + Accuracy + Pronuntie (coerent cu DoD ⑦).

**MAPARE obiectiv ① → itemi:**

| Obiectiv ① (CAN-DO) | Itemi care il testeaza |
|---|---|
| Numeste membrii familiei (≥12/15) | SRS EN→RO vocab; TRANSLATE „sister/mother/grandmother"; LISTEN Q2 |
| Spune ce/pe cine are (have got/has got, afirm/neg/interog) | MCQ have/has, Have you; CLOZE haven't, Has she; REORDER 1-2; TRANSLATE 1-2, 4; rubrica Accuracy |
| Exprima posesia (my/your/his/her/our/their) | MCQ his/her/their (3 itemi); MATCHING posesive; TRANSLATE „my mother"; CLOZE articol/posesiv |
| Descrie propria familie (≥6 propozitii, scris/oral) | Scenariu F + rubrica productie (Task completion) |
| Pronunta /ð/ distinct de /θ/ (≥70%) | Sectiunea D scorare + rubrica productie Pronuntie |

---


### A1-U6 — Numbers & Age · Straturile 2 & 3 (Pipeline + Consolidare)

## STRATUL 2 — Pipeline (conversatie & voce cu EVA)

### A. Configuratia EVA (system prompt pt unitate)

```
ROL & PERSONA
Ești EVA, un tutore AI de engleză prietenos, cald, calm și foarte răbdător. Vorbești
cu un ADULT/adolescent VORBITOR DE ROMÂNĂ care este la nivelul A1 și învață engleza
prin conversație scrisă și vocală (chat-first, ca pe WhatsApp). Ești un „young robot"
și poți glumi ușor despre asta (ai 1 an). Ton: încurajator, niciodată critic.

NIVEL & LIMITĂ DE CONȚINUT (foarte important)
- Nivel STRICT A1. Folosești DOAR structuri predate până la U6:
  to be (am/is/are), have got, imperativ simplu (count, listen), numere 0–100,
  How old…?, How many…? + plural, How much…? pentru preț.
- NU folosești: present simple (I work/like), can, there is/are, present continuous,
  past tense, condiționale, vocabular peste A1. Dacă ai nevoie de un cuvânt nou,
  îl explici imediat în paranteză în română.
- Propoziții SCURTE (3–8 cuvinte). O singură idee/întrebare pe replică.

TEMA UNITĂȚII
Numere 0–100, vârsta (How old are you? → I'm … years old), câți/câte (How many…?),
numere de telefon (citite cifră cu cifră, „oh" pentru 0), prețuri simple
(pounds/euros/dollars, cheap/expensive/free).

STRUCTURI DE ELICITAT (cere-le activ de la cursant)
1. „How old are you?" → „I'm … (years old)." (verbul TO BE, nu have)
2. Numărat cu voce tare 0–20, apoi zeci: 10, 20, 30 … 100.
3. „What's your phone number?" → citit cifră cu cifră.
4. „How many … have you got?" → „I've got … ."
5. „How much is …?" → „It's … pounds/euros." + cheap/expensive.

VOCABULAR-ȚINTĂ (elicitează și reia)
numbers 0–100, age, old, young, years old, birthday, phone (number), mobile, call,
money, price, pound, euro, dollar, cent, cheap, expensive, free, how much, how many,
count, thanks, please, shop.

CORECTARE PRIN RECAST (blând, NU marcaj roșu)
- Nu spui niciodată „Greșit!". Reformulezi corect modelul, apoi îl reiei ca întrebare.
  Ex.: Cursant: „I have twelve years." → EVA: „Ah, in English we say: I'm twelve
  years old. 🙂 So — how old are you again?"
- Greșeala #1 de urmărit: *I have … years* (calc după română). Recast obligatoriu spre
  *I'm … (years old)*, cu o notă scurtă în RO: „(în engleză vârsta cu «a fi», nu «a avea»)".
- Greșeala #2: confuzia -teen/-ty (fifteen/fifty, nineteen/ninety). Recast + contrast:
  „fifTEEN — 15, accent la final; FIFty — 50. You mean 15? 🙂"
- Pronunție /θ/ (three, thirteen, thirty, thanks): dacă apare *tree*/*free*, notează
  blând: „«three» — limba între dinți, /θ/. Not «tree» (copac) 🙂".
- Recast MAX o corecție pe replică; laudă întâi ce e bun.

PROPORȚIA RO/EN
~70% engleză, ~30% română. Româna DOAR pentru: glosă rapidă între paranteze,
încurajare, o instrucțiune nouă. Întrebările-țintă mereu în engleză.

CE CERI CURSANTULUI (comportament de tutore)
- O singură sarcină pe rând. Aștepți răspunsul înainte de a merge mai departe.
- Lauzi concret: „Perfect — I'm twelve. Great to be! ✅".
- Verifici numerele repetându-le („So, fifteen — one-five. Yes?").

REACȚIE LA TĂCERE / GREȘEALĂ / BLOCAJ
- Tăcere sau „I don't know": oferi în RO un indiciu + un model de completat:
  „No stress 🙂 Spune: I'm ____ years old. (Am ___ ani.)"
- Dacă tot nu merge: dai tu răspunsul model și ceri o simplă repetare.
- Dacă răspunde în română: accepți sensul, apoi dai varianta EN și ceri s-o spună.
- Rămâi mereu în temă (numere/vârstă/preț); readuci blând conversația la unitate.
```

### B. Fluxul conversatiei (3 etape)

**Etapa 1 — GHIDAT** (EVA conduce; răspunsuri MODEL date; structură fixă de elicitat)

| # | EVA (replică de pornire) | Răspuns MODEL | Structură elicitată |
|---|---|---|---|
| 1 | Hi! I'm EVA. 🙂 Let's play the **number game**. How old are you? *(Câți ani ai?)* | I'm twelve years old. | to be + age |
| 2 | Great — I'm one year old, a young robot! Now **count with me**: one, two, three… *(numără cu mine)* | …four, five, six, seven! | numărat 1–10 |
| 3 | Perfect. What's your **phone number**? Say it slow. *(cifră cu cifră)* | It's oh-seven-seven, one-two-three. | citit numere |
| 4 | Nice! **How many** brothers have you got? | I've got two brothers. | How many + have got |
| 5 | Good! And **how many** sisters? | I've got one sister. | How many + have got |
| 6 | Wow, three! Now a shop 🛒 **How much** is the pen? It's two pounds. | Two pounds. Cheap! | preț + cheap |

Notă: dacă cursantul spune *I have twelve years* la #1 → recast imediat: „In English: **I'm** twelve years old 🙂 (vârsta cu «a fi»). Try: I'm ___ years old."

**Etapa 2 — SEMI-GHIDAT** (întrebări deschise + „prompts" în română)

- EVA: *How old is your mother?* — prompt: „She's ____ years old. (folosește **she's**)"
- EVA: *How old is your father?* — prompt: „He's ____ years old."
- EVA: *How much is a coffee here?* — prompt: „It's ____ (pounds / euros)."
- EVA: *Is it cheap or expensive?* — prompt: „It's cheap 👍 / It's expensive 👎"
- EVA: *Count the big numbers: ten, twenty, thirty…?* — prompt: „…____, ____, one hundred."
- EVA: *When is your birthday? How old are you today?* — prompt: „Today I'm ____ 🎂"

Indiciu de branching: dacă cursantul dă doar cifra („30"), EVA cere fraza întreagă: „Yes — say it: **She's thirty years old.** 🙂"

**Etapa 3 — LIBER** (scenariu + obiectiv + branching)

- **Scenariu:** „At the small shop." Cursantul e client; EVA e vânzătoarea. Cursantul (1) salută, (2) întreabă prețul a 2 obiecte cu *How much…?*, (3) spune dacă e cheap/expensive, (4) mulțumește. La final EVA îl întreabă vârsta și numărul de telefon „ca să facă un card de client".
- **Obiectiv:** cursantul produce spontan ≥ 2 întrebări cu *How much…?*, citește 2 prețuri, spune corect vârsta cu *to be* și citește 1 număr de telefon.
- **Branching — dacă cursantul GREȘEȘTE:**
  - *I have X years* → recast la *I'm X years old* + reia întrebarea o dată.
  - confuzie -teen/-ty → EVA repetă contrastul și cere confirmarea numărului („15 or 50?").
  - preț fără monedă („It's five") → EVA cere: „Five what? pounds? euros? 🙂".
- **Branching — dacă cursantul TACE:**
  - EVA oferă în RO un schelet: „Spune: **How much is the book?** 🙂" și așteaptă.
  - După a doua tăcere, EVA dă modelul complet și cere doar repetarea.
- **Închidere:** EVA rezumă pozitiv: „Great client! You said: I'm ___, two pounds, cheap. Thanks! 🎉"

### C. Ascultare (script audio pt TTS + itemi)

**Script audio (monolog scurt A1 — de generat cu TTS, voce clară, ritm lent):**

> Hi! I'm Tom. I'm thirteen years old. My birthday is in May.
> I've got one brother and two sisters. My brother is nineteen — nineteen, not ninety!
> My phone number is oh-seven-seven, one-five, three-oh.
> This is my new book. It's fifteen pounds. Fifteen, not fifty! It's expensive.
> Thanks for listening. Bye!

**Itemi de comprehensiune (4–5):**
1. How old is Tom? — *(cu ce structură răspunzi?)*
2. How many brothers and sisters has Tom got?
3. How old is Tom's brother — 19 or 90?
4. What is Tom's phone number?
5. How much is the book — £15 or £50? Is it cheap or expensive?

**Răspunsuri:**
1. He's thirteen (years old).
2. Three — one brother and two sisters.
3. Nineteen (19), not ninety.
4. Oh-seven-seven, one-five, three-oh (077 15 30).
5. Fifteen pounds (£15) — it's expensive.

### D. Pronuntie (drill + scorare)

**Sunete-țintă (focus români):**
- **/θ/** (limba între dinți, fără voce) — românii tind spre /t/ sau /f/.
- **Accent -teen vs -ty** — poziția accentului (final vs inițial) + vocala finală.

**Minimal pairs (perechi):**
| Pereche | Contrast |
|---|---|
| three /θriː/ ≠ tree /triː/ | /θ/ vs /t/ (three = trei, tree = copac) |
| thirteen /ˌθɜːˈtiːn/ ≠ thirty /ˈθɜːti/ | accent final vs inițial |
| fifteen /ˌfɪfˈtiːn/ ≠ fifty /ˈfɪfti/ | -teen vs -ty |
| nineteen /ˌnaɪnˈtiːn/ ≠ ninety /ˈnaɪnti/ | -teen vs -ty |
| thanks /θæŋks/ ≠ tanks /tæŋks/ | /θ/ vs /t/ |

**Listă de cuvinte (drill):** three · thirteen · thirty · thanks · birthday · thirty-three · fifteen · fifty · nineteen · ninety.

**Propoziții de drill (3–5):**
1. Three, thirteen, thirty. /θ/ every time.
2. Thanks! Happy birthday!
3. Thirty-three, please.
4. Fifteen, not fifty.
5. She's nineteen, not ninety.

**Config de scorare (pronunție):**
- Foneme evaluate: **/θ/** în {three, thirteen, thirty, thanks, birthday}; **poziția accentului** în perechile -teen/-ty.
- Prag: **≥ 80%** corect (≥ 8/10) la nivel de cuvânt-țintă; /θ/ ≥ 3/5 (aliniat cu Stratul 1 ⑦).
- Feedback tipic pt români:
  - „/θ/ — pune vârful limbii ușor între dinți și suflă (fără voce). Nu «t», nu «f»."
  - „«three», nu «tree» — «tree» înseamnă copac 🙂."
  - „fifTEEN (15) accent la FINAL; FIFty (50) accent la ÎNCEPUT."
- Scorare per item: /θ/ prezent = 1p; accent corect = 1p; medie ponderată → % → prag 80%.

**Set de shadowing (repetă după TTS, 3–5):**
1. I'm thirteen years old.
2. Three, thirteen, thirty.
3. Thanks! Happy birthday!
4. Fifteen pounds, not fifty.
5. She's nineteen, not ninety.

## STRATUL 3 — Consolidare & evaluare

### E. Pachet SRS (carduri live)

| Front | Back | Tip | Notă |
|---|---|---|---|
| How old are you? | Câți ani ai? | EN→RO | întrebare-țintă |
| I'm twelve years old. | Am doisprezece ani. | EN→RO | to be, nu have |
| Câți ani ai? | How old are you? | RO→EN | producție |
| Am doisprezece ani. | I'm twelve years old. | RO→EN | anti-calc |
| She's nineteen, not ninety. | Ea are nouăsprezece ani, nu nouăzeci. | EN→RO | -teen/-ty |
| He's thirty years old. | El are treizeci de ani. | EN→RO | he's + age |
| I'm ____ years old. (Am 12 ani) | I'm twelve years old. | cloze | vârstă |
| How old ____ she? (is/are) | How old **is** she? | cloze | is/are |
| What's your phone number? | Care este numărul tău de telefon? | EN→RO | funcție |
| My number is oh-seven-seven, one-two-three. | Numărul meu este zero-șapte-șapte, unu-doi-trei. | EN→RO | „oh"=0 |
| How many brothers have you got? | Câți frați ai? | EN→RO | How many |
| Câți frați ai? | How many brothers have you got? | RO→EN | producție |
| I've got two sisters. | Am două surori. | EN→RO | have got |
| How ____ brothers have you got? (many/much) | How **many** brothers have you got? | cloze | many vs much |
| Count from one to ten. | Numără de la unu la zece. | EN→RO | imperativ |
| Thirteen and thirty are different. | Treisprezece și treizeci sunt diferite. | EN→RO | contrast |
| It's fifteen pounds. | Costă cincisprezece lire. | EN→RO | preț |
| How ____ is the book? (much/many) | How **much** is the book? | cloze | preț |
| The pen is cheap. | Pixul este ieftin. | EN→RO | cheap |
| The book is expensive. | Cartea este scumpă. | EN→RO | expensive |
| Happy birthday! How old are you today? | La mulți ani! Câți ani ai azi? | EN→RO | funcție |
| A hundred, please! | O sută, te rog! | EN→RO | 100 + please |

**Config FSRS (pe scurt):**
- Tag-uri: `a1`, `u6`, `numbers`, `age`, `to-be-age`, `teen-vs-ty`, `phone`, `price`, `have-got`, `theta`.
- Introducere: cardurile EN→RO (recunoaștere) imediat după lecție; RO→EN și cloze (producție) după prima reușită de recunoaștere sau a doua zi.
- Prioritate leech: `to-be-age` (anti *I have … years*) și `teen-vs-ty` — interval inițial mai scurt, retrigger la orice lapse.
- Retenție-țintă: 0.9; review de a doua zi obligatoriu (aliniat cu pragul ⑦ ≥ 70% retenție vocabular).

### F. Scenariu task-based

**Situația (reală):** „Number game & the shop." EVA îți cere vârsta și numărul de telefon, numărați împreună, apoi ești la un mic magazin și citești/întrebi prețuri (coerent cu ⑧ din Stratul 1).

**Obiectiv:** produci corect propria vârstă cu *to be*, citești un număr de telefon, numeri 0–20, întrebi și citești 2 prețuri cu *How much…?* + cheap/expensive.

**Criterii de succes MĂSURABILE:**
- Spune vârsta cu *to be* (fără *I have … years*) — 1/1.
- Numără corect 0–20 fără ezitări majore — ≥ 4/5.
- Citește 1 număr de telefon (cifră cu cifră) — 1/1.
- Întreabă 2 prețuri cu *How much…?* și le citește — ≥ 3/4 elemente.
- Folosește cheap sau expensive corect ≥ 1 dată.

**Rubrică de scorare LLM (0–2 pe criteriu; descriptori A1):**
| Criteriu | 0 | 1 | 2 |
|---|---|---|---|
| Task completion | nu duce sarcina la capăt | completă parțial (prețuri SAU vârstă) | vârstă + telefon + 2 prețuri complete |
| Accuracy | *I have … years* / monedă lipsă des | mici erori, se autocorectează la recast | to be corect, prețuri cu monedă, -teen/-ty corect |
| Fluency | pauze lungi, doar cuvinte izolate | fraze scurte cu ezitări | fraze A1 fluente (3–8 cuvinte), ritm firesc |
- Prag: **≥ 4/6** total ȘI accuracy ≥ 1 (nicio eroare de *have … years* nerecuperată).

**Variante:**
- (a) „At the market": fructe cu prețuri în euro.
- (b) „New phone": schimb reciproc de numere de telefon.
- (c) „Family ages": vârstele a 3 membri de familie cu he's/she's.

### G. Evaluare automata (test de unitate)

**Itemi structurați** `[tip | întrebare | (opțiuni) | răspuns_corect | puncte]`

```
[MCQ    | 15 se scrie: | (a) fifty (b) fifteen (c) fifth | b | 1]
[MCQ    | „She is 90 years old." — 90 = | (a) nineteen (b) ninety (c) ninth | b | 1]
[MCQ    | Cum întrebi vârsta cuiva? | (a) How many are you? (b) How old are you? (c) How much are you? | b | 1]
[MCQ    | Prețul: „How ___ is the pen?" | (a) many (b) old (c) much | c | 1]
[CLOZE  | Vârsta cu „a fi": I'm twelve ____ old. | | years | 1]
[CLOZE  | „How ___ brothers have you got?" | | many | 1]
[CLOZE  | „How old ___ she?" | | is | 1]
[CLOZE  | 100 în litere: a ____ | | hundred | 1]
[MATCH  | Potrivește cifra cu cuvântul | 14=? 40=? 15=? 50=? / fourteen,forty,fifteen,fifty | 14-fourteen,40-forty,15-fifteen,50-fifty | 2]
[REORDER| Ordonează: old / how / are / you / ? | | How old are you? | 1]
[REORDER| Ordonează: I'm / years / thirteen / old | | I'm thirteen years old. | 1]
[TRANS  | RO→EN: „Am două surori." | | I've got two sisters. | 1]
[TRANS  | RO→EN: „Ea are treizeci de ani." | | She's thirty years old. | 1]
[TRANS-CHECK | Corectează: „I have twenty years." | | I'm twenty (years old). | 2]
[DICT   | Audio → scrie cifra: „seventeen" | | 17 | 1]
[DICT   | Audio → scrie cifra: „sixty" | | 60 | 1]
[LISTEN | (din script C) How much is the book? | (a) £15 (b) £50 (c) £5 | a | 1]
[LISTEN | (din script C) How old is Tom's brother? | (a) 9 (b) 19 (c) 90 | b | 1]
```

**Logică de scorare:**
- MCQ/CLOZE/REORDER/LISTEN/DICT: exact-match (cloze normalizat: lowercase, trim, ignoră punctuația).
- TRANS: acceptă variante echivalente A1 (ex. *I have got two sisters* = *I've got two sisters*; *She's thirty* = *She is thirty years old*). Verificare LLM cu toleranță la contracții/„years old" opțional.
- TRANS-CHECK & MATCH: 2p, parțial 1p dacă corectează *have→to be* dar omite „years old" / potrivește 2–3 din 4.
- Total: **22 puncte**. **Prag de promovare ≥ 80%** (≥ 18/22). *(Notă: testul scurt din ⑦ folosește prag intern 70% pe 20p; testul de unitate complet aici cere 80%.)*

**Rubrică LLM pt producție (vorbire/scriere):**
| Criteriu | Descriptor A1 | Prag |
|---|---|---|
| Accuracy | folosește *to be* pt vârstă, plural după numere, monedă la preț; recuperează la recast | fără *I have … years* nerecuperat |
| Task completion | răspunde la ce s-a cerut (vârstă/telefon/preț) | ≥ 80% din prompturi acoperite |
| Fluency | fraze scurte A1 inteligibile, ritm acceptabil | comunică fără blocaj major |
| Pronunție /θ/ | three/thirteen/thirty/thanks recognoscibile | ≥ 3/5 |

**MAPARE obiective ① → itemi:**
| Obiectiv ① (Stratul 1) | Itemi care îl testează |
|---|---|
| Numără 0–100 & citește numere izolate | MCQ (15/90), MATCH (14/40/15/50), REORDER, DICT |
| Ascultă & scrie numere dictate | DICT (17, 60), LISTEN (£15, brother 19) |
| Spune/întreabă vârsta cu *to be* (fără *have … years*) | MCQ (How old…?), CLOZE (years/is), TRANS-CHECK, TRANS (She's thirty), REORDER, rubrică producție |
| Distinge accent -teen vs -ty | MCQ (15 vs 50; 90), MATCH (14/40, 15/50), pronunție D |
| Citește număr de telefon & preț simplu | MCQ (How much), CLOZE (many/hundred), LISTEN (£15), scenariu F |

---


### A1-U7 — What time is it? · Straturile 2 & 3 (Pipeline + Consolidare)

## STRATUL 2 — Pipeline (conversatie & voce cu EVA)

### A. Configuratia EVA (system prompt pt unitate)

```
ROL: Ești EVA, un tutore de engleză prietenos, cald și foarte răbdător, pentru un
vorbitor NATIV DE ROMÂNĂ aflat la nivelul A1 (începător). Conversația e prin chat de
voce/text (stil WhatsApp). Ești încurajatoare, folosești emoji rar și cu rost, faci
mesaje SCURTE (1–3 propoziții), o singură întrebare pe replică.

UNITATEA CURENTĂ: A1-U7 „What time is it?" — ora, zilele, lunile, data.

CE POȚI FOLOSI (gramatică introdusă până AICI, inclusiv):
- verbul TO BE (am/is/are, forme negative și interogative), have got;
- a/an/the, this/that, plural, adjective posesive, numere 0–100;
- STRUCTURILE-ȚINTĂ ALE ACESTEI UNITĂȚI:
  • What time is it? — It's seven o'clock / half past six / quarter past nine / quarter to five.
  • When is…? — It's on Monday / in July / at seven o'clock.
  • Prepoziții de timp: AT + oră exactă și „at night"; ON + zi/dată; IN + lună/parte a zilei/an.
  • I've got school on Monday. See you on Wednesday!

CE NU AI VOIE SĂ FOLOSEȘTI (încă neînvățat):
- ⚠️ NICIODATĂ present simple (I get up, I start, she works). Vorbește despre program DOAR
  cu „to be" + „have got". Dacă vrei „mă trezesc la 7", spune „My morning is at seven o'clock" —
  nu introduce verbe noi.
- Fără present continuous, past, will, timpuri viitoare, modale. Fără vocabular peste cele 65
  de cuvinte ale unității, decât dacă e absolut necesar și îl glosezi imediat în română.

VOCABULAR DE ELICITAT (țintă): time, clock, watch, hour, minute, o'clock, half past,
quarter past, quarter to, midday/noon, midnight, morning, afternoon, evening, night, a.m.,
p.m., today, tomorrow, tonight, zilele (Monday…Sunday), day, week, weekend, lunile
(January…December), month, year, when, what time, at/on/in, date, birthday, breakfast,
lunch, dinner, class, school, party, film, holiday, timetable, calendar.

PROPORȚIA RO/EN: ~70% engleză, ~30% română. Româna e „plasa de siguranță": o folosești
pentru a explica o regulă grea (mai ales at/on/in), pentru a traduce un cuvânt nou în
paranteză, sau când cursantul e blocat. Instrucțiunile și încurajările scurte pot fi
bilingve: „Great! (Bravo!)".

CORECTARE PRIN RECAST (blând, fără roșu, fără „Wrong!"):
- Nu spui niciodată „greșit". Reformulezi corect, natural, apoi mergi mai departe cu o
  întrebare. Exemplu:
   User: „My class is in Monday."
   EVA: „Ah, on Monday! 👍 Zilele merg cu «on». And what time is your class?"
- Corectezi MAXIM 1 lucru pe replică (cel mai important). Restul îl lași să curgă.
- Pentru pronunție (voce): dacă aude /t/ în loc de /θ/ („Torsday"), model scurt:
  „Almost! Thursday — pune limba între dinți: /θ/. Say it: Thursday."

CE CERI CURSANTULUI: să spună ora la diferite ceasuri, să dea ziua/luna/data lucrurilor lui
(școală, oră de engleză, petrecere, ziua de naștere) și să aleagă corect at/on/in.

DACĂ TACE (>~6 sec sau „…" / „nu știu"): oferi un indiciu în română + un început de
propoziție: „No stress! Începe cu «It's…». It's… o'clock?" Nu răspunde tu în locul lui din
prima; dă schela, apoi așteaptă.

DACĂ GREȘEȘTE: recast (vezi mai sus) + reîntrebi aceeași structură pe alt exemplu, ca să
consolideze. Dacă greșește de 2 ori la fel, dă mini-regula în română, foarte scurt.

TON FINAL: laudă des și specific („Perfect — «on Saturday» is exactly right!"), nu vag.
Termini interacțiunile cu o formulă din unitate: „See you on Monday! 👋".
```

### B. Fluxul conversatiei (3 etape)

#### Etapa 1 — GHIDAT (EVA conduce; cursantul completează un tipar)

Structura de elicitat: `It's + [oră]` · `It's at/on/in + …` · răspuns la `What time…? / When…?`

| # | EVA (replică de pornire) | Răspuns MODEL (ținta) |
|---|---|---|
| 1 | Hi! I'm EVA. 😊 Look at the clock — it's 7:00. **What time is it?** | It's seven o'clock. |
| 2 | Great! And this one is 8:30. What time is it? *(indiciu: half past…)* | It's half past eight. |
| 3 | Perfect. Now **when** is your English class — Monday or Wednesday? | It's on Wednesday. |
| 4 | Nice! Is your class in the morning or in the afternoon? | It's in the afternoon. |
| 5 | And **what time** is the class? *(indiciu: at … o'clock)* | It's at four o'clock. |
| 6 | Lovely. Last one: **when** is your birthday — which month? | It's in July. |

Regula ascunsă pe care o antrenăm: **oră → at**, **zi → on**, **lună/parte a zilei → in**.

#### Etapa 2 — SEMI-GHIDAT (întrebări deschise + „prompts")

EVA pune întrebări reale despre cursant; dă indicii doar dacă e nevoie.
- „**What time is it now** where you are?" — *(prompt: It's … o'clock / half past …)*
- „**When is** the weekend for you — Saturday and Sunday?" — *(prompt: on …)*
- „Have you got a party this week? **When**?" — *(prompt: on … , in the evening)*
- „**What time** is dinner at your home?" — *(prompt: at … o'clock)*
- „**When is** your birthday — month and date?" — *(prompt: in … , on the … of …)*

Branching indiciu: dacă răspunde doar cu cifra („four"), EVA face recast-schela:
„Full sentence, please: **It's at** four o'clock. 🙂"

#### Etapa 3 — LIBER (scenariu + obiectiv)

**Scenariu:** „Tell EVA your week." Cursantul îi spune lui EVA orarul lui din această
săptămână: școală, oră de engleză, o petrecere și ziua de naștere — la ce oră (**at**),
în ce zi (**on**), în ce lună/parte a zilei (**in**). Obiectiv: ≥6 propoziții corecte de
tip „X is at/on/in …".

Branching (ce face EVA):
- **User corect** → laudă specifică + cere detaliu nou: „And what time?"
- **User greșește prepoziția** (in Monday) → recast: „on Monday 👍" + continuă.
- **User folosește present simple** (I start at 8) → recast pe structura permisă: „Ah —
  «My school is at eight o'clock». La A1 folosim «to be». Try it: My school is at…?"
- **User tace** → indiciu RO + început: „Nicio grabă. Începe cu «My …». My party is on…?"
- **User cere cuvânt** („cum zic marți?") → dă cuvântul + îl pune într-un model: „Tuesday.
  Say: My class is **on Tuesday**."
- **Închidere** când are ≥6 propoziții: rezumat cald + „See you on Wednesday! 👋".

### C. Ascultare (script audio pt TTS + itemi)

**Script audio (monolog scurt A1, ~40 s, voce clară, ritm lent). Titlu: „Tom's week".**

> Hello! My name is Tom. What time is it now? It's half past seven in the morning.
> My English class is on Monday. It's at five o'clock in the afternoon.
> I've got a party on Saturday. The party is in the evening, at eight o'clock.
> My birthday is in June — on the third of June. See you on Monday! Bye!

**Itemi de comprehensiune (5):**
1. What time is it now? (A) 7:30 (B) 8:30 (C) 5:00
2. When is Tom's English class? (A) on Saturday (B) on Monday (C) on Sunday
3. What time is the party? (A) at seven o'clock (B) at eight o'clock (C) at five o'clock
4. When is the party — morning or evening? (A) in the morning (B) in the evening
5. When is Tom's birthday? (A) in July (B) on the third of June (C) in May

**Răspunsuri:** 1-A (half past seven = 7:30) · 2-B · 3-B · 4-B · 5-B.

### D. Pronuntie (drill + scorare)

**Sunete-țintă (RO-focus):**
- **/θ/** fără voce (limba între dinți) — *Thursday, month, three, thirty, birthday*.
- **/z/ final** sonor (nu se surzește la /s/) — *days, Tuesdays, is*.
- **Reducerea vocalelor** neaccentuate — *to* → /tə/ (quarter **to** five), *o'clock* → /əˈklɒk/, *quarter* → /ˈkwɔːtə/, *at* → /ət/.

**Minimal pairs (perechi de contrast):**
| Țintă /θ/ vs. eroare RO | Alt contrast |
|---|---|
| **th**ree /θriː/ ↔ **t**ree /triː/ | **th**ick /θ/ ↔ **s**ick /s/ |
| **th**irty /ˈθɜːti/ ↔ **t**hirty→„tirty" | mon**th** /mʌnθ/ ↔ „mont" /t/ |
| **Th**ursday /θ/ ↔ „Torsday" /t/ | day**s** /deɪz/ ↔ „days"→/deɪs/ |

**Lista de cuvinte (drill):** Thursday · month · three · thirty · birthday · days · Tuesdays · o'clock · quarter · morning · evening · half past.

**Propoziții de drill (3–5):**
1. It's **three** **o'clock** on **Thursday**. /θriː … θɜːzdeɪ/
2. My **birthday** is in the **month** of July. /ˈbɜːθdeɪ … mʌnθ/
3. It's **thirty** minutes — **half past** six.
4. I've got classes on **Tuesdays** and **Thursdays**. (focus /z/ + /θ/)
5. **Quarter to** nine in the morning. (reducere: /ˈkwɔːtə tə/)

**Config de scorare:**
- Foneme evaluate: **/θ/** (prioritar), **/z/ final**, plus reducerea /tə/ în „quarter to".
- Prag de trecere: **≥80%** din cuvintele-țintă corecte (echiv. ⑦: ≥3 din 4 la *Thursday/month/three/thirty*).
- Feedback tipic pentru români:
  - /θ/ realizat ca /t/ („Torsday", „tree", „mont") → indiciu: „Limba ÎNTRE dinți, aer, fără voce: /θ/."
  - /θ/ realizat ca /f/ („free" pentru three) → „Nu buza pe dinți (/f/), ci limba între dinți (/θ/)."
  - /z/ surzit la /s/ („days"→/deɪs/) → „Motorul pornit — vibrează: day**z**."
  - „quarter to" pronunțat plin /tuː/ → acceptabil, dar model reducerea /tə/ pentru fluență.

**Set de shadowing (repetă după EVA, 3–5):**
1. „What **time** is it?"
2. „It's **quarter to** five."
3. „My **birthday** is in the **month** of **March**."
4. „See you on **Thursday**!"
5. „It's **half past** **three** in the afternoon."

---

## STRATUL 3 — Consolidare & evaluare

### E. Pachet SRS (carduri live)

| Front | Back | Tip | Notă |
|---|---|---|---|
| What time is it? | Cât e ceasul? | EN→RO | funcție-cheie |
| Cât e ceasul? | What time is it? | RO→EN | producție |
| It's seven o'clock. | E ora șapte. | EN→RO | o'clock |
| It's ___ past ten. (10:30) | half | cloze | half past |
| It's quarter to nine. | E nouă fără un sfert. | EN→RO | quarter to = 8:45→9 |
| E nouă fără un sfert. | It's quarter to nine. | RO→EN | logica „to" |
| My class is ___ four o'clock. | at | cloze | oră → at |
| The party is ___ Saturday. | on | cloze | zi → on |
| My birthday is ___ July. | in | cloze | lună → in |
| I'm at home ___ night. | at | cloze | excepție: at night |
| When is your birthday? | Când e ziua ta? | EN→RO | When…? |
| Ne vedem luni! | See you on Monday! | RO→EN | on + zi |
| Today is Thursday. | Azi e joi. | EN→RO | /θ/ |
| Azi e joi. | Today is Thursday. | RO→EN | /θ/ producție |
| It's early in the morning. | E devreme dimineața. | EN→RO | in the morning |
| Dinner is ___ eight o'clock. | at | cloze | at + oră |
| E zece și jumătate. | It's half past ten. | RO→EN | producție |
| It's twelve o'clock — ___. | midday / noon | cloze | 12:00 |
| Petrecerea e sâmbătă. | The party is on Saturday. | RO→EN | on |
| Ziua mea de naștere e în iulie. | My birthday is in July. | RO→EN | in + lună |

**Config FSRS (pe scurt):**
- Tag-uri: `A1-U7`, plus sub-tag-uri `time-telling`, `prep-at-on-in`, `days-months`, `phon-θ`.
- Introducere: cardurile intră DUPĂ ce cursantul termină Etapa 1–2 din pipeline (recunoaștere înainte de producție). Ordine: mai întâi EN→RO (recunoaștere), apoi cloze prepoziții, apoi RO→EN (producție).
- Prioritate „leech": cardurile at/on/in și /θ/ (Thursday, month) primesc interval inițial mai scurt; dacă ratează de 2 ori, se re-injectează în pipeline la Etapa 2.
- Prag de „învățat": ≥80% recunoaștere la revizuire (coerent cu ⑦: ≥52/65 cuvinte).

### F. Scenariu task-based

**Situația reală:** Îți faci orarul acestei săptămâni cu EVA înainte de weekend. EVA e „secretara" ta prietenoasă și notează când ai fiecare lucru important.

**Obiectiv:** Comunică-i lui EVA — folosind DOAR *to be* + *have got* + *at/on/in* — cel puțin 4 evenimente cu **oră** și **zi/lună**: (1) ora acum, (2) ora de engleză, (3) o petrecere, (4) ziua ta de naștere.

**Criterii de succes MĂSURABILE:**
- Produce **≥6 propoziții** corecte de tip „X is at/on/in …".
- **≥80%** prepoziții corecte (at/on/in).
- Spune corect **≥2 ore** cu structuri diferite (o'clock / half past / quarter…).
- Zero folosiri de present simple (respectă limita de nivel).

**Rubrică de scorare LLM (0–2 pe criteriu):**
| Criteriu | 0 | 1 | 2 (A1 target) |
|---|---|---|---|
| **Task completion** | <2 evenimente comunicate | 2–3 evenimente, incomplete | ≥4 evenimente cu oră ȘI zi/lună |
| **Accuracy (at/on/in + oră)** | <50% corecte | 50–79% corecte | ≥80% prepoziții + ore corecte |
| **Fluency** | răspunsuri de 1 cuvânt, multe pauze | propoziții scurte cu ajutor | propoziții complete „It's… at/on/in…", puține pauze |
| **Range (control de nivel)** | folosește present simple/structuri nepredate | 1 alunecare | doar to be + have got, ≥2 structuri de oră |
| **Prag de promovare a task-ului:** ≥7/8 puncte (≥80%). | | | |

**Variante:** (a) *Family week* — orarul unui membru din familie (his/her class is on…); (b) *Invitation* — invită un prieten: „There's a party on Saturday at eight — see you!"; (c) *Timetable read* — EVA îi arată un orar și cursantul confirmă „The film is on Friday, at nine."

### G. Evaluare automata (test de unitate)

**Itemi structurați `[tip | întrebare | (opțiuni) | răspuns_corect | puncte]`:**

```
[MCQ    | What time is it? 10:45 | quarter past ten / quarter to eleven / half past ten | quarter to eleven | 1]
[MCQ    | 8:30 in words | half past eight / quarter past eight / eight o'clock | half past eight | 1]
[cloze  | My class is ___ four o'clock. | at/on/in | at | 1]
[cloze  | The party is ___ Saturday. | at/on/in | on | 1]
[cloze  | My birthday is ___ May. | at/on/in | in | 1]
[cloze  | I'm at home ___ night. | at/on/in | at | 1]
[MCQ    | The film is ___ Friday. | at / on / in | on | 1]
[matching | Potrivește: 1)7:00 2)9:15 3)12:00 | A)quarter past nine B)midday/noon C)seven o'clock | 1-C,2-A,3-B | 3]
[matching | Potrivește Q-A: 1)What time is it? 2)When is your class? 3)When is your birthday? | A)It's in June. B)It's half past ten. C)It's on Tuesday. | 1-B,2-C,3-A | 3]
[reorder | on / birthday / my / is / Sunday | — | My birthday is on Sunday. | 1]
[reorder | class / my / at / is / o'clock / five | — | My class is at five o'clock. | 1]
[cloze  | Spelling: Th___sday (joi) | — | Thursday | 1]
[cloze  | It's ___ to nine. (8:45) | quarter | quarter | 1]
[translate | „E ora zece." | — | It's ten o'clock. | 1]
[translate | „Ziua mea de naștere e în iunie." | — | My birthday is in June. | 1]
[translate | „Ne vedem luni!" | — | See you on Monday! | 1]
```

**Logica de scorare + prag:**
- Total = **20 puncte**. MCQ/cloze/reorder: exact-match (case-insensitive, spații și punctuație ignorate). Matching: punctaj parțial (1p / potrivire corectă). Translate-check: acceptă variante echivalente A1 (ex. *twelve o'clock = midday = noon*; *My English class = My class*; prepoziția și ora TREBUIE corecte).
- **Prag de promovare a unității: ≥80% (≥16/20).**
- Sub-praguri diagnostice: dacă prepozițiile (cei 5 itemi at/on/in) < 4/5 → re-drill secțiunea D + carduri cloze prep. Dacă orele < 4/5 → re-drill telling-time.

**Rubrică LLM pentru producție (vorbire/scriere, când testul e oral):** vezi F (task completion / accuracy / fluency / range, descriptori A1, prag ≥80%). Suplimentar pentru pronunție: /θ/ ≥3/4 la *Thursday, month, three, thirty* (secțiunea D).

**MAPARE obiective ① → itemi:**
| Obiectiv ① (Stratul 1) | Itemi care îl testează |
|---|---|
| Spune ora (o'clock/half past/quarter past/quarter to), ≥8/10 | MCQ 10:45, MCQ 8:30, matching ore, cloze „quarter to nine", translate „It's ten o'clock", secțiunea A din mini-test ⑦ |
| Cere/dă ziua, luna, data (What day…?/When…?), ≥4/5 | matching Q-A (When is…), translate „…in June", reorder „…on Sunday" |
| Folosește at/on/in corect, ≥80% | 5 itemi cloze (at four / on Saturday / in May / at night) + MCQ „on Friday" |
| Vorbește despre program cu *to be*, ≥6 propoziții | reorder „My class is at five o'clock", reorder „My birthday is on Sunday", translate-uri + task-ul F |
| Pronunță /θ/ (Thursday, month, three), ≥3/4 | cloze spelling „Thursday", secțiunea D (drill + scorare fonetică) |

---


I've read the complete Layer 1 file. Now I'll produce Layers 2 and 3, coherent with the exact vocabulary, dialogue (③), task (⑧), and SRS bank (⑨).

### A1-U8 — My daily routine · Straturile 2 & 3 (Pipeline + Consolidare)

## STRATUL 2 — Pipeline (conversatie & voce cu EVA)

### A. Configuratia EVA (system prompt pt unitate)

```
ROL: Esti EVA (English Voice Assistant), o tutore AI prietenoasa, calda si RABDATOARE.
Vorbesti cu un adult roman care invata engleza de la ZERO. Nivel STRICT A1, Unitatea 8 —
"My daily routine". Tema: rutina zilnica la persoana I/you/we/they.

OBIECTIV DE ELICITAT (fa cursantul sa PRODUCA, nu doar sa asculte):
- Present simple AFIRMATIV la I/you/we/they = verb de baza, FARA -s ("I work", "we eat").
- NEGATIV cu "don't + verb" ("I don't watch TV").
- ADVERBE DE FRECVENTA inaintea verbului: always / usually / often / sometimes / never.
- Vocabular-tinta din unitate: get up, wake up, have breakfast/lunch/dinner, go to work/school/bed,
  make coffee, drink tea, watch TV, read, relax, listen to music, morning/afternoon/evening/night,
  every day, early, late, o'clock, weekend.

STRUCTURI PERMISE (control de nivel — NU depasi):
- DOAR persoanele I/you/we/they. NU folosi persoana a III-a cu -s (he works) — vine in U9.
- NU folosi "do you...?" ca structura de predat; poti pune intrebari simple, dar accepta raspunsuri
  scurte. NU introduce past simple, present continuous, articole complexe, comparative.
- Propozitii scurte (max 6-8 cuvinte). Un singur mesaj = 1-2 idei.

REGULI DE CORECTARE — RECAST (blând, FARA marcaj rosu):
- Nu spune niciodata "Wrong / Gresit". Reformuleaza corect natural, apoi continua conversatia.
  Ex: cursant: "I no eat breakfast." → EVA: "Ah, you don't eat breakfast! I understand. And lunch?"
- Corecteaza MAX 1 lucru pe replica (cel mai important). Ignora restul greselilor minore.
- Tine cont de greselile TIPICE romanesti si recasteaza-le blând:
  * subiect omis ("Work every day") → "Yes, you work every day!"
  * negativ gresit ("I no sleep") → "You don't sleep in the afternoon, I see."
  * -s adaugat gresit ("I works") → "You work, nice!"
  * ordine adverb ("I go always") → "You always go to work — good routine!"

PROPORTIA RO/EN: ~80% engleza, ~20% romana. Foloseste romana DOAR pentru:
- a debloca cand cursantul tace sau spune "nu inteleg" (glosa scurta intre paranteze),
- a incuraja ("Foarte bine!"), a explica un cuvant nou o singura data.
Pune mereu glosa RO scurta dupa un cuvant/expresie nou(a): "Tell me about your day. (Povesteste-mi...)".

CE CERI CURSANTULUI: sa descrie propria rutina — cel putin 8 propozitii pe parcursul conversatiei,
din care >=2 negative (don't) si >=2 cu adverb de frecventa.

DACA CURSANTUL TACE (>~8 sec / mesaj gol): ofera un model + o intrebare inchisa cu 2 optiuni.
  Ex: "No problem! I get up at six. And you — early or late? (devreme sau tarziu?)"
DACA GRESESTE: recast blând (vezi mai sus) + continua, nu opri fluxul.
DACA RASPUNDE CORECT: valideaza scurt si natural ("Me too!" / "Great!") si adauga o intrebare noua.

TON: incurajator, prietenos, uman. Emoji ocazional (1 la 2-3 replici), niciodata jargon gramatical
in fata cursantului (nu spui "present simple", spui "we say it like this: I work").
```

### B. Fluxul conversatiei (3 etape)

**Etapa 1 — GHIDAT** (EVA da model, cursantul imita; structura de elicitat: `I + verb de baza` + adverb de frecventa)

| # | EVA (replica de pornire) | Raspuns MODEL (cursant) | Structura de elicitat |
|---|---|---|---|
| 1 | Hi! I'm EVA. 😊 This is my day: I always get up early. And you? *(Si tu?)* | I get up early too. / I get up at six. | `I get up...` (afirmativ pers. I) |
| 2 | I have breakfast at seven o'clock. Do you have breakfast? *(Iei micul dejun?)* | Yes, I have breakfast. / I have breakfast at eight. | `I have breakfast...` |
| 3 | First, I make coffee. Then I go to work. What do you drink — coffee or tea? | I drink tea. / I make coffee. | `I drink / I make...` |
| 4 | I work every day. I don't work at night. And you? | I work every day too. / I don't work at night. | negativ `I don't + verb` |
| 5 | In the evening I sometimes watch TV. How often do you watch TV? *(Cat de des?)* | I sometimes watch TV. / I never watch TV. | adverb de frecventa + verb |
| 6 | I never go to bed late. What about you? *(Tu?)* | I go to bed early. / I never go to bed late. | `I never/always + verb` |

**Etapa 2 — SEMI-GHIDAT** (intrebari deschise + indicii)

- EVA: "Tell me about your morning. *(dimineata ta)*" — indiciu: `get up / breakfast / coffee / go to work`.
- EVA: "What do you do in the evening?" — indiciu: `read / watch TV / listen to music / relax`.
- EVA: "Tell me two things you DON'T do. *(doua lucruri pe care NU le faci)*" — indiciu: `I don't...`.
- EVA: "How often? Use: always / usually / often / sometimes / never." — indiciu: adverb + verb.
- EVA: "And on the weekend? *(la sfarsit de saptamana)*" — indiciu: `On the weekend I...`.

**Etapa 3 — LIBER** (scenariu + obiectiv + branching)

- **Scenariu:** "Describe your whole day to EVA — from morning to night." 
- **Obiectiv:** >=8 propozitii despre rutina proprie, din care **>=2 negative** (`don't`) si **>=2 cu adverb de frecventa**, la ordinea corecta a cuvintelor.
- **Branching:**
  - *Daca tace* → EVA da un start si o alegere binara: "It's ok! In the morning — coffee or tea? *(cafea sau ceai?)*" si asteapta.
  - *Daca greseste gramatical* → recast blând (max 1/replica), fara sa opreasca: cursant "I watch always TV" → EVA "Ah, you always watch TV! 😄 And in the morning?"
  - *Daca da propozitii scurte/putine* → EVA cere extindere: "Nice! Tell me one more thing. What about lunch? *(pranzul?)*"
  - *Daca foloseste cuvant necunoscut/din afara nivelului* → EVA accepta sensul, ofera echivalentul A1: "You mean you tidy? We say: I clean the house."
  - *Daca reuseste (>=8 propozitii, 2 negative, 2 adverbe)* → EVA inchide cu lauda + rezumat: "Perfect! You get up early, you always make coffee, and you never go to bed late. Great routine! 🎉"

### C. Ascultare (script audio pt TTS + itemi)

**Script audio (monolog A1, ~45-55 sec, voce EVA — de generat cu TTS, ritm rar, pauze la punct):**

> Hello! I'm EVA. This is my day. I always get up early, at six o'clock. First, I make coffee. I usually have breakfast at seven. Then I go to work. I work every day, but I don't work on the weekend. In the afternoon I sometimes drink tea. In the evening I read or I listen to music. I don't watch TV. I never go to bed late. I go to bed at ten o'clock. Good night!

**Itemi de comprehensiune:**
1. What time does EVA get up? *(La ce ora se trezeste EVA?)*
2. What does EVA make first in the morning?
3. Does EVA work on the weekend? (Yes / No)
4. Does EVA watch TV in the evening? (Yes / No)
5. What time does EVA go to bed?

**Raspunsuri:** 1. At six (o'clock). · 2. Coffee. (She makes coffee.) · 3. No. · 4. No. · 5. At ten (o'clock).

### D. Pronuntie (drill + scorare)

**Sunet-tinta RO-focus:** **/w/** (labial, buze rotunjite, FARA dinti pe buza) vs **/v/** (dintii ating buza de jos). Romanii tind sa pronunte /w/ ca /v/ ("work" → "*vork*").

**Minimal pairs (perechi /w/ vs /v/):**

| /w/ | /v/ |
|---|---|
| wake /weɪk/ | — |
| work /wɜːk/ | — |
| we /wiː/ | very /ˈveri/ |
| west /west/ | vest /vest/ |
| wine /waɪn/ | vine /vaɪn/ |
| wet /wet/ | vet /vet/ |

**Lista de cuvinte (drill):** wake, work, watch, walk, we, weekend, wash — vs — very, visit, evening.

**Propozitii de drill:**
1. **W**e **w**ake up and **w**e **w**ork.
2. I **w**atch TV in the **w**eekend.
3. I **w**alk to **w**ork every day.
4. We are **v**ery busy in the e**v**ening. *(contrast: v)*
5. I **w**ash, then I **v**isit a friend. *(contrast w vs v in aceeasi propozitie)*

**Config de scorare:**
- **Foneme evaluate:** /w/ (target principal) in {wake, work, watch, walk, we, weekend}; contrast /v/ in {very, visit, evening}.
- **Prag:** >=80% (min. 4 din 6 cuvinte cu /w/ pronuntate labial). Corespunde criteriului ① (>=4/6).
- **Feedback tipic pt romani:** daca /w/ e realizat ca /v/ → "Rotunjeste buzele ca pentru un pupic 😗, NU atinge dintii de buza. Say: /w/... work." Daca e corect → "Perfect /w/! Buze rotunjite, fara dinti."

**Set de shadowing (cursantul repeta imediat dupa EVA):**
1. I always get up early.
2. We work every day.
3. I sometimes watch TV in the evening.
4. I never go to bed late.
5. We wake up and we make coffee.

## STRATUL 3 — Consolidare & evaluare

### E. Pachet SRS (carduri live)

| Front | Back | Tip | Nota |
|---|---|---|---|
| I get up early. | Ma trezesc devreme. | EN→RO | ⑨ core |
| Nu ma trezesc tarziu. | I don't get up late. | RO→EN | negativ |
| I always have breakfast. | Intotdeauna iau micul dejun. | EN→RO | adverb |
| De obicei fac cafea. | I usually make coffee. | RO→EN | adverb |
| We go to work every day. | Mergem la munca in fiecare zi. | EN→RO | we + every day |
| Tu nu muncesti noaptea. | You don't work at night. | RO→EN | negativ (you) |
| I sometimes watch TV. | Uneori ma uit la televizor. | EN→RO | adverb |
| Niciodata nu ma culc tarziu. | I never go to bed late. | RO→EN | adverb never |
| They eat dinner in the evening. | Ei iau cina seara. | EN→RO | they |
| I often read in the evening. | Deseori citesc seara. | EN→RO | adverb often |
| Nu mergem la munca in weekend. | We don't go to work on the weekend. | RO→EN | negativ (we) |
| I drink tea in the morning. | Beau ceai dimineata. | EN→RO | core |
| Ma culc la ora unsprezece. | I go to bed at eleven. | RO→EN | core |
| You always study in the afternoon. | Intotdeauna inveti dupa-amiaza. | EN→RO | adverb (you) |
| I don't sleep in the afternoon. | Nu dorm dupa-amiaza. | EN→RO | negativ |
| I ______ get up early. (100%) | always | cloze | adverb slot |
| We ______ watch TV. (0%) | never | cloze | adverb slot |
| I ______ (not/eat) breakfast. | don't eat | cloze | negativ |
| First I make coffee, ______ I go to work. | then | cloze | conector `then` |
| I always ______ up early. | get | cloze | phrasal `get up` |

**Config FSRS pe scurt:**
- **Tag-uri:** `A1-U8`, `daily-routine`, `present-simple-I`, `negative-dont`, `freq-adverbs`.
- **Moment de introducere:** cardurile EN→RO / RO→EN se introduc IMEDIAT dupa Etapa 1 (recunoastere). Cardurile `cloze` (gramatica) se introduc dupa Etapa 2 (productie ghidata).
- **Parametri:** carduri noi/zi = 8; retention target = 0.90; interval initial "again" = 1 zi, "good" = 3 zile. Reintroducere prioritara a cardurilor cu adverbe si negativ (obiective ①.2 si ①.3).

### F. Scenariu task-based

**Situatia reala:** EVA te intreaba despre ziua ta (coerent cu ⑧). Descrie-i rutina zilnica intr-o conversatie chat/voce.

**Obiectiv:** produ **>=8 propozitii** despre propria rutina, din care **>=2 negative** (`don't`) si **>=2 cu adverb de frecventa**, in ordine logica (morning → evening).

**Criterii de succes MASURABILE:**
- Nr. propozitii >=8.
- Propozitii negative corecte cu `don't` >=2.
- Propozitii cu adverb de frecventa (plasat inaintea verbului) >=2.
- Acuratete gramaticala >=75% (subiect prezent, fara -s la I/you/we/they, ordine corecta).
- Foloseste >=6 cuvinte-tinta din vocabularul unitatii.

**Rubrica de scorare LLM (descriptori A1):**

| Criteriu | 2 (peste asteptari) | 1 (indeplineste A1) | 0 (sub prag) |
|---|---|---|---|
| **Task completion** | >=8 prop., 2 negative + 2 adverbe, acopera dimineata→seara | 6-7 prop. sau lipseste 1 cerinta (ex. doar 1 negativ) | <6 prop. sau nu descrie rutina |
| **Accuracy** | >=90% corect; subiect mereu prezent, fara -s, ordine adverb corecta | 75-89%; greseli minore recastabile | <75%; negativ gresit / subiect omis repetat |
| **Fluency** | raspunde prompt, extinde singur, foloseste `first/then` | raspunde cu indicii, propozitii scurte dar clare | tacere lunga/monosilabic, necesita RO constant |

**Prag task:** minim 1 la fiecare criteriu SI cerintele masurabile de mai sus indeplinite.

**Variante:**
- V1 (usor): "Describe just your morning" (get up → breakfast → coffee → go to work).
- V2 (standard): ziua intreaga (scenariul de baza).
- V3 (extindere): "Your day vs the weekend" — contrast `every day` vs `on the weekend` (foloseste `don't`).

### G. Evaluare automata (test de unitate)

**Itemi structurati `[tip | intrebare | (optiuni) | raspuns_corect | puncte]`:**

```
[cloze     | I ____ (not/watch) TV in the morning.                | —                              | don't watch                        | 1]
[cloze     | We ____ get up early. (100%)                          | —                              | always                             | 1]
[mcq       | ____ go to bed late.                                  | a) I doesn't b) I don't c) I no| b                                  | 1]
[reorder   | early / I / get up / always                           | —                              | I always get up early.             | 1]
[cloze     | You ____ (have) breakfast at eight.                   | —                              | have                               | 1]
[mcq       | Correct order:                                        | a) I watch often TV b) I often watch TV c) I watch TV often | b      | 1]
[matching  | 1.have 2.go 3.make 4.listen 5.brush                   | a.to bed b.coffee c.breakfast d.my teeth e.to music | 1-c,2-a,3-b,4-e,5-d | 2]
[translate | Eu nu muncesc in weekend.                             | —                              | I don't work on the weekend.       | 1]
[translate | Uneori mananc tarziu.                                 | —                              | I sometimes eat late.              | 1]
[mcq       | Bifeaza cuvintele cu /w/: work, very, watch, visit    | multi-select                   | work, watch                        | 1]
[cloze     | They ____ (not/go) to school on Monday.               | —                              | don't go                           | 1]
[translate | a se trezi (RO->EN)                                    | —                              | get up (sau wake up)               | 1]
[translate | de obicei (RO->EN)                                     | —                              | usually                            | 1]
[cloze     | I ____ (0%) go to bed late.                            | —                              | never                              | 1]
[reorder   | TV / we / watch / never                               | —                              | We never watch TV.                 | 1]
```

**Logica de scorare:**
- Total = 16 puncte (matching = 2p, restul 1p). Prag de promovare **>=80% = >=12,8/16**.
- `cloze` / `reorder`: normalizare (lowercase, trim, spatii multiple → unul); `don't` = `do not` acceptat; punctuatia finala ignorata.
- `translate`: acceptare de variante echivalente (ex. `get up`/`wake up`; `on the weekend`/`at the weekend`); verificare prezenta subiect + verb corect + negativ/adverb daca e cerut. Ambiguitatile marginale → verdict LLM (vezi rubrica).
- `matching`: 0,4p / pereche corecta.
- `mcq` multi-select (/w/): scor complet doar daca ambele corecte si nicio bifa gresita.

**Rubrica LLM pt productie (vorbire/scriere) — daca testul include raspuns liber:**

| Criteriu | Descriptor A1 „trece" (>=1) | „nu trece" (0) |
|---|---|---|
| Grammar accuracy | subiect prezent; verb la baza fara -s la I/you/we; `don't` corect; adverb inaintea verbului | subiect omis repetat / `I no...` / `-s` gresit / adverb dupa verb |
| Vocabulary use | >=6 cuvinte-tinta din unitate, folosite corect | <6 sau folosire gresita a sensului |
| Task fulfillment | >=8 propozitii, 2 negative, 2 adverbe | sub oricare din praguri |

**Prag productie:** toate 3 criteriile la >=1.

**MAPARE obiective ① → itemi de test:**

| Obiectiv ① (Stratul 1) | Itemi care il testeaza |
|---|---|
| ①.1 Descrie rutina proprie (>=8 prop., pers. I present simple) | Scenariu F (task-based) · rubrica LLM „Task fulfillment" · reorder (I always get up early) · cloze `have` |
| ①.2 Spune ce NU face (`don't + verb`, >=2) | cloze „don't watch" · mcq „I don't" · translate „I don't work on the weekend" · cloze „don't go" · rubrica LLM |
| ①.3 Cat de des (adverbe de frecventa, plasare corecta, >=2) | cloze „always" · mcq ordine „I often watch TV" · reorder „We never watch TV" · cloze „never" · translate „I sometimes eat late" |
| ①.4 Recunoaste/numeste ~60 cuvinte (RO→EN >=7/10) | translate „get up" · translate „usually" · matching (have/go/make/listen/brush) · pachet SRS E |
| ①.5 Pronunta /w/ distinct de /v/ (>=4/6) | Sectiunea D (drill + scorare fonetica) · mcq multi-select „work, watch" |

---


### A1-U9 — He works, she plays · Straturile 2 & 3 (Pipeline + Consolidare)

## STRATUL 2 — Pipeline (conversatie & voce cu EVA)

### A. Configuratia EVA (system prompt pt unitate)

```
ROL: Esti EVA, un tutore de engleza prietenos, calm si rabdator. Vorbesti cu un
adult ROMAN care invata engleza de la zero. Nivel STRICT A1. Esti incurajatoare,
nu corectezi niciodata cu "rosu" si nu certi. Zambesti in cuvinte, folosesti emoji
rar (max 1/replica).

TEMA UNITATII (A1-U9): persoana a III-a singular (he/she/it) la present simple si
intrebarile WH. Vrei ca cel care invata sa DESCRIE o alta persoana: ce meserie are,
unde lucreaza, cand incepe, ce face seara, ce NU face.

STRUCTURI-TINTA DE ELICITAT (numai acestea, nimic peste nivel):
- Afirmativ pers. III: "He/She works / plays / watches / goes / studies ..." (+ -s/-es/-ies)
- Negativ: "He/She doesn't work / eat / drink ..."
- Intrebari WH: "What/Where/When/Who does he/she ...?"
- Intrebare da/nu: "Does he/she ...?" -> "Yes, he does. / No, he doesn't."

VOCABULAR-TINTA (foloseste DOAR de aici sau ce e sub nivel):
- Profesii: teacher, doctor, nurse, driver, cook, waiter, farmer, student, singer, worker
- Verbe: work, play, watch, go, read, write, teach, drive, cook, eat, drink, live, start,
  finish, study, speak, help, wash, clean, get up
- WH & aux: what, where, when, who, does, doesn't
- Locuri/timp: hospital, school, restaurant, office, job, morning, evening, every day, people

REGULI DE LIMBA IN LECTIE:
- Vorbesti ~70% engleza simpla, ~30% romana (sprijin). La A1 dai indiciul in engleza,
  iar daca userul tace sau nu intelege, traduci scurt in romana intre paranteze.
- Propozitii scurte (max 6-8 cuvinte). O singura intrebare pe replica.
- NU introduci timpuri noi (fara past, fara continuous), fara pronume noi peste el/ea/it.

CORECTARE PRIN RECAST (blanda, fara marcaj):
- Daca userul spune "He work in a hospital" -> raspunzi natural reformuland corect:
  "Ah, he workS in a hospital! Nice. And when does he start?" — accentuezi discret forma
  corecta, apoi mergi mai departe. NU spui "gresit".
- Greseala tipica romani #1: lipsa lui -s la afirmativ (He work -> He works).
- Greseala tipica romani #2: dublarea lui -s in intrebare/negatie (Does he works? /
  He doesn't works) -> recast: "Right — does he WORK on Sunday?" / "He doesn't WORK, exactly."
- Dupa recast, poti adauga o mica nota in romana DOAR daca userul repeta greseala de 2 ori:
  "(Micul truc: cand apare *does/doesn't*, verbul ramane fara -s.)"

REACTII:
- La TACERE (fara raspuns): asteapta, apoi ofera un model: "You can say: 'She is a teacher.'
  Try it! (Poti spune...)". Oferi 2 optiuni daca inca tace.
- La GRESEALA: recast + mergi inainte, nu insista.
- La REUSITA: lauda scurt si specifica ("Great — you used -s correctly!").

OBIECTIV DE SESIUNE: userul produce >=5 intrebari WH corecte cu do/does si >=4 propozitii
la pers. III (afirmativ + negativ). Inchei cand a descris o persoana complet (meserie,
loc, ora, o activitate de seara, un lucru pe care NU il face).
```

### B. Fluxul conversatiei (3 etape)

**Etapa 1 — GHIDAT** (EVA conduce; user completeaza dupa model)

| # | EVA (replica) | Raspuns MODEL (user) | Structura elicitata |
|---|---|---|---|
| 1 | Hi! Let's talk about a person. Tell me about your brother or sister. Who is it? | This is my brother. / This is my sister. | This is my ___. |
| 2 | Nice! **What does he do?** (Cu ce se ocupa?) | He is a driver. | He is a + profesie |
| 3 | A driver! **Where does he work?** | He works in a company. / He drives a bus. | He works + -s |
| 4 | Good. **When does he start** work? | He starts at seven. | He starts (+ -s, ora) |
| 5 | **Does he work** on Sunday? | No, he doesn't. | Yes/No + does/doesn't |
| 6 | And **what does he do** in the evening? | He watches TV. / He reads books. | He watches / reads (+ -s) |

*Structura de elicitat:* propozitie afirmativa pers. III cu `-s` + un raspuns scurt cu `does/doesn't`.

**Etapa 2 — SEMI-GHIDAT** (intrebari deschise + indicii)

- EVA: *Tell me one thing she does every morning.* — indiciu: *(get up / eat / go to work...)*
- EVA: *And one thing he does NOT do?* — indiciu: *(He doesn't ___ ... coffee? meat? work on Sunday?)*
- EVA: *Now YOU ask me about my job. Use "Where..." or "When..."* — indiciu: *(Where does EVA...? / When does EVA...?)*
- EVA: *Who cooks at home in your family?* — indiciu: *(My mother cooks / My father cooks...)*

Reguli EVA: da 1 indiciu, asteapta, apoi recast la raspuns. Daca userul pune intrebarea WH corect, lauda specific: *"Perfect question! You put 'does' before the verb."*

**Etapa 3 — LIBER** (scenariu + obiectiv, cu branching)

**Scenariu:** *"A new friend"* — userul ii prezinta lui EVA o persoana reala din familie/prieteni si o descrie complet (meserie, loc, ora de start, o activitate de seara, un lucru pe care NU il face). EVA reactioneaza natural si pune 2-3 intrebari WH proprii.

**Obiectiv:** minim 5 propozitii pers. III corecte + 1 negativ cu `doesn't` + userul pune cel putin 1 intrebare WH.

**Branching:**
- *Daca userul GRESESTE (-s lipsa / -s dublat):* recast bland, fara oprire. La a 2-a repetare -> micro-nota RO in paranteza, apoi o mini-repetare: *"Say it with me: She workS."*
- *Daca userul TACE:* EVA ofera un schelet: *"You can start with: 'This is my ___. He/She is a ___.'"* Daca inca tace, EVA pune o intrebare inchisa (da/nu): *"Is it a man or a woman?"*
- *Daca userul depaseste nivelul (foloseste past/continuous):* EVA nu corecteaza gramatica noua, doar readuce la present: *"Nice! And today, what does she do every day?"*
- *Daca userul reuseste fluent:* EVA ridica usor stacheta cu o intrebare `Who...?` sau cere un detaliu in plus (ora exacta / al doilea verb de seara).

### C. Ascultare (script audio pt TTS + itemi)

**Script audio** (monolog scurt A1, ~40 cuvinte, ritm lent, o voce feminina):

```
[TTS · voce feminina · viteza 0.9 · pauze scurte dupa fiecare propozitie]

My name is Elena. My friend Paul is a cook.
He works in a big restaurant in the city.
He starts at ten o'clock in the morning.
He cooks pizza and pasta. People love his food!
Paul doesn't work on Monday. On Monday he plays football.
```

**Itemi de comprehensiune (4-5) + Raspunsuri:**

1. What is Paul's job? — *He is a cook.*
2. Where does he work? — *In a big restaurant (in the city).*
3. When does he start work? — *At ten o'clock (in the morning).*
4. Does Paul work on Monday? — *No, he doesn't.*
5. What does he do on Monday? — *He plays football.*

### D. Pronuntie (drill + scorare)

**Sunete-tinta (focus romani):** terminatia `-s` cu 3 realizari — **/s/** (dupa surd), **/z/** (dupa sonor/vocala), **/ɪz/** (dupa suierator) — plus auxiliarul redus **does** /dəz/.

**Minimal pairs / contraste utile:**
- /s/ vs /z/: **works** /wɜːks/ ↔ **plays** /pleɪz/ ; **starts** /stɑːts/ ↔ **reads** /riːdz/
- /z/ vs /ɪz/: **goes** /ɡəʊz/ ↔ **watches** /ˈwɒtʃɪz/ ; **lives** /lɪvz/ ↔ **washes** /ˈwɒʃɪz/
- silaba extra: **finish** /ˈfɪnɪʃ/ (2 sil.) ↔ **finishes** /ˈfɪnɪʃɪz/ (3 sil.) — atentie, `-es` = silaba noua.

**Lista de cuvinte (grupate):**
- /s/: works, starts, helps, eats, gets, drinks
- /z/: plays, reads, goes, lives, cleans, drives
- /ɪz/: watches, washes, finishes, teaches

**Propozitii de drill (3-5):**
1. He **works** and she **plays**. /wɜːks/ … /pleɪz/
2. She **watches** TV and **finishes** at ten. /ˈwɒtʃɪz/ … /ˈfɪnɪʃɪz/
3. My father **reads** and **goes** to work. /riːdz/ … /ɡəʊz/
4. **Does** he **teach** English? /dəz/ … /tiːtʃ/
5. He **doesn't drink** coffee. /ˈdʌzənt drɪŋk/

**Config de scorare:**
- Foneme evaluate: realizarea finala `-s` (/s/ ~ /z/ ~ /ɪz/), prezenta silabei /ɪz/ la `watches/finishes/teaches/washes`, si reducerea `does` -> /dəz/ in vorbire.
- Prag: scor global **≥80** pt promovare; per-fonem `-s` corect la **≥8/10** itemi.
- Feedback tipic pt romani:
  - Tind sa nu pronunte deloc `-s`-ul final -> reminder: *"Add a small /s/ or /z/ at the end: work-S."*
  - Confunda /z/ cu /s/ (asurzesc consoana finala, tipic RO) -> *"'plays' ends soft: /pleɪz/, not /pleɪs/."*
  - Uita silaba /ɪz/ -> *"'watches' has TWO parts: wat-ches /ˈwɒtʃɪz/."*
  - Pronunta `does` plin /dʌz/ mereu -> in vorbire fluenta e slab /dəz/.

**Set de shadowing (3-5, userul repeta imediat dupa TTS):**
1. She works in a hospital.
2. He plays football on Sunday.
3. My mother teaches English.
4. He doesn't drink coffee.
5. Where does he live?

## STRATUL 3 — Consolidare & evaluare

### E. Pachet SRS (carduri live)

| Front | Back | Tip | Nota |
|---|---|---|---|
| She works in a hospital. | Ea lucreaza intr-un spital. | EN→RO | `-s` afirmativ |
| He plays football on Sunday. | El joaca fotbal duminica. | EN→RO | vocala+y → plays |
| What does she do? | Cu ce se ocupa? / Ce face ea? | EN→RO | WH + does |
| Where does he live? | Unde locuieste el? | RO→EN | intrebare WH |
| My mother teaches English. | Mama mea preda engleza. | EN→RO | -ch → teaches |
| He doesn't drink coffee. | El nu bea cafea. | RO→EN | doesn't + baza |
| She watches TV in the evening. | Ea se uita la televizor seara. | EN→RO | -ch → watches |
| When does the school start? | Cand incepe scoala? | EN→RO | WH cu obiect nesubiect |
| Who cooks at home? | Cine gateste acasa? | RO→EN | who + -s |
| He gets up at six o'clock. | El se trezeste la ora sase. | EN→RO | phrasal get up + -s |
| She goes to work by car. | Ea merge la munca cu masina. | EN→RO | -o → goes |
| The driver starts early. | Soferul incepe devreme. | RO→EN | -s /s/ |
| Does he speak English? | Vorbeste el engleza? | EN→RO | intrebare da/nu |
| My father reads every day. | Tatal meu citeste in fiecare zi. | EN→RO | -s /z/ |
| She doesn't work on Sunday. | Ea nu lucreaza duminica. | EN→RO | doesn't + baza |
| He ____ (watch) football. → watches | El se uita la fotbal. | cloze | regula -es |
| She ____ (study) English. → studies | Ea studiaza engleza. | cloze | cons.+y → -ies |
| Where ____ he work? → does | Unde lucreaza el? | cloze | auxiliar does |
| He ____ cook at home. → doesn't | El nu gateste acasa. | cloze | negativ |
| He ____ (go) to work by car. → goes | El merge la munca cu masina. | cloze | -o → goes |

**Config FSRS (pe scurt):**
- Tag-uri: `a1-u9`, `present-3rd`, `wh-questions`, `does-doesnt`, `phonics-s`.
- Introducere: cardurile EN→RO/RO→EN se lanseaza imediat dupa dialogul ③ si task-ul ⑧; cloze-urile dupa exercitiile ⑤ (userul a vazut deja regula).
- Prioritate: cardurile de `does/doesn't` si cele de scriere (`-es`/`-ies`) au retention target usor mai mare (0.92) fiindca sunt greseala tipica RO; restul 0.90.
- Reintroducere a vocabularului de profesii ca sub-deck (EN→RO) daca retentia scade sub 70%.

### F. Scenariu task-based

**Situatia reala:** Userul intalneste un coleg nou online si ii povesteste lui EVA despre un membru al familiei care are o meserie interesanta. Trebuie sa il descrie complet, ca EVA sa "il cunoasca".

**Obiectiv:** Descrie o persoana la pers. III: meserie + loc de munca + ora de start + o activitate de seara + un lucru pe care NU il face. In plus, userul pune cel putin o intrebare WH lui EVA.

**Criterii de succes MASURABILE:**
- ≥5 propozitii pers. III cu `-s/-es/-ies` corect.
- ≥1 propozitie negativa cu `doesn't` (+ verb la baza).
- ≥1 intrebare WH corecta formulata de user (`does` + verb-baza).
- Task completat = toate cele 5 informatii transmise inteligibil.

**Rubrica de scorare LLM (A1):**

| Criteriu | 3 (bun A1) | 2 (in curs) | 1 (insuficient) |
|---|---|---|---|
| Task completion | Toate 5 info + 1 intrebare WH | 3-4 info, fara intrebare | ≤2 info |
| Accuracy (-s / does) | `-s` corect ≥80%, `does/doesn't` fara verb dublat | greseli ocazionale, mesaj clar | omite `-s` sistematic sau dubleaza in intrebari |
| Fluency | raspunsuri prompte, propozitii scurte legate | ezitari, are nevoie de indicii | tacere lunga, doar cuvinte izolate |

**Prag:** promovat la **≥7/9** (si minim 2 la Accuracy).

**Variante:**
- V1: descrie un prieten in loc de familie.
- V2: descrie doua persoane si contrasteaza (*He works in a hospital, but she works in a school.*).
- V3 (mai usor): userul raspunde doar la intrebarile WH ale EVei (fara initiativa proprie).

### G. Evaluare automata (test de unitate)

**Itemi structurati** `[tip | intrebare | (optiuni) | raspuns_corect | puncte]`:

```
[cloze | She ____ (work) in a school. | — | works | 1]
[cloze | He ____ (watch) TV in the evening. | — | watches | 1]
[cloze | My father ____ (go) to work by car. | — | goes | 1]
[cloze | He ____ (study) English every day. | — | studies | 1]
[mcq | ____ she speak English? | Do / Does / Is | Does | 1]
[mcq | Where ____ they live? | do / does / is | do | 1]
[cloze | He ____ (not/like) coffee. → doesn't ____ | — | doesn't like | 1]
[reorder | Fa intrebarea: work / where / does / he / ? | — | Where does he work? | 1]
[reorder | Fa intrebarea: does / what / she / do / ? | — | What does she do? | 1]
[matching | Leaga profesia de verb: 1)teacher 2)cook 3)driver 4)singer | a)drives a bus b)teaches children c)sings songs d)cooks food | 1-b,2-d,3-a,4-c | 1]
[transform | Din pers. I in pers. III: "I finish at three." → She ____ | — | She finishes at three. | 1]
[negative | Completeaza: She ____ ____ (eat) meat. | — | doesn't eat | 1]
[translate | Ea lucreaza intr-un spital. | — | She works in a hospital. | 1]
[translate | Unde locuieste el? | — | Where does he live? | 1]
[correct | Corecteaza: Does he plays? | — | Does he play? | 1]
[phonics | Grupeaza dupa sunet final /s/·/z/·/ɪz/: works, plays, watches, reads, finishes, starts, goes, teaches | — | /s/: works,starts ; /z/: plays,reads,goes ; /ɪz/: watches,finishes,teaches | 2]
```

**Logica de scorare:**
- Total = 18 puncte. Normalizare la 100%.
- `cloze/transform/negative/correct`: match exact dupa normalizare (lowercase, trim, colaps spatii, `'`↔`’`). Accepta contractia `doesn't` = `does not`.
- `mcq/matching`: match exact pe cheie.
- `reorder`: match exact al propozitiei tinta (ignora majuscula initiala si `?`).
- `translate`: fuzzy — corect daca contine forma verbala corecta (`-s`/`does`) SI cuvintele-cheie; toleranta pentru `a`/lipsa articol.
- `phonics`: 2p, partial 1p daca ≥6/8 verbe corect grupate.
- **Prag de promovare: ≥80%** (≥14,4/18 → practic ≥15/18).

**Rubrica LLM pt productie (vorbire/scriere)** — se aplica raspunsului liber la task ⑧/F:

| Criteriu | Descriptor A1 "promovat" |
|---|---|
| Accuracy | `-s` la pers. III corect ≥80% din verbe; `does/doesn't` folosit fara verb dublat; verbul principal la baza in intrebare/negativ. |
| Range | Foloseste ≥6 verbe-tinta si ≥3 intrebari WH diferite. |
| Task/Fluency | Transmite cele 5 informatii; propozitii scurte inteligibile; ezitari acceptabile. |

**Prag LLM:** promovat daca Accuracy = "promovat" **si** cel putin 2 din 3 criterii atinse.

**MAPARE obiective ① → itemi:**

| Obiectiv ① (Stratul 1) | Itemi care il testeaza |
|---|---|
| Descrie rutina la pers. III, `-s/-es` ≥8/10 | cloze (works, watches, goes, studies), transform (finishes), translate (She works...), rubrica Accuracy |
| Formeaza intrebari WH cu do/does ≥5/6 | mcq (Does/do), reorder (Where does he work? / What does she do?), translate (Where does he live?), rubrica Range |
| Propozitii negative cu `doesn't` ≥4/5 | cloze "doesn't like", negative "doesn't eat", correct (He doesn't cook din banca ⑤) |
| Pronunta `-s` (/s/–/z/–/ɪz/) ≥8/10 | phonics (grupare 8 verbe), drill+scorare D (prag ≥80) |
| Numeste profesii uzuale ≥6/8 | matching (teacher/cook/driver/singer), SRS sub-deck profesii, task F (meserie obligatorie) |

---


I have read the Layer 1 file. Now I will produce Layers 2 and 3, fully coherent with the exact text, vocabulary, task ⑧, SRS bank ⑨, and objectives ① already written.

### A1-U10 — My house · Straturile 2 & 3 (Pipeline + Consolidare)

## STRATUL 2 — Pipeline (conversatie & voce cu EVA)

### A. Configuratia EVA (system prompt pt unitate)

```
ROL & PERSONA
Ești EVA, o tutore de engleză prietenoasă, caldă și foarte răbdătoare. Vorbești cu
un adult vorbitor de ROMÂNĂ, nivel A1, la Unitatea 10 „My house". Ești încurajatoare,
zâmbești în cuvinte, folosești mesaje scurte (max 1–2 propoziții per replică), ca într-un
chat de WhatsApp. Nu ești un profesor sever; ești un prieten care ajută.

NIVEL & DOMENIU LINGVISTIC (nu depăși!)
- Doar A1. Gramatică permisă: to be, have got, can, prezentul simplu, plural, articolele
  a/an/the, numerale, și — NOU în această unitate — „there is / there are" (+/–/?),
  „some/any", prepoziții de loc: in, on, under, next to, behind, between, in front of, near.
- NU folosi: past tense, present continuous pentru povestire, present perfect, condiționale,
  vocabular peste A1. Propoziții scurte, frecvente, concrete.

TEMA & VOCABULAR-ȚINTĂ (elicitează ACESTE cuvinte)
- Camere: house, home, room, kitchen, bathroom, bedroom, living room, dining room, hall,
  garage, garden, door, window, floor, wall, stairs.
- Mobilier & obiecte: table, chair, sofa, armchair, bed, desk, shelf, bookshelf, wardrobe,
  cupboard, drawer, mirror, carpet, lamp, clock, picture, curtain, fridge, cooker, oven,
  sink, bath, shower, toilet, TV, phone, plate, cup, glass, book, key, bag, box, ball, toy,
  plant, vase, pillow, blanket.
- Prepoziții: in, on, under, next to, behind, between, in front of, near.

STRUCTURI DE ELICITAT (fă cursantul să LE PRODUCĂ)
1. „There is a … / There are … + număr" (descriere).
2. „There isn't a … / There aren't any …" (negativ).
3. „Is there a …? / Are there any …?" + răspuns scurt (Yes, there is. / No, there aren't.).
4. Obiect + prepoziție de loc: „The lamp is on the desk." „The bag is under the bed."

CORECTARE PRIN RECAST (blând, fără roșu, fără „Wrong!")
- Nu marca greșeala explicit. Reformulează natural forma corectă, apoi mergi mai departe.
  Ex.: User: „There is two chairs." → EVA: „Nice — there ARE two chairs! And what is on the
  table?" (accentuezi discret forma corectă, apoi întrebi mai departe).
- Greșeli tipice de vizat: „It is a book on the table" → „There is a book…"; „is" în loc de
  „are" la plural; lipsa inversiunii la întrebare; „some" la întrebare în loc de „any";
  „next of / near of" → „next to / in front of".
- Corectează maxim 1 lucru per replică. Laudă orice încercare reușită.

PROPORȚIA RO/EN (A1: sprijin în română, dozat)
- ~75–80% engleză, ~20–25% română. Româna DOAR pentru: a debloca, a traduce un cuvânt nou,
  a da o instrucțiune de sarcină, a liniști. Formatul: engleză + glosă scurtă în paranteză.
  Ex.: „Is there a garden? (o grădină?)". Nu traduce propoziții întregi dacă nu e nevoie.

CE CERI CURSANTULUI
- Să descrie o cameră (a lui sau din imagine): ce se află unde, minim 6 propoziții.
- Pui întrebări simple: „What is in the kitchen?", „Where is the sofa?", „Is there a …?",
  „Are there any …?". Una câte una. Aștepți răspunsul.

REACȚIE LA TĂCERE / GREȘEALĂ / „NU ȘTIU"
- Tăcere >1 replică: oferă un început de propoziție ca sprijin: „Try: There is a ______ …".
- „I don't know" / „nu știu": dă un cuvânt-model + traducere: „Maybe a bed? (un pat) —
  There is a bed. Try you!".
- Greșeală: recast (vezi mai sus), niciodată critică.
- Menține ritmul: 1 întrebare → aștepți → laudă/recast → următoarea întrebare.

STIL DE IEȘIRE
- Mesaje scurte. Emoji sobru, ocazional (🙂🏠), nu în exces. Fără liste lungi. Fără explicații
  gramaticale nesolicitate — dacă cursantul cere, dă nota scurtă în română.
```

### B. Fluxul conversatiei (3 etape)

**Etapa 1 — GHIDAT** (EVA conduce; cursantul completează structuri fixe)

| # | EVA (pornire) | Răspuns MODEL (cursant) | Structura de elicitat |
|---|---|---|---|
| 1 | Hi! 🏠 Let's talk about your house. How many rooms are there? | There are four rooms. | There are + număr |
| 2 | Nice! What is in the living room? | There is a sofa and a TV. | There is a … |
| 3 | Is there a table in the living room? *(o masă?)* | Yes, there is. | răspuns scurt afirmativ |
| 4 | Where is the sofa? *(unde e canapeaua?)* | It is next to the window. | obiect + prepoziție |
| 5 | Great! Are there any plants? *(vreo plantă?)* | Yes, there are. There is a plant on the window. | Are there any…? + There is |
| 6 | Lovely! Is there a garden? | No, there isn't. | răspuns scurt negativ |

*Dacă cursantul dă doar un cuvânt (ex. „sofa"), EVA recast + reîncadrează: „Yes — there is a sofa! 🙂"*

**Etapa 2 — SEMI-GHIDAT** (întrebări deschise + indicii „prompts")

- EVA: **Tell me about your kitchen.** *(prompt: fridge? cooker? cups?)* → cursantul produce 2–3 propoziții cu *there is/are*.
- EVA: **What is on your desk?** *(prompt: lamp / book / phone — on the desk)* → obiect + *on*.
- EVA: **Where is your bag?** *(prompt: under / behind / next to)* → obiect + prepoziție.
- EVA: **Are there any pictures on the wall?** → răspuns scurt + locație.
- EVA: **Describe your bedroom in three sentences.** *(prompt: bed, wardrobe, lamp)* → 3× *there is/are* + prepoziții.

Indicii se dau DOAR dacă apare ezitare; altfel EVA lasă cursantul liber și doar reacționează (laudă/recast).

**Etapa 3 — LIBER** (scenariu + obiectiv + branching)

- **Scenariu:** „**Show me your room!**" Cursantul descrie camera lui reală (sau imaginea din aplicație) în **≥6 propoziții**, folosind *there is/are* și **≥4 prepoziții de loc**. EVA pune 3–4 întrebări de aprofundare (Is there…? Where is…? Are there any…?).
- **Obiectiv (măsurabil):** ≥6 propoziții, ≥80% corecte, ≥4 prepoziții corecte (leagă de ① obiectivele 1 & 2).

Branching:
- **Dacă tace (>8s / o replică goală):** EVA oferă un starter — „No problem 🙂 Try: In my room there is a ______." și numește un obiect model.
- **Dacă greșește forma** („There is two beds"): recast — „There ARE two beds — cool! And where are they?" (fără a opri fluxul).
- **Dacă folosește RO** („e un pat lângă geam"): EVA traduce-model și cere reluarea în EN — „In English: There is a bed next to the window. Now you try! 🙂".
- **Dacă răspunde corect & scurt:** EVA extinde — „Nice! And what is UNDER the bed?" ca să obțină mai multe prepoziții.
- **Dacă termină <6 propoziții:** EVA cere completare țintită — „Two more! Is there a lamp? A picture? A carpet?".
- **La final:** EVA laudă + rezumă discret formele reușite: „Great job! Your room has a bed, a desk and a lamp — lovely! 🏠".

### C. Ascultare (script audio pt TTS + itemi)

**Script audio (dialog scurt A1, ~40s, 2 voci — de generat cu TTS; voce feminină EVA + voce Tom):**

```
EVA: Hi, Tom! Tell me about your bedroom.
TOM: Hello, EVA! My bedroom is small but nice. There is a bed and a big wardrobe.
EVA: Is there a desk?
TOM: Yes, there is. It is next to the window. There is a lamp on the desk.
EVA: Are there any books?
TOM: Yes, there are. There are many books on the shelf, behind the door.
EVA: And where is your bag?
TOM: My bag is under the bed. There is a ball in the bag!
EVA: Ha! Your bedroom is lovely, Tom.
```

*Note TTS: ritm lent A1, pauze clare între propoziții; accentuează /ð/ în „there/the" și /θ/ în „bathroom" (dacă e reutilizat); „next to" → formă slabă /ˈnekstə/.*

**Itemi de comprehensiune (4–5) + Răspunsuri:**
1. What is in Tom's bedroom? *(numește 2 lucruri)*
2. Where is the desk?
3. Are there any books? Where?
4. Where is Tom's bag?
5. What is in the bag?

**Răspunsuri:**
1. There is a bed and a (big) wardrobe. *(și un desk + lamp)*
2. It is next to the window.
3. Yes, there are. They are on the shelf, behind the door.
4. It is under the bed.
5. There is a ball (in the bag).

### D. Pronuntie (drill + scorare)

**Sunete-țintă (RO-focus):**
- **/ð/** (th sonor, cu voce, limba între dinți) — românii tind să spună „d/z".
- **/θ/** (th surd, fără voce) — românii tind să spună „t/s/f".
- **Forme slabe:** *next to* /ˈnekstə/, *in front of* /ɪn ˈfrʌntəv/.

**Minimal pairs (perechi de contrast):**
| /ð/ sau /θ/ vs. eroare RO | | |
|---|---|---|
| there /ðeə/ | vs. **dare** /deə/ | (nu „der/zer") |
| they /ðeɪ/ | vs. **day** /deɪ/ | |
| thin /θɪn/ | vs. **tin** /tɪn/ | (nu „tin") |
| bath /bɑːθ/ | vs. **bat** /bæt/ | |
| three /θriː/ | vs. **tree** /triː/ | |
| mouth /maʊθ/ | vs. **mouse** /maʊs/ | (nu „s") |

**Lista de cuvinte (drill):** there, the, they, this, that (/ð/) · bathroom, bath, three, think, mouth (/θ/).

**Propoziții de drill (3–5):**
1. **There** is a **bath** in the **bathroom**.
2. **There** are **three** chairs.
3. **They** are in **the** living room.
4. **This** is **the** door, **that** is **the** window.
5. The mirror is next to /ˈnekstə/ the **bath**.

**Config de scorare:**
- **Foneme evaluate:** /ð/ (there, the, they, this, that) și /θ/ (bathroom, bath, three, think, mouth); bonus: forme slabe /ˈnekstə/, /ɪn ˈfrʌntəv/.
- **Prag:** ≥80% pe setul de cuvinte-țintă pentru „trecut" (aliniat la ⑦ care cere ≥70% minim; ținta drill = 80). Scor per cuvânt: 1 dacă fonemul-țintă e produs corect (voce/lipsă voce + poziția limbii), 0 altfel.
- **Feedback tipic pt români:**
  - /ð/ → „d/z": „Pune vârful limbii ÎNTRE dinți și pornește vocea — bzzz. There, nu «der»."
  - /θ/ → „t/f/s": „Limba între dinți, DAR fără voce — suflă. Bath, nu «bat/bas»."
  - „next to" citit „nekst tu": „Leagă-le: /ˈnekstə/, «to» devine slab."

**Set de shadowing (3–5, cursantul repetă după TTS, sincron):**
1. There is a sofa next to the window.
2. There are three books on the shelf.
3. The bag is under the bed.
4. Is there a bath in the bathroom?
5. The picture is behind the door.

## STRATUL 3 — Consolidare & evaluare

### E. Pachet SRS (carduri live)

| Front | Back | Tip | Notă |
|---|---|---|---|
| There is a bed in the bedroom. | Există un pat în dormitor. | EN→RO | there is (sg) |
| Există un pat în dormitor. | There is a bed in the bedroom. | RO→EN | there is (sg) |
| There ___ two chairs in the kitchen. | are | cloze | plural → are |
| There are two chairs in the kitchen. | Sunt două scaune în bucătărie. | EN→RO | there are (pl) |
| Is there a bathroom? | Există o baie? | EN→RO | întrebare sg |
| Există o baie? | Is there a bathroom? | RO→EN | inversiune |
| ___ there any plants? | Are | cloze | întrebare pl + any |
| Yes, there is. / No, there isn't. | Da, există. / Nu, nu există. | EN→RO | răspuns scurt sg |
| Sunt (vreo) plante? | Are there any plants? | RO→EN | any la întrebare |
| No, there aren't. | Nu, nu sunt. | EN→RO | răspuns scurt pl |
| The lamp is ___ the desk. (pe) | on | cloze | prepoziție on |
| The bag is under the bed. | Geanta este sub pat. | EN→RO | prepoziție under |
| The sofa is next to the window. | Canapeaua este lângă fereastră. | EN→RO | next to |
| Tabloul este în spatele ușii. | The picture is behind the door. | RO→EN | behind |
| The table is ___ two chairs. (între) | between | cloze | between |
| There is a mirror on the wall. | Există o oglindă pe perete. | EN→RO | there is + on |
| There aren't ___ cups in the cupboard. | any | cloze | negativ + any |
| Nu sunt cești în dulap. | There aren't any cups in the cupboard. | RO→EN | negativ pl |
| There is a plant ___ ___ ___ the window. (în fața) | in front of | cloze | in front of |
| Casa mea are patru camere. | My house has four rooms. | RO→EN | have got/has |

**Config FSRS (pe scurt):**
- **Tag-uri:** `a1-u10`, `there-is-are`, `prepositions`, `vocab-house`, `question-answer`.
- **Introducere:** cardurile se activează DUPĂ ce cursantul termină Etapa 1 (ghidat) din Stratul 2 — nu înainte, ca să existe expunere prealabilă.
- **Ordinea de introducere:** întâi EN→RO (recunoaștere), apoi RO→EN (producție) după prima reușită, cloze la reviziile ulterioare (cel mai greu).
- **Parametri:** desired retention 0.90; carduri noi/zi la A1 max 8–10; „again" pe RO→EN re-programează cardul EN→RO corespunzător ca refresh.

### F. Scenariu task-based

**Situația reală:** „**My room tour**". Cursantul are o poză cu camera lui (sau folosește imaginea din aplicație) și îi face lui EVA un „tur" al camerei prin chat/voce — exact sarcina ⑧ din Stratul 1. EVA joacă rolul unui prieten curios care pune întrebări.

**Obiectivul:** Descrie camera în **≥6 propoziții**, spunând ce se află unde, cu **≥4 prepoziții de loc**, răspunzând la 3–4 întrebări ale lui EVA.

**Criterii de succes (măsurabile):**
- ≥6 propoziții cu *there is/are* sau obiect+prepoziție.
- ≥4 prepoziții de loc folosite corect (in/on/under/next to/behind/between/in front of/near).
- Răspunde corect la ≥3 din întrebările lui EVA (Is there…? / Where…? / Are there any…?).
- ≥80% din propoziții gramatical corecte (there is vs there are; some/any).

**Rubrică de scorare LLM (0–4 per criteriu):**

| Criteriu | 4 (foarte bine A1) | 3 (bine) | 2 (suficient) | 0–1 (reia) |
|---|---|---|---|---|
| **Task completion** | ≥6 propoziții + răspunde la toate întrebările | 5–6 propoziții, majoritatea întrebărilor | 4 propoziții, câteva întrebări | <4 propoziții, nu răspunde |
| **Accuracy** | ≥80% corect, there is/are & prepoziții stabile | ~70% corect, greșeli minore | ~50–60%, confuzii is/are sau some/any | <50%, calchiază din RO („It is a…") |
| **Fluency** | răspunde prompt, propoziții legate | mici pauze, se autocorectează | pauze dese, are nevoie de indicii | tăceri lungi, nu produce |

**Prag task:** ≥ 8/12 (echivalent ~80% pe Task completion + Accuracy).

**Variante ale scenariului:**
1. **My kitchen** (fridge, cooker, cups, plates — some/any).
2. **My dream house** (rooms: garden, garage, dining room — there are + număr).
3. **Spot the difference** — EVA descrie o cameră, cursantul spune ce e diferit în a lui („In my room there isn't a…, but there is a…").

### G. Evaluare automata (test de unitate)

**Itemi structurați** `[tip | întrebare | (opțiuni) | răspuns_corect | puncte]`:

```
[MCQ | ___ two beds in the room. | There is / There are / It is | There are | 1]
[MCQ | The ball is ___ the box (minge înăuntru). | in / on / under | in | 1]
[MCQ | The lamp is ___ the sofa and the chair. | between / behind / on | between | 1]
[cloze | ___ there a bathroom? (întrebare, singular) | | Is | 1]
[cloze | There aren't ___ cups in the cupboard. | | any | 1]
[cloze | There is a plant ___ ___ ___ the window (în fața). | | in front of | 1]
[MCQ | Are there any plants? — correct short answer (negativ) | No, there isn't / No, there aren't / No, it isn't | No, there aren't | 1]
[matching | Potrivește camera cu obiectul | kitchen=fridge; bathroom=shower; bedroom=bed; living room=sofa | kitchen-fridge, bathroom-shower, bedroom-bed, living room-sofa | 4]
[reorder | is / there / a / lamp / on / the / desk | | There is a lamp on the desk. | 1]
[reorder | any / are / there / plants / ? | | Are there any plants? | 1]
[translate-check | Există o grădină? | | Is there a garden? | 1]
[translate-check | Sunt niște scaune în bucătărie. | | There are some chairs in the kitchen. | 1]
[translate-check | Nu există o cadă în baie. | | There isn't a bath in the bathroom. | 1]
[vocab | „unde faci duș" → cameră | | bathroom | 1]
[vocab | „unde ții mâncarea rece" → obiect | | fridge | 1]
[negative-transform | There is a clock on the wall. → negativ | | There isn't a clock on the wall. | 1]
[question-transform | There are cups in the cupboard. → întrebare | | Are there any cups in the cupboard? | 1]
```

**Logica de scorare:**
- Total puncte: 21 (matching valorează 4, restul 1 fiecare).
- **MCQ / vocab:** potrivire exactă (case-insensitive).
- **cloze / translate-check / transforms:** normalizează (lowercase, elimină punctuația finală, spații multiple); acceptă variante echivalente listate (ex. „There's" = „There is"; „some/any" corect după context — la întrebare/negativ doar `any`). La `translate-check` acceptă contracția și ordinea corectă a prepoziției.
- **reorder:** propoziția reconstituită trebuie să fie identică (ordine + capitalizare inițială + semn final corect ? / .).
- **matching:** 1 punct per pereche corectă (4 max).
- **Prag de promovare:** **≥80%** → ≥17/21.

**Producție (vorbire/scriere) — rubrică LLM:**

| Criteriu | Descriptor A1 „trecut" (≥prag) |
|---|---|
| **Task completion** | Descrie o cameră în ≥6 propoziții + răspunde la întrebări. |
| **Accuracy** | there is/are & prepoziții corecte ≥80%; folosește any la întrebare/negativ. |
| **Range (vocab)** | Folosește ≥8 cuvinte-țintă (camere/mobilier) + ≥4 prepoziții. |
| **Pronunție** | /ð/ (there) și /θ/ (bathroom) inteligibile ≥70% pe 6 cuvinte. |

Prag producție: ≥80% la Task completion + Accuracy și ≥70% la Pronunție.

**MAPARE obiective ① → itemi de test:**

| Obiectiv ① | Itemi care îl testează |
|---|---|
| **① 1** — descrie camerele cu *there is/are* (≥6 prop.) | MCQ „There are two beds", reorder „There is a lamp…", negative-transform, question-transform + **scenariul F** (producție ≥6 prop.) |
| **① 2** — spune unde se află obiectele (prepoziții) | MCQ „in the box", MCQ „between…", cloze „in front of", reorder + **scenariul F** (≥4 prepoziții) |
| **① 3** — întreabă/răspunde despre casă (*Is there/Are there* + răspuns scurt) | cloze „Is there…?", MCQ răspuns scurt „No, there aren't", question-transform, translate-check „Is there a garden?" |
| **① 4** — folosește ~60 cuvinte casă/mobilier | matching (4 camere-obiecte), vocab „bathroom", vocab „fridge" + Range în rubrica de producție |
| **① 5** — pronunță /ð/ și /θ/ | Secțiunea D (drill + scorare), item de pronunție „bathroom" + criteriul Pronunție din rubrica LLM |

---


I have the full Layer 1. Now producing Layers 2 & 3, coherent with its exact text, vocabulary, task ⑧ and SRS bank ⑨.

### A1-U11 — Food & drink · Straturile 2 & 3 (Pipeline + Consolidare)

## STRATUL 2 — Pipeline (conversatie & voce cu EVA)

### A. Configuratia EVA (system prompt pt unitate)

```
ROL & PERSONA
Esti EVA, o tutore de engleza prietenoasa, calda si foarte rabdatoare. Vorbesti cu un
adult vorbitor nativ de ROMANA care este la nivelul A1 si invata engleza. Esti mereu
incurajatoare, niciodata critica. Zambesti in text (folosesti emoji simple: 😊 🙂 🍎).

NIVEL & TEMA
Nivel STRICT A1, Unitatea 11: "Food & drink" (mancare, bauturi, preferinte, abilitati).
Gramatica permisa pana aici: to be, have got, present simple (U9), plural, articole a/an,
this/that. NOU in aceasta unitate: like/don't like (+ noun / -ing), countable/uncountable
cu some/any, can/can't (abilitate). NU folosi timpuri sau structuri neintroduse (fara
past, fara present continuous pt actiuni, fara will, fara would like inca, fara comparative).

STRUCTURI-TINTA DE ELICITAT (fa cursantul sa le PRODUCA, nu doar sa le auda)
- I like + noun / I like + verb-ing  (I like tea. I like cooking.)
- I don't like + noun / -ing         (I don't like eggs. I don't like cooking.)
- Do you like…?                       (raspuns: Yes, I do. / No, I don't.)
- I've got some… / I haven't got any… / Have you got any…?
- I can… / I can't… / Can you…?  (fara "to", fara "-s")

VOCABULAR-TINTA (foloseste DOAR aceste cuvinte ca focus nou)
Fructe/legume: apple, banana, orange, grape, lemon, pear, strawberry, fruit, tomato,
potato, carrot, onion, salad, vegetable.
Mancare: bread, egg, cheese, butter, rice, pasta, meat, chicken, fish, soup, ham, jam,
sugar, salt, honey, yoghurt, cake, biscuit, chocolate, ice cream, sandwich, pizza, snack.
Bauturi: water, milk, tea, coffee, juice, coke.
Mese: breakfast, lunch, dinner, meal.
Verbe (pt can): eat, drink, cook, make, swim, drive, sing, dance, run.
Adjective/altele: like, favourite, delicious, hungry, thirsty, some, any.

REGULI DE CORECTARE — RECAST (reformulare blanda, NICIODATA marcaj rosu)
- Daca cursantul greseste, NU spui "gresit". Repeti corect, natural, si continui:
  User: "I like the coffee." → EVA: "Oh, you like coffee! 😊 I like coffee too. And do you
  like tea?"
  User: "She can to swim." → EVA: "Yes, she can swim! Great. Can you swim?"
  User: "I have got any milk." → EVA: "You've got some milk, nice! Have you got any bread?"
- Maxim O corectare pe replica (cea mai importanta). Restul le lasi sa curga.
- Lauzi efortul des: "Well done!", "Perfect!", "Good English!".

PROPORTIA RO/EN (A1: sprijin in romana, dozat)
- ~75% engleza simpla, ~25% romana DOAR pentru sprijin: glosare intre paranteze, o
  incurajare, sau clarificarea unei sarcini. Ex: "Are you hungry? (Ti-e foame?)".
- Cand cursantul e blocat sau tace, dai indiciul in romana + modelul in engleza.
- Nu traduce tot; da romana doar cand ajuta intelegerea.

CE CERI CURSANTULUI
Preferinte reale (like/don't like), ce mananca la mese, ce stie/nu stie sa faca (can/can't),
ce alimente are in casa (some/any). Pui O intrebare pe rand. Propozitii scurte.

REACTIE LA TACERE / GRESEALA
- Tacere (fara raspuns): reformulezi mai simplu + dai 2 optiuni.
  "What do you like — tea or coffee? ☕"
- Nu intelege: traduci intrebarea in romana + dai un raspuns-model in engleza.
- Greseala: RECAST (vezi mai sus), apoi mergi mai departe. Nu insisti pe eroare.
- Raspuns doar RO: accepti ideea, oferi versiunea engleza si ceri s-o repete blând.
  "Da, cartofi! In engleza: 'I like potatoes.' Can you say it? 🙂"

LUNGIME & TON: replici scurte (1-2 propozitii), calde, o singura intrebare pe replica.
```

### B. Fluxul conversatiei (3 etape)

**Etapa 1 — GHIDAT** (EVA porneste, cursantul completeaza dupa model)

| # | EVA (replica de pornire) | Raspuns MODEL asteptat | Structura de elicitat |
|---|---|---|---|
| 1 | Hi! I'm EVA. 😊 Are you hungry? *(Ti-e foame?)* | Yes, I am. / No, I'm not. | to be (recap) + hungry |
| 2 | What do you eat for breakfast? *(la micul dejun)* | I eat bread and cheese. I drink tea. | present simple: eat/drink |
| 3 | Nice! Do you like eggs? | No, I don't like eggs. / Yes, I like eggs. | (don't) like + noun |
| 4 | And do you like cooking? *(sa gatesti)* | Yes, I like cooking. / No, I don't like cooking. | like + verb-ing |
| 5 | Have you got any milk? *(Ai lapte?)* | Yes, I've got some milk. / No, I haven't got any milk. | some/any + have got |
| 6 | Can you cook? *(Stii sa gatesti?)* | Yes, I can cook soup. / No, I can't cook. | can/can't (ability) |

> Structura de elicitat, pe scurt: *I (don't) like + noun/-ing · Do you like…? · I've got some / I haven't got any · Can you…? / I can(’t)…*

**Etapa 2 — SEMI-GHIDAT** (intrebari deschise + indicii)

- EVA: *What's your favourite food?* — indiciu daca tace: *(pizza? chicken? salad?)*
- EVA: *What do you drink — water, juice or coffee?* — indiciu: *(My favourite drink is…)*
- EVA: *Tell me two things you like and one thing you don't like.* — indiciu: *(I like…, I like…, but I don't like…)*
- EVA: *What can you cook?* — indiciu: *(I can cook… / I can make…)*
- EVA: *Have you got any fruit at home?* — indiciu: *(I've got some… / I haven't got any…)*
- Prompt de extindere: dupa fiecare raspuns EVA cere UN detaliu: *Why? Is it delicious?* / *And for lunch?*

**Etapa 3 — LIBER** (scenariu + obiectiv)

> **Scenariu:** *"Lunch with EVA."* Este pranzul. EVA si cursantul isi spun ce le place, ce au in casa si ce stiu sa gateasca, ca si cum ar pregati masa impreuna. (coerent cu task-ul ⑧ din Stratul 1)
>
> **Obiectiv de productie:** cursantul produce **>=6 preferinte** (like/don't like), foloseste **some/any corect macar o data** si **>=2 propozitii cu can/can't**.

Branching — ce face EVA:
- **Daca cursantul raspunde bine** → EVA aprofundeaza: *"Delicious! And what about drinks? What's your favourite?"* si contorizeaza in tacere structurile-tinta produse.
- **Daca greseste** → RECAST scurt + continua: user *"I can to make soup"* → EVA *"You can make soup — yummy! 😋 Can you make a cake too?"*
- **Daca tace >1 replica** → EVA simplifica la alegere binara + model: *"No problem! Do you like tea or coffee? I like tea: 'I like tea.'"*
- **Daca raspunde in romana** → EVA valideaza ideea, ofera engleza, cere repetarea: *"Îți place ciocolata! In engleza: 'I like chocolate.' Say it with me 🙂"*
- **Inchidere** (dupa ce obiectivul e atins) → EVA rezuma pozitiv: *"Great lunch chat! You like chicken and rice, you can cook soup, and your favourite drink is tea. Well done! 🎉"*

### C. Ascultare (script audio pt TTS + itemi)

**Script audio (dialog A1, ~40s, 2 voci — de generat cu TTS):**

```
[NARRATOR]  Listen. Tom and Mia are hungry. It's lunchtime.
[TOM]  Hi Mia! Are you hungry?
[MIA]  Yes, I am! I like lunch. 😊
[TOM]  Me too. Do you like pizza?
[MIA]  No, I don't like pizza. But I like chicken and rice.
[TOM]  Have you got any bread?
[MIA]  Yes, I've got some bread and some cheese. I haven't got any soup.
[TOM]  Can you cook?
[MIA]  Yes, I can cook rice. But I can't make a cake!
[TOM]  That's OK. I can help you. What's your favourite drink?
[MIA]  My favourite drink is juice. I don't like coffee.
[TOM]  Me too! Let's eat. This chicken is delicious!
```

**Itemi de comprehensiune (5) + Raspunsuri:**
1. Does Mia like pizza? — *No, she doesn't.*
2. What food does Mia like? — *She likes chicken and rice.*
3. Has Mia got any bread? — *Yes, she's got some bread (and cheese).*
4. Can Mia make a cake? — *No, she can't.*
5. What is Mia's favourite drink? — *Juice. / Her favourite drink is juice.*

### D. Pronuntie (drill + scorare)

**Sunete-tinta (RO-focus):** **/æ/** (gura mai deschisa, intre „a" si „e"), **/e/** (ca „e" romanesc scurt), **/ɔː/** (o lung, buze rotunjite). Greseala tipica: romanii pun „e" peste tot (*epple* in loc de *apple*).

**Minimal pairs (/æ/ vs /e/):** bad – bed · man – men · ham – hem · sat – set · had – head · pan – pen.

**Lista de cuvinte de drill:**
- /æ/: **a**pple, h**a**m, j**a**m, c**a**rrot, s**a**ndwich, s**a**lad, b**a**nana(a doua silaba nu).
- /e/: br**ea**d, **e**gg, l**e**mon, br**ea**kfast, v**e**getable.
- /ɔː/: w**a**ter, s**a**lt.

**Propozitii de drill (5):**
1. I like **a**pple j**a**m on br**ea**d. *(/æ/ apple/jam vs /e/ bread)*
2. I eat **e**ggs and **ha**m for br**ea**kfast. *(/e/ vs /æ/)*
3. This s**a**lad has c**a**rrots and a l**e**mon.
4. Can I have some w**a**ter and s**a**lt? *(/ɔː/)*
5. The s**a**ndwich and the ch**ee**se are delicious.

**Config de scorare:**
- Foneme evaluate: **/æ/** (apple, ham, jam, carrot, sandwich, salad), **/e/** (bread, egg, lemon, breakfast), **/ɔː/** (water, salt).
- Prag: **scor >=80%** per cuvant (ASR/forced-alignment pe vocala-tinta); la nivel unitate criteriul din ① = **>=4/6** cuvinte corecte.
- Feedback tipic pt romani:
  - /æ/ auzit ca /e/ → „Deschide mai mult gura: *ham*, nu *hem*. E intre «a» si «e».”
  - /e/ prea deschis/lung → „Scurt, ca «e» romanesc: *egg, bread*.”
  - /ɔː/ nerotunjit → „Rotunjeste buzele si tine «o» lung: *waater, saalt*.”

**Set de shadowing (repeti dupa TTS, 5):**
1. I like apple and ham. 🍎
2. I eat eggs and bread for breakfast.
3. I've got some water and salt.
4. I don't like lemon in my tea.
5. This chicken sandwich is delicious!

## STRATUL 3 — Consolidare & evaluare

### E. Pachet SRS (carduri live)

| Front | Back | Tip | Nota |
|---|---|---|---|
| I like tea. | Imi place ceaiul. | EN→RO | din ⑨ · like + noun |
| I don't like coffee. | Nu-mi place cafeaua. | EN→RO | din ⑨ · don't like |
| Do you like eggs? | Iti plac ouale? | EN→RO | din ⑨ · Do you like…? |
| I like cooking. | Imi place sa gatesc. | EN→RO | din ⑨ · like + -ing |
| I've got some bread. | Am (niste) paine. | EN→RO | din ⑨ · some |
| I haven't got any milk. | Nu am (deloc) lapte. | EN→RO | din ⑨ · any (neg) |
| Have you got any juice? | Ai (niste) suc? | EN→RO | din ⑨ · any (intrebare) |
| An apple is good. | Un mar e bun. | EN→RO | din ⑨ · countable a/an |
| I eat bread for breakfast. | Mananc paine la micul dejun. | EN→RO | din ⑨ · meal |
| Water is good for you. | Apa e buna pentru tine. | EN→RO | din ⑨ · uncountable |
| I can cook rice. | Stiu sa gatesc orez. | EN→RO | din ⑨ · can |
| She can't drive. | Ea nu stie sa conduca. | EN→RO | din ⑨ · can't (pers. III) |
| Can you swim? | Stii sa inoti? | EN→RO | din ⑨ · Can you…? |
| This soup is delicious. | Supa asta e delicioasa. | EN→RO | din ⑨ · delicious |
| Nu-mi plac ouale. | I don't like eggs. | RO→EN | productie · don't like |
| Stiu sa gatesc supa. | I can cook soup. | RO→EN | productie · can |
| Ai (niste) paine? | Have you got any bread? | RO→EN | productie · any |
| I like ___ and rice. (chicken) | chicken | cloze | vocab · meat/chicken |
| I haven't got ___ sugar. (any) | any | cloze | gramatica · some/any |
| She ___ swim, but she can't drive. (can) | can | cloze | gramatica · can |

**Config FSRS (pe scurt):**
- Tag-uri: `A1-U11`, `food-drink`, sub-tag-uri `like`, `some-any`, `can`, `vocab`, `pronunciation`.
- Momentul introducerii: cardurile EN→RO se activeaza **imediat dupa lectie**; cardurile RO→EN si cloze (productie) intra **a doua zi** (dupa prima verificare de comprehensiune).
- Retentie-tinta: **90%** (default FSRS). Prag de succes al unitatii (din ⑦): **>=70%** din 15 cuvinte-tinta la review-ul din ziua 2.
- Prioritate reintroducere: cardurile marcate „lapse” pe structurile noi (some/any, can fara „to”) revin cu interval scurt.

### F. Scenariu task-based

> **Situatia reala:** *"Ordering / planning lunch."* Cursantul si EVA planuiesc pranzul impreuna. Cursantul spune ce ii place si ce nu, ce are in frigider (some/any) si ce stie sa gateasca (can/can't). (coerent cu task-ul ⑧)

- **Obiectiv:** poarta o conversatie de ~10 schimburi in care exprimi preferinte reale, verifici ce ai in casa si ce stii sa faci.
- **Criterii de succes MASURABILE:**
  - **>=6** propozitii de preferinta corecte (min. **2 afirmative** *I like* + **2 negative** *I don't like*).
  - foloseste **some/any corect >=1 data**.
  - **>=2** propozitii cu **can/can't** (fara „to”, fara „-s”).
  - foloseste **>=8 cuvinte-tinta** din vocabularul unitatii.

**Rubrica de scorare LLM (0-4 pe fiecare criteriu):**

| Criteriu | 4 (A1 solid) | 3 (A1 ok) | 2 (in curs) | 0-1 (insuficient) |
|---|---|---|---|---|
| Task completion | Toate obiectivele atinse: >=6 preferinte, some/any, >=2 can/can't | Aproape toate; lipseste un element minor | Doar partial (ex. fara can/can't) | Nu abordeaza sarcina |
| Accuracy | like/some/any/can corecte; fara „to” dupa can | 1-2 erori care nu blocheaza sensul | Erori repetate pe structurile-tinta | Structuri gresite/absente |
| Fluency (A1) | Raspunde prompt, propozitii scurte legate | Mici ezitari, dar continua | Depinde mult de indicii/RO | Tacere frecventa |

- **Prag task:** **>=9/12** total SI toate cele 3 criterii **>=2**.
- **Variante:** (a) *Breakfast chat* (coerent cu textul ③); (b) *At the shop* — „Have you got any…? / Yes, some… / No, not any…”; (c) *Cooking together* — accent pe can/can't + verbe cook/make.

### G. Evaluare automata (test de unitate)

**Itemi structurati** `[tip | intrebare | (optiuni) | raspuns_corect | puncte]`:

```
[MCQ    | She ___ swim.                              | can / cans / can to        | can            | 1]
[MCQ    | I like ___ .                               | a bread / bread / breads   | bread          | 1]
[MCQ    | Have you got ___ milk?                      | some / any / a             | any            | 1]
[MCQ    | I ___ eggs. (☹)                             | like / don't like / likes  | don't like     | 1]
[CLOZE  | I've got ___ bread but I haven't got ___ juice. |                        | some | any     | 2]
[CLOZE  | She can't ___ , but she can sing.  (drive) |                             | drive          | 1]
[CLOZE  | I like ___ . (cook, verb-ing)              |                             | cooking        | 1]
[MATCH  | apple↔mar; water↔apa; egg↔ou; chicken↔pui  |                             | apple-mar,water-apa,egg-ou,chicken-pui | 2]
[MATCH  | countable/uncountable: apple,water,egg,rice|                             | C:apple,egg / U:water,rice | 2]
[REORDER| don't / I / eggs / like / .                |                             | I don't like eggs. | 1]
[REORDER| cook / can / you / ?                        |                             | Can you cook?  | 1]
[REORDER| any / haven't / I / juice / got / .        |                             | I haven't got any juice. | 1]
[TRANSL | Imi place branza.                           |                             | I like cheese. | 2]
[TRANSL | Stiu sa gatesc.  (fara "to", fara "-s")     |                             | I can cook.    | 2]
[TRANSL | Ai (niste) apa?                             |                             | Have you got any water? | 2]
[CORRECT| Corecteaza: She cans to cook.               |                             | She can cook.  | 2]
```
*Total: 24 puncte.*

**Logica de scorare + prag:**
- MCQ/MATCH/REORDER/CLOZE: exact-match dupa normalizare (lowercase, trim, punctuatie/articol optional; „don't” = „do not”).
- TRANSL / CORRECT: acceptare cu variante echivalente (ex. „I like cheese” ✔; respinge „I like the cheese”, „I can to cook”, „She cans cook”). Half-credit daca sensul e corect dar apare o eroare pe structura-tinta (ex. „to” dupa can → -50%).
- **Prag de promovare: >=80%** (>=19,2 / 24), plus regula: **fara nicio eroare de tip „to” dupa can** in itemii TRANSL/CORRECT.

**Rubrica LLM pt productie (vorbire/scriere)** — vezi si sectiunea F:
- **Vocabular** (0-3): A1 = >=8 cuvinte-tinta corect folosite.
- **Gramatica-tinta** (0-3): like/don't like, some/any, can/can't corecte; descriptor A1 = max 2 erori minore, zero erori „to+can”.
- **Sarcina** (0-3): >=6 preferinte + some/any + >=2 can/can't.
- **Prag:** >=7/9 si gramatica-tinta >=2.

**MAPARE obiective ① → itemi:**

| Obiectiv ① (Stratul 1) | Itemi care il testeaza |
|---|---|
| ①.1 Numeste >=12 alimente/bauturi (>=80%) | MATCH (apple/water/egg/chicken), MATCH C/U, + criteriul „>=8 cuvinte-tinta” din rubrica productie |
| ①.2 Preferinte cu I like / I don't like (+noun/-ing), >=6 propoz. | MCQ „I ___ eggs”, CLOZE „I like cooking”, TRANSL „I like cheese”, REORDER „I don't like eggs”, rubrica F (>=6 preferinte) |
| ①.3 Countable/uncountable + some/any | MCQ „Have you got ___ milk”, CLOZE „some…any”, MATCH C/U, MCQ „a bread/bread”, TRANSL „Have you got any water?” |
| ①.4 can / can't (ability), fara „to”, fara „-s” | MCQ „She ___ swim”, CLOZE „can't drive”, REORDER „Can you cook?”, TRANSL „I can cook”, CORRECT „She cans to cook” |
| ①.5 Pronuntie /æ/–/e/ si /ɔː/ (>=4/6) | Sectiunea D: drill + scorare foneme (ASR), minimal pairs, shadowing |

---


I have the Stratul 1 content. Now I'll produce Straturile 2 & 3, coherent with the exact text, vocabulary, task ⑧, SRS bank ⑨, and objectives ①.

### A1-U12 — At the shop · Straturile 2 & 3 (Pipeline + Consolidare)

## STRATUL 2 — Pipeline (conversatie & voce cu EVA)

### A. Configuratia EVA (system prompt pt unitate)

```
ROL: Esti EVA, o tutore de engleza prietenoasa, calda si rabdatoare. Vorbesti cu un
adult VORBITOR DE ROMANA aflat la nivel A1 (incepator). In aceasta unitate joci si
rolul de VANZATOARE (shop assistant) intr-un magazin mic.

TEMA UNITATII (A1-U12 "At the shop"): cumparaturi simple, cererea politicoasa a unui
produs, intrebarea pretului, o mica tranzactie completa (salut → cerere → pret → plata
→ multumire).

NIVEL & GRAMATICA PERMISA: Doar A1, si DOAR gramatica introdusa pana la aceasta unitate.
Structuri-tinta de ELICITAT de la cursant:
  - "Can I have + (a/an/some/număr) + produs, please?"  (cerere politicoasa)
  - "How much is …?" (singular/necontabil) vs "How much are …?" (plural)
  - Formule de tranzactie: "Here you are.", "Anything else?", "That's … .", "Thank you.",
    "Goodbye."
Recapitulare integrata: a/an/the, plural -s/-es, numere 0–100, present simple
(I want, it costs). NU introduce timpuri noi, past simple, present continuous pt viitor,
conditionale sau vocabular in afara listei unitatii.

VOCABULAR-TINTA (foloseste-l pe acesta, nu sinonime avansate): shop, supermarket, market,
bakery, customer, apple, banana, orange, tomato, potato, bread, milk, water, coffee, tea,
juice, egg, cheese, rice, sugar, chocolate, cake, biscuit, chicken, bag, bottle, box,
newspaper, stamp, ticket, money, price, pound, pence, euro, cent, change, receipt, card,
cash, buy, pay, want, need, cost, kilo, litre, some, any, please, thank you, how much,
here you are, that's…, anything else, expensive, cheap. Preturi in POUNDS (lire/pence).

PROPORTIA RO/EN: ~70% engleza, ~30% romana. Vorbeste in propozitii SCURTE si simple.
Ofera sprijin in ROMANA (in paranteza) doar cand cursantul pare blocat, tace sau greseste
de doua ori. Ex.: "Can I help you? (Cu ce va pot ajuta?)". Nu traduce tot; lasa cursantul
sa ghiceasca din context.

CORECTARE PRIN RECAST (blanda, fara marcaj rosu, fara metalimbaj gramatical greu):
  - Nu spune niciodata "Gresit!". Reformuleaza corect, apoi continua conversatia.
  - Ex.: Cursant: "How much cost the apples?" → EVA: "Ah, how much ARE the apples? They're
    one pound fifty. 🙂" (auzi forma corecta, apoi mergi mai departe).
  - Ex.: Cursant: "I want apple." → EVA: "Sure — some apples? How many apples?"
  - Corecteaza MAXIM 1 lucru pe replica (prioritate: structura-tinta a unitatii). Ignora
    micile greseli care nu impiedica intelegerea.
  - Dupa recast, lauda scurt si concret: "Nice! 'Can I have' is perfect."

CE CERI CURSANTULUI: sa ceara cel putin 3 produse cu "Can I have…?", sa intrebe pretul la
cel putin 1 produs cu "How much is/are…?", sa incheie plata ("Here you are." → "Thank you.
Goodbye."). Pune UNA singura intrebare pe rand. Da timp de raspuns.

DACA CURSANTUL TACE: asteapta, apoi ofera un indiciu in romana + un model in engleza:
"Poti spune: 'Can I have some bread, please?'". Reia intrebarea.
DACA CURSANTUL GRESESTE: recast bland (vezi mai sus), nu intrerupe fluxul.
DACA CURSANTUL RASPUNDE IN ROMANA: accepta ideea, apoi ofera varianta engleza si invita-l
sa o repete: "In English: 'How much is the milk?' — try it! 🙂"

TON: cald, incurajator, cu emoji ocazional (🙂🛒). Propozitii scurte. Un singur pas o data.
```

### B. Fluxul conversatiei (3 etape)

**Etapa 1 — GHIDAT** (EVA conduce; cursantul completeaza cu structura fixa)

| # | EVA (replica de pornire) | Raspuns MODEL (cursant) | Structura de elicitat |
|---|---|---|---|
| 1 | Hello! Welcome to the shop. Can I help you? *(Cu ce va pot ajuta?)* | Hello. Can I have some apples, please? | `Can I have some + N, please?` |
| 2 | Of course! How many apples? | Four apples, please. | numar + plural |
| 3 | Here you are. Anything else? *(Altceva?)* | Yes. Can I have a bottle of water, please? | `Can I have a + N, please?` |
| 4 | Sure. How much is the water? Ask me! *(Intreaba-ma pretul.)* | How much is the water? | `How much is …?` (necontabil) |
| 5 | The water is ninety pence. And the apples? | How much are the apples? | `How much are …?` (plural) |
| 6 | The apples are two pounds. That's two pounds ninety. | Here you are. Thank you! | `Here you are.` + `Thank you.` |

*Structura de elicitat globala Etapa 1:* `Can I have…?` (×2), `How much is/are…?` (×2), formule `Here you are / Anything else / Thank you`.

**Etapa 2 — SEMI-GHIDAT** (intrebari deschise + indicii; cursantul alege produsele)

- EVA: "Today you have **£5**. What do you want to buy?" *(prompt: Can I have some… / a…)*
- EVA: "Good! Now **ask the price** of one thing." *(prompt: How much **is** the …? / How much **are** the …?)*
- EVA: "Do you want anything else? A drink? Bread?" *(prompt: Yes, can I have…? / No, thank you.)*
- EVA: "OK, that's **£4.20**. How do you pay — **cash or card**?" *(prompt: Cash, please. / Here you are.)*
- Indicii (prompts) daca ezita: *"Remember: is = 1 thing/milk-bread, are = many things."*, *"After 'Can I have', use a / some / a number."*

**Etapa 3 — LIBER** (rol-play complet, min. 8 replici)

- **Scenariu:** Cursantul e clientul; EVA e vanzatoarea. Are un buget de **£5**. Obiectiv: cumpara **>=3 produse**, intreaba pretul la **>=1 produs**, incheie plata cu formule (salut → cerere → pret → plata → multumire).
- **Obiectiv masurabil:** min. 8 replici, fara pauze mari; foloseste corect `Can I have…?` de >=3 ori si `How much is/are…?` corect (is vs are).

**Branching (ce face EVA):**
- *Cursantul TACE >6 sec* → indiciu RO + model EN: "Poti incepe cu: 'Can I have some bread, please?' 🙂". Daca tot tace → EVA propune un produs: "Do you want some apples?"
- *Greseste is/are* ("How much is the eggs?") → recast: "How much **are** the eggs? They're two pounds." (fara alta explicatie).
- *Foloseste 'cost' in intrebare* ("How much cost the milk?") → recast: "How much **is** the milk? It's one pound." + lauda scurta la finalul rundei.
- *Omite articolul* ("Can I have apple?") → recast: "Sure — **an** apple, or **some** apples?"
- *Depaseste bugetul* → EVA (in rol, natural): "That's £6 — a little too much for £5. Take away one thing?" *(gramatica ramane in limita)*.
- *Termina cu succes* → EVA lauda concret + rezuma: "Great shopping! You used 'Can I have' and 'How much are' perfectly. 🛒"

### C. Ascultare (script audio pt TTS + itemi)

**Script audio (dialog A1 ~40 sec; 2 voci — SHOP ASSISTANT calm, CUSTOMER clar):**

```
[SHOP ASSISTANT] Hello! Can I help you?
[CUSTOMER]       Hello. Can I have some bananas, please?
[SHOP ASSISTANT] Yes, of course. How many bananas?
[CUSTOMER]       Six, please. And a box of tea.
[SHOP ASSISTANT] Here you are. Anything else?
[CUSTOMER]       How much is the cheese?
[SHOP ASSISTANT] The cheese is two pounds fifty.
[CUSTOMER]       OK. Can I have some cheese, please. And how much are the eggs?
[SHOP ASSISTANT] The eggs are one pound thirty. So, that's five pounds.
[CUSTOMER]       Here you are.
[SHOP ASSISTANT] Thank you. Here's your change. Goodbye!
[CUSTOMER]       Thank you. Goodbye!
```

*Note TTS:* accent britanic, tempo lent, pauza scurta intre replici; accentueaza preturile (**two pounds fifty**, **one pound thirty**, **five pounds**) si /θ/ din *thank you, thirty*.

**Itemi de comprehensiune (4–5):**
1. What does the customer buy first? *(Ce cumpara clientul mai intai?)*
2. How many bananas does the customer want?
3. How much is the cheese?
4. How much are the eggs?
5. How does the customer pay — cash or card?

**Raspunsuri:** 1) (some) bananas — 2) six — 3) two pounds fifty (£2.50) — 4) one pound thirty (£1.30) — 5) cash (Here you are / not card).

### D. Pronuntie (drill + scorare)

**Sunete-tinta (focus romani):**
- **/θ/** (limba intre dinti, aer suflat — NU „t", NU „f"): *three, thirty, thirteen, thousand, thank you, anything, something.*
- **/aʊ/** (gura larg deschisa → rotunjita): *how, pound, about, now.* Atentie la **much = /mʌtʃ/** (nu „maci"; vocala /ʌ/ scurta).

**Minimal pairs (perechi):**
| Tinta /θ/ vs. capcana | Tinta /aʊ/ & /ʌ/ |
|---|---|
| **three** /θriː/ ≠ *tree* /triː/ | **how** /haʊ/ ≠ *who* /huː/ |
| **thirty** /ˈθɜːti/ ≠ *dirty* /ˈdɜːti/ | **pound** /paʊnd/ ≠ *pond* /pɒnd/ |
| **thank** /θæŋk/ ≠ *tank* /tæŋk/ | **much** /mʌtʃ/ ≠ *march* /mɑːtʃ/ |
| **thin** /θɪn/ ≠ *tin* /tɪn/ | **now** /naʊ/ ≠ *no* /nəʊ/ |

**Cuvinte de drill:** three, thirty, thirteen, thousand, thank you, how, how much, pound, pounds, about, now, much.

**Propozitii de drill (3–5):**
1. **How much** is the bread? *(/aʊ/ + /mʌ/)*
2. That's **three** pounds **thirty**. *(/θ/ ×2)*
3. **Thank** you — **thirteen** pence, please. *(/θ/ ×2)*
4. **How** many? **Thirty**? *(/aʊ/ + /θ/)*
5. It's a **thousand** euros — too **much**! *(/θ/ + /ʌ/)*

**Config de scorare:**
- Foneme evaluate: **/θ/** (word-initial: three, thirty, thank), **/aʊ/** (how, pound), **/ʌ/** (much).
- Prag: **inteligibilitate >=80%** pe cele 5 preturi/propozitii cu /θ/ si pe *How much*.
- Feedback tipic pt romani:
  - /θ/ realizat ca „t" → "Pune limba intre dinti si sufla usor: th-th-**three** (nu 'tree')."
  - /θ/ realizat ca „f" → "Nu 'free' — buza jos ramane liber, limba atinge dintii: **three**."
  - *much* pronuntat „maci" → "Vocala scurta /ʌ/, ca in 'cup': **much** = /mʌtʃ/."
  - /aʊ/ prea inchis („hau" scurt) → "Deschide gura mai mult: h-**ow**, p-**ou**-nd."

**Set de shadowing (repeta dupa audio, 3–5):**
1. How much is the milk?
2. How much are the apples?
3. That's three pounds fifty.
4. Thank you. Here's your change.
5. Anything else? — No, thank you.

## STRATUL 3 — Consolidare & evaluare

### E. Pachet SRS (carduri live)

| Front | Back | Tip | Nota |
|---|---|---|---|
| Can I help you? | Cu ce va pot ajuta? | EN→RO | formula vanzator |
| Can I have some bread, please? | Pot sa primesc niste paine, te rog? | EN→RO | cerere + some (necontabil) |
| How much is the milk? | Cat costa laptele? | EN→RO | is = necontabil |
| How much are the apples? | Cat costa merele? | EN→RO | are = plural |
| It's one pound thirty. | Costa o lira treizeci. | EN→RO | pret + /θ/ |
| That's three pounds. | Asta face trei lire. | EN→RO | total plata |
| Here you are. | Poftim. | EN→RO | cand dai ceva |
| Anything else? | Altceva? | EN→RO | oferta |
| No, thank you. | Nu, multumesc. | EN→RO | refuz politicos |
| Here's your change. | Poftim restul. | EN→RO | change = rest |
| I want two tickets, please. | Vreau doua bilete, te rog. | RO→EN | numar + plural |
| How many bananas? | Cate banane? | RO→EN | how many + plural |
| The bread is cheap. | Painea e ieftina. | RO→EN | cheap |
| The coffee is expensive. | Cafeaua e scumpa. | RO→EN | expensive |
| Thank you. Goodbye! | Multumesc. La revedere! | RO→EN | inchidere |
| Can I have ___ apple, please? → **an** | (articol corect inaintea vocalei) | cloze | a/an |
| How much ___ the eggs? → **are** | (acord is/are) | cloze | plural → are |
| How much ___ the water? → **is** | (acord is/are) | cloze | necontabil → is |
| Can I have ___ bread, please? → **some** | (necontabil) | cloze | some |
| That's five ___. → **pounds** | (plural moneda) | cloze | pound/pounds |

**Config FSRS (pe scurt):**
- **Tag-uri:** `A1-U12`, `shopping`, `can-i-have`, `how-much`, `is-vs-are`, `phonics-θ`, `transaction-formulas`.
- **Moment de introducere:** carduri EN→RO si formulele fixe la **finalul unitatii** (dupa task ⑧); cardurile **cloze** (is/are, a/an/some) se introduc **dupa** ce cursantul a trecut testul de gramatica (G, sect. B), pentru consolidare.
- **Prima repetare** la 1 zi; graduare FSRS standard. Cardurile ratate de 2× → re-marcheaza tema in urmatoarea sesiune de conversatie (recast in context).
- Carduri de pronuntie (three/thirty/how much) marcate `audio` — se testeaza prin shadowing, nu prin scriere.

### F. Scenariu task-based

**Situatia reala:** Esti la un magazin din Anglia cu **£5** in buzunar. EVA e vanzatoarea. Faci cumparaturile si platesti.

**Obiectiv:** Duci la capat o tranzactie completa: saluti, ceri **>=3 produse** cu *Can I have…?*, intrebi pretul la **>=1 produs** cu *How much is/are…?*, platesti si multumesti. Min. **8 replici**, in buget.

**Criterii de succes (masurabile):**
- >=3 cereri corecte cu `Can I have + (a/an/some/număr) + N, please?`
- >=1 intrebare de pret cu `is`/`are` ales corect.
- Inchidere completa: `Here you are.` → `Thank you.` → `Goodbye.`
- Ramane in buget (£5); min. 8 replici; fara pauze mari.

**Rubrica de scorare LLM (0–4 pe fiecare axa):**
| Axa | 4 (foarte bine A1) | 3 (bine) | 2 (partial) | 0–1 (insuficient) |
|---|---|---|---|---|
| **Task completion** | 3+ produse, pret intrebat, plata & multumire, in buget | mici omisiuni (ex. fara „goodbye") | doar 1–2 produse SAU fara pret | tranzactie neterminata |
| **Accuracy** | `Can I have…?` si `is/are` corecte peste tot | 1–2 alunecari auto-corectate | is/are gresit o data, articol lipsa | structura-tinta absenta/gresita repetat |
| **Fluency** | 8+ replici, ritm bun, fara pauze mari | mici ezitari | pauze dese, are nevoie de indicii | blocaje frecvente, majoritatea in RO |

**Prag task:** medie >=**2,7/4** SI Task completion >=3.

**Variante:**
- **A (usor):** lista de cumparaturi data (2 fructe + 1 bautura); EVA ofera preturile.
- **B (standard):** buget £5, cursantul alege liber.
- **C (provocare):** EVA nu are un produs ("Sorry, no oranges today.") → cursantul cere altceva; sau da rest gresit si cursantul spune "How much is the change?".

### G. Evaluare automata (test de unitate)

**Itemi structurati** `[tip | intrebare | (optiuni) | raspuns_corect | puncte]`

```
[MCQ    | Can I ___ a newspaper, please? | have / to have / having | have | 1]
[MCQ    | That's three ___.              | pound / pounds / pounded | pounds | 1]
[MCQ    | ___ you are.                   | Her / Here / Hear | Here | 1]
[CLOZE  | How much ___ the apples?       |  | are | 1]
[CLOZE  | How much ___ the water?        |  | is | 1]
[CLOZE  | How much ___ the eggs?         |  | are | 1]
[CLOZE  | Can I have ___ apple, please?  |  | an | 1]
[CLOZE  | Can I have ___ bread, please?  |  | some | 1]
[CLOZE  | How ___ apples do you want?    | (much/many) | many | 1]
[MATCH  | 1.How much is the milk? 2.Anything else? 3.Can I help you? | a.No,thank you. b.Yes,can I have some bread? c.It's one pound. | 1-c,2-a,3-b | 3]
[REORDER| have / I / can / some / apples / ? |  | Can I have some apples? | 1]
[REORDER| are / how much / the / oranges / ? |  | How much are the oranges? | 1]
[TRANS  | Pot sa primesc niste paine, te rog? |  | Can I have some bread, please? | 1]
[TRANS  | Cat costa merele?              |  | How much are the apples? | 1]
[TRANS  | Poftim. (cand dai ceva)        |  | Here you are. | 1]
[TRANS  | Altceva?                       |  | Anything else? | 1]
[VOCAB  | Tradu RO→EN: pret / bani / rest / magazin / ieftin |  | price / money / change / shop / cheap | 5]
```

**Logica de scorare:**
- MCQ / CLOZE / REORDER / TRANS / VOCAB(per cuvant): comparare case-insensitive, ignora spatii duble si punctuatia finala; `some/any` si `a/an` verificate strict (sunt tinta). La TRANS accepta variante echivalente A1 (ex. cu/fara „please" pentru itemul „Poftim").
- MATCH: 1p per pereche corecta.
- **Total = 22 puncte** (16 itemi de 1p + MATCH 3p + VOCAB 5p − recalcul: 12×1 + 3 + 5 = 20; plus 2 cloze suplimentare = **22**). **Prag de promovare: >=80% (>=18/22).**

**Pt productie (vorbire/scriere) — rubrica LLM:**
| Criteriu | Descriptor A1 „trece" (>=2/3) |
|---|---|
| **Task completion** | cere 3+ produse, intreaba 1 pret, incheie plata |
| **Accuracy** | `Can I have…?` corect; `is/are` corect in >=80% din cazuri; articol a/an/some in general corect |
| **Fluency** | raspunsuri prompte, 8+ replici, foloseste formulele fixe |
| **Pronuntie** | /θ/ si *How much* inteligibile >=80% la 5 preturi |

**Prag productie:** medie >=**2/3** pe cele 4 criterii, cu Task completion >=2.

**MAPARE obiective ① → itemi de test:**
| Obiectiv ① | Item(i) care il testeaza |
|---|---|
| Cere politicos un produs (*Can I have…, please?*, >=3/4) | MCQ „Can I ___" ; CLOZE „an/some" ; REORDER „Can I have some apples?" ; TRANS „niste paine" ; rubrica productie (Task completion) |
| Intreaba pretul (*How much is/are*, is vs are, 4/5) | CLOZE is/are (×3) ; REORDER „How much are the oranges?" ; TRANS „Cat costa merele?" ; MCQ „much/many" |
| Duce la capat o tranzactie (8+ replici) | Scenariu F + rubrica LLM productie (Task completion / Fluency) |
| Foloseste formulele de tranzactie (*Here you are / Anything else / That's…*, >=3) | MCQ „Here you are" ; MATCH (Anything else / Can I help you) ; TRANS „Poftim" & „Altceva?" |
| Pronunta inteligibil preturile /θ/ + *How much* /aʊ/ (>=80%) | Sect. D scorare pronuntie (drill + shadowing) ; rubrica productie (Pronuntie) |

---


## Testele de nivel A1 (Checkpoints + Test final)

> **Scop și principii.** Testele măsoară doar structuri **A1 introduse până la punctul de testare** (control de nivel strict). Corectarea în feedback rămâne prin **recast** (reformulare blândă), dar în teste itemii sunt punctați binar/obiectiv pentru măsurabilitate. Instrucțiunile de test sunt în **română** (sprijin A1); itemii sunt în engleză. Fiecare checkpoint = un „gate" formativ (nu blochează progresul, dar declanșează remediere dacă e sub prag). Testul final = **sumativ**, cu 6 porți conjunctive (TOATE trebuie trecute) pentru promovare la A2.
>
> **Legendă competențe:** G = gramatică/structură · V = vocabular · F = funcție comunicativă · R = citire · L = ascultare · S = vorbire · P = pronunție.

---

### CHECKPOINT 1 — după U4

**Scope:** U1 Hello&Goodbye · U2 to be · U3 a/an/the · U4 this/that + plural.
**Format:** 14 itemi scriși (12 min) + 1 sarcină orală cu EVA (2–3 min).
**Prag scris:** ≥ **11/14 (≥ 78%)**. **Prag vocabular SRS cumulat (U1–U4, ~200 carduri):** ≥ **160 „știute" (80%)**.

**A. Greetings & functions (U1) — 3p**
1. Complete: „__ morning, Eva!" → **Good**
2. Match: cineva pleacă seara → alegi: (a) Good morning (b) **Goodbye / Good night** (c) Hello. → **(b)**
3. Reply to „How are you?" (o variantă corectă A1) → **„I'm fine, thank you." / „Fine, thanks."**

**B. Verb *to be* (U2) — 4p**
4. „I __ Ana." → **am**
5. „She __ from Romania." → **is**
6. „We __ students." → **are**
7. Negativ: „He is not a teacher." → forma scurtă → **He isn't a teacher.**

**C. Articles a/an/the (U3) — 4p**
8. „__ apple" → **an**
9. „__ dog" → **a**
10. „__ hour" → **an** (h mut)
11. „Look at __ sun." (unic) → **the**

**D. this/that + plural (U4) — 3p**
12. „__ is my book (aici, lângă mine)." → **This**
13. Plural: „one box → two __" → **boxes**
14. „__ are my friends (departe)." → **Those**

**Sarcină orală cu EVA (S):** Joc de rol „Prima întâlnire". EVA salută, întreabă numele, țara și dacă e student. Elevul trebuie să producă **min. 4 replici**.
**Criteriu de trecere oral:** ≥ **3/4** replici corecte funcțional + folosește corect `to be` în ≥ 2 replici (auto-scor EVA + tabel de bife). Sub prag → 1 mini-lecție de remediere pe structura ratată.

---

### CHECKPOINT 2 — după U7

**Scope nou:** U5 have got + familie · U6 numere/vârstă · U7 ora + prepoziții de timp (at/in/on). **Reactivare (spiral):** `to be`, plural (U2, U4).
**Format:** 15 itemi (14 min) + 1 sarcină orală cu EVA (3 min).
**Prag scris:** ≥ **12/15 (≥ 80%)**. **SRS cumulat (U1–U7, ~350 carduri):** ≥ **280 „știute" (80%)**.

**A. have got + familie (U5) — 5p**
1. „I __ a sister." → **have got / 've got**
2. „She __ two brothers." → **has got / 's got**
3. Negativ: „We haven't got a car." (scrie forma din „We have not got…") → **haven't got**
4. Întrebare: „__ you got a dog?" → **Have**
5. Vocabular familie: „my mother's mother is my __" → **grandmother**

**B. Numere & vârstă (U6) — 5p**
6. Scrie în litere: „13" → **thirteen**
7. „30" → **thirty**
8. „How old are you?" → răspuns model → **„I'm ___ (years old)."** (orice număr corect gramatical)
9. Corectează: „She have 8 years." → **She is 8 (years old).** (vârsta cu *be*, nu *have*)
10. „21" → **twenty-one**

**C. Ora + prepoziții de timp (U7) — 5p**
11. „7:00" → **It's seven o'clock.**
12. „7:30" → **It's half past seven.**
13. „__ Monday" → **on**
14. „__ the morning" → **in**
15. „__ 8 o'clock" → **at**

**Sarcină orală cu EVA (S):** „Familia mea + programul meu." EVA întreabă câți frați/surori are, vârsta lor și la ce oră se trezește. **Min. 5 replici.**
**Criteriu oral:** ≥ **4/5** corecte funcțional; `have got` corect ≥ 2×; o oră + o prepoziție de timp corecte. Sub prag → remediere țintită (have got SAU ora).

---

### CHECKPOINT 3 — după U10

**Scope nou:** U8 present simple I/you/we + rutină · U9 pers. a III-a + întrebări WH · U10 there is/are + casă. **Reactivare:** ora/prepoziții (U7), have got (U5).
**Format:** 15 itemi (16 min) + 1 sarcină orală cu EVA (4 min).
**Prag scris:** ≥ **12/15 (≥ 80%)**. **SRS cumulat (U1–U10, ~500 carduri):** ≥ **400 „știute" (80%)**.

**A. Present simple I/you/we (U8) — 4p**
1. „I __ (get up) at 7." → **get up**
2. „We __ (not / watch) TV." → **don't watch**
3. „__ you __ (like) coffee?" → **Do … like**
4. Ordonează: „every / I / breakfast / have / day" → **I have breakfast every day.**

**B. Pers. a III-a + WH (U9) — 6p**
5. „He __ (work) in Cluj." → **works**
6. „She __ (go) to school." → **goes**
7. Negativ: „He __ (not / play) football." → **doesn't play**
8. „__ does she live?" (loc) → **Where**
9. „__ time do you start?" → **What**
10. „__ is your teacher?" (persoană) → **Who**

**C. there is / there are + casă (U10) — 5p**
11. „__ a sofa in the living room." → **There is / There's**
12. „__ two windows in the kitchen." → **There are**
13. Negativ: „There __ any chairs." → **aren't**
14. Întrebare: „__ there a bathroom?" → **Is**
15. Vocabular casă: alege intrusul: bedroom / kitchen / **banana** / bathroom → **banana**

**Sarcină orală cu EVA (S):** „Casa mea + rutina zilnică." EVA cere descrierea a 2 camere (there is/are) și 3 acțiuni de rutină; pune 2 întrebări WH. **Min. 6 replici.**
**Criteriu oral:** ≥ **5/6** corecte funcțional; `there is/are` corect ≥ 2×; present simple corect ≥ 3×; răspunde corect la ≥ 1 întrebare WH. Sub prag → remediere pe pers. a III-a `-s` SAU there is/are.

---

## TEST FINAL A1 (promovare la A2)

Testul final are **6 stații** care corespund 1:1 celor 6 criterii de ieșire. Toate stațiile trebuie trecute (**decizie conjunctivă**).

### 1) Blueprint de acoperire — Stația Scris/Gramatică (Criteriul 1, ~60 itemi, prag ≥ 80% = ≥ 48/60)

Matrice **unitate × competență** (fiecare item = 1p):

| Unitate | G | V | F | R | **Total** |
|---|---|---|---|---|---|
| U1 Hello&Goodbye | 1 | 1 | 2 | – | **4** |
| U2 to be | 4 | 1 | 1 | – | **6** |
| U3 a/an/the | 4 | 1 | – | – | **5** |
| U4 this/that + plural | 4 | 1 | – | – | **5** |
| U5 have got + familie | 3 | 2 | – | – | **5** |
| U6 numere/vârstă | 3 | 2 | – | – | **5** |
| U7 ora/prepoziții | 3 | 1 | 1 | – | **5** |
| U8 present simple I/you/we | 4 | 1 | 1 | – | **6** |
| U9 pers. III + WH | 5 | – | 1 | – | **6** |
| U10 there is/are + casă | 3 | 2 | – | – | **5** |
| U11 like + mâncare + some/any | 3 | 2 | – | – | **5** |
| U12 cumpărături (recap) | – | 1 | 2 | – | **3** |
| **Reading integrat (U8–U12)** | – | – | – | **4** | **4** |
| **TOTAL** | **37** | **15** | **8** | **4** | **60** |

Distribuție pe competențe: **Gramatică 37 (62%) · Vocabular 15 (25%) · Funcție 8 (13%) · Citire 4** (reading e integrat, textul folosește doar structuri A1). Toate cele 12 unități sunt reprezentate cu ≥ 3 itemi → nicio unitate nu poate fi „sărită".

### 2) Eșantion reprezentativ — 20 itemi cu răspunsuri

*(gap-fill, transformare, alegere, reordonare, corectare-recast)*

**U1–U2 (to be / funcții)**
1. „Hello! __ name is Tom." → **My**
2. „They __ from Spain." → **are**
3. „She isn't a doctor." → întrebare da/nu → **Is she a doctor?**

**U3–U4 (articole / this-that-plural)**
4. „I want __ orange and __ banana." → **an / a**
5. „one child → three __" → **children**
6. „__ shoes over there are new." → **Those**

**U5–U6 (have got / numere-vârstă)**
7. „My grandfather __ a big garden." → **has got / 's got**
8. „Corectează: My brother has 15 years." → **My brother is 15 (years old).**
9. „40 + 2 in words" → **forty-two**

**U7 (ora / prepoziții)**
10. „9:15" → **It's (a) quarter past nine.**
11. „I go to bed __ 10 o'clock __ night." → **at / at**

**U8–U9 (present simple + WH)**
12. „My sister __ (study) English." → **studies**
13. „__ (not) he like tea? / He __ like tea." (negativ) → **He doesn't like tea.**
14. „__ do you go to work? — By bus." → **How**
15. „Ordonează: does / where / live / she / ?" → **Where does she live?**

**U10 (there is/are)**
16. „__ three bedrooms in my house." → **There are**
17. „Is there a garden? — No, there __." → **isn't**

**U11 (like + some/any)**
18. „I'd like __ water, please." → **some**
19. „Have we got __ apples?" → **any**

**U12 (cumpărături — funcție/recap)**
20. Alege replica potrivită într-un magazin, la „How much is it?": (a) I'm fine (b) **It's five pounds** (c) You're welcome → **(b)**

**Barem eșantion:** 20p; extrapolat la testul complet, prag identic 80%.

### 3) Rubrică de VORBIRE — Stația S (Criteriul 3) + PRONUNȚIE (Criteriul 4)

**Sarcină:** dialog de rutină cu EVA, **min. 10 replici** ale elevului (subiecte combinate: salut → prezentare → familie → oră/rutină → casă → mâncare/cumpărături). EVA conduce scenariul și scorează live.

**Rubrică vorbire (acuratețe structuri A1), prag ≥ 75%:**

| Dimensiune (0–3 fiecare) | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **Acuratețe gramaticală** (to be, have got, present simple, there is/are) | multe erori, blochează sensul | erori frecvente | erori ocazionale, sens clar | corect constant |
| **Îndeplinire task / relevanță** | nu răspunde la temă | parțial | răspunde la majoritatea | răspunde complet la toate |
| **Vocabular A1** | insuficient | limitat | adecvat | bogat pt. A1 |
| **Fluență / interacțiune** | tăceri lungi, nu susține | dependent de sprijin | susține cu ezitări | schimburi naturale A1 |

**Scor vorbire = itemi corecți structural / total structuri țintă.** Prag: **≥ 75% acuratețe pe structurile A1** ȘI ≥ 8/12 puncte de rubrică, ȘI dialog ≥ 10 replici duse la capăt.

**Rubrică pronunție (Criteriul 4), prag compus:**
- **Producție /θ ð/ și /w v/:** scor ≥ **80/100** (EVA punctează pe listă de cuvinte-țintă: *three, this, mother · water, very, west, van*). Formula: (cuvinte pronunțate acceptabil ÷ total țintă) × 100.
- **Discriminare auditivă minimal pairs:** /iː ɪ/ (*sheep–ship, seat–sit*) și /æ e/ (*cat–bed style: man–men, bad–bed*) ≥ **75%** răspunsuri corecte (min. 8 perechi × 2 = 16 itemi, prag ≥ 12).

### 4) Rubrică de SCRIERE (parte din Criteriul 1, verificare productivă)

**Sarcină:** elevul scrie **un mesaj scurt de 40–50 cuvinte** (prezentare + familie + rutină + camera preferată). Evaluat separat de gap-fill.

| Dimensiune (0–2) | Descriptor A1 |
|---|---|
| Sarcină acoperită | atinge cele 4 sub-teme cerute |
| Corectitudine A1 | to be / present simple / there is-are folosite corect majoritar |
| Ortografie & majuscule | cuvinte A1 scrise corect, propoziții cu punctuație de bază |
| Coeziune | folosește *and / but*, ordine SVO corectă |

**Prag scriere:** ≥ **6/8** (≥ 75%). (Scrierea productivă nu se contorizează în cele 60 de gap-fill, dar este o poartă calitativă în interiorul Criteriului 1.)

### 5) Stația ASCULTARE (Criteriul 5), prag ≥ 80%

3 dialoguri scurte, lente (10–12 replici total), pe teme A1 (prezentare, oră/programare, cumpărături). **10 itemi de comprehensiune** (alegere/completare). Prag: **≥ 8/10 (80%)**.

### 6) Stația VOCABULAR / SRS (Criteriul 2), prag ≥ 80%

Măsurat pe cardurile SRS live: din **~600 cuvinte**, elevul are ≥ **480 carduri în starea „known"** (interval ≥ 1 zi, ≥ 2 recall-uri corecte consecutive). Verificare de test: **eșantion aleator de 40 carduri**, prag ≥ 32/40 pentru a confirma acoperirea (evită „inflația" SRS).

---

### Logica de scorare cumulativă și maparea pe criteriile de ieșire

Fiecare stație produce un scor normalizat 0–100. **Promovarea la A2 = ȘI logic (conjunctiv) pe toate cele 6 porți** — nicio compensare între stații.

| # | Criteriu de ieșire A1 | Stație de test | Măsură | Prag (poartă) |
|---|---|---|---|---|
| 1 | Scris/gramatică integrat | Blueprint 60 itemi + scriere 40–50 cuv. | % corect + rubrică scriere | **≥ 48/60 (80%)** ȘI scriere ≥ 6/8 |
| 2 | Vocabular ~600 cuvinte | SRS + eșantion 40 carduri | carduri „known" / verificare | **≥ 480/600** ȘI ≥ 32/40 |
| 3 | Vorbire task rutină | Dialog live EVA ≥ 10 replici | % acuratețe structuri A1 + rubrică | **≥ 75%** ȘI rubrică ≥ 8/12 |
| 4 | Pronunție | Producție + discriminare | scor /θ ð/,/w v/ + minimal pairs | **≥ 80/100** ȘI discriminare ≥ 75% |
| 5 | Ascultare | 3 dialoguri lente | 10 itemi | **≥ 8/10 (80%)** |
| 6 | Descriptor CEFR A1 | Confirmare holistică | checklist „can-do" A1 | **toate 6 can-do** bifate |

**Checklist CEFR A1 (Criteriul 6) — toate bifate:** (a) se prezintă și salută; (b) pune/răspunde întrebări simple despre familie și vârstă; (c) spune ora și programul; (d) descrie camera/casa cu there is/are; (e) exprimă preferințe de mâncare și face o cumpărătură simplă; (f) înțelege întrebări lente, directe.

**Decizie de promovare (algoritm):**
```
if (C1 și C2 și C3 și C4 și C5 și C6 toate ≥ prag):
    → PROMOVAT la A2 (certificat A1 emis)
elif (5 din 6 trecute, unul între 70–79% din prag):
    → "Aproape" — remediere țintită pe stația ratată + reexaminare doar acea stație (max. 2 reîncercări)
else:
    → NEPROMOVAT — plan de recuperare pe unitățile cu itemi < 60%, reia checkpoint-ul relevant, reprogramează test final complet
```

**Scor compozit informativ (doar raportare, NU decide):** media aritmetică a celor 6 scoruri normalizate → afișat elevului ca „profil A1" (radar cu 6 axe), pentru a arăta punctele forte/slabe. Decizia rămâne pe porțile conjunctive, nu pe medie (evită mascarea unei competențe slabe printr-una puternică).
