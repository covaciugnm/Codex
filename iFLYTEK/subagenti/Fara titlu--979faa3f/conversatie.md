# Fara titlu

ID: `01a18da7-f7b8-7450-9ad3-568a979faa3f`  
Proiect: iFLYTEK  
Export UTC: 2026-11-02T21:26:40.664214+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Asistent

Material de cercetare pentru capitolul „Ecosistem pentru persoane cu dificultăți auditive”, verificat la 30.10.2026. Nu am creat documentul înaintea aprobării template-ului.

### Concluzia de inginerie

**Cea mai realistă arhitectură este ochelari pentru subtitrare și control, telefon/tabletă pentru aplicație și recunoaștere vocală, aparat auditiv compatibil pentru redare audio.** Introducerea unei aplicații de amplificare în ochelari este un proiect separat, dependent de accesul la traseul audio și de măsurători acustice. Nu rezultă automat din existența unui SDK, a Androidului sau a difuzoarelor.

Separă în raport trei funcții:

1. **Accesibilitate vizuală:** transcriere în aceeași limbă, traducere, identificarea vorbitorului, notificări vizuale.
2. **Audio asistiv:** microfon distant, reducerea zgomotului, egalizare și redare către dispozitive compatibile.
3. **Compensarea hipoacuziei:** procesare adaptată persoanei, limitarea ieșirii și validare clinică/reglementară. Nu este echivalentă cu „volum mai mare”. FDA diferențiază aparatele auditive de amplificatoarele destinate persoanelor cu auz normal. Este o delimitare conceptuală utilă; cadrul FDA nu înlocuiește verificarea pentru UE/România. [FDA](https://www.fda.gov/medical-devices/consumer-products/hearing-aids)

### Dovezi pe platformele prioritare

| Platformă | Demonstrat în documentație | Ce rămâne de verificat |
|---|---|---|
| **Even G2** | Română explicit la transcriere Conversate, intrare și ieșire Translate, afișare text și traducere bidirecțională. | Română offline nu este demonstrată de sursele consultate. |
| **Rokid Glasses** | Traducere online 89 limbi; offline șase: EN/ZH/JA/FR/DE/ES. SDK oficial oferă canale imagine/audio/afișaj/comenzi. | Lista oficială nominală nu confirmă româna în pagina citată; nu presupune că numărul 89 dovedește funcția română în firmware-ul cumpărat. |
| **RayNeo X3 Pro** | Traducere vizuală/audio; pagina oficială numește 14 limbi și dependența de rețea pentru funcțiile online. | Româna nu este în lista nominală consultată; listă offline verificată absentă în această sursă. |
| **INMO AIR3** | Campania oficială declară traducere în peste 40 de limbi. | Română nominală, offline, API microfon, canale audio brute și full-duplex nu sunt demonstrate de această afirmație. |
| **LLVISION LEION HEY2 / LEION HEARING** | Producătorul oferă subtitrare și un produs distinct LEION HEARING orientat către conversații accesibile. | SDK-ul LEION Pro nu demonstrează SDK pentru HEY2/HEARING; româna și limbile offline necesită verificare contractuală. |

Surse și nuanțe:

- **Even G2:** [lista oficială pe funcții](https://support.evenrealities.com/hc/en-us/articles/13755354799247-Language-Support). Documentația [Conversate](https://support.evenrealities.com/hc/en-us/articles/14273795154319-Conversate) confirmă alegerea microfonului ochelarilor ori telefonului înainte de sesiune și afișarea transcrierii. În timpul sesiunii nu poți schimba sursa din funcția descrisă. Aceste detalii sunt mai relevante decât „40 limbi”.
- **Even SDK:** [overview oficial](https://hub.evenrealities.com/docs/get-started/overview) confirmă patru microfoane, dar **un singur flux PCM 16 kHz**. Nu echivala patru microfoane fizice cu patru canale independente accesibile dezvoltatorului. [Tutorialele oficiale](https://hub.evenrealities.com/docs/learn/videos) descriu aplicația web rulată pe telefon și alegerea microfonului. Alegere bună pentru prototip de subtitrare; capacitatea de redare/procesare în aparate auditive prin aceeași aplicație trebuie demonstrată separat.
- **Rokid:** [FAQ oficial](https://global.rokid.com/pages/faq) și [tutorial traducere din august 2026](https://global.rokid.com/en-hispano/blogs/academy-glasses/3-2-real-time-translation) confirmă pachetele offline și variațiile regionale/firmware. [Portal SDK](https://open.rokid.com/) confirmă accesul I/O prin CXR-L și aplicația Rokid AI; această pagină nu dovedește latență audio, acces DSP ori full-duplex.
- **RayNeo:** [explicația oficială X3 Pro](https://www.rayneo.com/en-ca/blogs/news/rayneo-x3-pro-live-translation-explained) indică aproximativ 2,1 secunde și un interval comercial 1–3 secunde dependent de rețea. Acestea sunt latențe declarate pentru traducere, **nu** latența necesară pentru amplificare auditivă. Există pagini regionale și postări comunitare cu alte afirmații despre offline; păstrează-le drept conflict de rezolvat prin versiune și model, nu fuziona promisiunile.
- **INMO:** [FAQ al campaniei oficiale](https://www.kickstarter.com/projects/inmo-air3-ar-glasses/inmo-air3-smart-ar-glasses/faqs). [Quick Start AIR3](https://support.inmoxr.com/air3/guides/air3-quick-start/) confirmă asistentul și configurarea, nu nivelul de deschidere al traseului audio.
- **LEION:** [FAQ comercial](https://leion.glass/de-de/pages/haeufig-gestellte-fragen) descrie HEARING drept dispozitiv de subtitrare, nu aparat auditiv/dispozitiv medical. Pentru HEY2 declară patru microfoane și pachete offline pentru limbi selectate, fără listă suficientă pentru România. Atenție la afirmația „200 ms”: nu este măsurare independentă și nu trebuie folosită drept latență completă a transcrierii. [Pagina LLVISION la MWC](https://www.mwcshanghai.com/exhibitors/37279-beijing-llvision-technology-co-ltd) confirmă orientarea către accesibilitate și legătura companiei cu domeniul leion.glass.

### Pot difuzoarele ochelarilor să funcționeze ca aparat auditiv?

**Pot reda sunet procesat dacă platforma permite; utilitatea compensatorie nu este demonstrată.** Pentru open-ear, sunetul natural ajunge direct la ureche și se amestecă cu copia procesată întârziată. Pot apărea colorație, ecou, filtrare în pieptene și dificultăți cu propria voce. Cercetarea arată dependența de întârziere, gain, audiogramă și cuplaj, inclusiv diferențe perceptibile la întârzieri mici; „sub 10 ms” nu este un certificat universal de acceptabilitate. [Studiu experimental privind întârzierile](https://pmc.ncbi.nlm.nih.gov/articles/PMC11638989/), [studiu despre percepția propriei voci, 2026](https://pubmed.ncbi.nlm.nih.gov/41869839/)

Cerințe de PoC, propuse de inginerie:

- captură și redare simultană continue; drepturi API concrete, nu doar înregistrare fișier;
- latență **acustică end-to-end**, distribuție mediană/p95, jitter și întreruperi;
- control al procesării fabricantului: AEC/AGC/NS, resampling, buffere;
- procesare pe benzi, gain și compresie independente pe urechi, limitare calibrată a nivelului maxim;
- feedback acustic și gain maxim stabil cu mâna lângă ramă, păr, căciulă, poziții diferite;
- răspuns în frecvență și distorsiune la ureche, nivel de scurgere către ceilalți;
- inteligibilitate în zgomot și efort auditiv, nu doar preferință subiectivă pentru volum;
- confort simultan cu aparate BTE/RIC, implant cohlear și lentile corectoare.

Nu prescrie în raport valori individuale de amplificare. [Ghidul ASHA pentru aparate auditive la adulți](https://www.asha.org/practice-portal/professional-issues/hearing-aids-for-adults) tratează adaptarea fizică, feedbackul, cuplajul și verificarea beneficiului. Pentru o aplicație care urmărește compensarea hipoacuziei, este nevoie de audiolog și analiză de reglementare a utilizării intenționate.

Pe Android, Oboe/AAudio poate cere mod low-latency și acces exclusive, dar acestea **nu sunt garantate pe dispozitiv**. Instalarea APK-ului nu garantează acces la o cale rapidă ori la DSP. [Ghid oficial Oboe](https://github.com/google/oboe/blob/main/docs/FullGuide.md)

### Hearing aid connectivity: câmpuri obligatorii în template

Pentru **fiecare SKU**, coloane distincte:

- Bluetooth versiune;
- A2DP source/sink, HFP și rol;
- **ASHA**: sursă compatibilă sau receptor compatibil;
- **MFi hearing devices**: suport explicit;
- **LE Audio**, codec LC3 și profil HAP;
- **Auracast transmitter / receiver / assistant**, fiecare separat;
- simultaneitate ochelari–telefon–aparat auditiv;
- matrice model telefon + OS + firmware + model aparat auditiv testat;
- rută selectabilă pentru microfon și ieșire, comportament la apel și reconectare.

**Bluetooth 5.3/5.4 nu demonstrează niciuna dintre funcțiile auditive de mai sus.** ASHA și MFi nu sunt sinonime cu LE Audio. [Microsoft, delimitarea protocoalelor](https://support.microsoft.com/en-us/accessibility/windows/using-hearing-devices-with-your-windows-11-pc), [specificația Android ASHA](https://source.android.google.cn/docs/core/connect/bluetooth/asha?hl=en)

Un **Auracast assistant** poate descoperi/selecta fluxul pentru receptor fără să recepționeze sau să redea el însuși audio. [Bluetooth SIG, roluri](https://www.bluetooth.com/wp-content/uploads/2024/05/2403_How_To_Auracast_Assistant.pdf). Registrul [Find an Auracast Product](https://www.bluetooth.com/auracast/find-a-product/) permite verificarea rolurilor declarate.

În cercetarea făcută **nu am găsit dovezi suficiente de suport nativ ASHA/MFi/HAP/Auracast la ochelarii analizați**. Marcați „nedocumentat”, nu „nu există”.

### Ecosistem realizabil

**Variantă A — subtitrare plus aparat auditiv existent:** ochelarii primesc text de la aplicație; aparatul auditiv continuă propriul traseu de procesare. Este calea cu cele mai puține dependențe audio între dispozitive. Even G2 este candidat puternic pentru română și prototip de subtitrare.

**Variantă B — microfon distant și subtitrare:** telefon/tabletă aproape de vorbitor sau microfon extern verificat → STT → ochelari; în paralel, rută audio compatibilă către aparat auditiv. Trebuie testată capturarea simultană: două aplicații nu primesc automat același microfon.

**Variantă C — iPhone/iPad ca microfon:** Apple documentează Live Listen către aparate MFi, inclusiv utilizarea iPad. Aceasta demonstrează un traseu auditiv prin tabletă, **nu integrarea automată cu aplicația ochelarilor**. [Apple Live Listen](https://support.apple.com/en-us/111777)

**Variantă D — Android Sound Amplifier ca reper:** oferă reducere de zgomot și amplificare către căști cu fir sau Bluetooth; Google avertizează asupra întârzierilor/calității unor căști Bluetooth. Util pentru comparație experimentală, nu dovadă că ochelarii pot substitui un aparat auditiv. [Google Sound Amplifier](https://support.google.com/accessibility/android/answer/9157755?hl=en)

**Tabletă:** în template separă „tabletă oficială a producătorului”, „compute puck”, „telefon cu ecran”, „tabletă Android/iPad compatibilă”, „monitor conectat USB-C”. Nici suportul Android, nici un port USB-C nu demonstrează compatibilitatea aplicației, DP Alt Mode sau alimentarea simultană.

### Reviewuri: ce poate fi citat

- [Android Central, test X3 Pro timp de o lună, 20.01.2026](https://www.androidcentral.com/wearables/i-used-rayneo-x3-pro-for-a-month-these-ar-glasses-are-futuristic-but-theres-a-problem): experiență pozitivă cu afișajul/traducerea, autonomie raportată foarte slabă în exemplarul/testul autorului. Nu generaliza rezultatul la toate firmware-urile.
- [TechRadar, review X3 Pro](https://www.techradar.com/pro/rayneo-x3-pro-ai-ar-smart-glasses-review): util pentru fricțiunea software și interacțiune; nu benchmark clinic de accesibilitate.
- [Relatare comunitară HEY2, octombrie 2026](https://www.reddit.com/r/accessibility/comments/1wzfbje/measuring_caption_delay_on_glasses_the_leion_hey2/): aproximativ 2,5 secunde raportate, unitate oferită gratuit de LLVISION, fără plată declarată. Etichetează „test utilizator / mostră furnizată”, nu studiu independent. Aceeași relatare apare în mai multe subreddits; **nu o număra de trei ori**.

### Protocol minim pentru decizia de achiziție

1. Confirmați firmware/region și demonstrație în **română vorbită**, separat transcriere și traducere.
2. Test avion fără Wi-Fi/date după activare și descărcarea modelelor.
3. Lot audio română: liniște, cafenea, mai mulți vorbitori, nume proprii, numere, vorbire rapidă.
4. Măsurați WER, întârziere prim text/final text p50/p95, pierderi și revizuiri ale textului.
5. Verificați font, diacritice, contrast, vizibilitate soare și posibilitatea repoziționării.
6. Test continuu minimum două ore pentru autonomie/temperatură și comportament de fundal.
7. Pentru audio: măsurare end-to-end și limitare de ieșire înainte de evaluare pe persoane.
8. Verificați conexiunea cu **modelul real de aparat auditiv**, inclusiv apeluri și reconectare.
9. Confirmați costuri ASR/cloud, licență SDK, publicare aplicații, acces date, export/ștergere.
10. În tabel: „Da demonstrat”, „declarat de producător”, „condiționat”, „nedocumentat”, „nu”, fiecare cu sursă și versiune.

**Recomandare provizorie:** Even G2 pentru subtitrare română și dezvoltare prin telefon; Rokid/RayNeo/INMO pentru explorarea aplicației native și traseului audio, după PoC; LLVISION pentru soluție de subtitrare gata făcută, cu deschiderea SDK verificată separat. Niciunul nu trebuie declarat câștigător pentru „hearing aid în ochelari” în absența măsurătorilor.

## Asistent

Inventar verificat la **30 octombrie 2026**. „Comercializat în 2026” trebuie să includă produsele retrase în cursul anului; prototipurile și paginile istorice au statut separat. Nu pot demonstra exhaustivitatea tuturor SKU-urilor regionale/private ODM.

## Even Realities

| Model / variantă | Statut 2026 | Specificații și software |
|---|---|---|
| **G1 A** — ramă rotunjită | Vândut în 2026; vânzarea directă oprită la 15.09.2026. Stocuri distribuitori posibile, neconfirmate. | Waveguide binocular verde MicroLED, **640×200**, **25°**, **20 Hz**, **1.000 nit**; 2 microfoane; BLE 5.2; fără cameră/difuzoare. Telefon necesar. |
| **G1 B** — ramă rectangulară | Același statut; variantă de ramă, nu generație separată. | Aceeași platformă optică/software G1. |
| **G2 A** — panto/rotunjită | Comercial actual | Waveguide binocular verde MicroLED, **640×350**, **27,5°**, **60 Hz**, **1.200 nit**, 98% transmisie declarată; 4 microfoane; BLE5.4; baterie192mAh, husă2000mAh; IP65; autonomie declarată 2 zile utilizare obișnuită. |
| **G2 B** — rectangulară | Comercial actual | Aceeași platformă G2; geometria ramei diferă. |
| **R1** | Accesoriu comercial, **nu ochelari/tabletă** | Inel pentru control G2; nu îl număra ca AI Glasses. |
| **G3** | În dezvoltare / roadmap | Nu am găsit dovadă suficientă de comercializare până la data cercetării. Exclude din lista de cumpărare curentă. |

**Surse oficiale:** [G1 produs și specificații](https://www.evenrealities.com/g1); [anunț retragere G1](https://support.evenrealities.com/hc/en-us/articles/17564427335823-Even-G1-Sales-Discontinuation-Notice); [G2 specificații](https://support.evenrealities.com/hc/en-us/articles/13499229138959-Specifications); [magazin oficial](https://www.evenrealities.com/en-CA/store).

G1 continuă să funcționeze cu aplicația, iar perioada publicată de suport de securitate nu se încheie înainte de **25.06.2029**, conform anunțului oficial. Nu înseamnă promisiune de funcții noi.

**Dezvoltare:** [Even Hub overview](https://hub.evenrealities.com/docs/get-started/overview) pentru G2: aplicația rulează pe telefon, ochelarii sunt interfață; patru microfoane fizice, **single stream PCM16kHz**, nu patru canale brute. [Tutorial SDK](https://hub.evenrealities.com/docs/learn/videos) arată suprafață de desen **576×288**: păstrează separat *rezoluție optică 640×350* și *canvas SDK576×288*. Nu prezenta Even Hub pentru G1 fără dovadă de compatibilitate actuală. Nu este instalare APK nativă în ochelari.

**Aplicație iOS:** [Even Realities](https://apps.apple.com/ro/app/even-realities/id6747017725). Aplicația companion este și pe Android, dar cerințele minime/compatibilitatea tabletelor trebuie fixate la versiunea livrată. Nu am identificat tabletă proprie Even.

**Reviewuri reale:** [Tom’s Guide G1 — o lună, 18.07.2025](https://www.tomsguide.com/computing/smart-glasses/even-realities-g1-smart-glasses-review); [TechRadar G2 — 13.09.2026](https://www.techradar.com/computing/virtual-reality-augmented-reality/even-realities-g2-review); [Tom’s Guide G2](https://www.tomsguide.com/computing/smart-glasses/even-realities-g2-smart-glasses-review). Ultimul are tabel cu cifre G1, în conflict cu fișa oficială G2: **nu importa 640×200/20Hz/1.000nit la G2**. Reviewurile favorizează confortul/discreția, dar lipsa camerei și audio limitează utilizările.

**Alibaba:** am găsit [listare intitulată Even G1](https://germany.alibaba.com/product-detail/2025-Even-Realities-G1-AI-AR_11000034961357.html), însă titlul pretinde **cameră** și „Made in USA”, incompatibile cu produsul oficial. **Listare respinsă ca bază de achiziție, autenticitate neconfirmată.** Pentru G2 apar agregări Alibaba cu numele modelului, dar n-am verificat pagină individuală + vânzător autorizat. Raportul să spună „exact match autentic neconfirmat”; să nu recomande produsele „G1 style”.

## LLVISION / LEION

| Model | Statut verificabil | Specificații / integrare |
|---|---|---|
| **LEION HEY2** | Comercial, pagina spune disponibil | 49g; afișaj verde, **480×640** conform ordinii publicate; patru microfoane; BLE5.4; Wi-Fi2,4/5GHz; 245mAh; până la8h; încărcare magnetică și până la12 reîncărcări în husă. **Fără cameră frontală și fără difuzor.** Android8+/iOS11+ declarate; telefon companion. |
| **LEION HEARING — Tea Brown** | **Precomandă**, expediere estimată sfârșit octombrie2026; nu presupune livrare realizată | 49g, subtitrare prioritară, cameră absentă; 699USD; 4.800 minute Pro; garanție comercială2ani. Este SKU/pachet distinct, nu dovadă de generație hardware complet diferită. |
| **LEION Pro** | Produs enterprise în catalog oficial; disponibilitatea de livrare2026 prin ofertă de reconfirmat | Waveguide binocular,640×400; FoV30° diagonal; până la4.000nit; transmisie85%;90g; cameră13MP; MyriadX;512MB; stereo; USB-C2/3; Android8+ host. |
| **GLXSS SE** | În catalog enterprise; stoc/contract2026 neconfirmat | Monocular640×400;20°; cameră13MP/1080p; Myriad2 în pagina actuală;512MB;32g modul/45g cu ramă; microfon cu reducere zgomot; un difuzor;USB-C2.0. |
| **LEION HEY / G35A-00** | Model anterior documentat; nu am confirmat vânzare nouă2026 | Nu îi atribui automat datele HEY2; păstrează într-o anexă de legacy. |
| **GLXSS ME** | Pagină/documentație istorică, comercializare2026 neconfirmată | Nu include la „disponibil acum” doar pentru că URL-ul răspunde. |
| **GLXSS SE special explosion-proof** | Configurație specială enterprise menționată oficial | Certificarea și SKU-ul exact necesită documente; nu transfera certificarea întregii familii. |

**Surse:** [HEY2 cumpărare/fișă](https://leion.glass/products/leion-hey-2-smart-ar-glasses); [HEARING precomandă](https://leion.glass/products/leion-hearing-tea-brown-caption-glasses); [catalog comercial](https://leion.glass/collections/all); [LEION Pro oficial](https://www.llvision.com/leion-pro.html); [GLXSS SE oficial](https://www.llvision.com/glxss-se.html); [manual HEY anterior](https://static1.squarespace.com/static/64a291569090725a6bc6ea3e/t/64e71701f129251d4272f13f/1692866327754/LEION%2BHEY%2BUser%2BManual.pdf).

**Punct important tablete:** LEION Pro declară explicit compatibilitate USB cu **smartphone-uri, tablete și terminale industriale Android8+**. Ochelarii nu au emițător wireless propriu; conectivitatea 5G/Wi-Fi/Bluetooth vine de la host. Nu marca Wi-Fi nativ „da”.

**SDK:** [broșura oficială enterprise](https://file.llvision.com/download/AR_FSM_Solution.pdf) documentează SDK AR, dar este veche. Confirmarea accesului curent, licenței și compatibilității se face per LEION Pro/GLXSS. **Nu există în cercetarea mea dovadă suficientă de SDK public pentru HEY2/HEARING.**

**Apps:** [LEION iOS](https://apps.apple.com/us/app/leion/id6450490984?platform=watch). Parametrul URL `platform=watch` nu demonstrează aplicație watchOS; este pagina App Store găsită, verificați rubricile de compatibilitate. Android este declarat de produs, APK oficial verificabil neextras.

**Abonamente/pachete:** „Leion Pro Translation Access” și „Hey2 Pro translation access” din magazin sunt **servicii**, nu noi modele de ochelari. HEY2 este549USD, HEARING699USD; Pro Minutes trebuie bugetate separat. Nu am confirmat lista nominală română/offline.

**Review:** [HearingTracker comparație caption glasses](https://www.hearingtracker.com/hearing-glasses/hear-with-your-eyes-five-ar-live-captioning-glasses) utilă pentru context, dar poate trata HEY2 și Hearing ca aceeași familie; diferența de SKU/precomandă se ia de pe magazin. [Test utilizator HEY2](https://www.reddit.com/r/accessibility/comments/1wzfbje/measuring_caption_delay_on_glasses_the_leion_hey2/) raportează circa2,5s și declară mostră oferită de LLVISION; nu este validare clinică.

**Alibaba:** nicio listare individuală exactă, suficient verificată, găsită pentru aceste modele. O pagină generică sau un intermediar Taobao nu este link Alibaba de achiziție validat.

## SmartXY / Shenzhen Xingyi

Catalogul spune explicit **8 intrări de produs +2 referințe istorice**, cu stadii diferite. [Catalog](https://smartxy.com.cn/products/)

| Model | Statut | Date esențiale |
|---|---|---|
| **AR99 / Mimosa AR99** | Producție de serie OEM/ODM | Fără cameră; waveguide VHG verde monocular dreapta;640×480/30Hz;30°; până la2.000nit;28g fără lentileRx;100mAh; Bluetooth/telefon. |
| **AR99 MY / Mimosa** | Producție; ramă cat-eye distinctă | Platformă AR99 comună,29g fără lentileRx. |
| **AR99 Pro** | **EVT3, prototip CNC** | SRG monocular verde;640×480/30Hz;25°;1.800nit;25g; carbon;2×40mAh interschimbabile fără oprire declarată; inel obligatoriu inclus. |
| **C100** | **EVT3, prototip CNC** | Cameră+waveguide binocular; Android11 autonom client de servicii AI, nu LLM local. |
| **K900 / XY-008** | Producție din2024, în principal comenzi ODM | Cameră/audio, **fără afișaj**. |
| **Audio01** | Numai proiect ODM | Open-ear+microfoane; fără cameră și fără afișaj; SDK per proiect. |
| **Nudge** | Concept/configurație proiect, serie neconfirmată | Fără cameră; senzori distanță/înclinare, semnal vizual prin „smart fog”, nu display AR pixelat. |
| **BB Medical** | Platformă configurată pe proiect | Headset display clinic; nu produs medical certificat demonstrat. |
| **Confidant** | Referință istorică2021 | Nu produs pregătit overseas; fără mostre. |
| **Falcon007Pro** | Referință istorică | Nu produs pregătit overseas; fără mostre. |

Date adiționale din pagini distincte:

- **AR99:** [tehnologie oficială](https://smartxy.com.cn/technology/): autonomie funcțională de referință1–3h, standby72+h; nu confunda cu cele8h dintr-un comunicat al furnizorului de cip. [AR99 Pro](https://smartxy.com.cn/products/ar99-pro/) confirmă etapaEVT3.
- **C100:** [fișă platformă](https://www.topaiglasses.com/products/c100/):640×480/ochi,25°;SonyIMX68112MP/1080p30;ATS6095+MTK8766;Android11;2GB/32GB;Wi-Fi5 dual-band;BT6.0 declarat la SoC;5microfoane, stereo;IMU6axe;IP44;45g. Bateria/capacitatea husei necesită ofertă. SDK ochelari + Android telefon; acces prin cerere. Separă **capacitatea cipului** de funcțiile expuse în firmware.
- **K900:** [pagina oficială](https://www.smartxy.com.cn/products/k900/):39g;SonyIMX25813MP/1080p30EIS;5microfoane;stereo;MT6765+BES2700H;2GB/32GB;270mAh;BT5.4+Wi-Fi6 2,4GHz declarat;8–10h muzică versus55min video continuu. Livestreaming numai configurații partener; nu dovedește API standard live video.
- **Nudge:** [fișă](https://www.topaiglasses.com/products/nudge/):aprox30g, senzori distanță și înclinare; aproximare de proiect pentru copii3–12ani. Nu atribui prevenție/tratament miopie.
- **BB Medical:** [fișă](https://www.smartxy.com.cn/products/bb-medical/):MicroOLED binocular1920×1080/60Hz;55°;205g fără cablu;500nit;DC5V/2A;adaptorHDMI/USB-C;IMU6axe. Latența<20ms este referință video, nu sistem validat. Sursa/tableta/adaptoarele trebuie convenite.

**SDK AR99:** [pachet și limite publicate](https://www.topaiglasses.com/products/ar99/) Android+iOS, arhivă20260827/1.0.3 versus ghid Android2.0.0 — **nu versiuni uniform validate**. Pachetul nu a fost compilat/testat de autorul paginii. Canvas arbitrar, licența sursă și accesul tuturor funcțiilor necesită probe. Nu scrie doar „SDK complet deschis”.

**App:** [SmartXY iPhone](https://apps.apple.com/vn/app/smartxy/id6755132016), asociată AR99, conexiune/setări, interpretare, teleprompter,navigație,transcriere,AI. Listing „Only for iPhone”; nu este dovadă iPad. Nu am găsit tabletă proprie SmartXY.

**Reviewuri:** Nu am găsit test independent solid al AR99/C100/K900 cu măsurători repetabile. [Actions Technology](https://www.actionstech.com/index.php?id=8419&siteId=4) confirmă integrarea cipului AR99, dar este furnizor, nu review. Articolele de lansare și paginile SmartXY nu se etichetează review independent.

**Alibaba:** nicio listare individuală exactă, verificată, găsită. RFQ direct producător este ruta documentată. **XY-DC Reference Architecture** apare ca direcție ODM fără display, explicit *nu SKU suplimentar*, deci nu o număra drept model comercial.

**Observație transversală:** pentru toate cele trei companii, n-am găsit dovadă suficientă de profil nativ ASHA/MFi/HAP sau rol Auracast pe ochelari. În tabel: **ND**, nu „Nu”; surround, full-duplex PCM și acces DSP la fel, dacă pagina nu le specifică.

## Asistent

Am trimis către root generatorul pentru **22 de modele, 3 producători** și **7 secțiuni de analiză hearing**, plus corecțiile și oferta Alibaba respinsă.

Nu am scris fișiere: aprobarea shell a rămas blocată. Root poate salva conținutul transmis fără alte cercetări.
