# SYS-001 — Plan de măsuri după auditul A-SYSTEMS r01

Data: 2026-09-24. Autor și responsabil tehnic: P-SYSTEMS. Starea tuturor măsurilor: **PLANIFICAT**. Livrabil vizat: SYS-001 / G00. Destinația corecțiilor propuse: o versiune nouă pentru r02, numai după arhivarea r01 și mandat separat de editare.

Acest document este numai un plan. Nu schimbă produsul înghețat, manifestul, registrele operaționale, rapoartele r01, scorurile, constatările sau verdictul auditorului. Metaauditul r01 trebuie să poată continua pe aceeași versiune înghețată. Nu declară implementări, retestări, închideri sau aprobări realizate. Nu conține note ori scoruri noi.

## 1. Baza documentară și identificarea versiunii

Surse citite integral:

- `05_AUDIT/SYS-001/A-SYSTEMS-r01.json`, audit ID `AUD-SYS-001-A-SYSTEMS-r01`, verdict `RETURN`, `reviewed_at: 2026-09-24T01:09:09.1165470Z`.
- `05_AUDIT/SYS-001/A-SYSTEMS-r01.md`, inclusiv secțiunile `#probe-results`, `#reproduction` și `#hash-verification`.

Auditorul înregistrat în raport: A-SYSTEMS, UUID `01a0d0ee-a18e-78a1-a069-9e87df0efc87`. Planul păstrează cele patru ID-uri de finding și severitățile din JSON. Starea lor în audit rămâne `open`; `PLANIFICAT` descrie numai măsurile de mai jos.

SHA-256 citite efectiv la pregătirea acestui plan:

| Fișier | SHA-256 |
| --- | --- |
| `05_AUDIT/SYS-001/A-SYSTEMS-r01.json` | `a825a5db3032848664851c345440a795f8870545617af85f8e3ed915efa97d4a` |
| `05_AUDIT/SYS-001/A-SYSTEMS-r01.md` | `a1a8657f7c9c6236d23c334a724ed2c5a562a59392a0119937b6a47edbfff95f` |
| `04_INSTRUMENTE/gatekeeper.py` | `c63140cb773b101f90bdca7858baadb31edbef99de894ab93ad39a08d4724145` |
| `04_INSTRUMENTE/archive_round.py` | `2c6f3d39a717765e03595bd535b3ad8dcbaf52cf22f5bc40e5c7050fdc514031` |
| `04_INSTRUMENTE/README.md` | `d0426ea6fe4ce159370ca06128190b53253d571d5bc8f5f4d12f344f81278a9a` |

Cele trei hash-uri de produs de mai sus corespund valorilor din raportul r01. Aceasta este o verificare prin citire pentru ancorarea planului, nu o nouă verificare integrală a celor 61 de artefacte și nu un metaaudit.

Auditorul consemnează 151 teste existente trecute și 23 de probe suplimentare. Acestea sunt rezultate istorice din r01; unele probe demonstrează defecte. Nu reprezintă rezultate de închidere pentru măsurile propuse. În acest mandat nu se rulează probele, nu se schimbă fixture-urile și nu se creează rezultate de retest.

## 2. Acoperirea constatărilor

| Finding exact | Severitate din audit | Probe ale auditorului | Măsură | Stare măsură |
| --- | --- | --- | --- | --- |
| SYS-A-SYSTEMS-r01-F01 | high | P10-dependency-v2-parent-v1 | Fixarea contractului și a versiunilor dependente în audit și metaaudit | PLANIFICAT |
| SYS-A-SYSTEMS-r01-F02 | high | P11-evidence-drift; P23-external-evidence-recovery; control P22 | Fixarea prin hash și conservarea tuturor surselor probatorii | PLANIFICAT |
| SYS-A-SYSTEMS-r01-F03 | high | P12-stale-return-archive; control P13 | Conservarea explicită a respingerii, cu declarații și observații separate | PLANIFICAT |
| SYS-A-SYSTEMS-r01-F04 | medium | P21-later-Setext-synopsis | Aceeași identificare ATX/Setext pentru etichete și numărare | PLANIFICAT |

### SYS-A-SYSTEMS-r01-F01 — Contractul și dependențele nefixate

