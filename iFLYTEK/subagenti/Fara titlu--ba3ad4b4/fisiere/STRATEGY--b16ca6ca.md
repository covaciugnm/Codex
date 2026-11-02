# Strategie verificabila pentru erorile decompilarii

Data: 1 noiembrie 2026. Rol: manager/arhitect. Stare: **propusa pentru audit; pilotul si corecturile nu sunt autorizate de acest document pana la gate-ul auditorului**. Rezultatele vechi si APK-urile brute raman neschimbate. Nu se face commit in aceasta etapa.

## Obiectiv si limite

Obiectivul este recuperarea verificabila a cat mai mult cod decompilat corect, prin diagnosticul tuturor erorilor, corelarea versiunilor, rulari alternative controlate si comparatie cu DEX/Smali/CFG. Fiecare problema trebuie sa primeasca o rezolutie explicita, inclusiv atunci cand nu poate fi transformata sigur in Java structurat. Eliminarea unui mesaj de eroare sau inlocuirea unei metode cu un `return` inventat nu reprezinta reparare.

Un scor 10/10 de audit poate certifica indeplinirea criteriilor unei etape, nu faptul ca un decompilator recupereaza sursa originala in toate cazurile. `recovered-java`, `fallback-only`, `smali-only`, `unresolved` si `not-a-decompiler-error` sunt stari distincte. Problemele din ultimele stari nu vor fi raportate drept Java reparat. Daca obiectivul de recuperare Java pentru toate metodele nu poate fi atins, raportul final pastreaza numarul si motivele problemelor ramase.

## Acoperire

[INVENTORY.json](INVENTORY.json) si [INVENTORY.md](INVENTORY.md) identifica 14 variante deja procesate, grupate in 11 seturi DEX. Cele trei variante Translate 3899 implicit/FY10030001/FY10030002 impart acelasi set DEX; full-rebuilt/romania40 impart alt set. Nu exista un DEX intreg identic intre doua grupuri DEX diferite, conform SHA-256-urilor din manifestele existente. Nu se lanseaza din nou aceeasi analiza pentru variante cu acelasi set DEX.

HeyCyan `com.glasssutdio.wear` 1.0.173_20261017 este inclus obligatoriu ca extensie distincta in acelasi proiect: XAPK cu 20 de componente APK, inclusiv baza. Nu exista decompilare anterioara pentru acesta in cele 11 grupuri. Extensia necesita extragere, identificare seturi DEX si baseline de erori proprii, inainte de corecturi; nu se presupune compatibilitate cu XF-AIGlasses-01. Repararea seturilor existente nu trebuie prezentata drept acoperire automata a HeyCyan. Totalul inputurilor proiectului este astfel 15; numarul final al seturilor DEX se recalculeaza dupa inspectarea extensiei.

## Separarea responsabilitatilor

- Arhitect: inventar, strategie, criterii de corelare si acoperire, fara rescrierea rezultatelor vechi.
- Executor: diagnosticul reproductibil in `tools/repair-diagnostics-20261101.cjs`, rularile alternative si artefactele candidate numai dupa gate. Workroot separat: `D:/Codex-iflytek-decompilation-repair-20261101`.
- Auditor: verificare independenta si registru de gate-uri in `decompilation-repair-2026-11-01/audit`. Orice neconformitate se intoarce la executor/arhitect. Managerul nu poate autoaproba propriile rezultate.

## Etapa 1: baseline si diagnostic

Se pastreaza pentru fiecare grup: input APK/component, SHA APK si DEX, versiunea/hashul JAR JADX, versiunea Java, comanda si parametrii, logul integral, codul de iesire, inventarul Java anterior si hashurile artefactelor. Baseline-ul reutilizat 3899 are 301 erori declarate; acest numar nu trebuie confundat cu metodele care au ramas nerecuperate.

Diagnosticul numara separat:

1. Erorile raportate de tool in log si iesirile procesului, inclusiv eventualele esecuri de incarcare, plugin sau memorie.
2. Metodele care contin stubul generat `Method not decompiled`, cu clasa si prototipul DEX identificabile. O exceptie `UnsupportedOperationException` valida din aplicatia originala nu este automat un esec JADX.
3. Marcajele `JADX ERROR`, `JADX WARNING`, structurile suspecte, dumpurile omise si blocurile cu instructiuni comentate. Numerele de marcaje, fisiere si metode sunt distincte.
4. Erorile de reconstructie Java care nu corespund unui stub, cu tipul exact si contextul disponibil.

