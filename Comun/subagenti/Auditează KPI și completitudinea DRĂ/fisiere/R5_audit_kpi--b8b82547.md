# G0-STUDIO-v4 · R5 · Audit independent KPI & Completitudine

**NOTĂ: 9,65 / 10 — PASS AU-K. Blocanți confirmați: 0. Defecte critice: 0; majore: 0; minore: 4.**

Data: 24.09.2026. Auditor independent, fără contribuție la documentele auditate și fără agenți lansați. Raportul este o singură lentilă; nu acordă singur PASS întregii porți. Pragul rămâne minimum 9,50 pentru fiecare dintre cei trei auditori; majorul plafonează la 9,20, criticul la 8,50, iar contradicția unei decizii aprobate este critică. Nu am transferat notele R4 și nu am schimbat grila.

ROOT = `D:/00. Downloads/Dracula Book/DRACULA-COMICS-CODEX-G0-20260924`.
P2 = `ROOT/00_STUDIO/audit/RELUARE_CODEX_20260924_120350/PACHET_AUDIT_02`.
Toate locațiile de conținut de mai jos sunt în P2. Referințele de arhivă sunt în ROOT. Originalul celeilalte sesiuni nu a fost accesat.

## Fișiere și amprente

Am recalculat SHA-256 și mărimile celor **32/32 fișiere** declarate în manifest, inclusiv înaintea scrierii raportului: zero diferențe. Tabelul de la sfârșit fixează individual toate amprentele.

- Organizare v4.4: `2f232e2596c99c54238b1a831db2453e2ad23c9c4181bc4bff1b9ad3fd0f1203`.
- Jurnal v4.4: `9f69d8a6354d4704867e4cd7b51c143a2c800dd011aa66200c59e43f8081f380`.
- Anexa S: `6ade4a2018a8a4c0416707e0b3d88c674abbee33614d6d7e0e6ffa985a8a8737`.
- Canonul de referință v4.3: `b51981121c39953258b32989d85a4239120f85aa8746229736ca605c25f57357`.
- Manifest P2: `4ed6aa7d04e4b652944845eb2e8ea4324d3459c1252f7b351ab32e53f16a9d6f`.
- Procedura v4, referință citită fără execuție: `2c13db6a6d9a8817e70538fa8df4ff7c7ba6378140c0102590db53e3ad403ead`.

Raportul meu Canon R3 rămâne nemodificat: `ROOT/00_STUDIO/audit/G0-CANON-v4/R3_audit_kpi.md`, SHA-256 `91d502c52e1881ba5f9c3448a9203814b408f08793fc1ea664374f1772994db8`. Mesajul ulterior al Producătorului anunță arhivarea celor trei avize Canon R3, 9,80/9,70/9,90. Nu penalizez pachetul fix, anterior acelui mesaj, pentru faptul că anunță încă auditul canonului în curs; nu modific pachetul și nu transfer acele note Studioului.

## Metoda executată

Lectură integrală a organizării, **1.892 rânduri / 42.270 cuvinte**, și jurnalului, **474 rânduri / 12.106 cuvinte**. Lectură integrală a secțiunii curente S, rândurile 1–38; întregul fișier S are 566 rânduri / 13.565 cuvinte, incluzând istoria. Numărătoarea folosește `splitlines()` și `split()`; nu reprezintă paginare tipografică. Canonul identic a fost citit integral la auditul meu R3; aici i-am verificat din nou amprenta și pasajele de aplicabilitate relevante, fără reauditarea sau renotarea lui.

Am citit registrul celor 15 decizii, contrasemnările, briefurile S și AU-K și pasajele relevante ale briefurilor de producție. Toate cele 25 de briefuri au fost procesate integral pentru amprentă, numărători, comparația secțiunilor normative și căutarea urmelor. Nu pretind o nouă lectură literară, rând cu rând, a fiecărui extras istoric din fiecare brief.

Am parcurs cele trei rapoarte R4, planul cu exact șapte măsuri, EXECUTIE.md și rezultat.json; am verificat manifestul și am regenerat independent diferențele. Planurile anterioare Canon R1 și Studio R3 sunt referințe de trasabilitate consultate pe măsurile/arbitrajele relevante, nu un nou certificat exhaustiv al tuturor execuțiilor lor. Registrul central din P2 a fost consultat pentru grilă, proveniență, izolarea și predarea rundelor.

