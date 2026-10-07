# ROM-001 — pregătirea depunerii/arhivării r01

Autor: P-SYSTEMS, `01a0d0d9-1f95-7211-8093-c26e28e6ebee`. Creat: 2026-09-24T07:00:01Z. Selecția fișierelor și amprentele de lucru: 2026-09-24T06:55:41Z. G00 r03 acceptat conform mandatului; G01 în producție. Acesta este un inventar de pregătire, nu depunere finală, audit, PASS sau acceptare de etapă.

Au fost scrise numai acest MD și JSON-ul pereche. Niciun instrument, registru global, contract, raport de audit, arhivă, original ori site nu a fost modificat. Nu s-a executat arhivatorul/exportatorul și nu au fost creați subagenți.

## Rezultatul inventarierii

143 căi relative ROOT, deduplicate după cale, toate citite pentru calculul SHA-256. JSON-ul pereche este lista de lucru exactă `files:[{path,sha256,category}]`; nu este schema arhivatorului sau un contract de produs. Cele 130 de fișiere din enumerarea ROM-001/ROM001 sunt completate punctual cu trei configurații de export, nouă copii preexistente indicate de matricea G01 și setul comun de calibrare citat de QA. Nu s-au căutat alte surse.

Protocolul de arhivare, manualul și rolul propriu au fost citite integral. Pentru inventar s-au consultat metadatele, mandatele/predările/proveniența necesare, concluziile nominale QA și indexurile. Nu se pretinde relectura tuturor conținuturilor, reevaluarea literaturii sau un nou control al calificărilor.

| Categorie JSON | Fișiere |
| --- | ---: |
| `calibrare_context` | 3 |
| `calibrare_raspuns` | 10 |
| `calibrare_set` | 3 |
| `calibrare_verificare_QA` | 4 |
| `componenta_canon_r01` | 4 |
| `configuratie_export` | 3 |
| `context_fix_integrare` | 3 |
| `document_G01_contract_posibil` | 9 |
| `draft_istoric` | 2 |
| `draft_productie_r01` | 2 |
| `erratum_observabil` | 1 |
| `export_observabil_derivat` | 20 |
| `export_observabil_index` | 2 |
| `incident_executie` | 1 |
| `mandat` | 24 |
| `mandat_beneficiar` | 2 |
| `predare_inchidere` | 19 |
| `provenienta_copie` | 4 |
| `rezultat_control` | 10 |
| `sursa_G01_contract_posibil` | 8 |
| `sursa_preexistenta_contract_posibil` | 9 |

## Depunerile și traseul deja documentat

- Mandatul beneficiarului, aprobarea G01/DB-047 și mandatele de reconciliere/delegare sunt în `00_BRIEF` și `06_REGISTRU/PROMPTURI`. Existența unui mandat de audit nu înseamnă că auditul a avut loc.
- Editorul a predat două componente DRAFT r01: `BRIEF_ROMAN_r01.md` și `DECIZII_PROPUSE_r01.md`. Există predare, închidere și două copii distincte în `ISTORIC_PREINTEGRARE_r01`, cu proveniență. Hashurile copiilor coincid cu declarațiile și cu drafturile r01 observate; păstrez toate căile, nu deduplic după conținut.
- Canonistul a predat cele patru componente `01_CANON/r01`; predarea include închiderea în `close_result`. Declarația sa de lectură integrală H este documentată acolo și în jurnal, nu recertificată de acest inventar. Mandatul lateral pentru `CONSTRANGERI_CALENDAR_r01.md` este inclus; rezultatul era în producție la selecție.
- Cele 17 surse din matrice sunt reprezentate prin nouă copii existente în `02_DOCUMENTARE/INTRARI_REFERINTA` și opt în `01_CANON/INTRARI_G01`. Hashurile actuale ale copiilor coincid cu cele trei declarații de proveniență/verificare consultate. Nu am accesat originalele exterioare și nu transform rapoartele istorice de scor/originalitate în aprobări curente.
- Fotografia `CONTEXT_INTEGRARE_r02` are trei copii de context plus proveniență. Toate trei corespund hashurilor declarate; nu trebuie înlocuite cu registrele live. Un hash comun cu altă fotografie nu anulează proveniența separată.
- Calibrare A: patru răspunsuri, set suplimentar, context și proveniență, mandate, predări/închideri, raport QA MD/JSON și rezultatul de verificare. A-QAMANAGER consemnează A-GENRE/A-ORIGINALITY/A-STRUCTURE/A-EN, fiecare 11/11 (44/44 total).
- Calibrare B: șase răspunsuri, set suplimentar, context, mandate, predări cu închideri încorporate, raport QA MD/JSON și rezultatul de verificare. A-QAMANAGER consemnează A-CHARACTER/A-FACT/A-RO/A-DE/A-TRANSLATION/A-PRODUCTION, fiecare 11/11 (66/66 total). Aceste rezultate sunt calificări pe TEST, nu audituri G01; nu cer fișiere de închidere separate când predarea conține deja închiderea.
- Incidentul `ROM-001-P-EDITOR-limita-executie-r01.json` este explicit `EXECUTION_INTERRUPTION_NOT_EDITORIAL_RETURN`, consemnat la 2026-09-24 06:50:23 UTC. Mandatul `ROM-001-G01-P-EDITOR-reluare-dupa-limita-r02.md` reactivează aceeași identitate. Nu interpretez limita tehnică drept respingere editorială și nu pretind r02 predat.

