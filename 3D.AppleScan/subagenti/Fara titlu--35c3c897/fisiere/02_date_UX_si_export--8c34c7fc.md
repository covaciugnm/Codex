# 2. Date locale, experiența utilizatorului și exporturi verificabile

**Adaptarea contractelor:** manifestul folosește șiruri zecimale pentru revizii și dimensiuni de fișier, fără pierdere prin parsere JSON cu numere flotante. Baza SQLite locală folosește INTEGER semnat pentru revizii și lungimi; importatorul respinge valori peste 9 223 372 036 854 775 807 înainte de conversie. Epocile de transport rămân TEXT în SQLite pentru întreg domeniul UInt64, verificat semantic de adaptor. Pozele metrice ale camerelor și obiectelor sunt artefacte CAS JSON; manifestul le expandează în câmpurile `project_from_room` și `pose`. Un manifest `draft` poate avea liste goale; `processed` cere geometria corespunzătoare modului. O bază de date conține un singur proiect.

**Statut:** proiect tehnic V2; persistența, exporturile și interfețele sunt specificate, nu implementate în aplicația iOS. Autor: agentul proiectant iOS/CV. Profilul de referință este iPhone 17 Pro Max, cu OS și SDK final identificate la prima probă; Jetson AGX Thor este destinație opțională pentru procesare autorizată. Site-ul comercial existent nu este baza de date a capturilor.

## 2.1. Modelul de proiect și sursa de adevăr

Un proiect persistent este un container cu identificator UUID, titlu, tip obiect/camere, unitate internă metru, referințe de calibrare și revizii imuabile ale rezultatelor. O revizie nouă nu înlocuiește silențios observația inițială. Datele brute, geometria derivată, corecțiile manuale și exporturile au proveniență diferită și pot avea politici de retenție diferite.

Un proiect nu este același lucru cu sesiunea camerei. Același proiect poate avea mai multe sesiuni, iar o sesiune poate eșua fără a pierde reviziile deja confirmate. `project_id` este identitatea persistentă. `session_id` este identitatea procesului/sesiunii operaționale negociate; `map_epoch` identifică reperul hărții, iar `clock_epoch` domeniul temporal continuu. Valorile epoch și secvențele sunt stringuri zecimale în manifest, convertite verificat la întregi în cod.

`project.schema.json` validează manifestul proiectului salvat, nu pachetele robotice și nu memoria live. Schema declară exact tipuri, câmpuri obligatorii, enum-uri, hashuri, lungimi de vectori și interdicția câmpurilor suplimentare. Sunt necesare verificări semantice suplimentare pentru unicitatea ID-urilor, existența referințelor, norma cuaternionului, date ordonate temporal și limitele uint64. JSON Schema nu rezolvă singur aceste relații și documentul nu pretinde contrariul.

## 2.2. Alegerea SQLite și a fișierelor după hash

Alegem SQLite pentru metadate și un depozit de fișiere adresate prin conținut, CAS, pentru imagini, geometrii și exporturi. `PersistenceActor` deține o singură conexiune de scriere. Modul inițial este `journal_mode=DELETE`, `synchronous=FULL`, `foreign_keys=ON`, cu tranzacții scurte. Interfața primește snapshoturi ale datelor și nu menține citiri de bază deschise pe durata unei capturi.

