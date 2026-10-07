# CAD BIM metrologie și imprimare 3D

Autor responsabil: agent specialist CAD și imprimare 3D. Destinatar: managerul de produs, arhitectul iOS și auditorul. Data verificării surselor: 2 octombrie 2026. Stare: specificație propusă, fără implementare sau rezultate experimentale.

Aplicația trebuie să transforme o captură într-un rezultat geometric cu scară explicată, incertitudine cunoscută și destinație clară. Un model vizual frumos nu dovedește corectitudinea dimensională. Prioritatea propusă este păstrarea dimensiunilor pe întregul traseu: captură, reconstrucție, editare, export, deschidere în aplicația destinatară și, când se cere, piesă imprimată.

## 1 Separarea produselor geometrice

Se proiectează șase reprezentări legate prin identificatori și transformări versionate:

1. Date de captură: cadre, adâncime, calibrare disponibilă, poziții cameră, timpi și indicatori de calitate. Acestea există persistent numai în modurile care permit salvarea.
2. Nor de puncte: eșantioane XYZ cu culoare, normale și atribute opționale. Nu reprezintă automat o suprafață închisă.
3. Mesh de scanare: suprafață triangulată cu textură, care poate conține goluri și regiuni incerte.
4. Model măsurabil: geometrii și repere asociate cu scară, proveniență și estimarea erorii.
5. Model de fabricație: copie derivată, reparată și verificată pentru procesul ales; modificările nu suprascriu scanarea originală.
6. Model semantic al clădirii: camere, pereți, goluri, niveluri, relații și cote. Grosimea pereților, materialele sau structura ascunsă nu se inventează dintr-o singură față scanată.

Dimensiunile se păstrează în metri în schema canonică propusă; milimetrii se folosesc explicit la export pentru fabricație. Fiecare reprezentare declară unitățile, axele, orientarea, originea locală, transformarea către proiect, proveniența scării și metoda măsurării.

**Decizie propusă:** toate elementele poartă categoria „observat”, „estimat”, „corectat manual” sau „generat pentru închidere”. Umplerea unui gol produce o suprafață derivată, care nu poate deveni probă metrologică.

## 2 Dimensiuni pentru cele trei componente

### 2.1 Obiecte cu dimensiuni

Fluxul propus permite lungime între două puncte, distanță între plane, diametre potrivite pe suprafețe cu suficientă acoperire, cutie de încadrare orientată, secțiuni și distanțe între repere. Cutia de încadrare este o estimare a gabaritului, nu o cotă funcțională de proiectare. Diametrul găurilor parțial vizibile trebuie marcat nesigur.

Sursa scării se afișează: sistem metric AR, reper măsurat independent sau scalare manuală. O corecție dintr-o cotă cunoscută se aplică inițial uniform, cu păstrarea versiunii precedente. Scalarea diferită pe axe reprezintă deformare deliberată și cere etichetă separată. Reperul de calibrare și reperele de verificare sunt distincte: aceeași lungime nu poate fi folosită simultan pentru corectare și validare independentă.

Metadatele unei cote includ punctele sau primitivele selectate, valoarea, unitatea, starea trackingului, versiunea geometriei, metoda de calcul, sursa scării, clasa materialului dacă este cunoscută și starea incertitudinii. Se oferă export CSV/JSON și raport PDF cu imaginea cotată.

### 2.2 Măsurare live fără persistența mediului

Rezultatul de bază există în memoria sesiunii. Nu se scriu automat norul, meshul, imaginile, ancorele sau traiectoria în proiect, cache persistent, telemetrie ori copii de siguranță. Salvarea unei fotografii cotate este o acțiune explicită: utilizatorul alege imaginea finală, iar aplicația salvează doar imaginea și metadatele aprobate. Pentru modul strict fără salvare nici această acțiune nu este disponibilă.

Metrologia rămâne aceeași: cifra se estompează sau este suspendată când trackingul se degradează; utilizatorul vede suprafața și punctele alese. O valoare stabilă numeric nu justifică singură încredere mare. Reluarea aplicației începe o sesiune nouă în acest mod, deoarece un jurnal complet cu date spațiale ar încălca intenția de confidențialitate.

### 2.3 Camere apartamente și case

Modelul canonic propus conține proiect, clădire, nivel, cameră, element și observație. Fiecare cameră păstrează transformarea către nivel; toate transformările și corecțiile manuale sunt versionate. Alinierea camerelor folosește suprapuneri observate și repere comune. Legarea nivelurilor folosește cote de nivel și repere documentate, cu posibilitatea introducerii unei înălțimi măsurate extern.

