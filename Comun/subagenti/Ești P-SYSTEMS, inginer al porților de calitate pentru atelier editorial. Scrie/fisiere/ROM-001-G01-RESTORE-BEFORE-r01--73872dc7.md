# ROM-001-G01 — recuperare REALĂ BEFORE r01

P-SYSTEMS, `01a0d0d9-1f95-7211-8093-c26e28e6ebee` — producător suport, nu auditor G01. Raport creat: 2026-09-24T07:32:57Z.

Rezultat: recuperare reală terminată și verificată față de snapshot. Validatorul restaurat a returnat **exit 2, passed:false**, exclusiv din lipsa auditurilor și a metaauditului G01, așteptată în BEFORE. Nicio eroare observată de hash, schemă, contract sau recuperare. Aceasta NU este acceptare G01 și nu închide constatări editoriale.

## Intrarea imuabilă și verificările

Snapshot: `08_ARHIVA/ROM-001-G01/r01-before-audit`.

SHA-256 index: `73befab70d1266a41f79a339ce00eadb00d32efd57c5afdf9eb9ea7817c99823`, identic cu mandatul, sidecar-ul, recipisa `06_REGISTRU/REZULTATE/ROM-001-G01-BEFORE-receipt-r01.json` și copia plată `06_REGISTRU/PROBE_ARHIVA/ROM-001-G01-r01-before/index.json`. Copia plată a sidecar-ului este și ea byte-identică prin SHA-256; proveniența declară aceeași rundă și 629 intrări.

Recipisa are SHA-256 `3848a0b3dc9c17b950852a9c3fbe3a009d8f98edc7f8226a278f6cbaa4dc8f96`. Câmpurile sale archived, snapshot_path, index_sha256, files_archived și editorial_approval_issued au fost confruntate efectiv, nu acceptate doar din rezumatul managerului.

Preflight final: 2026-09-24T07:26:05.3268462Z. Toate **629/629 intrări** au hash și dimensiune conforme. Inventarul pe disc este exact: cele 629 intrări plus index.json/index.sha256. Fără căi reparse, symlink/junction sau ieșire din perimetru.

Arborele `sources` are **625 fișiere**. Celelalte patru intrări sunt `manifest.json` și cele trei `dependency_manifests`; au fost verificate la sursă, dar nu copiate ca fișiere externe arborelui sources. Nu am completat recuperarea din live.

## Recuperarea păstrată

Rădăcina recuperată:

```text
D:\00. Downloads\Dracula Book\02. ATELIER EDITORIAL - ROMANE 50000\09_RECUPERARI\ROM-001-G01-r01-before-20260924T072727Z-334ca93c
```

Copiere: 2026-09-24T07:27:28.3970474Z → 2026-09-24T07:27:37.7883782Z. Director nou, identificator unic, cale absolută verificată înaintea creării sub `ROOT/09_RECUPERARI`; nu s-a reutilizat un director. S-au copiat cu `Copy-Item -LiteralPath … -Destination … -Recurse` numai copiii arborelui snapshot/sources, astfel încât `04_INSTRUMENTE`, `06_REGISTRU` etc. sunt direct în rădăcina recuperată.

625 fișiere, **80.135.939 bytes**, 41 subdirectoare. Fiecare fișier recuperat a fost comparat cu intrarea indexului după copiere și din nou după validator. Zero nepotriviri sau fișiere suplimentare. Directorul se păstrează; nu a fost șters sau curățat.

JSON-ul pereche conține pentru fiecare dintre cele 625 de fișiere calea recuperată relativă, calea în index, hashul/dimensiunea efectiv observate și comparația cu indexul. Include și comanda de copiere, recipisa, datele verificărilor și ieșirea reală integrală a validatorului.

## Comanda efectiv executată

Interpret: Python 3.12.10 instalat local. Cwd: rădăcina recuperată de mai sus. Codul executat este `04_INSTRUMENTE/gatekeeper.py` RESTAURAT, nu cel live; SHA-256 `ad90fd517856e7d7b55d965598b4f776ea5d1098baa6f5a71518b51b0c63363b`.

```powershell
& 'C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe' -B -X utf8 'D:\00. Downloads\Dracula Book\02. ATELIER EDITORIAL - ROMANE 50000\09_RECUPERARI\ROM-001-G01-r01-before-20260924T072727Z-334ca93c\04_INSTRUMENTE\gatekeeper.py' --root 'D:\00. Downloads\Dracula Book\02. ATELIER EDITORIAL - ROMANE 50000\09_RECUPERARI\ROM-001-G01-r01-before-20260924T072727Z-334ca93c' --deliverable ROM-001-G01 --json
exit $LASTEXITCODE
```

Nu s-a folosit `verify_archives_r02.py`. Opțiunile `-B -X utf8` au fost aplicate. Rezultat nativ: exit 2; JSON real `deliverable_id: ROM-001-G01`, `version_id: r01`, `passed: false`, `weighted_scores: []`, `word_count: null`.

Erorile exacte:

```text
AUDITS: missing audit reports for ROM-001-G01
INDEPENDENCE: at least two distinct registered auditors required
ROLES: missing passing audits for ['A-CANON', 'A-GOVERNANCE']
META: ROM-001-G01 requires meta_audit
```

Registrul BEFORE are `audits: []`, fără cheie `meta_audit`; politica recuperată are `require_meta_audit:true`. Mesajele INDEPENDENCE și ROLES decurg din absența rapoartelor, nu demonstrează un autoaudit sau o corupere. Nu am inventat audituri și nu am modificat registrele ca să obțin PASS.

