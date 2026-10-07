# EVA-3dScan — brief de redesign orientat spre utilizator

Data: 2 octombrie 2026. Responsabil: agentul `redesign_manager`. Solicitare: utilizatorul consideră site-ul prea slab și cere contribuții distincte de management, marketing de aplicații, arhitectură, design interior și meserii. Acest document stabilește obiectivele și acceptarea; nu constituie o validare cu utilizatori reali.

## Decizia de produs

**Specificația finală — 2 octombrie 2026:** după orientarea spre clienți și activități, utilizatorul a precizat ordinea dorită: „tipurile de clienți ... și dedesubt selector cu problema ... să găsească oricine ce caută”. Prima pagină folosește două selectoare verticale: **cine ești → ce problemă vrei să rezolvi**. Primul are șase profiluri și opțiunea „Proiect personal / altă activitate”; al doilea filtrează cele 36 de utilizări. Cele șase povești profesie–activitate urmează înaintea celor trei module. Aceasta înlocuiește varianta intermediară cu șase activități ca alegeri principale în hero.

Prima pagină trebuie să explice, înaintea oricărei documentații tehnice:

1. **Ce este:** o aplicație pentru iPhone, aflată în dezvoltare.
2. **Ce rezolvă:** transformă capturi ale obiectelor și spațiilor în informații utile pentru lucru.
3. **Unde mă regăsesc:** aleg profilul sau proiectul personal, apoi problema concretă din catalogul relevant.
4. **Ce primesc:** văd rezultatul relevant activității, apoi funcțiile care îl susțin: obiecte cu dimensiuni, cote live temporare sau proiect de camere salvate.
5. **Ce pot face acum pe site:** să explorez o demonstrație conceptuală și exemplele de utilizare.

Păstrăm siglele, paleta de culori și personajele aprobate. Schimbarea principală este ierarhia explicației și a dovezii vizuale. Personajul arată cine folosește produsul; ecranul de telefon și rezultatul trebuie să arate ce obține.

## Diagnostic al versiunii inspectate

Fișiere analizate: `public/app.js`, `public/campaign.css`, `public/discovery.css`, `content/locales/ro.json`, `docs/UTILIZARI_CERCETARE.md`, `docs/AUDIT_UTILIZARI_SEO.md`.

- Titlul spune deja că produsul este o aplicație pentru iPhone. Problema nu se rezolvă prin repetarea acestei propoziții în alte cinci locuri.
- Caruselul prezintă oameni și scene, dar nu demonstrează clar diferența dintre o fotografie, o măsurătoare și un rezultat reutilizabil.
- Cele trei module apar după hero și folosesc explicații generale. Vizitatorul trebuie să lege singur modulul de problema sa.
- Fluxul „intrare–proces–ieșire” este comun și abstract. Pentru un zugrav contează peretele și suprafața; pentru un arhitect, geometria și cotele; pentru un designer, încăperea și mobila existentă.
- Publicurile sunt enumerate, dar nu au un traseu cu rezultat și următor pas. Un nume de profesie și o pictogramă nu explică utilitatea.
- Catalogul cu 36 de utilizări este valoros pentru explorare și căutare, însă nu trebuie să devină sarcina inițială a vizitatorului.
- Pagini de modul încep cu formulări poetice sau tehnice: „Forma este doar începutul”, „rețea poligonală verificabilă”, „unire reversibilă”. Aceste concepte pot rămâne în explicațiile detaliate după prezentarea rezultatului.
- „Planificat”, „concept”, „verificare”, „limite” apar repetat. Statutul trebuie păstrat clar, cu limitele specifice lângă rezultatul relevant, fără să înlocuiască explicația utilității.
- Butonul către documentație domină prea devreme. Citirea unui dosar nu este primul pas firesc pentru cine evaluează o aplicație.

## Ierarhia propusă pentru prima pagină

### 1. Hero: produsul și o probă vizuală

Titlu editorial propus: **„Din realitate, în dimensiuni și modele 3D.”**

Subtitlu: **„EVA-3dScan este aplicația pentru iPhone concepută pentru obiecte cu dimensiuni, măsurători pe loc și camere reunite în planul locuinței.”**

Textul final poate fi mai scurt, dar trebuie să numească explicit iPhone și cele trei activități. Un badge vizibil spune „Aplicație în dezvoltare”.

