# Utilizări propuse pentru EVA-3dScan și direcții de căutare

Cercetare pentru echipa EVA, consultată la 2 octombrie 2026. Catalogul conține **36 scenarii în șase categorii**, cu public, intrare, rezultat, expresii de căutare și condiții. Aplicația EVA este în dezvoltare. Scenariile sunt propuneri de produs și de conținut; existența unei utilizări la un furnizor consacrat nu dovedește implementarea ei în EVA.

## Ce susțin sursele

Apple documentează capturarea interioarelor și reconstruirea obiectelor. Dimensiunile trebuie comunicate cu limitele metodei: inclusiv aplicația Measure folosește estimări. [RoomPlan](https://developer.apple.com/augmented-reality/roomplan/), [Object Capture iOS](https://developer.apple.com/videos/play/wwdc2023/10191/), [Measure](https://support.apple.com/en-euro/guide/iphone/iphd8ac2cfea/ios).

Designul poate porni de la spațiul și mobilierul existente. Reparațiile beneficiază de fotografii și note asociate planului; administrarea clădirilor, de contextul vizual. Acestea susțin direcțiile propuse, fără a transfera către EVA promisiunile comerciale ale furnizorilor. [Polycam](https://poly.cam/solutions/interior-design), [magicplan](https://help.magicplan.app/restoration-documentation-annotating-your-floor-plan), [Matterport](https://matterport.com/solutions/facilities-management).

Pentru imprimare se verifică mesh-ul și scara; pentru CAD poate fi necesară reconstrucția unui solid editabil. DWG presupune integrare și licențiere. Scanarea persoanei cere cooperare și nemișcare; animația este un pas separat. [Prusa](https://blog.prusa3d.com/photogrammetry-2-3d-scanning-simpler-better-than-ever_29393/), [Autodesk](https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-CONVERT-TO-SOLID), [ODA SDK](https://www.opendesign.com/products/drawings), [ODA licențiere](https://www.opendesign.com/pricing), [Polycam persoane](https://learn.poly.cam/hc/en-us/articles/28271869062420-How-to-Capture-a-Person).

## Catalogul de inspirație

Fiecare rând este o **propunere EVA**, dedusă din posibilitățile documentate ale industriei. Termenii sunt ipoteze editoriale, fără volume de trafic măsurate. Câmpurile complete sunt în [catalogul JSON](usecase-catalog-ro.json). `planned` înseamnă planificat; `conditional` cere integrare, prelucrare externă ori validare suplimentară. Niciun statut nu înseamnă disponibil astăzi.

### Obiecte și imprimare 3D

| Utilizare propusă | Public | Intrare → rezultat urmărit | Expresie principală | Bază documentară |
|---|---|---|---|---|
| Obiecte cu dimensiuni | arhitecți, designeri de produs | obiect fizic și reper măsurat → model 3D la scară verificată | scanare obiecte iPhone | [S02](https://developer.apple.com/documentation/realitykit/realitykit-object-capture), [S03](https://support.apple.com/en-euro/guide/iphone/iphd8ac2cfea/ios) |
| Replici pentru imprimare 3D | makeri, artiști | obiect mat, fotografii suprapuse → mesh curățat pentru slicer | scanare pentru imprimare 3D | [S08](https://blog.prusa3d.com/photogrammetry-2-3d-scanning-simpler-better-than-ever_29393/) |
| Referință pentru reproiectare CAD | proiectanți, ateliere | obiect și cote de control → referință mesh pentru modelare CAD | scanare piesă pentru CAD | [S09](https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-CONVERT-TO-SOLID) |
| Suporturi adaptate obiectelor | makeri, designeri | obiect, zona de contact și cote → referință pentru suport personalizat | suport personalizat 3D | [S09](https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-CONVERT-TO-SOLID), [S08](https://blog.prusa3d.com/photogrammetry-2-3d-scanning-simpler-better-than-ever_29393/) |
| Produse prezentate în 3D | artizani, comercianți | produs și fotografii complete → model texturat pentru vizualizator web | model produs 3D | [S02](https://developer.apple.com/documentation/realitykit/realitykit-object-capture) |
| Arhiva prototipurilor | studiouri de design | prototip etichetat și reper → model cu versiune și cote de referință | arhivă prototipuri 3D | [S02](https://developer.apple.com/documentation/realitykit/realitykit-object-capture), [S09](https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-CONVERT-TO-SOLID) |

### Măsurare și proiecte pentru acasă

| Utilizare propusă | Public | Intrare → rezultat urmărit | Expresie principală | Bază documentară |
|---|---|---|---|---|
| Lățimea și înălțimea pereților | meseriași, proprietari | perete vizibil și puncte alese → cote AR; imagine doar la salvare explicită | măsoară pereți cu telefonul | [S03](https://support.apple.com/en-euro/guide/iphone/iphd8ac2cfea/ios) |
| Încape mobila aici? | cumpărători, amenajatori | spațiu disponibil și dimensiunile mobilei → comparație orientativă de gabarit | măsurare spațiu mobilă | [S03](https://support.apple.com/en-euro/guide/iphone/iphd8ac2cfea/ios), [S04](https://poly.cam/solutions/interior-design) |
| Trece obiectul prin ușă? | echipe de mutare, proprietari | uși, holuri și gabaritul obiectului → cote și puncte de verificat pe traseu | măsurare ușă telefon | [S03](https://support.apple.com/en-euro/guide/iphone/iphd8ac2cfea/ios) |
| Suprafață orientativă pentru vopsit | zugravi, amatori DIY | lățimi, înălțimi și goluri → arie estimată și ipoteze de calcul | calcul suprafață pereți | [S03](https://support.apple.com/en-euro/guide/iphone/iphd8ac2cfea/ios), [S06](https://help.magicplan.app/magicplan-floor-plan-editor-faq) |
| Pardoseli și placări | montatori, proprietari | conturul zonei și obstacole → arie orientativă cu deduceri explicite | calcul suprafață parchet | [S06](https://help.magicplan.app/magicplan-floor-plan-editor-faq) |
| Poziții pentru tablouri și rafturi | decoratori, proprietari | perete, cote și elemente alese → ghid vizual orientativ de poziționare | poziționare rafturi | [S03](https://support.apple.com/en-euro/guide/iphone/iphd8ac2cfea/ios), [S04](https://poly.cam/solutions/interior-design) |

### Design interior

| Utilizare propusă | Public | Intrare → rezultat urmărit | Expresie principală | Bază documentară |
|---|---|---|---|---|
| Reamenajarea unei camere | designeri, cupluri care renovează | scanarea camerei și cote verificate → model de referință pentru amenajare | aplicație amenajare cameră | [S01](https://developer.apple.com/augmented-reality/roomplan/), [S04](https://poly.cam/solutions/interior-design) |
| Bibliotecă de mobilier existent | designeri, ateliere de mobilier | fotografii ale mobilierului și gabarit → bibliotecă de modele pentru proiect | scanare mobilier 3D | [S04](https://poly.cam/solutions/interior-design) |
| Variante de amplasare | designeri, proprietari | camera și mobilierul digital → scenarii vizuale în editor compatibil | variante amenajare living | [S04](https://poly.cam/solutions/interior-design) |
| Brief pentru bucătărie | proiectanți bucătării, clienți | pereți, goluri și instalații vizibile → model și note pentru ofertare | măsurare bucătărie iPhone | [S01](https://developer.apple.com/augmented-reality/roomplan/), [S04](https://poly.cam/solutions/interior-design) |
| Discuții cu designerul la distanță | designeri, clienți la distanță | modelul camerei și observații → vizualizare partajată sau export | consultanță design online | [S04](https://poly.cam/solutions/interior-design) |
| Amenajarea unui spațiu comercial | comercianți, designeri comerciali | scanarea spațiului și cerințe de utilizare → referință pentru proiectul de amenajare | amenajare magazin 3D | [S01](https://developer.apple.com/augmented-reality/roomplan/), [S07](https://matterport.com/solutions/facilities-management) |

### Reparații și construcții

| Utilizare propusă | Public | Intrare → rezultat urmărit | Expresie principală | Bază documentară |
|---|---|---|---|---|
| Ce avem de reparat? | maiștri, proprietari | spațiu scanat și defecte vizibile notate → listă de intervenții localizate | aplicație listă reparații | [S05](https://help.magicplan.app/restoration-documentation-annotating-your-floor-plan) |
| Înainte și după renovare | constructori, beneficiari | scanări și fotografii datate → istoric vizual al etapelor | înainte după renovare | [S05](https://help.magicplan.app/restoration-documentation-annotating-your-floor-plan), [S07](https://matterport.com/solutions/facilities-management) |
| Ofertă pentru reparații | meseriași, clienți | model, note și zone de lucru → pachet de referință pentru ofertare | ofertă renovare cameră | [S05](https://help.magicplan.app/restoration-documentation-annotating-your-floor-plan), [S06](https://help.magicplan.app/magicplan-floor-plan-editor-faq) |
| Instalații înainte de închidere | instalatori, beneficiari | pereți deschiși, trasee vizibile și cote → arhivă de referință a instalațiilor | documentare instalații | [S04](https://poly.cam/solutions/interior-design), [S05](https://help.magicplan.app/restoration-documentation-annotating-your-floor-plan) |
| Observații la predarea lucrării | beneficiari, maiștri | camere și observații introduse manual → listă de verificare pentru discuția de predare | listă remedieri renovare | [S05](https://help.magicplan.app/restoration-documentation-annotating-your-floor-plan) |
| Referință pentru planșe CAD | arhitecți, ingineri | captură validată și cote de control → export și referință pentru CAD | scanare cameră CAD | [S01](https://developer.apple.com/augmented-reality/roomplan/), [S09](https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-CONVERT-TO-SOLID), [S12](https://www.opendesign.com/products/drawings), [S13](https://www.opendesign.com/pricing) |

### Locuințe și administrarea spațiilor

| Utilizare propusă | Public | Intrare → rezultat urmărit | Expresie principală | Bază documentară |
|---|---|---|---|---|
| Planul apartamentului | proprietari, arhitecți | scanări de camere și legături verificate → plan/model al apartamentului | scanare apartament iPhone | [S01](https://developer.apple.com/augmented-reality/roomplan/) |
| Casa organizată pe niveluri | arhitecți, proprietari de case | camere scanate și niveluri etichetate → proiect cu structură pe etaje | scanare casă 3D | [S01](https://developer.apple.com/augmented-reality/roomplan/), [S07](https://matterport.com/solutions/facilities-management) |
| Prezentarea unei proprietăți | agenți imobiliari, proprietari | captură interioară și date aprobate → material vizual pentru prezentare | model 3D apartament | [S07](https://matterport.com/solutions/facilities-management) |
| Starea locuinței la predare | proprietari, chiriași | fotografii, model și observații datate → arhivă de predare a spațiului | inventar locuință închiriată | [S05](https://help.magicplan.app/restoration-documentation-annotating-your-floor-plan), [S07](https://matterport.com/solutions/facilities-management) |
| Harta vizuală pentru mentenanță | administratori, tehnicieni | model și etichete adăugate manual → referință pentru echipa de mentenanță | mentenanță clădire 3D | [S07](https://matterport.com/solutions/facilities-management) |
| Planificarea unui eveniment | organizatori, administratori de săli | sală scanată, mobilier și cote → referință pentru scenarii de amenajare | plan sală eveniment | [S01](https://developer.apple.com/augmented-reality/roomplan/), [S07](https://matterport.com/solutions/facilities-management) |

### Persoane, creație și patrimoniu

| Utilizare propusă | Public | Intrare → rezultat urmărit | Expresie principală | Bază documentară |
|---|---|---|---|---|
| Portret 3D de păstrat | familii, creatori | persoană nemișcată, lumină uniformă → mesh de portret pentru editare | portret 3D iPhone | [S10](https://learn.poly.cam/hc/en-us/articles/28271869062420-How-to-Capture-a-Person) |
| Miniatură personalizată | ateliere de cadouri, artiști | captură voluntară și model curățat → mesh pregătit în software de tipărire | figurină 3D personalizată | [S10](https://learn.poly.cam/hc/en-us/articles/28271869062420-How-to-Capture-a-Person), [S08](https://blog.prusa3d.com/photogrammetry-2-3d-scanning-simpler-better-than-ever_29393/) |
| Referință pentru un avatar | artiști 3D, studiouri | persoană în postură stabilă și captură completă → mesh pentru retopologie și rigging extern | avatar din scanare 3D | [S10](https://learn.poly.cam/hc/en-us/articles/28271869062420-How-to-Capture-a-Person) |
| Recuzită pentru jocuri și film | creatori de jocuri, artiști VFX | recuzită și fotografii suprapuse → mesh texturat pentru optimizare | scanare recuzită 3D | [S02](https://developer.apple.com/documentation/realitykit/realitykit-object-capture) |
| Obiecte de patrimoniu și colecții | muzee, colecționari, educatori | obiect autorizat și fotografii non-invazive → model de referință și metadate | digitalizare patrimoniu 3D | [S02](https://developer.apple.com/documentation/realitykit/realitykit-object-capture), [S17](https://poly.cam/blog/3d-scanning-for-historic-building-restoration-preservation) |
| Modele pentru învățare | profesori, studenți | obiecte permise și captură ghidată → model 3D pentru explicații și comparații | modele 3D educație | [S02](https://developer.apple.com/documentation/realitykit/realitykit-object-capture), [S08](https://blog.prusa3d.com/photogrammetry-2-3d-scanning-simpler-better-than-ever_29393/) |

## Priorități pentru site

1. Prima pagină explică trei rezultate: model de obiect cu dimensiuni, cote în imagine, camere reunite într-un proiect. Persoanele constituie un scenariu distinct de creație, cu statutul real.
2. Pagina de inspirație filtrează șase categorii. Fiecare card răspunde la „Ce obțin?” și trimite către modul. Catalogul oferă exemple concrete, fără 36 de pagini aproape identice.
3. Obiecte: arhitect matur cu obiect măsurat. Măsurare: meseriaș în salopetă lângă perete. Camere: două situații, amenajare cu designerul și reparații cu maistrul. Imaginile conceptuale sunt etichetate; nu reprezintă rezultate testate ale aplicației.
4. Pentru fiecare demonstrație viitoare, salvați dispozitivul, condițiile, data și rezultatul verificat.

## Cuvinte cheie și intenția de căutare

| Grup | Intenție | Exemple în română | Exemple în engleză |
|---|---|---|---|
| Descoperire | Caut o aplicație | aplicație scanare 3D iPhone; scanner 3D cu dimensiuni | iPhone 3D scanner app; 3D scan with dimensions |
| Obiecte | Vreau un model utilizabil | scanare obiect pentru imprimare 3D; scanare piesă pentru CAD | scan object to STL; 3D scan for CAD reference |
| Măsurare | Am o întrebare practică | măsoară pereți cu telefonul; încape canapeaua | measure walls with iPhone; furniture fit measurement |
| Spații | Pregătesc un proiect | releveu apartament; scanare cameră design interior | room scanner for interior design; apartment floor plan app |
| Reparații | Vreau să comunic lucrarea | fotografii defecte pe plan; documentare renovare | renovation documentation app; repair notes on floor plan |
| Creație | Vreau o reprezentare personală | portret 3D; figurină personalizată | 3D portrait scan; custom miniature scan |

Expresiile nu promit trafic sau poziții în Google. Traducerile DE/FR/ES/HU/BG trebuie adaptate intenției locale și revizuite în context; nu se repetă mecanic toate expresiile în fiecare paragraf.

## Descoperirea în Google

O singură implementare și dicționarele dinamice pot servi mai multe URL-uri de limbă. Google recomandă URL distinct pentru fiecare limbă și legături explicite; variantele accesibile numai după schimbarea preferinței pot rămâne nedescoperite. În configurația curentă, `?lang=ro` și `?lang=en` trebuie să fie linkuri reale și să redea limba cerută. O structură viitoare `/ro/...` poate reutiliza același șablon și aceeași bază de date. Parametrii nu sunt structura preferată Google pentru segmentarea pe țări. [Google multilingv](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites).

Fiecare rută are nevoie de titlu și descriere utile, text semantic randabil, linkuri `href` și metadate conforme cu conținutul. Randarea pe server poate reduce dependența de JavaScript pentru textul principal; nu garantează indexarea. Verificarea în Search Console se face după publicarea domeniului. [Google JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics).

Evitați expresiile ascunse, repetarea excesivă, recenziile inventate și paginile create numai pentru variații minore de cuvinte. Păstrați statutul „în dezvoltare” până la existența unei versiuni utilizabile. [Politicile Google](https://developers.google.com/search/docs/essentials/spam-policies).

## Obiective verificabile pentru publicare

- 36/36 utilizări cu rezultat, public, surse și limită specifică în catalog.
- 6/6 categorii accesibile; filtre utilizabile cu tastatura.
- 7/7 limbi cu titlu, descriere, conținut și linkuri coerente.
- 0 afirmații de precizie numerică, diagnostic structural sau funcții medicale fără teste dedicate.
- 0 volume SEO, ratinguri sau testimoniale inventate.
- După publicare: verificați accesul crawlerului și sitemap-ul; urmăriți impresii, clicuri și interogări pe intervale de 28 zile. Țintele de trafic se stabilesc după prima bază reală de comparație.

## Registrul surselor și limitele documentării

Sunt păstrate linkuri și rezumate originale, nu copii integrale ale paginilor. Consultarea nu este data publicării. Scaniverse suport redirecționează către Niantic Spatial Capture; vechile funcții nu se atribuie automat noii pagini. Ruta franceză Polycam pentru patrimoniu a eșuat, versiunea engleză a fost deschisă. Documentația Object Capture folosește JavaScript; sesiunea WWDC deschisă oferă baza suplimentară.

- **S01** [Apple — RoomPlan](https://developer.apple.com/augmented-reality/roomplan/) — Planuri 3D pentru interioare folosind cameră și LiDAR; dimensiuni și elemente de mobilier.
- **S02** [Apple — Object Capture](https://developer.apple.com/documentation/realitykit/realitykit-object-capture) — Fotografii din unghiuri multiple pentru reconstruirea obiectelor; pagina documentației este randată cu JavaScript.
- **S03** [Apple — Measure dimensions](https://support.apple.com/en-euro/guide/iphone/iphd8ac2cfea/ios) — Măsurarea pe telefon produce estimări; nu presupunem toleranțe industriale.
- **S04** [Polycam — Interior design](https://poly.cam/solutions/interior-design) — Biblioteci de mobilier, planificare în spațiul existent, prezentarea variantelor clienților.
- **S05** [magicplan — Documenting damages](https://help.magicplan.app/restoration-documentation-annotating-your-floor-plan) — Fotografii, note și adnotări asociate planului pentru coordonarea reparațiilor.
- **S06** [magicplan — Floor plan editor FAQ](https://help.magicplan.app/magicplan-floor-plan-editor-faq) — Suprafețe de pardoseală și placare, inclusiv zone cu forme particulare.
- **S07** [Matterport — Facilities management](https://matterport.com/solutions/facilities-management) — Reprezentări spațiale pentru inventar, comunicare, planificarea și gestionarea clădirilor.
- **S08** [Prusa — Photogrammetry 2](https://blog.prusa3d.com/photogrammetry-2-3d-scanning-simpler-better-than-ever_29393/) — Reconstrucția pentru tipărire poate necesita închiderea golurilor, curățare și verificarea scării.
- **S09** [Autodesk — Convert mesh to solid](https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-CONVERT-TO-SOLID) — Mesh și solid CAD sunt reprezentări diferite; unele conversii cer reparații și extensii.
- **S10** [Polycam — Capture a person](https://learn.poly.cam/hc/en-us/articles/28271869062420-How-to-Capture-a-Person) — Persoana trebuie să stea nemișcată; mesh-ul poate fi prelucrat pentru animație sau tipărire.
- **S11** [Niantic Spatial — Capture (redirecționare Scaniverse)](https://www.nianticspatial.com/products/capture) — scaniverse.com/support redirecționează aici la consultare. Folosit pentru contextul capturii spațiale, nu pentru a confirma vechi formate Scaniverse.
- **S12** [ODA — Drawings SDK](https://www.opendesign.com/products/drawings) — SDK pentru citire/scriere DWG; trebuie ales și integrat un exportator compatibil.
- **S13** [ODA — Licensing and pricing](https://www.opendesign.com/pricing) — Licențierea și dreptul de distribuție trebuie verificate pentru integrarea comercială.
- **S14** [Google — JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) — Linkuri accesibile, randare și metadate pentru site-uri JavaScript.
- **S15** [Google — Multilingual sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites) — URL-uri distincte pentru limbile indexate și hreflang; conținutul ascuns doar în preferințe poate rămâne nedescoperit.
- **S16** [Google — Spam policies](https://developers.google.com/search/docs/essentials/spam-policies) — Evitarea aglomerării de cuvinte cheie, paginilor repetitive și funcționalităților înșelătoare.
- **S17** [Polycam — Historic building restoration](https://poly.cam/blog/3d-scanning-for-historic-building-restoration-preservation) — Captures de patrimoniu planificate în sesiuni, verificarea scării și documentarea zonelor lipsă. Ruta franceză a dat eroare; versiunea engleză a fost deschisă.
- **S18** [Apple — Meet Object Capture for iOS](https://developer.apple.com/videos/play/wwdc2023/10191/) — Flux ghidat de captură și reconstrucție pe dispozitive iOS compatibile.