**Probă și localizare.** JSON: `findings[id=SYS-A-SYSTEMS-r01-F01]`. MD: constatarea F01 și proba P10, funcția de reproducere `dependency_retarget`. Localizare principală indicată de auditor: `04_INSTRUMENTE/gatekeeper.py:L295-L325`; suplimentar `L352-L375`, `L442-L459`. Proba consemnează `before=true`, `after=true`, `parent_reports_and_meta_unchanged=true`, după înlocuirea dependenței `source-v001` cu `source-v002`, deși noua sursă spune contrariul celei vechi.

**Cauză.** Auditul fixează fișierele și criteriile părintelui, dar nu întreaga declarație de intrare și identitatea versiunilor dependente. Metaauditul fixează rapoartele, care nu conțin această legătură. Verificarea separată a dependenței noi nu dovedește reevaluarea relației părinte–sursă.

**Corecție concretă planificată.** Introducerea contractului de intrare v2 descris în secțiunea 3. Fiecare audit și metaaudit trebuie să declare aceeași referință `{path, sha256}` la contract. Contractul fixează inclusiv versiunea părintelui, cerințele, rolurile, producătorii, criteriile, artefactele și fiecare dependență prin ID, versiune și hash al contractului dependent. Engine-ul compară declarația curentă cu contractul, verifică digesturile și parcurge recursiv dependențele. Schimbarea oricărei intrări legate de evaluare invalidează aprobarea veche a părintelui; nu se remediază prin simpla validare a copilului sau prin actualizarea numai a registrului.

**Responsabil.** P-SYSTEMS pentru schema executabilă, verificări și teste. P-MANAGER pentru actualizarea coordonată a registrelor, contractelor, documentației și mandatelor r02, după autorizare. A-SYSTEMS pentru retest independent; A-QAMANAGER pentru metaauditul rapoartelor r02, fără participare la producerea corecției.

**Test de închidere.** Reproducerea P10 se păstrează ca scenariu și se transpune în fixture-uri v2 fără a-i elimina schimbarea adversarială. Graful inițial complet valid trebuie să treacă. Înlocuirea dependenței cu una separat aprobată trebuie să dea `passed=false`, exit 2 și diagnostic de nepotrivire a contractului, cu rapoartele părintelui neschimbate. Refuzul trebuie să persiste și dacă se actualizează numai contractul/registrul părintelui, numai unul dintre audituri sau numai metaraportul. Acceptarea devine posibilă numai după audituri noi și metaaudit nou pentru contractul modificat. Se adaugă varianta cu același ID de dependență, dar octeți/contract schimbați, plus schimbarea unei cerințe sau a unui rol obligatoriu. Controlul pozitiv folosește întregul graf nemodificat.

**Impact.** Schimbare incompatibilă de schemă pentru fluxul de acceptare; rapoartele vechi nu mai pot autoriza r02. Afectează engine-ul, arhivarea contractelor, fixture-urile, documentația și modelele de audit/metaaudit. Nu impune modificarea conținutului vreunui manuscris sau traduceri în acest mandat.

**Rezultat așteptat.** Nicio aprobare a părintelui nu poate fi reutilizată pentru alt contract/dependență fără reevaluare independentă. **Stare: PLANIFICAT.**

### SYS-A-SYSTEMS-r01-F02 — Dovezi fără versiune fixată și recuperare incompletă

**Probă și localizare.** JSON: `findings[id=SYS-A-SYSTEMS-r01-F02]`. MD: F02, P11, P23 și controlul P22; funcțiile `evidence_drift`, `archive_evidence_recovery`, `archive_recovery`. Localizare indicată: `04_INSTRUMENTE/gatekeeper.py:L281-L293` și `04_INSTRUMENTE/archive_round.py:L125-L160`. P11 consemnează acceptare înainte și după schimbarea sursei citate, cu rapoarte identice. P23 consemnează eșec la recuperarea sursei neincluse; varianta cu `--extra` se recuperează, dar nu fixează retroactiv versiunea citită de auditor.

**Cauză.** Referința din `evidence` demonstrează numai că o cale există la verificare. Nici auditul, nici contractul nu fixează digestul acelei surse. Arhivarea copiază numai sursele enumerate, fără obligație verificată pentru toate dovezile citate.

