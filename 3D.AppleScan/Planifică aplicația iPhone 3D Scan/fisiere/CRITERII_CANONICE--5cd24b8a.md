# Criteriile canonice și porțile de acceptare

Acest fișier are autoritate pentru interpretarea pragurilor. Criteriile din CRITERII_MOSTENITE sunt păstrate pentru proveniență; clarificările de mai jos rezolvă agregarea lungimilor diferite și calificarea extinderii robotice. Toate pragurile aplicației sunt propuneri nevalidate. Acceptarea dosarului nu înseamnă trecerea acestor teste.

## Dimensiuni și rata capturilor valide

Pentru încercarea i, L_i este lungimea independentă de referință în mm, e_i este eroarea absolută, iar tol(L_i) este toleranța de mai jos. Definim r_i=e_i/tol(L_i). Pragul se aplică distribuției r pe observațiile valide dintr-un profil material/dispozitiv/condiții declarat. Criteriul este limita superioară a intervalului de încredere de 95% pentru P95(r) ≤1. Astfel, lungimi diferite nu sunt comparate cu un singur L arbitrar. Raportăm suplimentar eroarea în mm pe straturi de lungime preregistrate.

| Profil | Domeniu propus | tol(L) |
|---|---|---|
| Obiecte | Rigide, mate, suficient texturate, 100–1000mm | max(5mm,0.01L) |
| Live | 200–5000mm, puncte/suprafețe observabile | max(20mm,0.01L) |
| Camere | 1000–8000mm, repere accesibile | max(30mm,0.01L) |
| Conversie digitală | Fixture exact pe subsetul de export declarat | max(0.01mm,10⁻⁵L), aplicat ca eroare maximă, nu P95 |

Propunem suplimentar o poartă de disponibilitate: cel puțin 95% dintre toate încercările eligibile trebuie să producă rezultate valide și limita inferioară CI95 pentru această rată să fie cel puțin 90%. O captură validă produce un rezultat finit și complet pentru măsurand, independent de trecerea toleranței dimensionale. Eligibilitatea se stabilește înainte de captură; un eșec de tracking sau reconstrucție nu este exclus ulterior. Intervalul folosește resampling pe obiect/cameră sau o metodă care modelează gruparea, definită înainte de calificare. Aceste două condiții nu garantează rata de succes în alte populații. Dacă eșantionul nu susține intervalul, rezultatul este inconcludent.

Studiul final se dimensionează după pilot. Cadrele din aceeași sesiune nu sunt replici independente. Nu se rescalează rezultatele cu referințele ținute pentru evaluare. Suprafețele din afara domeniului sunt raportate separat, cu eșecuri și comportament UX, fără a fi promovate ca profil calificat.

## Poziția 6D și identitatea

Ținta de pilot EX-06 este P95 al translației ≤30mm și P95 al rotației ≤5° pentru obiecte asimetrice în condițiile declarate. Este un reper de explorare, nu toleranță de prindere robotică sau promisiune de release. Simetriile se evaluează cu echivalențele explicite ale modelului; orientarea neobservabilă rămâne ambiguă. Pragurile de recall, schimbări de identitate și utilizare robotică se fixează după pilot înainte de setul final, prin decizie auditată. În lipsa lor, acea funcție nu poate primi acceptare operațională.

Zero rezultate prezise pot fi etichetate ca observații curente. Fiecare rezultat are referință temporală și spațială, versiune și status al incertitudinii. Covarianța indisponibilă nu este reprezentată drept certitudine zero. EX-06/07 includ subtestele PER și APP-IF din capitole.

## Performanță și continuitate

P95≤100ms în EX-08 este ținta inițială pentru fluxul prioritar, măsurată captură–utilizare în configurația declarată. Nu este deadline universal de robot. Se raportează și P99, gap maxim, cadre abandonate și starea termică. Sesiunile uzuale de performanță sunt minimum3×30minute/configurație; stresul de rețea NET-06 este60minute. Aceste durate au scopuri diferite.

Recuperarea nu pierde date deja confirmate. Pierderea de maximum5s privește numai observații serializabile eligibile în fluxurile persistente controlate de aplicație, între checkpointuri. Se măsoară cu același ceas monoton înainte/după. Starea internă opacă a API-urilor are recuperare best effort; modul live nu păstrează mediul. Lotul de acceptare include50întreruperi, iar1000reprezintă stres ulterior.

## Robot și transport

Înainte de mișcare se închid W09 calibrare, W10 transport, W11 observație/simulare și W13 securitate. Sunt obligatorii pragurile și testele de timp, vechime, transformări și reacție aprobate pentru robot, viteză și spațiul de test. Un prag exploratoriu nu poate autoriza mișcarea. Deadline-ul rezultă din analiza distanțelor, vitezelor și comportamentului robotului și se verifică pe banc.

RB-03 propune ca punct de pornire eroare de sincronizare P95≤5ms; limita admisă efectiv se deduce din eroarea geometrică acceptabilă la viteza unghiulară/translațională testată. NET-01…11 și RB-01…07 sunt subteste obligatorii ale experimentelor EX relevante. Zero actualizări cu sesiune, epocă, secvență sau timp invalid pot fi aplicate. Identitatea după snapshot se verifică pe serializare canonică și hash semantic declarat.

## UX confidențialitate și export

UX are lot final de20participanți noi:18/20aleg modul≤10s;16/20finalizează captură/export autonom;18/20interpretează stările. Localizarea verifică7limbi și toate fluxurile anunțate. Modul live are50sesiuni fără persistență/upload implicit, plus20anulări și20salvări explicite.

Fiecare subset export trece fixture numeric și import în aplicația destinatară. Printarea are probă fizică separată. DWG nu se declară disponibil fără licență și integrare verificate. P0/P1/P2 sunt priorități de produs, distincte de severitățile auditului.

## Acceptarea documentară

G0 cere registre coerente, toate cerințele legate de teste, toate sarcinile cu autor și auditor diferit, artefacte găsibile, zero constatări documentare deschise, document unificat lizibil și copie verificată. Testele fizice rămân not_run. Denumirile EX și subtestele nu reprezintă rezultate executate.

La conflict între o formulare prescurtată dintr-un capitol și această definiție statistică, se aplică definiția de aici. Orice modificare viitoare se înregistrează în decizii, schimbă revizia pragului și redeschide auditul relevant.

