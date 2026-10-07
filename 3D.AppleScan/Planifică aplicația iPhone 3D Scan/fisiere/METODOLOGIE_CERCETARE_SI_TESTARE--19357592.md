# Metodologia de cercetare și verificare

## Întrebările cercetării

R1: În ce condiții oferă fiecare metodă de captură dimensiuni utile pentru obiecte și camere? R2: Cât reduc o referință de scară și ghidarea capturii eroarea? R3: Ce erori adaugă unirea camerelor și conversia formatelor? R4: Poate utilizatorul recunoaște o măsurare nesigură? R5: Cum se păstrează continuitatea proiectului în prezența întreruperilor fără a încălca modul temporar?

Ipoteze propuse: ghidarea reduce rata capturilor eșuate; o scară verificată reduce eroarea sistematică; segmentarea pe camere reduce pierderea muncii; avertizările explicite reduc acceptarea unor cote instabile. Aceste ipoteze trebuie testate și pot fi respinse.

## Fundament și limite ale literaturii

NIST explică de ce trasabilitatea aparține rezultatului măsurării și necesită un lanț documentat de comparații și incertitudini. Un instrument de referință calibrat nu face automat trasabil orice rezultat obținut cu el. Această distincție justifică păstrarea metodei și a dovezilor în aplicație. [MGR-S01](https://www.nist.gov/metrology/metrological-traceability)

Ghidul NIST TN1297 oferă un cadru pentru evaluarea componentelor de incertitudine și raportarea lor. Planul nostru separă dispersia repetărilor de eroarea față de referință și de intervalul de incertitudine raportat. Nu presupune că rezoluția afișată pe ecran este egală cu precizia. [MGR-S02](https://www.nist.gov/document/tn1297spdf)

Două articole identificate despre LiDAR Apple, în patrimoniu și în măsurarea arborilor, sunt în registrul de lectură suplimentară. Accesul integral prin instrumentul de navigare a returnat HTTP 429. Nu sunt folosite aici pentru praguri numerice sau concluzii detaliate; lectura integrală rămâne de completat.

## Organizarea unei cercetări reproductibile

Înaintea experimentelor se îngheață protocolul, criteriile de excludere, dispozitivele, metodele și rezultatele primare. Se păstrează atât capturile reușite, cât și eșecurile. Datele de reglaj sunt separate de datele de evaluare. Un obiect sau o cameră folosită pentru reglarea algoritmului nu se reutilizează drept dovadă independentă fără marcaj.

Pentru fiecare execuție se înregistrează: run_id, experiment_id, versiune aplicație, OS, model hardware, metodă, operator pseudonimizat, condiții de iluminare, obiect/cameră, referință, repetare, stare termică, durată, dimensiuni, erori, fișiere și hashuri. Nu se completează un rând cu rezultate simulate ca și cum ar proveni de la telefon.

Sursa propusă de adevăr pentru dimensiuni este un instrument adecvat și verificat: șubler sau etalon pentru obiecte, distanțometru și repere pentru camere, scaner de referință pentru geometrie când este disponibil. Calitatea referinței, amplasarea și incertitudinea sa trebuie documentate. Nu este suficient un model CAD nominal al unei piese imprimate cu contracții necunoscute.

## Experimente funcționale

| Experiment | Protocol propus | Rezultat și criteriu |
|---|---|---|
| DEVICE-EXP | Minimum 3 configurații: iPhone cu LiDAR mai vechi suportat, recent suportat, dispozitiv fără LiDAR | Matrice de capabilități; niciun buton care promite o funcție indisponibilă |
| SCALE-EXP | 30 modele digitale cu referințe de scară și conversii m/mm/inch | Unitățile și transformările rămân explicite; toate cotele afectate invalidate corect |
| METRO-EXP | Aplică loturile și pragurile pe clase din protocolul CAD | Distribuții de erori și rate de eșec; niciun prag declarat trecut fără date |
| ROOM-EXP | 10 proiecte de 3–8 camere, inclusiv buclă de coridor și podele diferite | Raport de derivă, geometrie suprapusă și cote față de referință |
| EXPORT-EXP | Cub 100 mm, cameră sintetică 4 × 3 × 2,5 m, model texturat, nor cu axe asimetrice | Dimensiuni, orientare, unități, texturi și cote verificate în destinatari |
| PRINT-EXP | Import în două slicere și lot fizic conform capitolului CAD | Erorile digitale separate de cele de imprimare și postprocesare |
| RESUME-EXP | 50 întreruperi în captură persistentă, salvare, procesare și export | Niciun rezultat incomplet declarat final; recuperare și pierdere măsurate |
| PRIV-EXP | 50 sesiuni temporare cu inspecția sandboxului și traficului | Zero persistență de mediu gestionată de aplicație; zero upload implicit |
| OFFLINE-EXP | Mod avion; captură, proiecte locale, exporturile locale declarate | Toate funcțiile P0 locale trec; funcțiile dependente de rețea au mesaj clar |
| PERF-EXP | 30 sesiuni de 15 min pe fiecare configurație minimă și recentă | Memorie, FPS, latență, temperatură, baterie; zero crash în lotul testat |
| UX-EXP | Pilot 5 participanți, apoi evaluare 20 cu sarcini prestabilite | Succes, timp, erori, înțelegerea incertitudinii; rezultate segmentate |
| RELEASE-EXP | Revedere dovezi, dispozitive, formate, confidențialitate și incidente | Zero defecte P0/P1 nerezolvate în funcțiile lansate |

Numerele reprezintă un plan inițial de inginerie. Pentru inferență științifică se calculează dimensiunea eșantionului după pilot, efectul minim relevant și variabilitatea observată. Nu se pretinde putere statistică doar pentru că există 20 de participanți sau 50 de execuții.

## Analiza datelor

Pentru fiecare lungime se calculează eroarea semnată `e = L_estimat − L_referință`, eroarea absolută și eroarea relativă doar când referința este nenulă. Se raportează bias, MAE, RMSE, mediana, percentila 95 și cel mai rău caz, împreună cu rata eșecurilor. Eșecurile nu dispar din numitor.

Repetările de pe același obiect sunt corelate. Analiza nu tratează fiecare triunghi sau fiecare cadru drept observație independentă. Intervalele pot fi obținute prin bootstrap pe obiect/cameră sau modele cu efecte mixte, dacă ipotezele sunt potrivite. Se raportează incertitudinea referinței și efectul operatorului, telefonului, materialului și iluminării.

Compararea metodelor folosește aceleași obiecte și condiții în ordine randomizată. Pentru suprafețe se păstrează separat distanțele geometrice și erorile de scară. O aliniere cu scalare liberă poate ascunde eroarea dimensională; evaluarea principală folosește transformare rigidă, iar rezultatele după rescalare sunt etichetate distinct.

Se raportează efectul practic și intervalele, nu numai o valoare p. Dacă se testează multe ipoteze exploratorii, ele se etichetează ca atare și se controlează interpretarea comparațiilor multiple. Rezultatele negative se păstrează în lucrare.

## UX și accesibilitate

Participantul trebuie să poată alege modul corect, să realizeze o captură, să identifice o zonă lipsă, să interpreteze o cotă instabilă, să exporte cu unitatea corectă și să recupereze un proiect. Moderatorul nu ajută înainte de înregistrarea eșecului. Se măsoară timpul, succesul neasistat, erorile și explicația verbală a limitelor. Pilotul și evaluarea principală sunt raportate separat.

Testarea include text mărit, contrast, orientare, utilizare cu o singură mână unde este posibil și etichete VoiceOver. Accesibilitatea capturii vizuale necesită alternative și ghidare auditivă; simpla etichetare a butoanelor nu o dovedește complet.

## Structura propusă a viitoarei teze

1. Problema, contribuțiile propuse și limitele.
2. Stadiul cercetării și criteriile de selecție bibliografică.
3. Modele geometrice, senzori, incertitudine și referințe.
4. Cerințele și cercetarea utilizatorilor.
5. Arhitectura și gestiunea datelor.
6. Captura obiectelor și estimarea dimensiunilor.
7. Măsurarea temporară și protecția datelor.
8. Reconstrucția camerelor și clădirilor.
9. Interoperabilitatea CAD și fabricarea aditivă.
10. Proiectarea experimentelor și seturile de date.
11. Rezultatele, analiza statistică și comparația cu bazele de referință.
12. Discuția, amenințările la validitate, concluziile și lucrările viitoare.

Capitolele 10–12 vor fi completate numai după experimente. O contribuție doctorală posibilă este calibrarea comună a calității cotelor și a alertelor UX pe mai multe metode de captură, însă originalitatea trebuie stabilită printr-o revizuire bibliografică sistematică.

## Registrul de rezultate

Șablonul CSV livrat conține antetul fără valori experimentale. Toate testele aplicației sunt `not_run`. Auditul documentar și verificarea integrității fișierelor sunt singurele verificări executabile în această etapă.
