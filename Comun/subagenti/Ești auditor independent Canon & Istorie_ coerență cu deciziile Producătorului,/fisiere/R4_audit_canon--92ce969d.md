# G0-STUDIO-v4 · R4 · Audit independent Canon & Istorie

**NOTĂ: 8,20 / 10 — FAIL.** Un defect critic de aliniere la regula aprobată a vehiculelor, un defect major privind monumentele și două defecte minore. Absența site-ului final sau a implementărilor G1 nu este penalizată.

## Perimetru și hashuri

Data: 24.09.2026. Auditor independent Canon & Istorie, fără contribuție la revizii și fără agenți lansați. O singură lentilă independentă pe două livrabile; nu pretind trei evaluări independente.

ROOT: `D:\00. Downloads\Dracula Book\DRACULA-COMICS-CODEX-G0-20260924`.
Pachet fix: `ROOT/00_STUDIO/audit/RELUARE_CODEX_20260924_120350/PACHET_AUDIT_01`. Toate rândurile indicate mai jos se referă la acest pachet. Referințele istorice au fost accesate numai în ROOT; căile absolute vechi din istoric nu sunt defecte prin simpla lor existență.

Am recalculat SHA256 și mărimea tuturor celor 32 de fișiere din manifest: **32/32 conforme**, inclusiv reverificarea înaintea redactării.
Manifest SHA256: `ca227d6345d935317ffb4780b6cd8286a874fbd165f4eda3c18ba907536847ac`.

| Fișier | SHA256 |
|---|---|
| Canon v4.2 | `243630e9071df7c7ee15cbf9f079fdac69f1d292950daab42cf927f36aa9ab26` |
| Organizare v4.3 | `d934ae4f3880962f1cc72ae8ee56dc213e40436a6ee43399dd274be344a853ac` |
| Jurnal | `4285ae42e7c63dc34bef438b12eda0c9b5e5fc1ed0bc39f473a3a363a890016c` |
| S_showrunner, anexă de stare | `3b32d634dcea786b7f907eb2c122e5ed6b43403e4cc193920179c375b2f616a0` |
| Registrul deciziilor | `dd0128b800270b219435b0b841f39232146fb96f88da94047e356817b8e44bdf` |
| Contrasemnări | `f5acdb54d286419b7cff509bf4183c2ec7471e57de0d21dacf34691978318588` |

Procedura din ROOT, verificată fără execuție: `00_STUDIO/audit/00_PROCEDURA_PIPELINE_v4.js`, SHA256 `2c13db6a6d9a8817e70538fa8df4ff7c7ba6378140c0102590db53e3ad403ead`.
Referința confidențială autorizată: `04_LUME/05_MISTERUL_OMULUI_FARA_UMBRA.md`, SHA256 `483961ee2ec2ac98dffa4447e808dd18a1efaf07454014f267d126852df0d6ca`. Consultată pentru compatibilitate; nicio identitate secretă nu este reprodusă.

Grila păstrată: PASS iff nota ≥9,50; major plafonează la 9,20; critic plafonează la 8,50; neconcordanță cu decizie aprobată = critic; minorele se cumulează. Notele vechi nu sunt transferate. G0 nu este aviz juridic sau certificare comercială externă.

## Metoda reală și limitele lecturii

Lectură integrală, cu recuperarea pasajelor principale trunchiate: canonul (873 rânduri), organizarea (1.888), jurnalul (470), cele 15 decizii și contrasemnările. S este anexă de stare consultată țintit: antet, delimitarea istoricului, starea Studio, OBS și integrarea predării. Nu revendic lectura sa integrală și nu extind retroactiv perimetrul vechilor audituri.

Am consultat auditurile AU-C precedente, măsurile relevante din planuri și dovezile autorilor. Am citit `REV_IZOLAT_20260924/MASURI_39.md`, `DEFECTE_64.md`, `RAPORT_REVIZIE.md` și `CODEX_R3_verificari/EXECUTIE_FINALA.md`. Briefurile au fost confruntate pe pasajele relevante, nu certificate integral. Nu pretind lectura integrală a tuturor planurilor, probelor și rapoartelor celorlalte lentile.

Verificări proprii read-only: hashuri/mărimi, text și trimiteri normative, recalcularea celor 32 de identități transcrise din tabel (durată = creștere de vârstă în 32/32 cazuri; formula pentru durate peste 12 ani respectă toleranța), cele 11 armistiții la 50 de ani (1526–2026), 2019+7=2026, vârstele Vlad 33 în 2026, Sânziana 28 în 1462, Ilinca 16 în 1679 și Iosif 58 în 2026. Excepția Valentin, 46 de ani la încheiere, este declarată. Nu am rulat verificatoarele autorilor ori procedura cu rădăcină originală. Testele autorilor nu înlocuiesc judecata semantică.


