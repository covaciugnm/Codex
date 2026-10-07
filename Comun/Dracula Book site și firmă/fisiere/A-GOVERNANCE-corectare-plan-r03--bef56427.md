# Plan de corectare a auditului — META-RES-001-r02-F01

24.09.2026. Responsabil A-GOVERNANCE; coordonare P-MANAGER; verificare finală A-QAMANAGER. Baza este constatarea din 05_AUDIT/RES-001/A-QAMANAGER-r02.md; perechea MD/JSON finală a metaauditului va fi păstrată în dosarul r02. Nu se modifică rapoartele primare sau meta existente.

## Cauză și rezultat cerut

A-GOVERNANCE a închis F-RES-SOURCES-001 după verificări procedurale sintetice, deși condiția originală T02 cere aplicații pe WorkID-uri reale. Același defect general nu înseamnă aceleași condiții de închidere pentru două ID-uri diferite. Proba de corectare a textului nu substituie proba de utilizare reală.

Rezultat cerut: o reevaluare ulterioară care urmărește cumulativ T01–T04, diferențiază executat/neexecutat și leagă fiecare concluzie de proba versiunii curente. Notele, MD-ul, JSON-ul și verdictul trebuie să concorde cu aceste probe; managerul nu impune un scor alternativ.

## Activități obligatorii în reaudit r03

1. Citește constatarea meta finală și condițiile exacte r01; explică eroarea și regula de prevenire într-o notă proprie nouă, fără a cosmetiza r02.
2. Construiește matrice T01–T04: cerință originală, probă actuală, operație proprie de retest, rezultat și limită. Distinge testul procedural GOV de T02b real.
3. Pentru T02b verifică toate cele patru WorkID-uri și sursele fixate în contractul nou; parcurge selecția și prezentarea pe fiecare. O fișă a producătorului este intrare pentru test, nu test extern deja trecut.
4. Decide statutul F-RES-SOURCES-001 numai după toate condițiile. Dacă o condiție lipsește, păstrează findingul deschis și verdictul adecvat, indiferent de alte note.
5. Finalizează MD/jurnale înaintea JSON-ului. Nota de corectare și matricea se declară în propriile supplemental_evidence_files; sunt verificabile de QA.
6. QA verifică raportul nou și măsura, inclusiv închiderea ulterioară a constatării meta. A-GOVERNANCE nu își acordă singur închiderea propriei erori de audit.

## Livrabile și acceptare

Livrabile A-GOVERNANCE: notă nouă de corectare, matricea T01–T04 și raportul r03 cu probe; nicio editare a r02. Rezultat măsurabil: 4/4 teste originale urmărite, 4/4 proiecte reale verificate pentru T02b sau lipsa declarată; zero concluzii de închidere bazate pe substituții. Pragurile produsului rămân >950 pe fiecare criteriu la doi auditori separați, apoi metaaudit valid.

Acesta este un plan de măsuri, nu o calificare nouă, un test deja trecut sau o închidere a constatării. Corecțiile produsului și corecția raportului sunt operații distincte.
