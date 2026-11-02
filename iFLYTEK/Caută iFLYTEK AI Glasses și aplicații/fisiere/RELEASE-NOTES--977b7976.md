Analiză statică pentru **14 APK/XAPK distincte**, cu directoare separate pentru fiecare aplicație, versiune și variantă. Sunt păstrate **24.333 de fișiere raw**, rezultatele celor **11 seturi DEX** și jurnalele de decompilare. Variantele `full-rebuilt` și `romania40` sunt derivate locale, separate de distribuțiile furnizorilor.

Cele cinci pachete TAR.GZ conțin **52.767 de obiecte noi**, verificate după SHA-256. Conținutul deja publicat în Git sau în Release-urile anterioare este reutilizat prin referințe; APK-urile de intrare nu sunt încărcate din nou.

- [Catalog, versiuni și rapoarte](https://github.com/covaciugnm/iFLYTEK/blob/research/ai-glasses-2026-10-31/apk-analysis-2026-11-01/README.md)
- [Restaurarea directoarelor și deschiderea fișierelor](https://github.com/covaciugnm/iFLYTEK/blob/research/ai-glasses-2026-10-31/apk-analysis-2026-11-01/LIVRARE.md)
- [Inventarul pachetelor și hashurilor](https://github.com/covaciugnm/iFLYTEK/blob/research/ai-glasses-2026-10-31/apk-analysis-2026-11-01/release-packs.json)
- [Audit independent și testele efectuate](https://github.com/covaciugnm/iFLYTEK/tree/research/ai-glasses-2026-10-31/apk-analysis-2026-11-01/audit)
- [Resursele pierdute sau etichetate greșit în vechea extracție raw Windows](https://github.com/covaciugnm/iFLYTEK/blob/research/ai-glasses-2026-10-31/apk-analysis-2026-11-01/BASELINE-RAW-FINDING.md)

Din repository-ul clonat, cu Node.js și `gh` autentificat:

```powershell
node tools/restore-apk-analysis-20261101.cjs --store-dir D:/iflytek-analysis-store
node tools/prefetch-apk-existing-git-20261101.cjs
node tools/materialize-all-apk-versions-20261101.cjs --store-dir D:/iflytek-analysis-store --output D:/iflytek-versions
```

`PATH-MAP.json` păstrează fiecare nume original și calea fizică distinctă pe Windows. Fișierele reprezintă extracția APK și cod Java decompilat; erorile JADX sunt documentate. Nu a fost găsit proiectul original public și nu se pretinde recuperarea sursei Dart/C++ sau a unui proiect recompilabil pentru fiecare aplicație. Nu s-a executat niciun APK în această activitate.
