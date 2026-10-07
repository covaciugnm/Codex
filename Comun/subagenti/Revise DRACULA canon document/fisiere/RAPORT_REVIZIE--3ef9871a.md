# Raport separat de revizie — G0-CANON-v4, v4.2

Data UTC a generării: 2026-09-24T09:23:55.736350+00:00. Autor: agentul de revizie Codex din această sarcină. Nu este raport de auditor și nu conține o notă. Niciun agent nou nu a fost lansat.

## E.1 Livrabilul și starea auditului

Canon: `D:\00. Downloads\Dracula Book\DRACULA-COMICS-CODEX-G0-20260924\01_CANON\00_CANON_NUCLEU.md`. SHA-256: `243630e9071df7c7ee15cbf9f079fdac69f1d292950daab42cf927f36aa9ab26`. Versiune: v4.2. Copie stabilă: `predat/00_CANON_NUCLEU.md`; manifest: `MANIFEST.json`, `SHA256SUMS.txt`. Aceleași octeți trebuie folosiți de toți cei trei auditori. Orice corectură ulterioară cere alt instantaneu; nu se auditează un fișier aflat în scriere.

Ultimele rapoarte independente găsite în dosarul propriu sunt R1: AU-C 9,31, AU-M 8,70, AU-K 8,70, pe v4.0. Nu se transferă la v4.2. Poarta de 9,50 de la fiecare auditor nu este trecută și nu este revendicată.

## E.2 Măsurile și atribuirea

`MASURI_39.md`: 39/39 măsuri inventariate cu stări și dovezi. `DEFECTE_64.md`: 57 defecte + 7 observații. Baza izolată era deja v4.1; majoritatea corecturilor R1 existau înaintea acestei sarcini. Nu le revendic ca implementări proprii. `diff_propriu.patch` este dovada exhaustivă a contribuției mele; `modificari_proprii.json` descrie prima etapă, iar diff-ul final include și condensarea, OBS-10 și corecturile ulterioare.

## E.3 Integritatea bazei

Baza izolată, exactă: `inainte/00_CANON_NUCLEU.md`, SHA-256 `eef72462df479ad0d88231aae6b0a9ead3a74df4621c5ceb88cc88961bcabad7`. Diferă de prima captură din original (`f553eb7d…bfcd8`) și de captura concurentă (`f9c6a3e2…62434`). Copiile acestora se află în dosarul anterior copiat `REV_20260924_120416/inainte/`. Diferențele sunt arhivate separat; nu sunt atribuite acestei revizii. Originalul nu a fost scris. Nu s-a găsit AGENTS.md în proiect ori în directoarele părinte verificate; AGENTS.md din profilul Codex era gol.

## E.4 Verificări reale

`verifica.py` și `verifica_url.py` folosesc numai rădăcina izolată. Nu am rulat scriptul R0 cu rădăcina originală. Scriptul R0 moștenit avea verificări lexicale și un prag vechi de 40 de cuvinte; verificatorul nou păstrează obiectivele structurale și explică limitele, fără a simula audit semantic.

Rezultate: {'OK': 39, 'ECHEC': 1}. Erori raportate: ['VC32']. Textul are 24971 cuvinte. URL-uri: 181, distribuție {'200': 173, '202': 1, '403': 5, '302': 1, '503': 1}. Accesul 202/302/403 sau o eroare de server nu certifică o sursă. Fișierele `stare_url*` păstrează încercările și excepțiile. Rezultatul structural se rerulează pe copia predată și se compară; HTTP este observație datată, nu rezultat reproductibil garantat.

## E.5 Trasabilitate și decizii blocate

Matricea defectelor: `DEFECTE_64.md`. Deciziile rămân 15; numele Ioana Mureșan rămâne blocat. Titlul DRACULA, eroul de zi, moda și glamourul Bond, burlăcia prezentului și despărțirea Paris 1794 sunt păstrate.

