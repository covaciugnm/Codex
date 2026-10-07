# Raport de audit · Canon & Istorie · G0-STUDIO-v4 · Runda R2

| Câmp | Valoare |
|---|---|
| **Livrabil** | [G0-STUDIO-v4] Organizarea studioului v4 (echipa, modul de gândire, sarcini, raportare, roadmap pe membri, Poarta 9,50, arhivare) și jurnalul de progres; versiunea v4.1, predată pentru R2 după revizia R1 |
| **Cod** | `G0-STUDIO-v4` · poarta G0 (termen: 28.09.2026) |
| **Runda** | R2 (a doua rundă a codului; versiunea auditată = v4.1, predată la 24.09.2026, 08:50) |
| **Auditor și lentilă** | AU-C, Auditor de Canon & Istorie (agentul `audit G0-STUDIO-v4 R2 canon`); complet nou, fără memoria rundei R1; nu a contribuit la livrabil |
| **Data** | 24.09.2026 |
| **Fișiere auditate (citite integral)** | `D:\00. Downloads\Dracula Book\DRACULA-COMICS\00_STUDIO\01_ECHIPA_SI_ROADMAP.md` · 1.782 de rânduri · 37.802 cuvinte (`wc -w`) · 247.037 B · modificat 24.09.2026 08:50:14 · SHA-256 `55bbd54cf2fbfbbd2ee1aead32ddd2738ec48a9d1d359eb57fa8a6f069084acd`<br>`D:\00. Downloads\Dracula Book\DRACULA-COMICS\00_STUDIO\03_JURNAL_PROGRES.md` · 408 rânduri · 10.951 cuvinte · 75.378 B · modificat 24.09.2026 08:50:15 · SHA-256 `338f22c39e4fce70876fe2fdceef8d0aaa26b7bc8cdc0b8f590c83ea7c0dd2cf` |
| **Perimetrul declarat de livrabil (§6.2 (b))** | de la R2, codul include și `D:\00. Downloads\Dracula Book\DRACULA-COMICS\00_STUDIO\rapoarte\S_showrunner.md` · 513 rânduri · modificat 08:38:43 · SHA-256 `55e49315f8a4d3cb430a5e2435ec4fc8cd959b6058f03fa8a1e3cf1a81af7f33`. Instrucțiunea de audit a listat doar cele 2 fișiere de mai sus; am citit antetul raportului S și secțiunea integrală `G0-STUDIO-v4` (r. 1–14, 199–413), pe lentila mea |
| **Concordanța cu predarea (regula (d))** | amprentele recalculate de mine sunt identice cu `R1_plan_masuri.md`, „Execuție”, E.1 (și cu `R1_verificari_automate/SHA256SUMS_predare_R2.txt`): livrabilul nu s-a modificat de la predare |
| **Referințe citite** | registrul Producătorului `D:\00. Downloads\Dracula Book\DRACULA-COMICS\01_CANON\01_DECIZII_PRODUCATOR.md` (integral; SHA-256 `dd0128b800270b219435b0b841f39232146fb96f88da94047e356817b8e44bdf`, modificat 07:55:04; identic cu antetul jurnalului) · canonul `D:\00. Downloads\Dracula Book\DRACULA-COMICS\01_CANON\00_CANON_NUCLEU.md` v4.0 (secțiunile 1–16 integral, 20 pe sondaj; SHA-256 `9d7b97be97b753ca01e95e7c38f8175a39858b397071a5c769a120f545217b2e`, 742 de rânduri, modificat 06:20:02; identic cu antetele ambelor fișiere, V24) · `00_STUDIO/audit/00_CONTRASEMNARI_PRODUCATOR.md` (integral) · `00_STUDIO/audit/G0-STUDIO-v4/R1_audit_canon.md` (integral) · `00_STUDIO/audit/G0-STUDIO-v4/R1_plan_masuri.md` (§1–§6 și Execuția E.1–E.3) · `02_RESEARCH/05_MODURI_DE_PREZENTARE.md` §6.6 · registrul central `00_STUDIO/audit/00_REGISTRU_AUDIT.md` (diff-ul reviziei) |
| **Procedura în vigoare (K8)** | `00_STUDIO/audit/00_PROCEDURA_PIPELINE_v4.js` · SHA-256 `2c13db6a6d9a8817e70538fa8df4ff7c7ba6378140c0102590db53e3ad403ead` (identică cu §6.6 și cu jurnalul) |
| **Registrul central la audit** | `00_STUDIO/audit/00_REGISTRU_AUDIT.md` · SHA-256 `5c529a6426054622a322ac1981e482e1f243a660c8d635af69d1f5f3a1c2556a` (08:31:48) |

## 1. Nota și verdictul

| Nota | Verdict |
|---|---|
| **8,85 / 10** | **FAIL** (sub pragul de 9,50) |

