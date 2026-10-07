# R2 — Audit independent KPI & Completitudine — G0-CANON-v4

**Data:** 24.09.2026. **Auditor:** AU-K, această sesiune; fără contribuții la revizii și fără agenți suplimentari.  
**NOTĂ: 8,50 / 10. Verdict: FAIL.** Pragul este 9,50 pentru fiecare auditor separat.

## 1. Perimetru și integritate

ROOT: `D:\00. Downloads\Dracula Book\DRACULA-COMICS-CODEX-G0-20260924`.  
Pachetul fix: `00_STUDIO/audit/RELUARE_CODEX_20260924_120350/PACHET_AUDIT_01`, relativ la ROOT. Toate locațiile curente de mai jos se referă la acest pachet, dacă nu se precizează ROOT. Numerele de linie sunt unu-based, pe textul UTF-8, inclusiv liniile goale.

Livrabil evaluat: `01_CANON/00_CANON_NUCLEU.md`, v4.2, **168.639 octeți, 873 linii, 24.971 cuvinte separate prin spațiu alb**. SHA256:
`243630e9071df7c7ee15cbf9f079fdac69f1d292950daab42cf927f36aa9ab26`.

Referințe comune:
| Fișier | SHA256 |
|---|---|
| Organizarea v4.3 | `d934ae4f3880962f1cc72ae8ee56dc213e40436a6ee43399dd274be344a853ac` |
| Jurnalul | `4285ae42e7c63dc34bef438b12eda0c9b5e5fc1ed0bc39f473a3a363a890016c` |
| S_showrunner, anexă de stare | `3b32d634dcea786b7f907eb2c122e5ed6b43403e4cc193920179c375b2f616a0` |
| Cele 15 decizii | `dd0128b800270b219435b0b841f39232146fb96f88da94047e356817b8e44bdf` |
| Contrasemnările | `f5acdb54d286419b7cff509bf4183c2ec7471e57de0d21dacf34691978318588` |
| manifest.json al pachetului | `ca227d6345d935317ffb4780b6cd8286a874fdb165f4eda3c18ba907536847ac` |

**Recalculare proprie:** 32/32 fișiere din manifestul pachetului au SHA256 și dimensiuni conforme; cele trei fișiere principale au fost reverificate înaintea redactării. Manifestul nu este o semnătură digitală: verificarea demonstrează concordanța cu instantaneul declarat.

În ROOT, recalculare proprie suplimentară, fără executarea verificatoarelor autorilor:
- `G0-CANON-v4/REV_IZOLAT_20260924/MANIFEST.json`: 34/34 fișiere conforme.
- `archives_avant.csv` din aceeași revizie: 24/24 fișiere arhivate păstrate la amprentele înregistrate.
- `G0-CANON-v4/R0_versiune_initiala/SHA256SUMS.txt`: 7/7 conforme.
- Procedura v4: SHA256 `2c13db6a6d9a8817e70538fa8df4ff7c7ba6378140c0102590db53e3ad403ead`, identic cu referința documentelor.

Căile vechi citate în istoric nu au fost accesate. Nu s-au modificat fișierele înghețate, producția, scripturile sau rapoartele altora.

## 2. Metoda reală și numărătorile

Am citit integral cele trei fișiere principale obligatorii: canonul (873 linii), organizarea (1.888), jurnalul (470), în tranșe; pasajele trunchiate au fost reluate. Am citit integral deciziile, contrasemnările, brief-ul S, RAPORT_REVIZIE, MASURI_39 și DEFECTE_64. Am confruntat sarcinile relevante din planul R1 și tabelul defectelor AU-K anterior cu textul nou. Anexa S a fost verificată pe stările curente și delimitările istorice; nu revendic o recitire integrală a tuturor anexelor sale istorice.

Am citit integral referința confidențială din ROOT, SHA256 `483961ee2ec2ac98dffa4447e808dd18a1efaf07454014f267d126852df0d6ca`. Ea se declară aliniată la v3.0; compatibilitatea integrală cu v4.2 **nu** este certificată. Canonul §10, linia 376, declară explicit alinierea la G1. Diferențele de pivoturi, reguli și cronologie ale propunerilor nu devin automat defecte G0. Identitățile și soluțiile confidențiale nu sunt reproduse aici.