Se separă planul de pardoseală, secțiunea orizontală și proiecția vederii de sus. Pereții înclinați, curbele, nișele și tavanele în pantă rămân cazuri distincte. Suprafața utilă, aria geometrică a pardoselii și aria învelitorii nu se numesc interschimbabil. Regulile comerciale sau normative de suprafață necesită specificație separată pe jurisdicție.

Clădirile mari cer segmentare, controlul erorii cumulative, închiderea traseului și verificări independente la distanță. Nu se extrapolează automat performanța unei camere către o casă cu mai multe niveluri.

## 3 Politica de formate

Prioritățile canonice ale produsului sunt stabilite în [Criterii canonice](../05_validare/CRITERII_CANONICE.md). Sunt obiective de implementare, fără afirmația că exporturile există deja:

- **P0:** 3MF și STL pentru obiecte, PLY pentru nor de puncte, USDZ pentru previzualizare, DXF pentru plan 2D cotat și JSON lateral pentru unități, transformări și proveniență.
- **P1:** OBJ, glTF/GLB, E57, LAS/LAZ, XYZ, PCD și DWG prin SDK cu licență verificată. Validarea fiecărui convertor precedă lansarea.
- **P2:** IFC, STEP și AMF; VRML și 3DS sunt opțiuni experimentale de compatibilitate, cu implementare, licență și destinatari încă de cercetat.
- **G-code și formatele de mașină:** rezultate ale unui slicer calificat pentru dispozitiv și material, fără exportator universal în aplicație.

Un fișier JSON lateral din P0 completează formatele care nu păstrează integral informația metrică. Exporturile PDF/SVG/PNG/CSV pentru raportare au prioritatea P1; salvarea imaginilor din modul live rămâne explicită.

Matricea completă din `matrice_formate.csv` folosește „direct propus” pentru un export care ar fi implementat în produs, „convertor propus” pentru un serviciu sau companion și „opțional” pentru cercetare viitoare. Niciuna dintre aceste etichete nu înseamnă funcție deja livrată.

### 3.1 Imprimare 3D

3MF este formatul preferat propus pentru schimb de geometrie de fabricație, deoarece include unități și poate grupa obiecte. Se fixează o versiune a specificației și un subset de extensii, apoi se verifică în slicerele țintă. Un container valid nu dovedește că o piesă are pereți fabricabili. STL rămâne exportul de compatibilitate: interfața și manifestul lateral declară milimetri, deoarece formatul nu transmite o unitate standard explicită. OBJ este util pentru mesh și textură, dar suportul de culoare diferă între destinatari. [CAD-S01, CAD-S02, CAD-S03]

**Capcană de interoperabilitate:** un proiect 3MF al unui slicer poate include setări și extensii specifice. Exportul aplicației trebuie să fie „model 3MF generic”, separat de „proiect slicer”. Profilurile de imprimantă nu se injectează implicit.

G-code este un traseu de mașină rezultat din slicing, dependent de imprimantă, profil, material și firmware; nu este echivalent cu scanarea sau meshul. Aplicația poate oferi predarea fișierului către un slicer. Generarea sau trimiterea comenzilor către imprimantă necesită o etapă distinctă, validată pe fiecare profil. Formatele proprietare pentru rășină se tratează ca integrare de slicer și dispozitiv, fără promisiunea unui export universal. [CAD-S04, CAD-S05]

### 3.2 CAD și BIM

Pentru planuri, se propune DXF cu unități, straturi, polilinii închise, goluri, texte și cote. Straturile inițiale: WALLS, OPENINGS, WINDOWS, ROOMS, DIMENSIONS, FURNITURE, UNCERTAINTY. Grosimile presupuse și contururile completate apar distinct. ezdxf poate genera DXF, dar nu este convertor DWG și nici nucleu geometric CAD. [CAD-S06]

DWG se planifică prin SDK licențiat, după evaluarea ODA Drawings SDK sau Autodesk RealDWG. Nu se redenumește un DXF și nu se folosește automat distribuția gratuită a unui utilitar ca dovadă a dreptului de integrare comercială. Pentru ODA, pagina verificată indică 3.000 USD primul an și 2.250 USD reînnoire pentru planul Commercial limitat; Sustaining indică 7.500 USD și 4.500 USD și permite SaaS/distribuție nelimitată. Costurile sunt valori publicate la consultare, fără taxe, negocieri sau garanție contractuală. RealDWG trimite licențierea către Tech Soft 3D; prețul necesită ofertă. [CAD-S07, CAD-S08, CAD-S09]

