# R4 — Audit independent KPI & Completitudine — G0-STUDIO-v4

**Data:** 24.09.2026. **Auditor:** AU-K, această sesiune, fără contribuții la revizii; fără agenți suplimentari.  
**NOTĂ: 8,35 / 10. Verdict: FAIL.** Pragul este 9,50 pentru fiecare auditor separat.

## 1. Perimetru înghețat și hash

ROOT: `D:\00. Downloads\Dracula Book\DRACULA-COMICS-CODEX-G0-20260924`.  
Pachetul obligatoriu: `00_STUDIO/audit/RELUARE_CODEX_20260924_120350/PACHET_AUDIT_01`, relativ la ROOT.

| Fișier din pachet | Octeți | SHA256 recalculat |
|---|---:|---|
| `00_STUDIO/01_ECHIPA_SI_ROADMAP.md`, v4.3 | 286927 | `d934ae4f3880962f1cc72ae8ee56dc213e40436a6ee43399dd274be344a853ac` |
| `00_STUDIO/03_JURNAL_PROGRES.md` | 83979 | `4285ae42e7c63dc34bef438b12eda0c9b5e5fc1ed0bc39f473a3a363a890016c` |
| `00_STUDIO/rapoarte/S_showrunner.md`, anexă de stare | 101294 | `3b32d634dcea786b7f907eb2c122e5ed6b43403e4cc193920179c375b2f616a0` |
| Canonul v4.2, referință | 168639 | `243630e9071df7c7ee15cbf9f079fdac69f1d292950daab42cf927f36aa9ab26` |
| Deciziile Producătorului | 6718 | `dd0128b800270b219435b0b841f39232146fb96f88da94047e356817b8e44bdf` |
| Contrasemnările | 1094 | `f5acdb54d286419b7cff509bf4183c2ec7471e57de0d21dacf34691978318588` |

**Manifestul pachetului:** SHA256 `ca227d6345d935317ffb4780b6cd8286a874fdb165f4eda3c18ba907536847ac`; **32/32 fișiere conforme la hash și dimensiune**, inclusiv toate cele 25 brief-uri. Fișierele principale au fost reverificate înaintea redactării.

Numerele de linie din constatări sunt unu-based, pe fișierele pachetului, cu liniile goale incluse. Referințele la planuri/verificări sunt în ROOT, nu în proiectul original. Raportul S este anexă de stare conform AP-16/ARB38, nu un al treilea fișier introdus retroactiv în perimetrul auditurilor vechi.

## 2. Metoda executată

Lectură integrală a celor trei fișiere principale: canon 873 linii, organizare 1.888, jurnal 470. Am citit deciziile 1–15 și contrasemnările, brief-ul S, execuțiile finale ale ambelor revizii, sarcinile M3.1–M3.31 și arbitrajele R3, precum și defectele AU-K R3. Am verificat stările curente relevante din anexa S, fără a revendica lectura integrală a tuturor anexelor sale istorice.

Verificări proprii, read-only, cu PowerShell/Python în memorie:
- SHA256 pe pachet, manifestul predării, baza izolată și instantaneele enumerate mai jos.
- Extragerea independentă a secțiunilor §4.1–§4.25 și compararea textelor de sarcini/KPI cu secțiunile **actuale** ale briefurilor; textul procedurii explicit istoric nu este tratat drept instrucțiune curentă concurentă.
- Numărarea independentă a categoriilor Anexei A.
- Compararea semantică a regulilor canonului cu riscurile/porțile/fișele studioului.
- Recalcularea numărului de tranșe și a ordinii față de datele BD din datele arhivate, fără importarea ori executarea scriptului autorului.
- Verificarea condiției porții GT direct în raport cu calendarul. Nu am refăcut exhaustiv calendarul de zile lucrătoare pentru scenariile A/B1/B2.

Nu am rulat verificatoare cu rădăcini hardcoded și nu am scris în producție. Rezultatele V1–V51 sunt tratate ca afirmații ale autorului, nu ca verdict independent.