**De ce:** 0 defecte critice, **4 defecte majore** (plafon 9,20) și 3 defecte minore. Revizia R1 a fost executată serios: toate cele 14 defecte ale AU-C din R1 sunt închise în conținut, tabelul deciziilor e identic cu registrul (15/15), trimiterile la canon sunt exacte, iar arhiva G0 corespunde acum discului. Livrabilul nu trece pentru că: (1) jurnalul și organizarea dau două date diferite pentru finalul Sezonului 1; (2) lista urmelor canonului vechi, declarată completă, omite o siglă și o pagină care conțin încă formula eliminată prin decizia 9 (verificarea automată V9 e sensibilă la majuscule); (3) temeiul legal al regimului minorilor e citat greșit; (4) calendarul tranșelor publică proza Ep. n+1 înaintea BD-ului Ep. n în 16 din 18 tranziții, inclusiv înaintea pivoturilor Ep. 10 și Ep. 15, fără nicio regulă care să protejeze ce află cititorul și când.

## 2. Metoda de verificare

1. **Citire integrală**, rând cu rând: organizarea (1.782 de rânduri, în 11 tranșe) și jurnalul (408 rânduri, în 4 tranșe), cu notarea fiecărei afirmații istorice, a fiecărei trimiteri la canon sau la registru și a fiecărei date. Raportul S: antetul și secțiunea `G0-STUDIO-v4`.
2. **Registrul Producătorului**, citit integral; tabelul din §2 al organizării comparat automat, rând cu rând, cu registrul (script Python, după înlocuirea celor 2 formule declarate cu „[…]”): **15/15 rânduri identice**.
3. **Canonul v4.0**: am verificat fiecare trimitere a organizării. Secțiunile citate efectiv (extrase automat): 1, 2, 3, 3.1, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16.1 (plus 9 prin intervalul „8–10” din Anexa A), deci antetul („secțiunile 1–3 și 5–16”) e corect. Verificate pe text: „Metoda Ostaticului” (secțiunea 2); cele 17 momente 1431–1476 (secțiunea 3, ≥ 15); cele 10 personaje istorice din fișa B (toate în secțiunea 3); regula anacronismelor (secțiunea 5, redată identic în 4 locuri); popasurile italiene #2, #3, #19 (RS27); R4–R5 (inelul, umbra); art. 6; conții de Făgăraș (secțiunea 8); dezvăluirea antagonistului la finalul S2 (secțiunea 10); ingredientele 1–8, pivoturile, structura celor 24 de pagini, aparatul, pragul #2–#24, albumul cartonat și „Ceasul finalului” (secțiunea 12); sigla fără semilună și „doar mustață 1448–1476” (secțiunea 13); regulile 4, 7, 11, 12, 13 și acțiunile pendinte (secțiunea 14); comparabilele (secțiunea 15); V4-09, V4-10, V4-24, V4-28, V4-30, V4-42 și tabelul 16.2.
4. **Căutări automate** (`grep -i`, `sha256sum`, `find`, Python): 0 caractere cu sedilă; 0 apariții ale formulei eliminate și ale numelui de lucru anulat în cele 2 fișiere; toate mențiunile „soție/soția” sunt conforme deciziei 13; căutarea pe tot proiectul (insensibilă la majuscule) a urmelor canonului vechi, comparată cu lista din jurnal și cu tiparul V9 din `R1_verificari_automate/verificari_v4_1.py` (r. 133); inventarul din jurnal §4 recalculat (identic pentru toate folderele din afara `audit/`); amprentele arhivelor R1 (`R1_versiune_inainte_de_revizie/` 27/27 OK; ancorarea `G0-CANON-v4` 3/3 OK; `G0-CANON/STARE_LA_OPRIRE/` 2/2 OK; `G0-CANON-v4/R0_versiune_initiala/SHA256SUMS.txt` 7/7 OK); diff-ul registrului central: 0 linii șterse.
5. **Continuitatea datelor**: toate datele-jalon din jurnal comparate cu §9.1–§9.6; zilele săptămânii pentru 42 de termene (script); tabelul tranșelor (§9.4) comparat cu tabelul publicărilor BD, pe tranziții Ep. n → Ep. n+1; tamponul recalculat pentru Ep. 1, 2 și 20 (10/7, 12, 20 de zile lucrătoare: conform).
6. **Decizia 3**: am căutat în cele 2 fișiere numele seriilor editurii (NOIR, AMORIS, MYTHICA, AURORA) și numele de personaje din catalogul editurii (Melina Kyriazi, Isabella Morgan, Arden Vale, „Umbra Trandafirului Negru”, Marienburg, Schäßburg): apar numai ca excludere. 0 preluări.
7. **Verificări pe web** (surse în §7): Legea nr. 190/2018, art. 5 (textul primar); Regulamentul (UE) 2025/2509; Directiva 2009/48/CE, anexa I. Afirmațiile istorice și de reper verificate (pe surse și pe canon): Van Dine 1928, Knox 1929; Bond, romanele din 1953 și filmele din 1962; Stoker 1897; *Dracula* (Universal, 1931), în domeniul public în SUA la 01.01.2027; *Lucifer* 2016–2021; anii de sânge 1456–1462; Bastilia (demolată din 1789); vechea Sf. Pavel (arsă în 1666); Mihnea ucis la Sibiu în 1510; arestarea din 26.11.1462; Beheim 1463; tipăriturile 1488–1500; Fronda 1648–1653; Afacerea otrăvurilor 1677–1682; Galigaï 1617; Loudun 1634; Podul Suspinelor 1600–1603; Opera din Viena 1869; Chrysler 23.10.1929 / 27.05.1930; *Walk of Fame* 1958–1960; Rosetti la Snagov 1933; moartea lui Vlad între sfârșitul lui decembrie 1476 și 10.01.1477; Zilele Babei 1–9 martie; D.Lgs. 42/2004, art. 107–108; Legea nr. 8/1996; Codul muncii, art. 139; marja ±9,8 puncte procentuale la n = 100 (95%). **Toate corecte**, cu excepția citării Legii nr. 190/2018 (defectul 3).