Instrument: Python 3.12, executabilul indicat de utilizator, cod propriu în memorie, fără scrierea de scripturi auxiliare. Nu am executat procedura de producție sau verificatoarele autorilor. Prima încercare a comparației s-a oprit la decodarea implicită Windows; am reluat explicit UTF-8, iar rezultatele raportate sunt ale rulării încheiate. Declarațiile autorului „12 conforme” și vechile V1–V51 nu au fost folosite ca substitut pentru verificare.

## Numărători și consistență

Unitatea numărată este cerința numerotată K din fișă, respectiv fiecare punct de sarcină, nu fiecare subcondiție dintr-un KPI compus. Comparația urmărește secțiunile „Sarcini” și „KPI”, fără adnotările comparative din finalul briefurilor.

| Rol | Sarcini | KPI | Concordanță fișă–brief |
|---|---:|---:|---|
| S | 11 | 13 | identice |
| MS | 6 | 6 | identice |
| A | 8 | 11 | identice |
| A1–A6 | 4 | 6 | identice |
| B | 7 | 11 | identice |
| C | 8 | 12 | identice |
| D1 | 4 | 17 | identice |
| D2 | 4 | 10 | identice |
| D3–D6 | 5 | 12 | identice |
| E | 7 | 12 | identice |
| E2 | 3 | 8 | identice |
| E3 | 2 | 7 | identice |
| E4 | 3 | 7 | identice |
| F1 | 8 | 14 | identice |
| F2 | 7 | 11 | identice |
| H1 | 7 | 8 | identice |
| H2 | 3 | 5 | identice |
| H3 | 5 | 10 | identice |
| H4 | 4 | 5 | identice |
| AU-C | 5 | 8 | identice |
| AU-M | 5 | 9 | identice |
| AU-K | 3 | 8 | identice |
| GR | 3 | 5 | identice |
| GR-S | 7 | 8 | identice |
| H5 | 2 | 5 | identice |
| **Total** | **131** | **228** | **25/25 briefuri** |

25 fișe pentru 25 posturi; 37 titulari prin 22×1 + 6 + 4 + 5. Organizarea are 12 secțiuni principale numerotate, 33 riscuri RS și 19 abateri AP. Anexa A are 228 identificatori după expandarea intervalelor: 40 „=”, 52 „precizează”, 26 „mai strictă”, 110 „nou”. Identitatea textelor curente nu dovedește singură echivalența semantică a tuturor clasificărilor față de vechea procedură; am verificat separat cazurile R4.

Roadmapul are 70 rânduri, cu rolurile grupate explicit și etapele inactive motivate; cele 25 posturi sunt reprezentate. Tabelul deciziilor așteptate are 19 rânduri. Calendarul are 20 episoade, iar cele trei coloane lunare de capacitate însumează fiecare 480 pagini. Acestea sunt ținte planificate, nu pagini deja realizate.

### Cerințele brief-ului Studio: matricea de acoperire

Am separat textul compus al brief-ului S:33 în 14 obiecte verificabile, fără a inventa 14 KPI noi.

| Cerință | Dovadă și rezultat G0 |
|---|---|
| Echipa și modul de gândire | §3–§4, 25 posturi/25 rubrici de gândire |
| Sarcini pe post | 131 puncte, sincronizate cu briefurile |
| Raportarea progresului | §5, jurnal, anexă S; minorul F2 de mai jos |
| Roadmap pentru fiecare membru | §9.3, 70 rânduri, activități/obiective/rezultate/termene |
| KPI numerici și căi de livrabile | §4, 228 K; căile viitoare sunt declarate ca atare |
| Etape și jaloane datate | §9.1–§9.7; 30.11, 01.12, 31.03 păstrate |
| Fiecare agent are verificator | §6.7, inclusiv MS, AU, GR și GR-S |
| Prag și circuit sub prag | §6.3: minimum 9,50, plan, revizie, auditori noi |
| Arhivarea procesului | §7 și verificările de integritate de mai jos |
| Independența și contrasemnarea | §3.2/§6.3; aprobarea generală este recunoscută |
| Alinierea la deciziile/canonul curent | 15 decizii, hash v4.3, cazurile M4.2–M4.6 |
| Jurnalul reflectă starea reală | antet, faza 0, inventar corectat, nota R4 finală; istoricul datat separat |
| Raportul S după șablon | 13 K prezente, livrabile/riscuri/pași/istoric; completitudine formală parțială, F1/F2 |
| Română, diacritice, urme vechi | scanare proprie a celor 29 documente G0 și lectură contextuală |

