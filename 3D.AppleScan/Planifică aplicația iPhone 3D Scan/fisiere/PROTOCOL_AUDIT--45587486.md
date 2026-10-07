# Protocolul de audit și închiderea constatărilor

## Domenii și independență

Auditurile acoperă Apple și performanță, viziune 6D, robotică, transport, produs și UX, metrologie și CAD, metodologie științifică, date, securitate și guvernanță. Un agent poate evalua mai multe domenii, cu checklist separat. Nu auditează drept independent un capitol pe care l-a scris. Jurnalele identifică autorul și auditorul efectivi, fără a pretinde existența unor experți umani certificați.

## Criterii documentare comune

- Scopul, intrările, ieșirile și stările de eroare sunt explicite.
- Faptele sunt sprijinite de surse adecvate, cu limite și disponibilitate declarate.
- Propunerile și țintele sunt separate de rezultate măsurate.
- Unitățile, reperele, timpul, versiunea și identitatea sunt coerente între capitole și contracte.
- Cerința are activitate, rezultat cuantificabil, responsabil și test.
- Întreruperile, datele vechi și limitele hardware au comportament definit.
- Fișierele necesare există, sunt lizibile și pot fi regăsite la reluare.
- Nu există promisiuni comerciale sau de siguranță dincolo de dovezi.

## Severități

P0 în audit reprezintă o problemă care ar putea conduce direct la un comportament grav nesigur sau pierdere majoră de date prin contractul propus. P1 reprezintă o eroare fundamentală de corectitudine, timp, cadru, persistență sau fezabilitate. P2 reprezintă o ambiguitate ori lipsă ce împiedică implementarea sau verificarea reproductibilă. P3 reprezintă o problemă editorială concretă. Aceste severități sunt independente de prioritățile de produs P0/P1/P2.

Pentru această livrare cerem zero constatări documentare deschise, inclusiv P3 identificate. O limită fizică explicită și un test planificat nu sunt defecte editoriale de „închis” prin inventarea unui rezultat. Ele rămân porți de implementare.

## Ciclul obligatoriu

Auditorul citește versiunea, verifică sursele și contractele, completează checklistul și scrie finding_id, severitate, fișier, problemă, dovadă și remediere. Autorul răspunde cu modificarea și probele. Auditorul reia criteriul și regresiile relevante pe noua versiune. Constatarea inițială rămâne în raportul R1; registrul curent primește closed numai după confirmarea independentă în R2 sau ulterior.

„100% satisfăcut” se operationalizează ca 100% criterii documentare aplicabile verificate și îndeplinite, fără constatări deschise în versiunea auditată. Nu reprezintă exhaustivitate absolută, certificare profesională ori lipsa oricărui defect viitor. Dacă dovezile nu permit acceptarea, verdictul rămâne respins sau inconcludent și se consemnează condiția de continuare.

## Dovada auditului

Fiecare raport include domeniu, autorul materialului, agentul auditor, moment, fișiere și versiune, checklist, constatări, limite și verdict. Manifestul final fixează identitatea livrării. Verificatorul automat susține integritatea și trasabilitatea, dar nu înlocuiește auditul semantic. Testele de hardware, Xacro expansion și compilările neexecutate sunt declarate ca atare.
