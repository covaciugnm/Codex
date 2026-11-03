# Fara titlu

ID: `01a19e31-5576-7980-a798-5d1e93bfd895`  
Proiect: iDempiere  
Export UTC: 2026-11-03T03:30:08.376808+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Asistent

Verific ce a rămas nedemonstrat în R10 pentru WMS și aleg o probă care urmărește efectul asupra lotului, locatorului sau returului într-o clonă sintetică.

## Asistent

Am reprodus o eroare de concurență în G2. Un gestionar ambalează un set din două piese. Dacă alt utilizator schimbă rețeta la trei piese înainte ca ambalarea să fie confirmată, modificarea este acceptată. La dezambalare, G2 înregistrează trei piese în locator și ajunge la **11 piese din cele 10 inițiale**. Dacă aceleași operații au loc succesiv, modificarea rețetei este refuzată și stocul rămâne 10.

Rezultatul a fost reprodus de două ori pe JAR-ul din Git și de două ori pe sursele recompilate, cu PostgreSQL 16. Cantitățile au fost recitite după confirmare printr-o conexiune nouă. Proba acoperă componentele WMS cu adaptor JDBC. Reproducerea prin fereastra nativă iDempiere și recepția independentă A11 rămân deschise.

Am predat cinci fișe de fișier și am închis clona sintetică. [Raport A05](<Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R11_fisiere/A05/Raport_A05_R11_WMS.json>) · [Manifestul probelor](<Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R11_fisiere/A05/Manifest_A05_R11_WMS.json>)