Un mesh convertit în BRep poate păstra câte o față pentru fiecare triunghi, sau poate necesita potrivirea unor primitive și suprafețe. Nu reconstruiește automat intenția CAD, istoricul parametric, toleranțele sau caracteristicile mecanice ale obiectului original. STEP se oferă inițial doar pentru primitive/solide reconstruite și validate, apoi pentru conversii avansate marcate ca aproximări. Documentația Autodesk distinge conversia faceted, prismatic și organic și arată că lipsa închiderii poate produce suprafață, nu solid. [CAD-S10]

IFC este un model de informație: pereți și camere cu relații, niveluri, unități și identificatori. Un mesh într-un container IFC nu devine automat un model BIM semantic. Se propune un subset IFC4 explicit: IfcProject, IfcSite când există informația, IfcBuilding, IfcBuildingStorey, IfcSpace, elemente de perete și goluri unde datele permit. Schema exactă și vederea de schimb se fixează cu destinatarii. IfcOpenShell se evaluează pe componente; nucleele LGPL și instrumentele GPL au obligații diferite. [CAD-S11]

### 3.3 Nori de puncte și vizualizare

PLY și XYZ sunt primele exporturi propuse pentru puncte; atributele și unitățile se descriu într-un manifest. PCD este un export pentru pipelineuri tehnice. Pentru LAS/LAZ se aleg explicit versiunea, formatul punctelor, scara numerică și sistemul de coordonate. Nu se scrie un EPSG inventat pentru o cameră locală. Nu se completează fictiv intensitatea, timpul GPS sau numărul de retur al unui senzor care nu le produce. [CAD-S12, CAD-S13]

PDAL documentează export E57 prin plugin, cu un singur nor cartezian per fișier și fără puncte sferice. Exportul inițial propus este un nor fuzionat ori câte un fișier pe cameră, însoțit de manifest. Pentru păstrarea mai multor scanări structurate într-un singur E57 este necesar un alt writer verificat și teste specifice. Opțiunea de precizie dublă trebuie evaluată. [CAD-S14]

La LAS, setarea implicită PDAL pentru scală este 0,01; cu unități în metri ar introduce un pas de cuantizare de 1 cm. Cerința propusă setează explicit pasul, de exemplu 0,0001 m pentru loturile de test adecvate, și verifică overflowul coordonatelor întregi. Pasul mai mic nu îmbunătățește precizia senzorului. [CAD-S13]

glTF/GLB este pentru distribuție vizuală și randare; USDZ este pentru ecosistemul USD și prezentare AR. Exporturile trebuie să păstreze transformări și scară, dar nu sunt certificate de fabricație. Nici aspectul fotorealist, nici Gaussian splatting nu substituie o suprafață metrică validată. [CAD-S15, CAD-S16]

## 4 Biblioteci și integrare propusă

| Componentă | Evidență și licență observată | Rol propus | Probă necesară înainte de integrare |
|---|---|---|---|
| Open3D | C++/Python, MIT; distribuții desktop documentate [CAD-S17] | filtrare, aliniere, reconstrucție și evaluare pe companion/server | build fixat, memorie, metrici, audit dependențe; nu se declară SDK iOS |
| COLMAP | SfM/MVS; BSD pentru nucleu cu dependențe separate [CAD-S18] | referință fotogrammetrică și pipeline offline | versiune/commit, drepturi dependențe, scală externă, resurse; nu se presupune rulare pe iPhone |
| PDAL | BSD cu componente/dependențe de verificat [CAD-S19] | LAS/LAZ/E57 și procesare nor | pluginuri disponibile, atribute, precizie numerică, round trip |
| ezdxf | MIT, Python [CAD-S06, CAD-S20] | planuri DXF în companion/backend | versiune DXF, unități, cote, fonturi și deschidere în CAD |
| IfcOpenShell | licențe per modul LGPL/GPL [CAD-S11] | scriere și audit IFC | listă exactă module, SBOM și validare semantică |
| lib3mf | BSD-2-Clause; C++ cu citire/scriere/validare [CAD-S21] | export 3MF generic | build iOS de demonstrat sau companion; extensii limitate și fixtureuri |
| ODA Drawings | abonament comercial [CAD-S07, CAD-S08] | DWG cu straturi și cote | contract, platforme suportate, distribuție, convertor izolat |
| Autodesk RealDWG | licențiere separată [CAD-S09] | alternativă DWG/DXF | ofertă, platformă, condiții de redistribuire și teste |