Erorile loaderului privind arhive incluse ca asset, de exemplu `shu_priory_oaid.zip`, se clasifica separat de esecurile decompilarii metodelor. Se verifica structura si rolul intrarii fara executare. O arhiva asset care nu este DEX nu se transforma artificial intr-o eroare de metoda si nici nu se sterge din APK pentru a reduce contorul. Daca instrumentul permite selectarea explicita a DEX-urilor verificate, aceasta se poate testa intr-un run separat, cu acoperire si inputuri documentate.

Fiecare problema are ID stabil derivat din grupul DEX, identitatea simbolica a metodei si categoria problemei. Registrul contine sursa dovezii, textul relevant, calea si linia; lipsa unei identitati de metoda se marcheaza, nu se inventeaza. Sursele deja publicate se refera prin hash/cale/asset, fara duplicate.

**Gate 1:** auditorul verifica independent inventarul, distinctia metrice/metode, maparea 11->14, conservarea baseline-ului si disponibilitatea intrarilor. Nu se incepe pilotul pana cand strategia si diagnosticul nu au 10/10 conform rubricii declarate.

## Etapa 2: corelare intre versiuni

Prima oportunitate sigura este identitatea intregului set DEX: aceeasi analiza poate fi referita de variantele identice. Pentru grupurile diferite, aceeasi cale Java sau acelasi nume obfuscat nu probeaza aceeasi metoda.

Un fingerprint de metoda acceptabil trebuie sa identifice prototipul si sa normalizeze referintele din instructiuni la simbolurile rezolvate (tipuri, campuri, metode, stringuri, call-sites/method-handles), nu la indicii numerici din DEX. Se includ fluxul de control si tintele, tabelele catch/try si tipurile lor, cheile si tintele switch, continutul array payload, constantele si instructiunile relevante. Egalitatea octetilor `code_item` din DEX-uri diferite este insuficienta: aceiasi indici pot desemna simboluri diferite.

Se verifica si contextul clasei: descriptor, superclasa/interfete, campuri si initializari relevante, metodele de constructie/initializare si dependentele folosite de metoda. Renumirea registrelor sau alte transformari structurale sunt permise numai daca algoritmul este verificat prin teste pozitive si negative; preferam false-negative in locul unei echivalente false.

Un donor Java din alta versiune poate fi acceptat numai dupa probe de echivalenta a metodei si contextului si verificare independenta. Altfel este doar `comparison/suggestion`, fara patch automat. Chiar si un donor fara mesaje JADX poate fi semantic gresit; lipsa marcajelor nu este o dovada suficienta. O metoda din alta versiune care implementeaza o functie similara nu se copiaza ca si cum ar fi aceeasi implementare.

**Gate 2:** auditorul verifica parserul/fingerprintul pe perechi cunoscute identice si pe cazuri negative cu indici DEX egali dar simboluri diferite, proto diferit, catch/switch/array payload schimbat si context de clasa diferit. Fara 10/10 pe corelare, rezultatele raman sugestii.

## Etapa 3: pilot de rulari alternative

Matricea se confirma prin `--help` al JAR-ului exact 1.5.6 si se inregistreaza. Nu se presupune ca un flag disponibil intr-o alta versiune exista local. Fiecare run are director nou, inputuri imuabile, log complet si hashuri.

| Mod planificat | Scop | Limita |
|---|---|---|
| RESTRUCTURE cu `--show-bad-code --comments-level debug` | Pastreaza diagnosticul si dumpurile mari omise anterior | Java afisat poate fi inconsistent; necesita DEX/Smali/CFG |
| RESTRUCTURE cu `--no-inline-anonymous --no-inline-methods --no-inline-kotlin-lambda` si alte transformari confirmate local dezactivate | Verifica daca transformarile provoaca eroarea | Modifica forma Java si numele afisate; nu schimba DEX |
| SIMPLE | Reprezentare mai putin structurata pentru comparatie | Succesul procesului nu certifica Java semantic corect |
| FALLBACK | Dump de instructiuni pentru metodele dificile | Este reprezentare/fallback, nu sursa Java recuperata |
| `--cfg` / `--raw-cfg` pe clasa/metoda selectata | Control-flow normal si brut, utile verificarii independente | Grafurile pot fi voluminoase si nu inlocuiesc validarea semantica |
| Smali original sau exportat din DEX | Reprezentare de referinta pentru instructiuni | Nu se numeste Java reparat |