## Exportul observabil și OBS-EXPORT-001

Captura existentă `06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01` are efectiv 10 surse, 1948 înregistrări și 299 mesaje în index. Setul de roluri/ID-uri/căi coincide cu configurația v02. SHA-256 al indexului: `cd9e96884d60c2c76b125b4b5ca5096a144f36a5fc9d0a6fcbe16a240b2ea698`; acesta corespunde sidecar-ului și recipisei. Toate cele 20 de ieșiri derivate coincid acum cu hashurile și dimensiunile declarate.

Literalul `nine` din `index.scope` este greșit pentru această captură. Păstrez indexul și `ROM001-G01-EXPORT_ERRATUM-r01.md` împreună, fără schimbarea exportatorului. Proba existentă `EXPORT_PREFIXE` consemnează verificarea celor 10 prefixe; nu am deschis rawlogs și nu am repetat verificarea lor.

Configurațiile efective au 6 surse (inițială), 10 (v02), 16 (v03). `06_REGISTRU/ROM-001_surse_export_G01_v03.json` nu include P-SYSTEMS `01a0d0d9-1f95-7211-8093-c26e28e6ebee`. Main trebuie să includă execuția reactivată într-o configurație NOUĂ și apoi într-o captură nouă, fără să editeze v03 sau capturile existente. Ar rezulta 17 numai dacă aceasta este singura adăugare; numărul final se calculează din configurația nouă. Captura pe 10 surse nu acoperă lotul B sau reactivarea mea.

## Suprapuneri cu viitorul contract: păstrate, nu eliminate

Lista de mai jos este propunerea conservatoare de `extras`: un fișier per cale, fără ingestia `08_ARHIVA`. Include intenționat componentele/sursele care pot ajunge și în `files` sau `evidence_files`. Nu există aici o comparație cu un contract G01 final și nu pretind că aceste suprapuneri sunt deja stabilite.

Main confruntă exact căile și hashurile cu manifestul/contractul final, dependențele și sursele copiate automat. Numai după această confruntare poate evita o declarare redundantă ca extra, păstrând acoperirea verificabilă; nimic nu a fost eliminat pe presupunerea că „intră automat”. Atenție în special la componentele `00_BRIEF`/`01_CANON`, cele 17 surse, contextul fix, calificări și setul comun de calibrare. Copiile de context G00 sunt fișiere plate, nu ingestia arhivelor vechi.

JSON-ul nu își conține propriul hash. După predare, main fixează separat ambele fișiere ale inventarului și răspunsul final exact, ca documente ale procesului. Acestea sunt completări explicite după creare, nu intrări fictiv hash-uite înainte.

## PENDING — nu lipsuri culpabile înaintea termenului

1. **Componente editoriale r02** — P-EDITOR / P-MANAGER. În producție după reluarea aceleiași identități. Nu erau în enumerarea fixată la 2026-09-24T06:55:41Z; nu este lipsă culpabilă, RETURN sau aprobare anticipată.\n\n   Căi cunoscute: `07_ROMANE/ROM-001/00_BRIEF/BRIEF_ROMAN_r02.md`, `07_ROMANE/ROM-001/00_BRIEF/DECIZII_CANON_r02.md`, `07_ROMANE/ROM-001/00_BRIEF/CANON_OPERATIONAL_r02.md`.