## 3. Numărătoarea efectivă a fișelor și briefurilor

Unitate de sarcină: punct de listă imediat sub „Sarcini”. Un KPI compus se numără o dată după K<n>; nu pretind că numărul KPI este numărul tuturor obligațiilor atomice din proză.

| Rol / fișă | Puncte de sarcină | KPI fișă | KPI brief actual | Text sarcini/KPI |
|---|---:|---:|---:|---|
| S | 11 | 13 | 13 | identic |
| MS | 6 | 6 | 6 | identic |
| A | 8 | 11 | 11 | identic |
| A1–A6 | 4 | 6 | 6 | identic |
| B | 7 | 11 | 11 | identic |
| C | 8 | 12 | 12 | identic |
| D1 | 4 | 17 | 17 | identic |
| D2 | 4 | 10 | 10 | identic |
| D3–D6 | 5 | 12 | 12 | identic |
| E | 7 | 12 | 12 | identic |
| E2 | 3 | 8 | 8 | identic |
| E3 | 2 | 7 | 7 | identic |
| E4 | 3 | 7 | 7 | identic |
| F1 | 8 | 14 | 14 | identic |
| F2 | 7 | 11 | 11 | identic |
| H1 | 7 | 8 | 8 | identic |
| H2 | 3 | 5 | 5 | identic |
| H3 | 5 | 10 | 10 | identic |
| H4 | 4 | 5 | 5 | identic |
| AU-C | 5 | 8 | 8 | identic |
| AU-M | 5 | 9 | 9 | identic |
| AU-K | 3 | 8 | 8 | identic |
| GR | 3 | 5 | 5 | identic |
| GR-S | 7 | 8 | 8 | identic |
| H5 | 2 | 5 | 5 | identic |
| **Total: 25 fișe/brief-uri** | **131** | **228** | **228** | **0 diferențe** |

Anexa A, recalculată independent: **40 „=” + 52 „precizează” + 26 „mai strictă” + 110 „nou” = 228**, pe 25 roluri. Comparația exactă demonstrează sincronizarea celor două reprezentări; nu validează semantic o cerință greșită reprodusă în ambele, exemplu S-K05.

### Acoperirea brief-ului G0-STUDIO

Descompunere în **14 cerințe de control**, după obiectele cerute în brief, nu după numărul de cuvinte:

| Nr. | Cerință | Dovadă / rezultat |
|---|---|---|
| 1 | Echipa și modul de gândire | §1–§4, 25 fișe |
| 2 | Sarcini pentru fiecare post | 131 puncte, identice cu briefurile |
| 3 | Raportare de progres | §5, șabloane, jurnal și buletine |
| 4 | Roadmap pe membri, inclusiv controlul | §9.3, etapele I–III; nu certific fiecare celulă împotriva fiecărui brief |
| 5 | KPI numerici și livrabile | 228 KPI; țintele H3 acum explicite; S-K05 |
| 6 | Roadmap datat | §9.1–§9.7; defectul de dependență S-K03 |
| 7 | Fiecare post are verificatori | §6.7; AP-16–AP-19 explicite |
| 8 | Prag 9,50 și măsuri sub prag | §6.1–§6.3; nu este înlocuit cu media celor trei note |
| 9 | Arhivarea procesului | §7 și instantaneele verificate; limitele sunt declarate |
| 10 | Independență și contrasemnări | §6.3(g), MS K4; decizia 15 prevalează |
| 11 | Aliniere la deciziile/canonul curent | mecanism prezent, însă S-K01 și S-K02 deschise |
| 12 | Jurnal concordant cu realitatea | S-K04: inventar curent cu versiuni vechi |
| 13 | Raportul echipei după șablon | K1–K13 prezente; anexa S păstrează stări curente contradictorii, S-K04 |
| 14 | Limbă și eliminarea urmelor vechi | delimitări istorice respectate; scanarea exhaustivă V9 a întregului proiect nu a fost refăcută de mine |

