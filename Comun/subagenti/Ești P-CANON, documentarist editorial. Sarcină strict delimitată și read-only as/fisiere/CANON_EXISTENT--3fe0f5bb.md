# SEL-001 — CANON EXISTENT pentru selecția preliminară

Autor de lucru: P-CANON, documentarist editorial. Verificarea inițială r01 și implementarea r02 în staging: 24.09.2026, Europe/Bucharest. Integrare și actualizare metadate de predare: P-MANAGER, după conservarea r01-after-audit.

**Identificator: SEL-001. Etapă: G00 — configurare. Tip: anexă de SELECȚIE PRELIMINARĂ. Stare: DRAFT, neaprobat.** Raportul nu reprezintă închiderea G01 — canon integral și nu certifică lectura integrală a celor aproximativ 95.000 de cuvinte din Hotelul V2. Documentează probele deja obținute, întinderea exactă a lecturii și ce rămâne pentru G01 înainte de scriere. Nu autorizează un roman nou, o rescriere a surselor sau publicarea. P-CANON nu acordă scoruri și nu își auditează propriul livrabil; auditurile independente sunt pregătite separat de coordonator.

**Versiune: r02, integrată pentru reaudit independent după metaauditul și arhivarea r01.** Corecția documentară privește findingul `SEL-001-A-CANON-F01` din auditul `SEL-001-A-CANON-r01`; în acest raport este urmărit și ca H-C9. Versiunea r01 din arhivă, auditul cu verdict RETURN și planul r01 rămas PLANIFICAT sunt păstrate neschimbate. Implementarea și integrarea nu închid findingul și nu constituie acceptare de autor sau audit independent. G01 rămâne blocat pentru închidere și scriere; documentarea integrală și deciziile explicite de canon sunt încă necesare.

## 1. Concluzie și comparație

