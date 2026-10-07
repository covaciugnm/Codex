# 🏛️ EVA — Arhitectura curriculară
### Documentul programatic pentru componenta scrisă a cursului (A1–C2)

**Produs:** EVA — *English Voice Assistant*. Aplicație **chat-first** (stil WhatsApp / Messenger): vorbești și scrii cu EVA ca într-o conversație de mesagerie, iar EVA te învață engleza pornind de la limba română.

**Ce este acest document.** Este *materialul-șablon* (blueprint) pe baza căruia se scrie, pas cu pas, întreg curriculumul. Definește: (1) cadrul celor 6 niveluri CEFR, (2) testele de validare/plasare, (3) **șablonul reutilizabil de unitate** cu obiective–activități–conținut–rezultate *măsurabile*, (4) cuprinsul propus pe niveluri, (5) procesul de autorare. Aplicat pe cuprins, produce **componenta scrisă a proiectului**.

**Cum se citește.** Partea I (acest capitol) = cadrul + șablonul + un exemplu complet lucrat. Partea a II-a = testele de validare. Partea a III-a = cuprinsul (syllabus) pe fiecare nivel. Partea a IV-a = procesul de autorare (cum aplicăm șablonul).

---

## 1. Principii de proiectare curriculară

1. **Aliniere CEFR verificabilă.** Fiecare obiectiv se formulează ca descriptor **CAN-DO** (Poate face…) din scara globală CEFR (pe care British Council o reproduce) și are un **criteriu măsurabil** de îndeplinire.
2. **Conversația e coloana vertebrală.** Fiecare unitate culminează într-o conversație reală cu EVA. Gramatica și vocabularul servesc vorbirii, nu invers.
3. **Sprijinul în română se stinge treptat.** A1–A2: explicații și traduceri în română. B1–B2: română doar la nevoie. C1–C2: aproape integral engleză.
4. **Progresie în spirală.** Fiecare nivel reia și extinde structurile anterioare în contexte noi (nu „predă o dată și uită").
5. **Măsurabil la fiecare pas.** Nimic nu intră în curriculum fără un rezultat observabil și cuantificat (prag %, scor, număr de producții corecte, descriptor CEFR atins).
6. **Fundamentat pe biblioteca EVA.** Textele, dialogurile, audio-ul și cele ~16.000 de propoziții RO-EN alimentează unitățile (vezi maparea per nivel în Partea a III-a).

---

## 2. Cadrul celor 6 niveluri (CEFR A1–C2)

Nivelurile sunt numerotate **1–6**. Testul de validare se aplică nivelurilor **2–6** (A2–C2); nivelul **1 (A1)** are intrare directă.

| # | Nivel | Descriptor global (CAN-DO) | Vocabular activ (cumulat) | Domeniu gramatical |
|---|---|---|---|---|
| 1 | **A1** *Beginner* | Înțelege și folosește expresii uzuale foarte simple pentru nevoi concrete. Se prezintă, pune și răspunde la întrebări elementare despre sine. | 500–1.000 | to be, present simple, articole, plural, can, have got, prepoziții de bază, întrebări WH |
| 2 | **A2** *Elementary* | Înțelege propoziții și expresii frecvente (informații personale, familie, cumpărături, muncă). Comunică în sarcini simple, de rutină. | 1.500–2.500 | past simple, present continuous, comparativ, going to, countable/uncountable |
| 3 | **B1** *Intermediate* | Se descurcă în majoritatea situațiilor de călătorie. Povestește întâmplări, vise, speranțe; își justifică opiniile. | 2.750–3.250 | present perfect, past continuous, first conditional, modale, relative clauses, phrasal verbs (intro) |
| 4 | **B2** *Upper-Intermediate* | Înțelege ideile principale din texte complexe. Se exprimă fluent și spontan cu un nativ, fără efort major; argumentează. | 4.000–5.000 | perfect continuous, conditionale 2/3, pasiv, mixed conditionals, discurs |
| 5 | **C1** *Advanced* | Înțelege o gamă largă de texte lungi și pretențioase. Se exprimă fluent, fin, fără să caute cuvintele; folosește limba flexibil. | 6.000–8.000 | inversiune, cleft sentences, condiționale avansate, colocații, idiomuri, registru |
| 6 | **C2** *Proficiency* | Înțelege fără efort tot ce citește/aude. Se exprimă foarte precis, nuanțat și natural, la nivelul unui nativ educat. | 8.000–16.000+ | stăpânire cvasi-nativă, stilistică, conotație, idiomatic complet |

**Descriptori pe competențe** (formatul în care se scriu obiectivele — exemplu A1/B1/C1, aplicat identic la toate nivelurile):

| Competență | A1 | B1 | C1 |
|---|---|---|---|
| 🎧 Ascultare | Recunoaște cuvinte/expresii de bază despre sine și familie, rostite rar și clar. | Înțelege ideile principale dintr-un discurs standard clar pe teme familiare. | Înțelege discurs lung chiar nestructurat, cu relații implicite. |
| 📖 Citire | Înțelege nume, cuvinte, propoziții foarte simple (afișe, cataloage). | Înțelege texte cu limbaj cotidian sau legat de muncă. | Înțelege texte lungi, complexe, literare și de specialitate. |
| 💬 Interacțiune orală | Interacționează simplu dacă interlocutorul repetă/reformulează rar. | Se descurcă în majoritatea situațiilor de călătorie; intră nepregătit în conversație. | Se exprimă fluent și spontan, fără căutări evidente ale cuvintelor. |
| 🗣️ Producție orală | Descrie cu expresii simple locul unde trăiește și oameni cunoscuți. | Leagă expresii pentru a povesti experiențe, vise, speranțe, planuri. | Prezintă descrieri clare, detaliate, pe subiecte complexe. |
| ✍️ Scriere | Scrie o carte poștală scurtă, completează formulare cu date personale. | Scrie un text simplu, coerent, pe teme familiare; scrisori personale. | Scrie texte clare, bine structurate, pe subiecte complexe. |

*(Toate descriptorele sunt formulate CAN-DO și primesc, în unități, un criteriu de măsurare — vezi §5.)*

---

## 3. Structura arhitecturală: Nivel → Modul → Unitate

```
CURS EVA (A1 … C2)
└─ NIVEL  (ex. A2)
   ├─ Test de validare la intrare   (A2–C2; A1 = intrare directă)
   ├─ MODUL 1  ── Unitate 1 … Unitate 4   → Checkpoint M1
   ├─ MODUL 2  ── Unitate 5 … Unitate 8   → Checkpoint M2
   ├─ MODUL 3  ── Unitate 9 … Unitate 12  → Checkpoint M3
   └─ Test final de nivel  → deblochează nivelul următor
```

- **Nivel** = 10–12 **Unități** grupate în 2–3 **Module**.
- **Codificare:** `A2-U05` (nivel-unitate), `A2-M2` (modul), `A2-TF` (test final).
- **Checkpoint** după fiecare modul (test scurt de progres, criteriu ≥80%).
- **Test final de nivel** = condiție de promovare (vezi Partea a II-a).

### Fluxul fiecărei unități — 3 faze (ordinea de autorare cerută)
> **întâi partea scrisă → apoi pipeline-ul → apoi tot restul.**

| Fază | Denumire | Ce conține | Livrabil scris |
|---|---|---|---|
| **1** | **Partea scrisă** *(input & studiu)* | Text/dialog de citit · explicație de gramatică în română (care se stinge) · prezentare vocabular · exerciții scrise · verificare de înțelegere | Textul unității, notele de gramatică, lista de vocabular, exercițiile |
| **2** | **Pipeline** *(conversație & voce cu EVA)* | Ascultare · conversație ghidată → liberă cu EVA pe temă · focus de pronunție RO-specific (th, v/w, i:/ɪ, æ/e, accent) · shadowing | Scriptul de conversație, prompt-ul EVA pe unitate, drill-urile de pronunție |
| **3** | **Consolidare & evaluare** *(restul)* | Carduri SRS (din vocabularul/propozițiile unității) · scenariu task-based din viața reală · auto-verificare · **test de unitate** | Setul SRS, scenariul, itemii de test + baremul |

**Această ordine se aplică și la nivel de proiect:** întâi producem **componenta scrisă** (Faza 1 a tuturor unităților), apoi stratul pipeline (Faza 2), apoi restul (Faza 3). Acesta e sensul lui „la final obținem componenta scrisă a proiectului".

---

## 4. Șablonul reutilizabil de unitate (blueprint)

Fiecare unitate din cuprins se dezvoltă completând EXACT aceste 7 secțiuni. Totul **măsurabil**.

> ### `<COD>` — <Titlu unitate> · Temă: <temă>
> **Nivel/sub-nivel CEFR:** <A2.1 etc.> · **Durată estimată:** <min> · **Prerechizite:** <unități anterioare>
>
> **① OBIECTIVE (CAN-DO, măsurabile)** — 3–5 obiective, fiecare cu criteriu:
> - *„La final, cursantul poate <can-do CEFR>"* → **Criteriu:** <observabil + prag> (ex. „poate cere prețul unui produs" → produce ≥3 întrebări corecte cu *How much…?* în conversația cu EVA).
>
> **② CONȚINUT LINGVISTIC**
> - **Gramatică:** <puncte>
> - **Vocabular:** <temă> — **țintă: N cuvinte** (listate)
> - **Funcții comunicative:** <acte de vorbire>
> - **Fonetică (focus RO):** <sunete-țintă> + cuvinte-exemplu
>
> **③ ACTIVITĂȚI** (pe cele 3 faze, mapate la competențe L/R/S/W)
> - *Faza 1 (scris):* <text de citit, exerciții…>
> - *Faza 2 (pipeline):* <ascultare, conversație EVA, pronunție…>
> - *Faza 3 (rest):* <SRS, scenariu, test…>
>
> **④ RESURSE din biblioteca EVA** — <manual/pagini, propoziții Tatoeba filtrate, fișiere audio, intrări dicționar>
>
> **⑤ REZULTATE MĂSURABILE (Definition of Done)** — pragurile de promovare a unității:
> - Înțelegere: ≥ <%> la itemii de comprehensiune
> - Producție: ≥ <N> producții corecte (scris + oral, rubrică)
> - Pronunție: scor ≥ <%> pe cuvintele-țintă (evaluare pe fonem)
> - Vocabular: ≥ <%> reținut la SRS (verificare la 24h/7 zile)
> - Descriptor CEFR: <care> — bifat prin sarcina finală
>
> **⑥ EVALUARE** — tip itemi (MCQ, completare, ordonare, traducere RO→EN, sarcină de vorbire cu EVA) + **barem**.
>
> **⑦ SARCINA COMUNICATIVĂ FINALĂ** (task) — o situație reală rezolvată în conversație cu EVA, care „demonstrează" obiectivele.

---

## 5. Cadrul de măsurare (cum cuantificăm totul)

Fiecare obiectiv → un **criteriu observabil** + o **metodă de evaluare** + un **prag**. Instrumentele:

| Dimensiune | Instrument de măsurare | Metric / prag tipic |
|---|---|---|
| Înțelegere (ascultare/citire) | itemi MCQ / adevărat-fals / potrivire | ≥ 80% corect |
| Producție scrisă | rubrică CEFR (range, accuracy, coherence) scorată de LLM | nivel-țintă atins pe rubrică |
| Producție orală (cu EVA) | rubrică CEFR (fluency, accuracy, interaction) + nr. schimburi reușite | ≥ nivel-țintă; ≥ N ture de dialog |
| Pronunție | evaluare pe fonem (Azure Pronunciation) pe cuvinte-țintă RO | scor ≥ 80 |
| Vocabular / retenție | SRS (FSRS) — verificare la 1 zi și 7 zile | retenție ≥ 85% la 7 zile |
| Progres de nivel | checkpoint de modul + test final | ≥ 80% checkpoint; test final promovat |

**Descriptor → criteriu (exemplu de transformare):**
- CAN-DO A2: *„Poate face cumpărături simple, cerând informații despre produse și prețuri."*
- **Criteriu măsurabil:** în scenariul „la magazin" cu EVA, cursantul (a) cere prețul cu *How much is/are…?* corect ≥3 ori, (b) înțelege 4/5 răspunsuri de preț, (c) scor pronunție ≥80 pe numere. **Îndeplinit = descriptor bifat.**

---

## 6. Exemplu complet lucrat (șablonul aplicat) — unitate demonstrativă

*Acesta arată cum se transformă o intrare din cuprins în componentă scrisă. Fiecare unitate se autorează la fel.*

> **Notă de reconciliere:** exemplul de mai jos este **ilustrativ** și combină, pentru demonstrație, temele din primele două unități ale cuprinsului finalizat A1 (Partea a III-a): `A1-U1` **Hello & Goodbye** (salut, alfabet, spelling) și `A1-U2` **Who are you?** (prezentare, țări, verbul *to be*). Când producem componenta scrisă, fiecare dintre aceste unități se dezvoltă separat, cu același șablon.