2. **Predarea și închiderea editorului pentru r02 reluat** — P-MANAGER. Se păstrează răspunsul final exact și recipisa observabilă după predarea efectivă; predarea/închiderea r01 nu le substituie. Nu se inventează nume final de fișier sau oră.

3. **Foaie laterală de constrângeri calendar și predarea sa** — P-CANON / P-MANAGER. Mandat lateral activ salvat; rezultatul nu era în enumerarea fixată. Este ajutor intern, nu audit al editorului; nu se așteaptă pentru încheierea acestui inventar.\n\n   Căi cunoscute: `07_ROMANE/ROM-001/01_CANON/CONSTRANGERI_CALENDAR_r01.md`.

4. **Configurație nouă de export după reactivarea P-SYSTEMS** — P-MANAGER. Configurația v03 are 16 surse și nu include 01a0d0d9-1f95-7211-8093-c26e28e6ebee. Noua configurație trebuie să includă această execuție reactivată și orice alte execuții autorizate între timp, deduplicate; v03 nu se modifică. 17 rezultă numai dacă singura adăugare este P-SYSTEMS.

5. **Captură observabilă nouă și probele sale** — P-MANAGER. După reluare/predări: captură filtrată pe noua configurație, index/sidecar, recipisă și controale actuale. Captura de pregătire existentă are 10 surse, nu acoperă lotul B sau această reactivare. OBS-EXPORT-001 însoțește interpretarea literalului nine; nu se modifică exportatorul.

6. **Manifest/contract final G01 și reconcilierea suprapunerilor** — P-MANAGER. Lista files este propunerea conservatoare de extras, nu manifest de depunere sau contract. Main confruntă fiecare cale/hash cu files/evidence_files, dependențele și sursele arhivate automat; nicio cale nu este eliminată aici pe presupunerea suprapunerii.

7. **Captura BEFORE_AUDIT G01** — P-MANAGER. Urmează după depunerea și înghețarea produsului. Nu s-a inspectat sau ingerat 08_ARHIVA; nu se deduce existența/absența unei runde din numele acestei sarcini.

8. **Audituri G01, metaaudit, rezultat de poartă și AFTER_AUDIT/recuperare** — A-CANON / A-GOVERNANCE / A-QAMANAGER / P-MANAGER. Etape viitoare pe versiunea înghețată; calificările TEST A/B nu sunt rapoarte G01. Se păstrează și orice RETURN, măsuri și retesturi dacă apar; nu se generează anticipat.

9. **Depunerea acestui inventar și răspunsul final al P-SYSTEMS** — P-MANAGER. După predare se includ aceste două documente și răspunsul final exact în runda potrivită. Nu apar în propriul files pentru a evita autohashul circular; main le fixează separat. Nicio oră/recipisă viitoare nu este inventată.\n\n   Căi cunoscute: `06_REGISTRU/ROM-001_PREGATIRE_ARHIVARE_r01.md`, `06_REGISTRU/ROM-001_PREGATIRE_ARHIVARE_r01.json`.

## Lista exactă deduplicată propusă pentru extras

143 căi, în aceeași ordine ca `files` din JSON; fiecare este relativă la ROOT. Nu este o comandă executată. Hashurile sunt în JSON, iar situațiile PENDING nu intră în această listă ca fișiere inexistente.