Licența unui depozit nu acoperă automat binarul cu toate dependențele. Se păstrează commitul, licențele tranzitive, opțiunile de build și lista de componente. Afirmațiile juridice finale se iau din contractele efectiv acceptate; acest document stabilește activitățile tehnice de verificare.

## 5 Pipeline pentru o piesă imprimabilă

Toți pașii de mai jos sunt activități propuse și generează evenimente separate în jurnal.

1. **Definirea utilizării.** Utilizatorul alege replică decorativă, piesă de probă sau piesă cu cote funcționale. Se salvează dimensiunile critice, toleranțele și procesul avut în vedere. Rezultat: fișă de cerințe a piesei.
2. **Pregătirea capturii.** Se verifică iluminarea, suprafețele problematice și acoperirea. Un reper cu dimensiune cunoscută este fotografiat separat de reperele de control. Acoperirile mate pot modifica dimensiunea sau suprafața; utilizarea lor se documentează și se aplică doar obiectelor potrivite.
3. **Reconstrucție.** Se păstrează modelul brut, scara, traseul prelucrării și parametrii. Zonele nevăzute nu primesc statut de măsurare.
4. **Verificare dimensională.** Se măsoară repere independente cu șubler, micrometru sau instrument adecvat, cu incertitudine cunoscută. Diferențele se raportează înainte de reparații.
5. **Curățare.** Se elimină suportul de scanare și componentele izolate; fiecare operație este reversibilă. Se raportează variația volumului și a cotelor critice.
6. **Reparare.** Se detectează muchii nemanifold, găuri, triunghiuri degenerate, auto-intersecții, normale și componente. Umplerea automată este previzualizată.
7. **Pregătire de fabricație.** Se verifică grosimi, goluri, acces pentru îndepărtarea suporturilor, suprafețe de contact și volumul de lucru. Pragurile provin din profilul calificat de proces; grosimea stratului nu este egală cu toleranța piesei.
8. **Export.** Se creează 3MF generic și opțional STL în mm, plus raport dimensional și hashuri. Verificatorul recitește fișierul și compară dimensiunile și transformările.
9. **Slicing.** Slicerul ales folosește profilul real de imprimantă/material/duză. Se inspectează straturile pentru regiuni lipsă, pereți eliminați, suporturi și coliziuni. Se salvează versiunea profilului și estimările slicerului.
10. **Imprimare și postprocesare.** Jurnalul de atelier include imprimanta, materialul și lotul, orientarea, setările aprobate, incidentele și operațiile de postprocesare.
11. **Control final.** Se măsoară aceleași cote pe piesă. Se separă eroarea scanării de eroarea fabricației. Un model corect nu compensează automat contracția sau deformarea la imprimare.
12. **Arhivă de reproducere.** Se păstrează legătura între scanare, model derivat, fișier exportat, proiect de slicer, profil și raportul piesei; nu se reutilizează automat un G-code pentru alt dispozitiv.

### 5.1 Procese și materiale

| Proces | Utilizare propusă | Date suplimentare obligatorii | Verificare concretă |
|---|---|---|---|
| FFF/FDM cu PLA/PETG | prototipuri și replici | duză, material, orientare, pereți, umplere, temperaturi din profil | cupoane de cote și potrivire, deformare și suporturi |
| FFF cu ABS/ASA/PA sau compozite | aplicații tehnice selectate | condiționare material, incintă, compatibilitate imprimantă și profil validat | contracție pe axe, anisotropie și stabilitate după condiționare |
| SLA/MSLA | detalii fine și replici | rășină, expunere, suporturi, spălare și postîntărire conform producătorului | cote după ciclul complet, deformare, evacuare pentru modele goale |
| SLS/MJF | comandă la furnizor | reguli furnizor, material, grosimi, spații și evacuare pulbere | raport furnizor și verificarea cotelor critice |
| Metal și utilizări critice | extensie prin furnizor calificat | proces, material și calificare dedicate | acceptare separată; un export valid geometric nu certifică piesa |

Tabelul reprezintă un plan de calificare, nu recomandări de temperatură sau toleranțe universale. NIST documentează necesitatea caracterizării geometriei și a procesului și oferă artefacte de test; acestea susțin alegerea unei metodologii, nu performanța aplicației noastre. [CAD-S22, CAD-S23]

