# Fara titlu

ID: `01a13fde-721d-7f70-a836-8840ef62470e`  
Proiect: WildMotion  
Export UTC: 2026-10-15T15:26:13.346330+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Asistent

Audit efectuat **fără modificarea documentelor proiectului**. Extracțiile și imaginile de verificare sunt în `C:\Users\User\AppData\Local\Temp\revo_audit`. Textul extras din 176 DOCX/PDF este în `all_text.json`.

### Versiunile dosarului

Există două versiuni importante, care nu trebuie amestecate automat:

- **„Achizitie REVO 5C”**: 14 documente procedură Anexele 1–7 și 10, două oferte PDF Marius/ARIDE, ofertă REVO marcată PROIECT, notă de verificare și două proiecte TGB. Are încă REVO cu TVA, reprezentant/telefon necompletate și recepție **22.05.2026**. Subfolderele celor două persoane fizice au contracte separate din12.10.2026.
- **„REVO 5C -CFMoto”**: documente actualizate cu REVO **neplătitor TVA**, reprezentant Giurgiu, ofertă REVO PDF, factură nr.5/14.10.2026, recepție14.10.2026, trei certificate de garanție și acte firmă. Are însă vechile estimări, comparații cu TVA19%, contract18.05.2026 și identificatori interni prezentați ca serii.
- „Achizitie veche”, „Dosar Achizitie”, ZIPurile omonime și drafturile istorice păstrează versiuni DANCOR. Acestea sunt surse/arhivă, nu ar trebui rescrise ca documente REVO.

### 1. Datele ofertelor și TVA

**Confirmat în ambele dosare:**

| Document | Data existentă |
|---|---|
| Invitații WM-ATV-009/010/011 | 27.04.2026 |
| Toate trei ofertele WM-ATV-015/016/017 | 04.05.2026 |
| Termen depunere | 04.05.2026, ora16 |
| Nota atribuire WM-ATV-022 | 11.05.2026 |
| Comunicări rezultat | 12.05.2026 |
| Contract WM-ATV-033 | 18.05.2026 |

Prin urmare ofertele sunt toate **la7zile**, nu la2/4/5zile după invitație.

Dacă se păstrează invitația27.04 și se aleg zile **calendaristice**, o variantă de aprobat este REVO29.04, Marius01.05, ARIDE02.05. **Această repartizare este o propunere, nu fapt documentat.** Dacă întreaga procedură trebuie mutată spre septembrie, trebuie stabilit calendarul real; ofertele au valabilitate30zile de la04.05 și nu acoperă automat18.09.

TVA21% este deja calculat corect în ofertele PDF Marius și ARIDE din ambele dosare:

| Ofertant | Net | TVA21% | Total ofertă |
|---|---:|---:|---:|
| Marius Code WNK |226.194,96|47.500,94|273.695,90|
| ARIDE RIDE IT |226.447,06|47.553,88|274.000,94|

**Excepție importantă REVO:** imaginea originală `3. Achizitie\2. Revo 5C SRL\ANAF -Revo 5C neplatitor de TVA.png` arată interogare ANAF la **14.10.2026**, REVO neînregistrată în scopuri TVA conformart316. Versiunea CFMoto folosește corect, conform acestei dovezi, „TVA nu se aplică”, total225.564,71. Nu trebuie introdus21% automat la REVO.

În dosarul mai vechi AchizitieREVO:
- ofertă REVO proiect:225.564,71+47.368,59 TVA21%=272.933,30;
- contract/atribuire/recepție:225.564,71+42.857,29 TVA19%=268.422.
Această versiune trebuie reconciliată cu regimul REVO și oferta efectiv asumată.

Ofertele examinate au rubrici de semnătură goale în text; nu trebuie afirmat că au fost depuse/reemise la alte date fără confirmarea faptelor și asumarea ofertanților.

### 2. Anexa5 și comparația

**Eroarea de valori confirmată:**

- Marius în Anexa5:269.172,00; oferta273.695,90. Diferență **4.523,90lei**.
- ARIDE în Anexa5:269.472,00; oferta274.000,94. Diferență **4.528,94lei**.
- Ambele valori greșite provin din19%, nu21%.
- În Anexa5 CFMoto, REVO este225.564,71 total fără TVA aplicabil; în AchizitieREVO este268.422.