**Corecție concretă planificată.** În v2, fiecare referință probatorie devine obiect explicit `{path, sha256, anchor}`; `anchor` este șir gol când nu se indică un fragment. Pentru auditul obișnuit, sursa trebuie să aparțină artefactelor ori listei `evidence_files` din contractul înghețat. Hash-ul din referință, cel din contract și cel al fișierului trebuie să coincidă. Pentru metaaudit, rapoartele citate sunt legate de `audit_files`, iar alte surse sunt legate de contract. Se interzice citarea propriului raport ca sursă în fluxul de acceptare, pentru a evita dependențe circulare de hash. Arhivatorul trebuie să includă automat reuniunea surselor declarate în contract și a rapoartelor/probelor referențiate explicit; nu face descoperire recursivă. `--extra` rămâne pentru materialele suplimentare, fără să înlocuiască obligația de legare a dovezilor.

**Responsabil.** P-SYSTEMS pentru validarea referințelor și completitudinea capturii. P-MANAGER pentru inventarul surselor contractuale și distribuirea modelului v2 către auditori. Auditorii r02 completează referințele și digesturile pe sursele efectiv evaluate; P-SYSTEMS nu le inventează. Retest: A-SYSTEMS; controlul rapoartelor: A-QAMANAGER.

**Test de închidere.** P11 adaptat v2 trebuie să treacă înaintea modificării, apoi să respingă după schimbarea exclusivă a sursei probatorii, fără modificarea rapoartelor. Lipsa digestului, digestul greșit, calea nefixată în contract, traversal și symlink-ul extern trebuie să respingă. P23 trebuie să producă o captură care conține exact sursa auditata și se revalidează folosind numai `snapshot/sources`, fără acces la ROOT-ul inițial. Dacă sursa lipsește ori s-a schimbat, modul strict trebuie să refuze precis captura pretins completă; conservarea incidentului urmează separat F03 și nu poate fi etichetată ca restaurare validă. P22 rămâne control pozitiv.

**Impact.** `evidence: [string]` din schema veche nu mai este acceptat tacit în r02. Va fi necesară actualizarea explicită a rapoartelor reale de către autorii lor. Snapshot-urile includ și sursele probatorii locale; dimensiunea lor poate crește. Hash-ul fixează octeții, dar nu certifică adevărul afirmației sau existența semantică a ancorei.

**Rezultat așteptat.** Orice derivă a unei dovezi invalidează acceptarea; fiecare captură declarată completă conține dovezile exacte necesare recuperării. **Stare: PLANIFICAT.**

### SYS-A-SYSTEMS-r01-F03 — RETURN/HASH nu poate fi conservat

**Probă și localizare.** JSON: `findings[id=SYS-A-SYSTEMS-r01-F03]`. MD: F03, P12, control P13; funcțiile `stale_return_archive` și `normal_return_archive`. Localizare indicată: `04_INSTRUMENTE/archive_round.py:L114-L137`. P12 consemnează `passed=false` pentru HASH, `archived=false` și inexistența directorului arhivei. Auditorul leagă problema de obligația AFTER_AUDIT din protocol. P13 confirmă că un RETURN cu hash-uri coerente se păstrează deja corect.

**Cauză.** Aceeași cerință de coerență este aplicată acceptării și conservării probelor unei respingeri. Refuzul intenționat al hash-urilor expirate împiedică păstrarea incidentului exact care a produs respingerea.

**Corecție concretă planificată.** Păstrarea modului strict și adăugarea unei opțiuni explicite, propusă `--preserve-rejected`, cu rezultat original de respingere obligatoriu. Separarea citirii sigure a surselor de verificarea conformității editoriale. Modul de conservare salvează nemodificat manifestul declarat, contractul disponibil, registrele/politica, rapoartele și rezultatul primit. Copiază octeții disponibili și consemnează pentru fiecare sursă: calea, hash-ul declarat, hash-ul observat calculat din octeții copiați, disponibilitatea și diagnosticul (`HASH_MISMATCH`, `HASH_INVALID`, `MISSING`, `UNREADABLE` sau `UNSAFE_PATH`, după caz). Valorile declarate nu se înlocuiesc cu cele observate. Pentru surse absente nu se inventează octeți ori SHA-256; se înregistrează explicit lipsa.

Indexul v2 separă integritatea copiilor de conformitatea surselor cu declarațiile. Hash-urile copiilor, ale rezultatului original și ale indexului trebuie să fie verificabile. Captura se marchează drept conservare a unei respingeri, cu disponibilitatea completă/parțială și `editorial_approval_issued: false`. Un rezultat r01 și un manifest v1 pot fi păstrate ca documente istorice, cu versiunea lor declarată; nu sunt reinterpretate ca aprobări v2. `RETURN`/`HASH` și orice metaraport respins rămân nealterate. O cale nesigură nu este urmată nici în acest mod: se conservă declarația și diagnosticul, fără citire în exterior. Sunt păstrate refuzul suprascrierii, indexarea tuturor copiilor, controlul schimbărilor din timpul citirii și semnalarea capturilor incomplete.

