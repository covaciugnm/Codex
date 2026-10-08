# Verifică API-ul REGIS

ID: `01a11168-ab9e-7910-8d91-0d0729122c5e`  
Proiect: iDempiere  
Export UTC: 2026-10-08T14:13:28.280906+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Utilizator

Exista API pentru Regis ? 
Am localizat iDempiere si compatibilizat cu SAGA si dorim sa avem comunicare cu REGIS - cum sa procedam ?


## Asistent

Voi verifica dacă vă referiți la REGES-ONLINE și ce opțiuni oficiale de integrare există pentru iDempiere.

## Asistent

**Da — dacă vă referiți la REGES-ONLINE, registrul salariaților al Inspecției Muncii, există API pentru integrarea aplicațiilor proprii.** Puteți conecta iDempiere direct. Compatibilizarea cu SAGA ajută la schimbul de date existent, dar conectarea la REGES necesită un conector dedicat.

Documentația pentru dezvoltatori este disponibilă în [reges-ro/integrare](https://github.com/reges-ro/integrare), împreună cu schema XSD, exemple Java și o colecție Postman. API-ul acceptă XML și JSON, pentru salariați, contracte și operațiuni precum suspendări, încetări sau detașări.

Pentru situația voastră, recomand următorii pași:

1. **Stabiliți unde se gestionează datele de personal.** Dacă salariații, contractele și actele adiționale se întrețin în iDempiere, acesta ar trebui să genereze raportările REGES. Dacă sunt întreținute în SAGA, trebuie definit cum ajung în iDempiere și cine transmite fiecare modificare. Aș desemna o singură aplicație responsabilă de transmiterea fiecărui contract, pentru a evita dublările.

2. **Configurați accesul pentru angajator.** Aplicația REGES include configurarea cheilor API în setările angajatorului. Conectorul trebuie să păstreze credențialele separat pentru fiecare firmă/CUI și pentru fiecare mediu. [Ghidul oficial pentru angajatori](https://reges.inspectiamuncii.ro/ajutor/ghid-utilizare-aplicatie-angajator/)

3. **Faceți corespondența între datele voastre și câmpurile REGES.** Verificăm salariatul, identificarea contractului, datele de început și modificare, ocupația, salariul, sporurile, norma și programul de muncă. Compatibilitatea contabilă cu SAGA nu garantează că toate aceste informații sunt deja disponibile în iDempiere.

4. **Implementați conectorul și urmărirea rezultatelor.** Aș construi un modul cu o coadă persistentă de transmiteri, validare înainte de expediere, jurnal și ecran de erori. **Recipisa inițială confirmă intrarea în coadă; succesul operațiunii se verifică ulterior**, prin răspunsul asincron. Documentația descrie și asocierea identificatorilor REGES cu salariații și contractele locale. [Fluxul API](https://github.com/reges-ro/integrare#2-principii-de-functionare-api)

5. **Testați înainte de conectarea la producție.** Există un [portal de test](https://reges.dev.inspectiamuncii.org) și [Swagger pentru API-ul de test](https://api.dev.inspectiamuncii.org/swagger/). Pilotul ar trebui să acopere preluarea referințelor contractelor existente, un salariat nou, un contract nou, o modificare și tratarea unei respingeri. [Documentația mediului de test](https://github.com/reges-ro/integrare#7-mediul-de-test)

Fluxul pe care îl propun este:

```text
Date HR din iDempiere
        ↓
Validare și aprobare pentru transmitere
        ↓
Coadă de mesaje → API REGES
        ↑              ↓
Stare și erori ← Rezultatul procesării
```

**Primul pas concret este inventarierea modulului de personal și a schimbului existent cu SAGA**, pentru a identifica datele lipsă și a stabili sursa fiecărei modificări.

În configurația voastră actuală, **salariații și contractele sunt gestionați în iDempiere sau în SAGA?** Și integrarea cu SAGA acoperă și salarizarea, ori doar contabilitatea?

## Utilizator

În configurația voastră actuală, **salariații și contractele sunt gestionați în iDempiere** &#x20;
integrarea cu SAGA acoperă și salarizarea = este o tranzitie de la SAGA la iDempiere - dorim sa renuntam la SAGA complet


## Asistent

Atunci **iDempiere devine sistemul principal pentru personal, contracte și salarizare, iar legătura cu REGES trebuie construită direct din iDempiere**. SAGA rămâne temporar sursă pentru migrare și verificarea rezultatelor.

Aș organiza implementarea în două direcții care se întâlnesc la momentul trecerii definitive:

| Direcție | Ce trebuie realizat |
|---|---|
| **Conector iDempiere–REGES** | Asocierea salariaților și contractelor existente cu identificatorii REGES; transmiterea modificărilor; preluarea confirmărilor și erorilor |
| **Înlocuirea completă a SAGA** | Migrarea istoricului necesar; verificarea calculului salarial, declarațiilor, plăților și înregistrărilor contabile |

**Pentru conector, propun un modul dedicat în iDempiere**, cu:

- Configurare pentru fiecare angajator: CUI, mediu de test/producție și credențiale protejate.
- Corespondență între identificatorii locali și cei din REGES.
- Validări ale datelor înainte de transmitere.
- O coadă persistentă de operațiuni, care păstrează exact versiunea datelor trimise.
- Un ecran cu stările „Pregătit”, „În așteptarea rezultatului”, „Confirmat” și „Respins”, plus explicația erorii.
- Istoric al transmiterilor și recuperare după întreruperi, cu verificări pentru evitarea dublării operațiunilor.

La pornire, trebuie **reconciliate contractele deja existente în REGES cu cele din iDempiere**. Pentru acestea folosim referințele REGES existente; crearea lor din nou ar produce probleme de duplicare.

Pentru renunțarea la SAGA, recomand o dată clară de trecere și o perioadă de verificare în care calculați aceleași salarii în ambele aplicații, dar desemnați o singură aplicație responsabilă de raportările efective. Comparația trebuie să includă brutul, contribuțiile, impozitul, netul, concediile, reținerile și notele contabile. Diferențele se explică și se corectează înainte de trecerea definitivă.

**Integrarea REGES și înlocuirea salarizării sunt două livrabile distincte:** un conector funcțional nu validează automat calculele salariale sau declarațiile.

Următorul pas este analiza implementării voastre actuale pentru a construi o mapare concretă „câmp iDempiere → câmp REGES” și lista funcțiilor rămase pentru eliminarea SAGA. **Modulul de personal și salarizare este dezvoltat de voi sau este bazat pe un plugin existent?**
