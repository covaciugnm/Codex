# 🗣️ EVA — Plan de produs
### Aplicație de învățare a englezei pentru vorbitori de română, bazată pe conversație și ecran interactiv

*Versiune plan: 3 august 2026. Bazat pe cercetare de piață, tehnologică și pedagogică (surse citate la final).*

---

## 1. Viziune și poziționare

> **„EVA — vorbește engleză fără frică."**
> Un tutore AI *conversation-first* care te învață engleza **pornind de la limba ta**, cu răbdare infinită, corectare blândă și feedback real de pronunție.

**Problema:** aplicațiile globale (Duolingo, Speak, ELSA, Babbel) te învață engleză *în engleză*. Pentru un român începător care se blochează exact la **vorbit**, lipsa sprijinului în limba maternă și tonul fie superficial-gamificat, fie corporate-rece, lasă un gol.

**Piața românească este practic goală:** nu există nicio aplicație conversațională AI dedicată vorbitorilor de română. Niciun jucător nu oferă simultan **L1 românesc + conversație + pronunție**.

**Cele 4 diferențiatoare (nimeni nu le are pe toate):**
| Axă | EVA | Ce fac competitorii |
|---|---|---|
| 🇷🇴 **Româna ca superputere** | Explică, corectează și traduce în română; sprijinul „se stinge" adaptiv RO→EN pe măsură ce progresezi | English-only sau doar limbi mari (ES/FR/DE/JP) |
| 🎯 **Pronunție tunată pe români** | Feedback fonemic pe erorile tipice RO (*th, v/w, i:/ɪ, æ/e*), **în conversație** | ELSA o face bine, dar prin drill-uri izolate; apps conversaționale au feedback slab |
| 💛 **Persona caldă, anti-anxietate** | Răbdare, încurajare, corectare prin reformulare (recast) | Duolingo = superficial; Loora/ELSA = ton serios, presiune |
| 💶 **Preț accesibil** | €5–8/lună | Speak/Loora/Duolingo Max = $20–30/lună |

**Public țintă inițial:** adulți A1–B1 — angajați care au nevoie de engleză la job, părinți, oameni intimidați de conversație. Exact segmentul pe care Duolingo îl pierde la vorbire și pe care Speak/Loora îl ignoră lingvistic. Extensibil ulterior la adolescenți și elevi.

---

## 2. Principii de produs (ADN-ul aplicației)

1. **Conversația e produsul, nu un feature.** Ecranul principal e o discuție cu EVA (voce sau text), nu un arbore de lecții.
2. **Sprijinul în română scade treptat.** A1: interfață + explicații în română, tap-to-translate pe orice. B1+: engleză aproape integral. Utilizatorul „crește" din română spre engleză.
3. **Siguranță psihologică înainte de corectitudine.** EVA nu întrerupe la fiecare greșeală; menține fluxul, reformulează natural. Scade „affective filter" → mai mult output.
4. **Ecran prietenos, nu foaie de test.** Micro-lecții de 3–5 min, vizual cald, animații blânde, zero „roșu" agresiv.
5. **Fundamentat pe conținut real, nu pe halucinații.** Tutorele e ancorat (RAG) în biblioteca proprie de manuale și în banca de propoziții etichetate CEFR.
6. **Ieftin de operat prin design.** Voce realtime scumpă doar pentru „free-talk"; restul pe pipeline ieftin controlabil.

---

## 3. Funcționalități — pe piloni și pe faze

### Pilonul A — Conversație cu EVA (nucleul)
- **Voce + text**, comutabil. Vorbești sau scrii; EVA răspunde vocal (voce caldă) cu subtitrare.
- **Persona EVA:** tutore răbdător, prietenos, care se adaptează la nivelul CEFR detectat.
- **Corectare prin recast:** când greșești („I have 25 years"), EVA continuă natural („Oh, you're 25 years old! And…") și marchează discret corecția pentru revizuire ulterioară.
- **Scenarii task-based din viața reală:** la aeroport, interviu de angajare, la doctor, comandă la restaurant, email către șef. (Alimentate din dialogurile State Dept. + generate de LLM.)
- **Buton „Ajutor în română"** oricând: „cum spun asta?", „ce a zis EVA?", „nu știu" — fără penalizare.
- **Rezumat post-conversație:** 3 lucruri făcute bine + 2 de lucrat + cuvinte noi trimise automat în SRS.

