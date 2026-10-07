# Riscuri decizii și întrebări deschise

## Decizii adoptate în proiectare

| ID | Decizie | Motiv | Reconsiderare |
|---|---|---|---|
| ADR01 | Cele trei moduri inițiale rămân distincte | Utilizare și persistență diferite | Test UX cu dovezi |
| ADR02 | Harta statică, obstacolele recente și catalogul au fluxuri separate | Frecvențe și criterii de validitate diferite | Benchmark și analiză de erori |
| ADR03 | Gateway pe calculatorul robotului | Separă aplicația iOS de middlewareul robotului | Spike și cost de integrare |
| ADR04 | Identificatori și epoci explicite în fiecare rezultat | Evită aplicarea în sesiunea ori timpul greșit | Schimbare de protocol versionată |
| ADR05 | Pool limitat de procesare și prioritizare | Acceleratorul și termicul sunt resurse partajate | Experimente1/2/4joburi |
| ADR06 | Audit independent și praguri canonice | Evită autoaprobarea și contradicțiile | Numai prin decizie cu re-audit |
| ADR07 | Eroare dimensională normalizată și poartă de succes | Compară lungimi diferite și include eșecurile | Pilot statistic preregistrat |
| ADR08 | Securitatea este precondiție pentru mișcare | Fluxurile conectate trebuie autentificate | Nu se elimină fără analiză explicită |

Deciziile sunt propuneri adoptate pentru document, nu dovada unei implementări. Schimbarea lor se consemnează în jurnal cu motiv și efect asupra sarcinilor.

## Registrul riscurilor

| ID | Risc | Semnal de detectare | Măsură propusă | Proprietar | Poarta afectată |
|---|---|---|---|---|---|
| R01 | API sau dispozitiv incompatibil | supports false sau spike eșuat | Matrice runtime și fallback explicit | IOS | W00 |
| R02 | Bias metric persistent | Eroare pe referințe independente | Calibrare și restrângere domeniu | MET | W03/W05 |
| R03 | Identități schimbate | ID switches în lot cu exemplare identice | Ambiguitate și reidentificare | CV | W07 |
| R04 | Procesare întârziată termic | Age_at_use crește | Reducere workload și expirare | PERF | W08 |
| R05 | Reper sau ceas schimbat | Epocă inconsistentă | Invalidare și resincronizare | NET | W10 |
| R06 | Montaj deplasat | Reproiecție/calibrare degradată | Verificare și recalibrare | HW | W09 |
| R07 | Mesh ratează obstacol nou | Discrepanță depth/mesh | Strat local din observații recente | ROB | W11/W12 |
| R08 | Date confirmate pierdute | Hash/manifest lipsă după restart | Tranzacție și jurnal durabil | DATA | W02 |
| R09 | Date personale persistate implicit | Audit disc/rețea | Separarea modurilor și retenție | SEC | W13 |
| R10 | Export incompatibil sau licență absentă | Reimport eșuat/verificare juridică | Subset calificat și etapizare | CAD | W06 |
| R11 | Eșantion insuficient | CI larg sau strat gol | Extindere lot și verdict inconcludent | SCI | W15 |
| R12 | Documente divergente la reluare | Hashuri/registre neconcordante | Autoritate unică și audit checkpoint | MGR | Toate |

## Informații de obținut în W00

Modelul exact de iPhone și iOS, Mac/Xcode, hardwareul robotului și ROS 2, montajul cap/trunchi, instrumentele de referință, vitezele și distanțele operaționale, materialele și dimensiunile prioritare, formatele/destinațiile CAD, regulile de retenție și bugetul. Fiecare răspuns devine configurație versionată; lipsa lui nu se completează cu o promisiune tehnică.
