# Plan numeric: corelare Smali read-only

Stare: propunere de gate separat pentru dezvoltarea uneltelor de corelare, fara pilot JADX, patch sau transfer Java. Arhitectul detine `correlation/`; executorul detine `tools/repair-diagnostics-20261101.cjs` si diagnosticul/pilotul. Inputurile si rezultatele anterioare raman neschimbate.

## Interfata si artefacte

API local confirmat prin `javap` in JAR-ul existent `D:/Codex-iflytek-apk-analysis-20261101/jadx/lib/jadx-1.5.6-all.jar`: `DexFileFactory.loadDexContainer`, `ClassDefinition(BaksmaliOptions,ClassDef).writeTo(BaksmaliWriter)`, `ClassDefinition.hadValidationErrors`. CLI-ul Baksmali din acel JAR nu este utilizabil local din cauza `NoSuchMethodError JCommander.getMainParameter`; nu se presupune ca este functional.

Un adaptor Java foloseste API-ul direct, cu `StringWriter` pentru fiecare clasa. Optiuni explicite: `debugInfo=false`, `sequentialLabels=true`, `implicitReferences=false`, `parameterRegisters=false`, `localsDirective=false`, `codeOffsets=false`, `accessorComments=false`, `normalizeVirtualMethods=false`, `registerInfo=0`, `allowOdex=false`, `deodex=false`. Nu se descarca dependinte si nu se ruleaza codul APK.

Fisierul Smali este deja simbolic: referintele numerice DEX sunt rezolvate de dexlib2/Baksmali la tipuri/campuri/metode/prototipuri. Normalizarea suplimentara este conservatoare: elimina numai linii debug (`.source`, `.line`, `.local`, `.end local`, `.restart local`, `.prologue`, `.epilogue`), comentarii complete de metadata, linii goale si diferente de indentare/final de linie. Pastreaza literalurile, registrele, labels, catch/try, switch, array payload, annotations si toate instructiunile. Nu redenumeste registre, clase sau metode.

Pentru fiecare clasa se calculeaza hashul intregului ClassDef Smali normalizat, hashul contextului fara corpuri de metoda si hashuri pentru fiecare metoda cu declaratia/prototipul inclus. Egalitatea ClassDef + metoda este numai candidat conservator de corelare. Nu autorizeaza copierea Java: aliasurile, inlining-ul si dependentele externe pot schimba reprezentarea decompilata.

Artefacte asteptate:

- `correlation/SmaliFingerprintExport.java`: adaptorul API.
- `correlation/normalize-smali.cjs`: normalizare, parser de sectiuni si hashuri.
- `correlation/test-normalize-smali.cjs`: fixtures independente de APK.
- `correlation/run-correlation.cjs`: orchestrare cu verificarea inputurilor si bugete.
- `correlation/fixture-results.json`: rezultate, asteptari si hashul implementarii.
- `correlation/smoke-results.json`: comanda, buget, input/tool hash, clase gasite si validationErrors.
- Workroot `D:/Codex-iflytek-decompilation-repair-20261101/correlation/`: clase compilate, loguri, exporturi NDJSON si Smali selectat pentru probe; nu se adauga automat in Git.
- `correlation/correlation-results.json`: metadate si candidate read-only, zero patchuri Java.

## Matrice concreta de comenzi si bugete

Java/Javac: `C:/Program Files/Java/jdk-21/bin/java.exe` / `javac.exe`; versiunea si hashul JAR-ului se inregistreaza in dovezi. Caile workroot se transmit prin argumente, fara shell interpolation din date APK.

