# Audit independent de guvernanță și instrumente — R1

Data: 2026-10-02. Auditor: doctoral_apple_perception. Autorul materialului inspectat: managerul proiectului, agent distinct. Domeniu: README, RELUARE, fișe de post, roles.json, PROMPT_MASTER, AGENTI_RUNTIME, PROTOCOL_AUDIT, manage.cjs și create-registers.cjs.

## Verdict

**NEACCEPTAT DOCUMENTAR ȘI FUNCȚIONAL PENTRU INSTRUMENTE: 6/10 criterii trecute, patru constatări deschise (3 P1, 1 P2).** Problemele sunt demonstrate în copii izolate ale instrumentelor. Registrele principale nu au fost modificate de auditor. Criteriile canonice și bibliografia aflate în integrare nu sunt tratate drept lipsuri în această rundă.

## Ce am executat efectiv

Harness: `07_audit/fixtures/governance_probe_r1.cjs`. Rezultate brute: `07_audit/fixtures/governance_r1_results.json`. Execuție cu Node local; fiecare caz are propriul subfolder și o copie a instrumentului. Probele rulează comenzi reale, dar asupra registrelor sintetice, nu asupra planului proiectului. Nicio probă pe iPhone, ROS sau robot.

| Probă | Intrare sau acțiune | Rezultat observat |
|---|---|---|
| GOV-T01 | Task accepted, outputs gol, roluri inexistente, experiment necunoscut | validate returnează passed, exit 0 |
| GOV-T02 | Cerință fără owner/acceptance, legătură nereciprocă, experiment cu același owner/auditor | validate returnează passed, exit 0 |
| GOV-T03 | Audit accepted, două required_domains, zero rapoarte/dovezi | validate returnează passed, exit 0 |
| GOV-T04 | event test_actor, fără task/type/result | Evenimentul incomplet este scris, exit 0 |
| GOV-T05 | Validarea jurnalului incomplet de la T04 | validate returnează passed, exit 0 |
| GOV-T06 | manifest cu interrupted.tmp existent | Manifestul este creat, exclude tmp, exit 0 |
| GOV-T07 | verify fără nicio schimbare după T06 | failed, extra=[interrupted.tmp], exit 1 |
| GOV-T08 | create-registers cu roles.json deja existent | Inițializarea refuză; bytes sentinel rămân identici — PASS |

Fixture-urile negative sunt date de test. Validatorul producției trebuie să le delimiteze de registrele operaționale atunci când introduce verificarea semantică; manifestul poate în continuare să le acopere ca artefacte ale auditului. Harness-ul R1 și rezultatele sale se păstrează; o rundă nouă folosește rezultate noi, fără rescrierea dovezii istorice.

## Criterii documentare

| Criteriu | Verdict | Dovadă |
|---|---|---|
| GC01 Roluri planificate distincte de agenții efectiv activi | PASS | FISE_DE_POST, roles.staffing și actual_execution |
| GC02 Autor/auditor independenți și ciclu de remediere explicit | PASS | PROMPT_MASTER și PROTOCOL_AUDIT |
| GC03 Contractele runtime distincte de rolurile echipei | PASS | AGENTI_RUNTIME și criteriile EX |
| GC04 Reluare din artefacte confirmate, fără garanție a muncii nesalvate | PASS | RELUARE, scenariile și limitele API Apple |
| GC05 Inițializarea refuză suprascrierea registrelor existente | PASS | create-registers save și GOV-T08 |
| GC06 Integritate criptografică prezentată fără certificare falsă de hardware | PASS | manifest/hashchain și limitele README |
| GC07 Validarea registrelor aplică proprietari, probe și trasabilitate | FAIL | GOV-A01; GOV-T01/T02 |
| GC08 Accepted audit impune acoperirea domeniilor și dovezi | FAIL | GOV-A02; GOV-T03 |
| GC09 Evenimentul/checkpointul obligatoriu poate fi emis și validat complet | FAIL | GOV-A03; GOV-T04/T05 |
| GC10 Generarea și verificarea manifestului au aceleași excluderi | FAIL | GOV-A04; GOV-T06/T07 |

## GOV-A01 — P1 — Registre semantic invalide acceptate

