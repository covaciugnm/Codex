# Audit nou: corectarea decompilării și corelarea versiunilor

Acest audit este separat de verificările arhivei anterioare. Un scor anterior de 10/10 pentru integritate nu aprobă modificări de cod și nu dovedește corectitudinea Java recuperat. Fișierele originale, raw și rezultatele publicate anterior rămân nemodificate.

## Gate-uri obligatorii

| Gate | Etapă | Ce trebuie verificat înainte de continuare |
|---|---|---|
| G0 | Inventar și diagnostic | Toate intrările/spliturile și seturile DEX sunt identificate și fixate prin hash; numărătorile de erori sunt separate; fiecare caz are identitate și proveniență |
| G1 | Strategie și pilot | Matrice de experimente cu unelte/flags documentate, aceiași bytes DEX și același set de ținte; criterii de acceptare, regresie și oprire explicite |
| G2 | Execuție | Comenzi/loguri/exituri/outputuri complete, fără mascarea erorilor, fără modificarea originalelor; rezultatele pilotului susțin extinderea |
| G3 | Verificarea corecțiilor și corelărilor | Dovadă pe DEX/metodă, verificarea referințelor și contextului, comparație înainte/după, separarea reparațiilor de reprezentările alternative |
| G4 | Livrare și commit | Overlay reproductibil, deduplicare, restaurare/materializare verificate, limite și acoperire măsurate; aprobare explicită pentru snapshotul propus |

Fiecare gate primește un verdict explicit, cu dovezile și hashurile analizate. Un verdict de strategie nu aprobă un commit. Nu se face niciun commit al acestei etape fără aprobarea auditorului asupra listei exacte de fișiere și a conținutului lor. Dacă fișierele aprobate se schimbă, aprobarea trebuie refăcută. Certificatul de aprobare nu încearcă să-și includă propriul hash în sine; identitatea lui poate fi comunicată separat.

## Rubrică de 10 puncte

1. **Scope complet și baseline imuabil.** Cele 14 variante / 11 seturi DEX existente sunt contabilizate; HeyCyan și orice intrare nouă sunt inventariate separat, cu starea reală a decompilării. Nicio intrare nu dispare prin filtrare.
2. **Identitate și integritate.** Containerul, componenta, DEX-ul, metoda și outputul sunt legate prin SHA-256/dimensiuni și identificatori stabili. Eventualul input DEX-only este demonstrat identic cu DEX-urile selectate din sursă.
3. **Diagnostic cu numărător corect.** Exit/tool errors, loader/nested-archive failures, clase/metode eșuate, `Method not decompiled`, `UnsupportedOperationException`, corpuri omise și marcaje JADX ERROR/WARN sunt măsurate distinct. Un warning sau un throw intenționat din bytecode nu devine automat defect de decompilare.
4. **Strategie controlată și reproductibilă.** Există o matrice finită de experimente, cu unelte/versiuni/hashuri, flags confirmate, ținte și criterii de acceptare. Se compară aceleași intrări și aceiași denominatori, nu un run filtrat cu un run complet.
5. **Execuție auditată.** Fiecare încercare are comandă, timp, exit, log și inventar de output; încercările întrerupte/supersedate sunt declarate. Nu se rulează APK-ul sau serviciile sale pentru a obține un rezultat aparent.
6. **Corecții susținute de dovezi.** Scăderea numărului de erori sau succesul compilării Java nu dovedește singur echivalența. Pentru fiecare corecție declarată există o verificare statică adecvată pe metoda/bytecode-ul original și un control de regresie. Dacă nu există dovadă suficientă, rezultatul rămâne candidat sau reprezentare alternativă.
7. **Corelare între versiuni verificată.** Numele obfuscate și asemănarea textului nu sunt suficiente. Se verifică instrucțiuni, prototipuri, referințe rezolvate și context; un hash brut de `code_item` nu dovedește singur echivalența când indicii DEX pot desemna alte referințe. Aliasurile și mapările ambigue rămân marcate.
8. **Fără substituții care ascund problema.** SIMPLE/FALLBACK/Smali/CFG sunt etichetate separat. Nu se șterg warninguri/stuburi pentru a obține artificial zero erori și nu se inventează logică. Codul nativ Flutter AOT nu este prezentat ca sursă Dart/C++ originală.
9. **Livrare sigură și fără duplicate.** Overlay-ul conține numai modificări și referințe verificate, păstrează old/new SHA și baseline, reutilizează conținutul deja publicat și materializează separat variantele cu mapare Windows reversibilă. Înlocuirile verificate sunt distincte de candidați și materiale de diagnostic.
10. **Închidere și aprobare exactă.** Auditorul verifică independent rezultatele, acoperirea și limitele. Înainte de fiecare commit se aprobă explicit snapshotul exact; înainte de publicarea finală se verifică artefactele și proveniența. Raportul nu afirmă că toate erorile sunt reparate dacă rămân cazuri nerecuperate sau doar reprezentări alternative.

## Cum se interpretează scorul

Scorul auditului și acoperirea reparațiilor sunt două valori distincte. Raportarea trebuie să arate numărul de metode/cazuri vizate, corecții confirmate, îmbunătățiri numai de pipeline, candidați, reprezentări alternative și cazuri nerezolvate. Un scor de audit nu transformă aceste ultime categorii în reparații semantice și nu justifică declararea obiectivului integral realizat dacă acesta nu este susținut de rezultate.

## Riscuri concrete urmărite

- Loader errors pot dispărea din inputul DEX-only fără a fi reparată nicio metodă.
- `--show-bad-code`, SIMPLE sau FALLBACK pot schimba marcajele ori forma textului fără a recupera corect logica.
- Java care compilează cu stuburi poate avea semantică diferită de APK-ul original.
- Identitatea DEX permite reutilizarea codului, nu a resurselor, bibliotecilor native sau certificatelor variantei.
- Obfuscarea schimbă identități între versiuni; indicii din bytecode trebuie interpretați în DEX-ul lor.
- Outputurile vechi și noi nu trebuie amestecate prin cache, nume de fișiere sau coliziuni Windows.
- Nicio concluzie de activare UE, autentificare SMS sau asociere cu ochelarii nu rezultă din corectarea unei reprezentări Java.
