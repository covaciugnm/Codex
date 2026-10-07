# OBS-MANAGER-001 — Probe produse de auditori după înghețarea produsului

Tip: observație de integrare a coordonatorului, NU constatare de auditor independent. Data: 24.09.2026. Produs: SYS-001 r02_staging.

Problema: schema propusă inițial cerea MD-ul auditorului în contractul produsului dacă era citat drept dovadă. Acest lucru complica ordinea normală produs înghețat → audit → meta și putea crea referințe circulare în hashuri. Nu schimbă constatările r01 și nu justifică reducerea verificării surselor.

Măsura cerută P-SYSTEMS: supplemental_evidence_files opțional, separat de intrările producerii, fixat prin hash de raportul JSON; pentru audit primar, JSON-ul este fixat suplimentar de meta. Declarații exhaustive, fără autoref/alias/override, surse reale cu hash actual și copiere automată la arhivare. Probe: supliment valid; deriva suplimentului respinge; sursa nedeclarată respinge; auto/alias/override resping; recuperarea arhivei include dovada exactă.

Mandatul exact: 06_REGISTRU/PROMPTURI/P-SYSTEMS-probe-auditor-r02.md. Stare la emitere: CERUT, în așteptarea rezultatului și auditului tehnic. Nu este implementare sau PASS pretins.