**Responsabil.** P-SYSTEMS pentru modul de conservare, schema indexului și teste. P-MANAGER pentru fluxul AFTER_AUDIT, includerea planurilor/rezultatelor și arhivarea efectivă după mandat. A-SYSTEMS verifică independent reproducerea; A-GOVERNANCE verifică concordanța cu protocolul, fără închidere declarată de producător.

**Test de închidere.** P12 trebuie să obțină în continuare `RETURN/HASH` din validator și refuz în modul strict. Cu opțiunea explicită de conservare, trebuie să rezulte o rundă nouă cu index verificabil, octeții disponibili și rezultatul original identic. Manifestul și rapoartele rămân identice cu cele anterioare capturii, cu hash-urile vechi intacte; indexul consemnează separat valoarea actuală diferită. Se verifică suplimentar lipsa unui artefact, lipsa unei dovezi, un hash declarat malformat, rezultat r01 păstrat fără promovare de schemă, sursă nesigură neaccesată și rundă existentă refuzată. P13 trebuie să rămână funcțional. Restaurarea unei capturi RETURN/HASH trebuie să păstreze respingerea ori diagnosticul incidentului, fără transformare în PASS.

**Impact.** Revizuire explicită a regulii prea înguste din README și a testului care respinge orice captură de hash expirat; modul strict rămâne verificabil separat. Indexul diferențiază două scopuri și nu mai permite confundarea integrității arhivei cu aprobarea produsului. Nu presupune WORM, semnătură externă sau autentificare antifals.

**Rezultat așteptat.** Respingerea și probele ei pot fi păstrate verificabil fără fraudarea manifestului, fără ascunderea lipsurilor și fără emiterea aprobării. **Stare: PLANIFICAT.**

### SYS-A-SYSTEMS-r01-F04 — Titlul Setext ulterior nu declanșează HUMAN_REVIEW

**Probă și localizare.** JSON: `findings[id=SYS-A-SYSTEMS-r01-F04]`. MD: F04, P21, funcția `later_setext_plan`. Localizare indicată: `04_INSTRUMENTE/gatekeeper.py:L419-L434`. Conținutul probei începe cu `# Manuscript`, apoi `Sinopsis` subliniat cu `========`, urmat de 50.000 tokenuri sintetice. Auditorul consemnează `passed=true`, `word_count=50000`, fără `HUMAN_REVIEW`.

**Cauză.** Lista de etichete verifică prima linie și titlurile ATX. Numărătorul recunoaște și elimină Setext într-un pas separat; titlul este exclus din număr, dar nu ajunge în verificarea etichetei.

**Corecție concretă planificată.** O singură extragere a titlurilor ATX și Setext simple, folosită atât pentru controlul etichetelor, cât și pentru excluderea titlurilor din numărătoare. Extragerea are loc după eliminarea comentariilor HTML și înaintea acceptării prozei. Toate titlurile Setext simple, indiferent de poziție, sunt verificate pentru etichetele documentate `Sinopsis`, `Synopsis`, `Outline`, `Plan de capitole` și variantele deja susținute de engine. Se păstrează regula de numărare prin whitespace și responsabilitatea auditului uman pentru conținutul nemarcat.

**Responsabil.** P-SYSTEMS pentru implementare, teste și precizarea regulilor din README. A-SYSTEMS pentru retest independent. Nu este sarcină de rescriere a manuscrisului sau de alegere a canonului.

**Test de închidere.** P21 adaptat numai la contractul v2 trebuie să dea `passed=false`, exit 2 și `HUMAN_REVIEW`. Se adaugă variante cu cele patru etichete după un titlu introductiv, subliniere `=` și `-`, plus control ATX echivalent. Un Setext obișnuit, fără etichetă de plan/sinopsis, trebuie exclus consecvent din numărătoare; 49.999 tokenuri narative resping și 50.000 trec condiția de volum. Comentariile HTML și dialogul păstrează comportamentul documentat. P19 și P20 rămân observații exploratorii ale auditorului, nu sunt prezentate ca alte findings și nu justifică extinderea la un parser Markdown general.

**Impact.** Corecție locală a consecvenței dintre detectarea etichetelor și numărare; modifică rezultatul numai pentru marcaje pe care regula documentată trebuia deja să le intercepteze. Nu pretinde clasificarea semantică a textului.

