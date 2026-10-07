# 11 Etapizarea livrării resursele și limitele

## 11.1 Ordinea dezvoltării

Ordinea propusă reduce dependențele: inventar și probe API; captură instrumentată; modelul de date și recuperare; cele trei moduri de produs; metrologie și export; 6D și catalog; interfață ROS 2 în observație; calificare pe robot; extinderi. Percepția robotică poate fi explorată devreme pe date înregistrate, însă mișcarea robotului rămâne o poartă ulterioară.

O funcție nu trece din cercetare în ofertă comercială prin simpla finalizare a codului. Necesită profil de dispozitive, condiții de utilizare, dovadă de teste, erori cunoscute, UX și suport. Formatele avansate și antropometria nu sunt condiții obligatorii pentru lansarea modulelor de bază.

## 11.2 Resurse și estimare

Nu există suficiente date pentru un termen sau buget ferm. Modelul de estimare propus însumează efortul pe sarcină, durata așteptării pentru hardware/licențe, integrarea și rezervele pentru experimente. Managerul estimează intervale optimist/probabil/pesimist după probe, înregistrează ipotezele și le revede la fiecare poartă.

Inventarul minim de calificat include Mac și Xcode compatibil, telefoane pentru profilurile vizate, instrumente dimensionale cu incertitudine adecvată, montaj rigid, robot sau banc de test cu encodere/IMU și calculator, rețea controlabilă și destinații CAD/slicer. Nu se prescrie cumpărarea unui model înainte de probele de compatibilitate.

Costul de operare are componente locale, stocare, transfer, conversie licențiată și eventual inferență externă. Folosirea unui LLM pentru descrieri nu justifică trimiterea continuă a tuturor imaginilor. Bugetele de resurse sunt măsurate pe sarcina reală și legate de opțiunile produsului.

## 11.3 Reguli de schimbare a scopului

O funcție nouă primește cerință, utilizator, rezultat, dependențe, criteriu și test înainte de a intra în plan. Managerul documentează efectul asupra temperaturii, rețelei, persistenței și confidențialității. Autorii și auditorii afectati sunt notificați. Promisiunea „toate formatele” este înlocuită operațional cu o matrice versionată de subseturi testate.

Schimbarea unui prag după un eșec nu transformă testul eșuat în succes. Se păstrează rezultatul inițial, se justifică noul profil și se reexecută evaluarea pe date adecvate. O deviație aprobată produce o limită explicită de utilizare, nu o ștergere din istoricul auditului.

## 11.4 Criterii de abandon sau restrângere

Dacă dispozitivul nu susține o funcție, aplicația oferă un mod compatibil cu limite declarate. Dacă calibrarea sau referința nu poate susține toleranța, profilul metric este restrâns. Dacă un flux robotic nu poate păstra prospețimea cerută, rămâne mod de observare și cartografiere. Dacă identitatea a două exemplare nu poate fi distinsă, interfața arată ambiguitatea.

Aceste rezultate sunt utile și trebuie publicate în raportul intern. O echipă de calitate are dreptul să respingă o ipoteză tehnică. Cerința de audit complet nu obligă auditorul să ajungă la un verdict pozitiv indiferent de dovezi.

## 11.5 Limitări cunoscute ale documentului

Dosarul nu conține build iOS, pachet ROS executat, calibrări reale, studiu de utilizatori, comparație comercială exhaustivă nouă sau benchmark fizic. Documentația API se poate schimba; capabilitățile condiționate se reconfirmă în SDK și pe dispozitiv. Exemplul Xacro este un contract de montaj, nu un robot calibrat. Exemplele de mesaje și criteriile numerice sunt propuneri.

Acceptarea documentară este limitată la criteriile auditate și versiunea salvată. Rezultatele viitoare pot impune revizuiri. Fiecare revizuire semnificativă redeschide domeniile afectate și păstrează istoricul versiunii anterioare.
