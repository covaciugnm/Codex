# Raport de audit · KPI & Completitudine · G0-STUDIO-v4 · R1

| Câmp | Valoare |
|---|---|
| **Livrabil** | [G0-STUDIO-v4] Organizarea studioului v4 (echipa, modul de gândire, sarcini, raportare, roadmap per membru, Poarta 9,50, arhivare) și jurnalul v4 |
| **Cod** | `G0-STUDIO-v4` · poarta G0 |
| **Rundă** | R1 (prima rundă a codului relansat; versiunea auditată = R0) |
| **Auditor și lentilă** | AU-K · Auditor de KPI & Completitudine (agentul `audit G0-STUDIO-v4 R1 kpi`); nu a contribuit la livrabil; nu a citit rapoartele celorlalți auditori ai rundei |
| **Data** | 24.09.2026 (verificările pe disc: 06:37–06:45) |
| **Fișiere auditate (SHA-256)** | `00_STUDIO/01_ECHIPA_SI_ROADMAP.md`: `8b2c6319c77a48480a1d90aa8c4775543da67dfcb843d835d8c256b79e53c7bc` · `00_STUDIO/03_JURNAL_PROGRES.md`: `d3a63ed3aa9dd662d34e41708a403b1dfc756f7aa13e4d087e9a1958e5f05924` |
| **Concordanța cu R0** | `sha256sum -c` pe `00_STUDIO/audit/G0-STUDIO-v4/R0_versiune_initiala/SHA256SUMS.txt` (SHA-256 al listei: `14631f54bb09b4684382a5f593a51088da49b2f48ba123d66ba8841240659e41`): 26/26 OK; cele 24 de brief-uri vii sunt identice cu copia R0. Nicio modificare a livrabilului după predare (niciun fișier din afara `00_STUDIO/audit/` modificat după 06:36:08). |
| **Referințe citite (SHA-256)** | registrul Producătorului `01_CANON/01_DECIZII_PRODUCATOR.md`: `b81d4b07b060e0cf502bfae4a859400483752abdadf1090eba972fc5e9194a9f` (integral) · canonul `01_CANON/00_CANON_NUCLEU.md` v4.0: `9d7b97be97b753ca01e95e7c38f8175a39858b397071a5c769a120f545217b2e` (secțiunile 2, 3, 5, 5.1, 10, 12, 13, 14, 16.1, integral; restul prin căutare) · raportul echipei `00_STUDIO/rapoarte/S_showrunner.md`: `39abe86bcc8bccfeaada2e89fd5f2e9549ac404350c3954a000c3a6b031f9eac` · registrul central `00_STUDIO/audit/00_REGISTRU_AUDIT.md`: `8ee64c7f96f2669f379156f4bef2ccb71d6b68a8641ddbecf1675e8c2ad4c4b1` · cele 24 de brief-uri din `00_STUDIO/02_BRIEFURI/` · ieșirile autoverificării din `R0_verificari_automate/` · raportul R1 KPI al codului oprit `G0-STUDIO` (pentru închiderea defectelor, §6.5 (5)) |

## 1. Nota și verdictul

| Nota | Verdict |
|---|---|
| **8,68 / 10** | **FAIL (NU TRECE)**: sub pragul de 9,50 |

**Calculul notei:** 4 defecte majore plafonează nota la 9,20; fiecare major suplimentar scade 0,08 (−0,24); cele 14 defecte minore scad câte 0,02 (−0,28). 9,20 − 0,24 − 0,28 = **8,68**. Niciun defect critic: 0 contradicții cu registrul Producătorului (tabelul din §2 e identic cu registrul, cu cele 2 intervenții declarate).

Documentul e, ca volum de muncă și ca rigoare aritmetică, cel mai bun livrabil de organizare pe care l-am văzut în acest proiect. Nu trece pentru că patru lucruri de fond nu sunt la nivelul „fără modificări substanțiale”: jurnalul afirmă o stare a arhivei care nu există pe disc, raportul S nu respectă șablonul pe care chiar acest livrabil îl impune, fișa prozatorilor contrazice canonul v4 și trei posturi, dintre care unul pe drumul critic al lansării, nu au titular.

## 2. Metoda de verificare

**Ce am citit integral:** `01_ECHIPA_SI_ROADMAP.md` (1.690 de rânduri), `03_JURNAL_PROGRES.md` (341 de rânduri), registrul Producătorului (37 de rânduri), registrul central de audit, raportul S (secțiunile v4 și „Stare audit”), secțiunile canonului enumerate în antet, antetul și extrasele brief-urilor AU-K, H3, D3–D6, ieșirile `verificari_v4_iesire.txt` și `calendar_bd_iesire.txt`, tabelul defectelor din `00_STUDIO/audit/G0-STUDIO/R1_audit_kpi.md`.

