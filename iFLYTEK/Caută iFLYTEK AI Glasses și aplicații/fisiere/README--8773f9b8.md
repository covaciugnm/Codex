# Căutare extinsă în descrieri, pagini Help și coduri QR — 1 noiembrie 2026

[Autentificare prin SMS, prefixe acceptate de formular și serverele serviciilor](SMS-LOGIN-SERVICES.md).

Căutarea a urmărit modelul iFLYTEK XF-AIGlasses-01, magazine internaționale și regionale UE/UK/US, descrieri comerciale, pagini de asistență, imagini cu QR, Alibaba și platformele oficiale. Nu a fost identificat un APK public demonstrabil separat pentru UE. Site-urile blocate și rezultatele pentru alte modele sunt marcate în inventar; accesul global la un magazin nu dovedește distribuție oficială în UE.

## Software suplimentar găsit și arhivat

| Software | Versiune / acces | Legătura cu ochelarii |
|---|---|---|
| iFLYTEK Translate Windows x64 | 1.0.9, EXE | Client al platformei de traducere; conectarea directă Bluetooth a ochelarilor la acest client nu a fost verificată |
| iFLYTEK Translate macOS Apple Silicon | 1.0.9, DMG | Aceeași platformă |
| iFLYTEK Translate macOS Intel | 1.0.9, DMG | Aceeași platformă |
| Extensie iFLYTEK Translate Chrome | 0.3.0, CRX | Traducere în browser; nu este driver pentru ochelari |
| Extensie iFLYTEK Translate Edge | 0.2.1, CRX | Traducere în browser; nu este driver pentru ochelari |
| Skill oficial Loomy „讯飞翻译” | `transaas01`, 1.0.4 | Istoricul traducerilor prin CLI autorizat; instalare prin Loomy |
| `@xfyun/cli` | toate cele 11 versiuni publicate găsite | Instrument generic pentru platforma cloud; nu este SDK Bluetooth și nici CLI-ul `transaas` |
| iFly-Skills | snapshot `b8f5d7d0bad672c7b12d161ab11cf1de53461e08` | Actualizare a surselor generice; snapshotul vechi exista deja în GitHub |