### Pilonul B — Pronunție tunată pe români
- Scor **per-fonem / cuvânt / fluență / prozodie** (Azure Pronunciation Assessment).
- **Listă RO-specifică** de perechi problematice: /θ ð/ („think/this"), /v–w/ („vine/wine"), /iː–ɪ/ („sheep/ship"), /æ–e/ („bad/bed"), schwa, plasarea accentului.
- **Shadowing** cu audio nativ + vizualizarea ritmului (engleza e stress-timed, româna silabică → sună „robotic").

### Pilonul C — Sprijin în română (fade adaptiv)
- **Tap-to-translate** pe orice cuvânt/frază (dicționar + Tatoeba).
- **Alerte „false friends"** contextuale: *library ≠ librărie*, *actually ≠ actual*, *sensible ≠ sensibil*, *eventually ≠ eventual*, *magazine ≠ magazin*.
- Explicații gramaticale **în română**, contrastiv (ce e diferit față de română).

### Pilonul D — Lecții & exerciții interactive
- **Micro-lecții** de 3–5 min, vizuale, task-based (nu „umple golul").
- **Modul dedicat de articole** (a/an/the) — eroarea nr. 1 a românilor, nu se auto-corectează, necesită drill contrastiv.
- **Progresie de phrasal verbs** amânată la A2+, predată tematic.
- Exerciții **generate de LLM din banca de propoziții deja etichetată CEFR** (control pe nivel).

### Pilonul E — Vocabular & memorare (SRS)
- **Spaced Repetition** cu algoritm **FSRS** (superior lui SM-2). Intervale 1/3/7/14/30 zile.
- Banca: **~16.000 propoziții paralele RO-EN** (Tatoeba) + cuvinte din conversații.
- KPI de retenție măsurat la 1 zi și 7 zile.

### Pilonul F — Plasare & progres
- **Test adaptiv de plasare** la onboarding (~10–15 min): *yes/no vocabulary test* (recunoaștere cuvinte reale vs pseudo-cuvinte) + 2–3 sarcini de producție evaluate de LLM. Mapare pe A1–B2. *(Nu întrebăm „ce nivel ai" — auto-evaluarea e nesigură.)*
- Hartă vizuală de progres pe competențe (vorbit / ascultat / citit / scris) și pe niveluri CEFR.

### Pilonul G — Gamificare blândă (anti-anxietate)
- **Streaks recuperabile** („streak freeze" automat, celebrează revenirea, nu pedepsi absența).
- XP, „badges", obiectiv zilnic reglabil (3/5/10 min).
- **Fără leaderboard agresiv** la început (opțional la v1).

### Împărțire pe faze
| Fază | Conținut | Durată |
|---|---|---|
| **MVP** | Auth + profil · plasare CEFR · SRS pe banca Tatoeba · 10–15 lecții · **1 mod** conversație vocală (cu limită de minute) · pronunție cu scor · streak/XP de bază · **doar 16+** | 8–12 săpt. |
| **v1** | RAG tutor pe manuale · exerciții generate LLM · gamificare completă · notificări · sync offline · scenarii multiple | +8–10 săpt. |
| **v2** | Consimțământ parental (sub-16) · personalizare adaptivă · voci multiple · mod „immersion" realtime · analytics pentru profesori · planuri plătite | +10–12 săpt. |

---

## 4. Pedagogie — de ce funcționează pentru români

**Analiză contrastivă (erorile tipice, țintă directă a exercițiilor):**
- **Articole** — româna are articol enclitic („mașina"), fără „a/an" separat → „I am student", „an advice". *Eroarea nr. 1, persistentă.*
- **Fonologie** — /θ ð/ inexistente → /t d s z/; /v–w/ neseparate; vocale /iː–ɪ/, /æ–e/ confundate; accent greșit; ritm silabic în loc de stress-timed.
- **Timpuri** — Present Perfect fără echivalent („I live here since 2010"); aspect continuu supraextins („I am knowing").
- **Ordine & prepoziții** — „a car red", „depend of", „married with".
- **False friends** și **phrasal verbs** (cea mai grea zonă la B1–B2).

**Metode aplicate:** comprehensible input / i+1 (Krashen) · output & task-based · SRS (retenție ~85% la 1 an vs ~22% fără) · shadowing · feedback prin recast.

**Progresie CEFR (vocabular activ):** A1: 500–1.000 · A2: 1.500–2.500 · B1: ~3.000 („fluență conversațională") · B2: 4.000–5.000.

**Cele 10 decizii pedagogice-cheie** sunt implementate în piloni A–G de mai sus (modul de articole, feedback fonemic RO-specific, SRS-FSRS, recast, plasare adaptivă, scenarii, alerte false-friends, phrasal verbs tematic, shadowing, streaks blânde).

---

## 5. Avantajul de conținut — biblioteca existentă

Aplicația NU pornește de la zero: se sprijină pe biblioteca `Z:\02. EVA - Learn English with EVA` (deja construită, ~4,4 GB, licențe libere/OER/domeniu public).

| Resursă din bibliotecă | Rol în aplicație |
|---|---|
| **~16.000 propoziții paralele RO-EN** (Tatoeba) | Banca de propoziții pentru **SRS** + generare de exerciții. Se clasifică o dată pe CEFR cu LLM (cost unic ~$5–15) și se stochează cu embedding. |
| **Manuale OER + gramatică** (PDF) | Chunk + embed → **RAG** care fundamentează tutorele (răspunsuri ancorate, nu halucinate). *Diferențiatorul tău față de un chatbot generic.* |
| **Dialogurile State Dept.** (Everyday Conversations, Dialogs) | Șabloane pentru **scenariile conversaționale** task-based. |
| **Audio (MP3)** | Ascultare + **shadowing**; ce lipsește → TTS on-demand cache-uit. |
| **Dicționar / gramatici RO-EN** | **Tap-to-translate** și explicații contrastive. |
| **Manualele școlare edu.ro** | Aliniere la programa școlară RO (pt. extensia către elevi, v2). |

Grounding-ul pe corpus propriu = **moat**: greu de copiat de competitorii generici.

---

## 6. Arhitectură tehnică

**Frontend: Flutter (mobil + web).** Un singur codebase iOS + Android + Web; Impeller redă constant 58–60 fps pe UI complex cu animații/gamificare; `flutter_webrtc` matur pentru voce realtime. *(React Native + Expo doar dacă echipa e deja JS/React. PWA singur = insuficient — audio în fundal și microfonul sunt fragile pe iOS Safari.)*

**Backend & date: Supabase (Postgres serverless).** Auth + Storage + Edge Functions + Realtime + **`pgvector`** (RAG în aceeași DB, fără bază vectorială separată). Pro $25/lună, 100k MAU. *(Firebase ajunge de 3–5× mai scump la scală și nu se potrivește la fel de bine cu SRS relațional.)* Regiune **Frankfurt** (rezidență UE).

**Model de date (Postgres + RLS):**
```
profiles(cefr_level, native_lang, goals)
lessons · vocab_items
sentences(en, ro, cefr, audio_url, embedding)
srs_cards(user_id, item_id, stability, difficulty, due_at)   ← FSRS
reviews(grade, timestamp)
conversations · messages(role, transcript, audio_url?, pron_score)
```

**Motorul de voce — strategie hibridă (cost-defensivă):**
- **Exerciții structurate & pronunție** → pipeline ieftin: **STT** (Whisper ~$0.006/min sau Azure STT) → **LLM text** → **TTS** (Azure Neural / OpenAI gpt-4o-mini-tts) → **Azure Pronunciation Assessment** (scor pe fonem). *Controlabil, ieftin, și — critic — îți dă scor de pronunție, ce speech-to-speech NU oferă.*
- **Mod „free-talk / immersion"** (premium, cu limită de minute) → **speech-to-speech realtime** (Gemini Live cel mai ieftin ~$0.02–0.04/min, sau OpenAI Realtime mini).

**Tutorele LLM:** **Claude Haiku 4.5** default (persona consistentă, corectare blândă, explicații în RO prin system prompt), escaladare la **Sonnet 5** pentru explicații gramaticale complexe. Costul textului e neglijabil (~$0.30–1/user activ/lună) — contează calitatea personei, nu prețul.

---

## 7. Motorul de conversație — design

**Schiță de system prompt pentru EVA** (ilustrativ):
```
Ești EVA, un tutore de engleză cald și răbdător pentru un vorbitor NATIV DE ROMÂNĂ, nivel {CEFR}.
Reguli:
- Vorbește ~80% engleză la {CEFR>=B1}, mai multă română la A1–A2. Adaptează dificultatea la i+1.
- NU corecta fiecare greșeală. Reformulează natural (recast) și continuă conversația.
- La cerere („ajutor"/„în română") → explică pe scurt ÎN ROMÂNĂ, apoi revino la engleză.
- Semnalează discret erorile RO-tipice (articole, th, false friends) → le trimiți în lista de revizuire.
- Ton: încurajator, fără judecată. Pune întrebări deschise ca să vorbească utilizatorul mai mult.
Context (RAG): {fragmente relevante din manuale/propoziții}.
```
- **Adaptare de nivel:** temperatura vocabularului și lungimea frazelor scad/cresc după `cefr_level`.
- **Control de cost:** prompt caching pentru system prompt; limită de minute pe free-talk; rezumatul și extragerea cuvintelor se fac cu Haiku.

---

## 8. Costuri și unit economics

**Cost per utilizator activ / lună** (ipoteză 200 min conversație/lună, pipeline):
| Componentă | Cost |
|---|---|
| STT (100 min) | ~$0.30 |
| LLM tutor (Haiku, ~200–300K tok) | ~$0.50 |
| TTS (100 min) | ~$1.50 |
| Pronunție Azure | ~$0.70 |
| **Total pipeline** | **~$3–4 / user / lună** |

- Utilizator *light* (60 min/lună): ~$1–1,5.
- Aceeași activitate pe realtime pur: ~$8–20/user/lună (3–5× mai scump, fără scor fonem) → de aceea realtime doar pentru free-talk premium.
- **Infra fixă MVP:** ~$25–75/lună (Supabase + servicii).

**Preț recomandat:** **€5–8/lună** (sau ~€49/an) — sub Speak/Loora/Duolingo Max, comparabil cu Praktika/TalkPal dar cu suport RO. La acest preț, cu cost variabil ~$3–4, **marja e sănătoasă**. Freemium generos (ca Gliglish: ~10 min/zi gratuit) pentru achiziție.

---

## 9. Legal — GDPR / AI Act (critic pentru UE/România)

- **Vocea NU e dată biometrică** dacă NU faci identificare de vorbitor. STT + evaluare pronunție ≠ speaker-ID → nu intră sub Art. 9. **Recomandare:** nu stoca audio brut implicit (procesare tranzitorie, păstrezi transcript + scor); dacă stochezi audio pentru progres → consimțământ separat, opt-in.
- **Rezidență UE:** Supabase Frankfurt; tier-uri API **zero-retention** (OpenAI/Google); DPA cu subprocesorii.
- **Minori:** vârsta consimțământului digital în **România = 16 ani**. **MVP doar 16+** ca să eviți fluxul de consimțământ parental în faza 1; sub-16 în v2.
- **AI Act:** transparență — utilizatorul știe clar că vorbește cu un AI.

---

## 10. UX/UI — limbaj vizual și ecrane

**Ton vizual:** cald, rotunjit, prietenos. Culoare-brand primară + accente moi; avatar EVA simpatic (nu antropomorfic-realist → evită „uncanny valley" și presiunea). Micro-animații de încurajare. Mod întunecat.

**Inventar de ecrane (MVP):**
1. **Onboarding & plasare** — obiectiv, motiv („de ce înveți?"), test adaptiv scurt.
2. **Acasă / Dashboard** — obiectivul zilei, streak blând, buton mare „Vorbește cu EVA", 2–3 carduri (revizuire SRS, lecția de azi, scenariu).
3. **Conversație cu EVA** *(ecranul-erou)* — avatar EVA, bule de dialog, subtitrare EN + RO la tap, buton microfon mare, „Ajutor în română", indicator blând de pronunție.
4. **Feedback de pronunție** — cuvântul pe silabe/foneme colorate (verde/galben/roșu blând), scor, buton „ascultă nativ" + „reîncearcă".
5. **Revizuire SRS** — card propoziție RO↔EN, audio, auto-evaluare (ușor/greu).
6. **Lecție interactivă** — micro-pas, exercițiu, feedback instant.
7. **Progres** — hartă CEFR pe 4 competențe.

*(Mockup vizual al acestor ecrane: fișierul `Mockup EVA.html` din acest folder / artifactul publicat.)*

---

## 11. Go-to-market & monetizare

- **Mesaj:** „Aplicațiile globale te învață engleză *în engleză*. EVA te învață să **vorbești**, plecând de la limba ta."
- **Canale:** TikTok/Instagram/YouTube RO (short-uri „cum spui corect X"), SEO pe întrebări RO („cum se spune … în engleză"), parteneriate cu angajatori/HR (engleză pentru angajați), influenceri educaționali RO.
- **Model:** Freemium → abonament €5–8/lună / €49/an. B2B2C ulterior (companii, școli — leverage manualele edu.ro).

---

## 12. Riscuri și mitigări

| Risc | Mitigare |
|---|---|
| Duolingo adaugă română la Video Call | Adâncime pe **pronunție RO-specifică + L1 profund + RAG pe conținut** — greu de copiat rapid |
| Costul vocii AI apasă marja la €5/lună | Pipeline ieftin + limite de minute pe free-talk + tier gratuit ca pârghie de achiziție |
| Calitatea personei / corectare enervantă | Investiție în prompt engineering + testare cu utilizatori reali; recast, nu marcaj roșu |
| GDPR/minori | MVP 16+, audio tranzitoriu, rezidență UE, DPA |
| Retenție (churn tipic în edtech) | Streaks blânde, micro-lecții, valoare vizibilă rapid (primul „am reușit să vorbesc") |

---

## 13. Metrici de succes (KPI)

- **Activare:** % care termină prima conversație cu EVA în prima sesiune.
- **Vorbit:** minute de conversație / utilizator / săptămână (metrica de bază — vorbitul e produsul).
- **Învățare:** retenție SRS la 1 zi și 7 zile; progres de pronunție (scor fonem în timp).
- **Retenție:** D1 / D7 / D30; „streak" median.
- **Business:** conversie free→paid, MRR, CAC vs LTV, cost voce / user.

---

## 14. Pașii următori imediați

1. **Validare concept** (1–2 săpt.): 5–10 interviuri cu români A1–B1 despre frica de a vorbi + un prototip de conversație (chiar și Wizard-of-Oz cu Claude).
2. **Prototip motor de conversație** (2–3 săpt.): Claude Haiku + system prompt EVA + pipeline STT/TTS + Azure pronunție, testat pe 20 de scenarii.
3. **Etichetare CEFR a bibliotecii** (batch LLM, cost unic ~$5–15): pregătește banca de propoziții + embeddings pentru SRS și RAG.
4. **MVP** (8–12 săpt.) conform fazei MVP de mai sus, cu 2–3 dezvoltatori.

---

### Rezumat executiv
Un tutore AI de engleză **conversation-first**, singurul construit **pentru români** (sprijin în română care se stinge treptat), cu **feedback de pronunție tunat pe erorile RO** și un **ton cald anti-anxietate**, la **€5–8/lună**. Tehnologie ieftin-controlabilă (Flutter + Supabase + pipeline STT/LLM/TTS + Azure pronunție, realtime doar premium), cost ~$3–4/user activ, fundamentată pe biblioteca OER deja construită. Piața RO e goală — fereastra e deschisă acum.

---

*Surse cheie: Duolingo Max / Speak / ELSA / Loora / Praktika / Gliglish / TalkPal / Babbel Speak (funcții & prețuri 2025–2026); OpenAI / Anthropic / Gemini / Azure / ElevenLabs (prețuri API voce & LLM 2025–2026); cercetare CEFR & SRS; Flutter vs RN; Supabase vs Firebase; GDPR voce/biometric & AI Act. Listă completă de linkuri în raportul de cercetare (`research_reports.md`).*
