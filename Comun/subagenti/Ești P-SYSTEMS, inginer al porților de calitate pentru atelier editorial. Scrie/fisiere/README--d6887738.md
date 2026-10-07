# Instrumente operaționale v2 — nucleu r02, depunere SYS-001 r03

P-SYSTEMS a produs versiunea în staging, iar P-MANAGER a integrat cele cinci fișiere după metaauditul și arhivarea r01-after-audit. Versiunea integrată este depusă pentru reaudit independent; nu închide findings și nu constituie aprobare editorială. Mențiunile de staging din descrierea migrării sunt contextul pregătirii. Exportatorul DOCX/PDF și exportatorul istoricului sunt livrabile distincte ale coordonatorului, incluse în manifestul SYS pentru control.

Python 3.10+, numai biblioteca standard; testat pe Python 3.12.10. Fișiere independente de implementarea r01: `gatekeeper.py`, `archive_round.py`, `test_gatekeeper.py`, `test_archive_round.py`, acest README. Validatorul citește fără să scrie. Arhivatorul scrie numai sub `ROOT/08_ARHIVA`. Nu există rețea, copiere pe S:, publicare ori modificare automată a registrelor. Toate probele livrate folosesc exclusiv `TemporaryDirectory` și date TEST sintetice, nu aprobări reale.

## Modificări urmărite

| Finding păstrat | Corecție propusă și probe TEST |
| --- | --- |
| `SYS-A-SYSTEMS-r01-F01` | Contract v2 legat prin hash de audit și metaaudit, inclusiv versiuni/contracte dependente. P10: dependența nouă poate trece separat, însă părintele cu rapoarte vechi respinge. |
| `SYS-A-SYSTEMS-r01-F02` | Referințe probatorii cu hash: intrările produsului în contract, suplimentele ulterioare în propriul raport JSON; toate în snapshot. P11: deriva sursei respinge. P23: recuperare din snapshot fără sursa originală. |
| `SYS-A-SYSTEMS-r01-F03` | Mod explicit `--preserve-rejected`, cu declarații originale și observații separate. P12: se conservă RETURN/HASH fără repararea declarației vechi. |
| `SYS-A-SYSTEMS-r01-F04` | Aceeași identificare ATX/Setext pentru etichete și numărare. P21 și variantele de titlu Setext ulterior declanșează HUMAN_REVIEW. |

Planul și raportul tehnic anterior sunt `ROOT/06_REGISTRU/MASURI/SYS-001-plan-r01.md`, respectiv `ROOT/06_REGISTRU/MASURI/SYS-001-tehnic-rezultate-r02.md`. Raportul tehnic descrie livrarea de dinaintea extensiei opționale de suplimente, nu hash-urile și suita acestei revizii; rămâne nemodificat. Rezultatele actuale TEST sunt la finalul acestui README. Rezultatele de test nu schimbă `open` în `closed`. Închiderea aparține auditorului; controlul rapoartelor aparține A-QAMANAGER.

## Schema strictă v2

Nu se acceptă tacit schema r01 în fluxul de validare sau de extragere a contractului. `schema_version` este întregul 2 în politică, registrul de livrabile, contract, audit, metaaudit, rezultatul validatorului și indexul nou de arhivă. `true`, `2.0`, șirurile numerice, versiunea 1 și versiunile necunoscute resping unde se cere acest întreg. Cheile JSON duplicate și câmpurile necunoscute din contractele validate resping.

Politica `ROOT/00_CONDUCERE/policy.json` are exact:

```json
{
  "schema_version": 2,
  "threshold_exclusive": 950,
  "score_scale": 1000,
  "min_independent_auditors": 2,
  "require_all_criteria_above_threshold": true,
  "require_meta_audit": true
}
```

`require_meta_audit` trebuie să fie explicit boolean. Atelierul folosește `true`; fixture-urile de regresie pot seta explicit `false` pentru izolarea controalelor. Engine-ul nu poate identifica singur dacă un registru este sintetic sau real. Schimbarea acestei politici modifică hash-ul legat de contract și invalidează contractele vechi, chiar dacă valoarea nouă ar fi permisă sintactic.

