# Specificația aplicației iPhone pentru scanare și măsurare 3D

Versiune de proiectare 1.0, 2 octombrie 2026. Autor coordonator: managerul echipei de agenți. Destinatar: proprietarul produsului și viitoarea echipă de dezvoltare. Numele de lucru este EVA 3D Scan; numele comercial rămâne de decis.

## 1 Scop și statut

Aplicația propusă transformă un iPhone compatibil într-un instrument de captură, măsurare orientativă, documentare spațială și pregătire de modele pentru alte programe. Are trei intrări clare: **Obiecte cu dimensiuni**, **Măsoară acum** și **Camere și clădiri**. Toate valorile numerice de performanță din această specificație sunt ținte propuse, nu rezultate măsurate. Nu există încă o aplicație implementată, un test clinic sau industrial, ori o validare experimentală.

Dosarul oferă o structură și o metodologie potrivite pentru o cercetare doctorală aplicată. Nu reprezintă o teză doctorală finalizată: contribuția originală, experimentele, rezultatele și validarea academică trebuie realizate ulterior. Cercetarea publică este o selecție documentată, nu o inventariere exhaustivă a întregului internet.

Obiectivul principal este să păstrăm legătura dintre geometrie, dimensiuni, condițiile capturii și dovezile calității. Un model care arată bine poate avea dimensiuni greșite. Un fișier care se deschide în CAD poate să nu conțină cote sau obiecte parametrice. Aceste situații trebuie făcute vizibile utilizatorului.

## 2 Utilizatori și activități

| Utilizator | Activitatea prioritară | Rezultatul util |
|---|---|---|
| Persoană care amenajează locuința | Măsoară un gol, mobilierul și camera | Imagine cotată sau plan verificabil |
| Pasionat de imprimare 3D | Scanează un obiect și îl reproduce | Mesh cu unități, scară și raport de reparare |
| Arhitect sau proiectant | Documentează camere și le unește | Plan editabil, referințe și export CAD condiționat |
| Tehnician de teren | Înregistrează o stare existentă | Nor de puncte, fotografie, metadate și jurnal |
| Cercetător | Compară metode și repetări | Date cu versiuni, condiții și protocol reproductibil |

Aplicația nu trebuie promovată ca substitut garantat al unui instrument metrologic calibrat, al unui releveu autorizat ori al proiectării unei piese critice. Aceasta este o limită de poziționare a produsului, nu o interdicție asupra cercetării sau utilizării orientative.

## 3 Modulul Obiecte cu dimensiuni

### Captură

Utilizatorul alege destinația: vizualizare, măsurare sau imprimare. Sistemul detectează capabilitățile telefonului și explică metoda disponibilă. O captură rapidă cu adâncime și o reconstrucție fotogrammetrică pot avea calități diferite. Metoda, dispozitivul și versiunea procesării sunt înregistrate în proiect.

Asistentul de captură explică iluminarea difuză, acoperirea din mai multe unghiuri, suprafețele lucioase, transparente ori uniforme și riscul mișcării obiectului. Indicatorul de acoperire trebuie să evidențieze zonele lipsă. Numărul de imagini și timpul estimat sunt adaptate capabilităților detectate; nu sunt hardcodate ca promisiune pentru orice telefon.

### Scară și cotare

Modelul păstrează unitatea internă metrul. Dimensiunile afișate se aleg în mm, cm, m sau inch, cu unitatea lângă valoare. Sistemul păstrează separat scara inițială și scara corectată folosind o lungime de referință. Referința nu trebuie să fie aceeași dimensiune folosită ca dovadă independentă a preciziei.

Utilizatorul poate selecta două puncte, o muchie sau un plan; poate obține lungime, cutie de încadrare orientată, diametru estimat, unghi și distanță între plane. Circumferințele și volumele sunt funcții ulterioare, condiționate de geometrie suficientă. Un volum al unui mesh deschis este refuzat sau etichetat ca estimare după reparare.

Fiecare cotă include metoda, punctele/elementele de sprijin, unitatea, versiunea geometriei, eventuala corecție manuală și starea de încredere. Înainte de validarea statistică a unui model de incertitudine se afișează o stare calitativă, fără un interval numeric inventat.

### Editare și livrare

Operațiile crop, eliminare suport, reducere număr triunghiuri, netezire, umplere goluri, orientare și rescalare generează versiuni derivate. Se păstrează originalul. Modificările care pot altera geometria prezintă o comparație și invalidează cotele afectate. Umplerea unui gol reprezintă geometrie inferată, identificată distinct.

Exportul oferă pachete după scop. Pentru imprimare: 3MF/STL validate și raport de scară. Pentru schimb de geometrie și texturi: OBJ, glTF/GLB sau USDZ, după implementarea adaptoarelor. Pentru cercetare: PLY/XYZ și metadate. Disponibilitatea este stabilită de matricea din capitolul CAD; niciun format nu este declarat implementat în această etapă.

## 4 Modulul Măsoară acum

