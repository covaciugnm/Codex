# Fara titlu

ID: `01a18da7-2044-72b0-ace8-e3c96af38038`  
Proiect: iFLYTEK  
Export UTC: 2026-11-02T15:26:35.221418+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Asistent

Template v3 **APROBAT de auditorul independent** după remedierea tuturor punctelor A01–A08 și M01. Aprobarea privește metodologia; catalogul factual și implementarea HTML necesită verificare finală.

**Structura cărții HTML**

1. Rezumat executiv și shortlist pe cerințe.
2. Metodologie, data-limită **30.10.2026**, legendă și glosar.
3. Zece capitole pentru producători.
4. În fiecare capitol: prezentarea producătorului, inventarul auditat și subcapitolele modelelor.
5. Ecosisteme complete: ochelari + telefon/tabletă/neckband/puck + aplicații + hearing aid.
6. Analiza dezvoltării software și accesibilității auditive.
7. Matrice comparativă cu filtre pentru toate dimensiunile.
8. Cost total, întrebări pentru furnizori și plan PoC.
9. Registrul surselor, contradicțiilor și informațiilor neconfirmate.

**Inventarul obligatoriu**

Pentru fiecare producător, tabel „modele căutate / incluse / excluse / neconfirmate”, cu motiv și surse din cataloage oficiale, magazin, regiunea China/global și portal developer.

Se includ modelele comercializate în orice moment dintre 01.01–30.10.2026, chiar lansate anterior; disponibilitatea actuală se separă de dovada vânzării în interval. Se marchează distinct disponibil, preorder, anunțat, prototip, retras și neconfirmat.

Seriile audio-only, display-only și fără waveguide rămân în inventar cu etichete clare. Modelul, generația, varianta regională și bundle-ul nu se confundă. Disponibilitatea hardware nu confirmă accesul SDK.

**Template pentru fiecare producător**

Entitatea juridică/brandul, sediul verificat, website, cataloage China/global, developer portal, magazine, aplicații, suport, politici de actualizare, distribuție, OEM/ODM, contacte publice, maturitatea dovezilor și limitele inventarului.

**Template pentru fiecare model/variantă**

| Secțiune | Câmpuri obligatorii |
|---|---|
| Identitate | Model exact, generație, SKU, variante, regiune, lansare, statut în 2026 și la cutoff |
| Optică | Waveguide/birdbath/prismă/altele, monocular/binocular, see-through/passthrough, tehnologie display, culoare, rezoluție W/H **per ochi**, FOV H/V/D, Hz, eye-box, eye-relief, IPD, dioptrii/Rx, dimming/transparență |
| Luminozitate | Valoare, unitate și punct de măsurare; source-nits și at-eye-nits nu se compară direct |
| Calcul | SoC/GPU/NPU, TOPS doar documentat, RAM/storage, edge/cloud/telefon/companion |
| Camere/senzori | Număr, rezoluție, FPS, FOV, RGB/stereo/depth, indicator confidențialitate, IMU/GPS/magnetometru/proximity/light |
| AR | 3DoF/6DoF, tracking mâini/ochi, ancore, mapping și acces API separat |
| Alimentare | mAh/Wh, autonomie cu scenariu, încărcare/conector/putere/timp |
| Ergonomie | Greutate cu configurație, dimensiuni, IP, temperatură, comportament termic, compatibilitate cu aparate auditive |
| Audio | Microfoane/array, beamforming, AEC, NR, AGC, speakere open-ear/bone/in-ear, mono/stereo/spatial confirmat, sample rates/codecs |
| Conectivitate | Wi-Fi generație/benzi/hotspot/Direct; Bluetooth versiune/profil/codecs; USB-C charging/data/DP separat; UVC/UAC/HDCP unde relevante; tether wired/wireless |
| Compatibilitate | PC/Android/iOS, modele/OS minime, DRM, controller/gamepad și limitări |
| Companions | Telefon/tabletă/neckband/puck/telecomandă, rol calcul/control/display/power, obligatoriu/opțional/inclus/separat, compatibilitate și preț |
| OS/aplicații | OS/version, APK/sideload/store/root/bootloader, Android/iOS app links/region/version, offline/cloud/login |
| SDK | Versiune și model suportat, platforme, licență, cost, aprobare enterprise, download, documentație, examples/repos, mentenanță |
| API | Display liber/templates, fotografie/video, microfon/raw PCM, speaker PCM/full duplex, input, senzori/pose, background/autostart, networking, modele AI proprii |
| Reviewuri | Link/data/model/firmware, hands-on vs anunț, metodă, sponsorizare, constatări și limite; „căutat, negăsit” când cazul |
| Achiziție | Oficial/distribuitor/Alibaba exact-match, furnizor, MOQ/preț/monedă/data/cantitate, transport/taxe/garanție/retur, SDK inclus și validarea variantei |
| Evaluare | Avantaje, dezavantaje, potrivire pe aplicații, hard gates, necunoscute, contradicții și surse |

