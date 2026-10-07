# SYS-001 — rezultate tehnice r02 — TEST / staging

Producător: P-SYSTEMS. Data de lucru: 2026-09-24. Momentul verificării finale a hash-urilor și inventarului: **2026-09-24 01:52:02 UTC**, citit de la ceasul instrumentului. Această oră nu este un timestamp certificat extern și nu pretinde ora exactă de început a fiecărui test.

Stare: **TEST — implementare propusă în staging, pentru retest independent**. Nu este raport de audit, nu conține scoruri editoriale și nu închide nicio constatare. Finding-urile A-SYSTEMS r01 își păstrează ID-urile și rămân de evaluat/închis de auditorul competent. Producătorul raportează implementarea și rezultatele testelor sale, nu își acordă aprobare.

## 1. Mandat și fișiere produse

Implementarea a fost autorizată exclusiv în `ROOT/04_INSTRUMENTE/r02_staging`, cu acest raport tehnic în `ROOT/06_REGISTRU/MASURI`. ROOT este `D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000`.

Au fost create prin `apply_patch` cele cinci fișiere din staging:

- `04_INSTRUMENTE/r02_staging/gatekeeper.py`
- `04_INSTRUMENTE/r02_staging/archive_round.py`
- `04_INSTRUMENTE/r02_staging/test_gatekeeper.py`
- `04_INSTRUMENTE/r02_staging/test_archive_round.py`
- `04_INSTRUMENTE/r02_staging/README.md`

Nu s-a integrat codul în cele cinci fișiere curente din `04_INSTRUMENTE`. Nu s-au scris registre reale, rapoarte de audit/metaaudit reale sau arhive reale. Nu s-a atins prin scriere `export_documente.py`, care rămâne în responsabilitatea main. Nu s-au folosit subagenți, rețea, copiere pe S: sau fișiere din alte directoare inspectate recursiv. Fixture-urile și capturile de test sunt exclusiv în `TemporaryDirectory` și au fost curățate de testele respective.

Baza de implementare este planul `06_REGISTRU/MASURI/SYS-001-plan-r01.md`, fundamentat pe `05_AUDIT/SYS-001/A-SYSTEMS-r01.json` și `.md`. P10, P11/P23, P12 și P21 sunt scenariile adversariale ale auditorului transpuse în teste v2; datele din această suită sunt sintetice și nu reprezintă aprobările SYS-001 reale.

## 2. Rulare efectivă a întregii suite din staging

Mediu verificat: **Python 3.12.10**, `Windows-11-10.0.26200-SP0`.

Director de lucru: `ROOT/04_INSTRUMENTE/r02_staging`.

Comandă executată:

```powershell
& 'C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe' -B -m unittest -q test_gatekeeper.py test_archive_round.py
```

Ieșirea efectivă a ultimei rulări, după ultimele modificări ale codului și testelor:

```text
----------------------------------------------------------------------
Ran 196 tests in 14.300s

OK
```

Cod de ieșire: **0**. Total: **196 teste executate; 0 failures, 0 errors, 0 skipped**. Testele de symlink și hard link au fost executate în acest mediu, nu omise. `-B` a prevenit cache-ul de import; inventarul final al staging-ului conține numai cele cinci fișiere enumerate.

Inventar verificat prin încărcătorul `unittest`, fără rerularea cazurilor:

| Clasă | Număr de teste |
| --- | ---: |
| `test_gatekeeper.GatekeeperTests` — regresii inițiale adaptate explicit la v2 | 115 |
| `test_gatekeeper.AdversarialR02Tests` — contracte, dovezi, migrare, Setext, extragere | 27 |
| `test_archive_round.ArchiveTests` — regresii de arhivare adaptate | 36 |
| `test_archive_round.ArchiveAdversarialR02Tests` — conservare incident și recuperare dovezi | 18 |
| Total | 196 |

Cele 151 de teste inițiale sunt păstrate/adaptate și sunt completate de 45 teste adversariale noi. Adaptarea este declarată, nu echivalată cu o rulare neschimbată a suitei r01: fixture-urile construiesc contracte/dovezi v2; cazul de arhivare a ciclului folosește conservarea explicită a respingerii; o rundă sintetică nouă își actualizează explicit probele; un copil care citează o sursă separată o declară ca dovadă înghețată.

