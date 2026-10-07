# Calibrare editorială suplimentară ROM-001 — set TEST rom001-r01
Autor set: P-MANAGER.24.09.2026,Europe/Bucharest. Exemple sintetice, deschise, cheia vizibilă. Nu sunt scene ale romanului sau audituri productive și nu deschid G02+.
Se păstrează regula existentă: C01–C09 din 06_REGISTRU/CALIBRARE/SET_TEST_r02.md plus două cazuri ale rolului de mai jos, 11/11 răspunsuri motivate, verificate nominal de A-QAMANAGER înainte de primul audit productiv. Nu se editează setul r02 înghețat, nu se califică retroactiv roluri și nu se pretinde test orb sau competență literară exhaustivă.
## A-GENRE-S01
Stimul TEST: Brief-ul aprobat cere romance cu final fericit/optimist al cuplului central. Proza finală ucide definitiv ambii parteneri, lasă relația fără deznodământ optimist și raportul o prezintă tot drept îndeplinire a brief-ului, fără schimbare aprobată.
Cheie: RETURN. Localizează finalul față de promisiunea contractuală. Nu condamna tragedia ca gen; este nepotrivirea cu brief-ul specific, nu gust personal.
## A-GENRE-S02
Stimul TEST: Produsul de cercetare vizează cititori adulți de romance contemporan cu mister familial. Are numai date pentru manuale școlare și un joc sportiv fără narațiune; nu explică transferul către publicul cărții și afirmă că dovedește cerere pentru romance.
Cheie: RETURN. Relevanța/publicul și afirmația de cerere nu sunt demonstrate. Deschiderea băncii către orice mediu narativ relevant nu înseamnă că orice succes este probă de potrivire.
## A-ORIGINALITY-S01
Stimul TEST: Documentul nou preia dintr-o operă-sursă aceeași succesiune distinctivă de șapte întâmplări, aceleași relații, indicii și răsturnare finală, modificând doar nume și oraș; numește procedeul combinare de mecanisme universale.
Cheie: RETURN. Configurația recognoscibilă a intrigii nu a fost transformată independent; simpla redenumire nu satisface originalitatea. Nu emite certificat juridic.
## A-ORIGINALITY-S02
Stimul TEST: Două opere folosesc ideea generală că o scrisoare provoacă o alegere. Matricea verificabilă a noului proiect arată personaje, motivații, relații, obiective, loc, timp, cauzalitate, indicii, rezolvare și voce distincte; nu există expresie sau scene preluate în materialul stipulat. Un critic cere respingere numai pentru prezența unei scrisori.
Cheie: NU_E_DEFECT_IN_SINE. Motivul generic comun nu dovedește lipsa originalității; evaluarea continuă pe toate criteriile, nu PASS automat sau garanție juridică.
## A-STRUCTURE-S01
Stimul TEST: Planul și proza nu plantează cheia, aliatul ori abilitatea necesară evadării. În climax apare un necunoscut cu o cheie universală și rezolvă singur conflictul central, fără legătură cauzală cu alegerile protagonistului.
Cheie: RETURN. Soluție din senin și agenție eludată; sunt necesare pregătire și cauzalitate verificate în plan și proză, nu afirmația din raport că indiciul ar exista.
## A-STRUCTURE-S02
Stimul TEST: O scenă liniștită de dialog schimbă o alianță, îl face pe protagonist să renunțe la o protecție și stabilește o obligație care cauzează următoarea scenă. Raportul o declară automat inutilă deoarece nu conține urmărire sau violență.
Cheie: NU_E_DEFECT_IN_SINE. Funcția cauzală și schimbarea de stare sunt stipulate; lipsa acțiunii fizice nu este lipsă de funcție. Restul calității scenei se evaluează separat.
## A-EN-S01
Stimul TEST: Pasaj EN în perspectivă limitată a Annei: “Anna have placed the cup down. He were afraid.” Nu există antecedent masculin, schimbare de perspectivă ori efect de dialect în brief. Raportul spune limbă impecabilă și referent clar.
Cheie: RETURN. Acord verbal neconform și referent/perspectivă nejustificate; localizează cele două propoziții. Nu inventa dialect sau personaj absent ca soluție.
## A-EN-S02
Stimul TEST: Brief-ul permite un dialog contemporan natural, inclusiv fragmente în replici. Replica este “Not tonight,” Anna said. Contextul face sensul și vorbitorul clare. Raportul cere respingere exclusiv fiindcă replica nu are propoziție cu verb finit.
Cheie: NU_E_DEFECT_IN_SINE. Fragmentul este dialog idiomatic legitim în contextul dat. Nu aplica o interdicție absentă din brief; celelalte criterii rămân de auditat.
## Format răspuns
Fișier separat 06_REGISTRU/CALIBRARE/ROM-001/<ROL>-r01.json:
agent_id, role, set_version="rom001-r01", responses=[{id,verdict,reason,evidence}], passed_count,total_count,qualified,completed_at. evidence localizează cazul în setul r02 pentru C01–C09 sau acest supliment pentru S01/S02. completed_at cu fus orar. Răspunsul propriu nu este calificare independentă; QA citește și verifică motivele, identitatea și probele, nu doar numărul.
Dacă o cheie este contestată, se raportează justificarea și nu se pretinde calificare prin ocolire. Pragul auditului productiv rămâne fiecare criteriu >950/1000, cu metaaudit terminal; calibrarea nu este auditul unui roman.