### Aplicabilitatea celor 13 KPI ai Showrunnerului

| KPI | Valoarea/controlul propriu și limita |
|---|---|
| K1 | 0 contradicții blocante confirmate în cazurile actuale; 15/15 decizii au mecanism de aplicare în §2. Nu substitui verdictul AU-C. |
| K2 | 25/25 briefuri; 228/228 K și 131/131 sarcini identice. Extrasele vechi sunt marcate istorice și subordonate fișei actuale. |
| K3 | Predarea R4 și jurnalul sunt datate 24.09.2026, în aceeași zi; nu reconstitui orele originale din timpii copiilor și nu certific toate evenimentele externe. |
| K4 | Planul R4 și cele trei rapoarte R4 sunt din aceeași zi; afirmația globală pentru toate planurile istorice nu este recertificată aici. |
| K5 | OBS-8 și OBS-10 au rezultat consemnat în jurnal:397/224 și canon V4-83/V4-87; nu tratez vechea stare „transmis” ca pendință nouă. |
| K6 | P2 32/32; R4 înainte/după 28/28; verificări istorice delimitate mai jos. Validarea GR-S și închiderea întregii porți nu sunt simulate. |
| K7 | Țintă normativă ≤3, evaluabilă la G5/final S1; anexa curentă citează eronat 2 (F1). Nu penalizez rezultatul viitor al mediei. |
| K8 | Aprobarea generală are sursă explicită și include rundele următoare; nu am găsit o derogare nominală inventată pentru tren. |
| K9 | 0 urme ale numelui/titlului anulat în 29 documente G0, inclusiv numele căilor relative; 0 caractere românești cu sedilă. |
| K10 | B0 există și nu înlocuiește B1; B1–B6 sunt viitoare. Nu cer 7 buletine produse la 24.09. |
| K11 | Procedura v5 are termen 09.10 și nu e pretinsă executată; fără audit tehnic al unei implementări viitoare. |
| K12 | Mediana creativă G1–G4 este viitoare, explicit nemăsurată. |
| K13 | Testele/retenția sunt viitoare; H3 K7/K10 și S K13 atribuie măsurarea și răspunsul. |

Criteriile creative ale Producătorului rămân operaționale: toate cele șapte atribute ale eroului în B K6/E K2; 24 popasuri în B/C; acțiune de zi, modă, vehicule și femei cu agendă proprie în D1/D2/D3–D6; meritul și generozitatea, prețul victoriei și emoția în D1 K13/K16, AU-M K9; aspirația și dorința de a continua lectura în H3. Nu înlocuiesc acestea cu gusturi personale sau cu rezultate de piață inexistente.

## Verificarea independentă a celor șapte măsuri