> ### `A1-U1` — **Hello! Who are you?** · Temă: Salut și prezentare personală
> **Nivel:** A1.1 · **Durată:** ~25 min · **Prerechizite:** niciuna (unitate de start)
>
> **① OBIECTIVE (CAN-DO, măsurabile)**
> 1. *Poate saluta și își poate lua rămas-bun formal/informal* → **Criteriu:** folosește corect ≥4 formule (*hello, hi, good morning, bye, see you*) în dialogul cu EVA.
> 2. *Se poate prezenta (nume, țară, naționalitate)* → **Criteriu:** produce 3 propoziții corecte cu *to be*: „I am… / I'm from… / I'm Romanian".
> 3. *Poate cere și da informații personale de bază* → **Criteriu:** pune și răspunde corect la „What's your name? / Where are you from?" (≥4 schimburi).
> 4. *Poate număra 0–10* → **Criteriu:** identifică și rostește 8/10 numere; scor pronunție ≥80.
>
> **② CONȚINUT LINGVISTIC**
> - **Gramatică:** verbul *to be* (am/is/are) — afirmativ + întrebare; pronume personale (I, you, he, she, it); articolul *a/an* (introducere contrastivă cu româna — *„I am **a** student"*, nu *„I am student"*).
> - **Vocabular (țintă ~15 cuvinte):** hello, hi, good morning/afternoon/evening, goodbye, bye, name, from, country, Romanian, England, numbers 0–10.
> - **Funcții:** a saluta, a te prezenta, a întreba numele/originea, a-ți lua rămas-bun.
> - **Fonetică (focus RO):** sunetul **/w/** în *what / where* (≠ /v/ românesc); diftongul **/eɪ/** în *name*; accentul în *hel-**lo***.
>
> **③ ACTIVITĂȚI**
> - **Faza 1 (scris):** citește micro-dialogul „At a language school" (EVA îl întâmpină pe Andrei); notă de gramatică în română despre *to be* + *a/an*; potrivește salutul cu momentul zilei; completează „I ___ from Romania".
> - **Faza 2 (pipeline):** ascultă dialogul; **conversație cu EVA** — EVA îl salută și îl întreabă cum îl cheamă și de unde e (ghidat → liber); **drill de pronunție** pe *what/where/name*; shadowing al salutărilor.
> - **Faza 3 (rest):** SRS cu cele 15 cuvinte + 8 propoziții (din Tatoeba); **scenariu:** „Te prezinți unui coleg nou" (task cu EVA); auto-verificare; test de unitate.
>
> **④ RESURSE din biblioteca EVA:** *Everyday Conversations* (dialogul „Formal/Informal Greetings & Introductions") + audio-ul aferent (`dialogue_1-01…1-04`); propoziții Tatoeba filtrate pe „name/from/hello"; *A Digital Workbook for Beginning ESOL* (secțiunea greetings & to be).
>
> **⑤ REZULTATE MĂSURABILE (Definition of Done)**
> - Înțelegere: ≥80% la 5 itemi despre dialog.
> - Producție: ≥3 propoziții corecte cu *to be* (scris) + prezentare orală reușită cu EVA.
> - Pronunție: scor ≥80 pe *what/where/name*.
> - Vocabular: ≥85% din cele 15 cuvinte reținute la 24h.
> - CEFR bifat: *„Se poate prezenta și poate saluta"* (A1).
>
> **⑥ EVALUARE:** 5 itemi (2 potrivire salut-moment, 2 completare *to be*, 1 traducere RO→EN „Mă cheamă… și sunt din România") + 1 sarcină orală cu EVA. **Barem:** 60% itemi scriși + 40% sarcina orală; prag 80%.
>
> **⑦ SARCINA COMUNICATIVĂ FINALĂ:** *„Fă cunoștință cu EVA"* — un dialog de 6–8 schimburi în care te saluți, te prezinți (nume, țară), întrebi și îți iei rămas-bun. EVA scorează pe rubrică + dă feedback de pronunție.
>
> **Schiță de script EVA (Faza 2):**
> ```
> EVA: Hello! I'm EVA. What's your name?         [RO: „Cum te cheamă?"]
> User: My name is Andrei.
> EVA: Nice to meet you, Andrei! Where are you from?
> User: I'm from Romania.
> EVA: Great — so you're Romanian! How do you say "bună" in English? … Yes, "hello"! 👋
> ```


---

# 📝 Partea a II-a — Testele de validare și plasare (A2–C2)

## Testele de validare si plasare (A2-C2)

> **Scop.** Un cursant care declara nivelul X (A2–C2 = nivelurile 2–6) da un test scurt (≈15–20 min), conversational, care fie **valideaza** ca poate incepe nivelul X, fie il **ruteaza** la nivelul real. **A1 = intrare directa**, fara test (incepator absolut). Testul e chat-first: EVA il conduce ca pe o conversatie prietenoasa, cu adaptivitate (item-response + oprire timpurie), nu ca pe un examen.

---

### 0. Principii de proiectare (masurabile)

| Principiu | Concretizare |
|---|---|
| Adaptiv, nu liniar | fiecare sectiune isi ajusteaza dificultatea dupa raspunsuri; se opreste cand incertitudinea scade sub prag (SE) |
| Scurt | buget total 15–20 min, defalcat pe sectiuni (vezi §1) |
| Chat-first | itemii vin ca mesaje EVA; raspuns prin tap (butoane), text sau voce |
| Doua roluri distincte | sectiunile receptive (A–D) **estimeaza** banda CEFR; sectiunea productiva (E) **valideaza** (poarta de decizie) |
| Scala comuna | totul se proiecteaza pe o scala numerica unica **1.0–6.9** (vezi §3) ca sa se poata combina |
| Anti-frauda / anti-bias | corectie yes-bias la vocabular, dubla-scorare LLM la productiv, itemi productivi imposibil de trecut cu traducere automata |
| Low-anxiety | ton incurajator, fara „ai gresit", feedback pe progres, RO ca limba de scafolding la nivelurile joase |

**Scala interna unica (EVA-CEFR).** Fiecare nivel are 3 sub-benzi:

```
X.0–X.3 = "intra in nivel"      (a consolidat X-1, e la pragul lui X)
X.4–X.6 = "mijloc de nivel"
X.7–X.9 = "stapaneste / iese spre X+1"
```
Ancore: A1=1, A2=2, B1=3, B2=4, C1=5, C2=6. Ex.: `3.2` = inceput de B1; `4.8` = B2 aproape terminat.

---

### 1. Structura testului: sectiuni si buget

| # | Sectiune | Ce masoara | Format | Itemi (adaptiv) | Timp tinta |
|---|---|---|---|---|---|
| **A** | Vocabular Yes/No | marimea vocabularului receptiv → banda CEFR de pornire | cuvinte reale vs pseudo-cuvinte, „stiu / nu stiu" | 40–60 stringuri | 2–3 min |
| **B** | Use of English | gramatica + vocabular sub control | MCQ 4 optiuni, calibrate IRT | 8–18 itemi | 4–6 min |
| **C** | Ascultare | intelegere dupa audio | clip scurt (10–40 s) + 1–2 intrebari | 2–4 clipuri | 3–4 min |
| **D** | Citire | intelegere text | text nivelat + gist/detaliu/inferenta/cloze | 2–3 texte | 3–4 min |
| **E** | Productiv (POARTA) | vorbire + scriere | conversatie voce cu EVA + text scurt, scorat LLM | 3–5 ture voce + 1 sarcina scrisa | 4–6 min |
| | **Total** | | | | **15–20 min** |

Sectiunile A→D se ruleaza in cascada: fiecare transmite estimarea sa (θ) ca punct de pornire pentru urmatoarea, ca sa nu se piarda timp pe itemi prea usori/prea grei. Sectiunea E este intotdeauna calibrata pe **nivelul auto-declarat X** (nu pe estimarea receptiva), fiindca ea decide validarea.

---

#### 1.A Vocabular Yes/No (marime vocabular → banda CEFR)

Test de tip Yes/No (Meara / LexTALE): se afiseaza un string; cursantul spune doar daca il recunoaste ca **cuvant real de engleza**.

- **Compozitie:** ~40 cuvinte reale distribuite pe 6 benzi de frecventa (fiecare banda ≈ o treapta CEFR) + ~20 pseudo-cuvinte plauzibile fonotactic (ex. *stronk, blicket, formation → farmition*). Sursa cuvintelor reale: liste de frecventa / profil lexical din manualele OER si din cele 16.297 propozitii paralele Tatoeba (§Resurse).
- **Prezentare chat:** carduri rapide, 2 butoane („✅ Stiu / ❌ Nu"), ~1.5 s/item.
- **Scorare cu corectie de yes-bias** (obligatorie — altfel „da la tot" trece):
  - `h` = rata de hit = (cuvinte reale marcate „da") / (nr. cuvinte reale)
  - `f` = rata de fals-alarma = (pseudo-cuvinte marcate „da") / (nr. pseudo-cuvinte)
  - **Scor corectat** `Vscore = h − f` (0–1), raportat si ca % ; optional indicele Isdt/ΔM pentru robustete.
  - Daca `f > 0.30` → sesiune marcata „nesigura" (raspuns la intamplare / yes-bias) si scorul A **nu** seteaza pornirea; se porneste B de la banda declarata − 0.5.
- **Mapare Vscore → banda CEFR de pornire** (orientativa, de recalibrat local):

  | Vscore (h−f) | Banda de pornire |
  |---|---|
  | < 0.35 | A1–A2 |
  | 0.35–0.50 | A2 |
  | 0.50–0.65 | B1 |
  | 0.65–0.80 | B2 |
  | 0.80–0.90 | C1 |
  | > 0.90 | C2 |

- **Rol:** estimare rapida, robusta, care **seteaza dificultatea de start** pentru sectiunea B. Nu decide singura plasarea.

#### 1.B Use of English adaptiv (CAT pe banca de itemi calibrata)

- **Banca de itemi:** MCQ cu 4 optiuni, fiecare etichetat cu (i) nivel CEFR, (ii) parametru de dificultate IRT `b` pe scala logit, ideal si discriminare `a` (2PL); pentru simplitate operationala se poate porni cu **model Rasch (1PL)**. Continut mixt: 50% gramatica (timpuri, aspect, articole, prepozitii, conditionale, modale), 50% vocabular/colocatii/phrasal verbs. Itemii pot fi generati din tiparele gramaticale ale manualelor (Verb Tenses for EAP, Evergreen) si validati pilot.
- **Algoritm adaptiv (CAT):**
  1. `θ₀` = logitul corespunzator benzii din sectiunea A.
  2. Selectie item = **informatie Fisher maxima** in jurul lui `θ` curent, cu balansare de continut (alterneaza gramatica/vocabular) si control de expunere.
  3. Dupa fiecare raspuns, reestimare `θ` (EAP bayesian sau ML).
  4. **Oprire timpurie:** `SE(θ) ≤ 0.33 logits` **SAU** `n ≥ 18` itemi **SAU** `n ≥ 8` cu banda deja neambigua (interval de incredere in intregime intr-o singura banda).
- **Iesire:** `θ_B` + interval de incredere → convertit in scor EVA-CEFR (§3).

#### 1.C Ascultare

- **Material:** clipuri 10–40 s din biblioteca audio MP3 (State Dept „Everyday Conversations / Dialogs", audio Tatoeba), nivelate.
- **Intrebari:** 1 de gist + 1 de detaliu per clip (MCQ, sau reordonare/potrivire in chat).
- **Adaptiv:** primul clip la banda estimata din A/B; escaladeaza/coboara dupa scor. 2–4 clipuri.
- **Regula:** un clip poate fi reascultat **o singura data**; se scoreaza obiectiv.

#### 1.D Citire

- **Texte:** scurte, nivelate prin readability + profil lexical CEFR, din manualele OER (BC Reads, Conestoga Readers, Green Tea, PDX Journeys).
- **Itemi:** gist, detaliu, inferenta, **cloze bancat** (completare cu banca de optiuni).
- **Adaptiv:** text la banda estimata; +1/−1 banda dupa performanta. 2–3 texte.

#### 1.E Validare PRODUCTIVA (poarta de decizie)

Aici estimarea receptiva devine „validat sa inceapa nivelul X". Sarcinile sunt **calibrate pe X auto-declarat**.

- **Vorbire (voce, cu EVA):** 3–5 ture, sarcina scalata pe nivel:
  - A2: descrie o poza / raspunde la intrebari despre rutina;
  - B1: nareaza o intamplare la trecut, da o opinie simpla cu motiv;
  - B2: sustine un punct de vedere, compara doua optiuni;
  - C1–C2: dezvolta un argument abstract, gestioneaza o obiectie a EVA.
  - Pipeline: ASR (transcriere) + semnale de fluenta (rata de vorbire, pauze, reformulari) + pronuntie → scorare LLM pe rubrica (§4).
- **Scriere:** 1 sarcina scurta calibrata pe X (40–80 cuvinte la A2–B1, 80–120 la B2–C2), ex. mesaj, mini-opinie. Scorata de LLM pe rubrica.
- **Anti-copiere:** promptul cere continut personal/imprevizibil („de ce ai ales…?"), iar EVA pune o intrebare de continuare in timp real — dificil de rezolvat cu traducere automata.

---

### 2. Administrare chat-first (conversational + adaptiv)

**Flux ca dialog EVA (nu ca formular):**

1. **Salut + calibrare asteptari** (RO la nivel jos, EN la nivel inalt): „Salut! Sunt EVA. Zici ca esti la **B1** — hai sa vedem in ~15 minute, ca sa incepi exact de unde trebuie. Fara note, fara stres. 💪"
2. **A (vocabular):** joc rapid de carduri („stiu / nu stiu"), bara de progres.
3. **B (use of English):** intrebari una cate una ca mesaje, raspuns prin tap; EVA reactioneaza scurt si pozitiv, fara sa dezvaluie corect/gresit.
4. **C / D:** „Asculta 20 de secunde…" / „Citeste mesajul asta…" apoi 1–2 intrebari.
5. **E (productiv):** trece natural in conversatie reala — „Acum hai sa vorbim un pic. Povesteste-mi…". Butonul de microfon; daca refuza vocea, doar scris (cu nota ca pronuntia nu poate fi validata).
6. **Rezultat:** ecran de tip „profil", nu „nota" (§3, §6).

**Mecanisme de adaptivitate vizibile discret pentru user, riguroase in spate:**
- pornire calda (itemi usori la inceputul fiecarei sectiuni pentru incredere), apoi CAT;
- oprire timpurie pe SE → sesiunea se scurteaza cand raspunsurile sunt consecvente;
- „ancore" de scafolding RO care dispar pe masura ce nivelul creste;
- salvare de stare: daca abandoneaza, reia de unde a ramas.

---

### 3. Scorare, combinare si mapare pe CEFR

**Pas 1 — fiecare sectiune produce un scor pe scala EVA-CEFR (1.0–6.9)** prin tabele de conversie:
- A: `Vscore → banda` (tabelul din §1.A), luat ca punct in mijlocul benzii.
- B: `θ_B (logits) → EVA-CEFR` prin cut-points calibrate (ex. tabel de ancorare Rasch↔CEFR).
- C, D: `% corect ponderat pe dificultatea itemilor → EVA-CEFR`.
- E: media rubricii productive (§4) exprimata direct in sub-benzi CEFR.

**Pas 2 — compozit receptiv** `R`:
```
R = 0.35·B + 0.25·D + 0.25·C + 0.15·A     (A–D pe scala EVA-CEFR)
```
plus interval de incredere `CI_R` din SE-urile agregate.

**Pas 3 — decizia de validare** foloseste atat `R` cat si productivul `E`.

**Ce inseamna „validat sa inceapa nivelul X":**
> Ca sa *incepi* nivelul X trebuie sa fi **consolidat X-1**, adica sa fii la pragul de intrare in X. Deci criteriul este demonstrarea abilitatii **cel putin la podeaua lui X (= varful lui X-1)**, atat receptiv, cat si productiv.

**Reguli de decizie (per nivel tinta X ∈ {2..6}):**

| Conditie | Decizie |
|---|---|
| `R ≥ X.0` **SI** `E ≥ (X−1).7` | ✅ **VALIDAT** — incepe nivelul X |
| `R ≥ X.4` **SI** `E ≥ X.0` pe o marja clara | ✅ Validat; se sugereaza chiar test de urcare (poate incepe mai sus, vezi randul urmator) |
| `floor(R) > X` (net peste) | ⤴ Se recomanda nivelul `floor(R)`; userul alege (respectam auto-declararea, dar recomandam) |
| `X−0.3 ≤ R < X.0` **SAU** `E` sub prag cu putin | ⚠ **Validare provizorie**: incepe X cu suport adaptiv + diagnostic tintit pe golul detectat; recheck la 2 saptamani |
| `R < X−0.3` **SAU** `E ≤ (X−2).x` | ⤵ **Rutat in jos** la `round(R)`; mesaj pozitiv: „Ai baze bune de [nivel]; incepem de acolo ca sa mergem rapid" |

**Praguri de promovare/validare pe nivel tinta (rezumat cifric):**

| Nivel tinta X | Podea receptiva `R` | Poarta productiva `E` (rubrica medie) |
|---|---|---|
| A2 (2) | ≥ 2.0 | ≥ A1 solid (1.7) |
| B1 (3) | ≥ 3.0 | ≥ A2 solid (2.7) |
| B2 (4) | ≥ 4.0 | ≥ B1 solid (3.7) |
| C1 (5) | ≥ 5.0 | ≥ B2 solid (4.7) |
| C2 (6) | ≥ 6.0 | ≥ C1 solid (5.7) |

**Regula de siguranta (accuracy floor):** daca `E` receptiv e mare dar productivul e slab (tipic „recunosc dar nu produc"), poarta productiva **primeaza** — validarea nu se acorda pe baza receptivului singur. Invers, productiv bun + receptiv slab → validare provizorie + diagnostic.

---

### 4. Rubrica de vorbire / scriere (criterii CEFR, scorata de LLM)

**Criterii** (vorbire = toate 6; scriere = fara *Interaction* si *Pronunciation*):

| Criteriu | Ce evalueaza |
|---|---|
| **Range** | amploarea vocabularului si a structurilor gramaticale folosite |
| **Accuracy** | corectitudinea gramaticala si lexicala; densitatea/gravitatea erorilor |
| **Fluency** | debit, pauze, reformulari (vorbire) / cursivitate si productivitate (scriere) |
| **Coherence** | organizare, conectori, coeziune, claritatea firului |
| **Interaction** | (vorbire) initiativa, raspuns la EVA, turn-taking, reparare |
| **Pronunciation** | (vorbire) inteligibilitate, accent, prozodie |

**Descriptori pe niveluri (originali, parafraza CEFR):**

| Nivel | Range | Accuracy | Fluency | Coherence | Interaction | Pronunciation |
|---|---|---|---|---|---|---|
| **A1** | cuvinte/expresii izolate, formule invatate | corect doar in tipare memorate | ezitari mari, enunturi f. scurte | cuvinte legate cu „and/then" | raspunde la intrebari simple, foarte lent | inteligibil cu efort, pentru interlocutor obisnuit |
| **A2** | repertoriu de baza pentru situatii uzuale | erori sistematice, dar sensul de baza trece | fraze scurte, pauze frecvente | idei inlantuite simplu, liniar | schimb simplu de replici pe teme familiare | in general inteligibil, cu accent puternic |
| **B1** | vocabular suficient pentru teme familiare, cauta cuvinte | control rezonabil pe structuri frecvente; erori la structuri complexe | continua audibil, chiar cu pauze de planificare | povesteste liniar, conectori simpli | initiaza/sustine conversatie pe teme cunoscute | clar inteligibil, accent evident |
| **B2** | gama larga, variaza formularea, putine goluri evidente | control gramatical bun, erori rare care nu deranjeaza | ritm relativ constant, spontan | argument structurat, conectori variati | interactioneaza fluent, preia si da initiativa | pronuntie clara, naturala; intonatie corecta |
| **C1** | repertoriu larg, exprima nuante, colocatii idiomatice | control constant; erori sporadice, se auto-corecteaza | spontan, fluent, aproape fara efort | discurs bine organizat, coeziune buna | intervine abil, alege registrul potrivit | variaza intonatia pentru accent fin |
| **C2** | stapanire totala, precizie si idiomaticitate | acuratete sustinuta chiar in enunturi complexe | fluent, fara efort perceptibil | structura logica impecabila, subtila | interactiune fara efort, manevra fina a discursului | control fonologic complet, subtilitati prozodice |

**Protocol de scorare LLM (pentru fiabilitate masurabila):**
1. LLM primeste: transcrierea/textul + rubrica de mai sus + 2–3 **exemple-ancora** per criteriu (calibrare).
2. Produce, per criteriu, **sub-banda CEFR + justificare scurta cu dovada** (citat din raspuns).
3. **Agregare:** media aritmetica a criteriilor, cu **plafonare pe accuracy** pentru afirmatia globala (un criteriu mult sub restul limiteaza banda globala cu max 0.3).
4. **Dubla-scorare / self-consistency:** 2 treceri; daca difera cu > 0.5 banda → a treia trecere sau marcaj „low-confidence" → recheck productiv scurt.
5. Semnale obiective de vorbire (rata de vorbire, % pauze, reformulari) intra ca priori in Fluency/Pronunciation, nu inlocuiesc judecata LLM.

---

### 5. Re-testare, checkpoint-uri si testul final de nivel

**a) Micro-checkpoint-uri (in flux, invizibile ca „test"):**
- retrieval spatiat integrat in lectii; quiz de unitate la fiecare ~5 lectii (5–8 itemi adaptivi).
- prag de trecere unitate: ≥ 75% receptiv + minim 1 productie scurta ≥ nivelul unitatii.

**b) Re-plasare periodica (ajustare sub-banda):**
- declansata de: fiecare ~10 lectii, SAU platou (3 quiz-uri sub prag), SAU progres rapid (3 quiz-uri ≥ 90%).
- format: recheck scurt 5–8 min (mini-A + mini-B adaptiv + 1 productie); poate urca/cobori **sub-banda** in interiorul nivelului sau, la platou persistent, propune consolidare.

**c) Testul final de nivel (poarta spre nivelul urmator):**
- **Comprehensiv, toate cele 5 skill-uri**, calibrat pe varful nivelului (X.7–X.9).
- **Criterii de promovare la X+1** (toate obligatorii):
  1. Receptiv (A–D) ≥ **80%** ponderat pe dificultate;
  2. Productiv (rubrica) ≥ **X.7** la fiecare criteriu, cu **Accuracy ≥ X.6** (fara criteriu sub X.5);
  3. Acoperirea „can-do statements" ale nivelului: ≥ **85%** din obiectivele functionale bifate in parcurs;
  4. Fara skill „in urma": niciun skill sub `X.4`.
- Rezultat: **Promovat** (deblocheaza X+1) / **Aproape** (2 saptamani de consolidare tintita pe skill-ul slab, apoi re-test partial doar pe acel skill) / **Consolidare** (mai ramane pe nivel).

**d) Reguli anti-degradare:** un skill neexersat > 60 zile declanseaza un mini-recheck inainte de a conta la promovare (evita „promovare pe scor vechi").

---

### 6. Iesirea catre cursant (profil, nu nota)

La final EVA arata un **profil**, nu un scor rece:
- verdict clar: „✅ Confirmat B1 — incepem nivelul B1" / „Incepem de la A2, ai baze bune";
- radar pe 5 skill-uri (vocabular, gramatica, ascultare, citire, vorbire+scriere) cu sub-banda per skill;
- 1–2 puncte tari + 1 gol prioritar pe care primele lectii il vor tinti;
- interval de incredere comunicat simplu („esti clar la B1"; sau „esti intre A2 si B1 — incepem la limita si ajustam din mers").

---

#### Resurse din biblioteca EVA folosite ca material de test
- **Yes/No vocab (A):** liste de frecventa + profil lexical din manualele OER si din cele 16.297 propozitii Tatoeba; pseudo-cuvintele se genereaza prin alterare fonotactica.
- **Use of English (B):** itemi din tiparele gramaticale (Verb Tenses for EAP, Evergreen), calibrati pilot.
- **Ascultare (C):** MP3 State Dept (Everyday Conversations, Dialogs) + audio Tatoeba, segmentate si nivelate.
- **Citire (D):** texte scurte din BC Reads, Conestoga Readers, Green Tea, PDX Journeys, nivelate prin readability + profil CEFR.
- **Scafolding RO (niveluri joase):** perechile RO-EN Tatoeba + Peace Corps RO-EN pentru instructiuni bilingve si itemi de traducere-recunoastere.

> **Nota de calibrare:** toate cut-point-urile numerice (Vscore→banda, θ→CEFR, praguri %) sunt **valori de pornire**, de rafinat cu un pilot de ancorare (ex. 100–200 useri cu nivel cunoscut) inainte de productie.


---

# 📚 Partea a III-a — Cuprinsul (syllabus) pe niveluri

*Fiecare unitate de mai jos se dezvoltă cu șablonul din Partea I (§4) pentru a produce componenta scrisă.*


## Nivel A1 — Beginner / Începător (CEFR A1: „Utilizator elementar — poate comunica simplu în situații de rutină, dacă interlocutorul vorbește rar și clar")

**Obiectiv global de nivel (CAN-DO):** La finalul nivelului A1, cursantul *poate* să se prezinte și să prezinte alte persoane, să pună și să răspundă la întrebări simple despre date personale (nume, unde locuiește, ce are, pe cine cunoaște), să interacționeze în tranzacții cotidiene foarte simple (salut, cumpărături, comandă de mâncare, spus ora), folosind propoziții scurte, izolate, cu vocabular frecvent — atât în scris (chat) cât și vocal cu EVA, la un ritm lent și cu sprijin.

**Prag de intrare / ieșire:**
- *Intrare:* zero cunoștințe presupuse (nivelul de start al aplicației); necesar doar alfabet latin și motivație.
- *Ieșire:* vocabular cumulat activ ~600-650 de cuvinte/expresii; arii gramaticale stăpânite: `to be` (afirmativ/negativ/interogativ), present simple (toate persoanele + persoana a III-a `-s`), articole `a/an/the` (+ contrast cu absența articolului), plural regulat + neregulate frecvente, `this/that/these/those`, `have got`, `can` (abilitate + cerere politicoasă), `there is/there are`, prepoziții de loc și de timp (`in/on/at/under/next to`), întrebări WH (`what/where/who/when/how many/how much/how old`), adjective posesive, `like + -ing/noun`, countable/uncountable la nivel introductiv.

*(Rezumat test de validare la intrare: nu se aplică — A1 este nivelul de start.)*

### Module și Unități (CUPRINS)

#### Modulul 1 — „Hello! Cine sunt eu" (salut, identitate, obiecte, articole)

| # | Unitate (temă) | Funcții comunicative (CAN-DO) | Gramatică | Vocabular (temă / nr) | Fonetică RO | Obiectiv măsurabil |
|---|---|---|---|---|---|---|
| 1 | **Hello & Goodbye** (salut, alfabet, spelling) | Pot saluta și îmi pot lua rămas-bun; pot spune și silabisi (spell) numele meu; pot cere cuiva să repete | Pronume personale subiect (I/you/he/she…); `My name is…`; imperative de clasă (`Listen, Repeat`) | Formule de salut, alfabetul englez, „spelling", politețuri de bază (temă / **40**) | `/h/` aspirat în *hello, hi, how* (românii îl „înghit"); intonație de salut | Silabisește corect propriul nume și 3 cuvinte dictate (≥90% litere corecte) și salută/își ia rămas-bun în ≥8 schimburi de chat fără eroare |
| 2 | **Who are you?** (informații personale, țări) | Pot să mă prezint și să cer identitatea altcuiva; pot spune de unde sunt și ce naționalitate am | Verbul `to be` — afirmativ/negativ/interogativ (`am/is/are`, forme scurte `I'm, he's`) | Țări, naționalități, întrebări personale de bază (temă / **55**) | `/iː/` vs `/ɪ/` în *he/she/is/it/this*; forme slabe („weak forms") ale lui *is/are* | Produce ≥6 propoziții corecte cu `to be` (min. 1 negativă + 1 interogativă) și completează o „fișă de prezentare" în chat cu ≥80% acuratețe |
| 3 | **A, an or the?** (obiecte, articole — drill contrastiv RO!) | Pot numi obiecte din jur și pot spune „este un/o…"; pot distinge prima menționare vs. cea cunoscută | `a/an` (vocală/consoană) vs `the` vs **articol zero** — contrast explicit cu limba română (art. hotărât enclitic *-ul/-a*!) | Obiecte de zi cu zi (clasă, birou, geantă), culori (temă / **35**) | `/ə/` (schwa) în *a*; `the` = `/ðə/` înainte de consoană, `/ðiː/` înainte de vocală, cu `/ð/` corect (nu *ză/de*) | La un test de 20 de spații cu `a/an/the/—`, obține ≥80% corect și explică oral 1 regulă de contrast RO-EN |
| 4 | **This, that & many things** (obiecte apropiate/depărtate, plural) | Pot indica obiecte („acesta/acela") și pot spune câte sunt; pot forma pluralul | `this/that/these/those`; plural regulat (`-s/-es`) + neregulate frecvente (*man→men, child→children*) | Extindere obiecte + școală/casă, cantități mici (temă / **50**) | `/ð/` în *this/that/these/those*; terminații de plural `/s/`–`/z/`–`/ɪz/` (*books/pens/boxes*) | Transformă corect ≥10 substantive la plural (inclusiv 2 neregulate) și clasifică terminația fonetică `/s z ɪz/` cu ≥80% acuratețe |

#### Modulul 2 — „Oamenii mei și timpul" (familie, numere, oră, dată)

| # | Unitate (temă) | Funcții comunicative (CAN-DO) | Gramatică | Vocabular (temă / nr) | Fonetică RO | Obiectiv măsurabil |
|---|---|---|---|---|---|---|
| 5 | **My family** (familie, posesie) | Pot prezenta membrii familiei și pot spune ce/pe cine am; pot exprima posesia | `have got / has got` (afirmativ/negativ/interogativ); adjective posesive (`my/your/his/her/our/their`) | Membri ai familiei, stare civilă, animale de companie (temă / **55**) | `/ð/` în *mother, father, brother, the*; contrast cu `/θ/` | Descrie propria familie în ≥6 propoziții cu `have got` + posesive (min. 4 corecte gramatical) în conversație vocală cu EVA |
| 6 | **Numbers & Age** (numere, vârstă, prețuri intro) | Pot număra, pot spune și întreba vârsta, pot citi numere de telefon și prețuri simple | Numere cardinale 0–100; `How old…? — I'm … (years old)`; `How many…?` | Numere 0–100, vârstă, telefon, prețuri de bază (temă / **60**) | `/θ/` în *three, thirteen, thirty*; contrast de accent *thirTEEN* vs *THIRty* | Ascultă și scrie corect ≥8/10 numere dictate și distinge *-teen/-ty* prin accent cu ≥80% acuratețe |
| 7 | **What time is it?** (ora, zile, luni, dată) | Pot spune și cere ora, ziua, luna și data; pot vorbi despre program | Prepoziții de timp `at/on/in` (`at 7 o'clock, on Monday, in July`); `What time…? When…?` | Ore, zilele săptămânii, luni, momente ale zilei (temă / **65**) | `/θ/` în *Thursday, month, three o'clock*; `/z/` final în *days*; reducerea vocalelor neaccentuate | Spune corect ≥8 ore diferite și completează un mini-orar cu prepozițiile `at/on/in` corecte în ≥80% din cazuri |

#### Modulul 3 — „Viața de zi cu zi" (rutină, casă, mâncare, cumpărături)

| # | Unitate (temă) | Funcții comunicative (CAN-DO) | Gramatică | Vocabular (temă / nr) | Fonetică RO | Obiectiv măsurabil |
|---|---|---|---|---|---|---|
| 8 | **My daily routine** (rutina zilnică — I/you/we) | Pot descrie ce fac zilnic și cât de des; pot vorbi despre programul meu | Present simple (I/you/we/they) afirmativ/negativ (`don't`); adverbe de frecvență (`always/usually/sometimes/never`) | Verbe de rutină (get up, work, eat, sleep…), părți ale zilei (temă / **60**) | `/w/` vs `/v/` în *wake, work, watch* vs *very* (românii confundă!); `/w/` labial nu labiodental | Produce ≥8 propoziții despre rutina proprie (min. 2 negative + 2 cu adverb de frecvență) cu ≥75% acuratețe gramaticală |
| 9 | **He works, she plays** (persoana a III-a, întrebări WH) | Pot descrie rutina altcuiva; pot pune întrebări despre ce, unde, când, cine | Present simple pers. a III-a `-s/-es`; `does/doesn't`; întrebări WH (`what/where/when/who`) | Verbe extinse + profesii, cuvinte de întrebare (temă / **45**) | Terminația `-s` la verbe: `/s/`–`/z/`–`/ɪz/` (*works/plays/watches*); auxiliar *does* redus | Adaugă corect `-s` și terminația fonetică la ≥8/10 verbe și formează ≥5 întrebări WH corecte cu `do/does` |
| 10 | **My house** (casă, camere, mobilier) | Pot descrie casa mea și pot spune ce se află unde | `There is / There are` (+ neg./interog. `Is there…? / any`); prepoziții de loc (`in/on/under/next to/behind`) | Camere, mobilier, obiecte casnice (temă / **60**) | `/ð/` în *there*; `/θ/` în *bathroom, three rooms*; forme slabe ale prepozițiilor | Descrie o cameră în ≥6 propoziții cu `there is/are` + ≥4 prepoziții de loc corecte, verificat pe o imagine (≥80% potrivire) |
| 11 | **Food & drink** (mâncare, preferințe) | Pot numi alimente, pot spune ce îmi place/nu-mi place și ce pot să fac | `like/don't like + noun/-ing`; countable vs uncountable (`some/any`) — introductiv; `can` (abilitate) | Alimente, băuturi, mese, verbe „a putea face" (temă / **65**) | `/æ/` vs `/e/` în *apple/cat* vs *bread/egg* (românii aud „e" peste tot); `/ɔː/` în *water* | Exprimă ≥6 preferințe alimentare (`I like / I don't like`) și clasifică ≥8 alimente în countable/uncountable cu ≥75% acuratețe |
| 12 | **At the shop** (cumpărături simple — recapitulare) | Pot cumpăra lucruri simple: pot cere un produs, întreba prețul, plăti și mulțumi | `Can I have…? How much is/are…?`; recapitulare integrată `a/an/the`, plural, numere, present simple | Magazin, produse, bani, formule de tranzacție (temă / **60**) | Recapitulare `/θ/` la prețuri (*three, thirty*); `/aʊ/` în *how much*; intonație politicoasă | Joacă un rol „cumpărături" cu EVA (min. 8 replici), cere ≥3 produse, întreabă corect prețul și încheie tranzacția cu ≥80% inteligibilitate |

**Checkpoint-uri și Test final de nivel:**
- **Checkpoint 1 (după Unit 4):** ≥80% la quiz de gramatică (to be, articole, plural) + prezentare vocală de sine de 5 propoziții, inteligibilă.
- **Checkpoint 2 (după Unit 7):** ≥80% la test (have got, numere, oră/prepoziții de timp) + ascultare: 8/10 numere și ore dictate corect.
- **Checkpoint 3 (după Unit 10):** ≥80% la test (present simple toate persoanele, WH, there is/are) + descriere vocală a unei imagini (cameră/rutină) cu ≥6 propoziții corecte.
- **Test final de nivel A1 (promovare la A2), criterii cumulative — trebuie îndeplinite TOATE:**
  1. **Scris/Gramatică:** ≥80% la testul integrat (60 de itemi acoperind toate cele 12 unități).
  2. **Vocabular:** recunoaște și folosește activ ≥80% din cele ~600 de cuvinte (test SRS: ≥480 carduri „știute").
  3. **Vorbire (task real cu EVA):** susține un dialog de rutină (prezentare + cumpărături SAU program zilnic), min. 10 replici, cu ≥75% acuratețe gramaticală pe structurile A1.
  4. **Pronunție:** scor de pronunție ≥80 pe cuvintele-țintă cu `/θ/–/ð/` și `/w/–/v/`; distinge auditiv `/iː/–/ɪ/` și `/æ/–/e/` cu ≥75% acuratețe.
  5. **Ascultare:** ≥80% înțelegere la 3 dialoguri scurte, lente (salut, oră/numere, cumpărături).
  6. **Descriptor CEFR atins:** confirmat A1 (Global Scale — „poate interacționa simplu, pune/răspunde întrebări despre date personale, dacă interlocutorul vorbește rar și e pregătit să ajute").

**Resurse din biblioteca EVA:**
- **Manuale OER / State Dept:** unitățile de început ale manualelor de engleză din bibliotecă (secțiunile „Greetings, Personal Information, Family, Numbers, Time, Food, Home, Daily Routine, Shopping") — sursă pentru texte, dialoguri și exerciții scrise (Faza 1).
- **Propoziții paralele RO-EN (Tatoeba, ~16.000):** filtrate pe frecvență/lungime scurtă pentru fiecare temă — alimentează drill-urile contrastive (mai ales articole și `to be`/present simple), cardurile SRS și shadowing-ul (Fazele 1 și 3).
- **Audio MP3:** clipuri scurte pentru ascultare, model de pronunție și exerciții de shadowing pe țintele fonetice (`/θ ð/`, `/w v/`, terminații `-s`, numere) — Faza 2.
- **Gramatici RO-EN:** referință pentru explicațiile de gramatică *în limba română* (care se estompează spre A2), în special contrastul articolului hotărât RO enclitic vs. `the` englez.
- **Dicționar RO-EN:** generarea listelor de vocabular tematic și a definițiilor din cardurile SRS (Faza 3).


## Nivel A2 — Elementary (Utilizator elementar / CEFR A2)

**Obiectiv global de nivel (CAN-DO):** La finalul nivelului, cursantul poate comunica în sarcini simple și de rutină care cer un schimb direct de informații pe teme familiare (cumpărături, muncă, călătorii, sănătate, evenimente trecute). Poate descrie în termeni simpli trecutul apropiat, mediul înconjurător și planurile imediate, poate cere și oferi indicații, și poate purta cu EVA o conversație scurtă susținută (6-10 schimburi) fără a se bloca.

**Prag de intrare / ieșire:**
- **Intrare (venind din A1):** vocabular cumulat ~800-1000 cuvinte; controlează *to be / have got*, present simple afirmativ/negativ/interogativ, plural, articole *a/an/the*, *there is/are*, prepoziții de bază, numere, cifre, întrebări *wh-* simple.
- **Ieșire (spre B1):** vocabular cumulat ~2200-2500 cuvinte; controlează present simple vs present continuous, adverbe de frecvență, *some/any/much/many* + countable/uncountable, past simple (regulate + neregulate) afirmativ/negativ/interogativ, comparativ/superlativ, *going to* și *present continuous* cu valoare de viitor, *should/shouldn't*.

**Rezumat test de validare la intrare (A2):** cursantul demonstrează, în ~15 minute mixt scris+voce, că poate: (a) se prezenta și pune 5 întrebări personale corecte la present simple; (b) descrie o imagine cu *there is/are* și 6 substantive; (c) conjuga corect present simple la persoana III (≥8/10 itemi, cu *-s*); (d) susține cu EVA un mini-dialog de 4 schimburi despre rutina zilnică. **Prag de admitere:** ≥70% global și scor de pronunție ≥65 pe cuvintele-test. Sub prag → traseu de recapitulare A1.

### Module și Unități (CUPRINS)

Progresie în spirală: fiecare modul reia structuri anterioare și adaugă un strat nou. Fiecare unitate parcurge cele 3 faze (scris → pipeline voce cu EVA → consolidare & test).

#### Modulul 1 — „Viața mea acum" (prezent, rutine, mediul apropiat)

| # | Unitate (temă) | Funcții comunicative (CAN-DO) | Gramatică | Vocabular (temă / nr) | Fonetică RO | Obiectiv măsurabil |
|---|---|---|---|---|---|---|
| **A2.1** | Eu, acum vs de obicei (rutină & prezent momentan) | Pot spune ce fac de obicei și ce fac chiar acum; pot descrie o zi tipică | Present simple **vs** present continuous; adverbe de frecvență (*always→never*) | Rutină, verbe zilnice, momente ale zilei / **120** (cum. ~1120) | *th* /θ/ /ð/ (*this, three, mother*); *-s* pers. III /s/-/z/-/ɪz/ | Produce **6 propoziții** care contrastează corect cele două timpuri (*I usually… / I'm …-ing now*); ≥5/6 corecte + scor pronunție **≥75** pe cuvinte cu /θ/ |
| **A2.2** | Cartierul meu & indicații | Pot cere/da indicații simple; pot descrie unde se află lucrurile | Prepoziții de loc/mișcare; *there is/are* + *some/any*; imperativ pt. indicații | Oraș, clădiri, direcții / **140** (cum. ~1260) | /w/ vs /v/ (*where, we, very, village*) | Ghidează EVA pe un traseu de **4 pași** (turn left/go straight/…) corect; ascultătorul (EVA) ajunge la destinație în ≥90% din încercări |
| **A2.3** | Mâncare & cumpărături | Pot cere produse și cantități; pot întreba prețul | Countable/uncountable; *much/many, some/any, a lot of, a few/a little* | Alimente, magazine, cantități, bani / **150** (cum. ~1410) | /iː/ vs /ɪ/ (*cheese/chips, eat/it, sheep/ship*) | Simulează cu EVA o cumpărătură cu **≥5 produse** folosind corect *some/any/how much/how many*; ≥80% acuratețe pe articolul countable/uncountable |
| **A2.4** | Muncă & studiu în desfășurare | Pot descrie ce fac colegii/eu în această perioadă; pot vorbi despre program | Present continuous pt. situații temporare; *love/like/hate + -ing* | Meserii, birou, activități, orar / **130** (cum. ~1540) | /æ/ vs /e/ (*man/men, bad/bed*); *-ing* /ŋ/ fără „g" dur | Descrie oral **5 activități** în desfășurare + 2 preferințe (*I like working…*); ≥80% la testul scris al modulului |

#### Modulul 2 — „Ce s-a întâmplat" (past simple: povești, călătorii, evenimente)

| # | Unitate (temă) | Funcții comunicative (CAN-DO) | Gramatică | Vocabular (temă / nr) | Fonetică RO | Obiectiv măsurabil |
|---|---|---|---|---|---|---|
| **A2.5** | Ieri (introducere trecut) | Pot spune unde/cum am fost și ce am făcut ieri | Past simple *was/were*; verbe **regulate** *-ed* (afirmativ) | Ieri, timp trecut, verbe regulate frecvente / **120** (cum. ~1660) | Terminații *-ed* /t/-/d/-/ɪd/ (*worked/played/wanted*) | Povestește oral **6 acțiuni** din ziua de ieri cu verbe regulate; pronunță corect terminația *-ed* la **≥80%** dintre ele |
| **A2.6** | Amintiri & povești | Pot povesti o întâmplare din trecut cu verbe uzuale | Past simple **neregulat** (*go/went, see/saw, have/had…* — top 25) | Copilărie, evenimente de viață, verbe neregulate / **150** (cum. ~1810) | Schimbări vocalice (*go→went, buy→bought*); schwa în silabe neaccentuate | Reproduce corect **≥20/25** verbe neregulate; spune o poveste scurtă (5-6 propoziții) cu ≥4 neregulate corecte |
| **A2.7** | O călătorie | Pot povesti o călătorie: negări și întrebări la trecut | Past simple negativ (*didn't*) + interogativ (*did you…?*); expresii de timp (*last, ago, in 2020*) | Transport, vacanță, cazare / **150** (cum. ~1960) | Accent în cuvinte bisilabice; *did you* → /dɪdʒə/ (connected speech) | Pune EVA-ei **6 întrebări** la past simple despre o călătorie și răspunde la 6, cu ≥85% acuratețe pe forma *did/didn't* |
| **A2.8** | Evenimente & sărbători | Pot descrie un eveniment trecut: cine, ce, când, unde, de ce | Recapitulare past simple (toate formele) + întrebări *wh-* la trecut | Sărbători, petreceri, evenimente sociale / **120** (cum. ~2080) | Intonație întrebări (rising/falling); linking între cuvinte | Descrie un eveniment în **8 propoziții** la trecut și răspunde la 5 întrebări *wh-*; ≥80% la checkpoint-ul de modul (atinge descriptorul A2 „poate povesti o experiență") |

#### Modulul 3 — „Comparații & planuri" (comparativ/superlativ, viitor, sănătate)

| # | Unitate (temă) | Funcții comunicative (CAN-DO) | Gramatică | Vocabular (temă / nr) | Fonetică RO | Obiectiv măsurabil |
|---|---|---|---|---|---|---|
| **A2.9** | Cumpărături & comparații | Pot compara două produse/opțiuni și îmi pot exprima preferința | Comparativ (*-er / more…*, *than*); *(not) as … as* | Produse, calități, prețuri, opinii / **130** (cum. ~2210) | *-er* final /ə/; *than* formă slabă /ðən/ | Compară oral **5 perechi** de produse (*cheaper/more comfortable than*) și alege motivat; ≥85% forme comparative corecte |
| **A2.10** | Cel mai bun (superlativ) | Pot spune care e cel mai bun/mare/ieftin dintr-un grup | Superlativ (*the -est / the most…*); *one of the…* | Recorduri, orașe, recenzii / **110** (cum. ~2320) | *-est* /ɪst/; *the* /ðə/ vs /ðiː/ | Descrie un „top 3" (oraș/produs) cu **5 superlative** corecte; scor pronunție **≥80** pe *the + superlativ* |
| **A2.11** | Sănătate & sfaturi | Pot descrie o problemă de sănătate și cere/da un sfat | *should/shouldn't*; *have a/an + boală*; *feel + adjectiv* | Corp, simptome, farmacie, sfaturi / **110** (cum. ~2430) | /ʃ/ (*should*); grupuri de consoane (*health* /helθ/) | Jucă un dialog pacient–EVA de **6 schimburi**: descrie 3 simptome + primește/dă 3 sfaturi cu *should/shouldn't* corecte ≥80% |
| **A2.12** | Planuri de viitor | Pot vorbi despre planuri, intenții și aranjamente viitoare | *going to* (intenții/predicții) vs present continuous (aranjamente fixe) | Weekend, obiective, agendă / **120** (cum. ~2550) | *going to → gonna*; *to* formă slabă /tə/; intonație de viitor | Prezintă **6 planuri** (3 cu *going to*, 3 aranjamente cu present continuous), distinge corect cele două ≥80%; susține conversație finală de 8 schimburi cu EVA |

**Checkpoint-uri și Test final de nivel:**
- **Checkpoint Modul 1 (după A2.4):** ≥80% la testul scris (present simple vs continuous, adverbe, *some/any/much/many*) **și** conversație voce de 6 schimburi despre rutină/mediu cu ≥75 scor pronunție global.
- **Checkpoint Modul 2 (după A2.8):** narează oral o experiență trecută (8-10 propoziții) cu ≥80% verbe la past simple corecte (regulate + neregulate) și terminații *-ed* pronunțate corect ≥80%.
- **Checkpoint Modul 3 (după A2.12):** produce comparativ/superlativ și *going to* în context real cu ≥80% acuratețe.
- **Test final de nivel (promovare la B1):** patru probe măsurabile —
  1. **Gramatică & vocabular (scris):** ≥80% pe 40 itemi ce acoperă toate structurile A2.
  2. **Producție scrisă:** un e-mail/postare de 60-80 cuvinte (o experiență trecută + un plan) — ≥80% propoziții corecte, ≥12 cuvinte din vocabularul nivelului.
  3. **Interacțiune voce cu EVA:** joc de rol task-based (ex. rezolvă o problemă la un magazin/aeroport) de ≥10 schimburi, susținut fără blocaj > 5 sec.
  4. **Pronunție:** scor global **≥80**, cu focus pe /θ ð/, /iː ɪ/, /v w/ și terminații *-ed*.
  - **Prag de promovare:** ≥80% global pe toate cele patru probe → descriptor CEFR A2 confirmat, deblocare B1.

**Resurse din biblioteca EVA:**
- **Manuale de bază (Faza 1 & 3):** *Digital Workbook ESOL*, *BC Reads Course Pack 1 + Reader 1*, *Evergreen Beginner*, *Conestoga Reader 1* (`Z:\02\01. Incepatori A1-A2`); pentru unitățile de tranziție A2.9-A2.12 se aduc texte din *Communication Beginnings*, *Evergreen Intermediate*, *PDX Journeys*, *Conestoga Reader 4* (`Z:\02\02. Incepator avansat - Intermediar A2-B1`).
- **Dialoguri & pipeline voce (Faza 2):** *Everyday Conversations* și *Dialogs for Everyday Use* (State Dept) + *More Dialogs* pentru scenariile de cumpărături/călătorii/sănătate; **audio MP3 State Dept** (de descărcat la cerere) pentru ascultare și shadowing.
- **Carduri SRS & propoziții paralele (Faza 3):** ~16.297 propoziții paralele RO-EN Tatoeba (`Z:\02\04. Resurse Romana-Engleza`) — sursă pentru cardurile SRS și autoverificare cu traducere RO ca sprijin, filtrate pe temele fiecărei unități.
- **Scriere (Faza 1/3):** *Developing Writing* (State Dept) pentru sarcinile de producție scrisă (e-mail, descriere, mini-poveste).
- **Sprijin RO & gramatică contrastivă:** *Peace Corps RO-EN* + *FSI Romanian Grammar* (`Z:\02\05. Dictionare si Gramatica`) pentru explicațiile de gramatică în română și țintirea greșelilor tipice ale vorbitorilor de română.


## Nivel B1 — Intermediate (Utilizator independent, prag / „threshold")
**Obiectiv global de nivel (CAN-DO):** Poate purta o conversatie sustinuta despre experiente, planuri, opinii si situatii cotidiene (calatorie, munca, timp liber); poate povesti intamplari trecute in mod coerent, isi poate exprima si justifica pe scurt parerile, si poate face fata majoritatii situatiilor care apar cand calatoreste intr-o zona anglofona. Se descurca fara ca interlocutorul sa fie nevoit sa vorbeasca „special" pentru el.
**Prag de intrare / iesire:**
- *Intrare (din A2):* vocabular cumulat ~1500-1750 cuvinte; controleaza prezentul simplu/continuu, past simple (verbe regulate + neregulate frecvente), viitor cu *going to*, comparative/superlative, cuantificatori de baza, *can/could*.
- *Iesire (spre B2):* vocabular cumulat **~2750-3250 cuvinte**; controleaza present perfect vs. past simple, past continuous, primul conditional, modale de obligatie/sfat, propozitii relative, baza discursului indirect si un set initial de phrasal verbs.
**Rezumat test de validare la intrare:** Candidatul trebuie sa demonstreze, in 15-20 min: (a) sa se prezinte si sa descrie rutina/trecutul recent in ≥8 propozitii corecte cu present simple + past simple; (b) sa inteleaga un dialog audio A2 (~1 min) cu ≥80% raspunsuri corecte; (c) sa produca 5 intrebari corecte (do/did/can); prag de promovare in B1: **≥70%**. Sub prag → recomandare de recapitulare A2.

### Module si Unitati (CUPRINS)

**Modulul 1 — Experiente & Povestiri** (past simple ↔ present perfect ↔ past continuous; a nara)
**Modulul 2 — Opinii, Sfaturi & Obligatii** (modale, relative, a-si argumenta parerea)
**Modulul 3 — Planuri, Calatorii & Raportare** (viitor, first conditional, discurs indirect, phrasal verbs)

| # | Unitate (tema) | Functii comunicative (CAN-DO) | Gramatica | Vocabular (tema / nr nou) | Fonetica RO | Obiectiv masurabil |
|---|---|---|---|---|---|---|
| **M1.1** | Life experiences — „Have you ever…?" | Pot intreba si spune ce experiente am trait de-a lungul vietii, fara sa precizez cand | Present perfect (ever/never, been/gone); participii trecute frecvente | Experiente de viata, activitati (călătorii, mancaruri, hobby-uri) / **130** | Terminatia *-ed* /t/–/d/–/ɪd/ (*worked, lived, wanted*); /h/ initial (*have, ever*) | Sustine un schimb de ≥6 replici cu „Have you ever…? — Yes, I have/No, never", ≥85% forme corecte de participiu; scor pronuntie *-ed* ≥80% |
| **M1.2** | News & recent changes — „What's happened?" | Pot da vesti recente si vorbi despre ce s-a schimbat, cu efect in prezent | Present perfect cu *just / already / yet / for / since* | Vesti, schimbari personale, stari / **120** | Contrast /ɪ/–/iː/ (*live–leave, since–seen*); accentul in *alREAdy* | Redacteaza si sustine oral un „update" de ≥5 propozitii folosind corect ≥4 din marcatorii just/already/yet/for/since (≥80% corecte) |
| **M1.3** | Telling a story — „What were you doing?" | Pot povesti o intamplare punand fundalul si actiunea principala | Past continuous vs. past simple (*while / when / as*) | Accidente, intamplari, emotii in naratiune / **125** | *th* /θ/–/ð/ (*thought, weather, then*); *was/were* slabite /wəz, wə/ | Nareaza oral o poveste de ≥8 propozitii cu ≥3 contraste past continuous/past simple corecte; scor /θ,ð/ ≥80% pe cuvintele-tinta |
| **M1.4** | Then vs. now — experiences of my life | Pot alege intre a spune *cand* s-a intamplat ceva si doar *ca* s-a intamplat | Present perfect **vs.** past simple (consolidare + *gone/been*) | Recapitulare tematica + biografii, etape de viata / **110** | Ritm si accent de fraza: silabe slabe (*have* /həv/, *for* /fə/) | La un test de discriminare de 12 itemi alege timpul corect ≥80%; produce un mini-interviu de ≥6 replici fara confuzie sistematica intre cele doua timpuri |
| **M2.1** | In my opinion — agreeing & disagreeing | Pot exprima, sustine si nuanta o parere; pot fi (partial) de acord | Verbe de opinie (*think/believe that…*); *so/neither do I*; *because/although* | Opinii, argumente, subiecte de societate simple / **135** | /v/ vs. /w/ (*believe–we, view–work*); accentul contrastiv | Intr-o discutie de 3 min sustine o opinie cu ≥2 argumente si reactioneaza la parerea partenerului cu ≥3 structuri de (de)acord corecte; /v–w/ ≥80% |
| **M2.2** | Giving advice — „You should…" | Pot cere si oferi sfaturi si sugestii intr-o problema cotidiana | Modale de sfat: *should / shouldn't / ought to / had better / why don't you…?* | Probleme & solutii, sanatate, viata de zi cu zi / **120** | *sh* /ʃ/ (*should*) vs. *ci/ce* romanesc; *-d* mut in *should/could* | Intr-un joc de rol „problema-sfat" ofera ≥4 sfaturi corecte cu ≥2 modale diferite; ≥80% forme corecte (fara *to* dupa *should*) |
| **M2.3** | Rules & obligations — must, have to, can't | Pot vorbi despre reguli, obligatii si interdictii (la scoala, munca, calatorie) | *must / mustn't / have to / don't have to / can't* (obligatie & interdictie) | Reguli, permisiuni, locuri publice, semne / **125** | Contrast /æ/–/e/ (*can–ten, have–head*); *have to* → /hæftə/ | Clasifica corect ≥10/12 situatii ca obligatie/interdictie/lipsa de obligatie; produce ≥6 reguli reale (ex. la aeroport) cu modalul potrivit ≥80% |
| **M2.4** | The person who… — describing with detail | Pot descrie oameni, locuri si lucruri adaugand informatie prin propozitii relative | Propozitii relative (*who / which / that / where / whose*), definitorii | Descrieri de persoane, locuri, obiecte / **115** | /r/ post-vocalic slab (non-rhotic) vs. *r* romanesc rulat; *th* in *that* | Combina 8 perechi de propozitii in relative corecte ≥85%; descrie oral o persoana/loc in ≥5 fraze cu ≥3 relative diferite |
| **M3.1** | Dreams & hopes — planning the future | Pot vorbi despre planuri, intentii, previziuni si sperante | Viitor: *will* (previziune/decizie de moment) vs. *going to* (plan); *might* (posibilitate) | Vise, obiective, planuri de viitor / **130** | *will* → contractie /aɪl, hiːl/; /ɪ/ in *will* vs. /iː/ | Prezinta un „plan de viitor" de ≥8 propozitii distingand corect will/going to in ≥80% din cazuri; foloseste *might* de ≥2 ori corect |
| **M3.2** | Travel situations — „If we miss the train…" | Pot rezolva situatii reale de calatorie si vorbi despre consecinte probabile | Primul conditional (*If + present, will…*); *when/as soon as/unless* | Calatorie: aeroport, hotel, transport, probleme / **140** | Ritmul lui *if*-clause; pauza intonationala intre clauze; /ə/ in *unless* | In 3 jocuri de rol de calatorie rezolva situatia si produce ≥4 propozitii conditionale corecte ≥80%; intonatie de clauza condusa acceptabila |
| **M3.3** | She said that… — reporting words | Pot raporta ce a spus sau a intrebat altcineva (baza discursului indirect) | Discurs indirect: *say/tell that…*, backshift de baza (present→past); intrebari raportate simple | Comunicare, mesaje, ce-a-zis-cineva / **120** | Reducerea lui *that* /ðət/; accent de fraza in propozitii lungi | Transforma corect ≥8/10 propozitii din vorbire directa in indirecta (backshift de baza); raporteaza oral un mini-dialog in ≥5 propozitii ≥75% |
| **M3.4** | Everyday phrasal verbs — „get up, look for, find out" | Pot intelege si folosi verbe frazale frecvente in vorbirea de zi cu zi | Introducere phrasal verbs (rutina, calatorie, comunicare); separabile vs. inseparabile de baza | Phrasal verbs uzuale (≥25 tinta) + recapitulare / **125** | Accent pe particula (*look UP, get ON*); legarea (*find_it_out*) | Foloseste corect ≥10 phrasal verbs frecvente intr-un text/dialog propriu; la test de potrivire sens-verb ≥80%; plasarea corecta a obiectului la cele separabile ≥75% |

*(11 unitati; **vocabular nou cumulat pe nivel ≈ 1435 cuvinte** peste intrarea A2 → total cumulat ~2950-3200, in tinta B1.)*

**Checkpoint-uri si Test final de nivel:**
- **Checkpoint 1 (dupa M1):** Nareaza o experienta trecuta in ≥10 propozitii, alegand corect present perfect / past simple / past continuous. Prag: ≥80% corectitudine gramaticala pe timpurile-tinta + scor pronuntie *-ed* si /θ,ð/ ≥80%.
- **Checkpoint 2 (dupa M2):** Discutie de opinie de 4 min: exprima o parere cu ≥2 argumente, ofera un sfat cu modal, formuleaza o regula si o descriere cu relativa. Prag: ≥75% precizie + fluenta fara pauze care blocheaza comunicarea.
- **Test final de nivel B1 (4 sectiuni, prag global ≥80%):**
  1. *Gramatica & vocabular* (scris, ~40 itemi): ≥80%.
  2. *Ascultare* (2 inregistrari B1, ~3 min total): ≥80% raspunsuri corecte.
  3. *Scriere* (email/poveste de 120-150 cuvinte): ≥80% pe grila (sarcina indeplinita, coerenta, acuratete, gama de structuri B1).
  4. *Vorbire* (interviu + joc de rol de calatorie, 8-10 min): ≥80% pe grila (fluenta, corectitudine pe structurile B1) **si** scor mediu de pronuntie ≥80% pe sunetele-problema pt romani (/θ,ð/, /v–w/, /iː–ɪ/, /æ–e/, *-ed*).
- **Criteriu de promovare la B2:** toate cele 4 sectiuni ≥80% **si** ambele checkpoint-uri trecute; altfel, plan de recuperare tintit pe modulul deficitar.

**Resurse din biblioteca EVA:**
- *Manuale OER / State Dept:* unitatile de nivel intermediar pentru textele-model (povestiri, dialoguri de calatorie, articole de opinie simple) si exercitiile de gramatica (present perfect, conditionale, relative, reported speech).
- *Corpus paralel RO-EN (Tatoeba, ~16.000 propozitii):* filtrare pe structurile-tinta (present perfect vs. past simple, past continuous, first conditional, modale, relative) pentru exercitii de traducere inversa, carduri SRS si banci de propozitii-model per unitate.
- *Audio MP3:* materiale de ascultare si **shadowing** pentru Faza 2 (pipeline de voce), cu segmente scurte per unitate; sursa pentru scorarea pronuntiei pe sunetele-problema.
- *Gramatica RO:* explicatiile din Faza 1 (in romana, cu „stingere" graduala spre finalul B1) — contrastive RO↔EN pentru timpuri, conditionale si discurs indirect.
- *Dictionar RO-EN:* alimenteaza listele de vocabular tematic (~120-140 cuvinte/unitate) si cardurile SRS din Faza 3.


## Nivel B2 — Upper-Intermediate (Utilizator independent, prag avansat: intelege idei complexe pe teme concrete si abstracte, interactioneaza cu fluenta si spontaneitate, argumenteaza un punct de vedere)

**Obiectiv global de nivel (CAN-DO):** Pot sustine o conversatie fluenta si spontana cu EVA pe subiecte abstracte (media, mediu, munca), pot argumenta si contra-argumenta un punct de vedere, pot povesti experiente cu nuante de timp si pot formula ipoteze despre prezent si trecut — cu suficienta acuratete cat sa nu impiedic comunicarea.

**Prag de intrare / iesire:**
- *Intrare (din B1):* vocabular cumulat ~2.900–3.100 cuvinte; controlul present perfect vs. past simple, first conditional, comparative, viitor (will/going to/present continuous), modale de baza, phrasal verbs frecvente.
- *Iesire (spre C1):* vocabular cumulat **~4.500–5.000 cuvinte**; control activ pe present perfect continuous, past perfect (continuous), toate conditionalele (2/3 + mixed), pasiv la toate timpurile, discurs conectat cu markeri, `used to`/`would`/`be used to`, phrasal verbs extinse, modale de deductie.

**Rezumat test de validare la intrare:** candidatul demonstreaza ca (a) distinge present perfect de past simple in ≥8/10 itemi, (b) formuleaza corect first conditional si comparative, (c) sustine 2 minute de conversatie ghidata cu EVA fara blocaje >5s, (d) scrie un paragraf de ~80 de cuvinte coerent. Prag de admitere in B2: **≥70%** cumulat.

### Module si Unitati (CUPRINS)

#### Modul B2.1 — Experiente, obiceiuri si povesti (reluare in spirala + extindere a timpurilor perfecte)

| # | Unitate (tema) | Functii comunicative (CAN-DO) | Gramatica | Vocabular (tema / nr) | Fonetica RO | Obiectiv masurabil |
|---|---|---|---|---|---|---|
| 1 | **Cat timp deja?** (rutina, stil de viata, sanatate) | Pot descrie o activitate in desfasurare si durata ei ("I've been learning…") | Present perfect continuous vs. present perfect simple; `for/since` | Rutine & wellbeing / **~150** | `/iː/` vs `/ɪ/` (*been/bin, live/leave*); forme slabe *have been* → /əvbɪn/ | Produce ≥8 enunturi corecte cu present perfect continuous in dialog cu EVA; scor pronuntie `/iː–ɪ/` **≥80%** pe lista tinta |
| 2 | **Povestea din spate** (amintiri, momente-cheie) | Pot povesti un eveniment din trecut ordonand actiunile in timp | Narrative tenses: past simple / past continuous / **past perfect (continuous)** | Naratiune personala / **~150** | Terminatii `-ed`: /t/–/d/–/ɪd/; accent pe cuvintele de continut | Povesteste oral o intamplare de ≥6 propozitii cu ≥3 timpuri corect articulate; **≥80%** acuratete la terminatiile `-ed` |
| 3 | **Cum eram vs. cum sunt** (schimbari, obiceiuri) | Pot contrasta obiceiuri din trecut cu prezentul si adaptarea la nou | `used to` / `would` (obiceiuri trecute) vs. `be/get used to` | Schimbare & adaptare / **~150** | `/juːst/` (*used to*) vs `/juːzd/`; connected speech *used-to* → /juːstə/ | Produce ≥6 contraste corecte trecut/prezent; distinge auditiv `/juːst–juːzd/` in **≥8/10** itemi |
| 4 | **Ce a spus, de fapt?** (relatii, neintelegeri) | Pot relata ce a spus/cerut/sfatuit altcineva | Reported speech extins; verbe de raportare (*claim, admit, suggest, deny*) | Comunicare & relatii / **~140** | Accentul verbelor de raportare; intonatie descendenta la afirmatii raportate | Reformuleaza corect ≥8 enunturi directe in vorbire indirecta; **≥75%** la testul de shift al timpurilor |

#### Modul B2.2 — Media, argumentare si idei abstracte

| # | Unitate (tema) | Functii comunicative (CAN-DO) | Gramatica | Vocabular (tema / nr) | Fonetica RO | Obiectiv masurabil |
|---|---|---|---|---|---|---|
| 5 | **Se stie ca…** (stiri, procese, obiecte) | Pot relata informatii cand agentul e necunoscut/neimportant | Pasiv la toate timpurile; `by`-agent; pasiv cu modale | Stiri & procese / **~150** | Forme slabe *was/were/been* → /wəz, wə, bɪn/; `/v/` vs `/w/` (*was–vas*) | Transforma ≥10 propozitii activ→pasiv corect; produce un buletin de stiri de ≥5 enunturi pasive, **≥80%** acuratete |
| 6 | **Filmul si recenzia** (media, film, cultura) | Pot recomanda si evalua un film/serial cu argumente | Reported speech aplicat la recenzii; `so/such`, adverbe de grad | Film & critica / **~160** | Accent de cuvant in adjective lungi (*unforgettable, predictable*); intonatie de opinie | Scrie o recenzie de ~120 de cuvinte cu ≥5 termeni de critica; sustine oral 90s de recomandare fara blocaje >5s |
| 7 | **Fir logic** (eseu, dezbatere de baza) | Pot structura un argument: introduc, contrastez, concluzionez | Conectori de discurs (*however, therefore, although, whereas, moreover, on the other hand*) | Argumentare & coeziune / **~150** | Schwa in conectori (*however* /haʊˈevə/, *therefore* /ˈðeəfɔː/); pauze-grup | Scrie un paragraf argumentativ de ~120 de cuvinte cu ≥5 conectori diferiti folositi corect; **≥80%** la exercitiul de coeziune |
| 8 | **Daca ar fi…** (dileme, subiecte abstracte) | Pot specula despre situatii ireale din prezent si da sfaturi | Second conditional; `unless`, `as long as`; `I wish + past` | Dileme & valori / **~150** | Contractia `I'd`; `/w/` in *would/won't*; forma slaba *would* → /wəd/ | Produce ≥6 propozitii corecte la second conditional intr-un dialog de dileme cu EVA; **≥80%** la testul de forma |

#### Modul B2.3 — Munca, mediu si scenarii ipotetice (integrare + productie extinsa)

| # | Unitate (tema) | Functii comunicative (CAN-DO) | Gramatica | Vocabular (tema / nr) | Fonetica RO | Obiectiv masurabil |
|---|---|---|---|---|---|---|
| 9 | **Regrete si consecinte** (decizii, film/viata) | Pot exprima regrete si analiza cauze din trecut | Third conditional; `should have + p.p.`; `I wish + past perfect` | Decizii & regrete / **~150** | `would have` → /ˈwʊdəv/ (capcana clasica RO); *should've/could've* | Produce ≥6 enunturi corecte la third conditional; pronunta `would/could/should have` redus in **≥8/10** itemi |
| 10 | **Cand trecutul intalneste prezentul** (mediu, cariera) | Pot lega o cauza trecuta de un rezultat prezent (si invers) | Mixed conditionals (3→2 si 2→3) | Mediu & sustenabilitate / **~160** | Connected speech in propozitii lungi; accentul frazei pe cuvintele de continut | Formuleaza corect ≥4 mixed conditionals in analiza unei probleme de mediu; **≥75%** la testul de potrivire cauza-efect |
| 11 | **La birou si dincolo de el** (munca, business) | Pot discuta sarcini, cariera si procese profesionale idiomatic | Phrasal verbs extinse (separabile/inseparabile) — munca/business | Munca & cariera / **~170** | Accent pe particula phrasal verbelor (*set ˈup, carry ˈout*); linking | Foloseste corect ≥12 phrasal verbs de business intr-un roleplay de interviu/reuniune cu EVA; **≥80%** la testul de sens |
| 12 | **Dezbaterea finala** (mediu vs. economie, argumentare) | Pot sustine si apara o pozitie, pot deduce si specula probabilitati | *Consolidare:* modale de deductie (*must/might/can't have*) + integrarea tuturor structurilor B2 | Recapitulare tematica (abstract/media/munca/mediu) / **~120** | Intonatie persuasiva; grupuri de gand & fluenta; forme slabe *must/might* | Sustine o dezbatere de 3–4 minute cu EVA argumentand + contra-argumentand, folosind ≥2 conditionale, ≥1 pasiv, ≥3 conectori; scor de fluenta **≥80** (fara blocaje >5s) |

**Checkpoint-uri si Test final de nivel:**
- **Checkpoint 1 (dupa Modul B2.1):** ≥75% la test de timpuri (perfect continuous, narative, `used to`) + relatare orala de 2 min a unei experiente personale.
- **Checkpoint 2 (dupa Modul B2.2):** eseu argumentativ de ~150 de cuvinte cu ≥6 conectori si ≥2 second conditionals; **≥75%**.
- **Checkpoint 3 (dupa Modul B2.3):** roleplay profesional + dezbatere pe mediu; scor de fluenta ≥80.
- **Test final de nivel (promovare spre C1):** (a) gramatica integrata — **≥80%** (pasiv, 2/3 + mixed conditionals, phrasal verbs, discurs); (b) scriere argumentativa ~180 de cuvinte, coerenta si registru adecvat, evaluata **≥80%**; (c) proba orala cu EVA de 5 min pe subiect abstract — scor de pronuntie **≥80** pe sunetele tinta (`/θ–ð/`, `/iː–ɪ/`, `would-have`), fluenta **≥80**, fara erori care blocheaza sensul; (d) intelegere audio **≥80%**. Prag global de promovare: **≥80%** cumulat + toate cele 3 checkpoint-uri trecute.

**Resurse din biblioteca EVA:**
- **Gramatica-nucleu:** *Verb Tenses for EAP* (folderul `03. Intermediar B1-B2`) — coloana vertebrala pentru Unitatile 1, 2, 5, 9, 10 (timpuri perfecte, pasiv, conditionale).
- **Explicatii in romana & contrast RO-EN:** *FSI Romanian Grammar* si *DLI Vol 01* (`05. Dictionare si Gramatica`) — pentru punti de contrast la `used to`/aspect, pasiv si topica, plus dictionar RO-EN pentru vocabularul tematic.
- **Input conversational & propozitii-model:** cele **16.297 de propozitii paralele Tatoeba** (`04. Resurse Romana-Engleza`) — sursa pentru carduri SRS, exercitii de transformare (activ↔pasiv, direct↔indirect) si banca de enunturi tinta pe teme (mediu, munca, media).
- **Dialog & registru:** manualele intermediar-avansat din `02. Incepator avansat - Intermediar A2-B1` (*Green Tea*, *Evergreen Intermediate*, *PDX Journeys*) — reciclate in spirala pentru shadowing si roleplay la Unitatile 4, 6, 11.
- **Audio (la cerere):** pachetele MP3 State Dept si Peace Corps (nedescarcate momentan) — de activat pentru fazele de ascultare/pronuntie ale pipeline-ului (Faza 2). *Lacuna cunoscuta:* nu exista manual OER dedicat vorbitorilor de romana, asa ca focusul fonetic RO (th, v/w, i:/ɪ, æ/e, `would-have`) e sustinut prin regulile din memoria proiectului, nu dintr-un manual.


## Nivel C1 — Advanced (Utilizator experimentat: se exprimă fluent și spontan, folosește limba flexibil și eficient în scopuri sociale, academice și profesionale)

**Obiectiv global de nivel (CAN-DO):** La sfârșitul nivelului, cursantul poate înțelege o gamă largă de texte lungi și pretențioase, sesizând sensuri implicite; se poate exprima fluent și spontan, fără a căuta prea evident cuvintele; poate folosi limba în mod suplu și eficient în relații sociale, academice și profesionale; poate produce un text clar, bine structurat și detaliat pe subiecte complexe, demonstrând control asupra tiparelor de organizare, a conectorilor și a coeziunii. Prag operațional cu EVA: susține o dezbatere de 8-10 minute pe o temă abstractă și scrie un eseu argumentativ de 350-450 de cuvinte cu poziție clară, contraargument și concesie.

**Prag de intrare / ieșire:**
- *Intrare (nivel B2 consolidat):* vocabular cumulat ~5.000-5.500 de cuvinte; control stabil al timpurilor verbale (inclusiv perfect continuu și forme de viitor), diateza pasivă în toate timpurile, vorbire indirectă, propoziții relative definite/nedefinite, structuri modale de deducție și modale perfecte, phrasal verbs frecvente, conectori de bază.
- *Ieșire (spre C2):* vocabular cumulat ~8.000 de cuvinte (colocații și idiomuri incluse); control al inversiunii, structurilor cleft, condiționalelor mixte și inversate, nominalizării, modalității nuanțate, hedging-ului academic și al comutării de registru; coeziune și fluență la nivel de discurs, nu doar de propoziție.

**Rezumat test de validare la intrare:** Cursantul trebuie să demonstreze că (1) înțelege un text autentic B2 de ~500 de cuvinte și extrage 3 idei implicite (nu doar explicite); (2) susține o conversație spontană de 5 minute cu EVA fără sprijin scris, corectându-se singur; (3) scrie 200 de cuvinte coerente pe o temă abstractă folosind corect minimum 4 conectori și 2 timpuri perfecte; (4) obține ≥70% la un test-grilă de gramatică B2 (pasiv, reported speech, modale perfecte, relative). Prag de admitere în C1: ≥75% cumulat.

### Module și Unități (CUPRINS)

#### Modul 1 — Precizie și Nuanță (structuri emfatice, condiționale avansate, colocații)

| # | Unitate (temă) | Funcții comunicative (CAN-DO) | Gramatică | Vocabular (temă / nr) | Fonetică RO | Obiectiv măsurabil |
|---|---|---|---|---|---|---|
| 1 | **Inversiune și emfază** (a atrage atenția, a sublinia) | Pot scoate în evidență o idee-cheie și pot da greutate retorică unei afirmații | Inversiune după adverbe negative/restrictive (*Never had I…, Not only… but also…, Hardly… when…*); fronting | Adverbe de accentuare și structurare a discursului (temă: retorică) / **50** | Ritm stress-timed vs. silabic RO; accent de frază pe elementul emfatic | Produce ≥6 propoziții cu inversiune negativă corectă în context (≥5/6 corecte) și le rostește cu accentul de frază corect (scor ritm ≥80) |
| 2 | **Cleft sentences** (a clarifica, a corecta o presupunere) | Pot reformula pentru a evidenția cine/ce/de ce contează cu adevărat | *It-cleft* (*It was X that…*), *wh-cleft* (*What I need is…*), *all-cleft* | Vocabular de nuanțare și corectare (temă: clarificare) / **45** | Intonație contrastivă (fall pe elementul focalizat); reducerea formelor slabe | Transformă 8 propoziții neutre în cleft adecvat contextului (≥7/8 corecte) și marchează prin intonație focusul (≥80% enunțuri corect accentuate) |
| 3 | **Condiționale avansate & ipotetic** (a specula, a regreta, a avertiza) | Pot exprima ipoteze fine, regrete și consecințe alternative | Condiționale mixte; inversiune condițională (*Had I known…, Were it not for…*); *wish/if only/it's time/would rather* | Verbe de speculație și consecință (temă: cauzalitate) / **50** | *Would/had* în forme slabe și contractate; linking în grupuri consonantice | Scrie un paragraf de 120 de cuvinte cu ≥3 tipuri de condițional (inclusiv 1 mixt și 1 inversat) fără eroare de structură; ≥90% acuratețe |
| 4 | **Colocații & precizie lexicală** (a alege cuvântul exact) | Pot înlocui vocabularul general cu combinații naturale și precise | Colocații verb+substantiv, adjectiv+substantiv, adverb+adjectiv; *delexical verbs* (*make/do/take/have*) | Colocații academice și cotidiene (temă: precizie lexicală) / **60** | Accent de cuvânt în familii lexicale (*PHOtograph → phoTOGraphy*); schwa în silabe neaccentuate | Completează un text-cloze de 25 de colocații cu ≥80% corect și reformulează 5 propoziții „traduse din RO" în engleză idiomatică (≥4/5 naturale) |

#### Modul 2 — Registru și Discurs (idiomuri, argumentare, sinteză)

| # | Unitate (temă) | Funcții comunicative (CAN-DO) | Gramatică | Vocabular (temă / nr) | Fonetică RO | Obiectiv măsurabil |
|---|---|---|---|---|---|---|
| 5 | **Registru & diplomație** (a atenua, a fi tactic) | Pot comuta între formal, neutru și informal și pot formula critici în mod diplomatic | Hedging (*tend to, seem to, it could be argued*); *softeners*; distanțare cu modale și pasiv impersonal | Limbaj formal vs. informal, expresii de atenuare (temă: registru) / **55** | Intonație descendent-ascendentă pentru politețe/rezervă; ton nuanțat | Rescrie 6 enunțuri directe în variantă diplomatică adecvată registrului (≥5/6) și livrează 3 oral cu intonație de politețe corectă (≥80%) |
| 6 | **Idiomuri & limbaj figurat** (a colora exprimarea) | Pot înțelege și folosi idiomuri frecvente și metafore uzuale fără a suna forțat | Idiomuri fixe și semi-fixe; metafore conceptuale; *binomials* (*by and large, sooner or later*) | Idiomuri tematice: muncă, timp, emoții (temă: expresivitate) / **50** | Accent și ritm în expresii fixe (chunk-uri prozodice); linking intern | Recunoaște sensul a 20 de idiomuri în context (≥85%) și integrează corect 6 într-o conversație cu EVA (≥5 folosite adecvat registrului) |
| 7 | **Argumentare complexă** (a construi o poziție) | Pot dezvolta un argument sistematic, cu premise, contraargument și concesie | Conectori de discurs (*nevertheless, whereas, thereby, insofar as*); subordonare multiplă; concesive | Vocabular de argumentare și evaluare (temă: dezbatere) / **55** | Grupuri tonale și pauze de sens la fraze lungi; accent pe conectori | Construiește oral un argument de 3 minute cu structură teză-contraargument-concesie-concluzie (rubrică ≥80%, minim 5 conectori distincți) |
| 8 | **Sinteza textelor lungi** (a rezuma, a parafraza) | Pot condensa un text pretențios păstrând ideile-cheie și pot parafraza fără a copia | Nominalizare (*to decide → the decision to…*); parafrază; vorbire indirectă complexă | Verbe de raportare și sinteză (temă: academic) / **50** | Reducerea vocalică în cuvinte lungi; deplasarea accentului la nominalizare | Rezumă un text de 500 de cuvinte în 100 de cuvinte parafrazate (≥80% idei-cheie acoperite, <15% suprapunere textuală) |

#### Modul 3 — Performanță și Fluență (aplicare profesională, academică, orală)

| # | Unitate (temă) | Funcții comunicative (CAN-DO) | Gramatică | Vocabular (temă / nr) | Fonetică RO | Obiectiv măsurabil |
|---|---|---|---|---|---|---|
| 9 | **Comunicare profesională** (email, negociere) | Pot redacta corespondență formală și pot negocia clar și politicos | Structuri de solicitare/propunere; condiționale de negociere; pasiv de distanțare profesională | Vocabular de business și corespondență (temă: profesional) / **55** | Intonație de propunere vs. cerere; accent contrastiv în negociere | Redactează un email formal de 150 de cuvinte (registru și structură ≥80%) și duce o negociere-simulare cu EVA atingând 2 din 3 obiective |
| 10 | **Nuanțe de atitudine** (a comenta, a evalua) | Pot exprima grade fine de certitudine, atitudine și evaluare | Modalitate avansată (*may well, might as well, needn't have*); adverbe de comentariu (*arguably, presumably, admittedly*) | Adverbe și expresii de atitudine (temă: evaluare) / **45** | Intonație pentru ironie/rezervă/entuziasm; accent pe adverbul-comentariu | Marchează corect atitudinea (certitudine/îndoială/concesie) în 8 enunțuri (≥7/8) și o exprimă oral cu intonația potrivită (≥80%) |
| 11 | **Engleză academică scrisă** (eseu argumentativ) | Pot scrie un eseu structurat, coerent și obiectiv pe o temă abstractă | Coeziune inter-paragraf; *it/there*-cleft de introducere; structuri impersonale; referire anaforică | Vocabular academic (Academic Word List) (temă: academic) / **60** | Prozodie de citire cu voce tare a textului academic (grupuri de sens) | Scrie un eseu de 350-450 de cuvinte cu introducere-corp-concluzie, ≥6 conectori distincți și registru academic constant (rubrică ≥80%) |
| 12 | **Dezbatere & prezentare orală** (a susține spontan) | Pot prezenta fluent și pot reacționa spontan la contraargumente | Recapitulare spiralată: inversiune, cleft, condiționale, hedging integrate în vorbire spontană | Vocabular de prezentare și replică (temă: oratorie) / **45** | Fluență și *connected speech* la debit natural; auto-corectare prozodică | Susține o prezentare de 4 minute + 3 minute Q&A cu EVA la ≥120 cuvinte/minut, <4 pauze de căutare a cuvântului și scor de pronunție global ≥85 |

**Checkpoint-uri și Test final de nivel (criterii măsurabile pentru promovarea la C2):**
- *Checkpoint 1 (după Modul 1):* ≥80% la testul de structuri emfatice și condiționale + producerea corectă a 3 propoziții cleft/inversate la vorbire spontană.
- *Checkpoint 2 (după Modul 2):* rezumat parafrazat validat (≥80% idei-cheie) + argument oral de 3 minute cu rubrică de coeziune ≥80%.
- *Test final de nivel (4 componente):*
  1. **Receptare:** înțelegerea unui text pretențios de ~700 de cuvinte, inclusiv 3 sensuri implicite → ≥80%.
  2. **Producere scrisă:** eseu argumentativ de 350-450 de cuvinte → rubrică (sarcină, coerență, gramatică, lexic, registru) ≥80%.
  3. **Producere orală:** dezbatere/prezentare de 8-10 minute → fluență ≥120 c/min, pronunție globală ≥85, min. 5 structuri C1 folosite corect.
  4. **Gramatică & lexic:** test integrat (inversiune, cleft, condiționale mixte/inversate, colocații, idiomuri, registru) → ≥80%.
- *Prag global de promovare la C2:* ≥80% media ponderată, fără componentă sub 75%; vocabular cumulat verificat ≥8.000 de cuvinte.

**Resurse din biblioteca EVA:**
- *Gramatică & structuri:* `03. Intermediar B1-B2/Verb Tenses for EAP` (bază academică de timpuri și nominalizare, extinsă spre C1); `05. Dictionare si Gramatica/FSI Romanian Grammar` (contrastiv RO-EN pentru fonetică și topică — sursă a focusului „Fonetică RO").
- *Propoziții & colocații:* `04. Resurse Romana-Engleza/Tatoeba` (16.297 propoziții paralele RO-EN — se filtrează perechile lungi/complexe pentru colocații, idiomuri, structuri emfatice și cardurile SRS de nivel).
- *Lexic & registru:* `05. Dictionare si Gramatica` (dicționare domeniu public) + generarea EVA de liste tematice pe Academic Word List; `02. Incepator avansat/Green Tea` pentru texte de lectură extinse reciclate ascendent.
- *Audio & pronunție:* extrasele audio State Dept (nedescărcate, la cerere) pentru shadowing și prozodie; pentru materialul de nivel C1 se completează cu texte autentice externe și conținut generat de EVA.
- *Notă de acoperire:* biblioteca OER actuală se oprește practic la B2; nivelul C1 se alimentează preponderent din **Tatoeba (segmente dificile) + Verb Tenses for EAP + conținut generat de EVA + texte autentice academice/profesionale**, deoarece nu există în bibliotecă un manual OER gratuit dedicat C1 pentru vorbitori de română.


## Nivel C2 — Măiestrie (Proficiency) (utilizatorul experimentat: înțelege practic tot, se exprimă spontan, fluent și precis, cu nuanțe fine de sens chiar și în situații complexe)

**Obiectiv global de nivel (CAN-DO):** La final, cursantul poate înțelege fără efort practic orice text sau discurs oral (inclusiv rapid, idiomatic, aluziv sau ironic), poate rezuma și reconstrui argumente din surse diverse într-o prezentare coerentă, și se poate exprima spontan, foarte fluent și cu mare precizie, diferențiind nuanțe subtile de sens chiar în subiecte complexe — la nivelul unui vorbitor nativ educat.

**Prag de intrare / ieșire:**
- *Intrare (venind din C1):* vocabular activ cumulat ~10.000–12.000 de unități; stăpânire completă a timpurilor, condiționalelor, modalelor, structurilor pasive/cauzative, relativelor și a discursului raportat; fluență cu ezitări rare; registre formal/informal deja diferențiate.
- *Ieșire (C2 atins):* vocabular activ ~14.000–16.000+, cu control fin al conotației, colocației și idiomaticului; gramatică cvasi-nativă (inversiune, fronting, cleft, elipsă stilistică, subtilități aspectuale); pronunție cu speech connectat natural, prozodie pragmatică (ironie, accent emfatic) și accent aproape neutru.
- *Explicația de gramatică în română:* aproape stinsă — apare doar ca notă-fulger de contrast RO↔EN pentru capcane reziduale; studiul se face predominant în engleză, prin observare de corpus și inducție.

**Rezumat test de validare la intrare:** Candidatul trebuie să demonstreze: (1) înțelegere a unui text de opinie/literar dens (≥90% la 10 întrebări de inferență și ton); (2) producție orală spontană de 4–5 minute pe temă abstractă, fluentă, cu ≤2 erori care afectează sensul; (3) reformulare a aceleiași idei în 3 registre (formal / neutru / colocvial); (4) recunoașterea a ≥8/10 idiomuri și colocații C1. Sub prag → recomandare de consolidare C1.

### Module și Unități (CUPRINS)

Progresie în spirală: fiecare modul reia arii din C1 (registru, idiom, retorică) și le duce la finețea nativă — de la *precizia cuvântului* (Modul A) → *stilul și jocul cu limba* (Modul B) → *spontaneitatea și specializarea* (Modul C).

#### Modul A — Precizie, conotație și registru (Unitățile 1–4)
*Focus: alegi cuvântul exact, nu doar corect.*

| # | Unitate (temă) | Funcții comunicative (CAN-DO) | Gramatică | Vocabular (temă / nr) | Fonetica RO | Obiectiv măsurabil |
|---|---|---|---|---|---|---|
| 1 | Conotație și nuanță lexicală (cvasi-sinonime, shades of meaning) | Pot alege între cvasi-sinonime în funcție de conotație (ex. *slim/skinny/slender*, *frugal/stingy*) și pot justifica alegerea | Sufixe evaluative, gradarea adjectivelor cu intensifiers fini (*utterly, faintly, borderline*) | Perechi/triade de cvasi-sinonime, conotație pozitivă–neutră–negativă / 70 | Weak forms și schwa în cuvinte funcționale (/ə/ în *of, to, that*) — eliminarea vocalei "pline" românești | Clasifică 20/20 cvasi-sinonime pe axa conotației (+/0/–) și produce 8 propoziții unde alegerea lexicală schimbă corect tonul (≥90% acuratețe evaluată) |
| 2 | Colocații și idiomuri avansate (full idiomatic command) | Pot vorbi natural folosind colocații și idiomuri fără a suna „de manual"; pot detecta un idiom folosit greșit | Verbe cu prepoziții idiomatice, phrasal verbs cu sens figurat, colocații delexicale (*make/do/take/have*) | Idiomuri tematice + colocații frecvente (business, emoții, timp) / 80 | Elizie și asimilare în lanțul vorbirii (*next door → nex(t)door*, *would you → wouldja*) | Într-un monolog de 3 min, folosește ≥12 colocații/idiomuri corecte și naturale; ≤1 utilizare forțată (evaluare nativă ≥90%) |
| 3 | Registru și adecvare stilistică (formal ↔ slang) | Pot comuta registrul în timp real după interlocutor și context (birocratic, academic, colocvial, argou) | Nominalizare vs. verbe active; contracții, ellipsis colocvial, hedging formal | Marcatori de registru, jargon vs. plain English, argou controlat / 65 | Ritm stress-timed: comprimarea silabelor neaccentuate, evitarea „syllable-timing" românesc | Reformulează același mesaj în 3 registre distincte, corect marcate stilistic în ≥90% din alegeri; niciun „amestec" de registru nedorit |
| 4 | Gramatica de precizie: inversiune, fronting, cleft, elipsă emfatică | Pot da emfază și focus informațional prin ordine sintactică marcată, ca un nativ educat | Inversiune negativă (*Not only… , Hardly… when*), it-/wh-cleft, fronting, elipsă stilistică | Conective de discurs avansate, marcatori de focus / 55 | Prozodie de focus: nucleul tonic pe elementul contrastat; intonație descendentă/ascendentă emfatică | Transformă 12/12 propoziții neutre în variante emfatice corecte (inversiune/cleft) și le rostește cu accentul nuclear plasat corect (≥90%) |

#### Modul B — Stilistică, retorică și umor (Unitățile 5–8)
*Focus: nu doar ce spui, ci cum și cu ce efect — ironie, imagine, persuasiune.*

| # | Unitate (temă) | Funcții comunicative (CAN-DO) | Gramatică | Vocabular (temă / nr) | Fonetica RO | Obiectiv măsurabil |
|---|---|---|---|---|---|---|
| 5 | Ironie, sarcasm, understatement (umor britanic) | Pot recunoaște și produce ironie, understatement și sarcasm, decodând sensul opus celui literal | Tag questions retorice, structuri concesive, modale de distanțare (*I dare say, one might think*) | Lexic al ironiei/understatement (*hardly ideal, not exactly thrilled*) / 55 | Intonație ironică (contur exagerat/plat), pauze semnificative, accentuare „falsă" | Identifică ironia în 9/10 replici audio și produce 6 replici ironice cu efect corect recunoscut de evaluator nativ (≥85%) |
| 6 | Jocuri de cuvinte, puns, metaforă vie | Pot aprecia și crea puns, metafore și ambiguități intenționate; pot explica de ce „prinde" o glumă | Ambiguitate sintactică/lexicală, metaforă conceptuală, comparație extinsă | Câmpuri metaforice, omofone/omonime, wordplay / 50 | Perechi minimale reziduale RO (/iː/–/ɪ/, /æ/–/e/, /θ/–/s/) exploatate în puns; discriminare fină | Explică mecanismul a 8/10 puns și creează 4 jocuri de cuvinte funcționale; scor de discriminare a perechilor minimale ≥90 |
| 7 | Retorică și persuasiune (argumentare & debate) | Pot construi și susține un argument persuasiv, anticipând și demontând contraargumente | Structuri concesive/adversative, condiționale retorice, paralelism, tricolon | Conective argumentative, verbe de poziționare (*contend, concede, refute*) / 60 | Prozodie persuasivă: ritm în trei, accent de listă, controlul volumului și al pauzei | Susține un discurs argumentativ de 4 min cu teză + 3 argumente + respingere; ≥90% coeziune și ≥85 scor de prozodie persuasivă |
| 8 | Analiză literară și stilistică textuală | Pot analiza tonul, vocea și efectele stilistice ale unui text și pot imita un stil dat | Aspect și timpuri în narațiune, voce pasivă stilistică, discurs indirect liber | Terminologie stilistică, ton/voce/mood / 55 | Lectură expresivă: frazare, enjambment oral, redarea vocii personajelor | Analizează 2 pasaje (ton + 3 procedee identificate corect) și produce un paragraf-pastișă recunoscut ca imitând stilul-țintă (evaluare ≥85%) |

#### Modul C — Fluență cvasi-nativă și specializare (Unitățile 9–12)
*Focus: performezi spontan, în domenii reale, la nivel de nativ educat.*

| # | Unitate (temă) | Funcții comunicative (CAN-DO) | Gramatică | Vocabular (temă / nr) | Fonetica RO | Obiectiv măsurabil |
|---|---|---|---|---|---|---|
| 9 | Discurs academic și scriere de cercetare/eseu | Pot scrie un eseu argumentativ/academic coerent și pot susține o prezentare academică | Nominalizare densă, hedging & boosting, cohesion devices, citare integrată | Lexic academic (AWL avansat), verbe de raportare / 70 | Prozodie de prezentare: chunking, semnalizare intonațională a structurii | Produce un eseu de 400–500 cuvinte cu teză clară și ≥90% acuratețe gramaticală/coeziune (grilă academică) + susținere orală de 5 min |
| 10 | Engleză profesională de specialitate (negociere, prezentări high-stakes) | Pot negocia, prezenta și gestiona întrebări dificile într-un context profesional real | Diplomatic language, conditionals de negociere, modale de tact | Jargon de domeniu (la alegere) + limbaj diplomatic / 70 | Weak forms + linking sub presiune, control al ritmului la stres, accent neutralizat | Simulare de negociere/prezentare de 6 min cu Q&A: atinge ≥85% obiective comunicative și ≤2 scăpări de registru; scor pronunție ≥90 |
| 11 | Spontaneitate: dezbatere live, improvizație, reparație conversațională | Pot participa fără efort la o conversație rapidă/în grup, pot repara elegant, glumi și schimba subiectul | Discourse markers spontani, elipsă, backchanneling, structuri de reparație (*what I meant was…*) | Fillers naturali, marcatori conversaționali, small talk avansat / 55 | Fluență în timp real: rata de vorbire nativă, reducerea pauzelor pline, connected speech automat | Dezbatere live de 8 min în grup: fluență ≥130 cuvinte/min utile, ≤3 ezitări perturbatoare, ≥4 reparații/schimbări de tur reușite |
| 12 | Capstone — Proiect integrat (Proficiency Showcase) | Pot livra un „număr magistral": prezentare + Q&A + text scris, integrând tot ce știu, adaptat publicului | Sinteză a tuturor ariilor C2 (recap în spirală A+B+C) | Consolidare tematică liberă (aleasă de cursant) / recap 60 | Sinteză fonetică: accent aproape neutru, prozodie pragmatică completă, gestionarea accentelor la ascultare | Livrează proiect final (eseu ≥500 cuv. + prezentare 8–10 min + Q&A): ≥90% la grila integrată C2 (conținut, limbă, pronunție, adecvare) = descriptor C2 atins |

**Checkpoint-uri și Test final de nivel:**
- **Checkpoint A (după U4):** test de precizie lexicală și gramatică emfatică — prag ≥85% (conotație, colocație, inversiune/cleft).
- **Checkpoint B (după U8):** probă de stilistică & retorică — recunoașterea ironiei/procedeelor ≥85% + producție persuasivă cu prozodie ≥85.
- **Checkpoint C (după U11):** probă de spontaneitate — dezbatere live evaluată la fluență, reparație și registru ≥85%.
- **Test final de nivel (integrat):** patru componente — (1) *Reading/Listening* pe text dens și audio idiomatic/ironic ≥90%; (2) *Writing* eseu academic/creativ ≥90% pe grilă; (3) *Speaking* prezentare + Q&A spontan, fluență cvasi-nativă ≥85%; (4) *Pronunție & prozodie* scor global ≥90 (weak forms, connected speech, intonație pragmatică). Promovare / certificare C2 = medie ≥90% și niciun modul sub 85%.

**Resurse din biblioteca EVA:**
- **Corpus paralel Tatoeba (~16.000 propoziții RO-EN):** exploatat la C2 pentru *mining de nuanță* — perechi cvasi-sinonime, colocații și contraste de registru; sursă pentru carduri SRS de finețe (U1–U3) și pentru detectarea capcanelor de traducere RO→EN.
- **Manualele OER de engleză (State Dept / OER avansate):** pasajele de nivel superior alimentează Modulul A–B (texte de opinie, analiză stilistică U8, discurs academic U9); explicațiile de gramatică se folosesc doar ca referință-fulger, nu ca predare.
- **Audio MP3 din bibliotecă + shadowing:** materialul pentru Faza 2 (pipeline de voce) — weak forms, connected speech, intonație ironică/persuasivă (U5, U7, U10); shadowing pe înregistrări la ritm nativ pentru U11–U12.
- **Gramatici de referință:** consultate punctual pentru inversiune, cleft, aspect stilistic (U4, U8) — auto-serviciu, în engleză.
- **Dicționar RO-EN + note de conotație:** suport pentru dezambiguizarea cvasi-sinonimelor și a idiomurilor (U1–U2), cu marcarea registrului.
- **Completare cu material autentic (recomandat la C2):** editoriale, literatură scurtă, podcast-uri și stand-up — pentru idiomaticul viu, umor și accente variate pe care corpusul OER nu le acoperă integral; folosite ca input pentru U5–U6 și pentru comprehensiunea accentelor din testul final.


---

# 🛠️ Partea a IV-a — Procesul de autorare (cum aplicăm șablonul)

Acest capitol transformă arhitectura în *linie de producție*. Aplicat pe cuprinsul din Partea a III-a, produce, în ordine, cele trei straturi ale cursului.

## 7. Cele trei straturi de producție ale proiectului

| Strat | Ce producem | Corespunde | Când |
|---|---|---|---|
| **STRAT 1 — Componenta scrisă** | Faza 1 a **fiecărei** unități din toate nivelurile: texte, dialoguri, note de gramatică (RO), liste de vocabular, exerciții + barem | Faza 1 | **ACUM** (obiectivul curent) |
| **STRAT 2 — Pipeline (voce & conversație)** | Scripturi de conversație EVA, prompt-uri de tutore pe unitate, drill-uri de pronunție, mapare audio/shadowing | Faza 2 | După Strat 1 |
| **STRAT 3 — Consolidare & evaluare** | Seturi SRS, scenarii task-based, teste de unitate/checkpoint/final, rubrici | Faza 3 | După Strat 2 |

> „Sa obținem la final componenta scrisă a proiectului" = livrarea completă a **Stratului 1** pentru toate unitățile. „Apoi tot restul" = Straturile 2 și 3.

## 8. Bucla de autorare a unei unități (Stratul 1)

Pentru fiecare intrare din cuprins se rulează aceiași 6 pași:

1. **Extrage specificația** din cuprins (temă, funcții, gramatică, vocabular-țintă, fonetică, obiectiv măsurabil).
2. **Selectează resursele** din biblioteca EVA (manual + pagini, propoziții Tatoeba filtrate pe temă/CEFR, audio, dicționar) — ancora anti-halucinație.
3. **Redactează componenta scrisă** completând §① – §⑦ din șablon: textul/dialogul, nota de gramatică în română, lista de vocabular, exercițiile, baremul, sarcina finală.
4. **Verifică nivelul** — vocabular și structuri în banda CEFR a nivelului (control automat: listă de vocabular permis + structuri gramaticale introduse până la acea unitate).
5. **Definește pragurile măsurabile** (§⑤) și itemii de evaluare (§⑥).
6. **Revizuire & Definition of Done** (vezi §10) → unitatea trece în „scris: gata".

## 9. Ordinea de producție (sequencing)

- **Pe orizontală, per strat:** întâi TOATĂ componenta scrisă (Strat 1) a unui nivel, apoi pipeline, apoi restul — astfel corectăm coerența înainte de a investi în voce/audio.
- **Prioritizarea nivelurilor:** recomandat **A1 → A2 → B1** primele (acoperă majoritatea publicului-țintă adult și validează formatul), apoi B2 → C1 → C2.
- **Unitate-pilot:** `A1-U1` (deja lucrată în Partea I) e referința de calitate; primele 3 unități se autorează manual, apoi se accelerează.
- **Autorare asistată:** draft generat cu LLM din specificația de cuprins + resurse (RAG pe bibliotecă) → **revizuire umană obligatorie** → aprobare.

## 10. Definition of Done — componenta scrisă a unei unități

O unitate e „scris: gata" când:
- [ ] Toate cele 7 secțiuni ale șablonului sunt completate.
- [ ] Obiectivele sunt CAN-DO CEFR **cu criteriu măsurabil** fiecare.
- [ ] Vocabularul respectă ținta numerică și banda CEFR; structurile gramaticale nu depășesc nivelul.
- [ ] Există text/dialog + notă de gramatică (RO) + ≥5 exerciții + barem.
- [ ] Rezultatele măsurabile (§⑤) au praguri numerice.
- [ ] Resursele din bibliotecă sunt citate (fără conținut inventat).
- [ ] Revizuit lingvistic (corectitudine + registru + ton prietenos).

## 11. Modelul de conținut (cum consumă aplicația materialul scris)

Fiecare unitate autorată se structurează ca date (pregătit pentru Supabase/Postgres), nu doar ca text:
```
unit(id, level, module, code, title, theme, cefr_sublevel, duration_min)
objectives(unit_id, can_do, criterion, threshold)
content(unit_id, text, grammar_note_ro, functions[])
vocab(unit_id, en, ro, cefr, audio_url, phonetic_focus)
exercises(unit_id, type, prompt, answer, points)
assessment(unit_id, items[], pass_threshold)
eva_task(unit_id, scenario, rubric)          ← Stratul 2
srs_seed(unit_id, sentence_ids[])            ← Stratul 3
```
Astfel, textul scris devine direct lecție interactivă în aplicație, iar Straturile 2–3 se atașează pe aceeași structură.

## 12. Metrici de calitate ale curriculumului (nu doar ale cursantului)

- **Acoperire CEFR:** % din descriptorii CAN-DO ai nivelului mapați pe cel puțin o unitate (țintă 100%).
- **Aliniere de nivel:** % din vocabular/structuri în banda corectă (țintă ≥95%).
- **Măsurabilitate:** % din obiective cu criteriu numeric (țintă 100%).
- **Ancorare în bibliotecă:** % din unități cu resurse citate (țintă 100%).

## 13. Pașii următori imediați (foaia de parcurs a scrierii)

1. **Validează** acest document programatic + cuprinsul propus (Partea a III-a).
2. **Autorează unitățile-pilot** `A1-U1 → A1-U3` complet (Strat 1), ca etalon de calitate.
3. **Rulează producția Stratului 1** nivel cu nivel (A1→C2), pe bucla din §8, cu revizuire umană.
4. La final Strat 1 = **componenta scrisă a proiectului** livrată. Apoi Straturile 2 (pipeline) și 3 (consolidare).

---

*Document programatic EVA — v1. Ancorat pe scara globală CEFR (reprodusă de British Council România) și pe biblioteca de conținut EVA (`Z:\02. EVA - Learn English with EVA`). Se aplică identic la toate cele 6 niveluri.*