### KPI Showrunner, aplicabilitate reală la G0

| KPI | Evaluare |
|---|---|
| K1 | Nu poate fi declarat 0: S-K01/S-K02/S-K03/S-K05 sunt neconcordanțe curente. |
| K2 | 25/25 brief-uri; 131 sarcini și 228 KPI identice. |
| K3 | Reluarea, R3 și predarea canonului sunt consemnate în aceeași zi; exactitatea tuturor stărilor nu rezultă din respectarea termenului (S-K04). |
| K4 | Planurile R1 canon și R3 studio sunt datate în ziua rundelor; nu recertific toate rundele istorice. |
| K5 | OBS-8/V4-83 și OBS-10/V4-87 consemnate; nu am recalculat fiecare timp de soluționare din întreg proiectul. |
| K6 | Integritate confirmată pentru eșantionul extins de manifest/instantanee de mai jos; validările GR/GR-S rămân distincte. |
| K7 | 7 runde istorice / 2 livrabile = 3,5 este declarat onest. Termenul de evaluare este G5/final; fără penalizare anticipată G0. |
| K8 | Aprobarea generală din decizia 15 există; nu cer o nouă contrasemnare pentru aceste planuri. |
| K9 | Mecanismul G0 și termenul G1 sunt separate; nu certific aici scanarea proprie completă V9. |
| K10 | B0 există; B1 este viitor la data pachetului. |
| K11 | Procedura v5 și GPR sunt viitoare; nu sunt cerute ca implementare G0. |
| K12–K13 | Rezultatele creative și măsurătorile publice sunt viitoare; nu se inventează valori. |

## 4. Defecte confirmate