- Două selectoare verticale cu etichete explicite: „Cine ești?” și, dedesubt, „Ce problemă vrei să rezolvi?”. Opțiunea pentru proiect personal permite accesul la toate cele 36 de probleme. Alegerea actualizează explicația, scena și modulul relevant.
- Un singur CTA primar: **„Vezi ce obții”**, care duce la traseul activității selectate pe aceeași pagină.
- Un CTA secundar poate deschide catalogul complet de utilizări.
- Fără „Descarcă aplicația”, buton App Store, timp de scanare sau precizie numerică până există dovadă.
- Imaginea arhitectului rămâne scena inițială. Un telefon ilustrativ, o piesă cotată sau un rezultat de cameră face vizibilă legătura dintre scenă și produs.
- Numerele dintr-un exemplu trebuie marcate ca date demonstrative. Nu sugerăm că au fost măsurate în fotografia generată.

### 2. Profilul meu și problema mea — alegerile principale

Primul selector oferă arhitect, designer, meșter, creator 3D/atelier, agent/proprietar/administrator și artă/educație/patrimoniu, plus proiect personal/altă activitate. Al doilea selector propune problemele relevante, grupate pe categorii. Oricine poate alege proiectul personal pentru acces la toate cele 36 de utilizări. Schimbarea profilului înlocuiește o problemă nepotrivită cu un exemplu valid. Profilul ajută orientarea fără a impune o profesie obligatorie.

Cele șase povești de mai jos dezvoltă relația profil–activitate. Ele apar după răspunsul la problema aleasă, înaintea modulelor:

| Activitate principală | Situația în care se recunoaște clientul | Rezultatul de explicat | Exemple secundare de clienți |
|---|---|---|---|
| Proiectez un spațiu | Încep de la o clădire sau cameră existentă | referință dimensională a spațiului și legăturii dintre camere | arhitect, proiectant, proprietar |
| Amenajez un interior | Vreau să verific mobila și amplasarea | camera și dimensiunile relevante pentru propunerea de amenajare | designer, proprietar, atelier de mobilier |
| Renovez sau repar | Trebuie să înțeleg zona lucrării | cote și observații manuale contextualizate pentru discuția despre lucrare | meșter, echipă de renovare, beneficiar |
| Creez un obiect 3D | Vreau o referință pentru modelare sau imprimare | model de obiect cu dimensiuni, care necesită verificare și pregătire | maker, artist, proiectant de produs, atelier |
| Prezint o proprietate | Vreau să explic spațiul unei persoane aflate la distanță | reprezentare spațială demonstrativă pentru prezentare | agent imobiliar, proprietar, administrator |
| Digitizez persoane sau obiecte | Vreau să păstrez ori să folosesc creativ o formă reală | referință 3D pentru portret, colecție sau creație | creator, familie, educator, muzeu |

Nu promovăm automat vizionare imobiliară completă, evaluare de proprietate, avatar animat sau imprimare gata de producție. Fiecare activitate trebuie să reflecte starea reală a funcțiilor planificate.

### 3. Răspunsul la problema selectată — imediat după hero

Secțiunea de rezultat afișează titlul și explicația problemei alese, plus un CTA către modulul potrivit. Urmează cele șase povești de client: **situația → trei pași → rezultat util → exemplu și următor pas disponibil**. Imaginea și diagrama ilustrează povestea. Profesia și activitatea sunt prezentate împreună.

Răspunsul principal trebuie să corespundă exact problemei alese. Povestea profesională oferă context mai larg pentru profil și nu este prezentată drept rezultat măsurat al cazului selectat. Cele șase activități au explicații și linkuri distincte. Mai multe probleme pot folosi același modul, dar rezultatul ales este explicat prin titlul și descrierea din catalog.

### 4. Trei funcții care susțin activitățile

După ce clientul vede ce poate obține, cele trei module explică mecanismul. Ele rămân accesibile și din navigație:

| Mod | Ce captez | Ce rezultat explicăm | Ce fac mai departe |
|---|---|---|---|
| Obiecte | un obiect și cote de control | model 3D cu dimensiuni și verificarea scării | referință pentru proiectare sau pregătire pentru imprimare |
| Măsurători | puncte pe un perete ori într-un gol | cote suprapuse imaginii, temporare implicit | verific orientativ spațiul; aleg explicit dacă salvez imaginea |
| Camere | încăperea, apoi camerele alăturate | model/plan și camere organizate într-un proiect | amenajare, documentare sau pregătirea renovării |

Fiecare mod are: un titlu de maximum șapte cuvinte, o propoziție despre rezultat, maximum trei pași și un link spre pagina sa. Dacă există un carusel suplimentar, acesta rămâne o galerie, nu singurul loc care explică funcțiile.

#### Contribuțiile profesionale susțin traseele

