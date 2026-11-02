# Plan de analiză APK/XAPK și criterii de închidere

Rol: manager/arhitect. Data: 1 noiembrie 2026.

## Acoperire

Manifestul inițial și colecția din 1 noiembrie identifică 13 intrări APK/XAPK ale furnizorilor, reprezentând 12 SHA-256 distincte. Verificarea celuilalt branch și a Release-urilor adaugă două APK-uri derivate local, rezultând **14 APK/XAPK unice în acoperirea totală**:

- Bavvo `com.iflytek.bavvo`: 1.0.1112, 1.0.1179, 1.0.1197, 1.0.1205, 1.0.1211, 1.0.1222, în format XAPK.
- Translate `com.iflytek.translateapp`: 1.0.3899 implicit, 1.0.3899 canal FY10030001, 1.0.3899 canal FY10030002 și 1.0.3949.
- Loomy Android și AINOTE Android din arhiva inițială; identificatorii și versiunile trebuie citite din manifestele APK, fără presupuneri după numele fișierului.
- Două APK-uri derivate din Translate 1.0.3899: `full-rebuilt` și `romania40`. Acestea sunt reconstrucții locale din [Release-ul separat](https://github.com/covaciugnm/iFLYTEK/releases/tag/iflytek-apk-romania40-2026-10-31), nu versiuni originale ale furnizorului și nu dovezi pentru un APK oficial UE.

Cele două căi vechi `Biblioteca_Glasses/Aplicatii/iflytranslate-official.apk` și `Cercetare_SDK_2026-10-30/iflytranslate-official.apk` au același SHA-256 `73170cdc5c3331cd6055607015c04ed8e0a314f4c0bd2fd4651e2b732d1b3da2`. Reprezintă o singură intrare de analiză, cu două referințe de proveniență.

## Reutilizare

Analiza anterioară `Software/APK_Reconstituit_2026-10-30` corespunde APK-ului Translate 1.0.3899 implicit. README-ul său identifică 2.264 fișiere originale, 23.200 fișiere Java decompilate, reprezentarea Smali a 47.219 clase și 80 biblioteci native. JADX 1.5.6 a raportat cod de ieșire 3 și 301 erori; aceasta este o limită documentată, nu un export Java perfect.

Fișierele existente se reutilizează prin referințe cu hash și cale sau asset de Release. Nu se copiază fizic în fiecare versiune și nu se încarcă din nou. Diferențele față de versiunea de bază trebuie păstrate separat. Pachetele cu același versionName și conținut diferit rămân variante distincte.

Comparația existentului include și branch-ul `build/reproducible-apk-20261031`, commit `4792f6b38e2c51e8d98c9fbc0b537ef6a521db8f`, și Release-ul `iflytek-apk-romania40-2026-10-31`, nu numai branch-ul curent. Sunt deja publicate:

| Asset existent | SHA-256 |
|---|---|
| `iflytek-1.0.3899-full-rebuilt.apk` | `c10d5475f384d433884e44417126f1077478790241ab174bc5987a08a98f038c` |
| `iflytek-1.0.3899-romania40.apk` | `82aa11096fbd474f0669b5ca295e325fd0b0c45c2999360859d1bd93821a9aa8` |
| `iflytek-1.0.3899-editable-source.zip` | `e53fe743b74c2825323c9a2b62b2b01bcf1c19fb1c0a05a7af2ab6494eaa0eea` |
| `iflytek-1.0.3899-aot-analysis.zip` | `674b063c0a7b792c08d846868de5c800be1c06eda10d9a991f4ed116f49fc5fa` |
| `iflytek-20261031-analysis-toolchain.zip` | `f9d58bab1defe9da64924143227a4a4747869d184c56885548bc886e2700d9b7` |

Conținutul decompilat, Smali și analiza AOT din aceste arhive se includ în baza de comparație pentru deduplicare. Denumirea `editable-source` descrie proiectul reconstruit existent; nu îl transformă în sursa originală oficială a aplicației.

## Structură recomandată

Fiecare înregistrare se identifică prin `package/versionCode-versionName/variant-SHA-prefix`. Pentru XAPK se inventariază atât containerul, cât și toate APK-urile din interior: base și configurațiile ABI/limbă/densitate. Nu se tratează XAPK ca un APK unic și nu se pierd spliturile.

Fiecare versiune trebuie să conțină ori să refere verificabil:

1. Proveniența APK/XAPK, hashul complet, dimensiunea și metadatele manifestului.
2. Inventarul integral al fișierelor extrase, dimensiuni și hashuri.
3. Resursele și manifestul Android decodate, DEX originale și rezultatul decompilării cu loguri și erori.
4. Inventarul bibliotecilor native și al artefactelor Flutter/Dart, acolo unde există.
5. Comparația cu arhiva existentă și cu versiunea precedentă relevantă: identic, schimbat, adăugat, eliminat.
6. Fișiere noi ori referințe către conținut existent, fără duplicate la publicare.

## Livrare fără duplicate în GitHub

Indexurile pe versiune pot descrie directoare logice independente fără să copieze conținutul comun. Pentru fiecare fișier, cheia este SHA-256 a octeților, iar înregistrarea indică una dintre următoarele destinații:

- `existing`: calea și storage-ul din manifestul inițial sau din colecțiile deja publicate;
- `object`: un obiect nou adresat prin hash, împărțit cu celelalte versiuni care conțin aceiași octeți;
- `generated`: rezultatul decompilării, tratat la fel prin hash și comparat și cu rezultatele vechi, nu numai cu APK-ul brut.

În Git se păstrează indexurile pe versiune, rapoartele, manifestele packurilor și instrumentele de restaurare/verificare. Obiectele noi voluminoase se grupează în packuri de Release mai mici de 2 GB fiecare; fiecare pack are propriul SHA-256 și inventarul obiectelor. Același obiect nu intră în două packuri și nu se reîncarcă dacă există deja în arhiva veche sau într-un Release verificat.

Restaurarea rezolvă referințele vechi sau noi, verifică mărimea și hashul și materializează directoarele separate pe versiune. Raportul trebuie să deosebească clar „fișier prezent logic prin referință” de „fișier materializat local”. Packurile, indexurile și directoarele trebuie să fie suficiente pentru reproducerea verificabilă a structurii fără a executa aplicațiile.

Pentru fișiere deja publicate în arhivele sursă/AOT ale reconstrucției, [baseline-release-index.json](baseline-release-index.json) mapează hashul conținutului către `{storage:'release-zip-entry',release,asset,archiveSha256,entry,bytes}`. Instrumentul `tools/index-baseline-release-20261101.cjs` verifică SHA-256 și mărimea ZIP-ului, citește și hash-uiește fiecare intrare în memorie, fără extragere în filesystem. La restaurare se descarcă sau se reutilizează ZIP-ul o singură dată, i se verifică `archiveSha256`, apoi se citește exact `entry` și se verifică SHA-256 și `bytes` ale fișierului materializat. O cale de intrare din arhivă nu se folosește ca destinație de scriere nevalidată.

## Criterii verificabile pentru audit

Scorul 10/10 poate evalua completitudinea și corectitudinea activității statice, nu recuperarea imposibil de garantat a surselor originale. Pentru închidere:

- Toate cele 14 pachete unice sunt inventariate și au rezultate separate; cele 12 ale furnizorilor, cele două derivate local și aliasurile sunt explicit deosebite.
- Hashurile intrărilor coincid cu manifestele de descărcare și/sau arhiva inițială.
- Fiecare intrare ZIP este fie extrasă, fie referită către un exemplar identic verificabil; erorile de CRC, căile nesigure și coliziunile nu sunt ignorate.
- Toate spliturile XAPK sunt incluse și au propriile metadate.
- Instrumentele și versiunile lor, logurile și limitele sunt păstrate. Codul decompilat nu este numit sursă originală și nu se declară recompilabil fără test.
- Nicio aplicație nu este executată și nu se accesează conturi sau servicii private pentru această analiză.
- Auditorul verifică independent inventarele, câteva exemple reprezentative și rezultatele comparației; corecțiile se reauditează până nu rămân neconformități în criteriile declarate.

## Căutarea surselor originale

La 1 noiembrie 2026 au fost căutate expresiile `com.iflytek.translateapp github source code`, `com.iflytek.bavvo github source` și `site:github.com/iflytek Loomy Android source code`. A fost inspectată lista publică de 67 de repository-uri din organizația oficială [iflytek](https://github.com/iflytek), prin API-ul GitHub. Nu a fost identificat un repository public al sursei originale pentru APK-urile analizate.

[iFly-Skills](https://github.com/iflytek/iFly-Skills), [tutorialul Astron Harness/Loomy](https://github.com/iflytek/astron-harness-tutorial) și SDK-urile generice de voce/AI nu reprezintă sursa aplicațiilor Android. Rezultatele de căutare nu demonstrează inexistența unei surse private sau a unui repository public neindexat.