`ROOT/06_REGISTRU/agents.json` păstrează forma fără câmp nou de versiune:

```text
{agents: [{agent_id: UUID, role: string, kind: "producer" | "auditor", active: boolean}]}
```

UUID-urile sunt canonice, cu litere mici, nenule. `active` reprezintă autorizarea din registru, nu starea runtime; lifecycle se ține separat. Rolul main `P-MANAGER`, `kind: producer`, este permis. Registrul rămâne autoritatea locală și nu autentifică persoana care a scris un raport.

Registrul `ROOT/06_REGISTRU/deliverables.json` are exact:

```text
{
  schema_version: 2,
  deliverables: [{
    id, version_id, stage, status,
    files: [{path, sha256}],
    evidence_files: [{path, sha256}],
    producer_agent_ids: [UUID],
    required_audit_roles: [role, ...],
    dependencies: [deliverable_ID, ...],
    requirements: {min_prose_words?, prose_paths?},
    criteria: [{id, weight}],
    contract: {path, sha256},
    audits: [relative_JSON_path, ...],
    meta_audit?: relative_JSON_path
  }]
}
```

Aceasta este notație de schemă, nu un manifest real și nu un raport de audit. `version_id` este șir necomplet gol. Un ID are o singură intrare în registru; versiuni care trebuie să coexiste folosesc ID-uri de înregistrare distincte. Schimbarea versiunii la același ID invalidează părintele care avea contractul anterior. `files` este nevidă, `evidence_files` este obligatorie și poate fi `[]`; listele sunt disjuncte și nu pot conține aliasuri ale aceluiași fișier. Dependențele rămân ID-uri în registru; contractul extras le fixează suplimentar versiunea și hash-ul contractului.

`requirements` poate fi `{}`. Nu se deduce roman final din `stage` sau `status`. Pentru proză se declară explicit `prose_paths`; dacă apare `min_prose_words`, acesta este întreg >=50000 și necesită `prose_paths`. Dacă există numai `prose_paths`, pragul este 50000. `meta_audit` este obligatoriu la validarea livrabilului dacă politica îl cere; pentru pregătirea contractului, audituri și metaaudit pot lipsi încă.

### Contractul înghețat

Fișierul referențiat prin `contract` conține exact:

```text
{
  schema_version: 2, deliverable_id, version_id, stage,
  files, evidence_files, producer_agent_ids, required_audit_roles,
  requirements, criteria,
  dependencies: [{deliverable_id, version_id, contract: {path, sha256}}],
  policy: {path: "00_CONDUCERE/policy.json", sha256}
}
```

Engine-ul compară întregul obiect cu proiecția intrărilor curente din registru și cu hash-ul politicii citite. Verifică digestul octeților reali ai contractului și toate contractele dependente recursiv. Nu este suficient ca noua dependență să aibă audit separat favorabil: auditul și metaauditul părintelui trebuie să fixeze noul contract al părintelui.

Contractul nu conține `status`, `audits`, `meta_audit` sau propria referință `contract`. Acestea sunt în registrul operațional, fără recursie de hash. Propriul registru `06_REGISTRU/deliverables.json`, propriul contract și rapoartele JSON ale livrabilului nu pot deveni `files` sau `evidence_files`, nici prin symlink/hard link. Politica poate fi artefact, dar nu trebuie construită astfel încât să conțină un hash circular spre auditul care o evaluează.

Orice schimbare a octeților contractului, inclusiv spațierea JSON, schimbă digestul său. Ordinea listelor face parte din proiecția înghețată. Nu se efectuează completări, recalculări sau rescrieri de hash-uri în registre/rapoarte de către validator.

### Audit și metaaudit

Auditul v2 păstrează câmpurile inițiale și adaugă `version_id`, `contract`; extensia de integrare adaugă numai câmpul opțional `supplemental_evidence_files`:

```text
{schema_version: 2, audit_id, deliverable_id, version_id,
 contract: {path, sha256}, reviewer_agent_id, reviewer_role,
 files: [{path, sha256}],
 supplemental_evidence_files?: [{path, sha256}],
 criteria: [{id, score: integer_0_to_1000, weight,
             evidence: [{path, sha256, anchor}]}],
 findings: [{id, severity, status, location, description, remediation}],
 verdict: "PASS" | "RETURN", limitations: [string], reviewed_at: ISO8601}
```