| Măsură | Închidere | Probă proprie |
|---|---|---|
| M4.1 | **Închisă în perimetrul verificat** | 28 copii „inainte” identice cu P1 și hashurile before; arhivele R1–R3/baseline verificate separat. Nu pretind certificarea tuturor fișierelor istorice. |
| M4.2 | **Închisă** | RS28:1677 exclude explicit trenurile din excepția locurilor; canon:471 cere generic/fictiv ori derogare specifică după H1. Mențiunea unei opere în surse nu este vehicul autorizat. |
| M4.3 | **Închisă operativ** | RS19/27/28:1668/1676/1677; D3–D6 K5:519, E K4:550, H1:682 și briefurile. Opt categorii; hotelul descriptiv nu e marcă de obiect; interiorul monumentului nu e automat liber. Reziduul de index este F3, fără să anuleze regula explicită. |
| M4.4 | **Închisă** | Ep.5/deznodământ 19.02.2027 < GT 22.02 < tipar 23.02 < livrare 08.03. Date identice în GT:972, H4 K3:763, roadmap:1438, calendar:1569, H4_brief:34, jurnal:474 și S:31. |
| M4.5 | **Închisă pentru defectul R4** | RS33:1682, antetele, jurnal:69/78, S:1–38 indică aceeași predare v4.3 și v4.4. S istoric este sufix identic byte cu byte, 101.294 octeți; nu mai reprezintă starea curentă. F1/F2 sunt minore ale noului rezumat, distincte de vechea nesincronizare. |
| M4.6 | **Închisă** | D2 K2:491 = D2_brief:49. 23 pagini×5 panouri + splash p.4 =116/24=4,83; cu 21 pagini×5, splash p.4 și un splash dublu:107/24=4,46. Ambele respectă media și 24 pagini fizice. Pagina obișnuită de un panou, fără motivare, nu satisface regula; două pagini duble depășesc 0–1. |
| M4.7 | **Închisă ca propagare și predare** | 25 briefuri, 131 sarcini, 228 K; 28 diferențe regenerate identice cu patchurile, 9 documente schimbate; trei cazuri semantice și calendar verificate propriu. Nu există autor-PASS. Minorele reziduale sunt contabilizate separat. |

Cazurile semantice au fost judecate din regula actuală, nu din rezultatul scriptului: hotel real, numire descriptivă interioară → admis editorial; tren real, fără derogare → respins ca vehicul-semnătură; monument italian interior → evaluare H1 pe utilizare/teritoriu. Nu sunt concluzii despre legalitatea unei utilizări concrete.

Calendar: parsare proprie a tabelelor §9.4 confirmă 74 tranșe pentru Ep.2–20, din care 55 înaintea deznodământului și 19 deznodăminte la datele BD. 14 tranșe preced BD-ul episodului anterior și una coincide cu el: 15 cazuri cu protecția suplimentară; zero tranșe înaintea lansării. Cele nouă zile luni–vineri după tipar sunt 24–26 februarie, 1–5 și 8 martie; ziua predării nu este numărată. Aceasta este o durată de planificare după predare, nu nouă zile strict între cele două capete, nici dovadă de capacitate a tipografiei. Regula strictă a intervalelor de publicare rămâne explicită la:1457.

Dependențele nominale sunt păstrate: plot înaintea prozei; scenariul înaintea desenului; revalidarea culorii după scenariu; româna finală înaintea traducerii; niciun PASS G1 înaintea G0. Nu am recalculat integral toate intervalele lucrătoare, alternativele B1/B2 și graful complet de capacitate. Limita nu este transformată într-un defect.

## Defecte reziduale confirmate

| ID | Gravitate; scădere | Locație exactă | Criteriu, problemă și remediu |
|---|---|---|---|
| F1 | minor; −0,10 | `00_STUDIO/rapoarte/S_showrunner.md:19` | K7 curent spune „ținta medie de 2 runde”; fișa:302 și S_brief:117 cer ≤3. Corectarea cifrei și indicarea scadenței G5/final S1; nu cere atingerea anticipată a KPI. Fișa și brief-ul, care prevalează, sunt corecte. |
| F2 | minor; −0,10 | S:10–28, față de organizare:903–904/913 | Sunt 13 rânduri K, dar țintele nu sunt redate explicit pentru majoritatea, iar conformitatea celor 15 decizii este rezumată într-un paragraf, fără tabelul curent decizie–dovadă cerut de șablon. Tabelele istorice nu țin loc de verificare curentă. Adăugarea țintelor și a 15 trimiteri actuale este suficientă; datele de fond există în fișă și §2. Este o lipsă formală limitată a anexei, nu absența politicilor de producție. |
| F3 | minor; −0,10 cumulat | Organizare:1642, 1692, 1775; metadatele briefurilor, de ex. S_brief:6 | Trimiteri secundare rămase în urmă: §9.7 invocă declanșatorul RS33 la 25.09, deși RS33 actual urmărește 28.09 și schimbarea hashului; indexul temeiurilor restrânge descrierea RS27 la coperți/produse, deși regula include interiorul; coloana „versiunea curentă” și unele antete de brief indică v4.3. Actualizarea etichetelor și a trimiterii la monitorizarea RS33. Regula operativă și hashul sunt explicite; nu rezultă permisiune nouă, termen GT inversat ori decizie blocată contradisă. |
| F4 | minor cosmetic; −0,05 | `00_STUDIO/03_JURNAL_PROGRES.md:196–198` | Linia goală:196 rupe tabelul §5.3; cele două rânduri următoare devin paragraf cu bare. Confirmat prin randare în memorie cu Python-Markdown, extensia tables. Eliminarea separării sau repetarea antetului/separatorului restabilește tabelul; conținutul nu lipsește. Nu penalizez adevărul istoric al acestor rânduri. |