Camera afișează distanțe și cote peste imaginea live. Utilizatorul selectează puncte, muchii sau suprafețe; poate muta ancorele și modifica unitățile. La pierderea urmăririi, cota se marchează ca instabilă și nu se prezintă drept măsurare actualizată.

**Contract de confidențialitate:** modul implicit nu salvează fotografii, video, hărți AR, nor de puncte, mesh, miniaturi sau proiect. Datele necesare sesiunii există temporar în memorie. Jurnalele tehnice ale aplicației nu conțin imagini, coordonate, adrese sau valori ale măsurătorilor în acest mod. Ecranul din comutatorul de aplicații se maschează la trecerea în fundal. Ștergerea RAM și comportamentul capturilor de ecran făcute de sistem trebuie evaluate realist; aplicația nu poate garanta control absolut asupra telefonului.

Butonul separat **Salvează imagine cotată** permite utilizatorului să păstreze explicit o fotografie cu suprapunerea cotelor, fără a crea un proiect 3D. Înainte de salvare se afișează destinația, imaginea și faptul că poza va persista. Refuzul sau anularea păstrează comportamentul temporar. Această opțiune rezolvă cererea de cote pe imagini fără a face salvarea mediului obligatorie.

Nu există recuperare a unei sesiuni temporare după închiderea procesului. Reluarea fidelă a documentației și a proiectelor salvate nu trebuie confundată cu păstrarea datelor în modul fără salvare.

## 5 Modulul Camere și clădiri

Entitățile sunt proiect, clădire, nivel, unitate/apartament, cameră, suprafață, deschidere și obiect detectat. Un proiect poate conține o casă, mai multe niveluri și camere cu podele la cote diferite. Capabilitățile exacte RoomPlan și traseul de captură sunt descrise de specialistul Apple; compatibilitatea multi-etaj se validează pe SDK și dispozitiv.

Fluxul începe cu camera individuală. Utilizatorul verifică pereți, ferestre, uși și zone omise, apoi salvează camera. Următoarea cameră folosește repere comune, de exemplu o ușă. Aplicația încearcă alinierea și afișează suprapunerea, erorile și conflictele. Utilizatorul poate corecta sau respinge rezultatul. Fuziunea nu șterge camerele inițiale.

Planul 2D permite editarea numelor, a tipurilor de camere, corectarea lungimilor cu o măsură de control, adăugarea notelor și alegerea cotelor care intră în raport. O corecție manuală nu devine automat observație măsurată. Modificarea unui perete poate afecta suprafața, camera vecină și exportul; aceste dependențe trebuie invalidate și recalculate.

Scările, tavanele înclinate, pereții curbi, spațiile deschise, exteriorul și fațadele sunt extinderi cu cercetare proprie. Prima versiune trebuie să explice ce este aproximat și să ofere o captură de referință. Nu se inventează grosimea unui perete invizibil și nu se deduce certificarea energetică ori structura portantă din aspect.

## 6 Date și interoperabilitate

Fiecare proiect salvat include un manifest cu identificator stabil, versiune de schemă, mod, unitate, sistem de axe, transformări, dispozitiv, OS/SDK, momentele capturii, lista fișierelor și hashuri. Fotografiile, adâncimea, geometria, cotele și exporturile au politici de retenție separate. Un proiect rămâne utilizabil fără abonament pentru citirea datelor locale și pentru exporturile deja generate, dacă modelul comercial permite aceasta; condiția trebuie stabilită înainte de publicare.

Datele interne pot include informație pe care formatul extern nu o suportă. Fiecare export enumeră pierderile: unități implicite, texturi absente, cote neexportate, clasă semantică pierdută sau transformări aplicate. Un raport JSON lateral poate păstra proveniența, fără a pretinde că programul destinatar îl citește automat.

## 7 Cerințe de sistem și priorități

**P0 pentru lansarea controlată:** trei intrări UX distincte; obiect cu scară și cote; măsurare temporară; cameră salvată; unire verificabilă de camere; unități corecte; export minim testat (3MF, STL, PLY, USDZ, DXF 2D cotat și manifest JSON); proiecte recuperabile; erori clare; captură offline; ștergere; accesibilitate de bază.

**P1 după validarea nucleului:** editor și rapoarte 2D avansate; loturi de export; adaptoare point cloud suplimentare; procesare Mac opțională; organizare avansată a bibliotecii de proiecte; extinderea compatibilității la alte slicere și programe CAD; rapoarte comparate între versiuni; DWG prin convertor licențiat dacă este validat. Planul DXF cotat și verificarea importului pentru exporturile minime sunt deja cerințe P0.

**P2 de cercetare:** mai multe etaje robuste, IFC semantic, reconstrucție de suprafețe CAD, texturi avansate, vizualizare neurală, colaborare cu sincronizare și reconcilieri. O funcție P2 devine P1/P0 doar prin decizie documentată cu cost, test și dependențe.

Prioritizarea folosește scorul propus `3 × utilitate + 3 × reducerea riscului + 2 × frecvența estimată − 2 × efort − dependențe`, pe scări 1–5. Frecvența estimată nu este dedusă din numărul unor postări găsite. Ea trebuie validată prin interviuri și telemetrie agregată permisă.