Metaauditul v2:

```text
{schema_version: 2, deliverable_id, version_id,
 contract: {path, sha256}, reviewer_agent_id, reviewer_role: "A-QAMANAGER",
 audit_files: [{path, sha256}],
 supplemental_evidence_files?: [{path, sha256}],
 checks: [{id, passed: true, evidence: [{path, sha256, anchor}]}],
 findings: [], verdict: "PASS", reviewed_at: ISO8601}
```

Referința `contract` din fiecare raport trebuie să coincidă exact cu cea a livrabilului curent. Hash-urile din `audit_files` fixează octeții rapoartelor JSON curente. Check-urile minime sunt `independence`, `coverage`, `evidence`, `scoring`, `closure`, `version`; se admit check-uri suplimentare unice, toate cu literal boolean `true`. Check lipsă, duplicat, numeric în loc de boolean, constatare sau verdict diferit de PASS respinge metaauditul. Nu există scor literar de metaaudit și nici metaaudit infinit.

### Dovezi cu hash și suplimente proprii raportului

Fiecare dovadă are exact `{path, sha256, anchor}`. `anchor` este `""` pentru întregul fișier, `"#nume-ancoră"` sau `":L12-L18"`/`":L12-18"`/`":L12"`. Se verifică forma și ordinea capetelor intervalului, nu existența semantică a ancorei/liniei ori adevărul afirmației. Stringurile de dovadă r01 nu sunt convertite de engine.

La auditul obișnuit, `path` trebuie să existe în `files`/`evidence_files` din contract SAU în propriul `supplemental_evidence_files`. La metaaudit se pot cita în plus rapoartele primare din `audit_files`. Hash-ul din dovadă trebuie să coincidă cu declarația corespunzătoare și cu fișierul actual. Existența unei surse pe disc sau în raportul altui auditor nu o autorizează implicit. Meta nu moștenește suplimentele primare; le poate cita numai dacă le declară explicit și în propria listă, cu același hash actual.

`supplemental_evidence_files` este opțional exclusiv în audit/metaaudit v2: absența și `[]` sunt echivalente; `null`, listele malformate, hash-urile invalide, duplicatele și câmpurile suplimentare dintr-o referință resping. Contractul, registrul și criteriile nu primesc câmpuri noi prin această extensie. Rapoartele v2 existente fără suplimente rămân compatibile; v1 nu este acceptat tacit.

Fiecare supliment declarat este citit și verificat la SHA-256, inclusiv dacă nu apare în nicio dovadă. Nu poate redeclara o cale deja disponibilă raportului, nici cu același hash; nu poate înlocui sursa prin alias/symlink/hard link. Două intrări suplimentare pentru același fișier fizic resping. Propriul JSON, JSON-urile celorlalte audituri ale livrabilului, metaraportul, contractul propriu și registrul operațional `deliverables.json` sunt interzise ca suplimente, inclusiv prin alias. Căile externe sau nedeclarate resping. Același fișier poate fi declarat explicit de rapoarte diferite, dar fiecare hash trebuie să corespundă acelorași bytes actuali; un hash contradictoriu nu poate trece.

`files` și `evidence_files` rămân sursele primare ale produsului, fixate înainte de audit. Ele nu pot fi mutate în suplimente pentru a evita fixarea în contract. `files` din audit trebuie să acopere în continuare exact întregul bundle. Suplimentele sunt pentru probe produse de auditor ulterior: MD-ul propriu, jurnalul testelor sale etc.; nu se adaugă la volumul de proză. Engine-ul verifică declarațiile și integritatea, nu poate clasifica semantic originea unui fișier.

Toate sursele contractuale și suplimentele sunt copiate automat la arhivare, inclusiv cele necitate. `--extra` nu autorizează o referință probatorie nedeclarată și nu înlocuiește fixarea hash-ului în contract sau în raport.

### Ordinea normală de lucru și legătura de hash

