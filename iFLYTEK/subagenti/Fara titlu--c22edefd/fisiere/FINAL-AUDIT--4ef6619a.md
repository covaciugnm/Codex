# Audit independent — noua colecție Loomy / TransAAS / alte modele

**Scor final: 10/10 pentru integritatea și livrarea arhivei.** Nu există probleme tehnice sau afirmații funcționale nejustificate rămase deschise. Publicarea și commitul remote au fost verificate independent la 1 noiembrie 2026, 15:36 UTC. Auditul anterior al APK-urilor rămâne nemodificat; acest raport privește exclusiv noua colecție. Scorul nu confirmă asocierea sau activarea XF-AIGlasses-01 în UE.

## Integritate și acoperire

- Au fost recitite toate cele **86 de artefacte**, **380.352.911 octeți**. Dimensiunile și SHA-256 corespund inventarului. Hashurile sunt unice și nu coincid cu cele din cele cinci inventare anterioare verificate: arhiva inițială, colecția aplicațiilor, auditul comercianților, CAS-ul APK și indexul arhivelor sursă/AOT.
- Catalogul public arhivat conține **67 de identificatori unici**; fiecare URL `download_url` este acoperit de o arhivă verificată, cu `SKILL.md`. Este păstrată separat și arhiva istorică `transaas01` 1.0.3. Aceasta nu reprezintă o afirmație că toate versiunile istorice posibile ale tuturor skillurilor au fost găsite.
- Au fost verificate independent **69 de arhive externe**: 68 ZIP-uri de skill și un XAPK HeyCyan. Au fost verificate și cele **20 de APK-uri interne** din XAPK. Pentru toate cele **4.196 fișiere membre** s-au comparat datele efective, dimensiunile, SHA-256 și CRC32 cu directorul central ZIP și inventarul; intrările de directoare au fost și ele controlate.
- Cele două manuale au antet PDF valid. Pachetele și documentația HeyCyan sunt etichetate pentru alt hardware; nu sunt prezentate drept compatibile cu XF-AIGlasses-01.
- Cele patru CLI-uri au antete și arhitecturi PE x64, Mach-O ARM64/x64 și ELF x64 corespunzătoare. Metadatele Go/revizia încorporată au fost confirmate static. Fiecare pereche HTTP/HTTPS are același hash în observațiile de descărcare. Nu s-a atribuit CLI-ului o versiune semantică neverificată prin rulare și nu se pretinde verificarea semnăturii editorului.

Dovezi și verificator independent: [collection-integrity-results.json](collection-integrity-results.json), [verify-collection-independent.cjs](verify-collection-independent.cjs).

## Restaurare

Scriptul autorului a fost exercitat într-un mediu izolat, cu transport GitHub simulat și date de test. **9/9 cazuri au trecut**: restaurare validă, respingerea datelor corupte, duplicatelor, traversărilor de cale, Release-ului greșit, numelui de activ greșit, digestului remote greșit și stării draft; metadatele remote corecte sunt acceptate. Nu s-au modificat fișierele colecției și nu s-a descărcat sau executat vreun payload în aceste teste.

Dovezi: [restorer-fixture-results.json](restorer-fixture-results.json), [test-restorer-independent.cjs](test-restorer-independent.cjs).

## SUA / UE: corectitudinea concluziilor

Au fost verificate independent biblioteca originală Bavvo de **19.628.636 octeți**, hashul său și prezența celor cinci domenii internaționale, cinci simboluri de e-mail și patru rute native. JavaScript-ul public arhivat are hashul declarat și cele patru rute de e-mail descrise. Acestea confirmă existența codului client și a componentelor publice, nu înregistrarea reușită a unui cont sau asocierea ochelarilor.

Observațiile Apple păstrate acoperă exact cele 27 de țări UE, UK și SUA. Un recontrol independent public a confirmat România `resultCount: 0` și SUA `resultCount: 1`, cu `com.iflytek.bavvo`, versiunea 1.0.1191. Catalogul Loomy nu a putut fi reinterogat în acest recontrol din cauza unei erori de rețea; verificarea sa privește snapshotul GET 200 păstrat și toate cele 67 de distribuții corelate, nu o disponibilitate garantată permanent.

Documentul `INTERNATIONAL.md` păstrează explicit distincțiile necesare: Google Play `gl=RO` HTTP 200 reprezintă o listare publică, nu un test de instalare; contul internațional prin e-mail este identificat static; Bavvo rămâne un candidat concret, fără compatibilitate XF confirmată; CLI-ul cu servere chinezești și HeyCyan nu sunt prezentate drept soluții garantate de activare pentru ochelarii utilizatorului în UE.

Dovezi: [international-evidence-results.json](international-evidence-results.json), [live-public-checks.json](live-public-checks.json).

## Criterii de închidere

| Criteriu | Puncte |
|---|---:|
| Inventar complet pentru scope-ul declarat | 1/1 |
| Integritatea tuturor artefactelor | 1/1 |
| Fără artefacte duplicate față de inventarele anterioare | 1/1 |
| Acoperirea catalogului și istoriei identificate | 1/1 |
| ZIP/XAPK și componente APK verificate | 1/1 |
| Proveniență și arhitecturi CLI verificate static | 1/1 |
| Restaurare și respingerea coruperii/metadatelor greșite | 1/1 |
| Dovezi internaționale și limite exprimate corect | 1/1 |
| Activitate numai de citire/descărcare, fără execuție sau acces la conturi | 1/1 |
| Publicare și verificare remote independentă | 1/1 |

Cele șase active ale [Release-ului publicat](https://github.com/covaciugnm/iFLYTEK/releases/tag/iflytek-loomy-skills-2026-11-01) au fost verificate independent: **353.305.015 octeți**, digesturi și dimensiuni corecte, `isDraft: false`. Ținta Release-ului și ref-ul remote al branchului au fost confirmate la commitul [`87ed86b8b5342c35941fd64a79c8773fab37f1b2`](https://github.com/covaciugnm/iFLYTEK/commit/87ed86b8b5342c35941fd64a79c8773fab37f1b2).

Pentru cele **80 de artefacte stocate în Git**, identificatorii de blob și dimensiunile remote corespund identificatorilor Git calculați din octeții locali deja verificați prin SHA-256. Fișierele `file-inventory.json`, `manifest.json`, `archive-entries.json` și `INTERNATIONAL.md` au fost citite direct din GitHub la commitul de publicare și comparate separat prin SHA-256 cu datele auditate. Dovezi: [remote-release-results.json](remote-release-results.json), [verificator remote independent](verify-remote-independent.cjs).
