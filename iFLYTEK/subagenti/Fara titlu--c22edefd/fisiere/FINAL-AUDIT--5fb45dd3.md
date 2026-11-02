# Audit independent — APK/XAPK pe versiuni

**Scor final: 10/10. Activitatea verificată este închisă.** Toate cele zece criterii au dovezi independente. Publicarea, commitul remote, cele cinci active Release și metadatele principale au fost reverificate la 1 noiembrie 2026, 14:13 UTC.

Scorul evaluează inventarierea, despachetarea statică, separarea versiunilor, comparația, deduplicarea și reproducibilitatea activității cerute. Nu înseamnă Java fără erori, recuperarea proiectelor originale Dart/C++ sau validarea funcțională a aplicațiilor, autentificării ori ochelarilor.

## Rezultate verificate independent

- **14 containere distincte**, dintre care 12 distribuite de furnizori și două derivate local, cu 15 referințe de proveniență. Toate APK-urile/XAPK-urile identificate în manifestele existente și cele patru Release-uri anterioare sunt acoperite.
- **24.333 fișiere logice raw**: toate containerele, componentele și fișierele au fost recitite din APK/XAPK și verificate prin SHA-256, dimensiuni și număr de intrări. Spliturile sunt păstrate separat.
- **11 seturi DEX distincte**: zece execuții CLI noi și o decompilare existentă reutilizată pentru DEX identic. Fiecare rezultat are proveniență, unelte, jurnale și limitări. Toate sunt parțiale, cu cod de ieșire 3; erorile efective din loguri sunt păstrate.
- **14 arbori fizici separați**, materializați complet. Auditorul a recitit fiecare dintre cele **223.652 fișiere de conținut**, însumând **3.897.567.974 octeți**, și a verificat SHA-256/dimensiunea, maparea logică, metadatele și absența fișierelor suplimentare. Cu cele două metadate per versiune rezultă **223.680 fișiere** în arborii versiunilor.
- **52.767 obiecte noi unice**, **1.280.952.058 octeți necomprimați**, în cinci pachete. Verificarea independentă în flux a recitit fiecare obiect și fiecare pachet comprimat; hashurile, dimensiunile, antetele/footer-ele TAR și integritatea gzip corespund.
- Niciun obiect CAS nou nu coincide prin SHA-256 cu fișierele din manifestul inițial, colecția precedentă, auditul comercianților sau intrările indexate din arhivele existente editable-source/AOT. APK-urile originale existente nu sunt reîncărcate ca noi containere în acest Release.

## Corecții obținute prin iterațiile de audit

1. Inventarul a fost extins de la cele 12 pachete furnizor la toate cele 14, incluzând cele două APK-uri derivate din Release-ul separat.
2. Restaurarea TAR respinge acum date trunchiate, padding/footer incomplet, antete cu checksum greșit, obiecte duplicate/neindexate, conținut corupt și traversări de cale.
3. Decompilarea folosește explicit `jadx.cli.JadxCLI`; încercările inițiale care porneau launcherul GUI sunt documentate drept întrerupte și înlocuite, fără a fi prezentate ca exporturi reușite.
4. Reutilizarea seturilor DEX identice include numai cod Java/metadate de build. Resursele, bibliotecile native și certificatele fiecărei variante rămân cele din APK-ul respectiv.
5. Referințele Git sunt fixate prin identificator de blob; materializarea verifică SHA-256 și dimensiunea conținutului. Lipsa sau coruperea CAS împiedică reutilizarea falsă a unui raport decompilat într-o clonă nouă.
6. Rularea reală a detectat coliziuni de nume Windows înainte de suprascriere. `PATH-MAP.json` păstrează acum injectiv și reversibil fiecare nume logic, componentă, cale fizică și hash. Au fost verificate toate cele 152 de căi remapate pentru fiecare APK Translate furnizor și cele opt pentru AINOTE.