## 3. Lista de control a celor 15 decizii blocate (KPI AU-C K7)

| # | Decizia | Verdict | Dovada |
|---|---|---|---|
| 1 | Eroul = Vlad al III-lea (n. 1431, Sighișoara) | ✅ respectată în livrabil | §1, §2 (tabelul identic); 0 apariții ale numelui anulat în cele 2 fișiere; ⚠️ lista pe proiect omite 2 fișiere C cu șirul eliminat de canon (defectul 2) |
| 2 | 1431–1476 strict istoric | ✅ respectată | B K2, C K1–K2, F2 K5, AU-C K1, H5 (§4.25); nicio dată istorică greșită în cele 2 fișiere |
| 3 | Continuitate proprie | ✅ respectată | B K7, F2 K4, AU-C K4; 0 preluări (metoda, pct. 6); §9.4 leagă strategia editurii numai de calendar |
| 4 | Capitalele, obiectivele, clișeele | ✅ respectată | regula anacronismelor identică cu canonul, secțiunea 5, în §2, §4.6, C K6, RS12; OBS-3 marcată ca regulă a studioului |
| 5 | Supererou pozitiv, familia, *Saga* | ✅ respectată | §1, §2 (principiile 4–5), §4.5 |
| 6 | Română cu diacritice; prompturile în engleză | ✅ respectată | 0 sedile; E K7; glosarul §11 |
| 7 | Poarta 9,50 și arhivarea | ✅ respectată | §6, §7; arhiva G0 = discul (V29 confirmat de mine pe dosarele G0); contrasemnarea aplicată în §6.3 (g) |
| 8 | Surse din orice gen | ✅ respectată | citatul literal (principiul 11); A K2, K4 |
| 9 | Titlul DRACULA; formula eliminată peste tot | ⚠️ respectată în livrabil; **starea proiectului raportată incomplet** | 0 apariții în cele 2 fișiere; lista din jurnal §2 și avizul din raportul S omit `05_ART/logo/dracula_monograma_sigiliu.svg` și `05_ART/layout/pagina_03_splash.svg` (defectul 2) |
| 10 | Acțiune și ziua | ✅ respectată | D1 K5, K14; D2 K6; C K9; principiul 10 |
| 11 | Fashion icon | ✅ respectată | B K3, E K3, C K6 |
| 12 | Stil Bond | ✅ respectată | A K7, D1 K7, E K4, RS18–RS19 |
| 13 | Fără soție în prezent; femeia episodului; 14+ | ✅ respectată | B K8–K9, D1 K6, D3–D6 K5; 0 mențiuni ale Sânzianei ca soție în prezent |
| 14 | Fantezie aspirațională, merit, generozitate | ✅ respectată | tabelul ingredientelor (8/8), D1 K13, D2 K6, D3–D6 K3, testul 20/20 din §2 |
| 15 | Despărțirea de la Paris (1794); planurile S contrasemnate | ✅ respectată | rândul 15 identic; §6.3 (g); jurnalul DP-15 și intrarea 07:55:04, coerente cu `00_CONTRASEMNARI_PRODUCATOR.md`; confirmarea opririi G0 v3 corect lăsată „în așteptare” (§9.7) |

## 4. Închiderea sarcinilor R1 (regula (e); raportată separat de notă)

### 4.1 Sarcinile planului `R1_plan_masuri.md` (46)

**Bilanț pe lentila mea:** 45 închise (3 dintre ele cu un defect nou, semnalat în §6) · 1 parțială (M1.16) · 0 neînchise.

