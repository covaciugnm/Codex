# Fara titlu

ID: `01a19736-121d-7d22-b45d-8935ba3ad4b4`  
Proiect: iFLYTEK  
Export UTC: 2026-11-02T21:26:40.664214+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Asistent

Am creat [ARCHITECTURE.md](<\\192.168.100.169\Comun\00.Roboti\iFLYTEK\archive-repository\apk-analysis-2026-11-01\ARCHITECTURE.md>) cu:

- 14 pachete unice: 12 ale furnizorilor și două reconstrucții locale.
- Separare pe package, versiune și variantă; reutilizare CAS fără duplicate.
- Criterii verificabile pentru audit și restaurare.
- Distincția dintre sursa originală și codul decompilat.
- Comparație inclusiv cu branch-ul `build/reproducible-apk-20261031` și Release-ul reconstrucțiilor.

Nu am identificat sursele originale publice. Arhivele existente `editable-source.zip` și `aot-analysis.zip` nu au manifest extern complet per fișier; deduplicarea sigură necesită citirea și indexarea lor. Am comunicat executorului și auditorului această limită.

## Asistent

Indexarea baseline este completă:

- ZIP-urile existente sunt descărcate direct pe UNC, în `.work/baseline-release/`.
- Ambele SHA-256 ale arhivelor coincid cu Release-ul.
- Am citit în memorie 49.768 fișiere din `editable-source` și 3.197 din AOT.
- `baseline-release-index.json`: **52.829 obiecte unice**, 136 duplicate de conținut omise.
- Schema: `SHA256 -> {storage:'release-zip-entry',release,asset,archiveSha256,entry,bytes}`.
- Executorul și auditorul au primit schema și rezultatele; nu am extras fișierele pe filesystem și nu am încărcat duplicate.

Am completat și dovezile căutării surselor originale pentru toate cele patru pachete în `source-search.json`, cu lista celor 67 de repository-uri oficiale inspectate.

## Asistent

Am creat `VERSION-DIFFS.json` și `VERSION-DIFFS.md` pentru toate cele 14 intrări, cu cele 10 comparații cerute și liste complete de fișiere identice, schimbate, adăugate și eliminate.

Constatări importante:

- Fiecare variantă FY diferă de APK-ul implicit prin trei fișiere de semnătură și două biblioteci native. DEX și `channel.config` sunt identice.
- Două perechi Bavvo au seturi diferite de splituri ABI/limbă/densitate; acestea sunt separate de presupuse modificări funcționale.
- Loomy și AINOTE au câte un singur input, deci nu există perechi de versiuni.

Numărătorile au fost validate. Auditorul și executorul au primit rezultatele; manifestele executorului nu au fost modificate.

## Asistent

Am creat în `decompilation-repair-2026-11-01/`:

- `INVENTORY.json` și `.md`: 14 variante, 11 grupuri DEX, loguri/erori declarate și hashuri; zero DEX-uri integral identice între grupuri diferite.
- `inventory.cjs`: reproducere read-only.
- `STRATEGY.md`: diagnostic separat pe tipuri de erori, corelare conservatoare, pilot cu moduri JADX alternative și gate-uri de audit înaintea corecturilor/publicării.

HeyCyan este inclus obligatoriu ca extensie distinctă: al 15-lea input, 20 componente APK, fără decompilare anterioară.

Am coordonat ownership-ul cu executorul și am solicitat auditorului gate-ul strategiei. Nu am lansat corecturi sau pilot și nu am modificat raw. API-ul Baksmali din JAR permite generarea Smali în memorie fără CLI-ul defect; poate fundamenta corelarea după aprobare.

## Asistent

Corelarea este implementată și auditată independent **10/10**.

- 28/28 fixtures și smoke API validate.
- Export Smali pentru 6 clase: 147 metode, fără erori API.
- Comparație Material pe 9 inputuri: 18 clase, 2 referințe reutilizate, 16 exporturi noi deduplicate în 7 obiecte.
- Cele două clase/metode sunt identice conservator în Bavvo 1179–1222.
- Bavvo 1112 și cele trei grupuri Translate diferă; rămân probe pentru analiză manuală.

Rezultate: `correlation/targeted-correlation-results.json` și `TARGETED-CORRELATION-RESULTS.md`. Gate final: `audit/TARGETED-CORRELATION-RESULTS.json`.

Nu am promovat Java, modificat raw sau făcut commit.

## Asistent

La commitul `4792f6b`, păstrarea structurii și codului este susținută de rapoarte; păstrarea tuturor funcțiilor nu este încă demonstrată.

| Funcție | Full-rebuilt | România40 |
|---|---|---|
| Instalare și pornire | Confirmate pe Galaxy A14, Android 14 | Netestate |
| Interfață engleză, profil, pagini SMS/parolă | Confirmate vizual | Netestate |
| Selector țări originale | +86, +852, +853 confirmate | Păstrare verificată static |
| Selector +40 și validare număr | Nu există | 22 teste ARM64 trecute; interfața reală netestată |
| SMS, autentificare, acceptare server | Netestate | Netestate |
| Conectare ochelari, Bluetooth, audio, traducere, OTA | Netestate | Netestate |
| Flutter, GC și stabilitate îndelungată | Fără verificare completă | Fără verificare pe telefon |

Dovezile statice pentru full-rebuilt: 80 biblioteci native și 1.046 assets identice; 47.044 fișiere Smali identice, alte 175 acceptate prin normalizare; zero diferențe nerezolvate în comparația decodată. România40 schimbă exclusiv `libapp.so` față de această bază, păstrând cele șase DEX, manifestul și celelalte componente.

`Compare-Decoded.cjs` verifică Smali, resurse și manifest. Nativele și assets depind de auditul separat. Normalizarea verifică textul instrucțiunilor și acoperirea handlerilor; nu dovedește comportamentul aplicației, acceptarea certificatului local de către server sau corectitudinea patchului în execuție Flutter.

Nu există în aceste rapoarte o matrice exhaustivă a funcțiilor originalului și teste pentru fiecare. Prin urmare, formularea justificată este „reconstrucție verificată static, cu test limitat de instalare și interfață”, nu „toate funcțiile originale verificate”. Nu am modificat fișiere, checkout sau commit.
