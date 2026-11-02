# Deschiderea și restaurarea celor 14 directoare

În această sesiune, directoarele fizice sunt create în `D:/Codex-iflytek-apk-analysis-20261101/versions`. Deschide `INDEX.html` din acel director pentru lista aplicațiilor, versiunilor și variantelor. Rezultatele fiecărei materializări sunt în [materialization-runs.json](materialization-runs.json).

Fiecare variantă are propriile directoare `raw`, `decompiled` și `logs`, plus `SOURCE-MANIFEST.json`. Variantele cu același număr de versiune rămân separate. Fișierele fizice sunt verificate după SHA-256 și mărime la creare. Conținutul comun este încărcat o singură dată în GitHub; directoarele fizice pot conține copii independente pentru inspecție și lucru.

`PATH-MAP.json` leagă numele logice originale de numele fizice. Este necesar pentru resurse precum `res/2F.xml` și `res/2f.xml`, distincte în APK și confundate de Windows. Materializarea folosește nume unice pentru aceste cazuri, păstrând separat conținutul, numele original, mărimea și SHA-256. Această mapare privește directoarele de inspecție; APK-urile și inventarele originale rămân nemodificate.

## Restaurare pe alt calculator

Din rădăcina acestui repository, cu Node.js și `gh` autentificat pentru repository-ul privat:

```powershell
node tools/restore-apk-analysis-20261101.cjs --store-dir D:/iflytek-analysis-store
node tools/prefetch-apk-existing-git-20261101.cjs
node tools/materialize-all-apk-versions-20261101.cjs --store-dir D:/iflytek-analysis-store --output D:/iflytek-versions
```

Ultima comandă creează toate cele 14 directoare și indexul `D:/iflytek-versions/INDEX.html`. Pentru o singură variantă, folosește comanda din README-ul ei și adaugă `--preload-git` pentru citirea obiectelor Git într-un lot. Opțiunea `--local-only` este disponibilă după încălzirea cache-ului; refuză descărcările și citirea automată din rețea a obiectelor Git lipsă.

Fișierele noi sunt în [Release-ul analizei](https://github.com/covaciugnm/iFLYTEK/releases/tag/iflytek-apk-analysis-2026-11-01), împachetate în TAR.GZ deterministe. Inventarul [release-packs.json](release-packs.json) înregistrează SHA-256 al fiecărui pachet și al fiecărui obiect. Fișierele existente sunt citite prin identificatorul Git al conținutului sau prin intrarea exactă dintr-un ZIP anterior verificat. APK-urile originale, sursele Smali și analiza AOT publicate anterior nu sunt încărcate din nou.

## Interpretarea rezultatelor

`raw` este conținutul despachetat, inclusiv DEX, resurse și biblioteci native. `decompiled` conține reprezentarea Java obținută din DEX, inclusiv biblioteci scrise inițial în Kotlin. Erorile JADX sunt documentate în rapoarte și jurnale; codul rezultat nu garantează un proiect recompilabil. DEX-ul păstrează bytecode-ul original inclusiv pentru metodele pe care JADX nu le recuperează.

Nu a fost găsit proiectul original public al acestor aplicații. Flutter AOT rămâne în bibliotecile binare; nu pretindem recuperarea sursei Dart/C++. APK-urile `full-rebuilt` și `romania40` sunt derivate locale din cercetarea anterioară, identificate separat de distribuțiile furnizorilor. Nu s-a executat niciun APK în această activitate.