| Sarcina | Starea | Dovada verificată |
|---|---|---|
| M1.1 | închisă | `R1_versiune_inainte_de_revizie/` cu `anexe_atinse_de_revizie/`; `sha256sum -c`: 27/27 OK |
| M1.2 | închisă | `G0-CANON-v4/R0_versiune_initiala/ancorare_ulterioara_07-34-13/`: 3/3 OK; copia = `9d7b97be…` |
| M1.3 | închisă | `G0-CANON/STARE_LA_OPRIRE/`: 2/2 OK; copia v3.1 = `d05bdb2e…` |
| M1.4 | închisă | jurnal: antet (r. 9), §2 (r. 33, „R0 incomplet”), evenimentul de integritate 06:20:02 (r. 295–305, 7/7 câmpuri), nota sub citatul 06:18:48 (r. 291), §4 = discul, intrările R1 (r. 314–341) |
| M1.5 | închisă | diff-ul registrului: 0 linii șterse, rânduri „de validat de GR-S” |
| M1.6 | închisă | raportul S: secțiunea `G0-STUDIO-v4` după §5.2, conformitatea 15/15, „Stare audit” 4/4 coduri |
| M1.7 | închisă | antetul organizării (r. 11) cu amprenta completă; §6.4, pct. 3; amprenta = canonul viu |
| M1.8 | închisă | §2, tabelul ingredientelor 8/8 (r. 155–166); D1 K1 (18 câmpuri), D1 K13, D2 K6, D3–D6 K3; testul deciziei 14 (r. 150) |
| M1.9 | închisă | AP-13 (r. 1069); §4.9 cu tabelul de rotație, identic cu `02_RESEARCH/05_MODURI_DE_PREZENTARE.md` §6.6; K8–K10; brief-ul D3–D6 (5 mențiuni AP-13) |
| M1.10 | închisă | regula identică în 4 locuri (r. 140, 384, 405, 1571) |
| M1.11 | închisă | „#2–#24” în D1 K3, G2, faza 2, D1 · I |
| M1.12 | închisă | albumul cartonat nr. 1 implicit; varianta B = OBS-5; H4 K1–K3 condiționate |
| M1.13 | închisă | jalonul 26–27.12.2026 (§9.6), H3 K8, rândul A · III, §9.7, RS30, OBS-4 |
| M1.14 | închisă | RS27, RS28, H1 K2 = 11/11, criteriul G1, planul A/B, regula materialelor din §9.5 |
| M1.15 | închisă | 0 apariții „Canon §”; lista secțiunilor din antet = secțiunile citate (verificat independent) |
| M1.16 | **parțială** | termenul G1 și AP-15 sunt scrise, dar lista din jurnal §2 și avizul din raportul S sunt incomplete: omit `dracula_monograma_sigiliu.svg`, pe care managerul de ședință îl numise explicit (plan, §1.1, faptul 4), și `pagina_03_splash.svg` (defectul 2) |
| M1.17 | închisă | OBS-3…OBS-7 în jurnal §5.4 și în raportul S; canonul și registrul neatinse de revizie |
| M1.18 | închisă (defect nou) | regula 3 din §9.4, tabelul 19 × 4, rundele (j); regula acoperă însă numai dezvăluirile episodului propriu (defectul 4) |
| M1.19 | închisă | H3 K7, F1 K12, A · III, §1 |
| M1.20 | închisă | §9.7, 13.11.2026 |
| M1.21 | închisă | rezerva, stocul, scenariile B1/B2, E2 K8, RS15 cu declanșator; tampoanele recalculate de mine pentru Ep. 1, 2, 20: conforme |
| M1.22 | închisă | §9.5, două valuri, top-2-box, control, praguri |
| M1.23 | închisă | F1 K13; principiul 6; D2 K2 (1 + 21 + 2 = 24) |
| M1.24 | închisă | D1 K14; sarcina AU-M (surpriza) |
| M1.25 | închisă | H3 K9; RS32 |
| M1.26 | închisă | RS1, D1 K8, sarcina AU-M (*Lucifer*, 2016–2021, corect) |
| M1.27 | închisă | regula (l); `00_STUDIO/05_TITULARI.md` există; §8.2 |
| M1.28 | închisă | `S-PROC-v5`, GPR, K8 la cei 3 auditori, §6.7 |
| M1.29 | închisă | arborele §7.1 = discul pentru dosarele G0 (verificat) |
| M1.30 | închisă | §7.3, regula 1; GR-S K4 |
| M1.31 | închisă | GR K1 (28.09.2026); GR · I 30.10.2026 (vineri) |
| M1.32 | închisă | §6.2 (b), coloana „Fișiere” |
| M1.33 | închisă | „Showrunner delegat” numai în rândul MS și în titlul §4.2; AP-14 |
| M1.34 | închisă | §3.3, rândurile H2, H3, H4 |
| M1.35 | închisă | E2–E4 K1, K6; H2 K5 |
| M1.36 | închisă | §9.3: rândurile Etapei I pentru E2, E3, E4, H1, H3, H4, H5 |
| M1.37 | închisă (defect nou) | H1 K5 pe 4 canale, clasele 25 și 14, figurina (anexa I a Directivei 2009/48/CE, corect citată); citarea „Legea nr. 190/2018, art. 5”, prescrisă chiar de plan, e greșită (defectul 3) |
| M1.38 | închisă | `04_COSTURI_COLABORATORI.md` cu acces restrâns; §8.3, regula 1 |
| M1.39 | închisă | §4.25 H5; 25 de posturi = 25 de fișe; 22 + 6 + 4 + 5 = 37 de titulari (verificat) |
| M1.40 | închisă | §9.7, 17 rânduri |
| M1.41 | închisă | S K10 și S · I: 7/7; antetul B0 |
| M1.42 | închisă | jurnal r. 206 (Poenari, „prima lui soție”); §4.3 (1953/1962); citatul deciziei 8, literal |
| M1.43 | închisă | §6.2 (c) |
| M1.44 | închisă (dovada: Execuția, V36) | nu am reverificat integral glosarul (în afara lentilei) |
| M1.45 | închisă (dovada: Execuția) | „Pe scurt” prezentă; Anexa A: 213 coduri declarate |
| M1.46 | închisă | amprentele din E.1 = amprentele recalculate de mine |