### 5.2 Slicere verificate documentar

PrusaSlicer documentează 3MF, STL, STEP, OBJ și AMF; STEP se triangulează la import, iar materialele/textura OBJ sunt ignorate. UltiMaker listează STL, OBJ, X3D și 3MF, cu G-code/UFP ca rezultate distincte. Codul public Bambu Studio include importurile STL, STEP, OBJ și 3MF; alte formate sunt dependente de platformă și versiune. [CAD-S02, CAD-S04, CAD-S24]

**Plan de compatibilitate:** minimum 10 fixtureuri geometrice × 3 formate principale (3MF/STL/OBJ) × 3 slicere = 90 importuri pe versiunile de referință fixate la test. Nu se raportează „90 teste trecute” până când fișierele, logurile și capturile din aplicațiile respective există. Printarea color și extensiile 3MF se testează separat.

## 6 Protocol metrologic propus

### 6.1 Întrebări de cercetare

RQ1: În ce condiții de dispozitiv, distanță, lumină și suprafață poate fi menținută scara și ce erori rămân?

RQ2: Ce îmbunătățire produce un reper de scară independent și care este costul UX al calibrării?

RQ3: Cum se propagă eroarea de la camere individuale la apartament și apoi la mai multe niveluri?

RQ4: Cât modifică filtrarea, decimarea, închiderea golurilor și conversia dimensiunile funcționale?

RQ5: Poate aplicația anticipa corect măsurările care vor depăși toleranța, fără a bloca inutil capturile valide?

Ipotezele, metricile și excluderile se înregistrează înainte de evaluarea finală. Datele folosite pentru calibrare și alegerea pragurilor nu se reutilizează ca set final independent.

### 6.2 Design experimental

**Pilot propus:** 10 obiecte din clase de suprafață diferite, 3 operatori, 3 dispozitive eligibile și 3 repetări complete = 270 sesiuni. Un dispozitiv este non-LiDAR când fluxul permite. Pilotul estimează variația și timpul; nu fundamentează singur afirmații pentru toate iPhoneurile.

**Studiu principal propus:** 30 obiecte × 3 operatori × 3 dispozitive × 3 repetări = 810 sesiuni; 5 repere independente pe obiect = 4.050 observații dimensionale. Repetările sunt corelate: unitatea experimentală principală este sesiunea/obiectul, nu fiecare punct. Condițiile de lumină și distanță se alocă prin plan echilibrat; adăugarea lor ca factori compleți multiplică efectiv eșantionul.

**Camere propuse:** 12 încăperi cu geometrii variate × 3 operatori × 3 dispozitive × 3 repetări = 324 sesiuni; minimum 8 cote de referință pe încăpere = 2.592 observații. Separat: 6 configurații de apartament cu minimum 4 camere × 3 operatori × 3 repetări = 54 sesiuni agregate pe dispozitivul de referință. Minimum 3 configurații includ două niveluri; această extensie se raportează distinct și nu dovedește generalizare pentru orice clădire.

**Live propus:** 20 configurații de distanță/suprafață × 3 operatori × 3 dispozitive × 3 repetări = 540 sesiuni, fără persistența mediului în produs. Instrumentația de laborator obține consimțământ separat; rezultatele agregate ale testului nu schimbă contractul modului privat.

Numerele sunt planificare, nu analiză de putere finalizată. După pilot, statisticianul stabilește dimensiunea necesară pentru efectul și intervalul de încredere urmărit, fără a elimina retrospectiv cazurile nefavorabile.

### 6.3 Referințe și metrici

Se folosesc etaloane/instrumente cu calibrare adecvată, o procedură de măsurare repetabilă și incertitudine suficient mai mică decât toleranța evaluată. Ținta de proiect pentru raportul incertitudine referință/toleranță este cel mult 1:4, justificată și verificată separat pentru fiecare clasă. Pentru geometrie complexă se folosește scaner de referință sau CMM cu procedură calificată, nu chiar iPhoneul testat.

Pentru fiecare cotă: eroare semnată e = măsurat − referință, eroare absolută, eroare relativă unde referința nu este apropiată de zero, bias, MAE, RMSE, mediană, P90 și P95. Se adaugă repetabilitate intraoperator, variație între operatori și dispozitive, rată de eșec și timp până la rezultat.

Pentru suprafețe: distanțe simetrice între suprafețe, percentile, fracția de acoperire, goluri și abatere în regiunile funcționale. Alinierea pentru validare este rigidă după scara stabilită; o aliniere cu scalare liberă ar ascunde eroarea de scară. Orice evaluare suplimentară cu similaritate se etichetează separat.

