---
name: drakon-comics
description: "Proiect BD „DRACULA — Contele Nopții” (DRACULA COMICS): erou VLAD III Drăculea vampir pozitiv, traseu prin capitale, echipe agenți, site local; D:\\00. Downloads\\Dracula Book\\DRACULA-COMICS"
metadata:
  node_type: memory
  type: project
  originSessionId: 010d63d3-a2e0-494a-8e19-1a42f357e657
  modified: 2026-09-24T00:28:08.603Z
---

Început 24.09.2026. Serie BD color + povestiri RO pt editura Dracula Book ([[dracula-book-editura]]). Canon v3.0 (`01_CANON\00_CANON_NUCLEU.md` = sursă unică):
- Erou = **VLAD III Drăculea însuși** (userul: „păstrăm numele de VLAD”; „Valerian Drakon” anulat). Alias modern Vlad Dragomir, consultant Poliția Română; partenera comisar-șef Ioana Mureșan.
- 1431–1476 = **istorie reală strictă** (userul cere respectarea locurilor/anilor până la maturitate).
- BD = **continuitate proprie, diferită de romane** (NU se leagă de NOIR „Umbra Trandafirului Negru”).
- Transformat dec. 1476 (mormântul gol Snagov 1933) de soția Sânziana (legenda Râul Doamnei 1462). Familie: Mihnea cel Rău (asasinat Sibiu 1510), Ilinca (hacker), Buna Dochia, Brutus, majordom Iosif Hanzer. Antagonist fratern Radu cel Frumos (Casa Strigoi); arc lung „Omul Fără Umbră”.
- **Traseu 24 popasuri prin capitale 1476–2026** (Veneția, Istanbul, Praga, Paris, Londra 1888/Stoker 1897, Viena 1683, NY 1920, Hollywood 1931 Lugosi...) legat de obiective celebre + clișee Hollywood — cerință explicită user.

Structură: 00_STUDIO (echipă+roadmap+jurnal+rapoarte/) · 01_CANON · 02_RESEARCH · 03_PERSONAJE · 04_LUME (06_TRASEUL_CAPITALELOR.md) · 05_ART · 06_EPISOADE · 07_POVESTIRI · 08_SCENARII · 09_SITE (build_site.py → index.html).

**Why:** userul vrea „companie” de echipe-agenți cu roluri, KPI, raportare și roadmap.
**How to apply:** la revenire citește 00_STUDIO/03_JURNAL_PROGRES.md și canonul; schimbările de canon trec prin jurnal.

**Decizii Producător 9–14 (24.09.2026), registru `01_CANON/01_DECIZII_PRODUCATOR.md`:** titlul = doar „DRACULA” + subtitlu pe arc (NU „Contele Nopții”); acțiune și ziua; fashion icon pe epoci; stil Bond (cai/caleșe/mașini/avioane/iahturi, femei la superlativ, success story); FĂRĂ soție în prezent (Sânziana înstrăinată din 1794); fantezie aspirațională pt tineri (succes, bani, libertate — prin merit). Surse de inspirație = orice roman/scenariu de succes; contează modul de prezentare.
**Proces:** „Poarta 9,50” — 3 auditori (canon/craft/kpi), min ≥9,50, altfel plan de măsuri + revizie; arhivă completă în `00_STUDIO/audit/<COD>/` + `00_REGISTRU_AUDIT.md`. Pipeline v4 (workflow reluabil cu resumeFromRunId): scriptul copiat în `00_STUDIO/audit/00_PROCEDURA_PIPELINE_v4.js`. Atenție la limita de sesiune API (a oprit agenți o dată).
**Gotcha:** scripturile Workflow trebuie să aibă final de linie LF — Python pe Windows scrie CRLF (open(...,'w') fără newline='\n') și Workflow le respinge („control characters”). Pipeline activ din 24.09.2026 ~16:45: `00_PROCEDURA_PIPELINE_v4b_PARALEL.js` (ramura creativă G1→G5 + organizarea R6–R10 în paralel; decizia 16).
**Stare 28.09.2026 22:00:** limita SĂPTĂMÂNALĂ atinsă pe 25.09 (~10M tokeni în 1,5 zile cu 4 fluxuri paralele), resetată 28.09 09:00; toate 4 fluxurile reluate din cache (v4b principal wf_87b84590-f4c; H-ARSENAL wf_41d90592-99b, R1 min 9,00; I-ASCUNZATORI wf_604cd767-6c1; J-TRANSPORT wf_d487b934-0c4, R1 min 8,90). Cataloage 10/11/12 scrise, în audit. Decizii 17–19 = cataloagele ca sursă obligatorie. Userul NU a răspuns la propunerea „revizii fără extinderi”/secvențiere — a apăsat doar „Try again”.
**Decizia 20 (28.09.2026, „aplica”):** revizii fără extinderi necerute + fluxuri ÎN ORDINE: (1) v4b cu args only=[G1,G2] (rulare ws8rjf9k9, resume wf_87b84590-f4c) → (2) cataloagele H/I/J una câte una (resume wf_41d90592-99b / wf_604cd767-6c1 / wf_d487b934-0c4) → (3) v4b cu only=[G3,G4,G5]. NU relansa toate în paralel.
**PREDARE (29.09.2026):** folderul `00_PREDARE/` e punctul de intrare pentru orice cont/sesiune: 00_CITESTE_INTAI.md, STARE_CURENTA.md (generat de `python 00_PREDARE/actualizeaza_stare.py`; `--json` = starea pt fluxuri), JURNAL_EVENIMENTE.md (viu, doar append), LOCK_SESIUNE_ACTIVA.md (un singur cont activ), scripturi/dracula_v5_reluabil.js (flux care își citește starea de pe disc, disjunctor la prima eroare API, checkpoint pe etape, oprire la 95% din bugetul '+Nk'), scripturi/BRIEFURI_LIVRABILE.md. Userul a cerut explicit: jurnal complet + lucru multicont + salvare/raportare la apropierea limitei.