Rapoartele arhitectului, designerului și meșterului rămân surse pentru activitățile de proiectare, amenajare și renovare. Selectorul principal include și creația 3D, imobiliarele, educația/patrimoniul și un proiect personal. Documentul `CUSTOMER_FOCUS.md` și `content/customer-segments.json` detaliază mesajele celor șapte limbi.

| Public | Întrebarea de pornire | Exemplu de traseu | Ce trebuie arătat |
|---|---|---|---|
| Arhitect | „Pot porni releveul de aici și verifica ce preiau în proiect?” | cameră → cote de control → referință pentru proiectare | camere conectate, unități, verificări și statut separat pentru CAD/DWG |
| Designer | „Pot înțelege spațiul clientului și verifica dacă încape mobilierul?” | cameră existentă → model și dimensiuni → variantă de amenajare într-un instrument compatibil | spațiul existent, obiectul relevant, dimensiunea și ce poate fi comunicat clientului |
| Meșter | „Ce măsor, ce am de reparat și ce trimit pentru ofertă?” | perete → cote și note manuale → referință pentru lucrare | lățime/înălțime, eventual arie explicată, poziția observațiilor, salvare explicită |

Acestea sunt ipoteze profesionale pentru analiza agenților. Nu sunt citate sau rezultate ale unor interviuri efectuate.

### 5. Design nou și reparații, explicate separat

- Designerul și cuplul: înțelegerea camerei, mobila existentă, discuția despre o amenajare nouă.
- Maistrul și cuplul: observații introduse manual, zone de intervenție și referințe pentru ofertare.
- Nu sugerăm detecție automată de fisuri, probleme ascunse, calcul automat de deviz sau generare automată de design dacă acestea nu sunt implementate.
- Persoanele rămân un scenariu creativ distinct; se păstrează imaginea tinerei și a tânărului. Nu devin o a patra funcție principală în navigația celor trei module.

### 6. Ce este disponibil și ce urmează

O zonă scurtă răspunde la întrebările care blochează evaluarea:

- **Pot instala acum?** Stadiul real al aplicației și lipsa unei lansări confirmate.
- **Ce iPhone îmi trebuie?** Compatibilitatea depinde de funcție și de dispozitiv; legătură către explicația tehnică actualizată. Nu reducem toate funcțiile la „iPhone + LiDAR”.
- **Cât de precise sunt măsurătorile?** Nicio precizie numerică promisă fără teste; utilizări și cote de control explicate.
- **Pot exporta?** Formate planificate și conversii condiționate, înțelese în funcție de utilizare.
- **Se salvează camera automat?** Distincția dintre măsurarea temporară și proiectul de camere salvat.

### 7. Inspirație și detaliu

Catalogul celor 36 de utilizări, documentația, sursele, formatele și ecosistemul EVA rămân accesibile prin linkuri clare. Home prezintă câteva cazuri prioritare, nu toate detaliile.

## Obiective măsurabile și criterii de acceptare

| ID | Obiectiv | Criteriu verificabil | Probă așteptată |
|---|---|---|---|
| V2-01 | Recunoașterea produsului | primul ecran conține numele, „aplicație”, „iPhone”, statutul și un CTA executabil | captură desktop și mobil; inspecție DOM |
| V2-02 | Recunoașterea nevoii | profilul apare deasupra problemei; 6 profiluri + proiect personal; probleme compatibile, cu toate cele 36 accesibile prin proiect personal | inspecție pentru 7 profiluri, 36 probleme și 7 limbi |
| V2-03 | Rezultat tangibil | fiecare activitate include un rezultat ilustrat, nu doar un personaj sau o pictogramă | 6 capturi/stări și etichetă de demonstrație |
| V2-04 | Relevanță pentru client | 6 trasee diferite cu situație, 3 pași, rezultat și link util; profesiile sunt exemple secundare | matrice de conținut și verificarea linkurilor |
| V2-05 | Statut corect | zero afirmații inventate despre disponibilitate, precizie, viteză sau funcții automate | audit de conținut; lista afirmațiilor |
| V2-06 | Identitate păstrată | logo, paletă și cele 5 scene aprobate rămân accesibile în paginile potrivite | comparație de resurse și inspecție vizuală |
| V2-07 | Interacțiuni clare | CTA primar și selectoare funcționale cu mouse, tastatură și pe mobil; fără controale decorative | test browser pentru click, Tab, Enter și stări active |
| V2-08 | Accesibilitate vizuală | fără overflow orizontal la 390 px și 1440 px; focus vizibil; reduced-motion respectat | capturi și teste automate dedicate |
| V2-09 | Localizare | aceleași chei în cele 7 limbi; zero chei brute afișate; titlul și acțiunile nu sunt tăiate | test de randare × 7 limbi |
| V2-10 | SEO și funcții conservate | SSR, metadata, navigația, catalogul, auth/proiecte și app_i18n continuă să funcționeze | teste relevante de regresie; fără rescrierea componentelor fără legătură |
| V2-11 | Continuitate | fiecare etapă are intrări, fișiere, rezultat și stare; constatările au responsabil și rezoluție | loguri și raport final cu trimiteri |
| V2-12 | Coerența alegerii | profilul și problema rămân valide; răspunsul și CTA corespund problemei; modulul ilustrat se sincronizează; alegerile persistă la schimbarea limbii și refresh | test pentru 7 profiluri, toate problemele, schimbare limbă și eveniment de conținut |

