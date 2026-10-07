# Exportul istoricului observabil — r03 integrat, depus pentru reaudit

Propunere P-SYSTEMS limitată la `SYS-A-SYSTEMS-r02-F05` și `SYS-A-SYSTEMS-r02-F06`, identificate în raportul final A-SYSTEMS r02. Nu este audit, acordare de scor sau închidere de constatare. P-MANAGER a integrat implementarea P-SYSTEMS după conservarea r02, pentru un contract nou. Stagingul și rezultatul original al producătorului rămân păstrate separat; descrierea rulării din staging de mai jos este instrucțiunea pentru acea copie. Nu se înlocuiesc exporturile existente și nu se modifică sursele, configurația înghețată ori validatorul/arhivatorul v2.

Python 3.10+, numai biblioteca standard. Acesta rămâne un instrument auxiliar de recuperare a surselor explicit autorizate, nu un serviciu automat. Configurația atelierului enumeră cele nouă execuții relevante; nu se inventariază alte conversații.

## Rădăcină și rulare

Copia din `r03_staging` cere o rădăcină explicită. Nu deduce atelierul real din poziția de staging. Exemplu numai pentru un atelier sintetic deja pregătit:

```powershell
python -B export_istoric_observabil.py --root "C:\TEMP\ATELIER_TEST" --round history-TEST
python -B export_istoric_observabil.py --root "C:\TEMP\ATELIER_TEST" --round history-ALT --sources "surse-noi.json"
```

API pentru teste sau apel local: `export_capture(root, round_id, sources="06_REGISTRU/surse_export_istoric.json") -> dict`. Nu executați aceste exemple pe surse reale fără mandatul corespunzător.

După integrarea în `ROOT/06_REGISTRU/export_istoric_observabil.py`, rădăcina implicită este părintele lui `06_REGISTRU`, iar comanda existentă rămâne compatibilă:

```powershell
python -B 06_REGISTRU/export_istoric_observabil.py --round ID-NOU
```

`--sources` rămâne relativ la ROOT. Configurațiile absolute, cu traversare sau rezolvate în exterior sunt refuzate. Pentru o altă sesiune se pregătește o configurație NOUĂ internă; configurația înghețată nu se editează.

Configurația rămâne o listă de obiecte cu `agent_id`, `role`, `path`. UUID-ul trebuie să fie canonic, nenul și unic; calea sursei este absolută, către un fișier regulat al cărui nume se termină cu `<agent_id>.jsonl`. Sursele autorizate pot fi în afara atelierului: sunt numai citite, niciodată copiate brut sau modificate. Dublurile de sursă, inclusiv aliasuri fizice, sunt refuzate. Cheile JSON duplicate resping configurația. Cele nouă roluri actuale și structura configurației reale sunt compatibile.

## Prefixul sursei: numai bytes existenți

`complete_prefix(raw)` returnează `raw[:raw.rfind(b"\n") + 1]`. Prefixul se termină la ultimul LF existent. Dacă nu există LF, inclusiv pentru sursa goală sau un JSON complet fără terminator, prefixul este de zero bytes și se selectează zero înregistrări. Nu se adaugă LF și nu se normalizează CRLF. O coadă incompletă după ultimul LF nu se parsează și nu intră în hash.

Pentru orice captură acceptată: `source_prefix_bytes <= len(source)` și `source_prefix_sha256 == SHA256(source[:source_prefix_bytes])`, raportate la bytes citiți. Un JSON malformat într-o linie completă refuză captura. Terminatorul din JSONL-ul DERIVAT nu reprezintă un octet adăugat prefixului sursei; fișierul derivat gol păstrează formatul anterior.

## Izolarea ieșirilor și coliziuni

Destinația unică rămâne `ROOT/06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/<round>/`. Se validează întreaga configurație și toate numele înainte de scriere.