**Rezultat așteptat.** Un titlu Setext explicit de sinopsis/plan nu mai poate trece poarta de proză doar pentru că apare după alt titlu. **Stare: PLANIFICAT.**

## 3. Contractul tehnic v2 propus pentru r02

Aceasta este specificația de lucru a măsurilor F01/F02/F03, nu o schemă deja instalată și nu autorizație de schimbare în r01. Înaintea producerii rapoartelor reale r02, schema implementată, exemplele fără scoruri prefabricate și modelele de audit/metaaudit trebuie predate coerent către P-MANAGER și auditori.

### 3.1 Legarea intrărilor fără ciclu de hash

Se propune un document de contract de intrare separat, versionat, cu `schema_version: 2`. Identitatea sa este `{path, sha256}`, hash calculat pe octeții UTF-8 efectiv înghețați, nu pe o reserializare ulterioară. Nu se declară că două formatări JSON diferite au același digest. Nu se acceptă chei duplicate sau numere malformate; ponderile sunt comparate numeric exact.

Contractul conține exact setul de intrări care determină evaluarea:

| Câmp propus | Conținut fixat |
| --- | --- |
| `schema_version` | Întregul 2 |
| `deliverable_id`, `version_id`, `stage` | Identitatea livrabilului, versiunea și etapa evaluată |
| `files` | Lista completă `{path, sha256}` a artefactelor |
| `producer_agent_ids` | Producătorii versiunii |
| `required_audit_roles` | Rolurile necesare, fără relaxare ulterioară |
| `requirements` | Cerințele exacte, inclusiv pragul și căile prozei unde sunt aplicabile |
| `criteria` | ID-urile și ponderile exacte |
| `dependencies` | Lista `{deliverable_id, version_id, contract: {path, sha256}}` |
| `evidence_files` | Surse probatorii suplimentare `{path, sha256}`; poate fi goală |
| `policy` | Referință `{path, sha256}` la politica aplicabilă înghețată |

Registrul v2 conține versiunea și referința la contract pentru fiecare livrabil; dacă păstrează și câmpurile descriptive ale contractului, engine-ul impune egalitate, nu alege arbitrar una dintre declarațiile contradictorii. Statusul operațional și lista rapoartelor produse ulterior sunt păstrate separat de contractul de intrare. Ele nu sunt probe de acceptare. Contractul nu include hash-urile propriilor audituri/metaauditului, fiind anterior acestora; astfel se evită cercul contract → audit → contract. Politica înghețată nu primește la rândul ei un hash către raportul care o evaluează.

Auditul v2 păstrează verificările existente și adaugă `version_id` și `contract: {path, sha256}`. Probele criteriilor sunt obiectele explicite din F02. Metaauditul v2 conține aceeași identitate de versiune și aceeași referință la contract, lista exactă `audit_files` cu hash-urile rapoartelor curente și check-urile obligatorii `independence`, `coverage`, `evidence`, `scoring`, `closure`, `version`. Probele metaauditului au aceeași formă cu hash. El nu adaugă scoruri literare și nu cere metaaudit infinit.

Ordinea verificării propuse: schema și autorizarea → contractul și politica referențiate → intrările/dependențele și sursele probatorii → auditurile părintelui → metaauditul exact al acelor rapoarte → reverificarea surselor citite. O dependență nouă validă nu repară automat referințele vechi ale părintelui. `active` rămâne autorizare, nu stare runtime; un auditor `completed`/`closed` nu își pierde auditul istoric numai din acest motiv. Nu se introduce în acest plan autentificare externă a registrelor.

### 3.2 Trecere explicită de la v1 la v2

