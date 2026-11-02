# Pilot independent: rezultate si limite

Pilotul dex2jar 2.4 + CFR 0.152 a fost auditat 10/10 pentru executie/integritate in [INDEPENDENT-ENGINE-RESULTS.json](../audit/INDEPENDENT-ENGINE-RESULTS.json). Acest scor nu reprezinta acceptare semantica a surselor candidate.

- Doua DEX-uri Bavvo 1222 convertite, fara exception ZIP si cu exit 0.
- Toate cele 20 de clase closure si setul exact de 98 prototipuri root sunt prezente in classfiles; fara missing/empty/duplicate/unexpected Code. Parserul nu este validator JVM complet.
- CFR a emis Material2 fara marcaje, plus K6.d cu opt linii de diagnostic. Primul filtru JAR nu a emis a.b.
- Callback-ul direct a emis ulterior a/b.java, fara reconversie DEX, intr-un director nou. Rezultatul ramane `CANDIDATE-UNREVIEWED`.

## Callback a.b

JAR-ul convertit contine `A/b.class` si `a/b.class`; CFR confirma in help ca modul implicit case-insensitive redenumeste coliziunile. Retry-ul autorizat a folosit numai `a/b.class` si cele doua nested, cu `--caseinsensitivefs false` si ambele JAR-uri drept classpath.

Candidatul este in `D:/Codex-iflytek-decompilation-repair-20261101/independent-engine/callback-1793551823684/java/a/b.java`, SHA-256 `fa9b747b1dc81257e46c7367ab3dd0f42dbba591db67a8c9e7658a4fbee17d93`. Auditorul a identificat artefacte reale de tipare: `Object` folosit pentru HashMap urmat de apeluri `put`, precum si variabile de constructor anonymous nerecuperate. Absenta markerilor nu inseamna Java compilabil sau metoda recuperata. Fluxul poate servi drept proba suplimentara pentru review manual fata de Smali.

## K6: eroarea RegionMaker

Identitatea exacta este `LK6/d;->c1(ILjava/util/List;)V`, nu metodele k1 sau Y0 care au alte probleme. JADX a raportat `RegionMakerVisitor` si imposibilitatea identificarii splitter-ului unui handler inaintea stubului generat. Smali normalizat al metodei are SHA `983bd538ea9b6ddd499302edc8dfb43acb8abbdb976753bf7691cc0d74e02279`.

Referinta Smali auditata: `D:/Codex-iflytek-decompilation-repair-20261101/correlation/references-1793549463656/K6_d-0a2e2aa1.smali`.

CFR a produs `c1(int,List)` in `D:/Codex-iflytek-decompilation-repair-20261101/independent-engine/pilot-1793551545656/cfr-2/K6/d.java`, aproximativ liniile 441–495, dar cu `WARNING - void declaration`, declaratia invalida `void var2_5`, monitor-enter/exit convertite in comentarii si `throw var2_5` nerecuperat. Nu este o reparatie. Candidatul poate sprijini analiza control-flow si a catch/monitor-urilor, dar nu se promoveaza.

## Provenienta si continuare

[pilot-results.json](pilot-results.json) si [callback-results.json](callback-results.json) contin argv, bugete, loguri, hashuri, acoperire si diagnostice. Sursele anterioare si raw nu au fost modificate. Nu exista patchuri Java, APK recompilat sau commit din aceasta etapa.

Urmatoarea extindere vizeaza toate clasele cu stuburi din cele 11 grupuri istorice si grupul HeyCyan separat: 822 de markeri, nu 822 de metode unice demonstrate. Ownerii raw confirmati pot fi procesati in batch-uri controlate; aliasurile si legaturile de metoda neconfirmate raman pending explicit. Fiecare candidat necesita evaluare separata, chiar daca alt decompilator nu raporteaza erori.