Fișierele mari sunt în [Release-ul acestei cercetări](https://github.com/covaciugnm/iFLYTEK/releases/tag/iflytek-retailer-software-2026-11-01). CRX, TGZ și ZIP de dimensiuni mici sunt în folderul [software](software). Inventarul cu surse, mărime, SHA-256 și destinația fiecărui fișier este [file-inventory.json](file-inventory.json). Aplicațiile nu au fost executate sau instalate.

Sursele primare: [Download desktop](https://www.iflytranslate.com/client-download), [Download și extensii](https://www.iflytranslate.com/download), [Chrome Web Store](https://chromewebstore.google.com/detail/cmjdeaeonbhajidgpmbappcleimpcmlg), [Edge Add-ons](https://microsoftedge.microsoft.com/addons/detail/lhnkmmijpiijmedbojlefopjgagogmjl), [Microsoft Store](https://get.microsoft.com/installer/download/XPFD4ZXXW3VFGS?referrer=appbadge), [Loomy Skills](https://loomy.xunfei.cn/skills), [documentație xfyun CLI](https://www.xfyun.cn/xfyun-cli/doc).

Pentru skill, site-ul oficial publică `loomy://install-skill/transaas01`. Interfața cere Loomy 0.9.40 sau ulterior pentru instalarea automată; clientul 0.9.39 arhivat anterior nu îndeplinește această cerință. Nu a fost găsit un ZIP public separat al skillului sau un executabil public separat pentru `transaas`. Codul public al platformei menționează `transaas login --web`. Nu s-a efectuat autentificare.

Versiunile CLI generice sunt: 0.0.0-stage, 0.4.0, 0.4.1, 0.4.2, 0.5.0, 0.6.0, 0.6.1, 0.6.2, 0.7.0, 0.7.1, 0.7.2. `0.0.0-stage` este un pachet placeholder de 365 octeți. Integritatea SHA-512 a arhivelor npm a fost comparată cu metadatele registrului. Semnăturile editorilor aplicațiilor nu au fost validate.

## Comercianți și descrieri

| Site / pagină | Ce a rezultat |
|---|---|
| [A1 Smart Shop](https://a1smartshop.com/product/iflytek-ai-glasses/) | Modelul căutat, preț în GBP, descriere GlassClaw; niciun APK public în descriere. Moneda GBP nu dovedește sediu sau distribuție oficială UK |
| [Joom](https://uzummarket.joom.com/en/products/6a30e2450c735c016f6b2759) | Ofertă XF-AIGlasses-01; descărcarea automată a paginii a primit HTTP 429 |
| [Sahaha](https://sahaha.vn/en/san-pham/iflytek-ai-glasses/) | Ofertă pentru model; pagina nu a putut fi arhivată prin acces direct |
| [Tai Nghe Phien Dich](https://tainghephiendich.com/iflytek-ai-glasses/) | Descrie GlassClaw și Loomy; fără pachet de aplicație separat |
| [May Phien Dich](https://mayphiendich.net/en/8972) | Descriere a modelului; fără APK regional |
| [OpenChinaCart](https://www.openchinacart.com/products/2010225999563791) | Variantă de accesoriu/lentilă; HTTP 403, nu confirmă ochelari compleți |
| [Magazin oficial, produs 2448](https://www.xunfei.cn/goods?goodsId=2448) | Descriere în imagini și QR; codurile decodate trimit la WeChat comercial/asistență |
| [Jikemijing](https://jikemijing.com/product/57) | Director tehnic al modelului; imagini verificate |
| [VueAIS](https://www.vueais.com/product/iflytek-ai-glasses-smart-audio-wearable) | Director cu specificații; „No dealers available yet”, fără pachet software în descriere |
| [Tai Nghe Phien Dich — engleză](https://tainghephiendich.com/en/iflytek-ai-glasses/) | Descriere tradusă verificată separat; fără APK regional |
| [iFLYTEK UK](https://uk.iflytek.com/), [Franța](https://fr.iflytek.com/), [Global Store](https://store.iflytek.com/) | Acces direct blocat în această verificare; niciun APK UE confirmat |

Lista completă a paginilor, linkurilor extrase din descrieri, imaginilor, pasajelor relevante, erorilor și duplicatelor este [manifest.json](manifest.json). Linkurile comerciale nu reprezintă recomandări de cumpărare. Căutarea nu poate garanta inventarierea tuturor paginilor existente pe internet.

## Alibaba și piste pentru alte modele

[Toate cele nouă linkuri Alibaba identificate în această rundă](alibaba-links.json), inclusiv directoarele și categoriile cu rezultate amestecate. Nicio ofertă Alibaba nu a putut fi confirmată drept modelul original XF-AIGlasses-01.

- [Alibaba — ofertă AI Camera Smart Glasses](https://www.alibaba.com/product-detail/AI-Camera-Smart-Photo-taking-Glasses_1601689773331.html): ochelari generici, aplicație HeyCyan; nu sunt identificați drept XF-AIGlasses-01.
- [Alibaba — director furnizori iFLYTEK](https://electronics.alibaba.com/supplier/iflytek-translate): director general de dispozitive de traducere; nu oferă un APK verificat pentru modelul căutat.
- [Gold Optical G100](https://gold-optical.com/ai-glasses/), [Goodway G100](https://www.goodwaytechs.com/es/goodway-g100-smart-ai-camera-glasses.html), [Aventa](https://aventaglasses.com/): „Lumi Samp” / „Hello Lumi”. Mențiunea motorului iFlytek Spark nu identifică producătorul hardware și nu confirmă compatibilitatea aplicației.
- [Aurora AI Glass](https://auroraaiglass.com/): HeyCyan pentru alt hardware.

Nu am etichetat aceste aplicații pentru alte modele drept aplicații compatibile cu ochelarii iFLYTEK. Nu am găsit un SDK Bluetooth public nou pentru XF-AIGlasses-01. Tutorialul AstronClaw/Astron Harness și documentația generică xfyun existau deja în arhivă.

## QR, iOS și duplicate

Au fost analizate 62 de imagini. Cele trei QR-uri decodate indică două adrese WeChat de cumpărare/asistență, nu APK. Rezultatele și imaginile originale sunt în [qr-image-audit.json](qr-image-audit.json). Lipsa decodării nu exclude un cod în imagine, în special un mini-program WeChat.

Aplicația iOS [讯飞翻译](https://apps.apple.com/cn/app/id6739250870) menționează integrarea cu ochelarii; listările regionale și istoricul App Store sunt în [colecția anterioară](../collection-2026-11-01/README.md). Nu a fost găsit un IPA public descărcabil. Aplicațiile Android și arhivele Bavvo colectate anterior rămân documentate acolo; compatibilitatea Bavvo și existența unei ediții APK UE nu sunt confirmate.

Hashurile au fost comparate cu manifestul inițial și colecția precedentă. Paginile identice sunt referite prin `existing`, fără reîncărcare. Pistele fără legătură și duplicatele de fragment URL sunt în [excluded-leads.json](excluded-leads.json), fără a fi numărate drept rezultate relevante. Resursele web originale sunt păstrate ca dovezi, cu surse și SHA-256. Niciun endpoint privat și niciun cont de utilizator nu au fost accesate.

Verificare și restaurare: `node tools/verify-retailer-audit-20261101.cjs --restore`. Pentru repetarea extragerii HTML/QR, scripturile de audit necesită Node.js și pachetele `cheerio`, `sharp`, `jsqr`; calea către un `package.json` care le poate rezolva se poate configura prin `IFLYTEK_AUDIT_DEPENDENCIES`.