GUM oferă cadrul pentru bugetul de incertitudine. Se include contribuția referinței, repetiției, selecției reperelor, calibrării/scării, mișcării, materialului și prelucrării. Modelul simplificat cu suma pătratelor este permis doar când ipotezele de independență sunt justificate; altfel se includ covarianțe sau propagare numerică. Eticheta „95%” nu se deduce direct din scorul de confidence al senzorului. [CAD-S25]

### 6.4 Ținte de acceptare care trebuie validate

Aceste valori sunt **ținte de proiect inițiale**, nu precizie Apple, rezultate obținute sau garanții comerciale. Domeniile canonice de acceptare sunt obiecte 0,1–1 m, live 0,2–5 m și camere 1–8 m, conform [Criteriilor canonice](../05_validare/CRITERII_CANONICE.md). Cotele din afara acestor domenii, inclusiv obiecte de 50 mm sau camere măsurate până la 10 m, pot apărea numai în loturi exploratorii și nu intră în afirmația de acceptare.

| Clasă de utilizare | Domeniu propus | Țintă inițială pentru P95 al erorii absolute | Condiție |
|---|---|---|---|
| Obiecte generale | cote 0,1–1 m, suprafețe capturabile | max(5 mm, 1% din lungime) | evaluare per clasă dispozitiv și metodă; reper independent |
| Măsurare live | 0,2–5 m interior | max(20 mm, 1% din lungime) | suspendare la tracking slab; set adversarial separat |
| Dimensiuni cameră | 1–8 m | max(30 mm, 1% din lungime) | cote independente și raport pe geometrie |
| Îmbinare apartament | puncte comune și contur închis | reziduu P95 ≤ 30 mm pentru repere comune | țintă locală; eroarea globală se raportează separat |
| Piese cu ajustaje | cote funcționale restrictive | fără promisiune inițială | necesită validare independentă și reproiectare CAD |
| Export digital | fixtureuri exacte | abatere ≤ max(0,01 mm, 0,001% din gabarit) pentru formatele de mesh | fără a confunda eroarea numerică cu precizia scanării |

Criteriul de lansare propus cere limita superioară a intervalului de încredere de 95% pentru P95 sub pragul aplicabil, pe setul final, și o rată de succes raportată cu interval binomial. Bootstrapul se face pe grupuri independente, păstrând structura obiect/operator. Dacă eșantionul nu susține estimarea unei percentile, se raportează insuficiența; nu se afișează interval artificial îngust.

Pentru afișarea intervalelor individuale, ținta propusă este acoperire empirică 90–98% pentru intervalele nominale de 95%, pe minimum 200 sesiuni independente de evaluare. Intervalele foarte late nu rezolvă utilitatea: se raportează simultan lățimea lor și procentul măsurărilor utilizabile.

## 7 Cerințe verificabile