**Template original necompletat NEGĂSIT.** Am verificat:
- toate DOCX-urile extrase din proiect după conținut, nu doar nume;
- ZIPul de la rădăcină `Dosar Achizitie ATV uri Wild Motion.zip` și copiile sale;
- ZIPul REVO5C-CFMoto, arhivele drafturilor procedurii;
- `Publicare site inosocrural.rar`;
- metodologia oficială de evaluare planuri de afaceri,19pagini;
- anexele scanate ale contractului de subvenție.

Toate anexele5 de atribuire găsite sunt deja completate. `1. Documente oficiale InoSocRural 311779\Anexa5_Planul de afaceri.doc` este **altă anexă**, planul de afaceri, nu nota de atribuire. Nici anexeleV ale contractului de subvenție nu sunt template achiziții.

Cap actual în AchizitieREVO: „Denumire ofertant | Nr înreg oferta | Cantitate | Preț fără TVA | Valoare fără TVA | Total cu TVA”.
Cap CFMoto: „Denumire ofertant | Nr înreg oferta | Cantitate | Preț unitar | Valoare | Total de plată”.

Nu pot certifica neconformitatea exactă față de un template încă negăsit și nu recomand reconstruirea lui din memorie sau folosirea unui model generic. Este necesară localizarea/copierea fișierului original necompletat.

### 3. AA2 și plafon221.838

Sursa:
`6. Implementare Proiect-Raportari_Decontari\10. Octombrie\10. Personal\Act_Aditional_nr_2_WILD_MOTION s.pdf`
(plus DOCX și PDF `(1)`).

**Confirmat textual și vizual:**
- p3 varianta inițială și p4 varianta modificată;
- linia4.1 ATV600–1000cmc;
-3buc × **73.946lei =221.838lei**;
- antetele spun **TVA inclus**;
- finanțat subvenții187.517,82 + contribuție proprie34.320,18 =221.838;
- AA2 din09.10.2026 schimbă postul HR în Programator și păstrează această linie.
- AA1 DOCX precizează deja majorarea liniei de la205.638 la221.838 prin realocare16.200lei.

**Aprobarea bilaterală nu este confirmată prin copia găsită.** AA2 s.pdf are un singur câmp de semnătură digitală, nume Nicolae-Ioan Capota, data09.10.2026 15:07. P5 rubricile grafice de semnătură sunt goale pentru ambele părți; nicio semnătură digitală ASCO identificată. ArtIII spune că intră în vigoare la semnarea ultimei părți. Prezența semnăturii digitale nu a fost validată criptografic; este constatare de structură/metadate. Obțineți exemplarul aprobat sau dovada aprobării.

Anexa1 actuală este greșită și la finanțare: pune **221.838 drept subvenție** plus46.584 contribuție=268.422, ceea ce nu corespunde AA2.

Recomandări:
- estimare totală/buget221.838, dacă se confirmă bugetul aprobat;
- distribuție187.517,82/34.320,18;
- nu converti221.838 în „fără TVA”.
- pentru un calcul standard21% inclus: net183.337,19 și TVA38.500,81; această defalcare nu se aplică mecanic ofertei unui furnizor scutit.

Oferta/contractul REVO dinCFMoto **225.564,71 depășește bugetul cu3.726,71**. A corecta estimarea nu rezolvă automat încadrarea ofertei; trebuie stabilit prețul real asumat sau finanțarea suplimentară aprobată, fără modificare unilaterală.

Contractele PF:3×72.933=218.799lei cost achiziție REVO, diferență3.039față221.838 înainte de impozit și altecosturi. Nu este prețul automat de vânzare REVO cătreWILD.

### 4. Contract05→09

Contractul relevant este **WM-ATV-033/18.05.2026, Anexa7**, în ambele dosare. Data apare în titlu și în clauza finală („încheie astăzi18.05.2026”), plus referințe în recepție, factură, garanții/proiectAA.

Schimbarea cerută, păstrând ziua, ar fi **18.09.2026**, dar trebuie confirmată ca data reală:
- AchizitieREVO are recepție22.05.2026, devenită anterioară contractului dacă schimbăm numai contractul;
- CFMoto are recepție/factură14.10.2026, compatibile ca interval cu18.09 și termen30zile;
- ofertele/atribuirea dinaprilie–mai și valabilitatea30zile necesită clarificare;
- contractele PF din12.10.2026 nu sunt cele vizate de schimbarea lunii contractului de furnizare.

### 5. VIN șiCOC

În AchizitieREVO lipsesc identificatori individuali și rubrici dedicate VIN/COC. Contractul cere generic documente conformitate/omologare și înmatriculare.

