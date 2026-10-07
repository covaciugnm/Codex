# Criteriile canonice de acceptare

Acest document rezolvă diferențele dintre propunerile specialiștilor și are prioritate pentru praguri, eșantioane și etapizarea produsului. Toate criteriile aplicației sunt **propuse și nevalidate**. Auditul documentelor nu echivalează cu trecerea lor.

## Praguri dimensionale

L este lungimea de referință în milimetri. P95 reprezintă percentila 95 a erorii absolute, calculată separat pentru fiecare clasă declarată de material, dispozitiv și condiții. Eșecurile de captură se raportează separat cu numitorul tuturor încercărilor. Atingerea pragului pe un lot nu constituie garanție pentru toate capturile viitoare.

| Profil | Domeniu de acceptare inițial | Țintă propusă | Interpretare |
|---|---|---|---|
| Obiecte cotate | Lungimi 0,1–1 m, obiecte rigide, mate, suficient texturate, referință independentă | P95 ≤ max(5 mm, 0,01 × L) | Profil orientativ; piese cu toleranțe mai stricte necesită altă calificare |
| Măsurare live | Lungimi 0,2–5 m, suprafețe observabile și tracking stabil | P95 ≤ max(20 mm, 0,01 × L) | Nu se afișează acest prag ca incertitudine individuală |
| Camere | Lungimi 1–8 m, repere accesibile, geometrie validată | P95 ≤ max(30 mm, 0,01 × L) | Unirea camerelor și etajele se evaluează separat |
| Conversie numerică export și reimport | Fixture digital cu geometrie exact cunoscută, fiecare format/subset anunțat | Eroare maximă ≤ max(0,01 mm, 10⁻⁵ × L) | Măsoară conversia datelor, nu eroarea capturii fizice |

Testele în afara domeniilor sunt exploratorii. Suprafețele transparente, lucioase sau mobile nu sunt implicit acceptate în profilul de bază. Pentru LAS/LAZ se alege o cuantizare compatibilă cu testul; dacă subsetul nu poate respecta pragul, nu este declarat conform fără un profil distinct și o decizie versionată. Nu se ascunde eroarea exportului prin aliniere cu scară liberă.

Pentru acceptarea dimensională înainte de lansare, limita superioară a intervalului de încredere de 95% estimat pentru P95 trebuie să fie cel mult pragul profilului. Dacă eșantionul nu permite o estimare suficient de stabilă sau intervalul depășește pragul, rezultatul este insuficient/inconcludent ori neconform, după date; nu este trecut. Metoda statistică și resamplingul pe obiect/cameră se fixează înainte de evaluare.

## Eșantioane și faze

| Domeniu | Pilot sau probă | Acceptare | Stres ori cercetare extinsă |
|---|---|---|---|
| UX | 5 persoane formative; 15 interviuri separate | 20 participanți diferiți; alegerea modului 18/20 în ≤10 s; prima captură și export 16/20 fără ajutor; interpretarea stărilor 18/20 | 5 sesiuni asistive suplimentare și extindere după pilot |
| Confidențialitate live | 10 sesiuni instrumentate | 50 sesiuni fără persistență/upload implicit; 20 anulări +20 salvări explicite de foto | 100 sesiuni suplimentare pe combinații OS/dispozitiv |
| Întreruperi | 10 probe pe operații diferite | 50 întreruperi distribuite captură/salvare/procesare/export | 1000 întreruperi automatizate înainte de extinderea comercială |
| Procesare joburi | 20 scenarii idempotente | Parte din cele 50 întreruperi; fără rezultate dublate | Lotul de 1000 include joburi și migrarea datelor |
| Camere | Fixture sintetic 12 camere/2 niveluri pentru modelul de date | 10 proiecte reale cu 3–8 camere pentru captură și aliniere pe nivel | Etaje și clădiri complexe în P2, cu validare proprie |
| Metrologie | Pilot pentru variabilitate și ajustarea eșantionului | Planul CAD de obiecte/camere/live, stratificat | Puterea statistică și extinderea lotului se stabilesc după pilot |

Loturile funcționale, UX și metrologice au obiective diferite; nu se adună ca și cum ar fi observații independente. Numărul mai mare într-un capitol reprezintă stres sau cercetare extinsă doar dacă este etichetat explicit.

## Recuperare și date temporare

Datele deja confirmate ca salvate trebuie recuperate fără pierderi. Ținta de cel mult 5 secunde privește numai metadatele și fluxurile persistente controlate direct de aplicație între checkpointuri. Cadrele și stările interne ale sesiunilor opace RoomPlan/Object Capture au recuperare best effort: se păstrează ce API permite, se reia etapa permisă sau se solicită recaptură. Nu se garantează exact cadrul pierdut.

Pierderea de cel mult 5 secunde se măsoară ca diferența dintre timestampul ultimei observații serializabile eligibile înaintea întreruperii și timestampul ultimei observații eligibile recuperate, pentru fluxurile controlate de aplicație. Se folosește același ceas monoton al sesiunii. Absența pierderii datelor deja confirmate este verificată separat prin identificatori și hashuri. O operație încă neconfirmată nu poate fi reclasificată drept confirmată după eșec.

Modul live nu are recuperare după terminarea procesului, deoarece nu păstrează mediul. Recuperarea documentației și a proiectelor persistente are un contract diferit de acest mod.

## Etapizarea canonică a formatelor și funcțiilor

| Etapă | Formate sau funcții țintă | Poarta de acceptare |
|---|---|---|
| P0 | 3MF și STL pentru obiecte; PLY pentru nor; USDZ pentru previzualizare; DXF 2D cu cote implementate explicit și JSON lateral pentru metadate | Fixture numeric, import în destinație, informații pierdute declarate; niciun adaptor nu este implementat încă |
| P1 | OBJ, GLB/glTF, E57, LAS/LAZ, XYZ/PTS, PCD; DWG prin SDK/convertor licențiat | Probe pe subset, format și versiune; licență și platformă verificate |
| P2 | IFC semantic, STEP/BRep, AMF, VRML/3DS după nevoie; etaje reale, exterior și geometrii complexe | Proiect de cercetare și validare separată |

JSON nu este format universal CAD, ci manifest și metadate. USD/USDZ nu înlocuiesc automat un plan cotat. G-code rămâne produsul unui slicer configurat pentru mașină și material. Menționarea unui format în P0 stabilește obiectivul dezvoltării, nu suportul actual al aplicației inexistente.

P0/P1/P2 din acest tabel sunt priorități de produs. P0/P1/P2/P3 din audit sunt severități ale defectelor și nu trebuie amestecate. Modelul de date poate conține niveluri din P0, însă capturarea și unirea robustă între niveluri reale rămân în P2.
