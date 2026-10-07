# Plan de măsuri — G0-CANON-v4, R2

Data: 24.09.2026. Manager: coordonatorul Codex. Analiză pe baza celor trei rapoarte independente R2, citite după încheiere. Contrasemnarea generală din decizia 15 se aplică; nu se solicită din nou.

| Auditor | Notă | Verdict |
|---|---|---|
| Canon & Istorie, Einstein | 8,50 | FAIL |
| Meșteșug & Piață, Dirac | 8,50 | FAIL |
| KPI & Completitudine, Popper | 8,50 | FAIL |

Minimum 8,50: NU TRECE. Rapoartele R2_audit_canon.md, R2_audit_craft.md și R2_audit_kpi.md rămân nemodificate. Toate identifică aceeași cauză: introducerea a 20 de semne de întrebare în locul diacriticelor și simbolurilor din două pasaje noi. Nu se schimbă grila sau nota.

| Măsură | Responsabil | Acțiune | Acceptare |
|---|---|---|---|
| M2.1 | Coordonator, ca autor al corecturii | Copie înainte de revizie a canonului, cu amprentă; păstrarea pachetului auditat. | Copia corespunde hashului 243630e9…9ab26. |
| M2.2 | Coordonator | Rescriere exclusivă UTF-8 a pasajului OBS-10 din §12 și a rândului V4-87; repararea celor 20 de caractere, fără schimbare de sens. | Zero substituții ? în cele două fragmente; textul corespunde formulării din OBSERVATII_COORDONATOR.md; toate celelalte pasaje neschimbate în afara antetului de versiune. |
| M2.3 | Coordonator și autor Studio | Canon v4.3, amprentă nouă, propagare în rubricile curente ale organizării. | Un singur canon de referință pentru pachetul următor; istoria păstrată. |
| M2.4 | Coordonator | Copie nouă și audit cu trei agenți noi. | Niciun PASS anticipat; fiecare raport propriu, min.9,50. |

## Execuție

Se completează după aplicarea corecturii și verificarea diferențelor.


### Rezultatul corecturii

M2.1: copie exactă înainte în R2_corecturi/00_CANON_inainte.md. M2.2: 20 de caractere reparate în cele două pasaje; UTF-8 valid; comparația inversă confirmă restul conținutului neschimbat, exceptând antetul versiunii. M2.3: v4.3 predată, SHA-256 `b51981121c39953258b32989d85a4239120f85aa8746229736ca605c25f57357`; autorul Studio primește referința pentru aliniere. M2.4: în așteptarea noului complet. Dovezi: R2_corecturi/rezultat.json și diferente.patch. Nicio notă nouă nu este acordată de autor.