- Rol: 1–61 caractere ASCII alfanumerice/`_`/`-`, primul alfanumeric. Rundă: 2–61 caractere, aceeași regulă; limita anterioară a rundelor se păstrează.
- Sunt refuzate traversări, separatori, căi absolute, drive-uri, fluxuri NTFS, spații, puncte, caractere de control și formele de alias cu `~`. Numele dispozitivelor Windows sunt rezervate. Rolul `index` este rezervat conservator.
- Rolurile și numele de ieșire sunt unice fără diferențiere de majuscule. Lista completă include și `index.json`/`index.sha256`; o coliziune respinge, nu redenumește implicit.
- Rădăcina și strămoșii ei, apoi fiecare părinte al capturii, sunt verificate înainte de rezolvare. Symlink-urile și punctele Windows reparse, inclusiv junction-uri, sunt refuzate chiar dacă ținta este internă.
- Directoarele se creează componentă cu componentă; părinții se reverifică imediat înaintea fiecărei scrieri. Fișierele se creează exclusiv, cu `O_EXCL` și `O_NOFOLLOW` unde există. Nu se suprascriu fișiere, aliasuri ori runde existente, nici diferențiate numai prin majuscule; inclusiv symlink-urile suspendate sunt considerate ocupare.

JSONL-ul conține numai selecția observabilă, cu timestamp și linie sursă; MD-ul conține mesajele pentru lectură. Indexul păstrează schema anterioară, prefixele, numărătorile, omisiunile și hashurile fișierelor derivate. Sidecar-ul `index.sha256` este scris ultimul. Exit 0 înseamnă operație de export finalizată, nu aprobare editorială. Refuzul CLI are exit 2 și nu emite JSON de succes. Un eșec după începerea scrierii poate lăsa o rundă parțială; nu se șterge și nu se reutilizează automat. O captură se verifică prin hashul indexului și toate hashurile/dimensiunile declarate, nu numai prin existența unui sidecar.

## Filtru și limite păstrate

Funcțiile `clean_value`, `redact`, `select` sunt păstrate textual identic cu r02. Se păstrează selecția mesajelor publice, a apelurilor și rezultatelor observabile, excluderile pentru reasoning/system/developer/metadate ascunse, tratarea media și redacțiile cunoscute. Nu se exportă rawlogs. Nu s-au adăugat categorii publice și nu s-a schimbat pragul temporal `2026-09-24T00:35:17.566Z`.

Recuperarea este ulterioară evenimentelor, cu timestampuri locale, nu certificate. Nu reconstruiește ieșiri deja trunchiate și nu este detector universal de secrete sau dovadă a exhaustivității. Dosarul rămâne intern, fără publicare pe site. Originalele rămân read-only; rapoartele și sursele editoriale se arhivează separat.

Izolarea este verificată pe căi stabile. Codul portabil stdlib nu oferă o tranzacție atomică a întregului arbore: un administrator/proces concurent capabil să înlocuiască directoare exact între verificare și creare depășește garanția acestor verificări. Păstrați control exclusiv asupra arborelui destinației pe durata capturii; nu se pretinde rezistență absolută la curse privilegiate, WORM, semnătură sau certificare antifals. Operatorul local poate altera surse și indexuri și recalcula hashurile. Verificarea semantică/editorială rămâne o evaluare distinctă a auditorilor desemnați, nu un rezultat al acestor teste. Auditurile realizate de agenți nu sunt prezentate ca lecturi sau evaluări umane.

## Teste

Din `06_REGISTRU/r03_staging`:

```powershell
python -B -m unittest -v test_export_istoric.py
```

Cele 17 teste existente sunt păstrate; cele trei teste de configurație primesc explicit rădăcina sintetică. În plus: 12 teste de prefix, 23 de destinație și 13 de compatibilitate — total 65 metode unittest, nu număr de subcazuri.

Fixture-urile sunt exclusiv în `TemporaryDirectory`, inclusiv sursele și țintele numite `OUTSIDE_ROOT`. Înainte de cleanup se validează directorul temporar, căile și țintele linkurilor; linkurile/junction-urile se elimină ca linkuri, apoi se curăță fixture-ul. Niciun fișier real exterior nu este folosit drept țintă de test. Lipsa suportului OS pentru linkuri/junction-uri produce skip explicit, niciodată succes simulat. Rezultatele efective și probele auditorului sunt consemnate în `REZULTAT_EXPORT_r03.md`.