Auditul a confirmat și o problemă istorică: vechiul arbore raw Translate conține 2.264 nume fizice pentru 2.341 intrări originale, cu 77 nume logice absente și 75 nume asociate conținutului altei variante de capitalizare. Manifestele raw noi sunt corecte față de APK și păstrează toate intrările. Artefactele istorice nu au fost modificate în loc; dovezile sunt în [baseline-case-loss.json](baseline-case-loss.json).

## Criterii

| Criteriu | Puncte | Dovadă principală |
|---|---:|---|
| Inventar complet | 1/1 | [release-inputs.json](release-inputs.json), [raw-input-results.json](raw-input-results.json) |
| Identitate, versiuni și splituri | 1/1 | Manifestele celor 14 versiuni; [raw-input-results.json](raw-input-results.json) |
| Integritatea și proveniența intrărilor | 1/1 | Toate hashurile/dimensiunile input și fișierelor raw recitite |
| Separarea versiunilor și variantelor | 1/1 | [all-materialized-tree-results.json](all-materialized-tree-results.json) |
| Acoperirea despachetării statice | 1/1 | 24.333 fișiere raw; toate componentele și metadatele |
| Rezultate și limite de decompilare | 1/1 | [decompilation-results.json](decompilation-results.json) |
| Comparație și deduplicare | 1/1 | [diff-results.json](diff-results.json), [final-pack-results.json](final-pack-results.json) |
| Disponibilitatea sursei și corectitudinea afirmațiilor | 1/1 | Căutare pe pachete exacte, lista oficială de repository-uri, limitări explicite |
| Reproducibilitate și integritatea materializării | 1/1 | Toate cele 14 arbori recitiți, unelte fixate, teste de corupere/restaurare/mapare/cache |
| Livrare și închidere independentă | 1/1 | Release publicat, cinci active cu digest/dimensiune corecte, commit remote și patru fișiere de metadate remote identice |

## Publicare verificată

- [Release-ul analizei](https://github.com/covaciugnm/iFLYTEK/releases/tag/iflytek-apk-analysis-2026-11-01) este publicat (`isDraft: false`). Cele cinci active însumează **509.801.336 octeți comprimați** și au exact dimensiunile și digesturile SHA-256 ale pachetelor verificate local.
- Commitul de publicare a datelor este [`91bc12a1524bb790b006c29fe6b27f41c3504ddd`](https://github.com/covaciugnm/iFLYTEK/commit/91bc12a1524bb790b006c29fe6b27f41c3504ddd), confirmat independent atât ca țintă a Release-ului, cât și ca ref remote al branchului la momentul verificării.
- `catalog.json`, `cas-index.json`, `release-packs.json` și `materialization-runs.json` au fost citite direct din GitHub la acel commit; SHA-256 și dimensiunile corespund exact fișierelor auditate. Dovada este în [remote-release-results.json](remote-release-results.json). Actualizarea ulterioară a raportului de închidere nu schimbă datele înghețate sau pachetele Release.

## Dovezi suplimentare

- [Runda 1](ROUND-1.md), [runda 2](ROUND-2.md), [runda 3](ROUND-3.md).
- [Restaurare: 12/12 cazuri](restore-fixture-results.json); [împachetare: 6/6 cazuri](package-fixture-results.json).
- [Fixture independent de mapare Windows: 11 fișiere](independent-path-mapping-results.json); [Translate FY1: toate cele 25.547 fișiere recitite](full-translate-mapped-results.json).
- [Cache de decompilare: 8/8 verificări independente](independent-reuse-results.json).
- [Verificarea remote a pachetelor](remote-release-results.json).

Nu s-au executat APK-urile în această activitate, nu s-au trimis SMS-uri și nu s-au accesat conturi sau date private. Nu a fost identificată o sursă originală publică în căutarea limitată documentată; rezultatele livrate sunt extracții și decompilări statice cu limitele lor.
