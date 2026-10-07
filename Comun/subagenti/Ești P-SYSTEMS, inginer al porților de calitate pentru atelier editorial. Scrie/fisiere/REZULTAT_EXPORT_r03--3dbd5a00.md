# REZULTAT_EXPORT_r03 — TEST / propunere P-SYSTEMS

Data: 2026-09-24. Stare: remediere implementată numai în staging, propusă pentru retest independent. Nu se acordă scoruri, verdict de audit sau stare closed. Main integrează după încheierea și arhivarea r02, cu contract nou.

Livrarea este limitată la cele patru fișiere din `06_REGISTRU/r03_staging`: exportatorul, testele, README-ul și acest rezultat. Nu am modificat r02, registrele, contractele, rapoartele auditorilor, site-ul, exporturile anterioare, sursele originale sau nucleul gatekeeper/archive v2. Nu am deschis jurnalele reale enumerate de configurație și nu am copiat rawlogs în produse.

## Baza observabilă

Au fost citite integral cele trei fișiere live cerute: `06_REGISTRU/export_istoric_observabil.py`, `06_REGISTRU/test_export_istoric.py`, `06_REGISTRU/README_EXPORT.md`, plus configurația autorizată pentru verificarea compatibilității numelor/schema. Nu s-a rulat exportul pe configurația reală.

Inițial, sursa era `06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/history-r02-03/A-SYSTEMS.md`, mesajul observabil din 2026-09-24T02:32:14.432Z. În timpul implementării au devenit disponibile rapoartele finale; MD-ul și JSON-ul A-SYSTEMS r02 au fost citite integral, iar secțiunea HISTORY_PROCEDURE/HISTORY_RESULTS a jurnalului a fost citită pentru probele H01–H08. Identificatorii de mai jos provin din ambele rapoarte, nu sunt ID-uri provizorii inventate.

Surse citite, SHA-256 observat:

| Sursă în ROOT | SHA-256 |
| --- | --- |
| `05_AUDIT/SYS-001/A-SYSTEMS-r02.md` | `e26f641e1b0c8f100a538ca390436d85aa55188c9a69d6eeff77d76fc34fff60` |
| `05_AUDIT/SYS-001/A-SYSTEMS-r02.json` | `8fbbb12e49eae3c57d4304ef08f18a486c47680692cd60d2356a80c39bb120bd` |
| `05_AUDIT/SYS-001/A-SYSTEMS-r02-tests.txt` | `191f688cd66490d256c1c300bc2ca6b929bc50fce98cad9a9d3d6d5651d6d5d1` |

Aceste digesturi identifică lecturile, nu reprezintă validarea întregului audit. Nu s-a retestat în acest mandat nucleul v2 sau literatura.

## SYS-A-SYSTEMS-r02-F05

Cauză: codul r02 folosea `raw.rsplit(b"\n",1)[0]+b"\n"`. În absența oricărui LF, concatena un octet absent înainte de calculul lungimii/hashului prefixului. Auditorul demonstrează H03 (225 bytes fără LF declarați drept 226) și H04 (sursă goală declarată drept un byte); H01/H02 sunt controalele valide. Referințe: MD secțiunea F05, jurnal H01–H04, L929–L980.

Patch: `complete_prefix`, în exportatorul r03:L29, taie numai `raw[:raw.rfind(b"\n") + 1]`. Nicio linie completă înseamnă zero bytes și zero înregistrări; CRLF rămâne intact, fără LF inventat. Se exclude numai coada după ultimul LF. JSONL-ul derivat păstrează formatul anterior și are hash separat.

Test executat: toate cele 12 metode `PrefixRegressionTests`, inclusiv gol, JSON complet fără LF, prima linie parțială, LF/CRLF, CR fără LF, coadă UTF-8 incompletă, linii goale și mai multe înregistrări. Controalele end-to-end verifică lungime în limita sursei, SHA-256 al prefixului real, hashurile ieșirilor și sursa nemodificată. O linie completă JSON malformată refuză fără captură. Toate au reușit ca teste tehnice; închiderea findingului aparține auditorului.

## SYS-A-SYSTEMS-r02-F06

Cauză: `role` era concatenat direct în numele fișierelor, iar destinația era creată fără verificarea traseului fizic. Crearea exclusivă proteja doar împotriva overwrite, nu împotriva unei scrieri noi în exterior. Auditorul demonstrează H05 traversare în afara rundei, H06 în afara ROOT și H07 redirecționarea părintelui prin symlink; H01 este controlul normal. Referințe: MD secțiunea F06, jurnal L981–L1019.