| ID | Cerință propusă | Rezultat și criteriu de acceptare |
|---|---|---|
| CAD-001 | Scară canonică unică | 100% entități geometrice au unitate și transformare; fișier fără acestea este respins |
| CAD-002 | Proveniență cotă | fiecare cotă are geometrie, metodă, versiune și sursă de scară |
| CAD-003 | Repere independente | setul de validare nu include reperul folosit la calibrare |
| CAD-004 | Cutie orientată | gabaritul și orientarea sunt explicite, cu preview înainte de export |
| CAD-005 | Scară păstrată | fixtureuri de 10/100/1.000 mm se reimportă în limita numerică stabilită |
| CAD-006 | STL declarat în mm | UI, nume descriptiv și manifest indică unitatea; 3 slicere verificate |
| CAD-007 | 3MF generic | validare structurală și 10 fixtureuri per slicer fără setări de imprimantă injectate |
| CAD-008 | Mesh și print separate | reparația produce versiune derivată și permite revenirea la original |
| CAD-009 | Topologie verificată | raport cu muchii deschise/nemanifold, degenerări, auto-intersecții și componente |
| CAD-010 | Goluri transparente | fiecare închidere este marcată generată și exclusă implicit din cote verificate |
| CAD-011 | Cote după decimare | abatere pe 5 cote critice per fixture sub toleranța aleasă |
| CAD-012 | Export texturi | OBJ include MTL/texturi; lipsurile sunt semnalate înainte de arhivare |
| CAD-013 | Nor și mesh distinse | PLY manifest indică tipul și câmpurile, fără interpretare ambiguă |
| CAD-014 | LAS configurat | teste pentru scale/offset/overflow și 100% câmpuri documentate |
| CAD-015 | Coordonate corecte | proiectele locale nu primesc coordonate geografice inventate |
| CAD-016 | E57 limitat explicit | un nor per fișier în writerul PDAL inițial; logul confirmă pluginul |
| CAD-017 | DXF util | unități, straturi, cote și contururi validate în două aplicații CAD țintă |
| CAD-018 | DWG licențiat | contract și SDK aprobate înainte de includerea exportului comercial |
| CAD-019 | STEP descris corect | raportul indică BRep/mesh, aproximare și abaterea conversiei |
| CAD-020 | IFC semantic | relații spațiale și unități valide pentru toate entitățile subsetului declarat |
| CAD-021 | Aliniere camere | transformări versionate, reziduuri calculate și posibilitate de corecție |
| CAD-022 | Mai multe niveluri | cota de nivel are sursă; nu se deduce dintr-o îmbinare ambiguă |
| CAD-023 | Slicing separat | niciun G-code fără imprimantă, material și profil identificabile |
| CAD-024 | Profil de proces | pragurile de grosime provin din profil validat, nu din preset universal |
| CAD-025 | Control piesă | raport înainte/după print pe aceleași cote și cu instrument identificat |
| CAD-026 | Mod live privat | 0 artefacte spațiale persistente în scenariile de test normal/crash/background |
| CAD-027 | Jurnal sigur | evenimente tehnice fără imagini, poziții și coordonate în modul privat |
| CAD-028 | Incertitudine onestă | „nevalidată” până la calibrare; nicio echivalare confidence=95% |
| CAD-029 | Eșecuri incluse | rata de eșec include sesiuni abandonate tehnic; motive documentate |
| CAD-030 | Export tranzacțional | fișier final disponibil doar după scriere, validare și hash; exportul întrerupt se reia |
| CAD-031 | Licențe trasabile | SBOM, commituri și licențe per componentă pentru fiecare versiune |
| CAD-032 | Compatibilitate măsurată | matricea arată versiunea aplicației destinatare, OS, fixture și rezultat |
| CAD-033 | Avertizare aplicabilă | toleranța cerută sub capacitatea validată produce cerere de verificare externă |
| CAD-034 | Schimb fără pierderi ascunse | fiecare export listează date păstrate, pierdute și transformate |

## 8 Jurnale și reluare

Fiecare sarcină tehnică produce: task_id, agent, start/end UTC, intrări cu hash, versiune algoritm, parametri, ieșiri cu hash, criterii, rezultate, probleme și următorul pas. La audit se adaugă reviewer_id, constatări, severitate, dovezi și verdict. Evenimentele se adaugă, iar corecțiile au legătură la evenimentul înlocuit; nu se șterg urmele unui rezultat eșuat.

Pentru o operație de conversie se propun stările PLANNED, RUNNING, CHECKPOINTED, VALIDATING, SUCCEEDED, FAILED, INTERRUPTED. Checkpointul include fișierele confirmate și etapa exactă următoare. O stare SUCCEEDED necesită citire de control și verificarea criteriilor, nu doar cod de ieșire zero.

În modul fără persistență, jurnalul produsului include doar tipul operației, timpi și coduri de eroare neidentificabile spațial. Documentarea dezvoltării rămâne completă prin fixtureuri sintetice și date de laborator autorizate.

## 9 Limite și întrebări deschise

Nu sunt încă alese dispozitivele exacte, ținta minimă de iOS, imprimantele, toleranțele comerciale, furnizorul DWG sau aplicațiile CAD destinatare. Sunt necesare spikeuri tehnice pentru exporturile iOS, bugetul de memorie al norilor mari și capabilitățile multiroom reale. Nu există în acest dosar măsurători pe iPhone, importuri efective în slicere sau imprimări fizice. Auditul documentar poate verifica acoperirea și coerența; nu poate declara produsul 100% validat.

Sursele complete, datele de acces și notele de evidență sunt în `../07_surse/cad_sources.json`. Fișierul `../00_management/cad_events.jsonl` consemnează cercetarea și verificarea documentară efectuate.



## 10 Surse primare accesibile