| Decizie | Aplicare în canon | Locație |
|---|---|---|
| 1 | §2; rezumatul deciziei din antet păstrat | r. 78 |
| 2 | §3; rezumatul deciziei din antet păstrat | r. 95 |
| 3 | §8; rezumatul deciziei din antet păstrat | r. 328 |
| 4 | §5; rezumatul deciziei din antet păstrat | r. 149 |
| 5 | §2; rezumatul deciziei din antet păstrat | r. 78 |
| 6 | §19; rezumatul deciziei din antet păstrat | r. 764 |
| 7 | §17; rezumatul deciziei din antet păstrat | r. 689 |
| 8 | §1; rezumatul deciziei din antet păstrat | r. 66 |
| 9 | §13; rezumatul deciziei din antet păstrat | r. 449 |
| 10 | §6; rezumatul deciziei din antet păstrat | r. 243 |
| 11 | §5; rezumatul deciziei din antet păstrat | r. 149 |
| 12 | §20; rezumatul deciziei din antet păstrat | r. 829 |
| 13 | §8; rezumatul deciziei din antet păstrat | r. 328 |
| 14 | §20; rezumatul deciziei din antet păstrat | r. 829 |
| 15 | §8; rezumatul deciziei din antet păstrat | r. 328 |

## E.6 Relectură, cercetare și KPI

32 de identități și vârste calculate: `identitati.json`. Repere cinematografice: `clisee_24.md`. Informația personajelor: `cine_stie.md`. Scanarea tuturor absolutelor: `scan_absolut.csv` (inventar, nu certificare semantică automată). Cuvinte pe secțiuni: `rezultat_verificari.json`.

Corecții proprii: excepția Valentin la 46 de ani, termenul identității curente 2038, formula identică §4/§19; R7 în fișa rapidă; R9 și Protocolul Mureșan; excepția Hanzer 1915–1916 și succesorii ramurii vieneze; ochelarii din 1604 ca invenție BD, fără atestare falsă a atelierului; eliminarea priorității false din 1929; aniversarea civilă, păstrând conversia iuliană în §3.1; stingerea progresivă în R4; OBS-8 și OBS-10 acceptate. Nota confidențială nu mai certifică impropriu compatibilitatea tuturor ipotezelor C.