1. Producătorul finalizează produsul și intrările sale în `files`/`evidence_files`, fixează dependențele și îngheață contractul. MD-urile și jurnalele viitoare ale auditorilor nu sunt intrări artificiale ale produsului și nu sunt necesare la extragere.
2. Fiecare auditor independent verifică același contract. Își finalizează MD-ul/jurnalele, calculează hash-urile lor și finalizează propriul JSON, declarându-le în `supplemental_evidence_files`. MD-ul poate cita contractul deja înghețat, dar NU conține digestul propriului JSON. JSON-ul fixează MD-ul, nu invers.
3. După finalizarea tuturor JSON-urilor primare, A-QAMANAGER verifică rapoartele și sursele. Își finalizează MD-ul/jurnalele, apoi JSON-ul meta: `audit_files` fixează hash-urile JSON-urilor primare; propriul `supplemental_evidence_files` fixează MD-ul/jurnalele meta. MD-ul meta poate cita contractul și digesturile JSON-urilor primare, dar NU digestul propriului JSON meta.
4. Validatorul verifică fiecare legătură și bytes actuali, pe lângă toate celelalte condiții. Arhivatorul copiază sursele, rapoartele și suplimentele; indexul fixează hash-ul fiecărei copii, inclusiv al JSON-ului meta. Sidecar-ul fixează indexul. Nu se introduce un metaaudit infinit.

Legătura verificabilă este: contract → produs/intrări/dependențe; audit JSON → contract + suplimente proprii; meta JSON → contract + audit JSON-uri + suplimente proprii; index snapshot → toate copiile. Nici contractul, nici raportul nu se autohashează. Schema interzice referințele circulare directe descrise mai sus; engine-ul nu interpretează textul MD pentru a certifica absența oricărei circularități inventate de operator și nu certifică adevărul probelor.

După fixare, suplimentele nu se editează pe loc. O modificare a unui supliment primar invalidează auditul; un JSON primar refăcut invalidează hash-ul fixat de meta și cere metaaudit nou. O modificare a suplimentului meta invalidează metaauditul și cere raport meta nou. Se păstrează versiunile respinse și se folosesc runde noi de arhivă. Contractul produsului nu trebuie refăcut dacă produsul și intrările sale au rămas identice. Un MD preexistent poate rămâne intrare în `evidence_files`, dar atunci este înghețat ca intrare de produs, iar schimbarea lui cere contract nou; nu este fluxul obligatoriu pentru MD-ul auditorului.

## Extragerea contractului exact pentru auditori

API disponibil în `gatekeeper.py`:

```python
extract_contract(root, deliverable_id) -> bytes
validate(root, deliverable_id) -> dict
```

CLI, din 04_INSTRUMENTE după integrare:

```powershell
python -B gatekeeper.py --root "ROOT_DE_TEST_SAU_PREGATIRE" --deliverable SYS-001 --extract-contract
python -B gatekeeper.py --root "ROOT_DE_TEST_SAU_PREGATIRE" --deliverable SYS-001 --json
```

`--extract-contract` emite numai octeții UTF-8 ai contractului, cu un LF final, pe stdout binar. Nu creează fișiere, rapoarte, scoruri sau aprobări. La eroare: stdout gol, diagnostic pe stderr, exit 2. La reușită: exit 0, care înseamnă numai extragere. Opțiunea are prioritate față de `--json`.

Pentru prima pregătire, propria referință `contract` din registrul v2 trebuie să fie sintactic validă; hash-ul poate fi temporar 64 de zerouri, iar fișierul propriu poate să nu existe. Numai API-ul de extragere admite acest bootstrap. Artefactele și dovezile trebuie să aibă hash-uri corecte, iar dependențele trebuie să aibă deja contracte înghețate și coerente; auditurile lor nu sunt necesare pentru simpla extragere. Validarea pentru acceptare nu acceptă placeholder-ul.

Exemplu de utilizare API pentru operator, după mandatul său de integrare, nu operație executată asupra registrelor reale în acest staging:

```python
from pathlib import Path
import hashlib
import gatekeeper

root = Path(r"D:\ROOT_DE_PREGATIRE")
data = gatekeeper.extract_contract(root, "SYS-001")
destination = root / "06_REGISTRU/CONTRACTE/SYS-001-r02.json"
# Directorul există deja; destinația trebuie să fie fișier nou.
with destination.open("xb") as stream:
    stream.write(data)
print(hashlib.sha256(data).hexdigest())
```

Operatorul înregistrează separat calea și digestul fișierului nou în `contract`, apoi auditorii folosesc aceeași referință. Pe Windows PowerShell evitați redirecționarea text care poate schimba encoding-ul sau terminatorul de linie; API-ul de mai sus păstrează exact bytes. Contractele se pregătesc începând cu dependențele. Nu se face hash pe întregul registru pentru a înlocui contractul și nu se adaugă ulterior digestul propriului audit în contract.

## Validatorul și condițiile păstrate

CLI de validare: `python -B gatekeeper.py --root ROOT --deliverable ID [--json]`. Exit 0 numai pentru `passed: true`, exit 2 pentru respingere. Rezultatul v2 are exact:

```text
{schema_version: 2, deliverable_id, version_id, contract,
 passed, errors, weighted_scores, word_count, checked_files, dependencies}
```

`version_id` și `contract` pot fi `null` la erori anterioare identificării versiunii. `dependencies` conține recursiv rezultate cu aceeași formă. `checked_files` reprezintă artefactele citite, cu hash observat; la refuz poate fi parțial. Dovezile/contractele sunt verificate separat și sunt indexate în arhivă. `weighted_scores` este doar aritmetica scorurilor furnizate în audit, nu notare produsă de engine. Media nu compensează un criteriu <=950. Metaauditul nu adaugă scor.

Se păstrează cumulativ: fiecare criteriu strict >950; ponderi finite pozitive cu sumă exactă 100; criterii și bundle fără lipsuri, adaosuri sau duplicate; doi auditori autorizați distincți, câte un auditor separat pentru fiecare rol cerut; niciun producător drept auditor; A-QAMANAGER separat de producători și auditorii livrabilului; toate dependențele trecute curent și fără cicluri. `status: PASS` sau `RELEASED` nu acordă acceptare. Numerele booleene, scorurile fracționare și NaN/Infinity resping. `audit_id` este unic în graful verificat; același auditor poate evalua livrabile diferite.

În auditul obișnuit, numai stările `closed`/`resolved`, indiferent de majuscule, înseamnă constatare închisă; orice altă stare respinge indiferent de severitate. `reviewed_at` cere ISO8601 cu secunde și fus orar. Limitările textuale nu sunt evaluate semantic. `active` nu se confundă cu lifecycle.

Căile sunt relative la ROOT. Sunt refuzate inclusiv căile absolute din interior, `..`, `.`, segmente goale, drive-uri, fluxuri NTFS, caractere de control și segmente cu spații marginale sau punct final. Rezolvarea reală trebuie să rămână în ROOT. Se refuză evadarea prin symlink/junction și dublarea bundle-ului prin aliasuri/hard link-uri. Nu se face inventariere recursivă de directoare.

### Numărarea prozei și Setext

Proza trebuie declarată explicit în `prose_paths`, să fie în `files` și să fie UTF-8 `.md`/`.txt`. Fiecare fișier se numără o dată; BOM UTF-8 este ignorat, NUL binar și UTF-8 invalid resping. După eliminarea comentariilor HTML, inclusiv a restului unui comentariu neînchis, aceeași trecere identifică titlurile ATX și Setext simple pentru verificarea etichetelor și excluderea din numărătoare.

Titlurile `Sinopsis`, `Synopsis`, `Outline`, `Chapter plan(s)` și `Plan de capitole`/variantele implementate cer `HUMAN_REVIEW`, inclusiv când un Setext apare după un titlu introductiv. Titlurile ordinare sunt excluse; textul rămas se împarte prin `str.split()`. 49.999 tokenuri resping, 50.000 trec condiția de volum. Dialogul este inclus, iar punctuația separată prin spații contează ca token conform regulii simple.