- [CAD-S01 3MF specifications](https://3mf.io/spec/) — consultat 2 octombrie 2026.
- [CAD-S02 PrusaSlicer supported file formats](https://help.prusa3d.com/article/supported-file-formats_1772) — consultat 2 octombrie 2026.
- [CAD-S03 3MF Core v1.3.0](https://3mf.io/wp-content/uploads/sites/106/2025/02/3MF_Core_Specification_v1.3.0.pdf) — consultat 2 octombrie 2026.
- [CAD-S04 UltiMaker supported files](https://ultimaker.com/3d-printers/s-series/ultimaker-secure/) — consultat 2 octombrie 2026.
- [CAD-S05 UltiMaker Digital Factory API](https://docs.api.ultimaker.com/faq/digital_factory.html) — consultat 2 octombrie 2026.
- [CAD-S06 ezdxf Introduction](https://ezdxf.readthedocs.io/en/stable/introduction.html) — consultat 2 octombrie 2026.
- [CAD-S07 ODA Drawings SDK](https://www.opendesign.com/products/drawings) — consultat 2 octombrie 2026.
- [CAD-S08 ODA Pricing](https://www.opendesign.com/pricing) — consultat 2 octombrie 2026.
- [CAD-S09 Autodesk RealDWG API](https://aps.autodesk.com/developer/overview/realdwg-api) — consultat 2 octombrie 2026.
- [CAD-S10 Fusion Convert Mesh](https://help.autodesk.com/cloudhelp/ENU/Fusion-Mesh/files/MESH-CONVERT-TO-SOLID.htm) — consultat 2 octombrie 2026.
- [CAD-S11 IfcOpenShell repository](https://github.com/IfcOpenShell/IfcOpenShell) — consultat 2 octombrie 2026.
- [CAD-S12 Open3D File IO](https://www.open3d.org/docs/latest/tutorial/geometry/file_io.html) — consultat 2 octombrie 2026.
- [CAD-S13 PDAL LAS writer](https://pdal.io/en/stable/stages/writers.las.html) — consultat 2 octombrie 2026.
- [CAD-S14 PDAL E57 writer](https://pdal.io/en/stable/stages/writers.e57.html) — consultat 2 octombrie 2026.
- [CAD-S15 Khronos glTF](https://www.khronos.org/gltf/) — consultat 2 octombrie 2026.
- [CAD-S16 OpenUSD USDZ specification](https://openusd.org/release/spec_usdz.html) — consultat 2 octombrie 2026.
- [CAD-S17 Open3D repository and license](https://github.com/isl-org/Open3D) — consultat 2 octombrie 2026.
- [CAD-S18 COLMAP license](https://github.com/colmap/colmap/blob/main/COPYING.txt) — consultat 2 octombrie 2026.
- [CAD-S19 PDAL license](https://raw.githubusercontent.com/PDAL/PDAL/master/LICENSE.txt) — consultat 2 octombrie 2026.
- [CAD-S20 ezdxf license](https://raw.githubusercontent.com/mozman/ezdxf/master/LICENSE) — consultat 2 octombrie 2026.
- [CAD-S21 lib3mf repository](https://github.com/3MFConsortium/lib3mf) — consultat 2 octombrie 2026.
- [CAD-S22 NIST AM part qualification](https://www.nist.gov/programs-projects/additive-manufacturing-part-qualification) — consultat 2 octombrie 2026.
- [CAD-S23 NIST AM test artifact](https://www.nist.gov/el/intelligent-systems-division-73500/production-systems-group/nist-additive-manufacturing-test) — consultat 2 octombrie 2026.
- [CAD-S24 Bambu Studio importer source](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/GUI_App.cpp) — consultat 2 octombrie 2026.
- [CAD-S25 JCGM GUM 100 2008](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf) — consultat 2 octombrie 2026.
- [CAD-S26 ASPRS LAS official repository](https://github.com/ASPRSorg/LAS) — consultat 2 octombrie 2026.
- [CAD-S27 Open3D MIT license](https://raw.githubusercontent.com/isl-org/Open3D/main/LICENSE) — consultat 2 octombrie 2026.
- [CAD-S28 lib3mf BSD-2-Clause license](https://raw.githubusercontent.com/3MFConsortium/lib3mf/master/LICENSE) — consultat 2 octombrie 2026.
- [CAD-S29 COLMAP repository](https://github.com/colmap/colmap) — consultat 2 octombrie 2026.
- [CAD-S30 ODA membership published 2026 pricing](https://www.opendesign.com/agreements/2026/en/ODA%20Membership%20%26%20Extension%20pricing.pdf) — consultat 2 octombrie 2026.