## Puncte forte

- Antetul referă exact canonul predat; AP-19 impune realiniere la schimbarea lui. Hashul este corect, chiar dacă echivalența semantică nu este completă.
- Registrul deciziilor este restaurat în matricea accesului; contrasemnările au rând propriu.
- Ordinea text românesc final → traducere, protecția deznodământului și ordinea publicării în aceeași zi sunt explicite. OBS-8/10 sunt acceptate în canon.
- H5 include scenariul Ep. 1 înainte de G4; C K6/E K3/F2 K11 leagă costumul de o sursă iconografică la data scenei.
- Decizia 15 este recunoscută pentru planuri, distinct de lucrul pe risc și oprirea vechiului G0.
- Documentele vechi C/B și generatorul site-ului sunt sarcini G1. Defectele de mai jos apar în instrucțiunile operative G0.

## Defecte confirmate

| ID | Gravitate | Locație exactă | Probă și efect | Remediu verificabil |
|---|---|---|---|---|
| R4C-01 | **CRITIC** | `00_STUDIO/01_ECHIPA_SI_ROADMAP.md:1677`, RS28; nota juridică a Producătorului; canon `01_CANON/00_CANON_NUCLEU.md:471` | RS28 include *Orient Express* între mărcile de loc și permite folosirea descriptivă în interior. Registrul aprobat cere vehicule generice/fictive până la verificare juridică; canonul include trenurile explicit și cere decizia Producătorului după H1 pentru excepții. M1.5(b) din planul contrasemnat cere scoaterea numelui real al trenului din lista locurilor. Nu există aici derogare nominală aprobată. | Eliminarea trenului din excepția RS28 și folosirea numelui fictiv/generic din canon. Test: nicio regulă operativă nu permite marca trenului prin simpla clasificare ca „loc”. Excepția necesită dovada deciziei specifice; mențiunile bibliografice legitime se păstrează. |
| R4C-02 | **MAJOR** | Organizare `:1676`, RS27; canon `:473`; H1 organizare `:682` și `02_BRIEFURI/H1_brief.md:20` | „În interior, desen liber” și indicatorul „0 coperți fără aviz” omit verificarea cerută de canon după teritoriu și utilizare, inclusiv în interiorul BD. Nu afirm că orice desen este ilegal: contradicția este eliminarea controlului canonic. | RS27 și inventarul H1 includ evaluarea utilizărilor interioare relevante. Test: o pagină interioară cu un bun cultural italian intră în evaluarea utilizării concrete, fără declarație automată de libertate. |
| R4C-03 | minor | Organizare `:519`, `:550`, `:682`, `:1668`; `D3_D6_brief.md:60`, `E_brief.md` K4; canon `:464/471` | Hotelurile sunt atribuite celor „9 categorii” ale regulii 11, iar proza trebuie să aibă zero mărci reale inclusiv de hoteluri. Canonul le clasifică la locuri și permite numirea descriptivă în interior, inclusiv Plaza/Ambassador. Restricție suplimentară atribuită greșit canonului. | Separarea hotelurilor/locurilor de obiectele regulii 11 în liste, numărători și briefuri. Test: numirea descriptivă a hotelului în interior nu este respinsă automat ca marcă de obiect; utilizările externe respectă regula 4. |
| R4C-04 | minor | Organizare `:1682`, RS33; jurnal `:65–69`, `:78`; S `:3`, `:203`, față de organizare `:11`, jurnal `:9`, S `:313` | Hashul și predarea v4.2 sunt corecte, dar RS33 încă spune „fără ieșire pe disc după 08:32:09” și urmărește v4.1. Inventarul datat 12:16 în copia izolată descrie canon v4.0 neschimbat și organizare v4.2. S încă spune „rămâne de sincronizat”, deși integrarea finală există. Sunt etichete curente/datate, nu numai istoric explicit. | Actualizarea indicatorului RS33 și a celulelor de inventar/stare; păstrarea vechilor valori numai în istoric etichetat. Test: aceeași predare nu mai este simultan integrată și „nepredată/nesincronizată”. |

Calcul: plafon critic **8,50 − 0,20** pentru R4C-02 **− 0,05 − 0,05** pentru minore = **8,20**.
R4C-01 este critic conform regulii utilizatorului privind deciziile aprobate, coroborată cu nota Producătorului și M1.5 contrasemnat. Nu este concluzie juridică despre marcă. Defectul de transcriere al canonului nu este penalizat încă o dată aici: Studio l-a declarat și nu putea edita copia înghețată.