| ID | Gravitate | Locație exactă | Probă și efect | Remediu verificabil |
|---|---|---|---|---|
| **S-K01** | **Critic: neconcordanță cu decizia aprobată** | Organizarea `:1677`, RS28; față de canon §14 regulile 4/11 și ROOT `G0-CANON-v4/R1_plan_masuri.md:144`, ARB-C3 | RS28 include **Orient Express** între „loc și instituții” și permite utilizarea „descriptiv, în interior”. Nota Producătorului pentru vehicule și ARB-C3, acoperit de decizia 15, cer nume fictiv pentru tren, cu numele real păstrat numai ca sursă/titlu citat; excepția cere decizie a Producătorului după H1. Studioul reintroduce o permisiune pe care planul aprobat a eliminat-o. Prevalența canonului ajută la rezolvarea conflictului, dar nu face regula operațională locală concordantă. | Elimină trenul din categoria locurilor în RS28; trimite la regula obiectelor/vehiculelor și la excepția numai prin Producător + H1. Verifică toate aparițiile numelui în documentele curente, distingând sursele și istoricul. Test semantic: utilizarea mărcii de tren în interior, fără acele aprobări, trebuie respinsă. |
| **S-K02** | **Major** | Organizarea `:1676`, RS27; canon `:473`, §14 regula 13 | „în interior, desen liber” invocă exact regula canonică care acum cere verificare după teritoriu și utilizare **inclusiv în interiorul BD**. Autorul a aliniat hash-ul, dar a păstrat o derogare semantică nevalabilă. Un executant poate omite controlul cerut pentru interior. Nu emit o concluzie despre legea italiană; defectul este contradicția dintre două norme ale pachetului. | Înlocuiește permisiunea generală cu verificarea teritoriului/utilizării, inclusiv interiorul; păstrează sarcinile H1 pentru utilizările cerute. Relecturează RS27 împotriva textului canonic și adaugă un caz negativ care respinge „interior = liber”. |
| **S-K03** | **Major** | Organizarea `:972`, GT; `:1569`, varianta B; §9.4, Ep. 5 | GT cere „povestirile lor **publicate**”. Varianta B include Ep. 1–5 și fixează GT la **18.02.2027**, dar deznodământul povestirii Ep. 5 se publică **19.02.2027**, odată cu BD. Protecția surprizei interzice devansarea lui. Condiția declarată nu poate fi îndeplinită în ziua porții. Este un defect actual al planului G0, nu cererea de a produce volumul acum. | Fie mută GT și operațiunile dependente după publicarea cerută, fie aprobă explicit o condiție bazată pe versiuni corectate/aprobate, cu publicare comercială protejată. Păstrează regula anti-dezvăluire. Criteriu: fiecare precondiție GT să fie realizabilă cel târziu la GT; recalculează tiparul/livrarea dacă se mută poarta. |
| **S-K04** | **Minor cumulat, −0,10** | Jurnal `:65,69,78`; organizarea `:1682`, RS33; anexa S `:3,203,212,218`, față de `:313` | Inventarul datat 12:16:20 spune canon „v4.0… neschimbat”, organizare v4.2, deși pachetul și antetele sunt v4.2/v4.3. RS33 descrie lipsa ieșirii reviziei și așteaptă v4.1; anexa spune sincronizare încă de făcut, dar la 313 consemnează predarea integrată. Rândul livrabilului curent S:212 trimite la hash-ul planului R2; S:218 atribuie V1–V51 scriptului R2. Acestea sunt rubrici curente, nu istoricele delimitate S:9 sau S:364. Hash-urile actuale corecte fac incidentul recuperabil, fără a pretinde coruperea arhivei. | Actualizează numai rubricile curente, cu versiunea/amprenta reală și trimiterea la Execuția R3; marchează explicit ca observație istorică orice stare veche păstrată. Test: toate rubricile curente de inventar/predare trebuie să indice aceeași versiune și același hash. Nu modifica istoricul protejat. |
| **S-K05** | **Minor, −0,05** | Organizarea `:491`, D2 K2; `00_STUDIO/02_BRIEFURI/D2_brief.md`, secțiunea KPI, K2; canon §12 ingredientul 2 și glosarul „splash” | KPI admite **2–9 panouri pe o pagină**, fără excepție, însă pagina 4 obligatorie este splash, adică un singur panou. Textul identic în brief propagă aceeași inconsecvență. Intenția este recuperabilă din canon, dar verificarea literală respinge pagina obligatorie. | Precizează excepția paginii 4/splash și eventualele alte excepții admise; păstrează media pe episod. Verifică un scenariu cu pagina 4 de un panou: acceptat; o pagină obișnuită în afara limitelor fără justificare: respinsă. Sincronizează fișa și brief-ul. |

**Calculul notei:** criticul impune plafon **8,50**; cele două majore confirmă că sunt necesare corecturi de fond ale regulilor/dependențelor, fără dublă scădere aritmetică pentru plafoane. Minore distincte: 0,10 + 0,05. **8,50 − 0,15 = 8,35, FAIL.**

Nu penalizez studioul a doua oară pentru caracterele corupte din canon: autorul studio le declară și nu avea mandat să modifice canonul înghețat. Neconcordanțele S-K01/S-K02 sunt propriile reguli curente ale organizării.

## 5. Puncte forte și termene verificate

- Briefurile actuale sunt sincronizate efectiv cu fișele, nu numai declarativ.
- AP-16 descrie corect anexa de stare; AP-17/AP-18 dau executanți controalelor intermediare, iar decizia 15 este aplicată în MS K4.
- H5 include G4 și GS înaintea PASS; pre-producția cromatică are revalidări declarate după scenarii.
- D1/D2/proza disting ingredientele obligatorii de structură și formă. Țintele H3 sunt explicite, provizorii și recalibrabile.
- În datele calendarului A am renumărat **20 episoade, 74 tranșe pentru Ep. 2–20, 55 înaintea BD-ului propriu, 14 înaintea BD-ului precedent + 1 în aceeași zi = 15 protejate suplimentar**. Ultima dată declarată este 18.11.2027. Aceste numere concordă cu F2 și regulile publicării.
- Nu am certificat din această renumărare toate sărbătorile, toate duratele de lucru sau scenariile alternative. Contradicția GT este demonstrabilă doar din datele și condițiile pachetului.

