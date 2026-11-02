# APK/XAPK — analiză statică separată pe versiuni

[Audit independent final: 10/10 pentru activitatea de analiză și livrare](audit/FINAL-AUDIT.md).

[Deschiderea directoarelor fizice și restaurarea tuturor versiunilor](LIVRARE.md).

[Diferență confirmată în vechea extracție raw Translate: resurse cu nume confundate de Windows](BASELINE-RAW-FINDING.md).

Au fost inventariate **14 containere distincte**, cu 15 referințe de proveniență și **24333 fișiere logice**. Variantele cu același număr de versiune sunt păstrate separat. Conținutul identic este referit prin SHA-256, fără încărcări duplicate.

[Catalog complet](catalog.json) · [Index obiecte noi CAS](cas-index.json) · [Criterii și audit](audit/RUBRIC.md) · [Arhitectură](ARCHITECTURE.md)

## Versiuni

| Aplicație | Versiune / variantă | Intrări | Decompilare |
|---|---|---:|---|
| com.iflytek.bavvo | [1.0.1222 / bavvo-1.0.1222](versions/com.iflytek.bavvo/1.0.1222/bavvo-1.0.1222/README.md) | 1515 | complete-with-documented-limitations |
| com.iflytek.bavvo | [1.0.1211 / bavvo-1.0.1211](versions/com.iflytek.bavvo/1.0.1211/bavvo-1.0.1211/README.md) | 1514 | complete-with-documented-limitations |
| com.iflytek.bavvo | [1.0.1205 / bavvo-1.0.1205](versions/com.iflytek.bavvo/1.0.1205/bavvo-1.0.1205/README.md) | 1513 | complete-with-documented-limitations |
| com.iflytek.bavvo | [1.0.1197 / bavvo-1.0.1197](versions/com.iflytek.bavvo/1.0.1197/bavvo-1.0.1197/README.md) | 1513 | complete-with-documented-limitations |
| com.iflytek.bavvo | [1.0.1179 / bavvo-1.0.1179](versions/com.iflytek.bavvo/1.0.1179/bavvo-1.0.1179/README.md) | 1513 | complete-with-documented-limitations |
| com.iflytek.bavvo | [1.0.1112 / bavvo-1.0.1112](versions/com.iflytek.bavvo/1.0.1112/bavvo-1.0.1112/README.md) | 1469 | complete-with-documented-limitations |
| com.iflytek.translateapp | [1.0.3949 / translate-xlhs-current](versions/com.iflytek.translateapp/1.0.3949/translate-xlhs-current/README.md) | 2341 | complete-with-documented-limitations |
| com.iflytek.translateapp | [1.0.3899 / translate-channel-FY10030001](versions/com.iflytek.translateapp/1.0.3899/translate-channel-FY10030001/README.md) | 2341 | complete-with-documented-limitations |
| com.iflytek.translateapp | [1.0.3899 / translate-channel-FY10030002](versions/com.iflytek.translateapp/1.0.3899/translate-channel-FY10030002/README.md) | 2341 | complete-with-documented-limitations |
| com.ainote.mobile.doxent_oversea_app | [3.1.5 / AINOTE-Android](versions/com.ainote.mobile.doxent_oversea_app/3.1.5/AINOTE-Android/README.md) | 1093 | complete-with-documented-limitations |
| com.iflytek.loomy.mobile | [0.0.8 / Loomy-Android](versions/com.iflytek.loomy.mobile/0.0.8/Loomy-Android/README.md) | 163 | complete-with-documented-limitations |
| com.iflytek.translateapp | [1.0.3899 / iflytranslate-official](versions/com.iflytek.translateapp/1.0.3899/iflytranslate-official/README.md) | 2341 | complete-with-documented-limitations |
| com.iflytek.translateapp | [1.0.3899 / iflytek-1.0.3899-full-rebuilt](versions/com.iflytek.translateapp/1.0.3899/iflytek-1.0.3899-full-rebuilt/README.md) | 2338 | complete-with-documented-limitations |
| com.iflytek.translateapp | [1.0.3899 / iflytek-1.0.3899-romania40](versions/com.iflytek.translateapp/1.0.3899/iflytek-1.0.3899-romania40/README.md) | 2338 | complete-with-documented-limitations |

## Acces la fișiere

[Maparea reversibilă a numelor incompatibile cu Windows](PATH-MAPPING.md): fiecare director materializat include PATH-MAP.json, fără pierderea resurselor care diferă numai prin litere mari/mici.

Manifestele și paginile pentru fiecare versiune sunt în Git. Obiectele noi sunt împachetate în [Release-ul analizei](https://github.com/covaciugnm/iFLYTEK/releases/tag/iflytek-apk-analysis-2026-11-01); [release-packs.json](release-packs.json) păstrează hashurile pachetelor. Obiectele deja existente sunt referite prin calea Git sau prin intrarea exactă din arhivele Release anterioare.

```powershell
node tools/restore-apk-analysis-20261101.cjs --store-dir D:/iflytek-analysis-store
```

Apoi folosește comanda din pagina versiunii dorite pentru materializarea fișierelor sale. Nu este necesară instalarea aplicațiilor.

## Limite

Operația despachetează integral conținutul și verifică CRC32, SHA-256 și dimensiuni. JADX încearcă recuperarea Java/Kotlin din DEX; rezultatele și codurile de ieșire sunt păstrate. Erorile și codul incomplet nu sunt ascunse. Nu se pretinde recuperarea proiectului original, a sursei Dart Flutter AOT sau a unui proiect recompilabil pentru fiecare aplicație. Cele două APK-uri reconstruite/modificate anterior sunt etichetate distinct de cele ale furnizorului.

## Comparații și căutarea sursei originale

[Diferențe între versiuni și variante](VERSION-DIFFS.md) · [Datele comparației](VERSION-DIFFS.json) · [Căutarea surselor originale](source-search.json) · [Indexul arhivelor existente](baseline-release-index-audit.json) · [Notele execuției](execution-notes.json).
