# ROM-001-G01 r01 — recuperare REALĂ AFTER, rundă negativă

P-SYSTEMS `01a0d0d9-1f95-7211-8093-c26e28e6ebee`, producător suport, nu auditor G01. Raport: 2026-09-24T08:33:28Z. Momentele execuției sunt UTC.

## Rezultat

Recuperarea izolată este încheiată. Validatorul **restaurat** a returnat **exit 2, `passed: false`**. Rezultatul său este identic semantic cu `result.json` din snapshotul AFTER, fără eliminări de câmpuri sau normalizarea verdictului. Nu am comparat cu rezultatul live.

RETURN este păstrat; G01 nu este acceptat și nicio constatare nu este închisă de producător.

## Intrare și copie păstrată

- Snapshot: `08_ARHIVA/ROM-001-G01/r01-after-audit`.
- Index SHA256: `08d454312b19fc83debe2a159b5277a274ac0e796af63d2d1d1f39900a3871ce`; 197.571 bytes.
- Contract r01 SHA256: `07110637be555cb455727593ebdf9ef88de1f27c12b5a389f53e79544bd6cebe`; 25.144 bytes.
- Rezultat AFTER înghețat SHA256: `6acb5bf733935c0c5384b1900f3c5eeed17e7b34f991b425e605ab0f7d75466b`; 57.372 bytes.
- Director NOU păstrat: `09_RECUPERARI/ROM-001-G01-r01-after-20260924T082739Z-f607d274`.
- Calea absolută a destinației a fost validată sub ROOT/09_RECUPERARI la 2026-09-24T08:27:41.3019046Z, înainte de creare. Fără reparse/symlink/junction în trasee ori arborii controlați; fără suprascriere sau cleanup.

S-au verificat efectiv toate cele **751 intrări / 120.939.919 bytes** față de index: SHA256, dimensiuni, căi sigure și set exact. Indexul coincide cu digestul mandatului, sidecar-ul, copiile plate și recipisa. Proveniența existentă este `06_REGISTRU/PROBE_ARHIVA/ROM-001-G01-r01-after/provenienta.json`; afirmațiile ei nu au înlocuit verificarea proprie.

S-au copiat numai copiii arborelui `sources`: **746 fișiere / 120.799.809 bytes / 48 subdirectoare**. Cele cinci intrări rămase — trei manifeste dependente, manifestul G01 și `result.json` — au fost verificate în snapshot, fără copiere în rădăcina recuperată. Cu indexul și sidecar-ul, snapshotul are 753 fișiere / 121.137.555 bytes.

Copiere efectivă 2026-09-24T08:27:39.3063031Z → 2026-09-24T08:27:55.9412695Z, cu mecanismul nativ:
```powershell
Copy-Item -LiteralPath $top.FullName -Destination $restoreDestination -Recurse -ErrorAction Stop
```

Comanda a fost aplicată numai copiilor de nivel superior din snapshot/sources, după verificarea căilor și a întregului set sursă. Scripturile exacte de control/copiere și inventarul cu fiecare hash/dimensiune observată sunt în JSON-ul pereche.

## Rularea efectivă

Cwd și `--root`: `D:\00. Downloads\Dracula Book\02. ATELIER EDITORIAL - ROMANE 50000\09_RECUPERARI\ROM-001-G01-r01-after-20260924T082739Z-f607d274`.

```powershell
& 'C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe' -B -X utf8 'D:\00. Downloads\Dracula Book\02. ATELIER EDITORIAL - ROMANE 50000\09_RECUPERARI\ROM-001-G01-r01-after-20260924T082739Z-f607d274\04_INSTRUMENTE\gatekeeper.py' --root 'D:\00. Downloads\Dracula Book\02. ATELIER EDITORIAL - ROMANE 50000\09_RECUPERARI\ROM-001-G01-r01-after-20260924T082739Z-f607d274' --deliverable ROM-001-G01 --json
exit $LASTEXITCODE
```

Python 3.12.10; 2026-09-24 08:28:12 UTC → 2026-09-24 08:28:13 UTC; durata procesului raportată: 0.8444765 s. `exit $LASTEXITCODE` propagă explicit exitul 2. `-B` evită cache-ul.

Validator SHA256: `ad90fd517856e7d7b55d965598b4f776ea5d1098baa6f5a71518b51b0c63363b`. Registrul restaurat SHA256: `468289f1f00fa42f67667b8da2ce96804e13ded5edff6e5a9c0e64bddc71253d`. Schema este v2, versiune G01 r01, status conservat `RETURN_G01_r01`, 11 artefacte și 126 evidence_files. Manifestul restaurat coincide structural cu manifestul din snapshot; contractele dependente fixează SYS-001, SEL-001 și RES-001 r03.

Erorile emise exact:
```text
05_AUDIT/ROM-001-G01/r01/A-CANON.json: FINDING: unresolved medium finding ROM-001-G01-A-CANON-F01 in 05_AUDIT/ROM-001-G01/r01/A-CANON.json
ROLES: missing passing audits for ['A-CANON']
META: check evidence must explicitly pass
```

A-CANON există, are RETURN și `ROM-001-G01-A-CANON-F01` open. Eroarea ROLES nu spune că lipsește fișierul, ci că nu există un audit A-CANON care să treacă. META există, are RETURN și `META-ROM-001-G01-r01-F01` open, cu evidence/scoring/closure=false. Engine raportează primul check meta nepromovat (`evidence`), nu ID-ul constatării meta. PASS-ul individual GOV este conservat ca atare, dar invalidat de META; nu devine acceptare G01.

SYS-001/SEL-001/RES-001 r03 au `passed: true` în rezultatul restaurat, fără erori; aceasta nu este o reevaluare a lor de către mine. JSON-ul pereche păstrează integral rezultatul și textul ieșirii capturate, inclusiv calculele preexistente, fără scoruri noi.

## Control după execuție și limite

Reverificare 2026-09-24T08:30:04.4801741Z → 2026-09-24T08:30:09.2236624Z: toate cele 751 intrări ale snapshotului și toate cele 746 fișiere recuperate au aceleași hashuri/dimensiuni. Indexul, sidecar-ul, recipisa și probele plate sunt neschimbate. Seturile de fișiere și directoare corespund; **zero nepotriviri, zero cache noi**. Copia recuperată a rezultatului AFTER este byte-identică cu `result.json` din snapshot.

Nu există erori de hash/schema/contract/recuperare rămase. Două incidente auxiliare read-only au fost rezolvate înainte de concluzii: numele inițial presupus al provenienței și o ieșire agregată trunchiată la transport, recitită integral în apeluri separate. Detaliile sunt în JSON; niciun control parțial nu a fost considerat suficient.

Nu este audit semantic/editorial, certificare antifals, WORM, backup extern sau clonare completă a mediului. Hashurile verifică bytes față de intrarea fixată; nu autentifică autorii ori adevărul probelor. Copy-Item/citirile nu sunt atomice și nu protejează absolut împotriva unui operator privilegiat concurent. Python instalat rămâne extern copiei. Nu s-au urmărit rawlogs și nu s-au capturat reasoning/system/developer.

Nu s-au modificat live, registrele recuperate, contractele, r02, rapoartele r01, arhiva, G00, site-ul sau strategia. `verify_archives_r02.py` nu a fost folosit. Scrierile sunt exclusiv copia nouă păstrată și aceste două rapoarte. Producătorul nu închide findings și nu autorizează revizia; coordonatorul decide separat. După predare, scrierile sunt oprite.

