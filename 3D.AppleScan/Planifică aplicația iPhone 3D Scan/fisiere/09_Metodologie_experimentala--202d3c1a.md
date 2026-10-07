# 9 Metodologia experimentală și reproductibilitatea

## 9.1 Separarea etapelor

Studiul are patru etape: fezabilitate API, pilot instrumentat, calificarea profilurilor și pilot operațional. Fezabilitatea confirmă numai că datele necesare pot fi obținute și prelucrate. Pilotul estimează variabilitatea, stabilește configurații și permite proiectarea lotului final. Calificarea folosește date ținute deoparte. Pilotul operațional verifică utilizarea și recuperarea în condiții realiste.

Toate experimentele sunt planificate în registrul experiments. Nu există măsurători pe iPhone sau robot în acest dosar. Rezultatele viitoare se salvează ca fișiere noi, fără a înlocui șablonul ori protocolul folosit.

## 9.2 Ipoteze și comparații

H1 propune că fuziunea a trei treceri reduce eroarea pe repere independente față de o trecere, în condiții identice. Se raportează diferența și intervalul său de încredere. Rezultatul negativ este acceptabil științific și poate limita produsul.

H2 propune că folosirea adâncimii îmbunătățește estimarea poziției față de RGB singur în anumite clase de obiecte; efectele se raportează separat pentru geometrie și orientare. H3 propune că un planificator adaptiv reduce energia per minut și latența P95 la aceeași limită de degradare a urmăririi. H4 cere ca reconectarea și relocalizarea să nu aplice niciun rezultat în sesiunea sau harta greșită în lotul de fault injection.

Aceste ipoteze trebuie preregistrate înainte de lotul final: endpoint primar, test statistic, interval, excluderi, prag și regulă de oprire. Nu se alege ulterior cea mai favorabilă combinație dintre zeci de metrici.

## 9.3 Date și împărțirea loturilor

Identitatea obiectelor și camerelor este unitatea de împărțire între dezvoltare și testare. Cadre alăturate ale aceluiași obiect nu se repartizează aleator în ambele seturi, deoarece ar produce scurgere de informație. Sesiunile sunt grupate după locație, dispozitiv, operator și zi. Modelele de referință folosite pentru urmărire sunt înregistrate ca intrări, iar fotografiile de evaluare sunt distincte de antrenare.

Pilotul propus include 12 obiecte și 3 camere. Lotul inițial de calificare include cel puțin 30 obiecte distincte, trei sesiuni pe obiect și cel puțin 10 proiecte cu 3–8 camere, pe fiecare profil hardware comercializat. Se stratifcă materialul, dimensiunea, texturarea, iluminarea și ocluzia. Numerele sunt minime de proiectare; analiza de putere și precizia intervalelor după pilot pot cere extindere.

Suprafețele lucioase, transparente și foarte întunecate sunt o categorie de stres declarată. Eșecurile lor nu dispar din raport prin selecția exclusivă a reconstrucțiilor reușite. Dacă nu fac parte din domeniul comercial, rezultatul include detectarea limitei și mesajul către utilizator.

## 9.4 Referințe independente

Dimensiunile se compară cu instrumente și repere adecvate toleranței urmărite, cu incertitudine consemnată. Pentru traiectorie și 6D se poate utiliza un sistem extern de urmărire, un montaj cu poziții cunoscute sau o infrastructură de markere calibrată. Un marker folosit de algoritmul evaluat nu servește singur ca referință independentă pentru același rezultat.

Referințele sunt verificate înainte și după lot pentru a detecta deplasarea montajului. Operatorul care etichetează rezultatele nu ajustează algoritmul după ce vede lotul final. Când referința nu este suficient de bună pentru prag, testul este inconcludent și se îmbunătățește metoda de referință.

## 9.5 Metrici geometrice și semantice