Aceasta nu este clasificare semantică și nici parser Markdown complet. Metadatele YAML, codul, listele, citatele și alte marcaje neselectate pot conta dacă operatorul le pune în `prose_paths`. Operatorul păstrează numai narațiune; auditorul decide dacă un text nemarcat este plan sau sinopsis. P19 (tab) și P20 (Setext multilinie) rămân limite/observații exploratorii, nu noi constatări închise prin F04.

## Arhivare strictă și conservare explicită a respingerii

```powershell
python -B archive_round.py --root "ROOT" --deliverable SYS-001 --round r02-before-audit --extra "mandate/prompt.txt"
python -B archive_round.py --root "ROOT" --deliverable SYS-001 --round r02-after-audit --result "rezultate/gate.json" --extra "masuri/plan.md"
python -B archive_round.py --root "ROOT" --deliverable SYS-001 --round r02-incident-hash --preserve-rejected --result "rezultate/return-original.json" --extra "masuri/plan.md"
```

Acestea sunt exemple: căile trebuie să existe și operatorul folosește ID-uri/versiuni autorizate. `--result` este cale de fișier relativă la ROOT, nu JSON inline; `--extra` este repetabil pentru fișiere, nu directoare. ID și round: 1–100 caractere ASCII alfanumerice/`._-`, început alfanumeric, fără punct final/nume Windows rezervat. Nicio rundă existentă, inclusiv una incompletă, nu se reutilizează.

API: `archive(root, deliverable_id, round_id, result_path=None, extras=(), preserve_rejected=False)`.

### Modul strict

Verifică contractele v2, hash-urile declarate ale artefactelor/dovezilor, referințele contractuale și probele din rapoarte, bundle-urile exacte și hash-urile metaraportului dacă este declarat. Nu cere scoruri favorabile sau constatări închise ca să păstreze un raport coerent: un RETURN cu surse intacte se poate arhiva. Nu este un al doilea validator editorial și nu certifică verdictul rezultatului furnizat. Pentru rezultat cere forma v2, ID-ul corect, `passed` boolean și același contract/versiune. Un raport v1 nu este tratat ca raport v2.

Include registrul și politica exact ca octeți, contractele, artefactele, `evidence_files`, auditurile, metaraportul dacă este declarat, toate `supplemental_evidence_files` primare/meta, extras și rezultatul. Dependențele sunt incluse tranzitiv. O sursă contractuală sau suplimentară lipsă ori schimbată refuză captura strictă înainte de scrierea rundei. Nu cere `--extra` pentru surse din contract sau suplimente declarate. O cale declarată de mai multe rapoarte este copiată o singură dată în `sources`; declarațiile originale rămân în rapoarte.

### `--preserve-rejected`

Necesită rezultat original JSON lizibil, cu ID-ul cerut, literal `passed: false` și erori necomplet goale. Necesită registru de livrabile parsabil și ID neambiguu, pentru identificarea manifestului declarat. Nu acceptă un rezultat PASS sau numărul 0 în loc de boolean false. Registrele și rezultatele istorice v1 pot fi păstrate în acest mod ca documente, fără migrare și fără acceptare ca v2.

Păstrează manifestul și rapoartele originale, bytes disponibili și rezultatul original. Include automat și suplimentele declarate în rapoarte, inclusiv cele necitate. Nu recalculează hash-urile din declarațiile istorice. Pentru un supliment schimbat, digestul pretins de JSON rămâne separat de digestul bytes observați; o sursă lipsă nu este inventată. Fiecare observație are:

```text
{source_path, claim_source, declared_sha256, observed_sha256,
 copied_path, availability, diagnostics: [{code, detail}]}
```

`declared_sha256` este valoarea primită, chiar dacă e invalidă. `observed_sha256` descrie exact bytes copiați, nu cei pretins auditați. Când sursa lipsește, e ilizibilă sau nesigură, `observed_sha256` și `copied_path` sunt `null`; nu se inventează fișiere sau digesturi. Diagnosticele includ `HASH_MISMATCH`, `HASH_INVALID`, `MISSING_OR_UNREADABLE`, `UNREADABLE`, `UNSAFE_PATH`, `SCHEMA_INVALID`, `UNPINNED_EVIDENCE` pentru stringurile r01 și lipsa dependențelor/contractelor istorice. Declarații vechi și curente contradictorii rămân observații separate, cu sursa fiecărei afirmații.

