Aplicația iFLYTEK Translate 1.0.3899 poate fi reconstruită din Smali și resurse. Varianta suplimentară adaugă **România (+40)** în selector și păstrează transmiterea țării separat, prin `ccode: "40"`.

**Baza recompilată a fost instalată și pornită pe Galaxy A14 / Android 14. Varianta +40 este construită și semnată, dar încă neinstalată și netestată pe telefon.** Cele 22 de teste ARM64 nu validează randarea Flutter, GC pe dispozitiv sau acceptarea contului de către server. Autentificarea SMS nu a fost eliminată; nu s-au trimis SMS-uri de test și nu s-a validat autentificarea în cloud.

Atașamente:

- `iflytek-1.0.3899-romania40.apk` — varianta nouă, pentru test pe dispozitiv.
- `iflytek-1.0.3899-full-rebuilt.apk` — baza recompilată, instalată și pornită anterior.
- `iflytek-1.0.3899-editable-source.zip` — Smali, resurse și biblioteci binare; nu este proiectul original Dart/C++.
- `iflytek-1.0.3899-aot-analysis.zip` — analiza Blutter și patch-ul nativ, cu inventar SHA-256 intern.
- `iflytek-20261031-analysis-toolchain.zip` — unelte Windows și Blutter/Linux, grupate separat, cu inventar SHA-256 intern.
- `SHA256SUMS.txt` — amprentele celor cinci artefacte.

[Ghid Ubuntu, instalare și Codex CLI remote](https://github.com/covaciugnm/iFLYTEK/blob/build/reproducible-apk-20261031/CONTINUARE-UBUNTU.md) · [Proiect și dovezi](https://github.com/covaciugnm/iFLYTEK/tree/build/reproducible-apk-20261031/iFLYTEK_XF-AIGlasses-01_Documentatie/Software/APK_Recompilabil_2026-10-31).

Din branch-ul `build/reproducible-apk-20261031`, `node tools/restore-iflytek-apk-assets.cjs` restaurează și verifică artefactele; `--apk-only` selectează cele două APK-uri. Corpusul anterior rămâne în [release-ul de documentație](https://github.com/covaciugnm/iFLYTEK/releases/tag/iflytek-documentation-2026-10-31).

Cheia/parola locală de semnare și datele private ale telefonului nu sunt publicate. Cele două APK-uri folosesc același certificat local, diferit de cel al producătorului. Baza locală poate fi actualizată cu +40; instalarea peste aplicația oficială are conflict de semnătură și nu trebuie rezolvată prin dezinstalare automată.
