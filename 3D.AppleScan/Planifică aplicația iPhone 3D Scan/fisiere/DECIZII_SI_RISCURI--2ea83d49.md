# Decizii și riscuri

## Decizii de proiectare

| ID | Decizie | Motiv și efect | Stare |
|---|---|---|---|
| ADR-01 | Aplicație nativă iPhone, cu servicii externe opționale | Acces la API Apple și funcționare locală; implementarea se verifică în Xcode | Propus |
| ADR-02 | Trei moduri separate | Intenția utilizatorului și retenția datelor sunt diferite | Acceptat pentru specificație |
| ADR-03 | Metrul intern, conversie explicită | Evită erorile m/mm/inch în export | Acceptat pentru specificație |
| ADR-04 | Originale nemodificate și derivate cu versiuni | Cote și reparații auditabile | Acceptat pentru specificație |
| ADR-05 | DWG prin adaptor licențiat | Nu presupunem exporter nativ Apple sau conversie fără dependențe | Condiționat de probă și licență |
| ADR-06 | Fără salvare implicită în modul live | Respectă cererea de măsurare temporară; foto cotată separat | Acceptat pentru specificație |
| ADR-07 | Praguri metrologice pe clasă de utilizare | Un procent global ar ascunde diferențele dintre obiecte și camere | Acceptat pentru specificație |
| ADR-08 | Documentare locală plus copie în proiect | Continuitate și acces la fișierele cerute | Executat la livrare cu verificare |

## Registrul riscurilor

| ID | Risc | Impact | Măsură și semnal de control | Responsabil |
|---|---|---|---|---|
| R01 | Dimensiuni greșite deși meshul arată bine | Major | Referințe independente, intervale validate, benchmark pe clase | CAD |
| R02 | Schimbarea capabilităților SDK | Major | Versiuni fixate, runtime checks, probe pe device | Apple |
| R03 | Crash, lipsă spațiu, temperatură | Major | Checkpoint, limită sesiune, avertizare și test cu întreruperi | Apple |
| R04 | Derivă între camere sau etaje | Major | Repere comune, raport reziduuri, fuziune reversibilă | Apple/CAD |
| R05 | Pierdere unități sau cote în CAD | Major | Fixtures și import în destinatar; raport de pierderi | CAD |
| R06 | Licență incompatibilă cu distribuția | Major | Inventar pe versiune și dependențe, analiză înainte de integrare | Manager/CAD |
| R07 | Date ale locuinței încărcate implicit | Major | Local implicit, alegere explicită pentru cloud, test de trafic | Apple |
| R08 | Scope prea mare pentru prima versiune | Major | P0/P1/P2 și porți experimentale; funcții nevalidate rămân indisponibile | Manager |
| R09 | Feedback nereprezentativ sau vechi | Moderat | Etichetă anecdotică, versiuni/date, studiu direct de utilizatori | UX |
| R10 | Bibliografie sau linkuri schimbate | Moderat | Metadate, rezumate locale, copii permise și revalidare înainte de implementare | Cercetare |
| R11 | Imprimarea schimbă dimensiunile | Major | Separă eroarea scanării de slicer, material, mașină și postprocesare | CAD |
| R12 | Continuitate falsă după întrerupere | Major | Checkpoint, hash, jurnal, stare nefinalizată verificată înainte de retry | Manager |

## Resurse și costuri de estimat

Necesar pentru P03: Mac compatibil cu toolchainul ales, iPhone cu și fără LiDAR pentru testele de suport, cabluri, spațiu de stocare și conturile de dezvoltare necesare distribuției alese. Pentru metrologie: etaloane sau instrumente de referință adecvate și condiții de iluminare controlate. Pentru print: cel puțin două profile/slicere și imprimantele reprezentative domeniului comercial.

Costurile se bugetează pe categorii: hardware, personal, program Apple, conversie DWG, cloud opțional, stocare, testeri, materiale, mentenanță și audit. Nu există ofertă financiară aprobată în această sesiune. Nicio achiziție, abonare sau publicare nu este efectuată prin redactarea dosarului.