La dezvoltare, prima rulare a celor 151 de cazuri adaptate a avut un eșec și două erori de fixture/contract; acestea au fost corectate înaintea regresiilor finale. O rulare intermediară de 194 teste a trecut. Numai rezultatul final de 196 teste de mai sus este rezultatul declarat al versiunii livrate. Nu se folosesc aceste rezultate pentru a modifica starea finding-urilor.

## 3. Trasabilitate la cele patru constatări

Rezultatele din tabel sunt comportamente verificate de aserțiunile testelor trecute. Sunt rezultate TEST ale implementării propuse, nu verdicte ale auditorului.

| Finding păstrat | Implementare propusă | Teste și rezultat efectiv verificat | Stare de audit |
| --- | --- | --- | --- |
| **SYS-A-SYSTEMS-r01-F01** | Contract v2 separat, legat prin hash de registru/audit/metaaudit; fixează versiuni și contracte dependente, politica și toate intrările de evaluare. | `test_F01_P10_retarget_requires_both_new_parent_audits_and_new_meta`: graful inițial trece; copilul nou trece separat; părintele cu rapoarte identice respinge după schimbarea dependenței. Actualizarea numai a contractului, a unui audit sau a ambelor audituri fără meta nou continuă să respingă. Controlul cu toate rapoartele sintetice reemise trece. Cazul cu același ID dependent și versiune nouă respinge de asemenea părintele vechi. | Neînchisă de producător; pentru retest A-SYSTEMS. |
| **SYS-A-SYSTEMS-r01-F02** | `evidence_files` în contract; dovezi `{path, sha256, anchor}`; citările obișnuite sunt limitate la intrări înghețate; arhivarea include sursele automat. | `test_F02_P11_changed_evidence_with_identical_reports_is_rejected`: schimbarea exclusivă a dovezii păstrează rapoartele identice și produce refuz HASH. `test_F02_P23_auto_archived_evidence_restores_without_original_root`: sursa exactă este indexată și recuperarea din `snapshot/sources` trece după ștergerea sursei originale temporare. Digest lipsă/greșit, dovadă neînghețată sau sursă înghețată schimbată chiar necitată resping. | Neînchisă de producător; pentru retest A-SYSTEMS. |
| **SYS-A-SYSTEMS-r01-F03** | `--preserve-rejected` păstrează rezultatul și manifestul declarat, bytes disponibili și observații distincte; modul strict rămâne separat. | `test_F03_P12_RETURN_HASH_preserved_with_declared_and_observed_separate`: validatorul rămâne RETURN/HASH, modul strict refuză, conservarea explicită produce snapshot verificabil; manifestul/rapoartele originale sunt identice, hash-ul vechi rămâne declarat, hash-ul actual apare separat. Revalidarea capturii rămâne respinsă. Sunt testate lipsuri, hash invalid, v1 istoric, JSON malformat, symlink/traversal, extras și refuz de overwrite. | Neînchisă de producător; pentru retest A-SYSTEMS și concordanță de protocol A-GOVERNANCE. |
| **SYS-A-SYSTEMS-r01-F04** | O singură trecere pentru titlurile ATX/Setext, folosită la verificarea etichetelor și la numărare. | `test_F04_P21_later_Setext_labels_all_refuse_HUMAN_REVIEW`: Sinopsis, Synopsis, Outline și Plan de capitole după un titlu introductiv, cu `=` și `-`, resping HUMAN_REVIEW. Titlul Setext obișnuit este exclus consecvent; controalele 49.999/50.000 tokenuri rămân respins/acceptat pentru condiția de volum. | Neînchisă de producător; pentru retest A-SYSTEMS. |

Controale suplimentare relevante:

