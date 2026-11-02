# Pilot bounded: dex2jar 2.4 + CFR 0.152

Stare: pregatire read-only finalizata; conversia DEX si decompilarea CFR asteapta gate-ul auditorului. Scopul este obtinerea unor surse candidate independente de JADX, nu promovarea lor ca Java corect sau sursa originala.

## Provenienta si pregatire

Distributii oficiale descarcate direct in `D:/Codex-iflytek-decompilation-repair-20261101/independent-engine/toolchain/`:

| Artefact | Octeti | SHA-256 |
|---|---:|---|
| [dex-tools-v2.4.zip](https://github.com/pxb1988/dex2jar/releases/download/v2.4/dex-tools-v2.4.zip) | 19.105.975 | `ee7c45eb3c1d2474a6145d8d447e651a736a22d9664b6d3d3be5a5a817dda23a` |
| [cfr-0.152.jar](https://github.com/leibnitz27/cfr/releases/download/0.152/cfr-0.152.jar) | 2.162.315 | `f686e8f3ded377d7bc87d216a90e9e9512df4156e75b06c655a16648ae8765b2` |

`prepare-toolchain.cjs` a verificat marimile/hashurile, a extras doar distributia uneltei in D: cu validarea cailor si a rulat numai `--help`/`--version`. Nu s-a convertit niciun input al aplicatiei. `toolchain-preparation.json` pastreaza inventarul JAR-urilor extrase, comenzile help, logurile si hashurile. Distributiile nu se republica in GitHub; provenienta si URL-urile permit restaurarea fara duplicate.

## Inputuri si acoperire

Pilotul foloseste exclusiv cele doua DEX-uri brute Bavvo 1.0.1222 deja extrase si verificate, fara o noua copie a APK-ului:

- `classes.dex`, SHA `2248912e2d52fa7b8e591e860d550136fb26056f388c5b2c600c1e6b1387c449`;
- `classes2.dex`, SHA `aeec1cf0c5f216895e31fa1c47101984c58850842d35010056d919200480c39f`.

Clase radacina: `a.b`, `K6.d`, `CarouselStrategyHelper`, `ShadowDrawableWrapper`. Lista exacta de descriptori, `classDefIndex`, SHA DEX si closure este fixata in [PILOT-PLAN.json](PILOT-PLAN.json). Closure inseamna aici clasa radacina si clasele sale `$...` identificate in class_data, nu intreaga retea tranzitiva de dependente: 3 clase pentru a.b, 15 pentru K6.d si cate una pentru cele doua Material, in total **20 de clase bytecode**. Referintele Smali auditate definesc **98 de metode radacina** pentru verificarea acoperirii.

Conversia dex2jar proceseaza fiecare dintre cele doua DEX-uri integral deoarece CLI-ul nu ofera un filtru sigur pe clase. Aceasta nu inseamna ca pilotul decompileaza toate clasele in Java: CFR va fi filtrat la cele 4 radacini si closure-urile lor. Cele doua JAR-uri convertite ofera classpath-ul reciproc. Dependentele Android externe nu sunt executate sau inventate; absenta unui android.jar se documenteaza ca limita de rezolvare a tipurilor.

## Comenzi si bugete numerice

Java: `C:/Program Files/Java/jdk-21/bin/java.exe`, versiune si comanda pastrate. Se folosesc argumente structurate, fara executarea scripturilor batch sau shell text din APK.

1. Pentru fiecare DEX, serial:

   `java -Xmx2g -cp <dex-tools-v2.4/lib/*> com.googlecode.dex2jar.tools.Dex2jarCmd --exception-file <run>/errors-N.zip --output <run>/classesN.jar <verified-raw-dex>`

   Maximum 600 secunde/DEX, un JVM simultan, output nou. Nu se folosesc `--skip-exceptions`, `--no-code` sau `--force`. Se pastreaza logul, codul de iesire si arhiva erorilor, inclusiv cand exista un JAR partial.

2. Inventar bytecode al JAR-urilor, fara incarcare sau executare a claselor aplicatiei: SHA pe fiecare intrare, prezenta exacta a celor 20 de clase si citirea structurii classfile pentru descriptorii metodelor radacina. Se verifica cei 98 de descriptori fata de Smali. Un parser de classfile va masura doar structura si nu va interpreta sau executa bytecode.

3. CFR pentru fiecare JAR convertit, serial:

   `java -Xmx2g -jar <cfr-0.152.jar> <classesN.jar> --outputdir <fresh-dir-N> --jarfilter <pinned-regex-N> --extraclasspath <classes1.jar;classes2.jar> --comments true --silent false --clobber false --allowcorrecting false`

   Maximum 300 secunde/JAR, un JVM simultan. CLI help confirma optiunile folosite. Filtrele exacte sunt in JSON: `a.b` si nested pentru DEX1; K6.d + cele doua Material si nested pentru DEX2. Tipurile de comentarii si diagnosticul raman vizibile. Modurile mai agresive sau un alt set de clase cer gate nou.

Buget total de output nou: 3 GB. Se verifica dupa fiecare proces si inainte de continuare. Nu se porneste nicio conversie daca spatiul liber este sub 5 GB. Un timeout sau esec nu declanseaza repetari automate cu flaguri diferite.

Pragul de 3 GB este un criteriu de acceptare post-process, nu o cota impusa de sistemul de operare. Spatiul liber de minimum 5 GB se verifica inainte de fiecare JVM. Parserul classfile accepta identitati ASCII; MUTF-8/neASCII nesuportat produce oprire explicita, fara verdict de coruptie a APK-ului. Controleaza prezenta unui singur Code nevid la metodele concrete si absenta Code la native/abstract, dar nu este un validator JVM complet. Clasele closure raporteaza separat metode concrete fara Code, Code duplicat, Code vid si Code neasteptat; orice asemenea problema sau diferenta in setul exact al prototipurilor duce la rezultat partial, nu la acoperire completa.

## Artefacte, partiale si acceptare

Se asteapta `run-independent-pilot.cjs`, `pilot-results.json`, loguri complete, manifestul outputurilor si rapoarte de acoperire pe clase/metode. JAR-urile convertite si sursele candidate raman in workroot D:, separat de Java anterior si de candidații manuali ai root-ului.

Exit code 0 al dex2jar nu inseamna conversie completa: exceptiile de metoda pot produce bytecode stub si o arhiva de erori. Aceasta se inventariaza integral si se coreleaza cu tintele. Lipsa unei clase sau a unui descriptor radacina marcheaza acoperirea incompleta; nu se promoveaza un candidat pe baza unei clase vecine.

CFR poate integra clase nested in fisierul radacina sau poate lasa metode nerecuperate. Se raporteaza separat: clase bytecode prezente, descriptori root prezenti, fisiere Java emise, clase nested reprezentate/integrate si marcaje de esec/warning. Prezenta a 4 fisiere Java nu certifica recuperarea tuturor celor 20 de clase sau a celor 98 de metode.

O parte poate fi utila chiar daca alte metode esueaza, dar raportul ramane `partial-candidate` si pastreaza explicit erorile. Urmatorul gate al auditorului decide daca pilotul poate fi extins. Niciun rezultat nu devine `recovered-java` fara verificarea separata a fluxului/exceptiilor/efectelor fata de DEX/Smali; compilarea sau acordul dintre doua decompilatoare nu reprezinta singure dovada semantica.

STOP la hash/dimensiune neconforme, input nou neaprobat, output existent neasteptat, timeout/memorie/disc, JAR neparsabil sau lipsa clasei radacina. Se pastreaza outputul partial si logul; nu se sterg erorile pentru a raporta succes. Fara APK execution, patch sau commit.