## 6. Integritatea arhivei, verificată independent

Toate locațiile din acest tabel sunt relative la ROOT/00_STUDIO/audit.

| Inventar verificat | Rezultat propriu |
|---|---|
| `G0-STUDIO-v4/CODEX_R3_verificari/manifest_predare.json` | 28/28 amprente conforme cu documentele înghețate din pachet |
| `G0-STUDIO-v4/CODEX_R3_baseline_20260924/manifest.json` | 54/54 fișiere conforme |
| `G0-STUDIO-v4/R1_versiune_inainte_de_revizie/SHA256SUMS.txt` | 27/27 conforme |
| `G0-STUDIO-v4/R2_versiune_inainte_de_revizie/SHA256SUMS.txt` | 28/28 conforme |
| `G0-STUDIO-v4/R3_versiune_inainte_de_revizie/SHA256SUMS.txt` | 28/28 conforme |
| `G0-CANON-v4/REV_IZOLAT_20260924/MANIFEST.json` | 34/34 conforme |
| `G0-CANON-v4/REV_IZOLAT_20260924/archives_avant.csv` | 24/24 fișiere la amprentele de bază |
| `G0-CANON-v4/R0_versiune_initiala/SHA256SUMS.txt` | 7/7 conforme |
| Procedura v4 | SHA256 `2c13db6a6d9a8817e70538fa8df4ff7c7ba6378140c0102590db53e3ad403ead` |

Nu am certificat exhaustiv cele 529 fișiere ale inventarului arhivei ori proveniența criptografică a manifestelor. Nu am folosit timpii directoarelor copiate pentru a reconstitui momente originale. Fișierele suplimentare ulterioare unei măsurători datate nu constituie prin ele însele defecte.

## 7. Închiderea măsurilor anterioare relevante

### Defectele AU-K R3

| Defect anterior | Măsuri | Verdict independent și dovadă |
|---|---|---|
| R3K-1: randarea site-ului | M3.16 | **Închis la nivelul mandatului G0**: F1, K2/K10/K14 și §8.3 cer mascarea și site intern permanent; textul există identic în brief. Generatorul viitor nu a fost testat și nu este cerut acum. |
| R3K-2: perimetrul S | M3.12/M3.4 | **Închis ca regulă**: AP-16, §6.2(b), anexa de stare și arhivarea separată; evenimente consemnate în jurnal §6. Nu schimb perimetrul istoric. |
| R3K-3: grefieri/registru | M3.17 | **Regulă închisă; execuție integrală necertificată**: AP-17/AP-18 explicite. Nu am refăcut diff-ul integral al registrului central și nu revendic validarea GR-S. |
| R3K-4: convențiile calendarului | M3.19 | **Închis textual**: fereastra specială Ep. 1 și stocul strict sunt declarate; recalcularea tuturor zilelor lucrătoare neexecutată. |
| R3K-5: termene GS | M3.20 | **Închis structural**: coloana GS și trimiterile D2/H5 sunt prezente pe calendarul de 20 episoade. |
| R3K-6: proprietarul dosarului | M3.17 | **Închis**: S K6 și GR K5, GR verifică/GR-S validează. |
| R3K-7: alinierea G0 | M3.15 | **Parțial**: hash-ul corect și AP-19 există; alinierea semantică rămâne incompletă prin S-K01/S-K02, iar RS33 prin S-K04. |
| R3K-8: ținte H3 | M3.26 | **Închis**: newsletter ≥10%, retenție 50/40/35/30%, termen de recalibrare. |
| R3K-9: E-PREPROD | M3.23 | **Închis pentru dependența nominalizată**: revalidare după G4/GS înaintea culorii. Nu certific întreg graful; GT are defectul nou S-K03. |
| R3K-10: rigiditatea structurii | M3.7 | **Închis pentru K6**: abateri motivate, D1 K17. K2 are separat S-K05. |
| R3K-11: termen AU/MS | M3.22 | **Închis**: 19.10.2027 și regula prelungirii până la închiderea rundei. |
| R3K-12: cosmetice/stări | M3.28/M3.13 | **Corecturile nominalizate prezente, stare generală parțială**: separator, căi viitoare, titlu R2 corectate; S-K04 împiedică afirmația „o singură stare curentă”. |