Alternativa Core Data/SwiftData ar simplifica unele ecrane, însă aici urmărim explicit ordinea fișier–commit, cheile de idempotentă, schema portabilă pentru audit și compatibilitatea cu receptorul. Alegerea SQLite nu interzice un strat convenabil de acces; interzice doar ca migrarea și confirmarea rezultatelor să devină comportament opac. SQLite oferă tranzacții și integritate referențială, iar foreign keys trebuie activate și verificate pe conexiune. [I18 — SQLite foreign keys](https://sqlite.org/foreignkeys.html)

WAL este o alternativă pentru mai multă concurență, dar nu baseline-ul. Documentația curentă SQLite identifică un defect WAL de resetare corectat în 3.51.3 și backporturi, relevant pentru conexiuni care scriu și fac checkpoint concurent. Alegerea DELETE cu o conexiune evită dependența inițială de acel scenariu și de versiunea SQLite inclusă de OS. WAL poate fi activat ulterior numai prin ADR, verificarea versiunii/remedierii și teste dedicate. [I19 — WAL, secțiunea 11](https://sqlite.org/wal.html)

FULL este ales pentru confirmări persistente, cu costul aferent sincronizării; comportamentul real la întrerupere trebuie tot testat pe dispozitiv. O setare PRAGMA nu poate certifica singură întregul traseu hardware și filesystem. [I20 — synchronous](https://sqlite.org/pragma.html#pragma_synchronous) Modelul de date propus este inclus în `local_schema.sql`; nu conține valori ale unor scanări inventate.

## 2.3. Layout local și restricțiile căilor

Fiecare proiect are în sandbox `Application Support/Projects/<project_id>/project.sqlite`, `cas/<primele_două_hex>/<sha256>`, `staging/<job_id>/` și `exports/`. Extensia vizibilă a unui fișier de export poate fi reconstruită din manifest; adresa CAS rămâne hashul octeților. Identificatorul nu este numele introdus de utilizator. Un titlu cu slash, diacritice ori emoji nu devine cale de fișier.

Fișierele brute autorizate și rezultatele confirmate sunt păstrate în Application Support, cu protecția de date potrivită aplicației. Copiile pentru preview pot sta într-un cache regenerabil. Excluderea backupului se decide pe tip de date și este prezentată utilizatorului; nu denumim „cache” singura copie a unei capturi originale. Pentru export prin Files sau share sheet producem o copie verificată, iar dreptul de acces al aplicației destinatare este separat de existența proiectului intern.

Importurile sunt limitate înainte de parsare: maximum 512 MiB pentru pachetul inițial de model, maximum două milioane de triunghiuri după parsare și un buget total decomprimat de 1 GiB pentru profilul experimental. Pragurile sunt limite de proiectare reevaluate pe 17 Pro Max, nu limite Apple. Path traversal, legături externe și expansiunea arhivelor peste cotă sunt respinse. Texturile trebuie să rămână în containerul importat; lipsa lor nu autorizează căutarea pe disc sau internet.

## 2.4. Ordinea tranzacțională și confirmarea

Pentru salvarea unei geometrii, workerul scrie întâi un fișier temporar într-un director staging de pe același volum. Calculează hashul pe octeții finali, verifică dimensiunea și sincronizează scrierea prin API-ul filesystem disponibil. Mută fișierul către calea CAS, verifică existența și hashul, apoi deschide o tranzacție SQLite care adaugă artefactul, revizia și evenimentul. Numai după commit returnat cu succes se afișează „Salvat”.

Nu presupunem o tranzacție atomică comună SQLite–filesystem. Algoritmul este proiectat să lase, în cel mai rău caz, fișiere orfane înaintea commitului, care pot fi recuperate sau colectate ulterior. El nu publică intenționat o referință spre un fișier încă nescris. Fișierele confirmate nu sunt șterse de garbage collection înainte ca toate reviziile active și joburile să renunțe tranzacțional la referințe.

La pornire se verifică integritatea bazei și a artefactelor necesare ultimei revizii. `SQLITE_BUSY`, disc plin și eroare de sincronizare au coduri diferite. O eroare de commit nu produce automat o a doua salvare cu ID nou: se caută cheia operației pentru a vedea dacă primul commit a fost confirmat înainte de întrerupere. Logul UI nu este sursă de adevăr pentru durabilitate.

Politica de curățare păstrează stagingul unei operații neconfirmate până la clasificare. Garbage collection este un job separat, cu mark-and-sweep bazat pe referințele dintr-un snapshot consistent și fără ștergerea intrărilor unui job activ. Oprirea procesului după redenumirea CAS și înaintea commitului este un test obligatoriu. Ștergerea unui proiect confirmată utilizatorului este un alt flux, cu tratarea explicită a copiilor exportate, care pot aparține altor aplicații.

## 2.5. Joburi persistente și reluare

Cheia unui job derivat este hashul concatenării canonice a tipului operației, reviziei intrărilor, parametrilor și versiunii algoritmului. Două cereri identice reutilizează același rezultat confirmat. Schimbarea toleranței de simplificare sau a unui model ML creează alt job. `attempt` numără încercările fizice, nu creează automat un alt rezultat logic.

Stările sunt queued/running/checkpointed/completed/failed/cancelled/needs_recapture. `running` conține un lease cu termen și proprietar; după restart, lease-ul expirat permite o nouă încercare în urma verificării checkpointului. `completed` cere un hash de ieșire și tranzacția rezultatului. Un export anulat păstrează proiectul și poate elimina temporarul, dar nu modifică exportul confirmat anterior.

Checkpointul salvează etapa, indexul unității de lucru, intrările cu hash, parametrii și ultima ieșire confirmată. Pentru algoritmii proprii ținta canonică de cel mult cinci secunde se referă numai la observații serializabile eligibile, nu la memoria internă ARKit. Pentru Object Capture/RoomPlan salvăm datele pe care API le expune și reluăm etapa permisă; dacă lipsesc, starea devine needs_recapture. Nu promitem reluarea exactă a unei optimizări interne opace.

Migrarea bazei folosește număr de schemă, hashul scriptului și tranzacție. Pentru o migrare care transformă fișiere mari, copiem spre revizie nouă și păstrăm sursa până la acceptare. Downgrade-ul nesuportat este refuzat; utilizatorului i se oferă exportul sau revenirea la backup verificat. Nu deschidem în scriere un proiect nou cu o aplicație veche doar pentru că SQLite poate citi tabelele.

## 2.6. Modul live fără salvare

`live_ephemeral` construiește un `SessionContext` fără PersistenceActor, fără registru persistent de proiect și fără RobotLink. Este o restricție de injectare a dependențelor, nu un simplu checkbox în recorder. Bufferele, cotele și ancorele temporare rămân în memorie. La oprire sau intrarea în fundal se elimină referințele EVA și se invalidează sesiunile; nu promitem ștergerea fizică instantanee a fiecărui bit din bufferele gestionate de sistemul de operare.

Diagnosticarea implicită poate include cod de eroare și contoare agregate, fără imagine, mesh, coordonate de mediu, titlu de proiect sau inventar. Nu scriem stack dump-uri cu payloaduri brute în log. Pentru cercetare există un mod separat de captură diagnostică, ales explicit, care afișează ce date vor fi păstrate și durata retenției. El nu este denumit live fără salvare.

Butonul „Salvează fotografia cotată” îngheață numai cadrul ales și adnotările vizibile. Înaintea persistării prezintă destinația și conținutul. Dacă utilizatorul anulează share sheet-ul, copia temporară este eliminată conform politicii și proiectul live rămâne nesalvat. O astfel de imagine nu include implicit harta, istoricul pozițiilor sau cadrele anterioare. Probe pe disc, rețea, cache și crashlogs vor verifica efectiv această limită.

## 2.7. Fluxurile UX concrete

Prima pagină spune „Scanez obiecte cu dimensiuni”, „Măsor acum” și „Scanez camere”. Sub acestea există „Ce vreau să obțin”: model imprimabil, fotografie cotată, plan de cameră, amplasare mobilier sau catalog robotic. Profilurile arhitect/designer/meșter/maker/personal filtrează exemplele și explicațiile, fără să schimbe matematica măsurării. Modul robot este într-o secțiune explicită de conectare, nu activat automat la detectarea rețelei.

Permisiunea camerei este cerută când utilizatorul începe o activitate care o necesită, după o explicație scurtă. Refuzul nu blochează importul și vizualizarea proiectelor existente. Permisiunea de acces la rețea locală este cerută numai la conectarea unui robot ori serviciu ales. Aceste stări sunt testate din instalare nouă, după refuz și după revenirea din Settings.

**Obiecte:** alegere rezultat → verificare capabilități → obiect și scară de referință → captură ghidată → control acoperire → reconstrucție → revizie geometrică → export. Preview-ul arată separat suprafețe observate și completate. Dimensiunea este însoțită de metoda de obținere și profilul de validare, nu de o precizie universală. Utilizatorul poate reveni la o zonă lipsă fără a pierde captura confirmată.

**Măsurare live:** intrare cameră → tracking stabil → selectare capete/reper → cotă → ajustare capete → eventual salvare explicită de foto → ieșire cu eliminarea sesiunii. Dacă trackingul se pierde, cota este marcată indisponibilă sau ultima valoare validă, cu etichetă clară; nu continuăm animarea unei valori care pare măsurată. Markerii și liniile au contrast, grosime și etichete accesibile, fără dependență exclusivă de culoare.

**Camere:** proiect → prima cameră → scanare → verificare pereți/goluri → salvare cameră → trecere într-o zonă comună → camera următoare → unire → verificare aliniere → plan/export. Dacă reperul comun lipsește, se cere relocalizare sau aliniere manuală cu referințe și proveniență. Corecția manuală nu este ascunsă în rezultatul automat. Nivelurile diferite au identitate explicită, dar calificarea extinsă a clădirilor rămâne o etapă proprie.

Stările comune afișate sunt pregătire, capturare, procesare, necesită intervenție, rezultat parțial, salvat și eroare recuperabilă. Progresul procentual este afișat numai când motorul furnizează un progres interpretabil; altfel arătăm etapa și timpul scurs. Un estimate time necalibrat nu este prezentat ca promisiune. VoiceOver anunță schimbările importante fără a citi toate cadrele; UI păstrează focusul și proiectul la schimbarea limbii între en/de/fr/es/ro/hu/bg.

## 2.8. Exporturile de bază și contractul conversiei

`ExportService` primește un `ExportRequest` cu project_id, revision_id, format, profil, unitate și set de opțiuni. Returnează job_id; rezultatul conține SHA-256, dimensiunea, avertismentele, versiunile și un raport de verificare. Niciun adaptor nu poate cere geometria „cea mai recentă” în timpul scrierii: intrarea este o revizie imuabilă. Exportul are aceeași cheie logică la reluare și nu produce fișiere diferite fără a explica parametrul schimbat.

| Format | Implementare inițială propusă | Verificare și pierderi declarate |
|---|---|---|
| STL binar | Serializer propriu restrâns la mesh triangulat, coordonate exportate în mm | Fără unitate nativă sigură sau texturi; unitatea apare în manifest; reimport numeric |
| 3MF | Adaptor de pachet conform subsetului ales, după fixture și audit bibliotecă/spec | Unități și mesh în profil declarat; extensiile neimplementate sunt refuzate |
| PLY | Serializer cu header explicit și poziții/culoare, subset fix | Nori sau mesh distincte; lipsa semanticii de cameră este declarată |
| USDZ | Ieșirea Apple disponibilă plus manifestul EVA | Bun pentru preview; nu echivalează cu plan cotat CAD |
| DXF 2D | Writer restrâns pentru plan, entități/layers/unități/cote explicit implementate | Nu pretinde BIM sau solid parametric; verificare într-o destinație CAD aleasă |
| DWG | Job de conversie separat, numai după alegerea unei căi licențiate | Nu se activează doar schimbând extensia; versiune și subset testate |

P0 păstrează 3MF/STL/PLY/USDZ/DXF ca obiective de produs, în acord cu etapizarea canonică. Nu susținem că toate trebuie dezvoltate în aceeași săptămână. OBJ/glTF/GLB, E57, LAS/LAZ, XYZ/PTS și PCD urmează în etapa avansată conform cererii și valorii pentru utilizatori. IFC/STEP necesită semantică sau reconstrucție parametrică, deci sunt programe distincte, nu exporturi gratuite din triunghiuri.

Conversia geometrică folosește fixture-uri exacte și comparație după reimport fără scară liberă. Toleranța numerică a exportului nu este precizia scanării. Pentru lungimea L în mm, criteriul canonic de conversie este eroare maximă `≤ max(0,01 mm, 10^-5 × L)` pe subsetul declarat; geometria fizică are propriul profil. Pentru imprimare se verifică separat topologia, peretele minim, orientarea, suporturile și slicerul. G-code este rezultatul unui profil de imprimantă/material, nu un export universal EVA.

## 2.9. Procesare pe Thor și protecția datelor

Jetson AGX Thor poate primi un pachet explicit ales pentru reconstrucție sau estimare grea. Pachetul conține doar intrările necesare, hashurile, versiunea jobului și politica de retenție. Nu trimitem automat fotografiile unei locuințe doar pentru că este disponibil un calculator puternic. Pentru transmiterea robotică în timp real utilizăm contractul separat și indicatorul persistent de partajare.

Autorizarea destinației se bazează pe asocierea dispozitivului și credențiale, nu pe un IP familiar. Un rezultat revenit de la Thor este verificat față de job_id, intrări și versiune înainte de import. Întreruperea conexiunii nu șterge originalul; un rezultat duplicat identic este idempotent, iar același ID cu hash diferit produce conflict. Conversia DWG pe server necesită în plus gate de licență și compatibilitate, independent de existența hardware-ului NVIDIA.

Nu atașăm un PostgreSQL direct aplicației mobile și nu folosim serverul web de prezentare drept depozit implicit. Dacă va exista serviciu cloud multiutilizator, acesta va avea API, identitate, retenție și model tranzacțional propriu. SQLite rămâne baza locală offline; PostgreSQL poate fi alegerea unui serviciu ulterior, fără a obliga captura de bază să depindă de internet.

## 2.10. Plan de verificare a acestei implementări

Contractul SQL va fi exercitat pe bază temporară: foreign keys, CAS lipsă, unicitate job, restricții de stare, revenire după rollback și migration_id duplicat. Schema JSON va avea exemple pozitive și negative pentru unități, câmpuri necunoscute, dimensiuni vectori, hashuri, tip de proiect și referințe. Testele semantice verifică ceea ce schema nu poate exprima și nu sunt declarate „trecute” doar din validarea JSON.

Pentru fișiere injectăm opriri înainte și după scriere, sincronizare, mutare CAS și commit. Cerem zero pierderi ale rezultatelor confirmate în lotul canonic de întreruperi. Pentru live inspectăm persistența și traficul în sesiuni instrumentate. Pentru UX folosim participanți independenți de autorii interfeței și păstrăm numitorul tuturor încercărilor; țintele canonice rămân propuse până la executare.

Release-ul unui adaptor de export cere: fixture numeric, reimport în aplicația destinație, avertismente pentru informații pierdute, documentarea licenței și testele pe profilul iPhone 17 Pro Max. Migrarea către iPhone 18 Pro Max repetă probele de captură și resurse, dar nu rescrie proiectele vechi pentru a le atribui noua precizie. Astfel, utilizatorul primește un rezultat urmărit de la observație la fișier, cu limite clare și o cale concretă de reluare.