Recomandarea este **AMORIS / Isabella Morgan — Rue des Âmes, volumul 2: The Magenta Letters**, deoarece continuarea este anunțată explicit în masterul real Hotelul V2: H, P3981–P3984, în special „BOOK TWO: THE MAGENTA LETTERS” și „(Margaux's Story)”. Nu este un titlu inventat de acest raport. Epilogul pregătește aceeași poveste prin Margaux Beaumont, camera 14 și un plic încă sigilat; jurnalul V2 o confirmă separat la HC, L684–L685.

Recomandarea privește alegerea direcției de continuare. Nu înseamnă că întregul master este coerent: numele de familie al lui Alexandre — Boucher la H P166/P860, Dubois la H P3548/P3550 — este nereconciliat (H-C9 / SEL-001-A-CANON-F01), iar cronologia, ceasul lui Antoine și familia lui Alexandre necesită decizii editoriale explicite. Căsătoria cu Isabella este documentată separat la H P3553; nu validează una dintre formele numelui. Nu se poate transfera automat în volumul 2 nici itinerarul public Paris–Tokyo, nici vechiul plan Lisabona, nici o Isabella redevenită singură și fără familie.

| Opțiune în serie începută | Bază efectivă | Continuare susținută de surse | Probleme înainte de fixarea canonului | Recomandare documentară |
| --- | --- | --- | --- | --- |
| **Isabella Morgan / Rue des Âmes, vol. 2** | Un titlu în catalog; H este master EN autentic. | **The Magenta Letters**, povestea lui Margaux; plic adresat camerei 14, indiciu „M.”, registru din 1968. H, P3885–P3946; P3981–P3984. | Contradicții interne H, inclusiv numele nereconciliat Alexandre Boucher/Dubois (H-C9 / SEL-001-A-CANON-F01); HB este un jurnal vechi de revizii; Lisabona și itinerarul de pe site nu coincid cu promisiunea finală. | **Prima alegere, DRAFT.** Are titlu și fir de continuare identificabile direct, cu un nucleu restrâns de personaje și obiecte ce poate fi documentat. |
| **Alex Damian — următorul volum după clarificarea Beneath/Shadows** | Două titluri afișate în saga Alex. B și SH sunt texte EN distincte, dar reiau întâlnirea acelorași protagoniști. | B lasă deschisă o posibilă expediție la Delos, compatibilă cu viața de familie. SH lasă deschisă continuarea descoperirilor din jurul „Swan”. B, P2659–P2663; SH, P2120–P2129. | Nu este stabilit un lanț narativ coerent între cele două volume. Numerotarea „vol. 3” ar fi de catalog, nu o cronologie narativă validată. Nu există în finalurile citite un titlu explicit al următorului volum. | **Rezervă.** Mai întâi trebuie stabilit dacă SH este continuare, versiune alternativă ori altă amplasare în cronologie; raportul nu decide reclasificarea. |
| **Ten Crowns, vol. 2** | The Northern Crown este primul titlu public; master local N, V3 EDITED-FINAL. | **The Eastern Sands**: consecințele revenirii lui Dorian la viață, conducerea League of Crowns și amenințări din Eastern Desert. N, P3785–P3792. | Planul arhivat numește vol. 2 **The Crown of Waters** și continuă războiul cu Malachar, deși N îl ucide și formalizează deja alianța a cinci regate. Anexele au și contradicții proprii. | **A treia alegere pentru pornire imediată.** Promisiune puternică, dar necesită reconcilierea unei arhitecturi de serie mai largi. |

Această ordine este o judecată editorială asupra clarității continuității și întinderii reconcilierii necesare. Nu reprezintă scor literar, prognoză comercială sau aprobare de producție.

## 2. Metodă, niveluri de certitudine și identificarea surselor

Sursele au fost accesate exclusiv pentru citire. În r01, site-ul a fost verificat prin cereri HTTP GET; nu au fost folosite formulare, conturi, comenzi comerciale sau operații de publicare. În r02_staging nu s-a reverificat site-ul: datele, amprentele și acoperirea inițială de mai jos sunt păstrate ca înregistrare a verificării r01, nu ca lectură ori acces HTTP repetate. Verificarea suplimentară r02 constă în reextragerea H, căutarea variantelor de nume și lectura pasajelor indicate în §4.2.1, plus controlul de regresie al întregului raport. Nu au fost citite fișiere `.env` și nu au fost folosiți subagenți. Mandatul r02 permite numai prezentul fișier în `02_DOCUMENTARE/r02_staging/CANON_EXISTENT.md` și rezultatul în `06_REGISTRU/MASURI/SEL-001-rezultate-r02.md`, create prin `apply_patch`; nu modifică originalul înghețat, planul r01, sursele, site-ul sau manifestele.

Etichete utilizate:

- **CANON CERT ÎN MASTER**: în acest SEL-001, eticheta înseamnă exclusiv că faptul este afirmat explicit în pasajele inspectate și nu are, în verificările efectuate, o contradicție identificată asupra acelei afirmații. Este o constatare locală pentru selecția G00, supusă verificării integrale G01; nu certifică absența contradicțiilor în pasajele necitite integral și nu închide canonul universului.
- **PROMISIUNE DE CONTINUARE**: anunț sau angajament din final/teaser; dovedește promisiunea făcută cititorului, nu că evenimentul viitor s-a produs deja.
- **CONTRADICȚIE**: două afirmații incompatibile sau două versiuni care nu pot fi preluate împreună fără explicație.
- **NECLAR / NECONFIRMAT**: ipoteză a personajelor, informație parțială, schimbare insuficient explicată ori detaliu existent numai în materiale auxiliare.
- **PROPUNERE**: alegere de lucru a raportului sau variantă dintr-un plan; nu devine canon prin includerea aici.

Ierarhie propusă pentru această documentare: masterul narativ efectiv → finalul și teaserul său → jurnalul care descrie revizia → bible/planuri → metadate de catalog/site. Aceasta este o metodă de evaluare, nu o decizie de rescriere aprobată. Când masterul se contrazice singur, ierarhia nu rezolvă conflictul.

**Localizarea exactă:** `P` înseamnă paragraf DOCX nevid, numerotat de la 1 în ordinea documentului. Extragere în memorie cu Python `zipfile` și `lxml`, din `word/document.xml`, pentru `//w:body//w:p`, concatenând `.//w:t/text()` și eliminând paragrafele fără text. Sunt incluse titlurile și paragrafele din tabele; nu sunt unite paragrafele rupte de formatare. `L` înseamnă linie fizică, de la 1, într-un fișier text. `ZIP!/membru` identifică un fișier din arhivă, citit fără dezarhivare pe disc. Paginile Word nu sunt folosite, fiind dependente de randare.

### Registrul surselor

| ID | Cale exactă / adresă și întinderea relevantă a lecturii |
| --- | --- |
| A | [S:\dracula-book\public\app.js](<S:/dracula-book/public/app.js>). Catalogul, rafturile și descrierile de saga, în special L13–L115, L130–L144, L200–L214, L270–L284. |
| W | [Pagina publică](https://dracula-book.com/) și [fișierul public app.js?v=6](https://dracula-book.com/app.js?v=6). Secțiuni [AMORIS](https://dracula-book.com/#/amoris), [MYTHICA](https://dracula-book.com/#/mythica). HTML și datele de catalog citite; fără audit vizual complet al interfeței. |
| H | [D:\00. Downloads\Dracula Book\AMORIS SERIES\Hotelul din Rue des Âmes\Versiunea 2\Hotelul_din_Rue_des_Ames_FINAL_v2.docx](<D:/00. Downloads/Dracula Book/AMORIS SERIES/Hotelul din Rue des Âmes/Versiunea 2/Hotelul_din_Rue_des_Ames_FINAL_v2.docx>). 3.984 paragrafe nevide. **Citite integral în r01:** capitolul final 24, P3629–P3832; epilogul, P3833–P3978; închiderea și teaserul, P3979–P3984. În rest: lecturi țintite și căutări în întregul corp. În r02: reextragere în memorie, lectură P166/P860 și a contextului integral al nunții P3538–P3556; căutări de nume și lectură a paragrafelor returnate, nu lectură integrală a masterului. |
| HT | [D:\00. Downloads\Dracula Book\AMORIS SERIES\Hotelul din Rue des Âmes\Versiunea 2\Hotelul_din_Rue_des_Ames_FINAL_v2.txt](<D:/00. Downloads/Dracula Book/AMORIS SERIES/Hotelul din Rue des Âmes/Versiunea 2/Hotelul_din_Rue_des_Ames_FINAL_v2.txt>). 7.893 linii; finalul începe la L7188, epilogul la L7594, teaserul la L7889. Controlul integral la nivel de cuvinte arată echivalență cu H după eliminarea celor 18 cuvinte introductive din DOCX și normalizarea spațiilor. |
| HB | [D:\00. Downloads\Dracula Book\AMORIS SERIES\Hotelul din Rue des Âmes\Versiunea 2\Story_Bible_FINAL.docx](<D:/00. Downloads/Dracula Book/AMORIS SERIES/Hotelul din Rue des Âmes/Versiunea 2/Story_Bible_FINAL.docx>). **Citit integral, P1–P160**, împreună cu fișierul omonim `.txt`. Conținutul este un revision log v1.1, nu o bible completă actualizată după V2. |
| HP | [D:\00. Downloads\Dracula Book\AMORIS SERIES\Hotelul din Rue des Âmes\PLAN Hotelul din Rue des Âmes by Gabrielle St.docx](<D:/00. Downloads/Dracula Book/AMORIS SERIES/Hotelul din Rue des Âmes/PLAN Hotelul din Rue des Âmes by Gabrielle St.docx>). 116 paragrafe; lecturi țintite asupra cadrului, personajelor și finalului propus, în special P5, P86–P93, P113–P114. |
| HC | [D:\00. Downloads\Dracula Book\AMORIS SERIES\Hotelul din Rue des Âmes\Versiunea 2\ChangeLog_v2.txt](<D:/00. Downloads/Dracula Book/AMORIS SERIES/Hotelul din Rue des Âmes/Versiunea 2/ChangeLog_v2.txt>). Fragmente relevante: L16–L23, L466–L499, L548–L549, L571–L593, L684–L689. |
| AC | [D:\00. Downloads\Dracula Book\AMORIS SERIES\Dracula Amoris - concept Alex & Isabella.docx](<D:/00. Downloads/Dracula Book/AMORIS SERIES/Dracula Amoris - concept Alex & Isabella.docx>). **Citit integral, P1–P124**. Concept cu titluri și teme posibile. |
| B | [D:\00. Downloads\Dracula Book\AMORIS SERIES\BENEATH THE SKIN OF THE SEA\Versiunea 1\BENEATH_THE_SKIN_OF_THE_SEA_Complete_Novel.docx](<D:/00. Downloads/Dracula Book/AMORIS SERIES/BENEATH THE SKIN OF THE SEA/Versiunea 1/BENEATH_THE_SKIN_OF_THE_SEA_Complete_Novel.docx>). 2.691 paragrafe; începuturi și relații inspectate țintit; **epilog și închidere citite integral, P2637–P2691**. |
| SH | [D:\00. Downloads\Dracula Book\AMORIS SERIES\Shadows in the Port\Versiunea 1\Shadows in the Port V1.docx](<D:/00. Downloads/Dracula Book/AMORIS SERIES/Shadows in the Port/Versiunea 1/Shadows in the Port V1.docx>). 2.130 paragrafe; începuturi și nume inspectate țintit; **capitolul final 20 citit integral, P2076–P2130**. |
| N | [D:\00. Downloads\Dracula Book\MYTHICA SERIES\Saga Celor Zece Coroane\Cartea 1 The_Northern_Crown\Versiunea 3\Book-1-The-Northern-Crown-EDITED-FINAL.docx](<D:/00. Downloads/Dracula Book/MYTHICA SERIES/Saga Celor Zece Coroane/Cartea 1 The_Northern_Crown/Versiunea 3/Book-1-The-Northern-Crown-EDITED-FINAL.docx>). 3.792 paragrafe; deznodământ inspectat țintit; **epilog, nota autorului și teaser citite integral, P3739–P3792**. Citările canonice sunt la DOCX, nu la copia TXT cu alte marcaje. |
| NP | [D:\00. Downloads\Dracula Book\MYTHICA SERIES\Saga Celor Zece Coroane\Cartea 1 The_Northern_Crown\Versiunea 3\DRAMATIS_PERSONAE.md](<D:/00. Downloads/Dracula Book/MYTHICA SERIES/Saga Celor Zece Coroane/Cartea 1 The_Northern_Crown/Versiunea 3/DRAMATIS_PERSONAE.md>). Secțiunile personajelor principale și ale antagonistului, în special L8–L147; anexă verificată prin comparație, nu acceptată automat. |
| Z | [D:\00. Downloads\Dracula Book\MYTHICA SERIES\Saga Celor Zece Coroane\Cartea 1 The_Northern_Crown\saga-of-the-ten-crowns-complete-with-book1-world.zip](<D:/00. Downloads/Dracula Book/MYTHICA SERIES/Saga Celor Zece Coroane/Cartea 1 The_Northern_Crown/saga-of-the-ten-crowns-complete-with-book1-world.zip>) `!/book-outlines/complete-series-outline.md`, L56–L94; `!/series-bible/01-core-premise.md`, **citit integral, L1–L166**. Membrii au fost citiți în memorie. |
| Z0 | [D:\00. Downloads\Dracula Book\MYTHICA SERIES\Saga Celor Zece Coroane\Cartea 1 The_Northern_Crown\saga-of-the-ten-crowns-complete.zip](<D:/00. Downloads/Dracula Book/MYTHICA SERIES/Saga Celor Zece Coroane/Cartea 1 The_Northern_Crown/saga-of-the-ten-crowns-complete.zip>) `!/saga-of-the-ten-crowns/book-outlines/complete-series-outline.md`. Membrul este identic cu outline-ul din Z. |
| CAT | [D:\00. Downloads\Dracula Book\00. CATALOG SI REZUMAT.md](<D:/00. Downloads/Dracula Book/00. CATALOG SI REZUMAT.md>), în special L84–L87. Inventar secundar, nu arbitru al continuității. |
| OR | [D:\00. Downloads\Dracula Book\AMORIS SERIES\Hotelul din Rue des Âmes\Versiunea 2\Originality_Report.txt](<D:/00. Downloads/Dracula Book/AMORIS SERIES/Hotelul din Rue des Âmes/Versiunea 2/Originality_Report.txt>), verificare țintită a declarațiilor de metodă/certificare, L15–L20, L126–L138. |
| ST | [D:\00. Downloads\Dracula Book\02. ATELIER EDITORIAL - ROMANE 50000\00_CONDUCERE\STATUS.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/00_CONDUCERE/STATUS.md>). Citit integral; confirmă starea de configurare/audit, master EN minimum 50.000, ediții RO/DE și separarea producătorului de auditor. |

### Amprente de identificare SHA-256

Aceste amprente identifică versiunile citite, nu calitatea lor:

| Sursă | SHA-256 |
| --- | --- |
| A și W `/app.js?v=6` | `b3e62c3b0b84487a9b77da18f36b01b8b97e16cb7e92bba04976d83a0c0d4636` |
| H | `a9940d5776380cb40b105429f6976219440f3ea74fb8ebc1d1b4481e9da068c3` |
| HB | `9820461122fc30fcd82430a17b1d110fa9bdc3da4ad348b1883eba845c7615a9` |
| B | `4ebf04663fb5ee0ac9c0aa0ef26bd2d8c8222d95db93d16cbb372b7f8e7bf44c` |
| SH | `3f5fc3d81f584d23e7d029e90ebe2d40f7b25c5a24dfa78a81f0c2ff58e11b47` |
| N | `c77846fdc094d5800735ab8bdc7a1a3f62248a313f5cf2ae6e757e8baef22039` |
| Membrul outline din Z și Z0 | `9b65cbe17c0c6838005fb0ad6ce5c5bdeeb46ff60faf7bfd0685b47aad1c091a` |

## 3. Catalogul și site-ul la verificarea r01

Verificarea W `/app.js?v=6` a returnat HTTP 200 la **24.09.2026, 03:38:33 +03:00**. Fișierul public și A au câte **90.045 octeți**, amprente identice și text identic. Prin urmare, referințele de linie din A pentru datele de catalog sunt valabile și pentru versiunea publică verificată. Instrumentul inițial de navigare web nu a putut deschide pagina; accesul HTTP direct ulterior a reușit pentru HTML și JavaScript.

| Colecție / saga | Stare în datele verificate la momentul r01 | Referințe |
| --- | --- | --- |
| DRACULA NOIR / `noirvol` | Trei titluri marcate `avail:true`; descrise ca romane independente. | A, L15–L29, L105, L140. |
| DRACULA AURORA / `cycle` | Zece titluri; primele trei `avail:true`, următoarele șapte `avail:false`. Descrierea spune romane independente într-un ciclu. | A, L47–L96, L107, L137, L141. |
| DRACULA AMORIS / `alex` | Beneath și Shadows, ambele EN și `avail:true`; saga declară primele două titluri existente și zece planificate. | A, L31–L40, L106, L142. |
| DRACULA AMORIS / `isabella` | Hotelul, EN și `avail:true`; autor afișat Gabrielle St. Claire. | A, L41–L45, L106, L143. |
| DRACULA MYTHICA / `crowns` | The Northern Crown, EN și `avail:true`; atribuire publică Armin Vale, Ten Crowns 1. | A, L98–L102, L108, L144. |

Sunt 17 înregistrări de titlu, patru colecții și cinci grupări de saga în A. `avail` este o stare declarată de catalog; nu certifică existența integrală, auditarea ori concordanța tuturor edițiilor vândute.

**Corecție față de contextul auditului anterior:** Hotelul este marcat EN în versiunea verificată la momentul r01 în A/W, L41. Nu se raportează ca eroare a acestei versiuni o etichetă RO de pe o versiune anterioară a site-ului. Titlul de bază rămâne „Hotelul din Rue des Âmes”; varianta de afișare EN este „The Hotel on Rue des Âmes”, A, L42. H, P1–P4, păstrează titlul de bază și Gabrielle St. Claire.

Site-ul susține existența celor trei serii candidate, dar nu anunță The Magenta Letters ca titlu distinct în lista BOOKS. Pentru Isabella, descrierea de saga indică Paris, apoi Tokyo, Viena, Londra, Marrakech; AC, P60–P65, plasa însă Lisabona înaintea Tokyo. Acestea sunt prezentări/programări de serie, nu evenimente dovedite în continuarea încă nescrisă.

## 4. Isabella Morgan / Rue des Âmes — baza de canon

### 4.1. Masterul corect și statutul biblei

Fișierul din presupusa versiune Hotelul V1 este o copie byte-identică a Aurora 1. Au fost comparate:

- [D:\00. Downloads\Dracula Book\AMORIS SERIES\Hotelul din Rue des Âmes\Versiunea 1\AURORA_Book1_FINAL.docx](<D:/00. Downloads/Dracula Book/AMORIS SERIES/Hotelul din Rue des Âmes/Versiunea 1/AURORA_Book1_FINAL.docx>).
- [D:\00. Downloads\Dracula Book\DRACULA AURORA\Book 1\Versiunea 1\AURORA_Book1_FINAL.docx](<D:/00. Downloads/Dracula Book/DRACULA AURORA/Book 1/Versiunea 1/AURORA_Book1_FINAL.docx>).

Ambele au SHA-256 `cd158d30634e14505adfe6da00d04f2117851cade3be02615b1a2477bff3ecf2`; P1 este „AURORABook 1”, P2 „A Young Adult Novel”. Nu pot documenta antecedentele Isabellei. Nici afirmația HC, L16–L17, despre un draft Hotelul anterior nu face ca această copie Aurora să fie acel draft; antecedentul autentic nu a fost identificat în locația V1.

H este un text narativ în engleză. Are 95.079 de elemente separate prin spații în extracția integrală, dintre care 18 în introducerea proprie DOCX; restul coincide cu HT și cu totalul de 95.061 declarat în H, P5. Aceasta este o verificare de extracție, **nu** o măsurare finală a prozei eligibile: numără și titluri/teaser. Nu este folosită pentru a certifica pragul de producție al unui roman viitor.

HB, P1–P7, se prezintă drept FINAL, dar corpul este „STORY BIBLE v1.1 - REVISION LOG”, datat 11.10.2025. HC, L549, îl identifică explicit ca material provenit din dezvoltarea v1. Nu conține o bible completă care să închidă toate identitățile, datele și obiectele după V2. În inventarul local consultat nu a fost identificată o altă bible Hotelul completă și reconciliată.

### 4.2. Personaje, nume și relații

| Element | Ce este susținut exact | Statut și referință |
| --- | --- | --- |
| **Isabella Morgan** | Vine din Londra pentru activitate PR; relația cu Marcus se încheiase cu șase luni înaintea sosirii. La final este soția lui Alexandre și își formulează o vocație de recuperare responsabilă a poveștilor/scrisorilor. | CANON CERT ÎN MASTER: H, P40, P58, P3538–P3556, explicit P3553, P3839–P3842, P3959–P3966. Certitudinea căsătoriei nu fixează numele de familie al lui Alexandre: vezi H-C9 / SEL-001-A-CANON-F01. Vârsta exactă nu este fixată aici: AC, P48, spune 30, iar H, P58, evocă deja începutul anilor treizeci. |
| **Alexandre — Boucher / Dubois, nume de familie nereconciliat** | Istoric: se prezintă „Alexandre Boucher” și cu specializare în Franța postbelică; în formula de căsătorie este numit „Alexandre Dubois”. Partener de investigație, apoi soțul Isabellei; în epilog predă parțial la Sorbona și scrie istorie pentru public. | **CONTRADICȚIE de nume:** Boucher, H P166/P860; Dubois, H P3548/P3550. **Căsătorie documentată separat:** H P3553, în contextul P3538–P3556. Nicio formă nu este aleasă drept canonică; H-C9 / SEL-001-A-CANON-F01 rămâne de reconciliat în G01. Rol/profesie: H P166–P172, P3841; specializarea/etapa proiectului au variații de explicat. Nu este Alex Damian. |
| **Catherine Dubois** | Persoana căutată prin scrisoarea din 1974; iubirea din trecut a lui Antoine, regăsită în prezent. Are un frate, Guillaume. După moartea lui Antoine, locuiește într-un apartament mai mic la Rouen și continuă să aibă legături cu Isabella și Alexandre. | H, P170, P216, P666, P3750–P3789, P3809–P3814. Nu este prezentată aici drept soția lui Antoine: conviețuirea este documentată, căsătoria dintre ei nu este stabilită de pasajele citite. |
| **Antoine Mercier** | Locotenentul identificat în registru, autorul scrisorii pentru Catherine. Tatăl lui Marguerite. Moare după un al doilea infarct și are înmormântare explicită. | H, P149–P151, P3648–P3651, P3712–P3736. Numele „Antoine Boucher” și rolul de bunic al lui Alexandre apar în HP, P93, nu trebuie importate în H. |
| **Marguerite** | Fiica lui Antoine; coordonează îngrijirea și familia, găzduiește ulterior pe Catherine. | H, P3648–P3651, P3740, P3770. Nu îi este atribuit aici un nume de familie nespecificat în pasajele citate. |
| **Guillaume Dubois** | Fratele lui Catherine; protejează accesul la ea și cere condiții pentru contact. | H, P658–P696, în special P666. Protecția și refuzul lui fac parte din antecedentele etice ale investigației. |
| **Madame Besson** | Proprietara/administratoarea hotelului, sursă pentru registrele păstrate de bunica sa; ajută cu identificarea lui Margaux. | H, P17, P156, P3931–P3938. Nu este stabilit aici un prenume. |
| **Odette Renard** | Martoră a vieții lui Catherine în anii 1970; fusese proprietară de cafenea. Își amintește o prietenă roșcată, Margaux, care lucra la o galerie. | H, P260, P365–P401. Memoria ei nu oferă numele galeriei sau numele de familie al lui Margaux. |
| **Marcel** | Intermediar de arhivă; ajută la documentare, dar afirmă limite asupra furnizării adreselor. Menționează un partener. | H, P149–P160. HB, P80, îi atribuie explicit o identitate gay; aceasta este informație din materialul auxiliar, nu o concluzie dedusă doar din cuvântul „partner”. |
| **Jean-Paul / Marie-Claire** | Jean-Paul moare; relația lui cu Alexandre este contradictorie: bunic și mecanic la început, tată și om al universității ulterior. Marie-Claire este numită mama lui Alexandre, moartă când el avea șaisprezece ani. | H, P256 versus P1651–P1656, P1695, P1720, P1778–P1782. Nu se fixează arborele familial înainte de reconciliere. |
| **Margaux / Margaux Beaumont** | Odette descrie o prietenă a lui Catherine; registrul epilogului identifică o Margaux Beaumont roșcată în camera 14, în 1968. Isabella le asociază. | H, P396–P401, P3932–P3939. Registrul este o probă în ficțiune; identificarea aceleiași persoane în ambele perioade rămâne o legătură făcută de personaje, nu o verificare biografică încheiată. |

**Separări de nume obligatorii în documentare:** Margaux din trecut nu trebuie confundată cu Marguerite, fiica lui Antoine; HB, P77–P78, introduce și o Margaux contemporană, colegă a Isabellei, queer și franco-algeriană. Aceste caracteristici nu se transferă lui Margaux Beaumont. „Margot” din HB, P67, nu dovedește identitatea cu vreuna dintre ele. Numele Beaumont din firma „Beaumont Luxury Hotels”, HB, P108, nu dovedește vreo rudenie cu Margaux Beaumont. Raportul nu inventează această legătură.

Pentru **Alexandre Boucher / Alexandre Dubois**, contradicția privește numele partenerului Isabellei din același master, nu două identități reconciliate. Apariția „Dubois” la ceremonie nu dovedește rudenie cu Catherine ori Guillaume Dubois, schimbare legală de nume, pseudonim sau existența unui al doilea Alexandre. Conflictul este distinct de Antoine Boucher/Mercier din H-C8 și de tată/bunic din H-C5; nu se rezolvă prin frecvența uneia dintre forme sau prin preferința pentru ultima mențiune.

### 4.2.1. Proba exactă a numelui nereconciliat — SEL-001-A-CANON-F01

Sursa primară este **H**, [masterul DOCX original](<D:/00. Downloads/Dracula Book/AMORIS SERIES/Hotelul din Rue des Âmes/Versiunea 2/Hotelul_din_Rue_des_Ames_FINAL_v2.docx>); copia de control este [H.docx arhivat](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/08_ARHIVA/INTRARI_CANON/20260924-r01/H.docx>). Originalul și copia au fost reverificate în r02: fiecare are 269.789 octeți și SHA-256 `a9940d5776380cb40b105429f6976219440f3ea74fb8ebc1d1b4481e9da068c3`. Numerotarea de 3.984 paragrafe nevide a fost reprodusă prin metoda P din §2. Excerptele de mai jos sunt literale, nu traduceri sau parafraze; primele două sunt fragmente din paragrafe mai lungi.

| Paragraf H | Excerpt literal | Ce probează și ce nu rezolvă |
| --- | --- | --- |
| P166 | “My specialty is post-war France, particularly social history—how ordinary people lived. Alexandre Boucher.” | Autoprezentare cu Boucher; nu reconciliază formula ceremoniei. |
| P860 | “My name is Alexandre Boucher. I'm a historian in Paris.” | O a doua autoprezentare cu Boucher. |
| P3548 | “Do you, Isabella Morgan, take Alexandre Dubois as your spouse?” | Formula oficiantului folosește Dubois. |
| P3550 | “And do you, Alexandre Dubois, take Isabella Morgan as your spouse?” | A doua formulă folosește tot Dubois. |
| P3553 | “I now pronounce you married. You may kiss.” | Căsătoria este pronunțată, independent de reconcilierea numelui; context citit integral P3538–P3556. |

Căutarea literală a **numelor complete** în întregul corp H a returnat „Alexandre Boucher” în exact două paragrafe (P166, P860) și „Alexandre Dubois” în exact două (P3548, P3550). Aceasta nu înseamnă că șirurile „Boucher” sau „Dubois” apar numai de două ori: există și adresări „Monsieur Boucher”, precum și numele altor personaje. Contextul nunții P3538–P3556 folosește de două ori Dubois și deloc Boucher. Căutarea în tot corpul și lectura paragrafelor returnate nu sunt lectură editorială integrală a celor aproximativ 95k.

Proveniența corecției: [A-CANON-r01.md, §proba-identitate](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/05_AUDIT/SEL-001/A-CANON-r01.md:33>) și [A-CANON-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/05_AUDIT/SEL-001/A-CANON-r01.json>), finding `SEL-001-A-CANON-F01`, major, open, verdict r01 RETURN. Hashurile auditului, produsului r01, planului și noului fișier sunt consemnate în rezultatul de implementare r02. **Corecția selecției înregistrează contradicția; nu corectează masterul și nu închide findingul de audit.**

### 4.3. Loc, timp și final efectiv

| Subiect | Fapt documentat | Limită |
| --- | --- | --- |
| Paris / hotel | H, P8–P25: Rue des Âmes, Hôtel des Âmes, clădire cu placă 1902 și detalii Art Nouveau; camera 12, etajul trei. | Sunt elemente ale lumii ficționale. Nu a fost verificată existența reală a străzii/hotelului ori exactitatea istorică a arhitecturii. |
| Punct de pornire temporal | H, P33–P42: scrisoare datată 15 octombrie 1974, găsită „fifty-one years” mai târziu, în aceeași zi de octombrie. | **Inferență aritmetică: 15.10.2025.** Alte pasaje nu respectă consecvent această cronologie; nu se fixează un an al volumului 2. |
| Cuplul Isabella–Alexandre | Căsătorie efectivă în capitolul 23, apoi viață comună. În epilog au cumpărat un apartament în Marais și declară intenția de a rămâne la Paris. | H, P3538–P3556, explicit P3553, P3593, P3839–P3841, P3873. Căsătoria este certă; numele de familie al lui Alexandre este nereconciliat Boucher/Dubois (H-C9 / SEL-001-A-CANON-F01), iar calendarul aniversării este contradictoriu. |
| Sarcină | H, P3860: trei teste pozitive; intenția de a aștepta încheierea primului trimestru înainte de anunțul larg. | Cert este ce raportează textul despre teste și speranța lor. Nu sunt stabilite nașterea, sexul, numele copilului sau evoluția sarcinii. |
| Carieră | H, P3840: practică mică de storytelling etic pentru ONG-uri și instituții culturale; carte cu Catherine și refuzul unor oferte corporative. | Starea finală nu echivalează cu reluarea automată a rolului de consultant itinerant singur din AC/site. Premiile și succesul cărții sunt evenimente din ficțiune, nu validări externe ale manuscrisului. |
| Antoine și Catherine | Reuniunea este consumată; au aproximativ un an împreună, apoi Antoine moare și este îngropat. Catherine rămâne în viață, îndoliată și activă. | H, P3669–P3675, P3712–P3789, P3809–P3818. Antoine nu poate reapărea viu după acest final fără o schimbare de canon explicită; documentarea nu propune una. |
| Obiectul de trecere | Un nou plic, găsit în spațiul sertarului din camera 12, adresat camerei 14, cu inițiala „M.” pe verso. | H, P3882–P3892. Este un alt plic decât scrisoarea inițială pentru Catherine. Semnătura completă și conținutul nu sunt cunoscute. |

### 4.4. Promisiunea The Magenta Letters și necunoscutele ei

| Probă exactă | Ce permite să afirmăm | Ce nu permite să inventăm |
| --- | --- | --- |
| H, P396–P401: amintirea lui Odette despre Margaux | Prietenă apropiată a lui Catherine, roșcată, lucra la o galerie; localizarea galeriei este nesigură, Marais ori zona Saint-Germain. | Numele galeriei, angajatorul, vârsta exactă, biografia completă sau relația romantică a lui Margaux. |
| H, P3886–P3892: „Room 14, Hotel Rue des Âmes.” și „M.” | Destinația înscrisă este o cameră; nu apar nume sau an pe plic. | Că scrisoarea este sigur scrisă de Margaux ori sigur destinată ei. |
| H, P3932–P3934 | Registrul spune Margaux Beaumont, trei luni în camera 14 în 1968, plată săptămânală cash; note la 12 august și 3 septembrie despre așteptare, poștă și servicii de redirecționare. | Motivul real al așteptării, identitatea persoanei așteptate, cine a blocat sau a uitat mesajul. |
| H, P3938 | Pleacă în octombrie 1968, fără adresă de redirecționare; bunica lui Besson o descria ca îndurerată și resemnată. | Unde a mers, dacă s-a căsătorit, dacă are copii ori dacă este încă în viață. |
| H, P3939–P3941 | Isabella asociază Margaux Beaumont cu prietena lui Catherine și discută mai multe ipoteze despre plic. | Identificare finală a autorului/destinatarului sau o cauză definitivă a separării. |
| H, P3944–P3950 | Cei doi promit să o caute pe Margaux sau familia ei, să ceară acordul pentru predare/deschidere și să respecte opțiunea de a păstra plicul sigilat. O eventuală carte depinde de poveste și de acord. | O deschidere deja efectuată, un consimțământ deja obținut sau o investigație deja rezolvată. |
| H, P3954–P3955 | Plicul pleacă în geanta Isabellei; textul evocă un an pentru cercetare și decizie. | Un termen-limită extern demonstrat, o expirare a drepturilor sau data sigură la care începe volumul 2. Motivul acestui interval nu este explicat. |
| H, P3981–P3984; HC, L684–L685 | Titlul anunțat este The Magenta Letters, cu precizarea Margaux's Story; jurnalul îl leagă de 1968 și camera 14. | Existența unei ediții publicate, pluralitatea deja demonstrată a scrisorilor, culoarea cernelii/hârtiei sau semnificația cuvântului „Magenta”. |

„Biroul care păstrează și returnează secrete” este un motiv literar, H, P3971–P3977. Nu demonstrează un mecanism supranatural. O continuare cu magie explicită ar fi o propunere nouă, nu canon stabilit.

### 4.5. Contradicții și decizii de canon rămase deschise

| ID | Surse incompatibile / problemă | Consecință pentru continuare |
| --- | --- | --- |
| H-C1 — anii | H, P33–P42, implică 2025 la găsirea scrisorii; P3816 spune reuniune în **2024**; P3969 spune 57 de ani după 1968, adică tot 2025, deși P3836–P3839 plasează epilogul la doi ani după descoperire. | Nu se introduce în vol. 2 un calendar absolut prezentat drept cert. Trebuie aleasă explicit o cronologie și corelate consecințele, fără modificări în acest mandat. |
| H-C2 — luni și aniversări | Începutul este octombrie, H, P8, P41; P3631 spune final de noiembrie, aproape exact un an după găsire; P3786 numește februarie aniversarea găsirii; P3836 și P3839 descriu decembrie ca aniversare la doi ani de la prima vizită și un an de la căsătorie, dar nunta este 21 iunie, P3538. | Faptul căsătoriei rămâne; data aniversării și relațiile dintre salturile temporale nu sunt rezolvate. |
| H-C3 — ceasul lui Antoine | H, P3729–P3733, îl pune pe trup pentru înmormântare; P3763–P3764 și P3798 confirmă restituirea pentru îngropare. P3871 spune că a fost dăruit la înmormântare și este în apartamentul cuplului; P3957 repetă apartamentul. | Nu poate fi simultan obiect îngropat și moștenire păstrată acasă. Nu se alege tacit ultima mențiune și nu se inventează recuperarea lui. |
| H-C4 — găsirea primei scrisori | H, P29–P32: plic lângă vază, sub un ghid, pe birou. P232 și P3879 rememorează că ar fi căzut în spatele biroului/în golul sertarului și ar fi fost găsit acolo. | Canonul exact al primei descoperiri este contradictoriu. Noul plic din epilog este găsit explicit în sertar, dar nu trebuie folosit pentru a rescrie retrospectiv prima scenă. |
| H-C5 — familia lui Alexandre | H, P256: Jean-Paul, bunic și mecanic. P1651–P1656: tată, „Mon fils” / „Papa”; P1778–P1782: familie cu Marie-Claire și carieră de profesor. HB, P66–P67: ambii părinți mor când Alexandre are 12 ani; H, P1720/P1829: mama moare când el are 16. | Arborele familial și biografia academică nu sunt fixate. Nu se transformă Antoine Mercier în bunicul lui Alexandre prin importul HP, P93. |
| H-C6 — vârste | H, P497: Antoine are 80; P690: 78; P3635: 82. Catherine se declară 73 la P2835 și 74 după moarte la P3783. HC, L472, declară în schimb ambii aproximativ 76. | Nu se generează date de naștere din aceste cifre. Vârstele concrete sunt de reconciliat cu intervalul ales. |
| H-C7 — continuarea din documentele vechi | AC, P60–P62, și HP, P113, propun O cafea la capătul lumii / Lisabona. HB, P94–P103, introduce un jurnal al călătoriei lui Catherine la Lisabona din 1976. H, P3932–P3984, și HC, L684–L685, promit Margaux / 1968 / The Magenta Letters. | Lisabona este un plan anterior; nu un fapt de continuare care prevalează asupra teaserului V2. Nu este exclusă o folosire viitoare prin decizie nouă, dar ea nu este dedusă aici. |
| H-C8 — room 304 / 12 și Antoine Boucher / Mercier | HP, P87: camera 304; P93: Antoine Boucher, bunic al lui Alexandre. H, P19: camera 12; P150: Antoine Mercier. | Metadatele planului nu se transferă automat în nomenclatorul V2. |
| H-C9 — Alexandre Boucher / Dubois; finding SEL-001-A-CANON-F01 | Același master H: „Alexandre Boucher” în autoprezentările P166 și P860, „Alexandre Dubois” în formulele oficiantului P3548 și P3550. H P3553 pronunță căsătoria; context P3538–P3556. | Numele de familie rămâne **nereconciliat**. Căsătoria rămâne probată, dar nu autorizează alegerea unui nume. G01 trebuie să inventarieze toate aparițiile și să obțină o decizie editorială explicită, cu dovada/baza deciziei și consecințele asupra nomenclatorului. Nu se inventează rudenii, schimbare de nume sau un alt Alexandre. Se păstrează blocajul G01 înainte de scriere. |
| H-N1 — profesii și stadii de lucru | Catherine: profesor pensionat de arhitectură la H, P2835/P3809; în epilog predă la lycée, P3845/P3957. Alexandre: specializare postbelică, P166, apoi proiect medieval încheiat la P3841, dar aproape încheiat la P3872. | Sunt variații sau schimbări insuficient explicate; unele ar putea fi compatibile dacă ar fi motivate. Raportul nu le declară imposibilități biografice și nu inventează explicații. |
| H-N2 — structura capitolelor | După H, P1338, CHAPTER 10, urmează P1483, CHAPTER 12. HC, L574, spune explicit că 11 a fost eliminat; L592 spune că 25–27 au fost eliminate. | Sunt 23 de titluri numerotate de capitol plus epilog în H. Nu este corect să afirmăm automat că lipsește un capitol de proză; există o eliminare declarată și o numerotare păstrată. Referințele HB la capitolele 25/27 nu corespund structurii H. |

Nu toate conflictele au aceeași greutate. Noul plic, numele Margaux Beaumont din registru și titlul teaserului sunt localizabile independent de rezolvarea ceasului, a vârstei lui Antoine sau a numelui de familie al lui Alexandre. Acesta este motivul pentru care direcția Margaux poate rămâne recomandată ca DRAFT. F01 nu infirmă promisiunea The Magenta Letters sau faptul căsătoriei, dar interzice preluarea lui Boucher ori Dubois ca nume reconciliat și nu permite închiderea G01.

## 5. Alternativa Alex Damian

### Bază sigură și promisiuni

Catalogul public le grupează pe B și SH în saga Alex și afirmă că primele două titluri există: A, L31–L40, L142. AC, P4–P8, îl propune pe Alex Damian, 34 de ani, instructor de scufundări/fotograf și fost ofițer în marina română. Această vârstă și proveniență sunt detalii de concept; nu se certifică aici fiecare element prin manuscrise.

| Componentă | Dovezi și statut |
| --- | --- |
| Protagoniști | **Alex Damian și Dr. Elena Iordanou** apar cu aceste nume în ambele texte. B, P153–P155, o introduce de la University of Athens; SH, P92–P93, îi prezintă strângându-și mâinile ca la începutul colaborării. |
| Relația în B | Elena este inițial logodită cu Andreas, P350–P351; decide să rupă logodna, P758. Epilogul îi arată pe Alex și Elena ca parteneri și părinți, P2638–P2648. Nu se deduce o căsătorie juridică numai din această familie. |
| Finalul B | Primăvară, Samos, după saltul „THREE YEARS LATER”; fiica lor Sophia are trei ani, P2637–P2639. Locuiesc într-o casă; Poseidon's Promise rămâne barca lor, dar nu mai este locuința, P2668. |
| Firul viitor B | Dimitris propune Delos pentru anul următor. Elena și Alex doar discută evaluarea proiectului și compatibilitatea cu îngrijirea Sophiei, P2659–P2663. Este o oportunitate, nu un contract acceptat și nu un titlu de carte. |
| Finalul SH | Pe Kyma, echipa ridică și predă spre conservare torsul „Swan”; o ambarcațiune intruzivă este descurajată cu ajutorul comunității. Petros, Iro, Maya, Niko și Andreas sunt prezenți. SH, P2077–P2114. Niko contribuie la protejarea operației; aceasta nu dovedește automat absolvirea oricăror fapte anterioare. |
| Cuplu și fir viitor SH | Alex și Elena rămân apropiați; întrebarea despre ce urmează și răspunsul „Swan had a flock” deschid posibilitatea altor descoperiri. SH, P2119–P2129. Nu identifică un nou antagonist, un nou obiect cert sau un titlu. |
| Loc și timp SH | Începutul numește Egeea, SH, P2, iar finalul un port insular. Căutarea după Samos/Kalymnos/Santorini/Crete/Rhodes nu a găsit aceste nume în SH. | 

### Contradicții și limite ale opțiunii

**Problema principală este reluarea începutului relației:** B, P149–P155, și SH, P88–P99, introduc întâlnirea Alex–Elena; SH, P215/P240/P333, insistă asupra primei scufundări împreună și a încrederii abia formate. Aceasta nu este compatibilă cu o continuare simplă plasată după familia din epilogul B. Ar putea exista o structură retrospectivă sau o versiune alternativă, dar pasajele citite nu demonstrează soluția. Nu se certifică aici faptul că SH ar fi integral o rescriere a B: ar cere lectură comparată integrală, nu doar asemănarea începutului.

**Numele și funcția lui Andreas variază în SH:** P125 spune Andreas Konstantinidis, directorul unei fundații pentru patrimoniu maritim; P381 spune Andreas Voulgaris, logodnicul Elenei și funcționar în ascensiune la minister. Nu este explicată în pasajele citate existența a doi Andreas diferiți. Este conflict de identitate ce trebuie rezolvat, nu o invitație la inventarea unui al doilea personaj.

**Sophia nu se unifică după prenume:** în B, P2639–P2648, este fiica de trei ani. SH, P1675–P1676/P1727, prezintă o femeie care ajută la catalogare și provoacă gelozia Elenei. În B există și Dr. Sophia Konstantinou, arheolog de circa șaizeci de ani, P2235/P2239. Sunt referenți diferiți sau insuficient identificați, nu dovada unei singure biografii.

AC propunea la poziția 2 „Ultimul apus din Santorini”, P17–P19, iar la 3 „Respirația adâncurilor”, P20–P22. Catalogul actual are SH ca al doilea titlu. Aceste titluri din concept sunt **propuneri anterioare**, nu o numerotare obligatorie și nici un titlu cert pentru următorul roman.

**PROPUNERE DE DIRECȚIE, neaprobată:** dacă se alege ulterior Alex, continuarea poate păstra familia din B și explora o nouă aventură compatibilă cu ea, după rezolvarea statutului SH. Delos este o pistă textuală disponibilă, nu alegerea de intrigă a prezentului raport. Nu combinăm automat Delos cu „Swan” și nu anulăm relația cu Elena pentru a recupera schema veche a unei alte iubiri la fiecare volum.

## 6. Alternativa Ten Crowns

### Bază sigură și promisiuni

| Element | Canonul masterului N |
| --- | --- |
| Dorian Stormcrown | Supraviețuiește revenirii la viață, are coroana de Nord permanent afectată și emoțiile estompate. Recunoaște schimbarea în fața Serafinei; conduce în continuare. P3746–P3747, P3767–P3783. |
| Serafina | Purtătoare a Waters Crown, participă la salvare și îi oferă sprijin lui Dorian; răspunde schimbării prin adaptare. P3579–P3580, P3628/P3636 și P3770–P3776. Epilogul nu stabilește o căsătorie sau o relație romantică încheiată. |
| Rafael / Lyra / Torven | Rafael și Lyra participă la efortul de salvare; în consiliul final apar alături de Dorian, Serafina și regele Torven din Stormhaven. P3625–P3636, P3744. Numele extinse din NP nu sunt automat confirmate prin N. |
| Malachar | Shadow Crown este distrusă; Malachar se dizolvă și moare. P3540–P3545, P3561, P3677. Nu este doar o retragere temporară a antagonistului. |
| Loc și timp final | Sala mare din Frosthelm, „One week later”, P3739–P3743. Este un reper relativ după deznodământ; raportul nu fixează un calendar complet al lumii. |
| Ordine politică | Cele cinci regate votează unanim League of Crowns. P3755–P3763. Principiile includ suveranitate locală, apărare comună, comerț, vot în consiliu și admiterea unanimă a membrilor noi. Este deja o instituție creată, nu un proiect încă neînceput. |
| Promisiune vol. 2 | P3786: costurile revenirii lui Dorian la viață nu se rezolvă ușor; P3787: poate conduce și poate rezista alianța; P3788: noi amenințări din Eastern Desert și purtători de coroane cu alte concepții despre putere; P3791: **BOOK 2: THE EASTERN SANDS**. |

### Conflictul cu planul și cu anexele

Z `!/book-outlines/complete-series-outline.md`, L56, numește volumul 2 **The Crown of Waters**. L63–L84 menține atacurile flotei lui Malachar, unirea cu merfolk și consolidarea unei alianțe de trei regate. N îl omoară deja pe Malachar și încheie cu cinci regate unite. Nu este doar o diferență de titlu: planul pornește din altă stare militară și politică.

Z `!/series-bible/01-core-premise.md`, L49–L50 și L98–L110, distribuie formarea alianței în volumele 1–3 și confruntarea finală în 9–10. Finalul N consumă deja războiul cu Malachar și fondarea formală a League of Crowns. Importarea mecanică a arhitecturii celor zece volume ar repeta evenimente îndeplinite sau ar cere o revizuire explicită. Outline-ul conflictual este identic în Z0 și Z; existența a două arhive nu constituie două soluții concurente reconciliate.

Nici NP nu poate funcționa ca autoritate infailibilă. Exemple precise:

- NP, L110, spune că Malachar nu are coroană; N, P3540–P3544, îi distruge **Shadow Crown**, care îi susține forma. Contradicție directă.
- NP, L21/L141–L147, numește un frate decedat Bjorn Stormcrown. N, P56–P57, îl introduce pe **Bjorn Ironfist**, vechi luptător care îl antrenase pe Dorian de la opt ani; P3690 îl arată vorbind după bătălie. Nu se poate echivala automat luptătorul cu fratele din anexă. Căutarea numelui complet Bjorn Stormcrown în N nu l-a găsit.
- NP folosește Serafina Wavecrest, Rafael Sunborn, Lyra Greenmantle și Torven Stormwright, L17–L20/L29/L48/L67/L86. Căutarea acestor nume complete în N nu a produs rezultate. Prenumele și rolurile sunt susținute în epilog; numele extinse rămân metadate auxiliare neconfirmate prin această verificare.
- A, L99, atribuie titlul lui Armin Vale, în timp ce N, P3, are „Author: Cesiro Horeca” și o mențiune de echipă editorială. Este o neconcordanță de atribuire, nu un fapt despre personaje.

**PROPUNERE DE DIRECȚIE, neaprobată:** dacă se alege Ten Crowns, punctul documentar de plecare este The Eastern Sands și starea finală a League of Crowns, cu costurile revenirii lui Dorian păstrate. Numele liderilor din deșert, regatele lor, conflictele concrete și orice mecanism nou de magie sunt necunoscute sau propuneri viitoare. Raportul nu le completează.

## 7. Recomandarea DRAFT și condițiile de utilizare

Pentru selecția preliminară G00, recomand **The Magenta Letters ca al doilea volum al ramurii Isabella Morgan / Rue des Âmes**. Aceasta este recomandarea SEL-001 pentru o alegere ulterioară, nu o trecere în G01 sau o aprobare de scriere. Denumirea de ramură servește organizării: H spune „Book 1 of the Dracula Amoris Series”, dar A separă deja `alex` de `isabella`. Raportul nu renumerotează întreaga colecție AMORIS și nu rezervă un slot public nou.

Nucleul care poate fi dus la o decizie de canon este următorul: Isabella și Alexandre rămân cuplul căsătorit de la final (H P3553, context P3538–P3556), dar numele de familie al lui Alexandre rămâne nereconciliat — Boucher la H P166/P860, Dubois la H P3548/P3550, H-C9 / SEL-001-A-CANON-F01; Parisul și hotelul reprezintă punctul de pornire; Antoine este mort, Catherine supraviețuiește; există o sarcină timpurie sugerată de trei teste; noul plic este sigilat, adresat camerei 14, cu inițiala M.; registrul conduce la Margaux Beaumont în 1968; căutarea și eventuala povestire sunt condiționate în text de grija pentru persoanele implicate și de acordul lor.

Rămân de decis, fără a pretinde că au fost decise aici: numele de familie al lui Alexandre (Boucher/Dubois, H-C9 / SEL-001-A-CANON-F01), cronologia absolută și aniversările, traseul ceasului, arborele familial al lui Alexandre, vârstele și biografiile fluctuante, relația dintre Margaux din mărturie și cea din registru. Identitatea autorului și destinatarului scrisorii, conținutul ei, persoana iubită de Margaux și soarta acesteia sunt spații de creație viitoare, nu goluri pe care documentaristul are voie să le umple cu „canon”.

Mandatul de producție dat de utilizator și reflectat în ST este **minimum 50.000 de cuvinte de proză originală în masterul EN, apoi RO și DE**, cu auditori separați și prag **strict mai mare de 9,50/10**. Vechea țintă 95–110k din HC nu înlocuiește această cerință. Nu sunt aprobate prin acest raport lungimea exactă, structura, scenele, deznodământul nou sau calendarul producției.

Documentele vechi conțin comparații cu autori, promisiuni de succes, scoruri și declarații de originalitate. Acestea nu sunt probe independente pentru noul roman și nu sunt instrucțiuni de a reproduce stilul ori intriga unor cărți existente. OR menționează verificări și o certificare, dar în acest mandat nu a fost demonstrată funcționarea instrumentelor declarate, acoperirea bazei de comparație sau independența evaluatorului. **Nu se certifică originalitatea sau calitatea vreunui manuscris și nu se acordă niciun scor.**

**Clarificarea utilizatorului privind banca de mecanisme:** sursele de inspirație pot proveni din orice mediu cu succes, nu numai din romane; accentul include modul de prezentare a mecanismului. Aceasta este o cerință pentru documentarea ulterioară, nu o constatare despre canon. SEL-001 nu construiește banca, nu evaluează succesul unor exemple noi și nu formulează un plan de plot. Când va fi realizată banca, trebuie diferențiate mecanismul abstract, prezentarea lui și expresia concretă a sursei; exemplele nu devin biografii, evenimente sau scene canonice ale seriilor Dracula Book.

## 8. Acoperirea G00 și ce trebuie preluat în G01

**Lectura integrală a unui fișier nu este echivalentă cu extragerea lui integrală pentru căutare.** Corpul H a fost extras în memorie pentru indexare, căutări și comparația DOCX/TXT. Lectura editorială efectivă a acoperit integral numai capitolul final 24, epilogul și teaserul, plus fragmentele țintite citate în raport. Nu se declară citite integral capitolele 1–23 și nu se pretinde certificarea integrală a celor aproximativ 95k.

În r02_staging, controlul editorial a recitit întregul **raport** r01 și a verificat regresia versiunii corectate, nu întregul roman. Pentru proba nou introdusă au fost recitite H P166/P860, contextul integral P3538–P3556 și paragrafele returnate de căutările Boucher/Dubois. Aceste verificări suplimentare nu extind declarația de lectură integrală la capitolele 1–23. Celelalte surse și lecturi r01 rămân explicit istorice, nu sunt prezentate drept reverificări integrale r02.

| Acoperire realizată în SEL-001 / G00 | Ce rămâne pentru G01 înainte de scriere |
| --- | --- |
| H, lectură r01: finalul 24 P3629–P3832, epilogul P3833–P3978 și închiderea/teaserul P3979–P3984 citite integral; începutul, relațiile și alte afirmații verificate prin fragmente și căutări. R02 adaugă recontrolul de nume P166/P860/P3548/P3550 și lectura contextului P3538–P3556. | Lectura editorială integrală a masterului ales, inclusiv toate capitolele anterioare finalului. Verificarea fiecărui fapt propus pentru canon în întregul text și consemnarea acoperirii reale. Extragerea/căutarea de acum nu înlocuiește această lectură. |
| HB citit integral, P1–P160; AC citit integral, P1–P124. HP și HC au fost folosite prin lecturi țintite. A fost identificată incompatibilitatea dintre materialul de dezvoltare v1 și finalul V2. | Reconcilierea tuturor materialelor relevante pentru seria selectată și stabilirea explicită a autorității fiecăruia. O bible completă G01 trebuie să reflecte masterul ales și deciziile acceptate, fără importul automat al variantelor vechi. |
| Identități și relații documentate local; separările Margaux/Marguerite/Margot și conflictul Jean-Paul sunt păstrate. Este adăugat explicit **H-C9 / SEL-001-A-CANON-F01**: Alexandre Boucher la H P166/P860 versus Alexandre Dubois la H P3548/P3550; căsătoria este probată separat la P3553. | Nomenclator integral cu toate aparițiile, variantele numelor, relațiile, vârstele și biografiile. Pentru Alexandre se păstrează ambele forme, fără alegere în SEL-001; G01 trebuie să documenteze reconcilierea pe baza probelor și/sau a unei decizii editoriale explicite, fără a prezenta o decizie nouă ca fapt deja cert în sursă. Fără această reconciliere, numele rămâne blocaj de închidere G01 înainte de scriere. Nu se deduce o rudenie cu Catherine/Guillaume Dubois. |
| Sunt probate conflictele de calendar, aniversări, ceas și găsire a primei scrisori, H-C1–H-C6. | Cronologie integrală și traseu al obiectelor, cu decizii editoriale explicite și efectele lor asupra continuității. SEL-001 nu alege în locul responsabilului editorial versiunea câștigătoare și nu repară sursele. |
| Titlul The Magenta Letters și promisiunea plicului/Margaux sunt confirmate în final; identitatea autorului/destinatarului și soarta lui Margaux rămân deschise. | Registru al promisiunilor de continuare: ce este fapt deja produs, ipoteză de personaj, angajament viitor ori spațiu de creație. Confirmarea că noua direcție păstrează starea cuplului fără fixarea tacită a numelui nereconciliat (H-C9), doliul și incertitudinea sarcinii, fără un plan de scene în această etapă. |
| B: epilog P2637–P2691 integral și fragmente țintite. SH: final P2076–P2130 integral și fragmente țintite. | **Numai dacă se selectează Alex:** lectură integrală comparată B/SH și decizie asupra statutului fiecărui text, succesiunii, identităților și familiei. Nu este obligatorie auditarea integrală a acestei alternative pentru a continua documentarea G01 a Isabellei. |
| N: epilog/notă/teaser P3739–P3792 integral, fragmente de deznodământ și verificări țintite. Premisa din Z citită integral; outline și NP inspectate selectiv. | **Numai dacă se selectează Ten Crowns:** lectură integrală N și reconcilierea planului/biblei/anexelor cu moartea lui Malachar, League of Crowns și costul revenirii lui Dorian. Nu se certifică un canon al tuturor celor zece volume din probele actuale. |
| Site-ul și A au fost verificate la un moment precis; au fost înregistrate amprentele surselor principale. | Identificarea versiunii de referință efectiv acceptate pentru G01 și raportarea oricărei schimbări ulterioare. Dacă este necesar pentru canon, verificarea corespondenței cu ediția disponibilă cititorilor. Nu se presupune că metadatele publice sunt identice cu textul livrat. |

La ieșirea din G01 trebuie să existe un canon integral documentat pentru seria selectată, conflicte rezolvate explicit ori păstrate ca blocaje clare și evaluare independentă a versiunii exacte. SEL-001 nu declară îndeplinite aceste condiții. Cercetarea factuală și banca de mecanisme sunt lucrări ulterioare distincte de această selecție; raportul nu le simulează și nu le transformă în scene. În particular, corectarea omisiunii F01 în acest document nu rezolvă contradicția Boucher/Dubois din sursă. G01 rămâne blocat pentru închidere și pentru trecerea la scriere până la lectura integrală, reconcilierea documentată a identității și îndeplinirea celorlalte condiții; findingul de audit așteaptă retest independent.

## 9. Limite și livrabil

- Lectura integrală cerută pentru **finalul capitolului 24, epilogul, teaserul Hotelul V2 și documentul Story_Bible_FINAL** este acoperirea declarată și păstrată din r01, efectuată pe DOCX, cu referințe P exacte. Nu a fost efectuată o lectură critică integrală, scenă cu scenă, a tuturor romanelor.
- Au fost inventariate fișierele din rădăcina indicată și inspectate sursele relevante pentru cele trei opțiuni. Nu a fost identificat, în inventarul de nume consultat, un manuscris separat The Magenta Letters sau The Eastern Sands. Aceasta nu dovedește inexistența lor în alte locații, sub alte nume sau în arhive neinspectate.
- Nu s-au verificat integral toate manuscrisele NOIR/AURORA, edițiile de pe platforma de lectură, fișierele RO/DE, coperțile, drepturile, istoricul cultural francez ori exactitatea tehnică a scufundărilor. Formulările despre aceste lucruri în ficțiune sau în rapoartele vechi nu devin constatări externe ale P-CANON.
- Concordanța site/local este valabilă pentru fișierul și momentul HTTP consemnate; nu dovedește că fiecare ediție livrată cititorilor corespunde masterelor locale și nu este o monitorizare continuă. Site-ul nu a fost accesat din nou pentru această implementare r02.
- Constatarea suprapunerii B/SH nu este audit de plagiat sau verdict definitiv de reclasificare. Tabelele separă ceea ce textele afirmă de ceea ce ar trebui decis editorial.
- Recomandarea SEL-001 rămâne **DRAFT de selecție preliminară G00, neaprobat**, până la decizia responsabilului editorial și evaluarea separată a versiunii exacte. Raportul nu închide G01, nu produce romanul, nu produce un plan detaliat de scene și nu modifică sursele pentru a elimina contradicțiile. Corecția SEL-001-A-CANON-F01 este implementată în r02, păstrată și în staging, și așteaptă evaluare independentă; nici numele de familie, nici findingul nu sunt închise de autor.

**Fișier livrat în staging:** [02_DOCUMENTARE/r02_staging/CANON_EXISTENT.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/r02_staging/CANON_EXISTENT.md>). **Rezultatul implementării:** [06_REGISTRU/MASURI/SEL-001-rezultate-r02.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/MASURI/SEL-001-rezultate-r02.md>).

Predare P-CANON r02_staging: omisiunea documentară SEL-001-A-CANON-F01 este tratată în această copie nouă, cu proba ambelor nume, căsătoria separată și blocajul G01 explicit. Nu este atribuit niciun scor, nu este emis verdict de acceptare sau închidere a findingului și nu este solicitată aprobarea unui plot. Recomandarea rămâne selecție preliminară G00, DRAFT. Coordonatorul a integrat r02 după metaaudit și arhivarea r01-after-audit; versiunea r01 arhivată, RETURN r01, planul PLANIFICAT și arhivele istorice nu sunt modificate. Fișierul curent pentru audit este 02_DOCUMENTARE/CANON_EXISTENT.md; mențiunile de staging din metodă și predarea P-CANON descriu etapa istorică de pregătire, nu o integrare încă neefectuată.