### 4.2 Defectele AU-C din R1 (CI4-1 … CI4-14)

| Defect R1 | Starea | Dovada |
|---|---|---|
| CI4-1 (major: arhiva G0 și adevărul jurnalului) | închis | jurnal r. 9, 33, 291, 295–305; dosarele G0 verificate pe disc |
| CI4-2 (major: ingredientele 3 și 8) | închis | tabelul 8/8; D1 K13; D2 K6; D3–D6 K3; testul deciziei 14 |
| CI4-3 (aria H1) | închis | RS27, RS28, H1 K2 = 11/11 |
| CI4-4 (avizele H1 de la G1) | închis | planul A/B, OBS-6, criteriul G1 |
| CI4-5 (regula anacronismelor) | închis | text identic + OBS-3 |
| CI4-6 (Râul Doamnei, „pe atunci soția lui”) | închis | jurnal r. 206 |
| CI4-7 (buletinele; termenul GR) | închis | S K10 7/7; GR K1 |
| CI4-8 („Bond de 60 de ani”) | închis | §4.3 r. 301 |
| CI4-9 (26/27.12.2026 lipsă) | închis | §9.6, H3 K8, §9.7, RS30, OBS-4 (dar vezi defectul 1: jurnalul a rămas cu finalul S1 vechi, citat chiar în CI4-9) |
| CI4-10 (pragul #2–#24) | închis | D1 K3 etc. |
| CI4-11 (formatul primului volum) | închis | albumul implicit, OBS-5 |
| CI4-12 (igiena trimiterilor) | închis | antet, V27 |
| CI4-13 (arborele arhivei; RZ-20) | închis | §7.1; §7.3, regula 1 |
| CI4-14 (decizia 9 tolerată până la G5) | închis pe termen (G1) | lista fișierelor de aliniat e însă incompletă (defectul 2) |

## 5. Puncte forte

1. **Coerența cu registrul:** tabelul din §2 e identic cu registrul, rând cu rând (15/15, verificare automată), cu cele 2 intervenții declarate; „Pe scurt” rezumă fidel cele 15 decizii.
2. **Trimiterile la canon sunt exacte:** peste 100 de citări „canonul, secțiunea n” verificate (secțiunile 1–3, 5–8, 10–16.1), nicio trimitere greșită; lista secțiunilor din antet corespunde citărilor efective.
3. **Exactitatea istorică** a celor două fișiere e foarte bună: peste 40 de afirmații istorice, juridice și de reper verificate, toate corecte, cu o singură excepție (defectul 3).
4. **Canonul e redat, nu reinventat:** ingredientele 1–8, structura celor 24 de pagini, pragul #2–#24, pivoturile, rotația formelor prozei, regula anacronismelor, albumul cartonat; abaterile trec corect prin propuneri de canon (OBS-3…OBS-7), acceptate de planul `G0-CANON-v4` (ARB-C16).
5. **Arhiva și jurnalul spun adevărul despre G0:** R0 incomplet, evenimentul de integritate de la 06:20:02, ancorarea declarată ca atare, `STARE_LA_OPRIRE/` tardiv, toate consemnate și verificabile pe disc (amprente OK).
6. **„Cine știe ce și când” în studio:** identitatea antagonistului nu apare în niciun fișier auditat; matricea de acces și abaterile AP-1, AP-3 sunt coerente.
7. **Decizia 2 are acum o garanție umană:** postul H5, cu aviz scris pe secțiunea 3 și pe flashback-urile 1431–1476, la G3 și la GS.

## 6. Tabelul defectelor

| Nr. | Gravitate | Locația | Problema | Corectura concretă |
|---|---|---|---|---|
| 1 | **MAJOR** | `03_JURNAL_PROGRES.md`, §1 „Starea fazelor”, r. 27 (rândul „Etapa III”, coloana „Note”) față de `01_ECHIPA_SI_ROADMAP.md` r. 38, 272, 1283, 1307, 1346, 1372, 1410, 1454, 1479, 1481, 1528 | **Contradicție între cele două fișiere ale livrabilului privind finalul Sezonului 1.** Jurnalul, într-o secțiune de stare actualizată „la 08:50” și declarată aliniată la „§9 al organizării v4.1” (r. 16), dă „finalul S1: **28.10.2027**”. Organizarea v4.1 (calendarul cu rezervă, §9.4, și jalonul §9.6) dă **16.11.2027** în 11 locuri; 28.10.2027 era data v4.0 (R0 o conține de 10 ori), exact data invocată de defectul CI4-9 din R1. Revizia a actualizat organizarea, dar nu și tabelul de stare al jurnalului. O dată-jalon greșită, prezentată ca stare curentă, încalcă cerința „jurnal coerent cu starea reală” și S K3. | Jurnal r. 27: „finalul S1: 16.11.2027 (scenariul A; §9.4 și §9.6 din organizare)”. Adăugați în `verificari_v4_1.py` (sau în scriptul R2) o verificare nouă: fiecare dată-jalon din jurnal §1 (lansarea, figurina, finalul S1, termenele porților) = valoarea din §9.6. |
| 2 | **MAJOR** | `03_JURNAL_PROGRES.md` §2, r. 49 („V9 extins… 20 de fișiere”) și r. 40 (E-ARTA-v4: „8 fișiere”); `00_STUDIO/rapoarte/S_showrunner.md`, „G0-STUDIO-v4: aviz de aliniere la decizia 9”, r. 289–298 (în perimetrul R2, §6.2 (b)); organizarea §6.8 (V9) și S K9; cauza: `00_STUDIO/audit/G0-STUDIO-v4/R1_verificari_automate/verificari_v4_1.py`, r. 133 | **Lista urmelor canonului vechi, declarată completă, omite fișiere reale, între care o siglă.** Tiparul V9 e `re.compile(r'Contele Nop\|Count of the Night\|Valerian\|\bDrakon\b')`, fără `re.IGNORECASE` și cu `\b`. Căutarea insensibilă la majuscule găsește formula eliminată prin decizia 9 („DRACULA · CONTELE NOPȚII…”) și în `05_ART/logo/dracula_monograma_sigiliu.svg` și în `05_ART/layout/pagina_03_splash.svg`, absente din listă și din avizul de aliniere către E. Monograma fusese numită explicit de managerul de ședință (planul R1, §1.1, faptul 4). Decizia 9 cere eliminarea „peste tot (**sigle**, coperți, site, texte)”. În plus, `04_LUME/06_TRASEUL_CAPITALELOR.md` („Knyaz Vladimir Drakonov”, „Mademoiselle Drakonova”) și `04_LUME/01_CRONOLOGIE_SECOLE.md` („domnișoarei Drakonova”) conțin exact șirul pe care canonul l-a eliminat prin V4-30 (#9 = Drevlianski), iar `\bDrakon\b` nu îl prinde. Lista reală: 24 de fișiere (plus `09_SITE/__pycache__/build_site.cpython-312.pyc`), nu 20. Consecință: jurnalul raportează fals starea deciziilor 1 și 9 în proiect, iar criteriul G1 („0 apariții… inclusiv siglele din `05_ART/logo/`”) va fi măsurat cu un instrument care subraportează. | (a) V9: `re.IGNORECASE` și tiparul `Drakon` fără `\b` final (sau lista de șiruri interzise din verificarea canonului care a produs V4-30); rulare nouă, cu ieșirea arhivată. (b) Jurnal §2, r. 49 și r. 40: lista completă (24 de fișiere; `__pycache__` se șterge la regenerarea site-ului). (c) Avizul de aliniere din raportul S: E primește 10 fișiere (plus monograma și pagina splash), C primește 4 (plus cronologia și traseul, cu trimitere la V4-30). (d) Criteriul G1 și S K9 precizează că verificarea e insensibilă la majuscule și acoperă textul din SVG. |
| 3 | **MAJOR** | `01_ECHIPA_SI_ROADMAP.md` §9.5, rândul „Minorii și datele”, r. 1500; §10, RS16, r. 1575 (sursa: planul R1, ARB6 și M1.37 (a)) | **Temeiul legal al regimului minorilor e citat greșit.** Documentul întemeiază consimțământul parental sub 16 ani pe „Legea nr. 190/2018, art. 5; GDPR, art. 8”. Articolul 5 al Legii nr. 190/2018 privește **prelucrarea datelor în contextul relațiilor de muncă** (monitorizarea electronică și video a angajaților), iar legea nu conține nicio prevedere despre vârsta consimțământului digital. Pragul de 16 ani vine direct din GDPR, art. 8 alin. (1), pentru că România nu a folosit derogarea (13–15 ani). E o afirmație juridică falsă, prezentată ca fapt, într-o zonă de risc (datele minorilor), repetată în două locuri și trecută neobservată prin trei auditori și prin managerul de ședință. | În §9.5 și în RS16: „(Regulamentul (UE) 2016/679, art. 8 alin. (1): vârsta consimțământului digital e 16 ani; legislația română, inclusiv Legea nr. 190/2018, nu o coboară; confirmarea: H1)”. Nota de corectură se trece și în planul R2 (ARB6 și M1.37 (a) din planul R1 conțin aceeași citare), iar H1 primește verificarea explicită a temeiului în K5. |
| 4 | **MAJOR** | `01_ECHIPA_SI_ROADMAP.md` §9.4, regula 3 (r. 1381) și tabelul tranșelor (r. 1434–1454) față de tabelul publicărilor BD (r. 1389–1410); D3–D6 K10 (r. 488); F2 K9 (r. 634); H3 K5 (r. 697); RS30 (r. 1589); jurnalul OBS-7 (r. 198) | **Calendarul prozei dezvăluie banda episodului precedent, inclusiv două pivoturi, iar nicio regulă nu o interzice.** Regula tranșelor protejează numai episodul propriu („tranșele 1–3 ale Ep. n nu dezvăluie vinovatul, soluția, răsturnarea sau cârligul final” al Ep. n). Dar tranșa 1 a Ep. n+1 apare înaintea BD-ului Ep. n în **16 din 18 tranziții** (Ep. 4–5 și 7–20; de exemplu, Ep. 4: 13.01.2027, înaintea BD-ului Ep. 3 din 18.01.2027). Cele mai grave: **Ep. 11, tranșa 1, 02.06.2027, înaintea BD-ului Ep. 10 (04.06.2027), pivotul în care Ioana află adevărul** (canonul, secțiunea 12; R3; Protocolul Mureșan începe după Ep. 10), iar Ep. 11 e o ediție-pereche la persoana I, cu vocea lui Vlad; **Ep. 16, tranșa 1, 25.08.2027, înaintea BD-ului Ep. 15 (30.08.2027), pivotul în care Radu reapare**. Pagina 24 a fiecărui BD e „cârligul arcului lung”, iar proza episodului următor pornește, prin construcție, de după el. Continuitatea „cine știe ce și când” pentru cititor e neprotejată tocmai la pivoturile canonice, iar afirmația „76 de tranșe, 0 înaintea… BD-ului” (r. 1483) e adevărată numai pe episodul propriu. | (a) Regula 3 se completează: „Tranșele Ep. n+1 publicate înaintea BD-ului Ep. n nu conțin nimic din Ep. n (cazul, deznodământul, pivotul, cârligul p. 24) și nicio informație pe care cititorul o află abia în Ep. n.” (b) După pivoturile Ep. 5, 10 și 15, tranșa 1 a Ep. n+1 apare numai după BD-ul Ep. n (recalculare cu `calendar_bd_v4_1.py`: 3 tranșe înaintea BD-ului sau tranșe mai dese, cu ieșirea arhivată). (c) D3–D6 K10, F2 K9 și H3 K5 verifică și această condiție (numărătoarea F2: 57 de tranșe × 2 condiții); RS30 se actualizează. (d) OBS-7 se completează ca propunere de canon (precizarea variantei A). |
| 5 | minor | `03_JURNAL_PROGRES.md` §5.3, r. 178–186, față de §5.1 (r. 94, 107, 108, 133, 135) și de Anexa J3 (r. 389) | **Tabelul „Rândurile istorice schimbate de canonul v4” e incomplet**, deși §5.1 (r. 89) îl declară rezumatul schimbărilor v4 care privesc direct rândurile istorice. Lipsesc: C-P6 (v3.1: Chrysler „în construcție” → v4: #16 = 1920–1930, clădirea deschisă la 27.05.1930, V4-28); C-P8, SR-1 și J3, pct. 1 („barba scurtă doar în prezent” → v4: după 1477, barba și părul urmează moda epocii, canonul, secțiunile 2 și 5.2); B-A8 (Râul Doamnei: etimologia corectată, V4-42); B-A7 și SR-2 (plus regula decalajului, V4-25); A-2 (sursa gravurii corectată, V4-38). Cine citește jurnalul poate păstra fapte v3.1 depășite. | Adăugați cele 5 rânduri în §5.3 (sursa: canonul, secțiunea 16.2) sau reformulați r. 89: „§5.3 rezumă numai schimbările …; lista completă: canonul, secțiunea 16.2”. |
| 6 | minor | `03_JURNAL_PROGRES.md` §2, r. 39 (C-LUME-v4) și r. 38 (B-PERSONAJE-v4) | **Tipul urmei e atribuit greșit.** R. 39: „formula de titlu eliminată apare încă în `04_LUME/02_REGULILE_NOPTII.md` și în raportul C”. `00_STUDIO/rapoarte/C_lume.md` are 0 apariții ale formulei, dar conține numele de lucru anulat (decizia 1). Avizul din raportul S (r. 296) e corect. R. 38 nu menționează că raportul B și `03_PERSONAJE/01_VLAD_DRACULEA.md` conțin și numele anulat. | R. 39: „… formula eliminată în `04_LUME/02_REGULILE_NOPTII.md`; numele de lucru anulat (decizia 1) în raportul C”; r. 38: „formula eliminată și numele de lucru anulat”, ca în avizul din raportul S. |
| 7 | minor | `03_JURNAL_PROGRES.md` r. 203; `01_ECHIPA_SI_ROADMAP.md` §11.3, r. 1674–1680 | **Rămășițe ale v4.0 (14 decizii) într-un document v4.1 (15 decizii).** Jurnalul: „deciziile 1–14, în registrul `01_CANON/01_DECIZII_PRODUCATOR.md`” (registrul are 15). §11.3 descrie ținta ca „§2 (… tabelul deciziilor 1–14)”, „aceleași 24 de posturi”, „§9.1–§9.6”, „RS1–RS26”, deși v4.1 are 15 decizii, 25 de posturi (H5), §9.7 și RS1–RS32. | Jurnal r. 203: „deciziile 1–15”. §11.3: titlul „v2.0 → v4.1” și valorile curente (sau o coloană „v4.1”). |

**Totaluri:** 0 critice · 4 majore · 3 minore.

**Observație pentru GR-S și pentru Producător (nu e defect al livrabilului):** §6.2 (b) include `00_STUDIO/rapoarte/S_showrunner.md` în perimetrul `G0-STUDIO-v4` „de la R2”, dar instrucțiunea acestei runde a listat numai cele 2 fișiere. Am verificat secțiunea `G0-STUDIO-v4` a raportului S pe lentila mea (constatarea relevantă e în defectul 2). Recomand ca brief-ul rundelor următoare să listeze explicit și raportul S.

## 7. Surse web consultate

- Legea nr. 190/2018, art. 5 („Prelucrarea datelor cu caracter personal în contextul relațiilor de muncă”) și structura legii (fără prevederi despre minori): [SintactLegeFree, art. 5](https://sintact.ro/legislatie/monitorul-oficial/legea-190-2018-privind-masuri-de-punere-in-aplicare-a-16972363/art-5) · [Lege5, art. 5](https://lege5.ro/Gratuit/gi4dsnjugi2q/prelucrarea-datelor-cu-caracter-personal-in-contextul-relatiilor-de-munca-lege-190-2018?dp=gi3dimjwgq3dmmy) · [Euroavocatura, textul integral](https://www.euroavocatura.ro/print2.php?print2=lege&idItem=1306) · [Portal Legislativ](https://legislatie.just.ro/Public/DetaliiDocument/203151)
- Regulamentul (UE) 2025/2509 privind siguranța jucăriilor (publicat la 12.12.2025; în vigoare din 01.01.2026, aplicabil din 01.08.2030): [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2025/2509) · [UL Solutions](https://www.ul.com/news/ec-publishes-toy-safety-regulation-regeu-20252509)
- Directiva 2009/48/CE, anexa I („products for collectors… 14 years of age and above”): [EUR-Lex, versiunea consolidată](https://eur-lex.europa.eu/eli/dir/2009/48/2022-12-05/eng) · [Ghidul nr. 20 al Comisiei](https://www.assogiocattoli.eu/wp-content/uploads/2022/06/FinalGuidance_decorative-products_productsforcollectors.pdf)
- Celelalte afirmații (Van Dine, Knox, *Dracula* 1931, Codul muncii art. 139, D.Lgs. 42/2004, marca HOLLYWOOD) sunt neschimbate față de R1 și au sursele în `00_STUDIO/audit/G0-STUDIO-v4/R1_audit_canon.md`, §6; le-am confruntat cu textul v4.1 (identic) și cu canonul, secțiunile 3, 5 și 14.

## 8. Concluzia

Pe lentila Canon & Istorie, organizarea v4.1 e un document matur: registrul e redat fidel (15/15), canonul e citat exact și fără fapte canonice adăugate tacit, istoria verificată e corectă, iar jurnalul spune acum adevărul despre arhiva G0. Revizia R1 a închis toate cele 14 defecte ale mele din R1 și 45 din cele 46 de sarcini ale planului.

**Nu îl pot semna pentru trecerea porții**, din patru motive, toate ușor de corectat, dar de fond:
1. **Jurnalul trebuie să aibă aceleași date ca organizarea** (defectul 1: finalul S1).
2. **Starea deciziilor 1 și 9 în proiect trebuie măsurată cu un instrument corect** (defectul 2: V9 sensibil la majuscule; o siglă și o pagină cu formula eliminată lipsesc din listă).
3. **Nicio afirmație juridică fără temei exact** (defectul 3: Legea nr. 190/2018, art. 5).
4. **Proza nu are voie să dezvăluie nici episodul precedent**, mai ales pivoturile Ep. 10 și Ep. 15 (defectul 4).

Cu cele patru majore închise și cu minorele 5–7 corectate, livrabilul are, pe lentila mea, nivelul de 9,50 sau peste. Recomand managerului de ședință să verifice în planul R2 și citarea din planul R1 (ARB6, M1.37 (a)) și să ceară rularea V9 corectate înaintea predării pentru R3.

*AU-C, runda R2 · raport arhivat în ziua rundei (KPI AU-C K6) · `D:\00. Downloads\Dracula Book\DRACULA-COMICS\00_STUDIO\audit\G0-STUDIO-v4\R2_audit_canon.md`*