## Închiderea măsurilor precedente relevante

| Măsuri / defecte R3 | Stare și dovadă |
|---|---|
| M3.2 / R3C-1, matricea | Închisă în documentul curent: §8.2, r. 1301, registrul restaurat și contrasemnări prezente. Nu certific toate cele 34×22 celule istorice. |
| M3.3, M3.29, verificatoare | Fără închidere tehnică independentă integrală: execuția descrie martori V8/V45/V40, dar nu i-am rerulat. |
| M3.4 | Închisă ca consemnare: jurnal §6 cu evenimente și erată; istoria completă a scrierilor nu este recertificată. |
| M3.5–M3.6 / R3C-2–3 | Închise ca reguli G0: §9.4, regula 3(i)–(v), româna înaintea traducerii, BD primul în aceeași zi, excepție Ep. 1 explicită. Nu pretind recalcularea tuturor termenelor. |
| M3.7–M3.8 | Închise semantic față de canon: structură orientativă și OBS-10 acceptată; calitatea literară viitoare nu este certificată. |
| M3.11 | Închisă în fișe și extrasele C/E: C K6, E K3, F2 K11, sursă iconografică la data scenei. |
| M3.12 | Închisă: AP-16 tratează S ca anexă de stare, fără perimetru retroactiv inventat. |
| M3.13–M3.14 | Parțiale: istoric S delimitat și integrare prezentă, dar R4C-04 rămâne. |
| M3.15 / R3K-7 | Parțială: hash/AP-19 corecte; RS27/RS28/categoriile nu sunt semantic aliniate (R4C-01–03), iar RS33 este învechit. |
| M3.16 | Îndeplinită ca specificație G0; implementare G1 neevaluată: F1 și regulile de acces cer mascare/protecție. Site final nesolicitat la G0. |
| M3.17 | Verificată ca atribuire/regulă AP-17/AP-18; întreaga arhivă nu a fost recertificată prin V29. |
| M3.18 | Închisă: MS K4 și decizia 15 recunosc aprobarea generală. |
| M3.20–M3.21 / R3C-4 | Închise ca acoperire: H5 K3/G4/GS includ Ep. 1 și aviz înainte de PASS pentru flashback-urile 1431–1476; avizul nu este pretins deja emis. |
| M3.22 / R3C-5 | Închisă textual: AU/MS acoperă ultima rundă la 19.10.2027; capacitatea de execuție nu este certificată. |
| M3.27–M3.28, partea AU-C | Îmbunătățiri confirmate, fără închidere globală: regula datei scenei și istoric separat; rămâne R4C-04. |
| M3.1, M3.31 | Predarea comună 32/32 verificată; hashurile E.1 concordă; istoricul nu este recertificat. |
| M3.9–M3.10, M3.19, M3.23–M3.26, M3.30 | Fără închidere integrală proprie pe craft, piață, capacitate, calendar și autorevizuire. Nu sunt declarate defecte prin această limită. |

## Surse și limite

Pentru R4C-02: [Normattiva, art. 107](https://www.normattiva.it/uri-res/N2Ls?urn%3Anir%3Astato%3Adecreto.legislativo%3A2004-01-22%3B42~art107=) și [Parlamentul italian, D.Lgs. 42/2004](https://www.parlamento.it/parlam/leggi/deleghe/04042dl.htm), art. 107–108. Textul privește condițiile folosirii/reproducerii, nu libertatea universală rezultată din amplasarea în interiorul cărții. Pagina Parlamentului redă actul inițial; accesul direct la forma consolidată a art. 108 a eșuat. Nu deduc legalitatea actuală din textul vechi: defectul este demonstrat prin contradicția directă cu canonul actual. H1 stabilește aplicarea concretă.

Verificările istorice punctuale comune sunt documentate în R2 (KHM, BSB, USTC, RIS). Nu am reatestat toate afirmațiile istorice/juridice pe surse primare; nu declar „toate corecte”. Nu certific în această rundă legislația minorilor, clasificarea figurinei, drepturile filmului sau toate termenele comerciale. Calendarul de producție nu a fost recalculat integral pe zile lucrătoare.

Nu am verificat integral toate briefurile, anexele, probele sau echivalența tuturor tabelelor istorice. Dosarul confidențial C rămâne de aliniat la G1; nicio identitate nu este divulgată. Lipsa implementărilor și a avizelor viitoare nu devine defect G0.

**Remediile se aplică într-o revizie nouă, cu manifest și audit nou. Copiile înghețate rămân intacte.**