```text
02_DOCUMENTARE/INTRARI_REFERINTA/AC.docx
02_DOCUMENTARE/INTRARI_REFERINTA/H.docx
02_DOCUMENTARE/INTRARI_REFERINTA/HB.docx
02_DOCUMENTARE/INTRARI_REFERINTA/HBT.txt
02_DOCUMENTARE/INTRARI_REFERINTA/HC.txt
02_DOCUMENTARE/INTRARI_REFERINTA/HP.docx
02_DOCUMENTARE/INTRARI_REFERINTA/HT.txt
02_DOCUMENTARE/INTRARI_REFERINTA/OR.txt
02_DOCUMENTARE/INTRARI_REFERINTA/SITE_APP.js
05_AUDIT/ROM-001-CALIBRARE/VERIFICARE_B_r01.json
05_AUDIT/ROM-001-CALIBRARE/VERIFICARE_B_r01.md
05_AUDIT/ROM-001-CALIBRARE/VERIFICARE_r01.json
05_AUDIT/ROM-001-CALIBRARE/VERIFICARE_r01.md
06_REGISTRU/CALIBRARE/ROM-001/A-CHARACTER-b-r01.json
06_REGISTRU/CALIBRARE/ROM-001/A-DE-b-r01.json
06_REGISTRU/CALIBRARE/ROM-001/A-EN-r01.json
06_REGISTRU/CALIBRARE/ROM-001/A-FACT-b-r01.json
06_REGISTRU/CALIBRARE/ROM-001/A-GENRE-r01.json
06_REGISTRU/CALIBRARE/ROM-001/A-ORIGINALITY-r01.json
06_REGISTRU/CALIBRARE/ROM-001/A-PRODUCTION-b-r01.json
06_REGISTRU/CALIBRARE/ROM-001/A-RO-b-r01.json
06_REGISTRU/CALIBRARE/ROM-001/A-STRUCTURE-r01.json
06_REGISTRU/CALIBRARE/ROM-001/A-TRANSLATION-b-r01.json
06_REGISTRU/CALIBRARE/ROM-001/SET_SUPLIMENTAR_B_r01.md
06_REGISTRU/CALIBRARE/ROM-001/SET_SUPLIMENTAR_r01.md
06_REGISTRU/CALIBRARE/ROM-001/agents_at_A_check.json
06_REGISTRU/CALIBRARE/ROM-001/agents_at_A_check_provenance.json
06_REGISTRU/CALIBRARE/ROM-001/agents_at_B_check.json
06_REGISTRU/CALIBRARE/SET_TEST_r02.md
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/A-CANON.jsonl
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/A-CANON.md
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/A-EN.jsonl
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/A-EN.md
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/A-GENRE.jsonl
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/A-GENRE.md
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/A-GOVERNANCE.jsonl
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/A-GOVERNANCE.md
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/A-ORIGINALITY.jsonl
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/A-ORIGINALITY.md
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/A-QAMANAGER.jsonl
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/A-QAMANAGER.md
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/A-STRUCTURE.jsonl
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/A-STRUCTURE.md
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/P-CANON.jsonl
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/P-CANON.md
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/P-EDITOR.jsonl
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/P-EDITOR.md
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/P-MANAGER.jsonl
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/P-MANAGER.md
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/index.json
06_REGISTRU/ISTORIC/EXPORT_OBSERVABIL/ROM001-G01-preparare-r01/index.sha256
06_REGISTRU/ISTORIC/ROM-001-A-CHARACTER-calibrare-b-predare-r01.json
06_REGISTRU/ISTORIC/ROM-001-A-DE-calibrare-b-predare-r01.json
06_REGISTRU/ISTORIC/ROM-001-A-EN-calibrare-inchidere-r01.json
06_REGISTRU/ISTORIC/ROM-001-A-EN-calibrare-predare-r01.json
06_REGISTRU/ISTORIC/ROM-001-A-FACT-calibrare-b-predare-r01.json
06_REGISTRU/ISTORIC/ROM-001-A-GENRE-calibrare-inchidere-r01.json
06_REGISTRU/ISTORIC/ROM-001-A-GENRE-calibrare-predare-r01.json
06_REGISTRU/ISTORIC/ROM-001-A-ORIGINALITY-calibrare-inchidere-r01.json
06_REGISTRU/ISTORIC/ROM-001-A-ORIGINALITY-calibrare-predare-r01.json
06_REGISTRU/ISTORIC/ROM-001-A-PRODUCTION-calibrare-b-predare-r01.json
06_REGISTRU/ISTORIC/ROM-001-A-QAMANAGER-calibrare-a-predare-r01.json
06_REGISTRU/ISTORIC/ROM-001-A-QAMANAGER-calibrare-b-predare-r01.json
06_REGISTRU/ISTORIC/ROM-001-A-RO-calibrare-b-predare-r01.json
06_REGISTRU/ISTORIC/ROM-001-A-STRUCTURE-calibrare-inchidere-r01.json
06_REGISTRU/ISTORIC/ROM-001-A-STRUCTURE-calibrare-predare-r01.json
06_REGISTRU/ISTORIC/ROM-001-A-TRANSLATION-calibrare-b-predare-r01.json
06_REGISTRU/ISTORIC/ROM-001-P-CANON-G01-predare-r01.json
06_REGISTRU/ISTORIC/ROM-001-P-EDITOR-G01-inchidere-r01.json
06_REGISTRU/ISTORIC/ROM-001-P-EDITOR-G01-predare-r01.json
06_REGISTRU/ISTORIC/ROM-001-P-EDITOR-limita-executie-r01.json
06_REGISTRU/PROMPTURI/ROM-001-A-CHARACTER-calibrare-b-r01.md
06_REGISTRU/PROMPTURI/ROM-001-A-DE-calibrare-b-r01.md
06_REGISTRU/PROMPTURI/ROM-001-A-EN-calibrare-r01.md
06_REGISTRU/PROMPTURI/ROM-001-A-FACT-calibrare-b-r01.md
06_REGISTRU/PROMPTURI/ROM-001-A-GENRE-calibrare-r01.md
06_REGISTRU/PROMPTURI/ROM-001-A-ORIGINALITY-calibrare-r01.md
06_REGISTRU/PROMPTURI/ROM-001-A-PRODUCTION-calibrare-b-r01.md
06_REGISTRU/PROMPTURI/ROM-001-A-RO-calibrare-b-r01.md
06_REGISTRU/PROMPTURI/ROM-001-A-STRUCTURE-calibrare-r01.md
06_REGISTRU/PROMPTURI/ROM-001-A-TRANSLATION-calibrare-b-r01.md
06_REGISTRU/PROMPTURI/ROM-001-G01-A-CANON-r01.md
06_REGISTRU/PROMPTURI/ROM-001-G01-A-GOVERNANCE-r01.md
06_REGISTRU/PROMPTURI/ROM-001-G01-P-CANON-calendar-constraints-r01.md
06_REGISTRU/PROMPTURI/ROM-001-G01-P-CANON-r01.md
06_REGISTRU/PROMPTURI/ROM-001-G01-P-EDITOR-activare-r02.md
06_REGISTRU/PROMPTURI/ROM-001-G01-P-EDITOR-integrare-r02.md
06_REGISTRU/PROMPTURI/ROM-001-G01-P-EDITOR-r01.md
06_REGISTRU/PROMPTURI/ROM-001-G01-P-EDITOR-reluare-dupa-limita-r02.md
06_REGISTRU/PROMPTURI/ROM-001-G01-P-SYSTEMS-arhivare-pregatire-r01.md
06_REGISTRU/PROMPTURI/ROM-001-G01-autorizare-reconciliere.md
06_REGISTRU/PROMPTURI/ROM-001-G01-identificare-DB047.md
06_REGISTRU/PROMPTURI/ROM-001-QA-calibrare-context-r01.md
06_REGISTRU/PROMPTURI/ROM-001-QA-calibrare-editoriala-B-r01.md
06_REGISTRU/PROMPTURI/ROM-001-QA-calibrare-editoriala-r01.md
06_REGISTRU/REZULTATE/ROM-001-CALIBRARE-A-verification-r01.json
06_REGISTRU/REZULTATE/ROM-001-CALIBRARE-B-verification-r01.json
06_REGISTRU/REZULTATE/ROM-001-G01-sources-recheck-r01.json
06_REGISTRU/REZULTATE/ROM-001-INTRARE-RES-001-G01-r01.json
06_REGISTRU/REZULTATE/ROM-001-INTRARE-SEL-001-G01-r01.json
06_REGISTRU/REZULTATE/ROM-001-INTRARE-SYS-001-G01-r01.json
06_REGISTRU/REZULTATE/ROM-001-P-CANON-primire-r01.json
06_REGISTRU/REZULTATE/ROM001-G01-EXPORT_ERRATUM-r01.md
06_REGISTRU/REZULTATE/ROM001-G01-EXPORT_PREFIXE-r01.json
06_REGISTRU/REZULTATE/ROM001-G01-EXPORT_PREPARARE-r01.json
06_REGISTRU/REZULTATE/ROM001-G01-EXPORT_VERIFICARE-r01.json
06_REGISTRU/ROM-001_surse_export_G01.json
06_REGISTRU/ROM-001_surse_export_G01_v02.json
06_REGISTRU/ROM-001_surse_export_G01_v03.json
07_ROMANE/ROM-001/00_BRIEF/APROBARE_BENEFICIAR_G01.md
07_ROMANE/ROM-001/00_BRIEF/BRIEF_ROMAN_r01.md
07_ROMANE/ROM-001/00_BRIEF/CONTEXT_INTEGRARE_r02/STATUS_la_integrare.md
07_ROMANE/ROM-001/00_BRIEF/CONTEXT_INTEGRARE_r02/agents.json
07_ROMANE/ROM-001/00_BRIEF/CONTEXT_INTEGRARE_r02/deliverables_G00.json
07_ROMANE/ROM-001/00_BRIEF/CONTEXT_INTEGRARE_r02/provenienta.json
07_ROMANE/ROM-001/00_BRIEF/DECIZII_PROPUSE_r01.md
07_ROMANE/ROM-001/00_BRIEF/FISA_LIVRABIL_G01_r01.md
07_ROMANE/ROM-001/00_BRIEF/ISTORIC_PREINTEGRARE_r01/BRIEF_ROMAN_r01.md
07_ROMANE/ROM-001/00_BRIEF/ISTORIC_PREINTEGRARE_r01/DECIZII_PROPUSE_r01.md
07_ROMANE/ROM-001/00_BRIEF/ISTORIC_PREINTEGRARE_r01/provenienta.json
07_ROMANE/ROM-001/00_BRIEF/MANDAT_SESIUNE_20260924.md
07_ROMANE/ROM-001/00_BRIEF/REGISTRU_DREPTURI_r01.md
07_ROMANE/ROM-001/00_BRIEF/TRASABILITATE_DEPUNERE_r01.md
07_ROMANE/ROM-001/01_CANON/COMPARAISON_AUXILIARE_r01.json
07_ROMANE/ROM-001/01_CANON/INTRARI_G01/HCX.docx
07_ROMANE/ROM-001/01_CANON/INTRARI_G01/ORX.docx
07_ROMANE/ROM-001/01_CANON/INTRARI_G01/SCORES.txt
07_ROMANE/ROM-001/01_CANON/INTRARI_G01/SCX.docx
07_ROMANE/ROM-001/01_CANON/INTRARI_G01/STRATEGIE_date_plan.json
07_ROMANE/ROM-001/01_CANON/INTRARI_G01/TR_PROMPT.md
07_ROMANE/ROM-001/01_CANON/INTRARI_G01/WC.txt
07_ROMANE/ROM-001/01_CANON/INTRARI_G01/WCX.docx
07_ROMANE/ROM-001/01_CANON/INTRARI_G01/provenienta.json
07_ROMANE/ROM-001/01_CANON/INTRARI_G01/provenienta_docx.json
07_ROMANE/ROM-001/01_CANON/LECTURA_AUXILIARE_MANAGER_r01.md
07_ROMANE/ROM-001/01_CANON/MATRICE_SURSE_r01.md
07_ROMANE/ROM-001/01_CANON/VERIFICARE_IDENTITATE_CONTINUT_r01.json
07_ROMANE/ROM-001/01_CANON/VERIFICARE_SURSE_G01_r01.json
07_ROMANE/ROM-001/01_CANON/r01/CANON_FACTUAL.md
07_ROMANE/ROM-001/01_CANON/r01/CONTRADICTII.md
07_ROMANE/ROM-001/01_CANON/r01/CRONOLOGIE_OBSERVATA.md
07_ROMANE/ROM-001/01_CANON/r01/JURNAL_LECTURA.md
07_ROMANE/ROM-001/START_AICI.md
```

