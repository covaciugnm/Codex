# Calibrare suplimentară personaje, fapte, traduceri și ediții — TEST rom001-b-r01
P-MANAGER,24.09.2026,Europe/Bucharest. Set sintetic deschis, nu audit de roman, nu producție de etapă viitoare. Nu modifică seturile deja înghețate.
Regulă identică protocolului r02: fiecare rol rezolvă C01–C09 din SET_TEST_r02.md și cele2cazuri proprii de aici, 11/11, cu motive și localizări; QA verifică nominal înainte de audit productiv. Cheia vizibilă măsoară aplicarea regulilor, nu test orb, competență exhaustivă sau calificare umană.
## A-CHARACTER-S01
Stimul TEST: Nora refuză o înregistrare publică dintr-un motiv central stabilit. Fără eveniment, informație, alegere sau schimbare motivată, în scena următoare ea face exact opusul; nota autorului justifică numai prin „altfel nu ajungem la climax”.
Cheie: RETURN. Schimbarea este impusă mecanic de intrigă, fără motivație sau cost cauzal; nu inventa o explicație absentă.
## A-CHARACTER-S02
Stimul TEST: Nora își schimbă decizia după ce află o informație verificată, își recunoaște conflictul interior și acceptă pe pagină un cost clar. Un raport o respinge automat numai fiindcă decizia diferă de prima.
Cheie: NU_E_DEFECT_IN_SINE. Schimbarea motivată poate reprezenta evoluție credibilă; nu orice schimbare este contradicție. Celelalte criterii se evaluează separat.
## A-FACT-S01
Stimul TEST: Sursa fictivă primară S1 datată în exercițiu spune „podul s-a deschis în1900”. Narațiunea îl prezintă drept același pod deschis publicului în1890, fără istorie alternativă ori altă explicație. Raportul pretinde verificare exactă înS1.
Cheie: RETURN. Sursa stipulată nu susține data1890 și comparația o contrazice; cere corectare/documentare, nu aviz inventat. Nu este necesară cercetare web pentru acest obiect fictiv de test.
## A-FACT-S02
Stimul TEST: În ficțiune, un personaj crede greșit că podul este deschis. Scena îl arată ajungând la barieră, aflând informația corectă și suportând consecința. Narațiunea nu validează credința inițială. Raportul numește automat eroare factuală a autorului orice credință greșită a personajului.
Cheie: NU_E_DEFECT_IN_SINE. Se disting perspectiva personajului și faptele asumate de text. Un personaj poate greși în mod cauzal; celelalte verificări rămân.
## A-RO-S01
Stimul TEST: Sursa EN spune “She borrowed the book from the municipal public library.” Glosarul confirmă o bibliotecă publică de împrumut. ȚintaRO: „A împrumutat cartea de la librăria publică municipală.” Raportul declară sens și terminologie corecte.
Cheie: RETURN. Library a fost confundat cu librărie în contextul explicit al bibliotecii. Nu inventa servicii de împrumut ale unei librării pentru a salva ținta.
## A-RO-S02
Stimul TEST: Ghidul cere diacritice românești cu virgulă dedesubt. Fișierul final folosește sistematic Ş(U+015E) și ţ(U+0163), nu Ș(U+0218) și ț(U+021B); raportul declară convenție respectată.
Cheie: RETURN. Convenția Unicode cerută nu este respectată; citibilitatea aproximativă nu justifică bifa, corecția și retestul sunt necesare.
## A-DE-S01
Stimul TEST: EN: “I hadn't told her yet.” DE: “Ich hatte es ihr schon gesagt.” Nu există adaptare autorizată care să inverseze evenimentul.
Cheie: RETURN. Se inversează negația și stadiul acțiunii („nu încă” versus „deja”); gramatica fluentă nu compensează sensul.
## A-DE-S02
Stimul TEST: Ghidul DE păstrează numele francez Camille Duret. Traducerea îl păstrează consecvent, idiomul german din jur este corect în stimul. Raportul cere obligatoriu germanizarea numelui în Kamilla Dürer.
Cheie: NU_E_DEFECT_IN_SINE. Păstrarea numelui respectă ghidul; nu inventa obligația de germanizare. Restul limbii și integralității cer audit propriu.
## A-TRANSLATION-S01
Stimul TEST: EN/P12 spune că Nora îl avertizează pe Paul și că trenul este la18:40. RO/P12 îl face pe Paul să o avertizeze pe Nora și mută trenul la08:40. Numărul paragrafelor și al cuvintelor este apropiat.
Cheie: RETURN. Sunt inversate agentul acțiunii și ora; completitudinea numerică nu demonstrează fidelitate.
## A-TRANSLATION-S02
Stimul TEST: Traducerea integrală și alinierea sunt aprobate pentru EN-v1. Masterul curent EN-v2 schimbă finalul; predarea actuală încă folosește ținta dupăv1, fără evaluarea impactului.
Cheie: RETURN. Aprobarea vechii relații sursă–țintă nu se transferă asupra noului master; trebuie verificat și remediat impactul, păstrând istoricul.
## A-PRODUCTION-S01
Stimul TEST: Manifestul enumeră un PDF, dar fișierul nu se poate deschide și conține0octeți. Raportul spune „toateformateletestate” numai pentru că numele fișierului există.
Cheie: RETURN. Existența căii nu probează deschiderea, conținutul sau integralitatea; nu se declară test neefectuat.
## A-PRODUCTION-S02
Stimul TEST: Pachetul are3fișiere deschizibile, etichetateEN/RO/DE. FișierulRO conține textul german, iar cuprinsulDE trimite la capitole dinEN. Hashurile calculează corect acești octeți greșiți.
Cheie: RETURN. Integritatea byte-cu-byte nu certifică ediția/limba/navigarea corectă. Etichetele și conținutul trebuie confruntate.
## Livrare
06_REGISTRU/CALIBRARE/ROM-001/<ROL>-b-r01.json cu agent_id,role,set_version="rom001-b-r01",responses=[{id,verdict,reason,evidence}],passed_count,total_count,qualified,completed_at(cu fusorar). evidence localizează setul r02 pentru C01–C09 și acest set pentru rol. Nimeni nu completează în numele altui agent; qualified propriu este supus verificării QA. Fără scoruri productive, traduceri sau proză de roman.