**Calcul transparent: 10,00 − 0,10 − 0,10 − 0,10 − 0,05 = 9,65.** Niciun plafon major/critic activ. Corecturile rămase sunt locale, fără rescriere de reguli, roluri, calendar sau obiective creative. Nu am aplicat scăderi pentru simpla existență a istoricului, a unor fișiere viitoare sau a unor limite declarate ale auditului.

## Integritatea și dovezile execuției

| Control executat | Rezultat |
|---|---|
| P2, hash și mărime | 32/32 conforme |
| R4 „inainte” față de P1 și manifest before | 28/28 identice |
| R4 „predat” față de P2 și manifest | 28/28 identice |
| Patchuri regenerate independent cu difflib, corpul diferențelor | 28/28 identice; 9 nevidate, 19 fără modificare |
| Istoricul S față de fișierul anterior | 101.294 octeți identici, sufix integral |
| R1_versiune_inainte_de_revizie/SHA256SUMS.txt | 27/27 conforme |
| R2_versiune_inainte_de_revizie/SHA256SUMS.txt | 28/28 conforme |
| R3_versiune_inainte_de_revizie/SHA256SUMS.txt | 28/28 conforme |
| CODEX_R3_baseline_20260924/manifest.json | 54/54 conforme |
| CODEX_R3_verificari/manifest_predare.json față de P1 | 28/28 conforme |

Cele nouă documente schimbate sunt organizarea, jurnalul, S și briefurile D2, D3–D6, E, H1, H3, H4. Niciun rol sau KPI nou adăugat. Verificarea amprentelor atestă concordanța cu bazele disponibile, nu autenticitatea externă a manifestelor sau absența oricărei scrieri în întreaga istorie.

Scanarea urmelor: 29 documente G0 din P2, excluzând cele trei referințe de registru/decizii/contrasemnări, după căile lor logice. Normalizare casefold/NFD, eliminarea semnelor diacritice combinante, echivalarea spațiilor/cratimelor/underscore; subșirurile RO/EN/DE și derivatele numelui vechi. Excepția nominală a plantei este păstrată. Martori proprii: cinci cazuri de eșec detectat, două cazuri legitime acceptate; 7/7 rezultate așteptate. Căutarea soției a fost interpretată contextual: negația „nu mai e soția” și trecutul explicit nu sunt contradicții curente. Nu am extins scanarea la producția G1 din afara pachetului.

## Surse, puncte forte și limite