Numărătoare proprie pe documentele actuale:
- **25 fișe, 131 puncte de sarcină, 228 KPI**; blocurile celor 131 de sarcini și textele celor 228 KPI sunt identice cu secțiunile actuale ale celor 25 brief-uri.
- Anexa A: **40 egale + 52 precizări + 26 mai stricte + 110 noi = 228**. Am recalculat etichetele și intervalele K; aceasta confirmă acoperirea structurală, nu corectitudinea fiecărei reguli.
- Pentru S: **11 puncte de sarcină și 13 KPI**, nu vechile 8/10/11 KPI din istorice.
- Canon: **24 + 24 + 24 rânduri** în §5, §5.1, §5.2; **24/24 celule de modă cu exact trei segmente**; **87 ID-uri V4 distincte, continue V4-01–V4-87**.
- Cele 39 măsuri și 64 rânduri de trasabilitate ale autorului reprezintă inventarul **39 măsuri / 57 defecte + 7 observații**, nu 64 defecte noi și nici 39 închideri independente.

Unitatea de numărare a unei sarcini este punctul de listă imediat sub rubrica „Sarcini”; KPI compuși se numără o singură dată după identificator. Nu prezint 228 ca număr al tuturor obligațiilor atomice din toate propozițiile.

### Acoperirea brief-ului S pentru canon

Descompunerea de mai jos are **39 cerințe distincte**, separate după obiectul verificat; este o matrice proprie de acoperire, nu o însumare a aparițiilor aceluiași cuvânt. Textul istoric al procedurii se interpretează cu decizia 15 și abaterile aprobate. „Prezent” nu înseamnă validare istorică/juridică exhaustivă.

| Nr. | Cerință | Dovadă / rezultat actual |
|---|---|---|
| 1 | Autoritate canonică și decizii blocate | antet; 15 decizii, inclusiv 15 |
| 2 | Completitudine a nucleului | §1–§20 prezente |
| 3 | Istorie umană 1431–1476, cu surse | §3 și §18; existență verificată, exactitatea exhaustivă rezervată AU-C |
| 4 | Încadrarea obiectivelor în anii scenei | §5, regula explicită; controlul fiecărui fapt extern neexecutat |
| 5 | Lipsa contradicțiilor interne | lectură integrală; fără certificare K1 global = 0 |
| 6 | Utilizare de personaje/lume/plot/artă/proză | ghidul de lectură, §5.2, §12, avizul separat |
| 7 | Prezentare aspirațională | §1 |
| 8 | Mustață în flashback-urile vieții umane | §2 și §13 |
| 9 | Modă pe fiecare epocă | §5.2, 24/24 scheme complete |
| 10 | Protecția ochilor ziua | §2, §5.2, §6; ficțiunea tehnică delimitată |
| 11 | Viața de om | §3 |
| 12 | Noaptea transformării | §3.1, 26/27.12.1476 |
| 13 | Identități și regula schimbării | §4 și §5.1; nu pretind recalcularea independentă a tuturor celor 32 de identități |
| 14 | 24 popasuri | 24/24 în trei tabele |
| 15 | Obiectiv celebru pe popas | coloana dedicată din §5 |
| 16 | Clișeu cinematografic pe popas | §5; clasificarea tuturor operelor nu a fost reverificată extern |
| 17 | Moda pe popas | §5.2 |
| 18 | Vehiculul-semnătură | §5.2 |
| 19 | Luxul | §5.2, inclusiv absențele motivate |
| 20 | Iubirile după 1794 | §5.2; despărțirea rămâne blocată |
| 21 | Succesul familiei | §5.2; donația și portofoliile externe clarificate |
| 22 | Puteri, limite și ziua | §6, R1–R10 |
| 23 | Codul | §7, opt articole |
| 24 | Sânziana înstrăinată, fără soție în prezent | §8; lista întâlnirilor închisă |
| 25 | Familia și rolurile ei | §8; echivalențe interne în §20.1 |
| 26 | Ioana fără romantism în S1 | §9 și §20.5 |
| 27 | Radu și separarea istorie/ficțiune | §3 și §10 |
| 28 | Armistițiul la 50 ani din 1526 | §10; regula și calendarul prezente |
| 29 | Antagonist: numai profil public | §10; referința confidențială consultată separat |
| 30 | Locurile | §11 |
| 31 | Sezon, format, ingrediente, proză separată | §12; 24 + 4/8 = 28/32; defectul C-K01 în completarea OBS-10 |
| 32 | Identitatea vizuală DRACULA | §13 |
| 33 | Drepturi și originalitate | §14; reguli și responsabil H1, fără aviz juridic simulat |
| 34 | Registrul deciziilor | §16; 87 ID-uri V4; propunerile amânate au rânduri |
| 35 | Istoricul versiunilor | §17 |
| 36 | Numerotarea §1–§13 păstrată | verificată în text |
| 37 | Numărătoare și dovezi automate | 24.971 cuvinte, probe arhivate; scripturile autorilor nu au fost rulate aici |
| 38 | Tratarea defectelor anterioare relevante | matricea de închidere de mai jos; fără preluarea notei R1 |
| 39 | Raportarea Showrunnerului | raport separat E.1–E.9, cu 15 decizii și K1–K13; anexa veche nu certifică versiunea nouă |