Fiecare capabilitate are cinci niveluri separate: **hardware existent → funcție în aplicația comercială → acces SDK public → acces condiționat → validare practică**. Domeniul dovezii este model × variantă × firmware × SDK × companion.

**Analiza hearing aid / accesibilitate auditivă**

- Subtitrări/transcriere/traducere: română și alte limbi, offline/cloud, diarizare, identificare/direcție vorbitor și latență STT.
- Routing explicit: sursă → procesare → destinație, cu rol transmitter/receiver/broadcast assistant, protocol, host/OS, model hearing aid verificat, bilateral, media/apel/live mic și conexiuni simultane.
- LE Audio, LC3, HAP/unicast, Auracast broadcast, ASHA și MFi sunt câmpuri distincte. Bluetooth sau Auracast generic **nu confirmă** compatibilitatea cu un aparat auditiv.
- Fezabilitate DSP: PCM-in, PCM-out, full duplex, background susținut, control output și **latență măsurată acustic-in → DSP → acustic-out**. Latența STT/cloud/codec este separată.
- DSP analizat: gain pe benzi, WDRC, MPO/limiter, feedback cancellation, NR/beamforming, AEC separat, profil auditiv/calibrare.
- Speakere analizate: SPL/headroom, distorsiune, scurgere, feedback și interferența dintre sunetul direct și cel procesat la open-ear.
- Stări concluzie: fezabilitate teoretică / demonstrat prin SDK / validat prototip / nefezabil documentat / necunoscut.
- Necunoscutele critice înseamnă **fezabilitate nevalidată**. Nu se inventează prag universal de latență/gain și nu se deduce eficacitatea clinică din instalarea unui APK.
- Orice statut medical cere jurisdicție, indicație, identificator și sursă verificabilă.

**Schema normalizată**

Entități: `manufacturers`, `models`, `variants`, `companions`, `sources`, `claims`, `reviews`, `offers`, `relationships`, `evaluations`, `inventory`.

Afirmație:

```text
entityId, field, value, unit,
state: confirmed | conditional | unknown | conflicting | not_applicable,
sourceIds, originalValue, evidenceLevel,
scope: model/variant/region/firmware/SDK/companion,
asOf, location, conflictNote
```

`false` și `0` necesită dovezi; lipsa informației devine `null/unknown`. Fiecare afirmație factuală trebuie legată de surse. Promisiunea producătorului, testul independent și inferența autorului rămân distincte.

**Matrice și filtre**

Registru unic de câmpuri:

```text
key, label, group, type, unit, enum,
applicability, filterType
```

Fiecare câmp tehnic produce o coloană sau un filtru avansat vizibil, cu aceeași funcționalitate. Nu rămân dimensiuni exclusiv în proză.

- Numeric: interval min/max, inclusiv W și H separat.
- Enum/relații: selecție multiplă OR.
- Între coloane: AND.
- Boolean: da/nu/necunoscut/condiționat.
- Orice câmp: filtre necunoscut/conflict/nu se aplică.
- Text și date: căutare/interval.
- Reset, count rezultate, selector coloane/grupuri, preseturi, sticky header, scroll orizontal, export CSV filtrat.
- Capitol/model în `<details><summary>`, ancore, expand/collapse total, tastatură, mobil, print cu detaliile deschise.