Surse consultate punctual: [muzeul de optică — ochelari de soare](https://www.college-optometrists.org/the-british-optical-association-museum/history-fashion-sunglasses), [construcția ochelarilor](https://www.college-optometrists.org/the-british-optical-association-museum/the-history-of-spectacles), [17 USC, capitolul 3](https://www.copyright.gov/title17/92chap3.html), [Directiva 2006/116/CE](https://eur-lex.europa.eu/legal-content/RO/TXT/?uri=CELEX:32006L0116), [California §3344.1](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=3344.1.&lawCode=CIV), [hotărârea austriacă din 15.05.2019](https://www.ris.bka.gv.at/Dokumente/Vwgh/JWT_2018010076_20190515L00/JWT_2018010076_20190515L00.pdf). Sursele legale stabilesc reguli generale, nu un aviz pentru fiecare material DRACULA. Muzeul nu confirmă perechea fictivă de ochelari din 1604.

**Propunerea M1.6 către Producător:** păstrarea numelui blocat până la decizia explicită. Dacă dorește redenumire, variante de lucru: Ioana Vetriceanu, Ioana Brădetu, Ioana Sălceanu. Interogări exacte cu domeniile Wikipedia, portal.just.ro și politiaromana.ro: `cautari_nume.json`. Rezultatele vizibile pentru Sălceanu sunt potriviri de termeni separați, nu dovada unei identități exacte; nu declarăm numele liber ori rar statistic. Corbeanu a fost abandonat la prefiltrare după o potrivire nominală în indexul portalului. B și H1 verifică variantele și grafiile fără diacritice înaintea deciziei din 02.10.2026. Pentru tren, căutarea „L’Express des Deux Empires” a produs rezultate lexicale nespecifice; nu dovedește disponibilitatea unei mărci. Numele trenurilor rămân provizorii până la H1.

| KPI S (fișa curentă K1–K13) | Măsurare / limită |
|---|---|
| K1 | Cele 15 decizii păstrate; neconcordanțele interne de mai sus corectate. K1 global nu este declarat 0: documentele B/C/Studio trebuie sincronizate și AU-C măsoară. |
| K2 | Brief-urile nu sunt livrabilul acestei revizii; Studio. |
| K3 | Intrarea pentru jurnal este propusă în E.9; jurnalul nu a fost scris. |
| K4 | Planul R1 existent; fără ședință nouă inventată. |
| K5 | Corespondență în corespondenta_jurnal.md; OBS-8 și OBS-10 decise. Actualizarea jurnalului și termenul global de 48 h: Studio. |
| K6 | Dovezile acestei revizii arhivate; trei rapoarte independente noi încă lipsesc. |
| K7 | Media rundelor nu se calculează pe acest singur livrabil; registrul aparține părintelui. |
| K8 | Mandatul utilizatorului și contrasemnarea generală existente; nu sunt transformate în aprobare editorială nouă. |
| K9 | Căutare normalizată în canon, cu martori pozitivi, VC1/27: 0 urme interzise. Alte documente nu sunt certificate aici. |
| K10 | Buletinele săptămânale: în afara scopului. |
| K11 | Nicio procedură de audit v5 executată; doar verificări de autor. |
| K12 | Mediana AU-M pe livrabile creative nu este încă măsurabilă aici. |
| K13 | Măsurătorile de audiență: etapă ulterioară; nu se inventează date. |

## E.7 Diferențe și aviz de aliniere

`diff_propriu.patch` separă strict contribuția de baza izolată. Condensarea prezentării și a trimiterilor bibliografice redundante păstrează §1–§20 și registrul istoric integrat. Nu au fost modificate documente ale altor autori.

| Destinatar / cale relativă rădăcinii izolate | Măsura concretă |
|---|---|
| Studio: 00_STUDIO/01_ECHIPA_SI_ROADMAP.md; 03_JURNAL_PROGRES.md; rapoarte/S_showrunner.md | Sincronizare numai după această predare; v4.2 și amprenta E.1; OBS-8 → V4-83, OBS-10 → V4-87; fără atribuire retroactivă. |
| C: 04_LUME/02_REGULILE_NOPTII.md | Opt elemente R1: titlul eliminat; antetul vechi; numele galeriei; numele medicului; art. 1; veto după 1794 și sentința incompatibilă; puterile de zi; propunere de nume de fișier. În plus: R7/R9, cele 7 pietre, stingerea și Hanzerii. |
| C: 04_LUME/01_CRONOLOGIE_SECOLE.md; 06_TRASEUL_CAPITALELOR.md | Virgilio Dal Drago, vârstele, Dochia și prețul trezirilor, rolurile Hanzer, mormântul Mihnea, ochelarii și data scenei. |
| C: documentul confidențial | Aliniere la v4.2, R3 și pivoturi; nota de compatibilitate integrală este retrasă. Nicio ipoteză nu este divulgată aici. |
| B: 03_PERSONAJE/02_FAMILIA_DRACULESTI.md | Reconcilierea Konrad/Georg/Andreas, succesorii vienezi, somnul Dochiei, statutul Sânzianei; verificarea numelor. |
| E: 05_ART/ | Ochelarii (ficțiune/atestare), paleta de zi, un accent de culoare, pagina 4 cu artă nouă, trenurile fictive cu H1. |
| A: 02_RESEARCH/; F1: 09_SITE/ | Loglinia de 44 de cuvinte, comparabilele, separarea informației interne de materialul public. |
| D1 și D3–D6 | OBS-8/OBS-10, cele trei date fixe, luna de stingere, arcul interior, pista inelului; fără romantism Ioana în S1. |

## E.8 Abateri explicite și restanțe

Instrucțiunea utilizatorului prevalează asupra planului: nu se editează S_showrunner, jurnalul, registrul central sau alte documente; raportul de față înlocuiește execuția în acele fișiere. Planul R1 și auditurile vechi nu au fost rescrise. M1.1 este reluat pe baza exactă izolată, nu pe hash-ul istoric v4.0. Arhiva R0 rămâne intactă: nota ulterioară de reconstituire bit-cu-bit depășește afirmația mai veche că reconstituirea nu era posibilă; această revizie nu rescrie retrospectiv acele note.

Rămân: trei auditori independenți pe aceeași copie; verificarea semantică integrală a absolutelor și istoriei (M1.37); alinierea documentului C și a celorlalte documente la G1; avizele H1, decizia asupra numelui și confirmarea disponibilității mărcilor; accesul la sursele cu răspuns neconcludent. Aceste limite sunt vizibile și nu primesc închideri sau note fictive. Nu s-au inventat ședințe, date de piață ori rezultate de audit.

## E.9 Predare către părinte

Intrare propusă: „Canon v4.2 revizuit în copia izolată, pe baza eef72462…abad7. OBS-8 și OBS-10 acceptate; raport separat, copie stabilă și manifest în REV_IZOLAT_20260924. Urmează trei auditori independenți; poarta rămâne nepromovată.”

Părintele deține registrul. Studio integrează raportul după sincronizare. Autorul canonului a scris numai 01_CANON/00_CANON_NUCLEU.md și propriul dosar REV_IZOLAT_20260924. Nu va modifica copia predată pe durata auditului.
