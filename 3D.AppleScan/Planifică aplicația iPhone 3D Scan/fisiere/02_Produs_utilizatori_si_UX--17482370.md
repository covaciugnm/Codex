# 2 Produsul utilizatorii și experiența de folosire

## 2.1 Promisiunea produsului

Aplicația transformă observații ale mediului în rezultate utilizabile: obiecte cotate, dimensiuni pe imagine, modele de camere și poziții ale obiectelor. Fiecare rezultat arată originea datelor, unitatea, momentul și starea validării. Mesajul comercial trebuie să descrie aceste activități concret. Motto-ul creativ al campaniei nu reprezintă o afirmație metrologică.

Modul inițial de alegere folosește două întrebări: „Ce activitate ai?” și „Ce problemă vrei să rezolvi?”. Profilul profesional filtrează exemplele, fără a restricționa funcțiile. Un proprietar poate măsura aceeași deschidere ca un arhitect. După selecție, aplicația afișează rezultatul posibil, ce trebuie capturat și limitele hardware înainte de a cere un efort de scanare.

## 2.2 Activități și rezultate

| Profil | Problemă concretă | Flux | Rezultat propus | Verificare înainte de utilizare |
|---|---|---|---|---|
| Arhitect | Releveu pentru o intervenție | Camere, cote, verificări independente | Plan orientativ DXF și model spațial | Repere, goluri, grosimi neobservate, toleranțe |
| Designer | Încape mobilierul și rămâne circulație | Cameră plus obiect cotat | Amplasare cu gabarit și distanțe | Spațiu liber și dimensiuni critice măsurate separat |
| Meșter | Ce suprafețe și deschideri trebuie reparate | Live sau cameră salvată cu adnotări | Cote, arii estimate și fotografii explicite | Acces, obstacole, suprafețe ascunse |
| Maker | Copiere sau adaptare a unui obiect | Obiect plus scală și control plasă | 3MF/STL și raport geometric | Toleranțe, grosimi și profil imprimantă |
| Administrator imobil | Inventar și modificări în timp | Camere și catalog versionat | Obiecte localizate, observații și diferențe | Identități și schimbări confirmate |
| Creator | Obiect pentru prezentare sau scenă 3D | Captură, textură și simplificare | Model vizual și previzualizare | Drepturi asupra materialului și aspect |
| Integrator robotic | Harta și obiectele dintr-o zonă | Percepție continuă și ROS 2 | Fluxuri cu timp, cadru și calitate | Calibrare, prospețime, condiții operaționale |

Personajele de campanie ajută recunoașterea activității, dar nu sunt dovezi de testare cu profesioniști reali. Documentația de produs și site-ul trebuie să distingă imaginile promoționale de capturile efective ale aplicației.

## 2.3 Modul obiecte cu dimensiuni

Fluxul începe prin alegerea utilizării: previzualizare, cotare orientativă, printare sau urmărire 6D. Utilizatorul vede dacă dispozitivul permite captura aleasă. Aplicația verifică observabilitatea: rigiditatea obiectului, textură, reflexii, zone ascunse și mișcare. Lipsa LiDAR nu trebuie mascată prin afișarea aceleiași promisiuni de capabilitate.

În timpul capturii se arată acoperirea și instrucțiuni concrete pentru vederea lipsă. Progresul este o măsură a achiziției, nu un procent de „adevăr”. După reconstrucție, utilizatorul inspectează scara, axele, originea și gabaritul. O dimensiune introdusă pentru calibrare este marcată ca intrare și nu se reutilizează ca adevăr independent în testul aceleiași dimensiuni.

Editorul păstrează un original imutabil și o ramură procesată. Decimarea, umplerea găurilor și netezirea sunt operații reversibile care pot altera măsurarea. O gaură închisă automat primește proveniență de geometrie estimată. La export se explică ce păstrează formatul și ce pierde: culoare, unitate explicită, semantică, cote sau incertitudine.

## 2.4 Modul măsurare live fără salvare implicită

Acest mod pornește cu o sesiune temporară. Utilizatorul alege puncte, muchii ori suprafețe și vede cotele pe imagine. Datele brute, harta și identificatorii mediului nu intră implicit în baza persistentă, telemetrie sau cloud. Salvarea unei fotografii cotate este o acțiune distinctă, cu previzualizarea conținutului păstrat.

La întreruperea aplicației, modul poate solicita recaptură; nu se promite reluarea unei hărți care, prin contract, nu a fost păstrată. Cacheurile pe disc, rapoartele de crash și miniaturile sunt incluse în auditul confidențialității. Un jurnal poate reține codul unei erori fără a include imaginea ori geometria locuinței.