Ținta de cercetare pentru o etapă ulterioară: după o expunere de cinci secunde, cel puțin patru din cinci participanți fără context să poată spune „aplicație iPhone” și să identifice o activitate proprie; după o explorare de două minute, fiecare să poată explica rezultatul activității alese. Participanții trebuie să includă și clienți neprofesioniști. Această țintă **nu este un test executat** și nu poate fi înlocuită cu opinia agenților.

## Echipa și livrabilele ei

| Rol | Sarcină | Rezultat obligatoriu | Condiție de închidere |
|---|---|---|---|
| Manager | ierarhia informației, priorități, alinierea cerințelor | acest brief, criterii, log și decizie de livrare | fiecare V2-01–V2-12 are probă ori limită explicită |
| Marketing de aplicații | mesaj central, rezultat promis, CTA și obiecții | hero, microtexte, CTA și argumente susținute | textele răspund la „ce obțin?”; nu inventează disponibilitate |
| Arhitect | inspectarea traseului de releveu și proiectare | 5 întrebări prioritare și ordinea răspunsurilor | cote, scară, proiect, export și control explicate |
| Designer | inspectarea traseului pentru amenajare și client | 5 întrebări prioritare și o poveste de folosire | spațiul existent, mobila, variantele și predarea explicate |
| Meșter | inspectarea măsurării și documentării reparațiilor | 5 întrebări prioritare și un traseu de lucrare | perete, cote, note, salvare și ofertare explicate |
| Implementare | transformarea concluziilor în interfață | pagini, texte localizate și interacțiuni | criteriile funcționale și vizuale verificate |
| Audit | verificarea rezultatului față de brief | constatări cu gravitate, dovadă, remediere și stare | zero probleme majore rămase; limitările raportate clar |

Rolurile de arhitect, designer și meșter sunt perspective simulate de agenți. Nu prezentăm această colaborare drept certificare profesională sau studiu cu utilizatori reali. Cu patru locuri de lucru simultane, rolurile se pot executa în două valuri fără a combina concluziile într-o singură opinie.

## Ordine de lucru și reluare

1. **Brief și diagnoză:** salvează documentul; semnalează managerului cele trei priorități. Stare manager: finalizat.
2. **Perspective profesionale și marketing:** fiecare rol livrează un fișier separat; managerul unește cerințele, marchează contradicțiile și decide ordinea.
3. **Structură și exemplar în română:** aprobare internă prin criterii, fără a cere utilizatorului repetarea autorizării.
4. **Implementare și traduceri:** modificări limitate la interfața și conținutul relevante; verificarea schimbărilor paralele înainte de livrare.
5. **Teste și audit:** execută probele din tabel; orice constatare indică fișierul, responsabilul și criteriul afectat.
6. **Remediere și livrare:** reverifică zonele modificate; salvează capturi, rezultat și limite. Nu declara audit de 100% sau calitate absolută.

Pentru reluare se citesc mai întâi acest brief, `redesign-v2-manager.jsonl` și rapoartele rolurilor. Logul managerului descrie numai activitatea executată de manager; integrarea și testele au propriile rezultate. La întrerupere se notează ultimul pas închis și următorul pas concret, fără a echivala un plan cu o implementare.

La revizia din 13:54 UTC, agentul principal raportează corectarea celor patru constatări QA ale variantei pe profesii și 52 de verificări V2 trecute în browserul remote. Aceste rezultate aparțin variantei anterioare orientării pe șase activități; nu validează automat noua structură. Urmează inspectarea implementării pe activități și reverificarea zonelor schimbate.

**Actualizare finală:** structura cu două selectoare a fost inspectată de managerul QA. Agentul principal raportează 308 verificări pentru selecția client–problemă și 73 pentru povestea produsului, toate trecute, plus regresiile generale. Dovezile și atribuirea verificărilor sunt consemnate în `AUDIT_REDESIGN_V2.md`; acestea nu reprezintă testarea înțelegerii cu clienți reali.
