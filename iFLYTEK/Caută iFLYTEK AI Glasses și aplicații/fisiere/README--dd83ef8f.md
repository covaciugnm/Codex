# iFLYTEK — documentație, aplicații și analiză tehnică

[Skillul oficial 讯飞翻译, TransAAS CLI și catalogul public Loomy](loomy-translate-skill-2026-11-01/README.md): descărcări noi, verificări și [dovezile privind SUA/UE și contul internațional](loomy-translate-skill-2026-11-01/INTERNATIONAL.md).

[Analiza separată a versiunilor APK/XAPK](apk-analysis-2026-11-01/README.md): inventar, despachetare, decompilare statică, comparații și audit independent, cu reutilizarea fișierelor existente.

Comparația a identificat [resurse cu nume confundate de Windows în vechea extracție raw](apk-analysis-2026-11-01/BASELINE-RAW-FINDING.md). Noul inventar le păstrează separat.

[Căutare extinsă în magazine, descrieri, Help și QR](retailer-audit-2026-11-01/README.md): clienți desktop Translate, extensii Chrome/Edge, skill Loomy și CLI-uri suplimentare, cu linkuri și SHA-256.

## Colecție suplimentară — 1 noiembrie 2026

[Inventarul aplicațiilor, versiunilor, documentației și SDK-urilor verificate](collection-2026-11-01/README.md) include arhivele Bavvo, aplicațiile iFLYTEK Translate și Loomy, sursele și rezultatele verificării duplicatelor. Fișierele mari sunt în [Release-ul software](https://github.com/covaciugnm/iFLYTEK/releases/tag/iflytek-software-2026-11-01). După clonare, restaurarea și verificarea colecției se fac cu `node tools/verify-collection-20261101.cjs --restore`. Ediția UE și compatibilitatea Bavvo cu modelul XF-AIGlasses-01 nu sunt confirmate.

Arhiva iFLYTEK din 30–31 octombrie 2026 cuprinde **34.466 de fișiere și 4.946.780.973 de octeți**. Sunt păstrate structura folderelor și conținutul original al fișierelor: pagini de la producător și traduceri, aplicații descărcate, SDK-uri și exemple, APK extras, clase Java/Smali, biblioteci native, inventare, dicționare, protocol, analiza firmware și audituri.

- [Index HTML principal](iFLYTEK_XF-AIGlasses-01_Documentatie/INDEX.html)
- [Software și cod sursă](iFLYTEK_XF-AIGlasses-01_Documentatie/Software/INDEX.html)
- [Aplicații, Bluetooth, Glasses și AINOTE](iFLYTEK_XF-AIGlasses-01_Documentatie/Software/Biblioteca_Glasses/INDEX.html)
- [APK reconstituit](iFLYTEK_XF-AIGlasses-01_Documentatie/Software/APK_Reconstituit_2026-10-30/INDEX.html)
- [Dicționar de parametri și catalog de funcții](iFLYTEK_XF-AIGlasses-01_Documentatie/Software/APK_Reconstituit_2026-10-30/catalog-parametri-functii/INDEX.html)
- [Protocol de comunicare](iFLYTEK_XF-AIGlasses-01_Documentatie/Software/APK_Reconstituit_2026-10-30/protocol-comunicare/INDEX.html)
- [Analiza firmware](iFLYTEK_XF-AIGlasses-01_Documentatie/Software/APK_Reconstituit_2026-10-30/firmware-analiza/INDEX.html)
- [Reverificarea detaliilor și limitele rămase](iFLYTEK_XF-AIGlasses-01_Documentatie/Software/APK_Reconstituit_2026-10-30/reverificare-detaliata/INDEX.html)
- [Auditul documentației](iFLYTEK_XF-AIGlasses-01_Documentatie/Software/APK_Reconstituit_2026-10-30/audit-calitate/INDEX.html)
- [Manifest complet cu SHA-256](iflytek-manifest-sha256.json)
- [Fișiere mari și căile de restaurare](IFLYTEK_RELEASE_ASSETS.md)

## Descărcarea arhivei complete

**34.438 de fișiere sunt stocate direct în Git. Cele 28 de fișiere de minimum 25 MiB sunt păstrate în [release-ul iFLYTEK](https://github.com/covaciugnm/iFLYTEK/releases/tag/iflytek-documentation-2026-10-31)**, ca 27 de atașamente distincte: două copii identice ale APK-ului folosesc același atașament. Un simplu `git clone` sau „Download ZIP” nu include aceste fișiere mari.

Cu Node.js 18+ și GitHub CLI (`gh`) autentificat într-un cont cu acces de citire la acest repository privat:

```sh
gh repo clone covaciugnm/iFLYTEK
cd iFLYTEK
node tools/restore-iflytek-assets.cjs
node tools/verify-iflytek-snapshot.cjs
```

Scriptul descarcă atașamentele, verifică dimensiunile și SHA-256 și le pune la toate căile originale. Poate fi reluat; fișierele deja corecte sunt păstrate, iar cele diferite provoacă o eroare. O cheie SSH de deploy permite accesul Git conform drepturilor ei; descărcarea atașamentelor private prin `gh` folosește autentificarea GitHub CLI.

Pentru atașamente descărcate deja manual, păstrează numele lor din release și folosește `node tools/restore-iflytek-assets.cjs --from-dir "cale/catre/atasamente"`. Verificarea exclusiv a fișierelor din Git se face cu `node tools/verify-iflytek-snapshot.cjs --git-only`.

După restaurare, deschide local `iFLYTEK_XF-AIGlasses-01_Documentatie/INDEX.html` în browser. GitHub afișează sursa paginilor HTML. Documentele originale și constatările cercetării sunt păstrate în forma lor existentă; încărcarea verifică integritatea copiei și nu reprezintă o nouă validare pe dispozitiv. Modelul exact, versiunile dispozitivului utilizatorului și un pachet OTA real rămân necesare pentru verificările hardware.

## AI Glasses 2026 — cercetare și catalog comparativ

Snapshot încărcat la 31 octombrie 2026. Cercetarea din document este datată 30 octombrie 2026, revizia 2 China–Europa.

- **10 producători, 93 fișe, 140 câmpuri și 183 surse.** Fișele includ variante regionale, produse istorice, prototipuri și precomenzi, marcate distinct.
- [Catalog HTML autonom](AI_Glasses_2026/AI_Glasses_2026.html)
- [Pachet ZIP pentru descărcare](AI_Glasses_2026/AI_Glasses_2026_Livrare.zip)
- [Template aprobat](AI_Glasses_2026/template-analiza-v3.html)
- [Audit și re-audit](AI_Glasses_2026/audit-final.html)
- [Date complete](AI_Glasses_2026/catalog-data.json)
- [Surse regionale China–Europa](AI_Glasses_2026/regional-sources.json)

Descarcă arhiva sau clonează repository-ul și deschide catalogul în Chrome/Edge. GitHub afișează codul HTML, nu aplicația interactivă. Documentul nu are nevoie de server; internetul este necesar pentru sursele externe.

## Reproducere

Cu Node.js instalat, din folderul AI_Glasses_2026:

```sh
node build.cjs
node validate.cjs
```

`qa.cjs` folosește Chrome pe Windows pentru verificarea filtrelor, exportului și afișării mobile. Rapoartele și capturile incluse au fost produse în mediul de lucru original. Scripturile `make-*`, `polish*`, `update-regions.cjs` și celelalte remedieri păstrează istoricul construcției; nu le rula în bloc, deoarece unele suprascriu fișe sau adaugă secțiuni. Datele `data-*.json` actuale sunt intrările pentru rebuild.

## Conținut și limite

Specificații, SDK/APK/iOS, reviewuri, achiziție, companions/tablete, surse oficiale China–Europa și ecosistem pentru dificultăți auditive. Necunoscut nu înseamnă Nu. Nu au fost testate dispozitive fizice și nu au fost compilate SDK-uri; stocurile și eficacitatea medicală nu sunt certificate.

Au fost incluse toate fișierele proiectului, inclusiv scripturile și capturile QA. Profilul temporar Chrome și descărcările temporare QA sunt excluse. Cheile SSH nu fac parte din proiect.