- Politica, registrul de livrabile, contractul, auditurile, metaauditurile și indexul de arhivă pentru noul flux își declară explicit versiunea 2. Anvelopa rezultatului v2 declară de asemenea versiunea și referința la contract; actualizarea ei și a consumatorului `--result` se face coordonat, nu prin schimbarea ascunsă a câmpurilor. Registrul de agenți își păstrează semantica și câmpurile existente, fiind un control de autorizare separat.
- Engine-ul r02 respinge v1 în fluxul de acceptare și respinge absența versiunii, câmpurile noi lipsă, referințele probatorii vechi de tip string, amestecul audit v2/metaaudit v1 și versiunile necunoscute. Diagnosticul trebuie să precizeze fișierul și necesitatea migrării/reauditării, fără completare automată de hash-uri sau presupunerea unor aprobări.
- Rapoartele r01 se păstrează nemodificate ca istoric. Nu se convertesc prin simpla schimbare a `schema_version`, nu se copiază scoruri în rapoarte noi ca și cum ar fi fost reevaluate și nu se atașează retroactiv un contract pretins citit de auditor. Arhivarea explicită a respingerii poate păstra documente v1 ca octeți istorici, fără a le accepta drept v2.
- Contractele, registrele, README și modelele din `03_MODELE` se aliniază înaintea redactării rapoartelor reale r02. P-MANAGER distribuie modelul exact; A-SYSTEMS și A-GOVERNANCE își produc independent rapoartele r02 pe noua versiune înghețată, apoi A-QAMANAGER produce metaauditul pe octeții finali ai acelor rapoarte. P-SYSTEMS pregătește compatibilitatea tehnică, fără să producă în locul lor rapoarte, scoruri sau aprobări.
- Testele sintetice v2 acoperă schema completă, iar intrările v1 rămân cazuri negative pentru acceptare și cazuri de păstrare istorică în arhivă. Comportamentele de închidere P10/P11/P12/P21 se testează pe date v2 valide, pentru ca refuzul generic de schemă să nu fie confundat cu remedierea defectului.

Pragul strict >950 per criteriu, doi auditori independenți pentru rolurile cerute, separarea A-QAMANAGER, probele obligatorii, refuzul constatărilor deschise, hash-urile bundle-ului, ciclurile și siguranța căilor rămân condiții cumulative. Setarea de producție `require_meta_audit` rămâne `true`. Nicio parte a migrării nu relaxează aceste reguli.

## 4. Ordinea executării după mandat și închiderea independentă

1. **PLANIFICAT — P-MANAGER:** finalizează fluxul r01 pe versiunea înghețată și conservă artefactele, rapoartele reale JSON/MD, metaauditul, rezultatul și acest plan prin procedura autorizată. Nu se declară aici că AFTER_AUDIT a fost deja arhivat. Dacă se întâlnește F03 în produsul înghețat, nu se corectează hash-urile istorice ca să treacă arhivatorul; coordonatorul stabilește separat conservarea incidentului. Planul nu acordă mandat de editare pentru a ocoli acest pas.
2. **PLANIFICAT — P-MANAGER:** emite mandat separat pentru versiunea nouă, după arhivare. P-SYSTEMS nu începe implementarea înaintea acestui mandat.
3. **PLANIFICAT — P-SYSTEMS și P-MANAGER:** stabilesc și documentează coerent schema v2, contractele și modelele, apoi implementează F01/F02, F03 și F04 în noua versiune. Mențin accesibilă versiunea înghețată r01 și istoricul rapoartelor.
4. **PLANIFICAT — P-SYSTEMS:** rulează testele de închidere și regresie numai cu `TemporaryDirectory`, fără copii pe S:, rețea sau audituri sintetice în registrele reale. Rezultatele efective, comenzile, versiunea engine-ului și hash-urile testate intră în dosarul r02. Testele existente se adaptează explicit unde contractul se schimbă; nu se păstrează afirmația „151 trecute” ca substitut al unei rulări noi.
5. **PLANIFICAT — P-MANAGER și auditorii independenți:** îngheață r02, obțin cele două audituri reale și metaauditul pe aceeași versiune, arhivează rezultatele și retestările. Numai auditorul competent poate consemna închiderea finding-urilor pe baza probelor; producătorul nu schimbă `open` în `closed` prin acest plan. O constatare rămasă deschisă sau un criteriu care nu trece strict pragul păstrează RETURN.

## 5. Limita privind P-CANON și G01

Instrucțiunea separată a coordonatorului este păstrată explicit: eventuala corecție P-CANON vizează viitor documentul de selecție, numai după mandatul separat. Nu se modifică manuscrisul și nu se alege arbitrar între Boucher și Dubois. Acest plan nu introduce o constatare A-SYSTEMS nouă despre cele două nume și nu pretinde că a verificat sursele canonice pentru alegere.

Blocajul G01 se menține. Remedierea tehnică SYS-001/G00, trecerea la schema v2 ori reușita unor teste sintetice nu autorizează canonul, selecția sursei sau avansarea manuscrisului. P-SYSTEMS predă numai acest plan și așteaptă mandatul separat pentru editare după arhivare.