Româna cu diacritice este suplimentar o condiție transversală explicită a deciziei 6, verificată asupra textului predat.

## 3. Defecte confirmate și nota

Grila impusă rămâne: 9,50–10 excepțional; major plafon 9,20; critic plafon 8,50; neconcordanță cu decizie aprobată = critic. Nu transfer nota veche.

| ID | Gravitate | Locație exactă | Probă și impact | Remediu verificabil |
|---|---|---|---|---|
| C-K01 | **Critic, prin condiția explicită a deciziei 6** | `01_CANON/00_CANON_NUCLEU.md:408`, completarea OBS-10, și `:596`, V4-87 | Textul UTF-8 conține efectiv 13 semne ASCII „?” în completarea de la 408 și 7 la 596: „Proza ?i traducerile”, „h?r?ii”, „jurnal ?5.6”, „?12”, „D3?D6”. Nu este o eroare de afișare. Decizia 6 cere română cu diacritice. Sunt deteriorate inclusiv referința de secțiune și identificatorul echipei. Defectul este recunoscut și în jurnal:399, dar nu remediat în copia înghețată. | Într-o **nouă revizie**, restaurează cele 20 de caractere din pasajele respective prin comparație cu OBS-10 din jurnal și fișele D1/D3–D6; recitește semantic; confirmă grafiile „și”, „hărții”, „§5.6”, „§12”, „D3–D6”. Recalculează SHA256, manifestul și referința AP-19; distribuie noul pachet comun celor trei auditori. Nu corecta această copie în timpul rundei. |

Defectul este local, reparabil fără rescriere conceptuală; nu îl prezint ca eșec narativ ori istoric. Încadrarea critică rezultă din regula expresă a mandatului privind o decizie aprobată, aplicată deciziei 6. **Plafon 8,50; fără alte penalizări speculative: nota 8,50, FAIL.**

## 4. Puncte forte

Schema modei este acum completă 24/24, iar excepțiile au text utilizabil. Aritmetica broșurii este închisă. Propunerile amânate au identificatori și proprietari. V4-83/V4-87 consemnează adaptarea prozei și protejarea surprizei. Autorul nu mai certifică nejustificat compatibilitatea integrală a documentului C și nu pretinde PASS independent. Predarea este reproductibil identificabilă prin amprentă, iar probele de integritate verificate concordă.

## 5. Închiderea măsurilor anterioare relevante AU-K

„Închis” mai jos privește constatarea exactă, în perimetrul G0; nu certifică toate verificările auxiliare ale autorului.