În `tools/manage.cjs`, ramura validate pentru tasks verifică existența câtorva câmpuri și că owner diferă textual de auditor. Nu verifică dacă acele roluri există în roles.json, dacă status este admis sau dacă task.experiments referă experimente reale. Pentru accepted parcurge outputs, dar o listă goală trece fără rezultat ori raport de acceptare. Cerințele pot lipsi owner/acceptance, iar relația test–cerință nu este verificată reciproc. Experimentele pot avea același autor și auditor.

GOV-T01 și GOV-T02 demonstrează toate aceste combinații pe intrări JSON valide. Raportul passed pretinde verificarea trasabilității și stării documentare, deci depășește verificările realmente efectuate.

**Remediere:** definește câmpurile și enum-urile, validează identitatea rolurilor și referințele, verifică reciprocitatea cerință–experiment. O sarcină accepted trebuie să aibă artefacte existente și dovadă de audit independent referențiată. Stările planificate nu trebuie obligate să aibă rezultate fizice, dar trebuie să aibă rezultate așteptate. Adaugă teste negative și un caz valid de control.

## GOV-A02 — P1 — Acceptarea auditului fără acoperire

În ramura pentru `07_audit/REGISTRU.json`, condiția existentă respinge doar accepted cu un finding explicit neînchis. Un registru accepted cu lista goală trece chiar dacă required_domains conține domenii niciodată auditate. GOV-T03 demonstrează situația.

**Remediere:** fiecare domeniu aplicabil trebuie să indice raport existent, autor, auditor efectiv diferit, versiune și verdict. N/A cere motiv. Listele de constatări referite trebuie citite; un finding deschis nu poate fi ascuns prin omiterea sa din lista agregată. Validatorul nu trebuie să decidă adevărul tehnic, ci să impună existența dovezilor cerute de protocol.

## GOV-A03 — P1 — Eveniment incomplet acceptat și checkpoint inaccesibil

Comanda `event` validează numai actorul. GOV-T04 emite efectiv o linie fără task, event și result; GOV-T05 o declară validă. În plus, argumentele publice ale comenzii nu pot exprima attempt, input hashes, verificări și următoarea acțiune concretă cerute în RELUARE. Toate argumentele după result devin artefacte, iar next rămâne textul implicit.

**Remediere:** respinge lipsurile înaintea oricărei scrieri și furnizează o intrare structurată de checkpoint complet, validată printr-o schemă versionată. Validează jurnalele noi la citire. Jurnalele istorice ale acestei redactări pot păstra formatul declarat legacy, fără inventarea retroactivă a hashurilor sau etapelor. Delimitează evenimentul sumar de checkpointul capabil de reluare. Pentru fiecare actor este necesară o politică de unic scriitor sau protecție față de concurență; această politică se documentează și se testează înaintea folosirii simultane a aceluiași jurnal.

## GOV-A04 — P2 — Politici diferite pentru fișierele temporare

`manifest` exclude numele terminate în `.tmp`, dar `verify` exclude numai cele două fișiere din m.excludes. GOV-T06/T07 arată că un arbore nemodificat poate eșua imediat după generarea manifestului. Resturile temporare sunt plauzibile exact în scenariul de reluare după întrerupere.

**Remediere:** aplică aceeași regulă în ambele comenzi. Variante acceptabile: manifest refuză explicit cât timp există temporare nerezolvate, sau înregistrează o politică explicită de excludere aplicată identic de verify. Nu șterge automat fișierele temporare, deoarece pot conține lucru recuperabil. Include și fixture-urile de audit în politica documentată, evitând confundarea lor cu o salvare operațională incompletă.

## Limite și continuare

Nu am constatat suprascriere distructivă în generatorul inspectat: existența destinației provoacă eroare. Inițializarea parțială rămâne identificabilă și nu trebuie forțată prin ștergerea registrelor. Hashurile oferă verificare de integritate față de manifest, nu autenticitate criptografică în fața unui adversar care poate rescrie manifestul; documentația nu susține contrariul.

Autorul remediază instrumentele și documentele, păstrând rapoartele R1. Auditorul va executa controale pozitive și negative pe copii noi și va verifica diferențele. Acceptarea la 100% pentru acest domeniu înseamnă 10/10 criterii documentare îndeplinite și zero constatări deschise, cu toate limitele experimentale păstrate.