**Ce am numărat și cu ce instrument** (Python 3.12, scripturi proprii scrise în directorul de lucru al auditorului, plus `wc`, `sha256sum`, `grep`, `find`, `ls` prin Bash):

| Ce | Instrument | Rezultat |
|---|---|---|
| Dimensiunea | `wc -l -w -c` | organizarea: 1.690 de rânduri, 37.813 cuvinte, 242.560 B; jurnalul: 341 de rânduri, 8.871 de cuvinte |
| Structura | Python (titluri în afara blocurilor de cod) | organizarea: 75 de titluri (15 de nivel 2, 59 de nivel 3), 30 de tabele; jurnalul: 34 de titluri, 9 tabele |
| Fișele de post | Python (regex pe §4.1–§4.24) | 24/24 de fișe; 24/24 cu cele 4 rubrici (mod de gândire · sarcini · livrabile · KPI); **188 de KPI**, numerotare K1…Kn continuă în 24/24 |
| Anexa A față de fișe | Python (comparație text cu text) | 188/188 de rânduri; **0 diferențe** de text față de fișe; concordanța: „=” 51 · „fișa precizează” 56 · „fișa e mai strictă” 11 · „nou în fișă” 70 = 188 (identic cu cifrele declarate) |
| Brief-urile față de fișe | Python | 24/24 de brief-uri conțin toate KPI-urile fișei lor (0 lipsă); 16 extrase din procedura v4 + 8 scrise (câmpul „Tipul brief-ului”) |
| Tabelul deciziilor (§2) față de registru | Python `difflib` | 14/14 rânduri; singurele diferențe: cele 2 intervenții declarate („[…]” la deciziile 1 și 9) |
| Roadmapul pe membri (§9.3) | Python | 65 de rânduri; 24/24 de posturi; acoperirea pe etape: vezi defectul 9 |
| Calendarul BD (§9.4) | Python, recalculare independentă cu sărbătorile legale 2026–2027 | 20/20 de episoade conforme formulei (desen 12 z.l., culoare 8, lettering 4, GA +2, tampon exact 10 z.l.); Ep. 1: fereastră specială 10/8/4; 0 date de lucru în zile nelucrătoare; tabelul de capacitate: 0 luni peste plafon |
| Datele din document | Python | 146 de date distincte; în zile nelucrătoare: 30.11.2026 și 01.12.2026 (folosite intenționat), 01.01.2027 (citare juridică) și **31.10.2026 (sâmbătă)**, vezi defectul 7 |
| Diacritice și format | Python | 0 caractere cu sedilă (U+015E, U+015F, U+0162, U+0163) în cele 2 fișiere și în 24 de brief-uri; 0 cuvinte-test fără diacritice; 0 ghilimele drepte în text; „ ” echilibrate (232/232 și 88/88); 0 tabele cu număr greșit de coloane; 0 legături rupte (inclusiv 20/20 în registru); 1 ancoră între fișiere, validă |
| Căile de fișiere | Python (384 de căi în organizare, 95 în jurnal) | 0 căi lipsă nemarcate „(se creează …)”, în afara exemplelor ipotetice și a tabelului de corespondență din §11.2 |
| Inventarul din jurnal (§4) față de disc | `find … -type f \| wc -l` | 01_CANON 2 · 02_RESEARCH 11 · 03_PERSONAJE 5 · 04_LUME 6 · 05_ART 25 (7/8/2/8) · 06–08 0 · 09_SITE 4 · rapoarte 4 · brief-uri 24 · audit 132 + 27 (copia R0) = 159: **identic** |
| Tabelul propunerilor de canon (jurnal §5) | Python | 64 + 12 = 76 de rânduri, 64 de identificatori unici: identic cu bilanțul declarat |
| Anexa B | Python | cele 59 de identificatori R1 (CI-1…18, MP-1…20, KC-C1, KC-M1…M8, KC-m1…m12) sunt toți acoperiți |
| Arhiva G0-CANON-v4 (starea declarată în jurnal) | `ls`, `find`, citirea `rez_tmp.json` | **2 fișiere, fără copia canonului**: vezi defectul 1 |

**Testul automat al urmelor canonului vechi** (KPI AU-K K7): `grep -i -E "contele nop|contele noptii|count of the night|valerian|drakon|conte(le)? nopt"` pe cele 2 fișiere, pe cele 24 de brief-uri și pe canon: **0 apariții**. „Sânziana ca soție în prezent”: `grep` pe „soți(a|e)”: 12 apariții, toate în formularea corectă („fără soție în prezent”, „nu soția lui în prezent”) sau la trecut (jurnal, rândul 188: 1476). „Dracon…”/„Valeri…” în cele 2 fișiere: 0.