## 8 Cerințe operaționale cuantificabile

| ID | Cerință propusă | Criteriu de acceptare | Verificare |
|---|---|---|---|
| REQ-001 | Cele trei moduri au intrări distincte | 18 din 20 participanți aleg corect modul în sub 10 s | UX-EXP |
| REQ-002 | Dimensiuni la fiecare obiect exportat | 100% exporturi de probă au unitate și scară verificabile | EXPORT-EXP |
| REQ-003 | Referință de scară trasabilă în proiect | 30/30 rescalări păstrează originalul și valoarea introdusă | SCALE-EXP |
| REQ-004 | Măsurare temporară | 0 fișiere media/geometrie și 0 uploaduri în 50 sesiuni auditate | PRIV-EXP |
| REQ-005 | Poză cotată numai la cerere | 20/20 anulări nu creează imagine; 20/20 confirmări creează exact una | PRIV-EXP |
| REQ-006 | Camere individuale persistente | 30/30 camere salvate pot fi redeschise cu aceleași hashuri ale surselor | RESUME-EXP |
| REQ-007 | Combinare camere reversibilă | 10 proiecte cu 3–8 camere păstrează toate sursele și istoricul transformărilor | ROOM-EXP |
| REQ-008 | Schimbare unități fără scară greșită | 100/100 conversii m/mm/inch în limita toleranței numerice declarate | EXPORT-EXP |
| REQ-009 | Exportul eronat nu apare complet | 50 întreruperi ale exportului nu lasă fișier final marcat valid | RESUME-EXP |
| REQ-010 | Incertitudinea nu este inventată | 100% cote au stare calitativă sau interval cu metodă validată | METRO-EXP |
| REQ-011 | Geometria completată este vizibilă | 20/20 reparații marchează fețele inferate și invalidează cotele afectate | MESH-EXP |
| REQ-012 | Lucru de bază fără internet | Toate fluxurile P0 locale trec în mod avion pe dispozitivele suportate | OFFLINE-EXP |
| REQ-013 | Accesibilitate | 100% controale esențiale etichetate; 0 blocaje în fluxurile VoiceOver alese | UX-EXP |
| REQ-014 | Salvare recuperabilă | Zero pierdere de date confirmate; ≤5 s numai metadate/fluxuri persistente controlate de aplicație; stări opace RoomPlan/Object Capture best effort cu recaptură posibilă | RESUME-EXP |
| REQ-015 | Ștergere proiect și derivate | 30/30 proiecte dispar din stocarea gestionată și coada de procesare | PRIV-EXP |
| REQ-016 | Scară corectă în imprimare | Fiecare fixture digital are dimensiuni corecte în minimum două slicere | PRINT-EXP |
| REQ-017 | Cost transparent înainte de conversie | 100% operații cu cost cer o alegere explicită înainte de încărcare/plată | UX-EXP |
| REQ-018 | Temperatură și memorie | 0 crash în 30 sesiuni de 15 min pe dispozitiv minim; degradare explicată | PERF-EXP |
| REQ-019 | Compatibilitate determinată în execuție | 100% combinații testate afișează numai metodele suportate | DEVICE-EXP |
| REQ-020 | Audit de livrare | 0 defecte P0/P1 deschise pentru funcțiile declarate disponibile | RELEASE-EXP |

Aceste teste sunt planificate. Valorile de metrologie sunt stabilite în protocolul specialistului CAD, pe clase de obiecte și distanțe. Nu se extrapolează un singur procent la obiecte, camere, exterior și print.

## 9 Livrări și decizii rămase

Prima livrare este acest dosar. Următoarea este o probă tehnică executabilă pe iPhone real care demonstrează captură, scară, cotare, cameră și export minimal. Numai după măsurarea acelei probe se fixează compatibilitatea comercială și bugetul precis.

Proprietarul produsului va stabili dispozitivele disponibile, toleranțele relevante, bugetul, politica de cloud, modelul comercial și programele CAD prioritare. Aceste alegeri nu împiedică redactarea actuală; sunt dependențe ale implementării și ale promisiunilor comerciale.

## 10 Legături cu capitolele de specialitate

Capitolul din `01_cercetare` fundamentează UX prin concurenți și feedback. Capitolul din `03_arhitectura` fundamentează capabilitățile Apple. Capitolul din `04_cad_printare` definește formatele și metrologia. Registrul `07_surse` păstrează sursele, iar `08_audit` consemnează verificările. Cerințele de mai sus sunt decizii de proiectare ale echipei, nu funcționalități afirmate ale unui produs deja construit.


## Referința normativă pentru acceptare

[CRITERII_CANONICE.md](../05_validare/CRITERII_CANONICE.md) fixează pragurile, domeniile, eșantioanele și prioritățile după audit. Acesta este documentul de referință când un experiment exploratoriu folosește un lot mai mare sau un domeniu mai larg.