Nu urmărește căi spre exterior și nu ingerează vechiul arbore `08_ARHIVA`; consemnează refuzul în observații. Un raport JSON malformat poate fi copiat ca bytes, dar referințele lui nu sunt ghicite. `declaration_traversal_complete: false` semnalează că declarațiile nu au putut fi parcurse complet; `observed_availability: PARTIAL` semnalează surse indisponibile. `AVAILABLE` nu înseamnă aprobare sau autenticitate. Indexul are `archive_kind: rejected_evidence_snapshot`, `source_consistency: NOT_CERTIFIED`, `supplied_result_verdict: RETURN` și `editorial_approval_issued: false`.

Chiar dacă operatorul a fabricat rezultatul de respingere, acest mod îl păstrează numai ca declarație furnizată; nu îl autentifică. Nu conferă PASS la restaurare. O arhivă RETURN/HASH poate fi integră ca snapshot și neconformă cu manifestul în același timp.

### Structura și verificarea capturii

```text
08_ARHIVA/<ID>/<ROUND>/
  manifest.json
  dependency_manifests/...
  sources/<căi ROOT-relative ale documentelor și copiilor>
  result.json                 (dacă a fost furnizat)
  index.json
  index.sha256
```

Registrele/rapoartele/sursele se copiază octet cu octet. `manifest.json` este extragerea obiectului din registru, reserializată fără pierdere de valoare numerică; registrul original exact rămâne în `sources`. În conservarea respingerii, numele fișierelor de manifeste dependente folosesc hash-ul ID-ului pentru a nu transforma un ID nesigur într-o cale. ID-ul original rămâne în manifest.

Indexul v2 enumeră fiecare copie prin `path`, `sha256`, `size_bytes`, `kind` și, unde este cazul, `source_path`. Sidecar-ul conține SHA-256 al octeților `index.json` și este scris ultimul. Indexul/sidecar-ul nu se autohashează. Rezultatul CLI de arhivare are `archived`, `snapshot_path`, `index_sha256`, `files_archived`, `editorial_approval_issued: false`, fără câmp `passed`. Exit 0 indică finalizarea capturii, nu acceptarea editorială; exit 2 indică refuz/eșec.

Verificarea independentă trebuie să compare digestul indexului cu sidecar-ul și, preferabil, cu un digest păstrat separat, apoi SHA-256 și lungimea fiecărei intrări. Se verifică și căile înainte de citire. O captură este completă la nivel de scriere numai când perechea index/sidecar și copiile se verifică; observațiile pot indica în continuare surse lipsă ori neconforme.

Nu se suprascrie nimic. O eroare în timpul scrierii lasă runda parțială, fără ștergere/reutilizare automată; se cere un ID nou. Sursele citite sunt reverificate înainte și după copiere. Nu există WORM, semnături, timestamp certificat sau jurnal global hash-chained. Operatorul local poate altera registrele, fișierele, indexurile și recalcula hash-urile. Digestul nu autentifică autorul și nu certifică adevărul. Citirile nu sunt snapshot atomic al filesystem-ului; sursele trebuie menținute stabile. Nu există protecție absolută contra unui operator privilegiat care schimbă directoare între controale ori contra pierderii alimentării.

## Migrare și retestare

1. Păstrați r01 și arhivele sale, inclusiv `r01-primary-complete`, nemodificate. Nu convertiți rapoartele r01 prin schimbarea cifrei de versiune și nu copiați scoruri drept reevaluare.
2. După mandatul de integrare, main aliniază politica/registrul v2, cerințele, dovezile și modelele de audit/metaaudit. În staging nu s-a modificat niciun registru real.
3. Pregătiți produsul și intrările primare stabile, extrageți contractele începând cu dependențele, salvați bytes și înregistrați digesturile. Orice placeholder trebuie înlocuit înainte de validare. Nu așteptați MD-urile viitoare ale auditorilor pentru această înghețare.
4. Auditorii produc MD/jurnale și rapoarte reale r02 cu `version_id`, `contract`, probe structurate cu hash și, când este necesar, propriul `supplemental_evidence_files`; apoi A-QAMANAGER produce MD/JSON meta pe exact acei octeți. Respectați ordinea și legăturile din secțiunea de mai sus. Engine-ul nu completează aprobări lipsă.
5. Arhivați rundele și rezultatele, apoi auditorul competent decide închiderea celor patru constatări. Blocajul G01, selecția Boucher/Dubois și manuscrisul nu se rezolvă prin aceste teste tehnice.

