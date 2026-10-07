# SYS-001 — Plan de măsuri de guvernanță r01

Stare inițială: PLANIFICAT; 24.09.2026. Responsabil: P-MANAGER. Sursa: 05_AUDIT/SYS-001/A-GOVERNANCE-r01.json și .md. Rapoartele și scorurile inițiale rămân neschimbate. Implementarea va începe după metaauditul și arhivarea versiunii r01. Termen: înaintea depunerii r02; fără termen care să anuleze verificările.

## GOV-SYS-01 — Trasabilitate
Cauză: matricea inițială prezintă controale generale, fără lanț complet de probe. Măsură: ID per cerință, livrabil/etapă, test exact, auditor nominal de rol și dovadă localizată, cu distincție IMPLEMENTAT/DE VERIFICAT/VIITOR. Include distinct U02: arhivarea întregului proces și a RETURN. Test: toate cerințele U01–U03 și EN/RO/DE au câte un lanț; niciun test viitor nu este prezentat drept executat. Retest: A-GOVERNANCE.

## GOV-SYS-02 — Meta terminal
Cauză: fișa QA moștenește formula generică a auditorului primar. Măsură: înlocuire cu cele șase verificări booleene, referințe exacte, al treilea ID independent, fără note literare și fără al patrulea audit recursiv. Test: fișa, RUBRICI, modelul 07 și README au același contract. Retest: A-GOVERNANCE, A-SYSTEMS pentru schema executabilă.

## GOV-SYS-03 — Calibrare efectivă
Cauză: regula exista, dar nu erau păstrate răspunsuri per ID înaintea primei runde. Măsură: SET_TEST_r02 cu 9 cazuri comune și 2 specifice per rol, cheie și regulă 11/11; răspunsuri reale ale celor patru auditori și QA, verificare nominală; rolurile necalificate rămân blocate. Nu se inventează calificare retroactivă a r01. Test: ID, 11 răspunsuri, motive, referințe și verificare QA; primul reaudit calificat este r02. Retest: A-GOVERNANCE; QA controlează respectarea înainte de meta final.

## GOV-SYS-04 — Recuperarea și reconcilierea istoricului
Cauză: primele arhive au păstrat produse, dar unele mandate/predări numai în rezumat. Măsură: recuperarea mesajelor observabile exacte disponibile, instrucțiunile beneficiarului și prompturile integrale, arhivă suplimentară cu ID nou și hash, inventar care separă original, rezumat, recuperat și indisponibil. Nu se suprascriu arhivele inițiale și nu se reconstruiește drept original un mesaj necunoscut. Test: fiecare activitate efectuată are intrări, ieșiri, audit, măsuri și rezultat ori limită explicită; probele se găsesc din index; următoarele mandate sunt salvate înainte de trimitere. Retest: A-GOVERNANCE; orice lacună materială neînchisă rămâne raportată.

## Control transversal
Regenerează DOCX/PDF după modificarea documentelor, inspectează lizibilitatea, actualizează manifestul înainte de audit. Fișierele r02 și contractul se îngheață. Producătorul consemnează ce a făcut, fără să își atribuie punctaje sau să închidă constatările auditorului. Rezultatele se vor păstra separat în SYS-001-gouvernanta-rezultate-r02.md.