Se folosesc selectie de clasa/metoda unde CLI/API-ul suporta, numar redus de thread-uri si praguri de timp/memorie stabilite inainte de run. Nu se omit pachete din acoperirea finala doar pentru a obtine exit code 0. Rularile alternative nu suprascriu baseline-ul si nu declanseaza executarea APK-urilor.

Pilotul include minimum: o metoda cu stub, o eroare structurala, un dump omis/mare daca exista, un candidat de corelare cross-version daca exista, o eroare loader de asset daca exista, un caz original valid care ar putea fi confundat cu stubul si un control fara eroare. Selectia trebuie sa acopere atat cod de biblioteca cat si cod al aplicatiei daca ambele apar in diagnostic.

Pentru fiecare caz se pastreaza rezultatul fiecarui mod, diferenta fata de baseline, DEX/Smali/CFG si clasificarea propusa. Nu se trece la bulk pe baza numarului mai mic de mesaje sau a unui singur caz reusit.

**Gate 3:** auditorul evalueaza cazurile pilot si criteriile de selectie/acceptare, apoi permite bulk doar pentru transformarile care au 10/10. Modurile care produc numai fallback primesc aceasta eticheta; nu sunt acceptate ca recuperare Java.

## Etapa 4: acceptarea unei reparatii

Un candidat `recovered-java` necesita identitate de metoda verificata, verificarea fluxului de control si a cailor de exceptie fata de DEX/Smali, pastrarea apelurilor/campurilor/constantelor relevante si dovezi pentru orice donor. Compilarea metodei/codului atunci cand este posibila reprezinta doar un control suplimentar; un cod compilabil poate ramane semantic incorect. DEX recompilat poate avea structura binara diferita, deci simpla inegalitate a hashului nu este verdict semantic.

Orice editare manuala trebuie sa aiba un patch minim, justificare pe instructiuni, dovezi verificabile si revizuire independenta. Nu sunt acceptate: metode goale, valori implicite inventate, eliminarea catch-urilor, mutarea comentariilor pentru a ascunde erori sau declararea numelor originale recuperate fara probe. Daca verificarea nu este suficienta, candidatul nu se promoveaza.

Se foloseste un registru cu `problemId`, `baselineEvidence`, `attempts`, `candidate`, `verification`, `auditorDecision`, `resolution`. Patchurile se aplica numai in directorul de rezultate al etapei. Se poate reveni la orice input prin hash; raw, Java vechi si rapoartele anterioare raman disponibile.

**Gate 4:** fiecare lot de rezultate este auditat inainte de promovare/publicare. Auditorul poate cere reexecutarea, un caz negativ sau retragerea unui candidat; etapa se reia pana la indeplinirea rubricii, fara a transforma necunoscutele in afirmatii certe.

## Etapa 5: consolidare si livrare

Raportul final prezinta pentru fiecare dintre cele 11 grupuri si 14 variante deja existente, plus extensia obligatorie HeyCyan: probleme initiale, reparate in Java cu dovezi, fallback-only, smali-only, erori reale ale aplicatiei si nerezolvate. HeyCyan ramane rand separat, cu propriul baseline. Native Dart AOT/C/C++ sunt distincte de DEX; erorile de decompilare Java nu sunt dovada recuperarii surselor lor originale.

Livrarea pastreaza CAS/deduplicarea existente: obiectele identice deja in Git/Release sunt referite, iar numai continutul nou se publica dupa verificare. Rezultatele sunt materializabile separat pe versiune. Rapoartele si gate-urile sunt revizuite inainte de orice commit; niciun commit nu se face fara auditul explicit al etapei.

## Surse metodologice

[JADX Troubleshooting Q&A](https://github.com/skylot/jadx/wiki/Troubleshooting-Q%26A), verificat la 1 noiembrie 2026: documentatia oficiala explica limitele reconstructiei, consultarea Smali/CFG, `--comments-level debug` pentru dumpuri omise, `--cfg`/`--raw-cfg` si dezactivarea transformarilor de inlining. Matricea concreta de flags ramane verificata si fata de CLI-ul local, nu numai fata de wiki.

Baseline local: `tools/decompile-apk-versions-20261101.cjs`, manifestele `apk-analysis-2026-11-01/decompilation/`, `D:/Codex-iflytek-apk-analysis-20261101/decompile-jobs.json` si logurile `jadx-<dexSetSha256>.log`. Scriptul [inventory.cjs](inventory.cjs) reproduce maparea si inventarul fara corecturi.