În CFMoto, șirurile **REVO-WM-CFmoto1/2/3** apar ca serii în:
- Anexa10 recepție;
- factura nr5 Word/PDF;
- cele3certificate garanție Word/PDF, inclusiv denumirile fișierelor.

Acestea sunt coduri interne, nu VIN reale. Propun:
- tabel3rânduri, ATV1/2/3, VIN„de completat ulterior”, COC nr/data„de completat ulterior”;
- în contract/anexă identificare, recepție, factură și garanții;
- documentele semnabile ulterior trebuie completate cu VIN reale/COC și nu trebuie să certifice documente deja predate sau recepție integral conformă dacă ele încă lipsesc.
- Înaintea modificării PF, clarificat dacă noua cerință VIN vizează și cele2contractePF, deoarece utilizatorul ceruse anterior explicit fărăserii.
- Modelul încă diferă: proceduraCFMoto vs proiecteTGB/PF TGB. Nu armoniza fărădecizie.

### 6. Număr contractsubvenție vs codproiect

**Confirmat în sursa primară scanată:**
`00. Contract de finantare\CONTRACT SUBVENTIE_WILD MOTION.pdf`
- p1 număr manuscris **54/311779**;
- p23 data olografă **31.10.2025**;
- p24 semnăturile ambelor părți vizibile.
- deconturile folosesc uneori invers „311779/54/31.10.2025”; sursa primară justifică forma54/311779.

Propun:
**„Contract de subvenție nr.54/311779 din31.10.2025”**
separat de
**„Proiect InoSocRural – Întreprinderi sociale inovative în mediul rural din Regiunea Centru, Cod SMIS311779; cod PIDS/83/PIDS_P3/OP4/ESO4.1/PIDS_A12/311779”.**

Erori „contractsubvenție=PIDS…” identificate în fiecare dosar:
- Anexa1;
- cele3invitațiiAnexa2;
- Anexa5;
- cele3comunicăriAnexa6;
- suplimentar facturaWord/PDF CFMoto.
AA1/AA2 au și ele această confuzie; actele semnate nu se rescriu retrospectiv. Se propune rectificare/asumare separată dacă intră înscope.

ContractulAnexa7 și PV au codSMIS înantet/subsol dar nu rubrica greșităPIDS ca numărsubvenție; se poate adăuga referința corectă, nu există o simplă înlocuire acolo.

### 7. Invitații

Toate3invitațiileAnexa2, ambele dosare:
**„Valoarea estimată:225.564,71lei fărăTVA”**, necorelată cu221.838TVAinclus dinAA2.

De corectat împreună cuAnexa1/5 după confirmarea:
- bugetului aprobat;
- bazei net/brut și regimuluiREVO;
- calendarului real;
- eventual prețului contractului, întrucât actualul225.564,71scutit depășește221.838.

### Alte observații factuale pentru aprobarea intervenției

- REVO225.564,71 total vs75.188,24×3=225.564,72: diferență1ban la rotunjire.
- ARIDE75.482,35×3=226.447,05 vs totalofertă226.447,06: diferență1ban. Nu modifica totalul emitentului fărăclarificare; uniformizează modalitatea de rotunjire.
- Roș RaduIoan apare administratorARIDE în ofertă și Anexa3; există și contractPF prin care vinde cătreREVO. Anexa3 declară evitarea conflictului cuachizitorul și obligația informării despre modificări. Această asociere documentară cere clarificarea independenței ofertelor, **nu demonstrează automat conflictdeinterese**.

**Întrebări/decizii necesare înainte de editare:**
1. Care este dosarul de bază: actualulCFMoto sauAchizitieREVO, și rămâneCFMoto sauTGB?
2. Calendar real: doarcontract18.09 sau întreagaprocedură mutată? Ce ofertant corespunde+2/+4/+5, calendaristice/lucrătoare?
3. PrețulREVO rămâne225.564,71 cu diferențăsuplimentară3.726,71 sau există ofertănouă/prețasumat înplafon221.838?
4. Unde este templateoriginalnecompletatAnexa5 și exemplarulAA2 aprobatdeASCO?
5. VIN/COC și actualizareanumărului de subvenție se aplică șiPF/AA-uri sau doarprocedurii?
6. După aceste clarificări, aprobare explicită a listei concrete de modificări, conformcererii utilizatorului, apoi agenteditor și agentverificator independent.