**Căutări pe web:** niciuna. Verificările lentilei KPI sunt interne (numărători, comparații, aritmetică de calendar). Surse de referință pentru calendar: Codul muncii, art. 139 (sărbătorile legale: 1–2 și 6–7 ianuarie, 24 ianuarie, Vinerea Mare, Paștele și Rusaliile ortodoxe, 1 mai, 1 iunie, 15 august, 30 noiembrie, 1 decembrie, 25–26 decembrie); Paștele ortodox: 12.04.2026 și 02.05.2027 (calcul pascal iulian); Rusaliile: 31.05–01.06.2026 și 20–21.06.2027.

## 3. KPI-urile fișei rolului (S, §4.1) față de starea măsurată

| KPI S | Ținta | Valoarea măsurată | Stare |
|---|---|---|---|
| K1 | 0 contradicții nerezolvate canon–registru–livrabile | registrul: 14/14 respectate; **1 contradicție organizare–canon** (forma prozei: §4.9 față de canonul, secțiunea 12; defectul 3) | ❌ |
| K2 | 24/24 de brief-uri aliniate | 24/24 prezente, identice cu R0, cu 188/188 de KPI ale fișelor; 0 texte de procedură înlocuită | ✅ |
| K3 | jurnal în ≤ 24 h | oprirea, procedura v4, canonul v4 consemnate în aceeași zi; **evenimentul de integritate al canonului v4 (modificare la 06:20:02, R0 fără copie) neconsemnat** (defectul 1) | 🟡 |
| K4 | planuri în ziua auditului | nu se aplică la R0 | – |
| K5 | propuneri de canon în ≤ 48 h | 76/76 de rânduri cu decizie sau transmitere | ✅ |
| K6 | 100% din dosare complete | `G0-STUDIO-v4`: complet pentru R0; **`G0-CANON-v4`: R0 fără copia livrabilului și fără `SHA256SUMS.txt`**; `G0-CANON` și `G0-STUDIO`: `REZULTAT_FINAL.md` în așteptarea GR (AP-7, declarat) | ❌ |
| K7 | ≤ 3 runde în medie | 3 runde / 2 livrabile = 1,50 (B0: corect) | ✅ |
| K8 | 0 aprobări fără sursă | 0: oprirea, planurile R1, lucrul pe risc marcate „în așteptarea contrasemnării” / „în așteptare” | ✅ |
| K9 | 0 urme în livrabilele porții G0 | 0 în canon, organizare, jurnal, brief-uri; 21 de fișiere ale echipelor (țintă G5) | ✅ la G0 |
| K10 | buletin în fiecare vineri | B0 prezent (24.09.2026, joi); antetul nu urmează șablonul §5.5 (defectul 18) | 🟡 |

## 4. Matricea de acoperire a cerințelor din brief