### Alte măsuri R3 relevante lentilei

| Măsuri | Starea controlului meu |
|---|---|
| M3.1 și M3.31 | Integritatea bazei/predării confirmată prin manifestele de mai sus; nu atribui autorului izolat editările preexistente. |
| M3.2–M3.3 | Rândurile deciziilor și contrasemnărilor sunt prezente. Nu am reexecutat expansiunea 34×22 și comparația integrală a celor 15 tabele V45; nu declar echivalență independentă a tuturor celulelor. |
| M3.5–M3.6 | Reguli și excepția traducerii Ep. 1 explicite; numărătorile 15/55 refăcute. Toate duratele de traducere în zile lucrătoare nu au fost recalculate. |
| M3.8–M3.11 | Cerințe actuale prezente și sincronizate: proza după formă, prețul episodului, K12/K13, surse vestimentare; performanța creativă viitoare nu este certificată. |
| M3.13–M3.14 | **Parțiale**, S-K04; istoricele explicit delimitate nu se redeschid. |
| M3.18 | Închis: MS K4 și brief respectă aprobarea generală, fără reconfirmare cerută artificial. |
| M3.21 | Închis ca mandat: H5 înaintea G4/GS, nu numai 19 scenarii. |
| M3.24–M3.25 | Decizia ediției fizice este condițională; testul separă comparația textuală de cea vizuală. Nu verific aici calendarul real al târgului sau rezultate inexistente. |
| M3.27 | Surplusul de volum este justificat în E.8, opțiune permisă de plan; nu îl calific drept încălcare automată. |
| M3.29–M3.30 | Dovezi și autorevizuire există; afirmația generală de conformitate semantică nu este acceptată: S-K01–S-K05 sunt contraexemple reale. Scripturile și martorii autorului nu au fost rerulați de mine. |
| M2.8, M2.30, M2.31, M2.32 redeschise | Istoricul/perimetrul sunt corect delimitate; exactitatea stărilor rămâne parțială, iar echivalența exhaustivă și toate testele nu sunt certificate independent. |

Execuția R3 enumeră 31/31 sarcini și 31 rânduri de defecte R3. Acoperirea documentară nu este echivalentă cu 31/31 închideri independente.

## 8. Limite și verdict de utilizare

Evaluarea este strict G0/KPI. Nu am făcut audit juridic extern, cercetare istorică exhaustivă, verificarea fiecărui URL, recalcularea completă A/B1/B2, testarea site-ului, testarea producției BD, controlul integral al registrului sau al tuturor arhivelor. Constatările juridice aparente S-K01/S-K02 sunt **comparații interne cu deciziile și canonul aprobat**, nu afirmații despre aplicarea unei legi externe; nu necesită presupuneri juridice nesusținute și nu au fost extinse prin cercetări opționale.

Lipsa implementărilor viitoare, a avizelor H1, a rezultatelor de piață și a site-ului final nu este defect G0. Referința confidențială a fost citită pentru compatibilitate fără divulgarea soluțiilor sale.

Acest raport este **o evaluare independentă AU-K**, nu trei evaluări simulate. Nici nota veche, nici testele autorilor, nici așteptarea coordonatorului nu substituie nota de aici. G0 nu este aviz juridic ori certificare comercială externă. **FAIL: 8,35.** Pentru remediere sunt necesare o nouă revizie și un nou pachet comun, păstrând intacte fișierele acestei runde.