Rularea întregii suite, din `r02_staging`:

```powershell
python -B -m unittest -v test_gatekeeper.py test_archive_round.py
```

`-B` evită cache-ul de import. Fixture-urile istorice au fost adaptate explicit la schema v2; funcțiile de construcție/reaprobare din teste sunt strict sintetice. Noile regresii folosesc `persist(freeze=False)` după schimbarea adversarială, ca să nu actualizeze automat contractele sau auditurile și să ascundă defectul. P10 verifică explicit identitatea bytes a rapoartelor vechi. Probele au controale pozitive valide v2, astfel încât un refuz generic de schemă nu poate fi raportat drept remedierea funcțională a defectului.

Rezultat efectiv TEST pentru extensia opțională, 2026-09-24, Python 3.12.10: `python -B -m unittest -q test_gatekeeper.py test_archive_round.py` — **233 teste în 18,937 s, OK, exit 0, fără omisiuni**. Cele 196 de teste precedente sunt păstrate, plus 26 de regresii de validator și 11 de arhivare. Nu s-a emis audit literar și nu s-a închis nicio constatare de către producător.

Regresiile suplimentare acoperă fluxul produs înghețat → audituri → meta fără schimbarea bytes ai contractului/registrului, suplimente valide sau modificate (inclusiv necitate), surse nedeclarate și separarea surselor între rapoarte, autoreferințe/aliasuri/override, menținerea pragului de proză, captură automată, restaurare din `snapshot/sources` fără sursele originale și conservare RETURN/HASH cu declarații intacte. După restaurare se verifică întâi indexul și copiile, apoi se poate rula `validate(snapshot / 'sources', ID)`; o captură de respingere nu devine PASS prin restaurare.

Raportul tehnic din `06_REGISTRU/MASURI` rămâne documentul anterior extensiei și nu este actualizat în această intervenție limitată la staging. Pe sisteme fără permisiuni pentru symlink/hard link, testele respective anunță explicit omisiunea; nu sunt considerate executate. La rularea de mai sus nu a fost omis niciun test.


## Dovezi ale integrării curente
Raportul SYS-001-tehnic-rezultate-r02.md descrie baza v2 de 196 teste, înaintea extensiei pentru probe ale auditorilor. Predarea finală exactă P-SYSTEMS (233 teste, 196 + 37) este în 06_REGISTRU/ISTORIC/P-SYSTEMS-predare-finala-r02.json. Rezultatul rulării pe fișierele live integrate este în 06_REGISTRU/TESTE_CONFIGURARE_r02.txt; raportul de integrare al coordonatorului separă aceste momente. Niciun rezultat sintetic nu este audit editorial. Pentru capturarea mesajelor vezi 06_REGISTRU/README_EXPORT.md și testele sale, separate de această suită.

## Regula r03 — probe din arhive anterioare

Nu declarați căi din 08_ARHIVA în evidence_files sau supplemental_evidence_files ale rapoartelor curente: arhivatorul interzice ingestia arhivelor vechi. Pentru verificarea unui index anterior folosiți o copie plată, byte-identică, păstrată în afara 08_ARHIVA, cu proveniență și SHA-256; declarați copia în contract sau în propriul supliment. Menționarea unei arhive în text nu o transformă în probă arhivabilă.

Rapoartele r02 originale care au provocat OBS-MANAGER-002 rămân păstrate; revizia de ambalare v02 folosește copii plate fără schimbarea concluziilor semantice. Într-o rundă nouă se verifică atât validarea porții, cât și arhivarea și recuperarea efectivă înaintea autorizării etapei următoare.