| Defect anterior / măsură R1 | Starea independentă | Dovadă actuală și limită |
|---|---|---|
| AK-1 / M1.3 | Închis structural și operațional în G0 | §5.2, 24/24 rânduri cu trei segmente; protecția/absența motivată și accentele sunt explicite. Atestarea fiecărui accesoriu nu este certificată aici. |
| AK-2 / M1.32 | Închis pentru cele patru omisiuni nominalizate | §16.3: B-B6, B-B8, B-B11, C-P15 au rânduri și termene. Nu revendic o reconciliere automată exhaustivă a fiecărei propuneri din toate arhivele. |
| AK-3 / M1.34 | Închis prin raport separat autorizat | RAPORT_REVIZIE E.5–E.6: 15 decizii, K1–K13; anexa S:9 delimitează raportul canonic vechi. |
| AK-4 / M1.12 | Închis | §5/§5.1/§5.2: active japoneze donate, portofolii externe păstrate; revenirea fără bani nu mai presupune dispariția averii. |
| AK-5 / M1.10 | Închis | R8 și §2/§13: forma deplină și statura după transformare. |
| AK-6 / M1.2 | Închis în canon; aliniere C la G1 | §8: somn, locuri, treziri ordinare/extraordinare și preț; nu certific compatibilitatea integrală a referinței C. |
| AK-7 / M1.9 | Închis în canon | §5.1/§8 și R4: ramura vieneză, succesorii și excepția 1915–1916 declarate. |
| AK-8 / M1.30 | Închis pentru aritmetică | §12: 24 + 4/8, opționale 0/4. Noua problemă textuală OBS-10 rămâne C-K01. |
| AK-9 / M1.17 | Documentat, închidere externă neverificată | Sursele suplimentare și URL-ul înlocuit există în §18. Nu am rerulat cele 181 accesări; HTTP 503 declarat nu dovedește singur falsitatea unui fapt. |
| AK-10 / M1.18 | Închis pentru aliasul nominalizat | §5/§5.1: Virgilio Dal Drago. Nu atribui drept verificare proprie lista de 32 de identități a autorului. |
| AK-11 / M1.32 | Închis | §16: B-C3/B-C5/B-C1 și definițiile M/S/PR; ID-uri V4 unice și continue. |
| AK-12 / M1.11 | Închis | §8: statut 1456–1794, prezentarea publică și cele trei întâlniri; §5.1 #16/#17 nu adaugă întâlniri. |
| AK-13 / M1.31, M1.14, M1.36 | Corecturile vechi prezente; finisajul nou parțial | Antet/procedură actuală, jurământ, glosar; C-K01 împiedică închiderea finisajului întregii versiuni. |
| AK-O1 / M1.31 | Închis | Decizia 15 prezentă; contrasemnarea generală se aplică. |
| AK-O2 / M1.39 | Închis în mandatul izolat | Copie predată/manifest, 34/34 amprente; arhiva R0 nu a fost rescrisă pentru a ascunde cronologia. |
| AK-O3 / M1.35 | Închis pentru bugetul total | 24.971 ≤ 25.000; fișă rapidă și ghid de lectură prezente. |
| AK-O4 / M1.34 | Închis cu limita declarată | Raport separat cu date actuale; K1 global nu este inventat. |
| M1.1, M1.38–M1.39 | Integritate verificată; testele autorului rămân probe | 24/24 fișiere ale bazei arhivate și 34/34 manifest; niciun PASS semantic dedus automat. |
| M1.24 și M1.37 | Parțial/delegat explicit | Compatibilitatea integrală C și auditul istoric/semantic exhaustiv nu sunt declarate închise; alinierea documentelor G1 nu este cerută anticipat în G0. |

## 6. Limite și aplicabilitate

Aceasta este **o singură evaluare independentă AU-K**, nu cele trei lentile cerute pentru promovarea porții. Raportul studio aferent nu reprezintă un al doilea auditor al canonului.

Nu am rerulat verificatoarele autorilor, nu am testat implementările G1/G5, nu am verificat toate cele 181 URL-uri și toate faptele istorice/juridice; nu am recalculat toate identitățile sau fiecare absolut semantic. Nu afirm integritatea fiecărui fișier din întreaga arhivă: numerele de mai sus delimitează exact verificarea. Constatarea C-K01 este internă și direct verificabilă, fără o ipoteză istorică sau juridică incertă; nu am făcut cercetare web suplimentară.

G0 nu este aviz juridic sau certificare comercială externă. Site-ul final, paginile BD, rezultatele de piață, numirile și avizele programate nu sunt declarate lipsuri G0. K7 al S (3,5 observat, țintă ≤3 la G5/final) nu produce o penalizare anticipată. Istoricul explicit etichetat nu a fost evaluat ca stare curentă.