**Evaluare reproductibilă**

Deschiderea se separă de capacitatea tehnică și utilitatea auditivă.

Dimensiuni 0–4: instalare/distribuție, control UI, acces API la hardware relevant, lifecycle/background, documentație/licență/ecosistem. Un HUD poate primi maximum pentru UI fără funcții spațiale; lipsa camerelor nu este „închidere”.

Scor:

```text
100 × Σ_knownApplicable(w × s) / (4 × Σ_knownApplicable(w))
coverage = Σ_knownApplicable(w) / Σ_allApplicable(w)
```

Necunoscutul nu primește zero. Clasament numai cu hard gates îndeplinite, coverage ≥80% și dovezi comparabile; altfel provizoriu/neclasificat.

Ponderi instalare/UI/API/lifecycle/ecosistem:

- Visual AI: 20/15/35/20/10; gates cameră API + display API + inferență proprie.
- HUD/subtitrări: 15/35/15/20/15; gates text-render + rută STT.
- Spatial AR: 15/25/30/15/15; gates 6DoF + pose + spatial rendering.
- OEM: 20/20/20/15/25; gates ODM explicit + licență + furnizor validat.

Performanța este vector separat: rezoluție/FOV/tracking/calcul/latență/greutate/autonomie. Nu se emite scor clinic hearing aid.

**Cost și achiziție**

TCO = ochelari + compute obligatoriu + accesorii + licențe + subscriptions + AI usage + transport/taxe, cu monedă, dată și perioadă. Componente necunoscute împiedică un total pretins complet.

Alibaba: exact-match / variantă apropiată / doar căutare. Listing activ nu dovedește stoc, autenticitate sau SDK; „Verified Supplier” nu înseamnă distribuitor autorizat.

**Checklist QA final**

A01 inventar justificat; A02 hardware/app/API/test separate; A03 companions/connectivity complete; A04 DSP/acustică; A05 hearing routing; A06 scoruri/coverage/gates; A07 filtre; A08 cost/reviewuri/Alibaba; M01 rezumat/glosar/PoC.

Teste HTML: AND/OR, necunoscut/conflict/N/A, reset/count, fără rezultate, keyboard, ancore, expand/collapse, print, export cu Unicode și escaping CSV/formula injection, concordanță export/tabel, surse multiple și conflicte. Linkurile inaccesibile se raportează ca neverificate, fără a fi declarate automat inexistente.

## Asistent

Cercetare verificată la **30.10.2026**. Cele mai importante corecții față de lista inițială:

- **INMO AIR3 are recall oficial pentru supraîncălzire**; nu trebuie recomandat direct pentru achiziție fără verificarea remedierii.
- **INMO GO3 este RTOS**, nu Android; SDK-ul AIR3 nu se transferă.
- **Rokid Glass3 enterprise** este diferit de consumer **Rokid Glasses** și merită rând propriu.
- **Rokid Glasses 2 este preorder**, iar Rokid Color este anunțat pentru 2027; nu trebuie numărate drept modele deja livrate.
- **RayNeo iO „MFi Certified” nu înseamnă compatibilitate MFi hearing aid**. Senzorul bone-conduction este intrare, nu speaker.

### Rokid — modele principale

