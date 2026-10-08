## 11 Arhitectura recomandată pentru integrarea completă

Propunem un plugin nou, cu nume de lucru com.eva.ro.qms. Numele, tabelele și fluxurile de mai jos sunt proiectare propusă, nu componente existente în repository. Pluginul reutilizează persoanele AMN/C_BPartner, utilizatorii AD_User, contextul AD_Client/AD_Org și registrul de documente EVA, după validarea schemei efective. [P01–P07]

Fluxul principal este: procedură aprobată → revizie distribuită → angajat instruit → operație și lot → măsurătoare → neconformitate → acțiune → verificarea eficacității. Fiecare săgeată trebuie reprezentată prin chei și evenimente persistente, nu doar prin text liber sau URL.

### 11.1 Entități propuse

| Entitate nouă | Conținut minim | Legătura cu EVA |
|---|---|---|
| EVA_QMS_Document | Cod, titlu, proces, proprietar | AD_Client, AD_Org și sursa |
| EVA_QMS_Revision | Număr, conținut fixat, hash, stare, aplicabilitate | Document și document emis arhivat |
| EVA_QMS_Approval | Decizie, dată, motiv și revizie | AD_User și rolul la momentul deciziei |
| EVA_QMS_Training | Persoană, revizie, citire, instruire, evaluare | C_BPartner și AMN_Employee |
| EVA_QMS_Competence | Operație, nivel, valabilitate și dovadă | Persoană și cerință de proces |
| EVA_QMS_Audit | Program, criterii, auditor și constatări | Firmă, proces și documente |
| EVA_QMS_NC | Origine, severitate, cauză și responsabil | Lot, operație, inspecție și persoană |
| EVA_QMS_Action | Măsură, termen, responsabil și eficacitate | Neconformitate și analiză de rezultat |
| EVA_QMS_Inspection | Plan, caracteristici, eșantion și decizie | Produs, lot și document operațional |
| EVA_QMS_Measurement | Valoare, unitate, timp, instrument și corecții | Inspecție și operator |
| EVA_QMS_AnalysisRun | Metodă, parametri, versiuni și rezultat | Set de măsurători și hash |
| EVA_QMS_IntegrationEvent | Mesaj, stare, încercări și eroare | Cheia instanței și a firmei |

Tipurile de chei, numele finale și tabelele operaționale vor fi alese prin inspecția dicționarului aplicației. Nu presupunem că fiecare referință de lot sau operație există deja în forma necesară. Snapshot-urile de post, departament și rol păstrează contextul istoric fără a înlocui cheia persoanei.

### 11.2 Separarea firmelor și identitatea

EVA descrie cabinete ca instanțe separate și firme prin AD_Client. Cheia externă trebuie să includă cel puțin identificatorul instanței și AD_Client, împreună cu tipul și ID-ul entității; AD_Org se păstrează unde este relevant. Două instanțe pot avea aceleași ID-uri numerice. Un conector care folosește doar C_BPartner_ID poate atribui rezultatul unei alte firme. [P01]

Utilizatorul tehnic primește numai permisiunile necesare. Identitatea transmisă într-un mesaj nu acordă singură acces: serverul verifică apartenența și drepturile. Datele salariale și documentele de identitate nu sunt necesare pentru atribuirea unei proceduri și nu intră în payload-ul standard.

### 11.3 API și contractul mesajelor

Pluginul REST iDempiere documentează autentificare, modele, procese și alte resurse. Documentația publică și branch-ul consultat nu certifică versiunea instalată în EVA 13. Se verifică endpoint-urile din mediul de test înainte de dezvoltarea conectorului. [I01–I04]

Un mesaj va conține eventId, schemaVersion, sourceInstance, tenantKey, entityType, entityKey, entityVersion, occurredAt și payload. eventId se păstrează la reîncercare. Consumatorul respinge duplicatele fără repetarea efectului, compară versiunea entității și izolează mesajele nereușite pentru diagnostic. O eroare temporară nu trebuie să piardă evenimentul.

Scrierile în business se fac prin PO, procese native sau API autorizat. Un jurnal outbox poate fi proiectat în plugin pentru livrare după tranzacția de business. Politica de conflict se stabilește per entitate: EVA deține identitatea, produsul și rezultatul operațional; aplicația QMS externă poate deține conținutul aflat în redactare. Nu se aplică regula generică „ultima modificare câștigă” la aprobări ori documente emise.