Patch: `safe_component`, `validate_output_names` și `prepare_sources` validează rolurile/rundele și întregul set de nume, inclusiv indexul și sidecar-ul. Sunt refuzate rezervatele Windows, rolul index, duplicatele fără diferențiere de majuscule, ID-urile duplicate și aliasurile fizice de sursă. `checked_root`, `plain_directory`, `checked_tree` și `destination` verifică rădăcina/strămoșii/părinții lexical, înainte de resolve, respingând symlink/reparse/junction. Directoarele sunt create pe rând. `write_new` reverifică părinții și ocuparea numelui înainte de crearea exclusivă. Indexul și sidecar-ul au aceeași protecție ca celelalte ieșiri.

Test executat: toate cele 23 metode `DestinationRegressionTests`. Acoperă H05–H07, căi absolute/UNC/ADS/traversare, aliasuri și duplicate, symlink suspendat, alias intern, junction Windows pe destinație sau strămoșul ROOT, coliziuni index/index.sha256 și variante de majuscule, hard link/symlink pe ieșire, părinți redirecționați după preflight și coliziune injectată înaintea indexului. Sunt verificate țintele sintetice nemodificate și lipsa rezultatului de succes la refuz; o rundă existentă își păstrează exact bytes. Nu s-a folosit niciun fișier real exterior drept țintă.

## Rezultat efectiv al suitei

Rulare din `06_REGISTRU/r03_staging`, Python 3.12.10, Windows:

```text
python -B -m unittest -v test_export_istoric.py
Ran 65 tests in 1.545s
OK
exit_code: 0
failures: 0; errors: 0; skipped: 0
```

Componență: 17 teste existente păstrate + 12 prefix + 23 destinație + 13 compatibilitate = 65 metode, nu număr de subcazuri. Probele symlink/hard link/junction au rulat efectiv, fără skip. Cele 13 controale de compatibilitate includ configurația sintetică de nouă roluri, filtrul H08, apeluri/rezultate observabile, redacții, pragul temporal, configurație alternativă și CLI cu root sintetic/default injectat după integrare.

Verificări suplimentare read-only: numele celor 17 teste originale coincid; blocul `clean_value`/`redact`/`select` coincide textual cu r02; cele nouă roluri/nume de ieșire din configurația reală sunt acceptate de verificările de nume, fără citirea jurnalelor. Copia de staging are ROOT implicit `None`, deci cere `--root`; după integrare, locația `ROOT/06_REGISTRU` furnizează rădăcina implicită originală.

Fixture-urile, inclusiv directoarele OUTSIDE_ROOT, sunt exclusiv în TemporaryDirectory. Cleanup validează căile/țintele înainte de eliminarea linkurilor și directorului temporar. Pe un OS fără suport, testele corespunzătoare ar raporta skip explicit; rularea raportată nu are omisiuni.

## Limite și predare

Nu se pretinde protecție atomică împotriva unui administrator/proces concurent care înlocuiește părinții exact între verificare și creare. Arborele destinației trebuie menținut stabil și sub control exclusiv pe durata exportului. Nu există WORM, timestamp certificat, semnătură sau detector universal de secrete. Filtrul existent nu a fost extins/reproiectat. Un eșec I/O poate lăsa o rundă parțială nereutilizabilă; aceasta nu primește JSON de succes. Prefixele corespund lecturii, nu garantează că sursa nu este modificată ulterior.

Comparația read-only început/final pe zece căi urmărite găsește nouă neschimbate, inclusiv cele trei fișiere live ale exportatorului, configurația sa, gatekeeper/archive și exportul observabil citit. `06_REGISTRU/deliverables.json` s-a schimbat în cursul lucrului din afara intervenției mele: de la `850cdc6b3c81d32558d836fc574a1318d354b32126e93b1eabc776d4264ee72b` la `498c82c2f1a29aecab7e530aa2f07d42f023fee55fa4933d859147bce6d20e6c`. Nu l-am scris și nu l-am restaurat; nu atribui cauza schimbării. Nu afirm neschimbarea globală a tuturor fișierelor atelierului.

Hashuri ale celor trei fișiere de implementare/documentare livrate:

| Fișier din r03_staging | SHA-256 |
| --- | --- |
| `export_istoric_observabil.py` | `662fd74afabe6041f6ce73a757fe7415498022bef77919340922a147906ff23e` |
| `test_export_istoric.py` | `7fc50aa7f99378ad5b786677cb3f391752892b18c5d9f27d22e2c3744c5aa9b1` |
| `README_EXPORT.md` | `9b1c3483d849414430ca88e229dd39a30ac50d85131b56e649c15a59e1570cf2` |

Digestul acestui rezultat este comunicat separat la predare, nu inserat circular în propriul conținut. P-SYSTEMS propune remedierea; auditorul decide închiderea F05/F06. Nicio integrare sau actualizare de contract nu a fost executată aici.