- Contractul schimbat numai ca bytes, politica schimbată, relaxarea/modificarea cerințelor și câmpurile suplimentare ascunse invalidează evaluarea veche. `status` și listele de rapoarte nu intră în propriul hash; totuși lipsa rapoartelor respinge validarea.
- `test_F02_paired_MD_can_be_frozen_before_JSON_without_self_hash` și cazul de arhivare pereche verifică acceptarea tehnică a unui MD stabil, fără hash al JSON-ului viitor, fixat în `evidence_files`; modificarea ulterioară a MD-ului produce refuz HASH. Înghețarea propriului JSON sau a registrului în propriile intrări este refuzată pentru circularitate.
- v1 pentru audit/meta/politică/registru și dovezile vechi string sunt cazuri negative explicite; nu sunt convertite tacit. Refuzul generic de schemă nu ține locul probei funcționale: P10/P11/P12/P21 pornesc de la fixture-uri v2 coerente, cu controale pozitive.
- Pragul 950/951, criteriile/ponderile/bundle-ul exacte, autoauditul, auditorul duplicat, separarea A-QAMANAGER, constatări deschise, hash-uri vechi, cicluri, fișiere lipsă, căi nesigure și absența modificării intrărilor rămân acoperite de suită.

## 4. Interfața oferită auditorilor r02

API read-only: `gatekeeper.extract_contract(root, deliverable_id) -> bytes`.

CLI: `python -B gatekeeper.py --root ROOT --deliverable ID --extract-contract`.

Extragerea produce exact bytes UTF-8 ai contractului, cu LF final; nu produce un audit, note sau aprobare. Cazul pozitiv API/CLI a fost comparat octet cu octet cu contractul fixture-ului. Cazul cu sursă schimbată dă exit 2, stdout gol și diagnostic HASH pe stderr.

Proiecția contractuală conține: `schema_version: 2`, `deliverable_id`, `version_id`, `stage`, `files`, `evidence_files`, `producer_agent_ids`, `required_audit_roles`, `requirements`, `criteria`, dependențele `{deliverable_id, version_id, contract: {path, sha256}}` și politica `{path, sha256}`. Nu conține status, listele de audit, meta sau propria referință de contract. Acest lucru evită autohash-ul manifestului/raportului.

Bootstrap-ul este limitat la extragere: propria referință are cale/digest sintactic valide, digestul poate fi temporar zero, iar fișierul propriu poate încă lipsi. Dependențele trebuie să aibă contracte coerente și toate sursele trebuie să corespundă hash-urilor. Validarea pentru acceptare nu admite placeholder-ul. Main salvează bytes ca fișier nou și înregistrează separat digestul; auditorii folosesc referința exactă, fără completare automată a rapoartelor.

Schema completă și exemplele fără scoruri prefabricate sunt în README-ul staging-ului. Înainte de rapoartele reale r02, main trebuie să alinieze politica și registrul v2, contractele și modelele de audit/metaaudit. Auditorii r02 își redactează independent rapoartele, apoi A-QAMANAGER verifică exact acei octeți. Nu se schimbă `schema_version` pe rapoartele r01 ca substitut pentru reevaluare.

## 5. Hash-uri ale celor cinci fișiere livrate

SHA-256 calculate după rularea finală; fișierele din staging nu au mai fost modificate după această calculare:

| Fișier în `04_INSTRUMENTE/r02_staging` | SHA-256 |
| --- | --- |
| `gatekeeper.py` | `3e27a5e759a2f31b23e9158963aea140302c91b74d362d2126ad8b535d0177f8` |
| `archive_round.py` | `684c48c859a4f289d4f6955d450660bb7fa230d324dc802cabcb986c55948f97` |
| `test_gatekeeper.py` | `4bcce4b031e9ec5f269bdc098af2a4f0a931b63d5d0ded86a9f0706c953644f2` |
| `test_archive_round.py` | `331b714dd0fabd6063988948a24a5bff3ab57210d9e679707a7c6954d1a1abc7` |
| `README.md` | `bbc57affe30eaa0c8642d4e66ad880462a628c490ea0114a4cd947b4d0d822e8` |

Aceste hash-uri permit identificarea versiunii TEST propuse, nu sunt semnături ori certificare de autor.

## 6. Respectarea înghețării r01 și observații de concurență

Au fost comparate prin SHA-256 fișierele selectate înainte și după implementarea în staging. Cele cinci fișiere curente au rămas identice:

| Fișier curent din `04_INSTRUMENTE` | SHA-256 inițial = final |
| --- | --- |
| `gatekeeper.py` | `c63140cb773b101f90bdca7858baadb31edbef99de894ab93ad39a08d4724145` |
| `archive_round.py` | `2c6f3d39a717765e03595bd535b3ad8dcbaf52cf22f5bc40e5c7050fdc514031` |
| `test_gatekeeper.py` | `1281f657dec7711c55fc3a1297fbcd02d7be351afae3e98aad5b919f945620ed` |
| `test_archive_round.py` | `311e999191c96618c4701153cff22d58abaa705aac0d1601bdf663285921f2f6` |
| `README.md` | `d0426ea6fe4ce159370ca06128190b53253d571d5bc8f5f4d12f344f81278a9a` |

Au rămas identice și fișierele selectate:

- `06_REGISTRU/agents.json`: `7bdc7aff5dbdddfe76dfc47722655e42c05a9e03391dd72b23deed5ff243d446`.
- `00_CONDUCERE/policy.json`: `c81555cebd890fccadb224a22bf5939948861a28ca01816abcf28f4a50333c41`.
- `08_ARHIVA/SYS-001/r01-primary-complete/index.json`: `c3f3ba3a63ab03e84ac309b5859af07d9afbf41b20476ac8b2e2fd1a900d4797`.

Au fost observate două schimbări paralele între citirile inițială și finală. P-SYSTEMS nu a scris în aceste fișiere, nu atribuie autorul schimbării și nu a intervenit pentru a o anula:

| Fișier observat | SHA-256 inițial | SHA-256 final observat |
| --- | --- | --- |
| `04_INSTRUMENTE/export_documente.py` | `bf4fef7a0d634696cfc4cc8460a50c1f3bbf545dabad7bac4e7b423779e8bd8a` | `b86563ad2f27ef3bfdf8432e4f24897c5a9361a41ee165ec50774fce88da3296` |
| `06_REGISTRU/deliverables.json` | `f2cd4902b4e5be5fd9a31e6b9f72046785a7799dca365bf17988435719d0e86d` | `0af1735a3122add3894eb3996f97bd7cc788ea2d4d4bbdabcee3d04a59241457` |

Nu se afirmă că toate registrele sau întregul arbore al atelierului au rămas identice. Verificarea indexului existent nu este o revalidare integrală a arhivei r01. În acest mandat nu s-a copiat sau rescris nimic în acea arhivă.

## 7. Limite reale și predare

- Testele demonstrează comportamentele implementate pe cazurile executate; nu autentifică auditori și nu dovedesc adevărul probelor sau calitatea literară. `active` rămâne autorizare locală, independentă de lifecycle.
- Politica poate fi modificată de operatorul local. Legarea de hash invalidează un contract anterior, dar nu împiedică un operator privilegiat să rescrie întregul ansamblu. Nu există WORM, semnături externe sau certificare antifals.
- Arhivarea nu este snapshot atomic al filesystem-ului. Sursele se mențin stabile; schimbările observate sunt refuzate/semnalate, iar erorile de scriere lasă runde incomplete nereutilizabile.
- Conservarea respingerii cere registru parsabil și ID neambiguu plus rezultat original cu `passed: false`; nu pretinde recuperarea completă când declarațiile nu pot fi parcurse sau sursele lipsesc. Manifestul declarat și bytes observate pot rămâne neconforme; acesta este tocmai incidentul păstrat.
- Nu se validează semantic existența ancorelor, numărul liniilor, caracterul narativ al textului sau absența conceptuală a oricărei circularități inventate în MD. Hash-urile, căile și legăturile structurale sunt verificate; regulile limitate ATX/Setext sunt documentate.
- G01 rămâne blocat. Nu s-a ales între Boucher și Dubois, nu s-a modificat selecția canonică și nu s-a modificat manuscrisul.

Predare: cele cinci fișiere r02 sunt gata pentru integrarea ulterioară de către main, prin patch, după închiderea metaauditului r01. Acest document este rezultatul tehnic TEST al producătorului. Auditorul independent decide închiderea fiecăreia dintre `SYS-A-SYSTEMS-r01-F01`, `SYS-A-SYSTEMS-r01-F02`, `SYS-A-SYSTEMS-r01-F03`, `SYS-A-SYSTEMS-r01-F04`; nicio astfel de închidere nu este declarată aici.
