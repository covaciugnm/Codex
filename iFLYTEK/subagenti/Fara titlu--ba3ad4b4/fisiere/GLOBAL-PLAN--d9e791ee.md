# Extindere globala bounded: candidati dex2jar/CFR

Stare: draft pentru audit incremental; nu este autorizare de executie. Acoperirea proiectului include 12 seturi DEX (11 istorice si HeyCyan separat), 15 containere/variante logice si **822 de markeri de stub**: 798 istorici + 24 HeyCyan. Markerii nu sunt echivalati cu metode raw unice. Nicio sursa CFR nu se promoveaza automat.

## Date fixate si identitati

Registrul va pastra fiecare marker cu ID stabil, grup DEX, fisier/linie/hash Java, textul semnaturii afisate, candidati owner si status explicit. Clasele raw existente sunt selectii pentru colectarea de candidati, nu dovada automata a legaturii fiecarui marker cu o metoda. Aliasurile neconfirmate raman pending; nu sunt eliminate din numitorul 822.

Un index read-only nou prin dexlib2 extrage descriptorii ClassDef si prototipurile/metodele raw din fiecare DEX, fara JADX load, surse decompilate sau incarcare de clase JVM ale aplicatiei. Se pastreaza DEX SHA, methodIndex, owner, name/proto, flags si hashul octetilor de instructiuni. Hashul instructiunilor este numai egalitate de octeti in contextul exact al DEX-ului, nu echivalenta semantica intre DEX-uri. Reflection read-only asupra campului `codeOffset` din JAR-ul fixat este verificata fata de implementarea API si limitele bufferului; orice nepotrivire opreste etapa.

Regresie obligatorie: cele 4 clase/20 closure si 98 prototipuri din pilot trebuie sa coincida cu indexul raw inainte de extindere. Pentru fiecare owner procesat se verifica ulterior setul exact al metodelor din classfile, flags si prezenta Code, fara a numi acest control validare JVM completa.

## Limite si etape

1. Compilare adaptor raw: maximum 60 s. Index raw: un JVM 512 MB/un thread, maximum 60 s/DEX, serial. Lista exacta a DEX-urilor, cu SHA/marime/cale, este fixata in JSON; sunt asteptate 37 de DEX-uri unice. DEX-uri identice se indexeaza o singura data, cu toate referintele logice pastrate.
2. dex2jar: un JVM simultan, 2 GB, maximum 600 s/DEX. Se reutilizeaza cele doua conversii deja auditate daca input/tool/options SHA si output SHA coincid. Fara ignorarea exceptiilor. Restul conversiilor sunt noi, cu loguri si exception ZIP inventariate.
3. CFR: clase root directe, maximum 90 s/root, 2 GB/un JVM serial, aceleasi optiuni conservatoare probate in callback, inclusiv `--caseinsensitivefs false`. Se extrag numai root+closure `$...` intr-un director propriu. Cazurile cu coliziuni case-fold, cai Windows imposibile sau identitati neconfirmate se raporteaza pending si nu se suprascriu.
4. Batch de maximum 16 rooturi; primul checkpoint urmareste reprezentanti din toate grupurile pentru care exista owner confirmat. Dupa auditul checkpointului se solicita extinderea in acelasi profil la restul rooturilor fixate. Daca este aprobat direct un set mai mare de batch-uri, runnerul pastreaza checkpoint separat la fiecare 16 rooturi si nu depaseste setul din gate.

Minimum 5 GB liberi inainte de fiecare JVM; prag de acceptare post-process 3 GB de output nou/batch, maximum 10 GB pentru etapa globala, deadline global persistent de 6 ore si deadline de 60 minute/checkpoint (metadata maximum 30 minute). Nu este cota OS live. Timeout/memorie/tool hash mismatch opresc procesul curent; outputurile partiale si logurile se pastreaza. Nu se schimba automat flaguri si nu se repeta o clasa cu un alt profil neaprobat.

## Deduplicare si directoare

Directoare: `groups/<dexSetSha256>/roots/<hash-descriptor>/`, fara nume Java obfuscate concatenate in identificatorul rootului. Manifestele pastreaza numele logice originale. Obiectele classfile, Java si logurile identice pot fi adresate prin SHA, fara incarcare redundanta in GitHub.

Cache conversie: SHA DEX + toate JAR-urile tool + optiuni. Cache CFR: SHA classfile + closure + intregul classpath + CFR SHA + optiuni, nu doar octetii clasei. Egalitatea fizica a unui Code nu promoveaza sau uneste metode din contexte DEX diferite. Variantele cu acelasi DEX set refera aceleasi rezultate, pastrand identitatile logice.

## Acoperire si calitate

Per grup si per root: inputuri, owner raw, closure, expected/actual method protos, missing/extra, Code issues, converter exceptions, surse emise, diagnostice CFR, sintaxa evident suspecta si pending-uri. Lipsa markerilor nu demonstreaza compilabilitate: callback-ul a.b a produs deja contraexemplul `Object.put`. Nu se deduce acoperirea claselor nested din numarul fisierelor Java, deoarece CFR le poate integra.

Rezultatul final al acestei etape este un set de candidati si dovezi, nu repararea semantica a tuturor celor 822 de markeri. Registry-ul ramane complet si permite integrarea ulterioara a maparii autoritative a aliasurilor/metodelor de catre executor, fara omisiuni tacite. Orice target nou rezultat din aliasuri necesita delta de plan auditata daca nu era deja in setul de descriptori permis.
