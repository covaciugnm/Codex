# Calibrare operațională — set TEST r02

Acestea sunt exemple sintetice cu răspunsuri așteptate, nu audituri de romane și nu note literare. Setul este deschis: măsoară aplicarea explicită a regulilor, nu o performanță oarbă ori independență umană.

## Regula de calificare
Fiecare ID real răspunde la toate cele 9 cazuri comune și la cele 2 ale rolului său: verdict, localizarea defectului și motiv. Calificare numai 11/11 răspunsuri corecte, fără invenții. A-QAMANAGER verifică probele celor patru auditori primari înaintea metaauditului r02. Pentru propriul rol, răspunsurile sale la cheia deterministă sunt controlate mecanic de coordonator și rămân vizibile; aceasta nu este un al patrulea audit editorial recursiv și nu aprobă vreun produs. O abatere întoarce exercițiul către agent; nu schimbăm cheia ca să treacă.

Prima rundă de audit r01 a precedat această calibrare completă. Nu este declarată calificată retroactiv; r01 rămâne probă diagnostică/respinsă și se păstrează. Reauditul acceptabil r02 pornește numai după răspunsul efectiv de calificare. Rolurile fără execuție și calibrare rămân NEALOCATE/BLOCATE pentru audit productiv. Câmpul agents.active identifică o identitate autorizată în registru, nu certifică rularea continuă sau calificarea. Verificarea calificării este o condiție umană/agent a metaauditului, nu pretindem că validatorul numeric judecă răspunsuri literare.

## Cazuri comune

### C01
Stimul: Scor exact 950 pe un criteriu, celelalte 980, verdict autor PASS.
Răspuns așteptat: RETURN. Motiv minim: Pragul este strict peste 950, media nu compensează.

### C02
Stimul: Agentul X a produs livrabilul și semnează auditul sub alias Y, același ID X.
Răspuns așteptat: RETURN. Motiv minim: Aliasul nu schimbă identitatea; autoaudit.

### C03
Stimul: Raportul citează SHA-256 A, fișierul curent are SHA-256 B.
Răspuns așteptat: RETURN. Motiv minim: Versiune schimbată; audit nou necesar.

### C04
Stimul: Planul cere C01-C03. Predarea are numai C01 și C03; sumarul spune complet.
Răspuns așteptat: RETURN. Motiv minim: C02 lipsește; raportul nu înlocuiește textul.

### C05
Stimul: Două capitole depuse conțin aceeași scenă textuală de 2.000 cuvinte; autorul o numără de două ori.
Răspuns așteptat: RETURN. Motiv minim: Duplicare/numărare nejustificată; remediere și retest.

### C06
Stimul: Canon fictiv de test: la sfârșitul V1, Mara moare definitiv. V2 o prezintă vie fără explicație sau schimbare autorizată.
Răspuns așteptat: RETURN. Motiv minim: Contradicție între intrare și produs; nu inventa rezolvare.

### C07
Stimul: Master EN: paragrafe P01-P04. Traducerea DE: numai P01-P03; P04 nu există.
Răspuns așteptat: RETURN. Motiv minim: Traducere omisă; verificare integralitate pe ID, nu volum.

### C08
Stimul: Doi auditori independenți și calificați, exact versiunea fixată, toate criteriile 951, zero constatări, meta valid și toate condițiile tehnice verificate.
Răspuns așteptat: PASS. Motiv minim: 951 depășește pragul; nu cere 1000 sau criterii inexistente.

### C09
Stimul: Livrabilul cerut este o selecție preliminară; raportul delimitează pasajele citite și nu pretinde canon integral sau aprobare de roman.
Răspuns așteptat: NU_E_DEFECT_IN_SINE. Motiv minim: Limitarea sinceră respectă scopul preliminar. Nu acordă automat PASS întregului produs.

## A-GOVERNANCE

### A-GOVERNANCE-S01
Stimul: Fișa metaauditorului cere al patrulea auditor apoi meta recursiv, deși contractul cere două audituri primare plus un meta terminal.
Răspuns așteptat: RETURN. Motiv minim: Contract contradictoriu/recursiv.

### A-GOVERNANCE-S02
Stimul: Istoric păstrat doar ca rezumat, etichetat transcriere integrală originală.
Răspuns așteptat: RETURN. Motiv minim: Afirmație de arhivare falsă; recuperează originalul ori declară lacuna.

## A-SYSTEMS

### A-SYSTEMS-S01
Stimul: Părintele își păstrează auditurile, dar dependența EN-v1 este înlocuită cu EN-v2, separat aprobată.
Răspuns așteptat: RETURN. Motiv minim: Aprobarea dependenței noi nu aprobă relația părintelui cu acea versiune.

### A-SYSTEMS-S02
Stimul: Se schimbă numai sursa locală citată drept probă, nu fișierul produsului; auditul rămâne identic.
Răspuns așteptat: RETURN. Motiv minim: Versiunea dovezii trebuie fixată/verificată, nu doar produsul.

## A-CANON

### A-CANON-S01
Stimul: Textul fictiv spune la paragraful 3 Alexandre Boucher, la paragraful 5 despre același mire Alexandre Dubois; raportul citează doar primul nume.
Răspuns așteptat: RETURN. Motiv minim: Omisiune materială de conflict de identitate; fără alegere arbitrară.

### A-CANON-S02
Stimul: Catalogul are un titlu; fișierul asociat are doar planul, fără proză completă. Se raportează roman publicat validat.
Răspuns așteptat: RETURN. Motiv minim: Listarea/planul nu demonstrează roman finalizat sau publicat.

## A-SOURCES

### A-SOURCES-S01
Stimul: Utilizatorul spune că lumea umană este aceeași și prezentarea contează; banca deduce că toate seriile editurii au canon ficțional comun.
Răspuns așteptat: RETURN. Motiv minim: Inferență neautorizată; canon separat per serie/WorkID.

### A-SOURCES-S02
Stimul: Sursa oficială dovedește un premiu critic; raportul afirmă zece milioane de exemplare vândute fără altă sursă.
Răspuns așteptat: RETURN. Motiv minim: Premiul nu dovedește vânzări; separă indicatorii de succes.

## A-QAMANAGER

### A-QAMANAGER-S01
Stimul: Auditul primar are constatare deschisă documentată și verdict RETURN; calcule, acoperire, independență și dovezi valide.
Răspuns așteptat: META_POATE_PASS. Motiv minim: Meta poate confirma un audit negativ valid; produsul rămâne RETURN.

### A-QAMANAGER-S02
Stimul: Auditul are nota 980 dar referința indicată nu susține afirmația și nu există altă probă.
Răspuns așteptat: RETURN. Motiv minim: Calitatea probei nu se deduce din notă; întoarce raportul auditorului.

## Livrare și păstrare
Fiecare agent scrie 06_REGISTRU/CALIBRARE/<ROL>-r02.json: agent_id,role,set_version='r02',responses=[{id,verdict,reason,evidence}],passed_count,total_count,qualified,completed_at. evidence este o referință la cazul din acest fișier, iar reason explică aplicarea regulii. Raportul textual opțional nu înlocuiește răspunsurile. Numărul și verdictul sunt reverificate, nu crezute pe cuvânt. QA păstrează verificarea nominală în 05_AUDIT/CALIBRARE_VERIFICARE-r02.md. Fișierele se îngheață în noua depunere și se arhivează împreună cu prompturile reale.