O cotă cu tracking insuficient se marchează indisponibilă sau orientativă. Culoarea nu este singurul indicator: textul și simbolul rămân accesibile. Utilizatorul primește o acțiune utilă, precum „revino la zona deja observată”, fără explicații despre cozi GPU în interfața obișnuită.

## 2.5 Modul camere apartamente și case

Proiectul are clădire, nivel, cameră și sesiune, cu transformări explicite. Camerele se capturează progresiv, păstrând suprapuneri și repere. Apple documentează reunirea capturilor RoomPlan într-un CapturedStructure; continuitatea sau relocalizarea reperului comun trebuie gestionată de aplicație. Aceasta nu dovedește automat acuratețe cadastrală ori recuperarea oricărei sesiuni. [Apple RoomPlan](https://developer.apple.com/documentation/roomplan/scanning-the-rooms-of-a-single-structure)

După unire, interfața afișează neconcordanțele dintre camere: pereți dublați, goluri nepotrivite, suprapuneri și diferențe de nivel. Utilizatorul poate marca o zonă pentru recaptură sau introduce o referință verificată. Sistemul nu transformă automat orice colț în 90° doar pentru a obține un plan atrăgător.

Pentru reparații, adnotările se atașează unei suprafețe și unei versiuni de geometrie. Dacă geometria se schimbă, aplicația cere reconciliere când atașarea nu mai este sigură. Cantitățile de materiale sunt estimări care disting suprafața observată de cea inferată și permit pierderi tehnologice introduse de utilizator.

## 2.6 Persoane și obiecte deformabile

Capturarea persoanelor este o extensie cu consimțământ și protocol propriu. Un corp în mișcare nu este obiect rigid; un singur transform SE(3) nu descrie schimbarea posturii. Portretele și avatarurile nu sunt promovate ca măsurători medicale sau antropometrie calificată. Fața, hainele și textura pot constitui informații personale; scopul și durata păstrării trebuie explicate separat.

Pentru obiecte deformabile, catalogul poate păstra gabarit, clasă și segmente urmărite, dar nu promite o orientare rigidă unică. Dacă modelul nu se aplică, UI și API emit starea neadecvată, fără a fabrica șase coordonate cu precizie aparentă.

## 2.7 Catalogul spațial și vizualizarea incertitudinii

Fiecare obiect are ID de instanță, clasă, model de referință opțional, gabarit, poziție, orientare, momentul ultimei observații și stare. „Observat”, „prezis”, „pierdut” și „neconfirmat” au înțelesuri distincte. O masă mutată în afara câmpului vizual nu poate primi poziție actuală doar fiindcă modelul a rămas în hartă.

Utilizatorul poate defini o listă de obiecte importante sau o zonă. Aceste preferințe influențează prioritizarea procesării, cu afișarea acoperirii efective. Un contur 2D, o cutie 3D și un model aliniat sunt reprezentări diferite, accesibile în funcție de calitatea disponibilă. Aplicația nu afișează în mod implicit toate straturile simultan.

## 2.8 Accesibilitate și localizare

Limbile țintă sunt română, engleză, germană, franceză, spaniolă, maghiară și bulgară. Textele provin din chei comune; unitățile, separatorul zecimal și pluralizarea se formatează pentru limbă. Valoarea numerică stocată rămâne în unitatea canonică. Schimbarea limbii nu recreează scanarea și nu pierde selecția problemei.

Pentru site folosim WCAG 2.2 drept reper de evaluare a contrastului, navigării, focusului și etichetării. Conformitatea nu se deduce din existența unui selector de limbă. Pentru aplicația nativă se verifică separat VoiceOver, dimensiunea textului și alternativele la instrucțiuni exclusiv vizuale. [WCAG 2.2](https://www.w3.org/TR/WCAG22/)

## 2.9 Validare cu utilizatori

Se propun 15 interviuri exploratorii și 5 sesiuni formative, urmate de 20 participanți diferiți pentru acceptare. Fiecare primește o activitate, nu numele funcției dorite. Se măsoară alegerea modului, prima captură și export, interpretarea stărilor și recuperarea din erori. 18/20 trebuie să aleagă modul în cel mult 10 secunde; 16/20 să finalizeze captura și exportul fără ajutor; 18/20 să interpreteze corect stările. Aceste praguri sunt propuse și nu implică generalizare statistică la întreaga piață.

Auditorul UX verifică și cazurile de abandon. O sarcină încheiată cu ajutorul moderatorului nu este reclasificată drept succes autonom. Rezultatele sunt stratificate după familiaritatea cu scanarea și nevoile de accesibilitate; participanții din etapa formativă nu se amestecă în lotul de acceptare.