Pentru lungimi: eroare semnată, eroare absolută, bias, P50/P95, interval de încredere și rata capturilor valide. Pentru suprafețe: distanțe punct–suprafață, completitudine și acoperire în regiuni fixe, păstrând separat geometria completată artificial. Pentru traiectorie: ATE și RPE cu regula de aliniere declarată; o evaluare metrică nu poate absorbi scara printr-o aliniere arbitrară.

Pentru 6D raportăm eroarea de translație și eroarea geodezică de rotație, iar la obiecte simetrice utilizăm echivalențele declarate ale modelului. Benchmarkul BOP definește metrici care tratează simetria și vizibilitatea, precum VSD, MSSD și MSPD. Alegerea depinde de sarcină; scorurile nu sunt interschimbabile. [BOP](https://bop.felk.cvut.cz/challenges/bop-challenge-2019/)

Pentru catalog raportăm precizie/recall pe clasă, schimbări de identitate, obiecte duplicate, false reapariții și durata până la redetectare. O rată mare de cadre urmărite nu este suficientă dacă două exemplare identice își schimbă ID-ul. Pozițiile prezise se evaluează separat după orizont, fără a fi numărate ca observații noi.

## 9.6 Latență energie și temperatură

Latența principală se măsoară de la captura observației până la momentul în care rezultatul poate fi folosit de consumator. Include cozi, prelucrare, transport și conversia reperelor. Se raportează P50, P95, P99 și cel mai mare interval fără observație validă. Media singură poate ascunde pauze periculoase pentru utilizare.

Pentru sesiuni de cel puțin 30 minute se înregistrează configurația, temperatura/starea termică disponibilă, cadrele abandonate, memoria, debitul și energia prin metoda disponibilă. Dacă energia este estimată indirect, instrumentul și limitele sunt explicate. Ecranul, încărcarea, carcasa și temperatura ambientală sunt controlate sau raportate.

Se compară unul, două și patru joburi grele concurente, dacă implementarea și resursele permit. Mai mult paralelism nu este criteriu de succes. Configurația acceptată minimizează latența și consumul în condițiile limitelor de eroare; competiția pentru GPU poate face configurația cu patru joburi mai slabă.

## 9.7 Ablations și analiza statistică

Experimentele dezactivează pe rând adâncimea, modelul anterior, rafinarea geometrică, prioritizarea, compresia și corecțiile globale. Restul configurației și bugetul sunt păstrate comparabile. Versiunea completă nu primește un set de date mai ușor.

Intervalele se estimează ținând cont de gruparea pe obiect sau cameră; cadrele nu sunt tratate ca mii de replici independente. Pentru P95 se fixează metoda de cuantile și bootstrapul pe grup înainte de evaluare. O coadă insuficient eșantionată nu poate susține un P99 stabil. Se raportează atât efectul cât și incertitudinea, iar comparațiile multiple sunt identificate.

## 9.8 Erori și întreruperi injectate

Lotul include ordine inversată a pachetelor, duplicate, pierderea legăturii, reconectare, schimbarea epocii, lipsa transformării, offset temporal, presiune de memorie și oprirea procesului în timpul salvării. Pentru fiecare caz se verifică starea înainte, evenimentul injectat, starea recuperată și hashurile obiectelor deja confirmate.

Rezultatul acceptabil poate fi respingerea explicită a datelor ori oprirea controlată, nu neapărat continuarea cu orice preț. Refacerea legăturii de rețea nu reautorizează automat mișcarea robotului. Restaurarea proiectului nu reintroduce imagini într-un mod live fără persistență.

## 9.9 Pachetul reproductibil

Fiecare rulare păstrează run_id, commit sau versiune, configurația exactă, manifestul datelor, seed când există aleator, schema rezultatelor, logurile, metricile și limita de acces la date personale. Hashurile permit verificarea identității fișierelor, dar nu certifică autenticitatea fizică a capturii.

Un al doilea operator trebuie să poată calcula aceleași metrici din datele aprobate, cu toleranțe numerice declarate. Dacă biblioteca folosește operații GPU nedeterministe, se raportează dispersia rerulărilor. Rezultatele negative și rulările incomplete rămân în registru, cu motiv de excludere stabilit și verificabil.
