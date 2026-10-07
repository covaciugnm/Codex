# 10 Date securitate operare și recuperare

## 10.1 Limitele de încredere

Arhitectura propusă separă telefonul, calculatorul robotului, stația de dezvoltare și serviciile opționale. Telefonul furnizează observații autentificate; robotul decide dacă sunt suficient de proaspete și consistente pentru utilizare. Un server de documentare sau catalog nu primește implicit controlul articulațiilor.

Fișierele OBJ, texturile, norii de puncte și pachetele de proiect sunt intrări neîncrezătoare. Importatorul verifică dimensiunea, numărul de elemente, valorile finite, indexurile, compresia și căile relative. Un fișier cu milioane de elemente sau o arhivă cu expansiune enormă nu trebuie să blocheze aplicația sau să scrie în afara proiectului. Testele includ inputuri trunchiate, NaN, indexuri invalide și texturi cu căi externe.

## 10.2 Modelul de date

Entitățile principale sunt Project, CaptureSession, Observation, Calibration, CoordinateFrame, MapRevision, MeshChunk, ObjectInstance, ObjectModel, Measurement, Annotation, ProcessingJob, ExportArtifact și AuditEvent. Un Observation este imutabil; o interpretare nouă produce un rezultat nou cu legătura către observație. O MapRevision nu schimbă retroactiv sensul coordonatelor unui rezultat vechi.

ObjectInstance reprezintă exemplarul fizic; ObjectModel reprezintă geometria comună sau de referință. Două scaune identice pot folosi același model și ID-uri de instanță distincte. Când identificarea exemplarului este ambiguă, păstrăm ipoteze sau status ambiguu. Nu inventăm identitate stabilă pe baza categoriei.

Stocarea locală trebuie să susțină tranzacții pentru metadate, fișiere voluminoase adresate prin hash și migrări versionate. Alegerea concretă a bibliotecii iOS se face în proba de fezabilitate. PostgreSQL este potrivit pentru catalogul de server propus; nu este o dependență obligatorie a unei măsurări offline. Site-ul existent în Docker/PostgreSQL rămâne separat de serviciul robotic.

## 10.3 Consistența operațiilor

O salvare propusă parcurge prepared → data_written → metadata_committed → acknowledged. Confirmarea către utilizator se emite numai după ce datele și legăturile necesare sunt durabile conform mecanismului platformei. La restart, fișierele temporare și tranzacțiile incomplete sunt reconciliate. Joburile folosesc chei de idempotență formate din input_hash, algorithm_version și parametri normalizați.

Anularea este o stare proprie. Dacă un calcul GPU continuă după anulare, rezultatul său nu trebuie publicat într-un proiect nou ori într-o hartă cu altă epocă. Un rezultat final valid se atașează numai după verificarea versiunii de intrare. Politica pentru conflicte nu este „ultima scriere câștigă” când acea scriere poate fi o observație mai veche.

## 10.4 Confidențialitate

Planul separă modurile temporare de proiectele persistente și de exportul explicit. Camerele locuințelor, fețele și documentele vizibile pot dezvălui date personale. Minimizarea, scopul și durata păstrării sunt cerințe de proiect; baza legală și obligațiile concrete se evaluează înainte de utilizarea cu persoane reale. GDPR este o sursă normativă relevantă în UE, dar aplicabilitatea articolelor și eventualele excepții necesită analiză juridică pentru implementarea efectivă. [Regulamentul UE 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng)

Propunem criptarea datelor persistente prin mecanismele platformei, transport autentificat și criptat, acces după rol și revocarea perechii telefon–robot. Nu păstrăm secrete sau imagini în loguri obișnuite. Telemetria implicită conține coduri de evenimente și timpi, fără geometria locuinței. Colectarea unui set de cercetare se face printr-un flux explicit, separat de măsurarea live.

Ștergerea unui proiect trebuie să acopere metadate, fișiere, miniaturi, exporturi administrate și copii sincronizate în limitele politicii declarate. Copiile de siguranță au retenție și proces de expirare documentate. Nu se promite ștergerea din exporturile pe care utilizatorul le-a transferat deja unei alte organizații.

## 10.5 Amenințări și controale propuse

| Amenințare | Efect | Control | Dovadă cerută |
|---|---|---|---|
| Dispozitiv neautorizat trimite o hartă | Geometrie falsă folosită de consumator | Pairing, identitate verificată, autorizare | Test cu un client neînrolat respins |
| Retrimiterea unei observații vechi | Obiecte aparent actuale | Secvență, epocă, timp și expirare | Replay capturat respins și jurnalizat |
| Pachet foarte mare sau corupt | Blocarea procesării | Limite, parser verificat, cote de resurse | Corpus adversarial și memorie stabilă |
| Schimbarea modelului de referință | Poziții raportate în alt reper | Hash model și versiune în rezultat | Model schimbat fără actualizare detectat |
| Furtul unui export | Expunerea mediului | Alegere explicită, acces și retenție | Audit de permisiuni și fluxuri |
| Pierderea rețelei | Percepție învechită | Watchdog și stări de degradare | Test de întrerupere cu cronologie |

## 10.6 Funcționarea offline și actualizările

Captura și inspecția de bază trebuie proiectate pentru funcționare locală. Funcțiile care cer procesare externă sunt identificate înainte de captură. Coada de sincronizare are limite și prezintă utilizatorului ce date vor fi transferate. Robotul nu depinde de disponibilitatea internetului pentru bucla locală de control.

Actualizările de model ML sau algoritm pot modifica dimensiunile și identitățile. Fiecare versiune primește manifest, teste de regresie și posibilitate de revenire. Reprocesarea unui proiect vechi produce o versiune nouă comparabilă, cu raport de diferențe. Dacă o migrare eșuează, copia originală rămâne recuperabilă.

## 10.7 Observabilitate și operare

Metricile operaționale includ age_at_use, rate de cadre, cozi, joburi abandonate, offsetul ceasurilor, erori de transformare, driftul estimat, starea termică, reconectări și spațiul liber. Un dashboard poate evidenția degradarea, însă logurile rămân sursa pentru audit. Se păstrează versiunea pragului de alertare folosită în fiecare sesiune.

Pentru modul robotic, heartbeatul arată că procesul este viu; nu dovedește că senzorul produce observații utile. Prospețimea datelor și calitatea trackingului sunt semnale separate. O hartă primită fără actualizări recente poate rămâne disponibilă pentru consultare, dar nu autorizează o manevră nouă.

## 10.8 Continuitatea muncii de dezvoltare

Reluarea proiectului este diferită de reluarea percepției. Dezvoltatorii reiau din fișiere, decizii și teste salvate. Telefonul reia numai starea pe care API-urile și contractul de persistență o permit. Nu există o garanție realistă că memoria internă a tuturor frameworkurilor sau raționamentul nescris al unui agent se recuperează exact.

Protocolul de lucru consemnează înainte de execuție sarcina și intrările, apoi rezultatul, verificarea, auditul și checkpointul. Evenimentele sunt append-only; o corecție adaugă un eveniment nou. Un hashchain local detectează unele modificări accidentale raportate la o copie de încredere, dar nu este sigiliu antifraudă: un actor cu acces complet îl poate recalcula. Pentru utilizare comercială propunem backup independent și jurnal de server cu acces separat.