Sursele decisive sunt primare pentru proiect: deciziile Producătorului, contrasemnările, canonul fix, fișele, briefurile și copiile înghețate. Raportul R4 a identificat teme, dar fiecare închidere de mai sus are control propriu. Pentru contextul sărbătorilor am consultat [Portalul Legislativ, Codul muncii, art.139](https://legislatie.just.ro/Public/DetaliiDocument/234702); pagina recuperată reprezintă o formă datată, insuficientă pentru certificarea tuturor sărbătorilor viitoare. Calculul local 24.02–08.03 este declarat luni–vineri. Nu prezint această consultare drept aviz juridic ori drept recalculare completă a calendarului național.

Puncte forte: distincția locuri/obiecte este aplicabilă și propagată; GT are acum dependența corectă; excepțiile de pagină nu mai interzic splash-ul canonic; cerințele sunt sincronizate exact; ipotezele de capacitate și alternativele rămân declarate; G1 și avizele externe nu sunt pretinse realizate; arhiva păstrează versiuni, inclusiv încercările nereușite ale autorului, iar raportul S separă explicit prezentul de istorie.

Nu certific toate cele 529 de fișiere ale inventarului istoric, fiecare legătură din registru, toate cele 51 verificări ale autorului, toate permisiunile istorice celulă cu celulă sau toate afirmațiile istorice/juridice. Nu am testat site-ul, producția artistică, măsurătorile de piață, sursele confidențiale din nou în această rundă sau fiecare URL extern. Nicio identitate confidențială nu este reprodusă. Evaluarea literară, istorică și de procese este editorială G0, nu certificat extern, aviz H1 ori autorizare de publicare comercială.

**Verdict AU-K: PASS, 9,65; fără blocanți.** Închiderile operative M4.1–M4.7 sunt confirmate în limitele declarate, cu cele patru minore de mai sus. Pachetul rămâne înghețat; nu am aplicat remedii în el.

## Inventarul SHA-256 verificat

| Fișier relativ la P2 | Octeți | SHA-256 |
|---|---:|---|
| `01_CANON/00_CANON_NUCLEU.md` | 168880 | `b51981121c39953258b32989d85a4239120f85aa8746229736ca605c25f57357` |
| `00_STUDIO/01_ECHIPA_SI_ROADMAP.md` | 286828 | `2f232e2596c99c54238b1a831db2453e2ad23c9c4181bc4bff1b9ad3fd0f1203` |
| `00_STUDIO/03_JURNAL_PROGRES.md` | 83590 | `9f69d8a6354d4704867e4cd7b51c143a2c800dd011aa66200c59e43f8081f380` |
| `00_STUDIO/rapoarte/S_showrunner.md` | 104333 | `6ade4a2018a8a4c0416707e0b3d88c674abbee33614d6d7e0e6ffa985a8a8737` |
| `01_CANON/01_DECIZII_PRODUCATOR.md` | 6718 | `dd0128b800270b219435b0b841f39232146fb96f88da94047e356817b8e44bdf` |
| `00_STUDIO/audit/00_CONTRASEMNARI_PRODUCATOR.md` | 1094 | `f5acdb54d286419b7cff509bf4183c2ec7471e57de0d21dacf34691978318588` |
| `00_STUDIO/audit/00_REGISTRU_AUDIT.md` | 34460 | `fd9f9cebf15b9d60714b502eb58f4e2bfbf92fd56351568a524c747636ef8701` |
| `00_STUDIO/02_BRIEFURI/A1_A6_brief.md` | 3876 | `97daf0f2e5a78ea589c3a129e7959cc612c4fed8cac277ea4261188f5417d0c5` |
| `00_STUDIO/02_BRIEFURI/AU-C_brief.md` | 11926 | `19774a6398330dbc1a91e893eea871880d502d3e487c39c611eb3659ec977aa9` |
| `00_STUDIO/02_BRIEFURI/AU-K_brief.md` | 11644 | `d397d07358020f75b459c6d9ec28110bc989bb5bc8e5e52c584b74ddb8a57162` |
| `00_STUDIO/02_BRIEFURI/AU-M_brief.md` | 12699 | `63e337aa446f0575481566a5dc92b3078d1ef86a2323c4b67c6daef354db5201` |
| `00_STUDIO/02_BRIEFURI/A_brief.md` | 12221 | `4d0108f82a2fc48ae80bcc1c4200d7dcff414955d3b1b8b151f78b7032025294` |
| `00_STUDIO/02_BRIEFURI/B_brief.md` | 12141 | `029b12f3a1b44e2487c35f37184e3cff6a3808e9e7b0e6be7df5b40e77f4c9ac` |
| `00_STUDIO/02_BRIEFURI/C_brief.md` | 11914 | `452f9439b9bc0ea26945c81074d0eaf3d12ce0be1091501ccc0dc7219e391ba2` |
| `00_STUDIO/02_BRIEFURI/D1_brief.md` | 15078 | `d58bc6643dd3f18d288d27972eb96664d55c2d39e4b1c00c28923f143393eac5` |
| `00_STUDIO/02_BRIEFURI/D2_brief.md` | 9752 | `dc914659ad9671a82f70defefd61c05ce767f0ffb567101117eb1ed719ba6a86` |
| `00_STUDIO/02_BRIEFURI/D3_D6_brief.md` | 12864 | `0407f5978c2a3caa299260c5f6c620b8970c8b0fc30d514bcb1376dd50a68f2d` |
| `00_STUDIO/02_BRIEFURI/E2_brief.md` | 4101 | `4797b48461e5cc9dc5b32319b5beea4745c4f1ccaca0f16a773db3588fb6616d` |
| `00_STUDIO/02_BRIEFURI/E3_brief.md` | 3390 | `f891284cee74afed4baedc6b495f24675453a5a91363e929054308f322039468` |
| `00_STUDIO/02_BRIEFURI/E4_brief.md` | 3431 | `7ef03eb62b1ae7ec8caba39ff100b061cb177cd6b64b3b908e9ec0a689405a86` |
| `00_STUDIO/02_BRIEFURI/E_brief.md` | 13000 | `b81884f5b40e75c864a1349178ef5be6e88faf9f0249c6e1f7caeadb7634016b` |
| `00_STUDIO/02_BRIEFURI/F1_brief.md` | 11271 | `1cc4c1e58f4da43db6f5b84d8456dadf03a9e62c5bb1f7c14ce818b0c88af8b9` |
| `00_STUDIO/02_BRIEFURI/F2_brief.md` | 9065 | `92d5c04d086c5c95456feb2e256b78d50fddbea26036d37bad61dd1eb10d5589` |
| `00_STUDIO/02_BRIEFURI/GR-S_brief.md` | 7672 | `8b4cb9d18d6fa3232a18d514799cd3cdcf4b2b9c9c5661cdaea6bf354a88a58f` |
| `00_STUDIO/02_BRIEFURI/GR_brief.md` | 7329 | `f1860a610fe468f059470774509df3cf733511afa18ec3d662aa90faa5e0dc82` |
| `00_STUDIO/02_BRIEFURI/H1_brief.md` | 7471 | `d6e33a37b27b5c825085660d1ac049083b623722eb9e6356c6812ff3a5ab1fd9` |
| `00_STUDIO/02_BRIEFURI/H2_brief.md` | 4932 | `e8ab8337fe01d6e78e26a05c3c3193ef5efec6612dbc79966e69f00a951ef2aa` |
| `00_STUDIO/02_BRIEFURI/H3_brief.md` | 7971 | `830a143c29610f6f37cb68c138b8742ba35a94685f15fc5583276a63ad7e4a2f` |
| `00_STUDIO/02_BRIEFURI/H4_brief.md` | 4834 | `73e3798c84f61fc630d3a31ce899116060ee1669a9d36ee18255022f7dc637b6` |
| `00_STUDIO/02_BRIEFURI/H5_brief.md` | 4063 | `146576b51b143157a60ce9232160854b26199974afc3657707e089362609ed73` |
| `00_STUDIO/02_BRIEFURI/MS_brief.md` | 8144 | `b09462c61ee15f4c43ea5c68c3acba8834a9dbd87090a58e85aae1d11424d9c9` |
| `00_STUDIO/02_BRIEFURI/S_brief.md` | 21023 | `fefdc2d92f818177a18324617d137c65fb54d05cdfee0cb10066174306c4eff4` |

### Dovezi R4 citite/verificate

| Fișier relativ la dosarul G0-STUDIO-v4 | SHA-256 |
|---|---|
| `R4_audit_canon.md` | `6613628da8a166f3d3eea05e0db48519a8f1be3520eddd5b03796a1bf5705b80` |
| `R4_audit_craft.md` | `f3885eb004e29dc052860f7ebd40cb2a3dbfd745d021984855cff4b0e565543e` |
| `R4_audit_kpi.md` | `c682999f90fc91785de6ec27bf78b3505c9de16ae1dafd661c219ef190a5e9e1` |
| `R4_plan_masuri.md` | `d79b69bbae4f3e7da897645fbaa4b2f22286324ce9398328af5ef49fb0fb7d27` |
| `R4_corecturi/EXECUTIE.md` | `7ca362c8785b605cc6173e34e1c9ee604f6b0261fe40b2a5b11f83546c0e24bf` |
| `R4_corecturi/manifest.json` | `205e5cb4dabdd8a427189148f168430af816e2cecb506ab27102eebe43b21587` |
| `R4_corecturi/rezultat.json` | `d369a904de3716f40ba46debe09451a0eceec65db4a282b831f5723cfb1d6127` |
