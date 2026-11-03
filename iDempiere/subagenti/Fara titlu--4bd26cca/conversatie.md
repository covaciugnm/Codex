# Fara titlu

ID: `01a19e35-7826-7d32-8767-ba5a4bd26cca`  
Proiect: iDempiere  
Export UTC: 2026-11-03T03:30:08.376808+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Asistent

Verific cele 174 de scripturi respinse de parserul PostgreSQL. Pentru fiecare separ sintaxa destinată altui motor, comenzile interpretate de `psql` și erorile care se reproduc pe motorul declarat. Pentru proba funcțională folosesc o bază sintetică izolată.

## Asistent

Din cele 174 de fișiere, 82 folosesc sintaxa clientului `psql`, iar 74 sunt interogări Jasper acceptate după legarea parametrilor. Două sunt explicit pentru Oracle. Verific separat cele 16 respingeri rămase și compar interogările de lucru cu cele incluse efectiv în șabloanele Jasper.

## Asistent

Am clasificat toate cele **174 de scripturi SQL** respinse inițial. Dintre ele, 82 sunt parsabile prin convențiile `psql`, 74 după legarea parametrilor Jasper, iar două sunt destinate Oracle. Celelalte 16 sunt identificate individual, cu limitele probei. [Registrul nominal](<Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R11_fisiere/A02/Triaj_nominal_174_SQL.json>)

Pe PostgreSQL 16 am reprodus două defecte. Dacă ID-ul rezervat este ocupat de altă serie, configurarea poate lega **recepția de marfă sau factura pro forma de seria greșită**, fără eroare, inclusiv la reluare. Separat, scriptul de mentenanță `AMN_Schema` se oprește înainte să modifice oricare dintre cele 45 de coloane vizate. Nu s-au emis documente ERP, iar clona sintetică a fost ștearsă.

Raportul și probele au fost predate către A11 pentru verificare independentă. [Raport A02](<Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R11_fisiere/A02/Raport_A02_R11_DB.json>)
