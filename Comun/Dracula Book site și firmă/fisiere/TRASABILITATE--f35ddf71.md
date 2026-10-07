# Matrice de trasabilitate a mandatului — r03

Fiecare cerință este legată de livrabil, test, auditor și dovadă. Acoperirea în procedură nu înseamnă rezultat editorial deja obținut. Starea actuală este în STATUS și în validarea manifestului. R01–R16 sunt ID-uri de cerință, T01–T16 sunt proceduri de acceptare; nu sunt note sau teste pretins executate.

| ID | Cerință / livrabil | Test și rezultat necesar | Auditor | Dovadă și stare |
|---|---|---|---|---|
| R01 | U01 · Roman EN ≥50.000; G09/G11/G16 | T01: prag 49.999 respins/50.000 acceptat; citire integrală, numai proză | A-EN + A-GENRE; G16 A-PRODUCTION + A-GOVERNANCE | T01: teste existente; roman VIITOR, 0 cuvinte acceptate |
| R02 | U01 · Continuare în serie începută; SEL/G01 | T02: comparație 3 opțiuni și surse; G01 lectură integrală, zero contradicții | A-CANON + A-GOVERNANCE | SEL#recomandare preliminar; G01 VIITOR, nu este substituit |
| R03 | U01/U03 · Repere de succes din orice mediu; RES/G02 | T03: pentru fiecare reper sursă primară, tip de succes și limite; fără cote pe medii | A-SOURCES + A-GOVERNANCE la RES; A-GENRE la G02 | DE-001#fișa; RES surse individuale; reaudit necesar |
| R04 | U01 · Minimum 2 opere-sursă; originalitate G03/G10 | T04: mecanisme abstracte distincte; matrice pe 10 dimensiuni; fără scene/replici copiate | A-ORIGINALITY + A-GENRE; G10 A-FACT | MANUAL §6; ROADMAP G03/G10. Premisa romanului VIITOR |
| R05 | U03 · Contează modul de prezentare; fără univers comun impus | T05: fiecare mecanism are acțiune + relatare; verificare voce/POV/ritm; canon per serie/WorkID | A-SOURCES; A-CANON; A-EN potrivit etapei | DE-001#regula; RES banca 18 mecanisme; r01 RETURN păstrat |
| R06 | U01 · Pași compleți și reutilizabili; SYS/G00–G17 | T06: 18 etape, fiecare cu intrări, obiective, activități, rezultate, livrabile și ieșire | A-GOVERNANCE + A-SYSTEMS | ROADMAP G00–G17; 06_REGISTRU/roadmap.json |
| R07 | U01 · Echipă și fișe; 33 roluri | T07: fiecare rol are misiune, intrări, KPI, livrabile, limite; separă rolul de execuție | A-GOVERNANCE + A-SYSTEMS | 01_ECHIPA/00_ECHIPA_SI_RESPONSABILITATI.md și fișele individuale |
| R08 | U01 · Audit separat pentru fiecare livrabil/capitol/lot | T08: două ID-uri diferite de producători, roluri acoperite, fișiere și contract exact | A-GOVERNANCE + A-SYSTEMS; QA meta | MANUAL §3/8; T08 teste independență; G07 și traducerile VIITOR |
| R09 | U01 · Fiecare criteriu strict >9,50 | T09: 950 respins deși media mare; 951 acceptat numeric; niciun defect deschis | A-SYSTEMS + A-GOVERNANCE | policy.json; T09 teste prag + finding; RUBRICI |
| R10 | U01 · Întoarcere și îmbunătățire | T10: finding→cauză→măsură→versiune nouă→retest; fără editarea auditului vechi | Auditorul specialist + A-GOVERNANCE; QA verifică închiderea | 05_AUDIT/*/*-r01; 06_REGISTRU/MASURI; închidere numai prin retest independent al versiunii curente |
| R11 | U01 · Audit al arhitecturii și realizării | T11: audit de proces și tehnic G00; structural G05/G08, voce G06/G09, integral G11 | Perechile exacte din ROADMAP; QA separat | SYS auditurile r01/r02 și reevaluarea r03; G01–G17 VIITOR |
| R12 | U01 · Auditul auditorilor și calibrare | T12: 11/11 cazuri per ID; 6 checks meta, probe și al treilea ID; fără regresie infinită | A-QAMANAGER; A-GOVERNANCE verifică sistemul | CAL#regula; 01_ECHIPA/A-QAMANAGER.md; T12 teste meta |
| R13 | U02 · Tot procesul observabil arhivat, inclusiv RETURN | T13: index/hashes; mandate, versiuni, rapoarte, planuri și retest; recuperare; refuz overwrite | A-GOVERNANCE + A-SYSTEMS | PROTOCOL#flux; ISTORIC#reconciliere; 08_ARHIVA index per rundă; lacune declarate |
| R14 | U01 · Numai local; transfer doar finalizat | T14: zero scrieri în surse/site; G16 3 ediții acceptate; G17 aprobare pachet exact | A-PRODUCTION + A-GOVERNANCE; QA | MANUAL §13; 09_ELIBERARE_LOCALA/README.md; transfer VIITOR |
| R15 | U01 · Explicarea progresului | T15: status separă depus/acceptat, scoruri reale, defecte și cuvinte EN; jurnal decizii | A-GOVERNANCE; QA verifică raportarea | 00_CONDUCERE/STATUS.md și JURNAL_DECIZII.md; nu aprobare prin etichetă |
| R16 | Clarificări · 100 titluri distincte; EN cu RO și DE | T16: WorkID unic; traduceri/ediții nu sunt titluri noi; EN înghețat înainte de traduceri integrale | A-RO/A-DE + A-TRANSLATION; A-GOVERNANCE | MANUAL §1/12; G12–G16 VIITOR. Strategia de 100 titluri este document separat |

## Localizarea exactă a dovezilor
MANUAL = 00_CONDUCERE/MANUAL_ATELIER.md, secțiunea indicată. ROADMAP = 00_CONDUCERE/ROADMAP.md, titlul Gxx. DE-001 = 00_CONDUCERE/DECIZIE_EDITORIALA_001_SURSE.md. PROTOCOL = 00_CONDUCERE/PROTOCOL_ARHIVARE.md. CAL = 06_REGISTRU/CALIBRARE/SET_TEST_r02.md. ISTORIC = 06_REGISTRU/ISTORIC/RECONCILIERE_ISTORIC_r02.md. SEL = 02_DOCUMENTARE/CANON_EXISTENT.md; recomandarea din secțiunea de decizie. RES = REPERE_SI_MECANISME.md, BANCA_MECANISME_EXTINSA.md și APLICATII_WORKID_REALE.md din 02_DOCUMENTARE. Aceste aliasuri sunt pentru lectură; rapoartele JSON citează căile relative reale, nu aliasuri.

## Proceduri verificabile și limite
T01: 04_INSTRUMENTE/test_gatekeeper.py, test_49999_prose_words_rejected și test_50000_prose_words_pass; numărul se combină cu lectura editorială integrală, încă VIITOARE pentru roman.
T08: același fișier, test_self_audit_is_rejected, test_duplicate_auditor_is_rejected și test_two_people_in_one_role_do_not_cover_two_roles. T09: test_950_rejected_even_when_weighted_average_exceeds_threshold, test_951_passes_and_result_has_exact_public_fields și test_open_finding_of_any_severity_is_rejected.
T12: test_meta_missing_when_required_is_rejected, test_self_meta_by_ordinary_auditor_is_rejected și test_meta_stale_report_hash_is_rejected; calibrarea editorială are răspunsuri nominale în CALIBRARE, nu se deduce din testele Python.
T13: 04_INSTRUMENTE/test_archive_round.py, test_existing_round_is_never_overwritten, test_second_round_keeps_rejected_first_version și test_result_is_preserved_exactly_including_rejection; verificare suplimentară a conservării HASH/RETURN și surselor în retestul tehnic r02.
T02–T07/T10–T11/T14–T16 sunt verificări documentare/editoriale executate de rolurile din tabel, nu teste automate inventate. Pentru fiecare produs viitor se păstrează raportul cu localizări pe versiunea concretă înainte de a schimba starea în ACCEPTAT.

## Controlul acoperirii
U01/U02/U03 sunt transcrise în 06_REGISTRU/ISTORIC/INSTRUCTIUNI_BENEFICIAR.md. Toate cerințele de atelier ale acestora sunt acoperite de R01–R15; clarificările de portofoliu/limbi de R16. Arhivarea r01 a avut lacune identificate, remediate sau declarate în reconciliere; nu este prezentată retroactiv drept captură perfectă. G01–G17 sunt neîncepute la configurare. Niciun scor de sistem nu certifică un roman de 50.000 de cuvinte sau ținta de 100 titluri.