## Limite de utilizare

Control final 2026-09-24T07:01:17Z: 142 fișiere au păstrat hashurile inițiale. 07_ROMANE/ROM-001/00_BRIEF/FISA_LIVRABIL_G01_r01.md s-a schimbat în timpul producției din 0839ab40d982ea6b9028121ef08caf226ac035bb90c09ed5438084796a9c0735 în f99d6af0b361750c844e9a319fde46df26e52dc51c97c95e6491e8ecc5b1ba2a; files conține noul hash efectiv observat. Nu am modificat fișa și nu atribui cauza. Lista este o observație neatomică; ambele amprente sunt conservate aici pentru trasabilitate.

Nu este snapshot atomic, certificare de drepturi, autentificare externă, WORM ori control antifals. Hashurile identifică bytes observați; main reenumeră și recalculează la înghețare. Nu am deschis rawlogs/reasoning, originale din afara root-ului ori `08_ARHIVA`; numai capturi deja filtrate și copii locale relevante. Nu am transformat eticheta istorică din START_AICI, un mesaj „gata”, o calificare TEST sau acceptarea G00 în acceptare G01.

În total au fost confruntate 17 copii de surse, două copii ale drafturilor inițiale și trei copii de context cu declarațiile consultate; acest control nu afirmă adevărul conținutului sau o nouă comparație cu originalele. Tot ce apare după selecția indicată cere completare la următoarea depunere. Arhivarea efectivă, contractul final, auditurile și decizia de etapă rămân la fluxul main/QA. Inventarul este încheiat la această predare; nu se continuă scrierile.