## Versiune, contract și fișiere

Identitate recuperată: ROM-001-G01 / r01 / G01; starea înscrisă rămâne DEPUS. Intrarea G01 din registrul recuperat este semantic identică cu manifest.json al snapshotului. Contract schema 2: `06_REGISTRU/CONTRACTE/ROM-001-G01-r01.json`, SHA-256 `07110637be555cb455727593ebdf9ef88de1f27c12b5a389f53e79544bd6cebe`, exact cel din mandat.

Contractul are 11 artefacte și 126 fișiere probatorii. Componentele editorului r02 fac parte din această depunere G01 version_id r01; nu am redenumit versiunile. Cele 11 artefacte au fost verificate și de validator:

| Cale relativă rădăcinii recuperate | SHA-256 observat de validator |
| --- | --- |
| `07_ROMANE/ROM-001/00_BRIEF/BRIEF_ROMAN_r02.md` | `fb26a4a6bdfa76da4d0a66cc8fac9b75677ee2f299e014cc3de666978c9e78c7` |
| `07_ROMANE/ROM-001/00_BRIEF/DECIZII_CANON_r02.md` | `6ee676184ae2d21bbdffb57459158e18fae35ffb0ec3f2a7d7de4533d0b2b4a4` |
| `07_ROMANE/ROM-001/00_BRIEF/CANON_OPERATIONAL_r02.md` | `a5a9ff52b30f110d362e4b2175a17fe924d8a34d11c89efeb407d5025db54abc` |
| `07_ROMANE/ROM-001/00_BRIEF/REGISTRU_DREPTURI_r01.md` | `d8a18a237b0bc855b11f7c9dbc1030a52df39a462b6c9cf589456474df12be5f` |
| `07_ROMANE/ROM-001/00_BRIEF/TRASABILITATE_DEPUNERE_r01.md` | `04666f05d44e796d8ed6be5196930e0e164f76403e76d9c724239cfad1ea859f` |
| `07_ROMANE/ROM-001/01_CANON/r01/CANON_FACTUAL.md` | `0635d163992d0c63d0b1d815df000816f8b9320c84e33c732cb899dd6eebd3ab` |
| `07_ROMANE/ROM-001/01_CANON/r01/CRONOLOGIE_OBSERVATA.md` | `59532fffe2ce25487863a9ecb8517cab85ba836637b49bda597631dc0f81633c` |
| `07_ROMANE/ROM-001/01_CANON/r01/CONTRADICTII.md` | `593b11074efb6833d198af794256a0b1b3c2567c54a1acfde3b880dd328c05d0` |
| `07_ROMANE/ROM-001/01_CANON/r01/JURNAL_LECTURA.md` | `dba0d58e1e123a6e48dfe164fd54da669bfae4b4bb42655efe0dd07e0b938afc` |
| `07_ROMANE/ROM-001/01_CANON/MATRICE_SURSE_r01.md` | `692bf5108ef9a066fd0524eef6dccbb7f6bd172bb4f27f7ca149e76bd1d6b801` |
| `07_ROMANE/ROM-001/01_CANON/LECTURA_AUXILIARE_MANAGER_r01.md` | `8a08f2358479913c3c998d6110a7d00aabc4cbf0545d9c8bd32f94a1cbf02c39` |

Dependențele sunt cele fixate în contract și au fost evaluate din copia recuperată, fără schimbarea aprobărilor:

| Dependență | Versiune | passed în JSON real | Artefacte verificate | Erori |
| --- | --- | --- | ---: | ---: |
| SYS-001 | r03 | true | 68 | 0 |
| SEL-001 | r03 | true | 1 | 0 |
| RES-001 | r03 | true | 3 | 0 |

Aceste rezultate ale dependențelor nu compensează lipsa auditurilor G01.

## Control după execuție și limite

La 2026-09-24T07:29:34.0630966Z, toate cele 625 de fișiere recuperate corespundeau în continuare indexului, fără fișiere noi/cache/rapoarte în copie. Toate cele 629 de intrări ale snapshotului au fost reverificate și erau neschimbate. Hashul registrului recuperat înainte/după rulare este același: `95d3e76d6b80367b99af6e9d8e68da29a7b970100a9e380a42a12a83c4285619`.

Protocolul și README-ul instrumentelor au fost citite. Copierea/hashuirea nu echivalează cu lectură editorială, certificare de drepturi sau adevăr semantic. Nu s-au capturat rawlogs/reasoning/system/developer; numai fișierele deja prezente în sources al snapshotului autorizat. Originalele/platforma nu au fost folosite pentru a umple copia. Nu s-a modificat infrastructura G00, site-ul, strategia sau vreun contract/registru live.

Prima ieșire detaliată a preflightului read-only a depășit limita de transport/afișare; verificarea a fost reluată cu sumar compact înainte de copiere. Nu s-a confundat trunchierea harnessului cu eroare de arhivă sau cu verificare completă.

Hashurile sunt verificări locale, nu WORM, semnături ori backup extern. Nu există garanție absolută contra unui administrator sau a înlocuirii concurente a căilor; verificările repetate descriu starea efectiv observată. Căile 08_ARHIVA de aici identifică intrarea de recuperare, nu cer ingestia arhivelor vechi drept probe de audit; copiile plate sunt indicate separat.

Singurele scrieri: noul director recuperat (cu părintele 09_RECUPERARI creat dacă lipsea) și acest raport MD/JSON. Recuperarea AFTER_AUDIT este un test viitor separat. Nu se declară acceptare G01. După predarea acestei perechi, scrierile se opresc.