### 11.4 Ciclul documentului și al instruirii

Stările propuse sunt proiect, în revizuire, aprobat, în vigoare și retras. Aprobarea fixează conținutul, aprobatorul și perioada de aplicare. O schimbare creează o revizie nouă. Documentul retras rămâne accesibil pentru audit, cu stare clară, fără a fi prezentat operatorului drept instrucțiunea curentă.

Citirea, participarea la instruire și demonstrarea competenței sunt evenimente diferite. O confirmare de citire nu substituie evaluarea practică acolo unde procesul o cere. La o revizie relevantă se reatribuie instruirea conform regulii procesului. Schimbarea postului nu rescrie istoricul; se reevaluează doar eligibilitatea viitoare.

## 12 Legarea persoanelor de rezultate și manualul firmei

### 12.1 Exemplu de trasabilitate

Exemplu ipotetic: procedura de verificare dimensională revizia 3 este aprobată, iar operatorul este instruit și evaluat pentru ea. Pentru un lot se înregistrează măsurătorile, instrumentul și operația. O abatere generează o neconformitate; responsabilul stabilește acțiunea, iar după implementare se compară rezultatele pe o perioadă definită. Închiderea păstrează analiza folosită, decizia și persoana care a aprobat-o.

Exemplul nu descrie date reale ale firmei și nu presupune că operațiile de producție sunt deja modelate în repository. El definește relațiile care trebuie să existe pentru a răspunde la întrebarea „cine a lucrat, după ce instrucțiune, cu ce rezultat și ce s-a schimbat după corecție”.

| Informație | Sursa propusă | Control necesar |
|---|---|---|
| Persoană și stare activă | AMN/C_BPartner | Identitate unică per instanță și firmă |
| Cont și drepturi | AD_User și roluri | Separat de angajat |
| Post și departament | AMN și snapshot la eveniment | Istoric după transfer |
| Instrucțiune aplicată | QMS Revision | Revizie aprobată la data operației |
| Lot și operație | Modul operațional EVA de confirmat | Referință persistentă |
| Măsurătoare | QMS Inspection și Measurement | Unitate, instrument și corecții urmărite |
| Analiză statistică | Serviciu R | Date, parametri și versiuni reproductibile |
| Decizie și eficacitate | QMS Action și Approval | Responsabil și dovezi înainte de închidere |

### 12.2 Structura propusă a manualului

Manualul firmei trebuie să descrie domeniul sistemului, procesele și interacțiunile, responsabilitățile, controlul documentelor, competențele și instruirile, planificarea operațională, controlul furnizorilor, inspecțiile, echipamentele de măsurare, neconformitățile, acțiunile corective, auditul intern și analiza de management. Este o structură de lucru, nu o declarație de conformitate cu un standard ales.

Pentru fiecare proces se recomandă proprietar, intrări, ieșiri, riscuri relevante, criterii, indicatori, proceduri aplicabile și dovezi. Lista finală de cerințe se stabilește după confirmarea standardului și ediției urmărite, a domeniului de certificare și a proceselor firmei. În această analiză nu s-a furnizat textul standardelor și nu s-a efectuat o evaluare de conformitate clauză cu clauză.

## 13 Implementare etapizată și criterii de acceptanță

Prima etapă este un mediu de test cu versiunea reală EVA 13, inventarul HR și dicționarul tabelelor operaționale. A doua etapă implementează o procedură cu două revizii, aprobare, distribuție și instruire nominală. A treia leagă o inspecție de persoană, operație și lot. A patra adaugă neconformitatea, acțiunea și analiza R. Adoptarea extinsă urmează numai după probele de izolare, recuperare și audit.

| Test | Rezultat necesar pentru acceptare |
|---|---|
| Aceleași ID-uri în două cabinete | Nicio asociere între instanțe sau firme |
| Cont de acces nou pentru angajat | Angajatul rămâne corect în puntea AMN |
| Procedură modificată | Revizia veche și aprobarea ei rămân neschimbate |
| Instruire pe revizie veche | Nu validează automat cerința unei revizii noi |
| Transfer sau plecare | Istoricul se păstrează, atribuirea viitoare se actualizează |
| Cerere API pentru altă firmă | Acces refuzat și eveniment jurnalizat |
| Același mesaj trimis de trei ori | Un singur efect de business |
| Mesaj vechi după unul nou | Nu suprascrie starea mai nouă |
| Serviciu extern indisponibil | Eveniment păstrat și reluat controlat |
| Corecție de măsurătoare | Valoarea inițială și motivul rămân urmărite |
| Reexecutarea analizei R | Același rezultat la aceleași date și versiuni |
| Închiderea neconformității | Dovezi de implementare și eficacitate disponibile |
| Restaurare din backup | Relații, documente și hash-uri recuperate |
| Export pentru audit | Procedură, instruire, rezultat și decizie legate complet |