| Model / statut | Date verificate | Surse |
|---|---|---|
| **Rokid Glasses / With Display — disponibil global, variantă China separată** | Waveguide binocular MicroLED verde; rezoluție declarată **480×640**, FOV30°, 1.500nit; 49g; Snapdragon AR1, 2GB/32GB; cameră12MP, video până3K30; 4mic, 2speakere direcționale; Wi-Fi6, BT5.3, IMU, IPX4; 210mAh; charging magnetic,80%/20min; captions, translation, teleprompter, navigation; SDK declarat. | [Produs și specificații oficiale](https://global.rokid.com/products/b-h-rokid-glasses-with-display?variant=46066446368947) |
| **Rokid AI Glasses Style — disponibil global, fără display** | 38,5g fără lentile Rx; cameră SonyIMX68112MP,3K30,FOV109°,f/2.25; 32GB; 4mic cu reducere zgomot,2speakere open-ear; Wi-Fi6,BT5.3,IPX4; Hi Rokid obligatoriu, iOS16+/Android12+; preț pagină329USD. SDK specific Style neconfirmat, nu deduce din consumer display SDK. | [Produs oficial](https://global.rokid.com/products/rokid-ai-glasses-style?variant=45179509997747) |
| **Rokid Max2 — disponibil global** | OLED display tethered; rezoluție implicit1920×1080/ochi, până1920×1200 cu Station2;60–120Hz, dar Station2 folosește90Hz; dioptrii0…−6; microfon confirmat; nu se împerechează Bluetooth independent, căștile se conectează la host. | [Achiziție](https://global.rokid.com/products/rokid-max-2-ar-glasses?variant=44984888033459), [rezoluție oficială](https://global.rokid.com/blogs/max-2/what-is-the-display-resolution-of-the-rokid-max-2), [FAQ oficial](https://global.rokid.com/blogs/max-2) |
| **Rokid Glass3 RG301/RG303 — enterprise, lansare oficială29.06.2026** | YodaOS-Sprite Enterprise; canvas fix480×640 verde, cameră fixed-focus,2mic; Android SDK; iOS/HarmonyOS nesuportate; API pickup near-field/far-field/omnidirectional; comutare≈3sec, fără API public gain/sensitivity. Video SDK implicit1080×1920≈15–19fps; latență playback≈300ms **video**, nu hearing audio. | [FAQ developer primar](https://x-docs.rokid.com/docs/en/faq/%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98.html), [demo](https://x-docs.rokid.com/docs/en/downloads/demo-guide.html), [manual oficial](https://x-docs.rokid.com/lingmou_manual.pdf), [lifecycle](https://global.rokid.com/en-hispano/pages/security-center) |

**Bundle-uri/companions — nu dubla numărul modelelor:**

- **AR Spatial / AR Lite:** Max2+Station2, host de calcul spațial.
- **AR Joy2:** Max2+Station original, Android TV.
- Station2 este host dedicat; nu tabletă generală. Camera USB/SSD pe al doilea port nu sunt suportate conform FAQ, portul fiind charging-only.
- Power Capsule și charging case sunt alimentare, nu calcul.
- GameSir controller și Rokid Hub sunt accesorii.
- [Catalog oficial AR](https://global.rokid.com/collections/rokid-ar-glasses-series).

**Inventar suplimentar de păstrat cu statut neconfirmat în 2026:**

- **Max RA201**, **Max Pro RA202 + Station Pro RAS201 / AR Studio**, **Bolon AI RV201/RV202**: apar în [registrul oficial de suport](https://global.rokid.com/en-hispano/pages/security-center); acesta dovedește identitatea/lifecycle, nu stocul sau comercializarea în2026.
- **Rokid Air**, **Glass2 RG201**: listing Alibaba găsit, dar fără validare stoc/variantă actuală.
- **Glasses2 RV301…RV305:** preorder China, livrare raportată pentru noiembrie; data din security center este27.11.2026, divergentă față de presa11.11.2026. A se marca **preorder / dată divergentă**.
- **Rokid Color:** anunț octombrie2026, livrare raportată aprilie2027; **exclus din „comercializat și livrat până30oct”**, inclus anexă pipeline.
- [Relatare lansare Glasses2](https://www.notebookcheck.net/Rokid-Glasses-2-launch-with-upgraded-design-bigger-battery-and-Dolby-Audio-support.1435436.0.html). Specificațiile noii generații trebuie lăsate provizorii până la fișa primară.

**Software Rokid**

- [Developer portal oficial](https://open.rokid.com/), dinamic, fără text extractibil.
- [Aplicații oficiale](https://global.rokid.com/pages/app-download): **Hi Rokid1.16.0,30oct2026**, cere firmware `1.28.016-20261029-150201`; captions, agent store, translation cu playback audio opțional, teleprompter și control cameră.
- Glass3 are documentație primară clară, proiecte Android pentru telefon și ochelari, debugging prin cablu dedicat.
- CXR-L/M/S pentru consumer: diferențele de naming/versiune din surse comunitare sunt inconsistente; **nu aș marca public PCM/full-duplex/background „Da” fără documentul modelului exact**.
- [Repo universitar care implementează CXR-M1.2.2](https://github.com/hkust-spark/xg-glass-sdk/blob/main/devices/device-rokid/README.md): util pentru PoC, **sursă implementator terț**, nu contract oficial fabricant.

**Reviewuri Rokid**

- [Tom’s Guide — Rokid Glasses, utilizare pe5.000mile](https://www.tomsguide.com/computing/smart-glasses/rokid-glasses-review): hands-on, relevant pentru uz cotidian.
- [TechRadar — Style, o lună](https://www.techradar.com/computing/virtual-reality-augmented-reality/ive-spent-a-month-with-the-rokid-ai-glasses-style-theyre-excellent-smart-glasses-let-down-by-an-ugly-design): autonomie observată aproximativ5–6ore în sesiuni mixte față de marketing12ore; costurile lentilelor/case contează.
- [DigitalCameraWorld — Style](https://www.digitalcameraworld.com/cameras/digital-cameras/rokid-ai-glasses-style-review-could-these-smart-glasses-dethrone-metas-ray-bans): evaluare foto/video.

**Alibaba Rokid**

- [Rokid Glasses — listing exact ca denumire](https://www.alibaba.com/product-detail/Rokid-Smart-Glasses-AI-Display-AR_1601780559671.html): Guangdong Daoran Film And Television Equipment; MOQ2; preț indexat731,84USD. Varianta/SDK/autorizarea neconfirmate.
- [Rokid Air](https://www.alibaba.com/product-introduction/100-Rokid-Air-Smart-Glasses-Foldable_1600484720108.html): listing vechi, MOQ5,179USD la pragul inițial; nu dovedește suport2026.
- [Rokid Max](https://www.alibaba.co.uk/product-detail/Rokid-Smart-Ar-Glasses-Headband-Augmented_1600555301061.html).
- [Glass2 industrial](https://www.alibaba.com/pla/Rokid-Glass-2-foldable-AR-glasses_1600496530630.html?biz=pla&mark=google_shopping&product_id=1600496530630&searchText=ar+hardware): **nu consumer Glasses2 lansat2026**.

### RayNeo — inventar și date

Catalogul global confirmă **GT Max, GT, Air4Pro, Air3s, Air3sPro, iO, X3Pro, X2**. Air3sPro și X2 apar „Sold out”. Lista comparativă mai include Air2/Air2s. China are suplimentar **V4 și Air4**, iar V3/V3Slim apar în documente istorice.

| Model | Specificații / interpretare | Sursă |
|---|---|---|
| **X3Pro — disponibil global** | Waveguide binocular MicroLED color640×480;30°;3.500nit avg/6.000peak; AR1Gen1,4GB/32GB;12MP+spatial camera;3mic beamforming;245mAh;76±1g;Wi-Fi6,BT5.3,USB2-C; AIOS,6DoF+SLAM,Android/Unity ARDK, Gemini,14limbi. | [Produs oficial](https://www.rayneo.com/products/x3-pro-ai-display-glasses) |
| **X2 — listat sold-out, EOL declarat** | Waveguide color; cameră16MP; model older pentru developeri. Nu recomand achiziție nouă fără clarificarea suportului. | [Produs](https://www.rayneo.com/products/tcl-rayneo-x2), [EOL oficial](https://src.rayneo.cn/) |
| **iO — disponibil global** | Waveguide binocular MicroLED verde;33g;23,5°;1.300nit eye-level;camera absentă;4mic+bone-conduction sensor;240mAh;BT5.4,MFi certified;IP54;translation continuă6,2h declarată. Rezoluție, speaker și SDK specific neconfirmate în pagina extrasă. | [Produs oficial](https://www.rayneo.com/products/rayneo-io-ai-glasses) |
| **GT — disponibil global** | MicroOLED1920×1080;FOV46°;120Hz2D/60Hz3D;68g;3DoF nativ;luminozitate1.200nit non-pinned/336nit pinned;quad-speaker B&O,head-tracked spatial audio;USB-C DP. | [Produs](https://www.rayneo.com/products/rayneo-gt-ar-glasses) |
| **GT Max — disponibil global** | MicroOLED1920×1080;FOV59°;120Hz2D/60Hz3D;78g;aceleași moduri/pinned brightness,quad audio;USB-C DP;PocketTVPro pentru DolbyVision. | [Produs](https://www.rayneo.com/products/rayneo-gt-max-ar-glasses) |
| **Air4Pro — disponibil global** | MicroOLED FullHD,120Hz,1.200nit,HDR10,76g,quad B&O,spatial sound/Whisper;host extern, fără cameră. | [Produs](https://www.rayneo.com/products/rayneo-air-4-pro-ar-smart-glasses), [comparație fabricant](https://www.rayneo.com/blogs/news/the-complete-ar-glasses-buying-guide-7-essential-factors-for-first-time-buyers-4) |
| **Air3s — disponibil global** | MicroOLED1080p,120Hz,650nit to-eye;display tethered. | [Produs](https://www.rayneo.com/products/rayneo-air-3s-xr-glasses), [tabel oficial](https://www.rayneo.com/en-ca/blogs/news/rayneo-air-series-spec-table-compared) |
| **Air3sPro — sold-out global** | MicroOLED1080p,120Hz,1.200nit to-eye;quad-speaker;display tethered. | [Produs](https://www.rayneo.com/products/ar-glasses-rayneo-air-3s-pro-features), [fișă](https://www.rayneo.com/pages/ar-glasses-rayneo-air-3s-pro-1200nits) |
| **Air2s — model vechi/listat, EOL** | Patru speakere; sursa oficială amestecă600nit key specs și5.000nit marketing: păstrează separat baza măsurării. | [Comparație oficială](https://www.rayneo.com/en-ca/blogs/news/rayneo-air-series-spec-table-compared), [specs](https://uk.rayneo.com/pages/tech-specs) |
| **Air2 — model vechi/listat, EOL** | Două speakere; model display tethered; verificare stoc2026 incompletă. | [Specificații](https://uk.rayneo.com/pages/tech-specs), [EOL](https://src.rayneo.cn/) |
| **V4 — China, produs oficial cu buy link** | Camera/audio AI; pagina vizuală nu a expus specificațiile; nu completa cifre din analogie cu V3. | [Produs China](https://rayneo.cn/v4.html) |
| **Air4 — China, produs oficial** | Pagina China este „Air4”, navigația „Air4(Pro)”; versiunea non-Pro trebuie păstrată separat până la confirmarea SKU. | [Produs China](https://rayneo.cn/Air4.html) |

**Inventar neconfirmat:** V3/V3Slim, Air3 China, Air original, X2Lite. Ultimul nu trebuie presupus produs comercial din simpla prezentare CES. [Catalog China](https://www.rayneo.cn/), [catalog global](https://www.rayneo.com/pages/rayneo-shop).

**Companions RayNeo**

- PocketTV streaming box129USD; PocketTVPro199USD; GoogleTV media hosts, nu tablete.
- JoyDock89USD: NintendoSwitch adaptor/power.
- USB-C charging adaptor35USD, HDMI64USD.
- GT/GTMax „Sound Tube”19USD: direcționare acustică spre ureche; **nu hearing aid/DSP**.
- GT suportă USB-C video pe iPad compatibil,PC/Mac,Android,iPhone; incompatibilitățile concrete trebuie păstrate. [Catalog/accesorii](https://www.rayneo.com/pages/rayneo-shop).

**Software RayNeo**

- [Ghid Qualcomm primar, X3Pro](https://www.qualcomm.com/developer/project/get-started-with-rayneo-x3-pro-ar-development): Android/Unity ARDK,OpenXR,ADB; audio,cameră,gyroscope prin Android native APIs. Aceasta justifică API acces documentat, dar nu latență full-duplex măsurată.
- [Portal developer](https://open.rayneo.com/).
- [Download oficial](https://www.rayneo.com/pages/download): XR App pentru Air,Android8+cuDP; AR App pentru X,Android/iOS. Nu extrapola vechile minime la iO.
- Public Android API pentru audio face X3Pro candidat PoC; **nu există în sursele verificate validare hearing aid, gain calibrat sau latență acustică**.

**Reviewuri RayNeo**

- [TechRadar X3Pro,14iul2026](https://www.techradar.com/pro/rayneo-x3-pro-ai-ar-smart-glasses-review): display apreciat; autonomie activă foarte limitată, inclusiv≈45min în scenarii intensive; ecosistem dificil.
- [Tom’s Hardware X3Pro](https://www.tomshardware.com/peripherals/wearable-tech/rayneo-x3-pro-ar-glasses-review): problemă autonomie.
- [TechRadar Air3sPro,31ian2026](https://www.techradar.com/pro/rayneo-air-3s-pro-smart-glasses-review): confort/display și plug-and-play evaluate favorabil; dependent de host.
- Reviewuri individuale GT/GTMax/iO/V4: **nefinalizate**, nu inventa.

**Alibaba RayNeo**

[Listing X3Pro global](https://www.alibaba.com/product-detail/TCL-RayNeo-X3-Pro-AI-Glasses_1600989292035.html): Shenzhen Omni-In Technology,MOQ1,1.250USD indexat. Identificarea titlului este X3Pro, dar URL-ul versiunii germane păstrează **X2** și atribute generice3Dshutter/>80"; cere SKU/foto/firmware și drepturile SDK înainte de comandă. Listingul nu validează autorizarea.

### INMO — modele și inventar

| Model / statut | Date verificate | Surse |
|---|---|---|
| **GO3 IMG301 — disponibil global/China, variante de verificat** | Waveguide binocular MicroLED verde640×480,30°,1.500nit eye-level;RTOS,dual-core,256MB+64GB;≈58g;270mAh schimbabil,spare inclus;4mic/2speaker;camera8MP confirmată în app oficial. Ring4,INMO Speaker opționale; captions/translation/navigation. SDK public GO3 neconfirmat. | [Fișă oficială](https://www.inmo.com/pages/inmo-go3-ai-glasses), [app fabricant](https://apps.apple.com/us/app/inmo-global/id6758009618) |
| **AIR3 — comercializat Dec2025–Aug2026, recall** | Waveguide binocular full-color1920×1080,36°;Android14;8GB/128GB;Snapdragon nespecificat exact în sursa primară accesibilă;16MP;GooglePlay instalare;Unity developer portal. Greutatea și performanța după update necesită verificare: surse divergente119/135g. | [Comparație oficială](https://www.inmo.com/de/blogs/news/whats-difference-between-inmo-air3-and-meta-ray-ban-display-glasses), [FAQ crowdfunding fabricant](https://www.kickstarter.com/projects/inmo-air3-ar-glasses/inmo-air3-smart-ar-glasses/faqs), [SDK](https://developer.inmolens.com/) |
| **GO2 — China actual/catalog și support; global statut neconfirmat** | Produs translation cu sistem Android propriu potrivit istoricului fabricant; aplicație INMOGO Android. Nu transfera APK/SDK AIR3. | [Catalog China](https://inmolens.com/inmo-go/), [download oficial](https://www.inmolens.com/download), [istoric](https://www.inmo.com/pages/about-us) |
| **Magic AI Glasses J — pagină oficială actuală; comandabilitatea neconfirmată** | Fără HUD documentat;40,1g;camera8MP;open-ear audio,voice navigation/translation;BT5.2;Memories App Android/iOS;SDK neconfirmat. | [Pagina oficială](https://www.inmo.com/pages/magic-ai-glasses-j) |
| **AIR2 / AIR / GO original** | Generații istorice; AIR/AIR2 încă au aplicație INMOLENS Android, GO/GO2 INMOGO; dovada vânzării2026 insuficientă. | [Download](https://www.inmolens.com/download), [istoric](https://www.inmo.com/pages/about-us) |
| **INMO X / R2 / X R2** | X este familie camera AI; R2 are appINMOX Android/iOS în download actual, în timp ce pagina istorică spune „Coming soon” pentruXR2: identitatea/statusul trebuie clarificate. | Aceleași surse oficiale |

**Recall AIR3 — obligatoriu vizibil**

[Pagina oficială](https://www.inmo.com/pages/recall) cere oprirea utilizării și contactarea suportului pentru actualizare, din cauza supraîncălzirii brațului stâng. Menționează vânzări Amazon/Kickstarter/inmoxr.com,Dec2025–Aug2026,900–1.300USD. [Explicație updateV3.16](https://www.inmo.com/ja/blogs/inmo-insights/inmo-air3-recall-update-performance). Nu interpreta actualizarea drept validare independentă a remedierii sau performanței.

**Aplicații INMO**

- [INMO Global Android](https://play.google.com/store/apps/details?id=com.inmo.app.googleplay).
- [INMO Global iOS](https://apps.apple.com/us/app/inmo-global/id6758009618): iOS17+,GO3,versiune2.4.1 la verificare. App reviews includ probleme de background/iOS; acestea sunt anecdote ale utilizatorilor, nu comportament universal.
- [Download China pe model](https://www.inmolens.com/download).
- [Developer AIR3](https://developer.inmolens.com/): spatial tracking,6DoF,gestures,build/deploy. Portalul dinamic limitează inspecția completă a API.
- **Nu s-a confirmat** PCM/audio full-duplex/background public peGO3; nu presupune sideload Android peRTOS.

**Ecosistem auditiv INMO**

GO3+telefon+INMO Speaker+Ring4; speakerul extern redă traducerea și poate folosi voice cloning opțional. **Acesta transformă/redă vocea pentru interlocutor, nu corectează auzul purtătorului.** [Descriere oficială a rutelor](https://www.inmo.com/blogs/inmo-insights/ai-glasses-vs-ar-glasses-travel-translation-movies). Nicio tabletă dedicată confirmată; Air3 are compute integrat, touchpad/ring fiind controllere.

**Reviewuri INMO**

- [GO3 — evaluare o săptămână](https://smartglasses.fyi/en/journal/inmo-go3-review/): utilă pentru confort, baterii schimbabile și limite; trebuie păstrată clasificarea hands-on declarată.
- [AIR3 — bug roundup ianuarie2026](https://note.com/mrvr/n/n2a252f0ea13e?hl=en): agregator comunitar, nu review controlat.
- [T3 GO3,22oct2026](https://www.t3.com/tech/vr/these-new-smart-glasses-with-a-display-solve-the-camera-issue-in-simple-unique-fashion): articol despre produs, **nu test hands-on**.
- Pentru GO2/AIR2/X/R2/MagicJ: review specific actual neconfirmat.

**Alibaba INMO**

- [AIR3](https://www.alibaba.com/pla/INMO-Air-3-AR-Smart-Glasses_1601789376431.html?biz=pla&mark=google_shopping&pcy=nl_en&product_id=1601789376431&searchText=smart+glasses): Shanghai Blue Lemon,MOQ1,828–863USD indexat; **recall și firmware obligatoriu de verificat**.
- [GO3](https://www.alibaba.com/pla/INMO-GO3-Real-time-Translation-AR-Smart_1601781968022.html?biz=pla&mark=google_shopping&pcy=gb_en&product_id=1601781968022&searchText=ar+hardware): Dongguan Hecheng Interactive,MOQ1,456,80–576,80USD indexat; variantă regională/SDK/garanție neconfirmate.

Nu am obținut dovadă de interoperabilitate hearing aid verificată, certificare medicală sau latență acustică măsurată pentru niciunul dintre aceste modele. Pentru shortlist tehnic: **X3Pro și Glass3 enterprise** au cele mai concrete documente primare de dezvoltare inspectate; **Rokid Glasses** rămâne candidat consumer; **GO3/iO** sunt atractive pentru captions, dar deschiderea SDK trebuie validată separat.

## Asistent

Am transmis root-ului generatorul în **3 bucăți**, pentru **3 producători și 38 modele**, cu surse, reviewuri, oferte și necunoscute explicite.

Salvarea mea a rămas blocată la aprobarea shell și a fost întreruptă; **nu confirm existența fișierului**. Root poate salva și executa generatorul fără reluarea cercetării.