| # | Cerința | Unde | Stare |
|---|---|---|---|
| 1 | Echipa și modul de gândire | §2 (11 principii), §3 (24 de posturi, 36 de titulari), 24/24 de fișe cu „mod de gândire” | ✅ |
| 2 | Sarcini | 24/24 de fișe | ✅ |
| 3 | Raportare de progres, cu șablon | §5.1–§5.5; **raportul S nu respectă șablonul v4** (defectul 2); rapoartele a 12 posturi în afara auditului (defectul 5) | 🟡 |
| 4 | Roadmap măsurabil pentru FIECARE membru (inclusiv auditori, manageri, grefieri) | §9.3: 65 de rânduri, 24/24 de posturi; **6 posturi fără rând și fără justificare în Etapa I** (defectul 9); **H2, H3, H4 fără titular** (defectul 4) | 🟡 |
| 5 | Toți pașii auditați; fiecare agent are auditori | §6.7 (inclusiv auditorii, GR, GR-S, MS, calibrarea) | ✅ (cu defectul 5) |
| 6 | Minim 9,50; sub prag ședință + manager cu sarcini clare | §6.3 (a), (e), (f); §4.2 | ✅ |
| 7 | Totul salvat și arhivat | §7 (arborele, cine scrie, regulile, cum citește un auditor extern) | ✅ ca sistem; ❌ ca stare raportată (defectul 1) |
| 8 | Aliniere la cele 14 decizii | §1, §2 (tabelul 14/14 și testul fiecărei decizii), KPI noi în fișe | ✅ față de registru; ❌ față de canonul v4, secțiunea 12 (defectul 3) |
| 9 | Fișe cu KPI numerici și căi de livrabile | 188 de KPI; căi complete sau marcate; **7 KPI măsoară acțiuni ale Producătorului** (defectul 8) | 🟡 |
| 10 | Roadmap datat: I sprint; II până la 30.11.2026; III de la 01.12.2026; figurina 31.03.2027 | §9.1, §9.2, §9.6; recalculat: conform | ✅ |
| 11 | Poarta 9,50 | §6 | ✅ |
| 12 | Arhiva: `audit\<COD>\` cu R0, R<n>_audit_canon/craft/kpi, plan + Execuție, instantaneul, REZULTAT_FINAL, VERSIUNE_APROBATA, registrul | §7.1–§7.5; toate elementele prezente | ✅ |
| 13 | Independența auditului; contrasemnarea Producătorului („în așteptarea contrasemnării”) | §6.3 (g), MS K4, AP-8; formularea autorului „Showrunnerul delegat” (defectul 6) | ✅ (cu defectul 6) |
| 14 | Jurnal coerent cu starea reală, inclusiv oprirea G0 v3 și motivele | oprirea și motivele: ✅ (§6, 05:45:31, neregula 4); starea `G0-CANON-v4`: ❌ | 🟡 |

## 5. Închiderea defectelor KPI din R1 al codului oprit `G0-STUDIO` (§6.5 (5), Anexa B)

| Defect R1 (KPI) | Starea în v4.0 | Dovada |
|---|---|---|
| KC-C1 arhivarea | închis | §7; dosarele există; V1, V2 |
| KC-M1 auditorii, grefierii, MS în organigramă | închis | §3.1; §4.2, §4.20–§4.24 |
| KC-M2 roadmap pe membri, datat | parțial | 65 de rânduri datate; 6 posturi fără rând în Etapa I (defectul 9) |
| KC-M3 scenariile Ep. 2–20 | închis | D2 K9; §9.4 (19/19) |
| KC-M4 reziduul canonului anulat | închis | testul urmelor: 0 |
| KC-M5 pivoturile și pragul de popasuri | închis | D1 K2 (5/5), K3 (≥ 15) |
| KC-M6 raportul S conform șablonului | **parțial (redeschis)** | defectul 2 |
| KC-M7 jurnal coerent cu starea reală | **parțial** | defectul 1 |
| KC-M8 controlul versiunilor | închis | §12; R0 cu SHA-256, 26/26 OK |
| KC-m1 organigrama ASCII | închis | tabel |
| KC-m2 anglicismele | închis | §11; 0 termeni englezi în afara glosarului, a căilor și a codurilor (căutare pe 11 termeni) |
| KC-m3 KPI S nenumeric; KPI MS | închis | S K1–K10; MS K1–K6 |
| KC-m4 panourile (4–6 față de splash și double-spread) | închis, cu o ambiguitate nouă | D2 K2; defectul 16 |
| KC-m5 alocarea prozatorilor | închis | §3.3 |
| KC-m6 calea coperților; prompturile în engleză | închis | fișa E (livrabile, regula limbii) |
| KC-m7 registrul de riscuri | închis | RS1–RS26, cu probabilitate, impact, responsabil |
| KC-m8 istoricul în șablon | închis | §5.2 |
| KC-m9 titlul, „5bis”, liniile goale | închis | V16 |
| KC-m10 criteriile de calitate ale lui A | închis | A K1, K3 |
| KC-m11 codurile porților; conflictul de independență la G0 | parțial | coduri: §6.2; independența: regula (g); denumirea autorului: defectul 6 |
| KC-m12 măsurarea cititorilor | închis | H3 K3 (31.12.2026) |

**Rezultat:** 17 închise, 4 parțiale (KC-M2, KC-M6, KC-M7, KC-m11), 0 neînchise.

## 6. Puncte forte

1. **Sistemul KPI e complet și coerent intern:** 24/24 de fișe cu aceeași structură, 188 de KPI, Anexa A generată automat și identică text cu text cu fișele (0 diferențe), concordanța numărată exact (51/56/11/70).
2. **Integritatea predării e impecabilă pentru acest cod:** R0 cu `SHA256SUMS.txt`, 26/26 amprente identice cu fișierele vii, brief-urile vii identice cu anexa R0, iterațiile respinse ale autoverificării păstrate, nu șterse.
3. **Calendarul BD rezistă unei recalculări independente:** 20/20 de episoade exact după formulă, cu sărbătorile legale 2026–2027 (inclusiv 1 iunie și Rusaliile 2027), 0 luni peste capacitate, tampon exact de 10 zile lucrătoare.
4. **Aliniere fidelă la registrul Producătorului:** tabelul celor 14 decizii e identic cu registrul (numai cele 2 intervenții declarate), fiecare decizie are proprietar, verificator și test (§2).
5. **Curățenia textului:** 0 urme ale canonului vechi, 0 sedile, 0 ghilimele drepte, 0 tabele rupte, 0 legături rupte, inventarul din jurnal identic cu discul.
6. **Arhitectura de audit e matură:** statusurile OPRIT și EROARE_API, abaterile procedurii tratate explicit (AP-1…AP-12), „cine auditează fiecare post” (§6.7), calibrarea auditorilor, regula (j) pentru modificările de după PASS.
7. **Oprirea G0 v3 e documentată onest:** motivul, ora, neregula 4, instantaneul `STARE_LA_OPRIRE/` cu 27/27 de amprente identice.

## 7. Tabelul defectelor

| Nr. | Gravitate | Locația | Problema | Corectura |
|---|---|---|---|---|
| 1 | **MAJOR** | `03_JURNAL_PROGRES.md` §2, rândul `G0-CANON-v4` (r. 33: „livrat la 06:18:48 (R0 în dosar)”); antetul (r. 9); §4 (r. 76); §6, intrarea 06:18:48 (r. 267–272); registrul central, §2 (niciun rând pentru `G0-CANON-v4`) | Jurnalul nu e coerent cu starea reală a arhivei. `00_STUDIO/audit/G0-CANON-v4/R0_versiune_initiala/` conține numai `verificari_automate/verifica_canon_v4.py` și `verificari_automate/rez_tmp.json` (verificat la 06:43): **nicio copie a canonului și nicio `SHA256SUMS.txt`**. Singura amprentă arhivată (`rez_tmp.json`, 06:19:13: `fecf6ae6…`) **diferă** de canonul curent (`9d7b97be…`, fișier modificat la 06:20:02, după ora de predare declarată, 06:18:48). Inventarul din §4 numără chiar „`G0-CANON-v4/` 2”, dar jurnalul nu trage concluzia. Evenimentul de integritate (riscul RS13, regula (d) din §6.3, §5.3 regula 4) nu e consemnat, iar auditorii `G0-CANON-v4` nu au o versiune R0 cu care să compare amprenta. Interimarul a adăugat în registru rândul 7 pentru `G0-STUDIO-v4`, dar niciun rând pentru `G0-CANON-v4`. | În revizie: (a) rândul `G0-CANON-v4` din §2: „R0 incomplet: fără copia canonului și fără `SHA256SUMS.txt`; amprenta arhivată `fecf6ae6…` (06:19:13) ≠ versiunea curentă `9d7b97be…` (06:20:02)”; (b) intrare nouă în §6, ca eveniment de integritate (ora, sursa, efectul), plus punctul corespunzător în buletinul următor; (c) sarcină pentru autorul canonului: copia R0 și `SHA256SUMS.txt` înaintea rundei R1 a `G0-CANON-v4`, cu explicarea modificării de la 06:20:02; (d) rând factual în registru pentru `G0-CANON-v4`, simetric cu rândul 7. |
| 2 | **MAJOR** | `00_STUDIO/rapoarte/S_showrunner.md` (livrabilul S, §4.1): secțiunile „G0-STUDIO-v4” (r. 170–211) și „G0-CANON-v4” (r. 7–166), „Stare audit” (r. 267–275), r. 17–19, r. 181; `01_ECHIPA_SI_ROADMAP.md` Anexa B, tema T11 | Raportul echipei pentru acest livrabil nu respectă șablonul v4 din §5.2, introdus chiar de acest livrabil: secțiunea obligatorie **„Conformitatea cu deciziile Producătorului” are 0 apariții** (grep); tabelul KPI al `G0-STUDIO-v4` acoperă 6/10 KPI (lipsesc K4–K7), iar cel al `G0-CANON-v4` 8/10 (lipsesc K9, K10); pentru `G0-STUDIO-v4` lipsesc „Propuneri de modificare a canonului” și „Stare audit”; tabelul „Stare audit” nu are rândul `G0-STUDIO-v4` și arată `G0-STUDIO` „NU TRECE”, fără statusul ⏹ OPRIT. Raportul conține afirmații false: canonul, raportul și `rezultat_verificari_v4.0.json` „arhivate” în R0 (r. 17–19; pe disc nu există), „17 extrase fidele + 7 scrise (A1–A6, E2, E3, E4, H1–H4)” (r. 181; real: 16 + 8). Anexa B declară KC-M6 închis (T11), dar în v4 e redeschis. | Rescrieți secțiunea v4 a raportului S integral după §5.2: tabelul de conformitate 14/14 (decizia · cum e respectată · dovada), KPI K1–K10 cu valorile măsurate, propunerile, „Stare audit” la zi (`G0-STUDIO` ⏹ OPRIT; `G0-STUDIO-v4` R0 → R1; `G0-CANON-v4` R0 incomplet), istoricul; corectați r. 17–19 și r. 181; în Anexa B, T11: „redeschis în v4.0, închis în revizia R1”. |
| 3 | **MAJOR** | `01_ECHIPA_SI_ROADMAP.md` §4.9 (r. 382, sarcina 1; KPI K3, K4), §6.6 (AP-4); `00_STUDIO/02_BRIEFURI/D3_D6_brief.md` (r. 19); față de canonul v4, secțiunea 12 (r. 367) | Contradicție organizare–canon pe forma prozei. Canonul, secțiunea 12, prevede că formele povestirii „se rotesc”: jumătate sunt „ediția-pereche”, **la persoana I, cu vocea lui Vlad**, iar celelalte sunt jurnale, dosare sau vocile altor personaje; fiecare „aduce cel puțin o informație pe care banda n-o are”. Fișa D3–D6 impune pentru toate cele 20 de povestiri ghidul `STYLE`: **„persoana a III-a focalizată pe Vlad”**. Niciun AP nu consemnează divergența (AP-4 tratează numai lipsa ghidului, AP-12 numai faptele canonice). KPI-urile D3–D6 nu măsoară nici rotația formelor, nici „informația în plus”, iar K4 („0 abateri de la canon”) devine imposibil de atins dacă prozatorii urmează fișa. Riscul RS24 s-a materializat, iar S K1 nu e atins. | Adăugați AP-13 („`STYLE` contrazice canonul, secțiunea 12; se aplică canonul”); rescrieți sarcina 1 din §4.9 (forma fiecărei povestiri după tabelul adoptat de canon din `02_RESEARCH/05_MODURI_DE_PREZENTARE.md`; `STYLE` rămâne numai pentru registrul limbii); KPI nou: „10/20 de ediții-pereche la persoana I (episoadele din tabel), 10/20 în celelalte forme; 20/20 cu ≥ 1 informație absentă din BD”; actualizați Anexa A și brief-ul D3–D6; procedura v5 corectează `STYLE`. |
| 4 | **MAJOR** | `01_ECHIPA_SI_ROADMAP.md` §3.3 (r. 152–160); §4.17–§4.19; §9.3 (H3, H4); §9.5; §10; jurnalul, B0 (r. 295); registrul central §10.5 | Posturile H2 (redactorul-corector), H3 și H4 **nu au titular definit**: nu sunt în lista agenților din §3.3 („S, MS, A, … GR-S”) și nici în lista persoanelor de numit până la 15.10.2026 (E2–E4, H1, H2.EN, H2.DE, H2.RV); fraza „Pentru H2, H3 și H4, Producătorul poate numi și persoane” nu fixează nici tipul titularului, nici termenul. Totuși H3 răspunde de testul de concept din 28–30.10.2026 (n ≥ 50 de respondenți reali, 14+, inclusiv minori), care condiționează culoarea Ep. 1 (02.11.2026) și lansarea din 01.12.2026, iar H4 are termen la 20.11.2026. Producătorului nu i se cere nicio decizie pentru ele (B0, registrul §10.5), nu există buget sau canal de recrutare pentru panel, iar §10 nu are riscul „eșantion neatins în 3 zile”. | Rând nou în §3.3 pentru H2, H3, H4: tipul titularului (agent lansat de procedura v5 sau persoană), cine numește și termenul (propunere: 09.10.2026; H3 cel târziu 15.10.2026); decizie nouă cerută Producătorului (buletinul următor și registrul): numirea H3 și H4 și bugetul testului; riscul RS27 „recrutarea n ≥ 50 în 28–30.10.2026”, cu măsura (panel contractat până la 16.10.2026, recrutarea deschisă după avizul H1 din 23.10.2026) și indicatorul. |
| 5 | minor | §6.2 (b), coloana „Fișiere”; §5.1 | Rapoartele de echipă sunt în perimetrul auditului numai pentru A, B, C, E și D1. `S_showrunner.md`, `D2_scenariu.md`, `D3_proza.md` … `D6_proza.md`, `E2_desen.md`, `E3_culoare.md`, `E4_lettering.md`, `F1_web.md`, `F2_qa.md`, `H2_corectura.md` și `H4_dtp.md` nu intră în niciun cod, deci nu sunt auditate (consecința se vede la defectul 2). H1 și H3 nu au deloc raport, deși §5.1 cere unul fiecărui post de producție. | Adăugați raportul în lista de fișiere a fiecărui cod (`S_showrunner.md` la `G0-CANON-v4` și `G0-STUDIO-v4`); adăugați `00_STUDIO/rapoarte/H1_juridic.md` și `H3_marketing.md` sau declarați excepția în §5.1. |
| 6 | minor | §12, rândul v4.0 („Showrunnerul delegat (autorul `G0-STUDIO-v4`)”); jurnalul, antetul (r. 5) și r. 224 | „Showrunner delegat” e, prin definiție, managerul de ședință (§3.1, titlul §4.2), care „nu editează livrabilul” (MS K5) și are numai drept de citire pe jurnal (§8.2). A-l numi autor al livrabilului creează o ambiguitate de independență exact pe principiul pe care Producătorul l-a cerut (reziduul KC-m11). | Înlocuiți peste tot cu „Showrunnerul (agentul `scrie G0-STUDIO-v4`)” sau definiți în §3.3 un termen distinct (de exemplu, „autorul delegat”), diferit de MS. |
| 7 | minor | §4.23 GR K1; §9.3, rândul GR · I (r. 1211) | GR K1 cere `REZULTAT_FINAL.md` în ≤ 24 h de la oprire (oprirea: 24.09.2026, 05:45:31, deci până la 25.09.2026, 05:45), dar roadmapul fixează „2/2 dosare oprite închise … până la 28.09.2026”. Termenul rândului GR · I, 31.10.2026, cade într-o **sâmbătă** (toate celelalte rânduri ale Etapei I: 30.10.2026). | Aliniați: fie termenul 25.09.2026 în roadmap, fie o excepție declarată în K1 pentru opririle anterioare numirii GR; termenul rândului: 30.10.2026. |
| 8 | minor | §4.11 K1, K6; §4.12 K1, K6; §4.13 K1, K6; §4.17 K5; §9.3, rândul H2 · I | 7 KPI măsoară acțiuni ale Producătorului, nu performanța postului (confirmarea capacității, costul pe pagină, numirea traducătorilor). În plus, rândul H2 · I cere „5/5 titulari numiți”, iar H2 K5 numește doar H2.EN, H2.DE și H2.RV (4 persoane). | Mutați aceste ținte în „Jaloanele Producătorului” (§9.6) sau în lista deciziilor așteptate; înlocuiți-le în fișe cu KPI de performanță (de exemplu, E2: „pagini predate / planificate pe lună ≥ 100%”); aliniați 5/5 cu K5. |
| 9 | minor | §9.3 (regula din r. 1148); rândurile A1–A6 · II–III | E2, E3, E4, H1, H3 și H4 nu au rând în Etapa I și nici justificarea scrisă cerută de regula din §9.3; H1 e chiar activ în Etapa I (avizele cerute de canon la G1, RS26, H1 K7; avizul din 23.10.2026). Controlul „24/24 de posturi acoperite” al autoverificării ascunde golul. Rândul A1–A6 · II–III are termenul 05.10.2026 și poarta G1, anterioare etapei. | Adăugați 6 rânduri (H1 · I cu livrabile și termene; celelalte cu justificarea „neactiv în Etapa I”); rândul A1–A6 · II–III: termen „–”, poartă „–”. |
| 10 | minor | Anexa B, RZ-20; registrul central §10 | Interimarul, autorul livrabilului auditat, a eliminat un rând gol dintr-un rând existent al registrului. Intervenția e declarată, dar contrazice regula 1 din §7.3 („nimic din arhivă … nu se editează retroactiv”) și GR-S K4 („0 rânduri existente modificate”), fără o excepție scrisă în §7.3. | Adăugați în §7.3 excepția „corecturi de formă care nu schimbă conținutul, consemnate în registru și validate de GR-S” sau lăsați corectura pe seama GR-S. |
| 11 | minor | §11.1, coloana „Unde apare prima dată” | 5 intrări greșite: „plot, ploturi” (prima apariție: §2, r. 75, nu §4.3); „pitch” (§4.14, r. 491, folosit înainte de definiția din §4.18); „PASS / FAIL” (antetul, r. 9, nu §2); „OPRIT, EROARE_API” (§4.23–§4.24, nu §6.3 (i)); „webtoon, manga, anime” („manga” apare în §3.3, r. 154). | Corectați coloana sau glosați termenii la prima apariție reală. |
| 12 | minor | §6.2 (a), poarta GL; §9.1 (Etapa II: „GS (Ep. 2–5)”); §9.3 (D2, D1) | Regula (j) cere o rundă nouă după corectura H2 a povestirilor Ep. 1–5 (20.11.2026), înainte de publicarea din 01.12.2026, dar aceste runde nu apar în nicio poartă și în niciun termen. Scenariile Ep. 6–7 au PASS la 27.11.2026 (Etapa II), dar sunt trecute numai în rândurile Etapei III; D1 · II verifică indiciile numai pentru Ep. 2–5. | Adăugați în GL „rundele (j) ale `D3-EP01` … `D3-EP05`, 23–26.11.2026”; mutați Ep. 6–7 în rândurile D2 · II și D1 · II și în §9.1. |
| 13 | minor | §4.7 (D1 K1, K7); §4.9 (D3–D6 K3); față de canonul, secțiunea 12, ingredientul 8 | Ingredientul obligatoriu „Momentul de stil și de merit” (lecția de succes prin merit sau gestul de generozitate, pe fiecare episod) nu are KPI la nivel de episod: harta celor 20 de episoade (14 câmpuri) nu îl conține, iar decizia 14 e verificată numai global (§2). | Câmp nou în D1 K1 („lecția de merit / gestul de generozitate”) și ținta „20/20 de episoade” în D1 K7 și D3–D6 K3. |
| 14 | minor | §7.1 (arborele); §7.2 (rândul `R0_versiune_initiala/`); §7.3, regula 8 | Arborele omite dosarul existent `G0-CANON-v4/`, a cărui structură nu e conformă (`R0_versiune_initiala/verificari_automate/` în loc de `R0_verificari_automate/`, fără copia livrabilului), și subfolderele reale `iteratia_1/`, `iteratia_2_preliminar/` și `surse_asamblare/` din `G0-STUDIO-v4/R0_verificari_automate/`. §7.2 definește R0 „imediat după prima scriere”, dar R0-ul real e a treia iterație, cu alte două copii „R0_versiune_initiala_*” păstrate în anexe. | Completați arborele cu starea reală și cu neconformitatea `G0-CANON-v4`; reformulați §7.2: „R0 = versiunea predată; iterațiile anterioare se păstrează în `R0_verificari_automate/iteratia_<n>/`”. |
| 15 | minor | Anexa A (8.353 de cuvinte, 22% din document); documentul întreg (37.813 cuvinte, circa 150 de pagini) | Anexa A reproduce integral textul celor 188 de KPI, deja prezent în fișe, iar 43 de celule sunt identice („— (procedura v4 nu are brief pentru acest post; …)”). Documentul de organizare devine greu de folosit ca instrument de lucru zilnic. | Păstrați în Anexa A numai rolul, codul KPI, cerința brief-ului, referința și concordanța (textul KPI rămâne numai în fișă); comprimați celulele repetate într-o notă. |
| 16 | minor | §4.8 D2 K2; §9.4, rândul Ep. 1 | Nu e precizat dacă pagina-titlu fixă (p. 4, canonul, secțiunea 12) e splash page-ul sau una dintre cele 21 de pagini standard (4–6 panouri): KPI-ul poate fi măsurat în două feluri. Fereastra specială a Ep. 1 (desen în 10 zile lucrătoare, față de 12 la celelalte, adică 2,4 pagini pe zi față de circa 2,2 la 48 de pagini pe lună) nu e justificată; tabelul lunar de capacitate o maschează. | D2 K2: „p. 4 = pagina-titlu (nu intră în cele 21)” sau invers, explicit; în §9.4, o notă cu justificarea ferestrei Ep. 1 și cu confirmarea capacității suplimentare în ziua de 15.10.2026. |
| 17 | minor | jurnalul §2 (rândurile A, B, C, E, F1) față de B0 (r. 294); `S_showrunner.md` r. 34 | §2 enumeră 20 de fișiere cu formula eliminată, iar B0 anunță 21: al 21-lea, `S_showrunner.md`, lipsește din §2. Raportul S redă formula eliminată într-o listă de „șiruri interzise”, contrar convenției „[…]” adoptate în §2 (principiul 8) și în Anexa J. | Adăugați `S_showrunner.md` în §2 (rândul `G0-STUDIO-v4` sau `G0-CANON-v4`); în raport, „[formula eliminată prin decizia 9]”. |
| 18 | minor | jurnalul §8 (antetul B0); §4.1 K10; §9.3, rândul S · I | Antetul B0 nu urmează șablonul §5.5 (lipsește „săptămâna zz.ll–zz.ll”). K10 cere un buletin „în fiecare vineri”: între 25.09 și 30.10.2026 sunt 6 vineri, deci, cu B0 (joi, 24.09), 7 buletine; roadmapul cere „6/6 (B0–B5)”. | Antet conform șablonului; precizați în K10 dacă B0 ține loc de buletinul din 25.09.2026 și aliniați roadmapul (6 sau 7). |

## 8. Concluzie

Livrabilul `G0-STUDIO-v4` îndeplinește cantitativ aproape toate cerințele: 24/24 de fișe, 188/188 de KPI concordanți, roadmap datat pe etapele Producătorului, calendar BD corect la zi, arhivă și registru bine proiectate, 0 urme ale canonului vechi, 0 defecte de diacritice. Nu poate trece la 9,50 pentru că:

1. **jurnalul raportează o arhivă care nu există** (R0 al canonului v4, fără copie și cu amprenta necorespunzătoare) și omite evenimentul de integritate;
2. **raportul Showrunnerului nu respectă șablonul v4** și conține afirmații false despre arhivă;
3. **fișa prozatorilor contrazice canonul v4** (persoana a III-a peste tot, față de rotația formelor din canonul, secțiunea 12);
4. **H2, H3 și H4 nu au titular**, deși testul de concept (H3) e pe drumul critic al lansării din 01.12.2026.

Toate patru se pot închide într-o singură revizie, fără restructurarea documentului. Împreună cu cele 14 minore, revizia trebuie să producă: rândul corectat și evenimentul de integritate în jurnal, raportul S rescris pe șablon, AP-13 și KPI-urile noi ale prozei, titularii H2–H4 cu termenele și riscul RS27. Recomand ca runda R2 să ruleze din nou recalcularea independentă a calendarului și comparația Anexa A–fișe, care în această rundă au ieșit fără nicio abatere.

**Notă de independență:** în timpul acestei runde a apărut în dosar `R1_audit_craft.md`; nu l-am deschis. Singurul fișier creat de acest auditor este prezentul raport.