Pragurile de performanță se stabilesc după volumele reale: persoane, documente, revizii, măsurători pe zi, utilizatori simultani și dimensiunea atașamentelor. Nu estimăm cost, durată ori procent de integrare fără aceste date și fără prototip. Pilotul trebuie să măsoare și operarea de către utilizatori, nu doar succesul răspunsurilor API.

## 14 Comparația efortului și riscurilor

| Variantă | Reutilizare în EVA | Efort dominant | Risc principal |
|---|---|---|---|
| QMS nativ nou și R | Ridicată pentru HR, acces și documente | Construirea funcțiilor QMS | Subestimarea fluxurilor și testelor |
| OCA și conector | Redusă în interfață, posibilă în date | Două platforme și mapare | Identitate și revizii divergente |
| ERPNext și conector | Redusă în interfață | Evitarea duplicării ERP | Două surse de adevăr operațional |
| BookStack și QMS EVA | Medie pentru documente | Legarea aprobării și instruirii | Pagina curentă confundată cu revizia aplicată |
| DMS și QMS EVA | Potențial ridicată | Portare și validare pe 13 | Compatibilitate și dublarea registrului |

Evaluarea este calitativă, derivată din arhitectură, nu dintr-o ofertă de implementare. Recomandarea pentru conducere este aprobarea unui pilot nativ limitat și folosirea OCA drept reper de funcții. Dacă pilotul arată că dezvoltarea QMS internă este disproporționată, OCA devine prima alternativă externă de probat. R rămâne util în ambele variante.

## 15 Descărcare instalare și documentație

| Soluție | Descărcare și cod | Documentație de funcții | Integrare |
|---|---|---|---|
| OCA și Odoo Community | O01 O12 | O02 până la O11 | O13 O14 și I01 până la I04 |
| ERPNext și Frappe HR | E01 E07 E13 | E02 până la E10 | E11 E12 E14 |
| BookStack | B02 B03 B09 | B01 B08 B10 | B05 B06 B07 |
| Logilite DMS | D02 D03 D04 | D01 D03 D05 cu limitele indicate | I01 până la I06 și codul pluginului |
| R qcc SixSigma | R01 R02 R03 R04 R06 | Manualele din R01 R02 | R05 |

Adresele exacte și starea accesului sunt în registrul de surse și în fișierul CSV livrat. Pentru instalare se fixează versiuni sau commit-uri, se verifică dependențele și licențele și se salvează configurația de build. Nu se folosește automat ultima ramură a tuturor componentelor. Paginile publice se pot schimba după data consultării.

Anexele livrate includ registrul de surse cu URL complet, utilizare și verificare de acces. Referințele private necesită drepturi în repository și sunt fixate la commit-ul analizat. Nu sunt incluse chei de acces, date de angajați sau copii ale bazelor de date.

## 16 Glosar

| Termen | Sens în raport |
|---|---|
| QMS | Sistem de management al calității |
| CAPA | Acțiuni corective și preventive în terminologia aplicațiilor |
| SPC | Control statistic al procesului |
| AMN | Modelul HR AMERPSOFT utilizat în EVA |
| AD_Client | Firma sau clientul logic din iDempiere |
| AD_Org | Organizația din interiorul clientului |
| C_BPartner | Partenerul de business folosit și pentru angajat |
| AD_User | Utilizatorul sau contactul aplicației |
| PO | Obiect persistent și mecanismele de business iDempiere |
| SSO | Autentificare comună între aplicații |
| Idempotență | Repetarea cererii nu repetă efectul de business |
| Snapshot | Copie a datelor relevante la momentul evenimentului |

## 17 Registrul complet al surselor consultate

Registrul următor listează sursele folosite sau încercate, cu rolul lor. O sursă inaccesibilă nu este tratată ca dovadă a unei funcții. Verificarea HTTP certifică accesibilitatea la momentul verificării, nu corectitudinea unei aplicații. Documentația generală și paginile de instalare nu substituie testarea funcțiilor din versiunea aleasă.