1. Fixtures: `node decompilation-repair-2026-11-01/correlation/test-normalize-smali.cjs`; maximum 30 secunde, un proces Node, fara acces la retea sau APK.
2. Compilare adaptor: `javac -cp <jadx-all.jar> -d <workroot>/classes <repo>/decompilation-repair-2026-11-01/correlation/SmaliFingerprintExport.java`; maximum 60 secunde; fara executare APK.
3. API smoke: `java -Xmx512m -cp <classes>;<jadx-all.jar> SmaliFingerprintExport <Bavvo1222-base.apk> <smoke-output.ndjson> Lcom/iflytek/bavvo/MainActivity;`; maximum 60 secunde, un thread. Inputul componentului are SHA `1ecd3388f4749f4863fc1731adfce27e6530d7d842d548c83bf36dda1fb2d939`; acesta se verifica inainte. Clasa exista in exportul anterior, dar adaptorul trebuie sa confirme descriptorul exact in DEX.
4. Dupa smoke validat: export serial, maximum un JVM simultan, `-Xmx2g`, un thread, maximum 20 minute/grup. Cele 11 grupuri existente sunt deduplicate la intrare; HeyCyan se adauga numai dupa identificarea setului sau DEX si baseline-ul separat. Nu se afirma ca rularile au avut loc pana nu exista log si manifest.
5. Exporturile pot fi limitate la reuniunea claselor identificate de diagnostic pentru a mentine volumul controlat; orice filtru exact si clase negasite sunt inregistrate. Un run filtrat nu se prezinta ca analiza tuturor claselor.

Prag de disc pentru etapa: 5 GB de output nou in workroot; la depasire se opreste extinderea, se raporteaza si se reevalueaza formatul. Inputurile de sute de MB sunt citite ca artefacte, fara executare. Nu se lanseaza thread-uri suplimentare de baksmali.

## Fixtures minime (22)

| Nr | Modificare controlata | Asteptare |
|---:|---|---|
| 1 | CRLF vs LF | acelasi fingerprint |
| 2 | adaugare `.line` | acelasi fingerprint |
| 3 | `.local` / `.end local` / `.restart local` | acelasi fingerprint |
| 4 | comentariu complet de metadata | acelasi fingerprint |
| 5 | literal string cu `#` modificat | fingerprint diferit; nu este comentariu |
| 6 | valoare string diferita | diferit |
| 7 | referinta simbolica field diferita | diferit |
| 8 | referinta simbolica method diferita | diferit |
| 9 | prototip method diferit | diferit |
| 10 | field/context clasa diferit | ClassDef/context diferit, donor respins |
| 11 | tip catch diferit | diferit |
| 12 | cheie packed/sparse switch diferita | diferit |
| 13 | tinta switch diferita | diferit |
| 14 | array-data payload diferit | diferit |
| 15 | registru diferit | diferit; fara register normalization |
| 16 | label diferit | diferit; fara redenumire arbitrara |
| 17 | annotation semantica diferita | diferit |
| 18 | metoda fara `.end method` | eroare explicita, fara hash acceptat |
| 19 | descriptor de metoda duplicat | eroare explicita, fara donor |
| 20 | `.source` diferit | acelasi fingerprint |
| 21 | spatii in interiorul literalului schimbate | diferit |
| 22 | implementare/instructiune schimbata | diferit |

Se adauga cel putin un test API care verifica rezolvarea simbolica pe o clasa reala si hashul DEX/inputului. Fixtures de normalizator nu demonstreaza singure corectitudinea parserului DEX; API-ul este identificat si inputurile sale sunt verificate separat.

## Reguli stop, regresie si gate

Oprire imediata la: hash/dimensiune input sau JAR neconforme, fixture esuat, compilare/API error, `hadValidationErrors=true`, descriptor/clasa negasita, metoda duplicata, parse incomplet, lipsa outputului, timeout, limita de memorie sau disc. Rezultatul se marcheaza incomplet si nu furnizeaza donori acceptati. Nu se ignora exit codes si nu se revine tacit la numele Java.

Outputul unei rulari trebuie sa fie separat si complet auditabil. Snapshoturile raw si Java anterioare nu se modifica; reutilizarea unui rezultat necesita potrivirea input/tool/options SHA. Auditorul verifica independently rezultatele fixtures si cel putin o clasa/metoda exportata. O schimbare a normalizatorului sau optiunilor invalideaza fingerprinturile anterioare pana la reexecutare.

Gate-ul cerut aici autorizeaza numai implementarea si testarea uneltei read-only, apoi smoke-ul API numeric de mai sus. Pilotul JADX si orice donor/patch Java raman la gate-urile separate din STRATEGY.md. Daca nu exista donori confirmabili, rezultatul legitim este zero donori, cu masuratori si motive; nu se inventeaza o reparatie pentru obtinerea scorului.
