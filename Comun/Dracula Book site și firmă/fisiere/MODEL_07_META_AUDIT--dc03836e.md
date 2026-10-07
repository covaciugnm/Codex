# Metaaudit — MODEL
Agent A-QAMANAGER și ID: DE_COMPLETAT
Rapoarte exacte, hash-uri și livrabil: DE_COMPLETAT
Controale obligatorii: independence; coverage; evidence; scoring; closure; version.
Schema JSON v2: version_id, contract, audit_files cu hashuri exacte; probe path/sha256/anchor și eventual supplemental_evidence_files pentru MD-ul metaauditorului. Verifică și calificarea nominală efectuată înainte de reaudit, precum și fotografiile stabile de context. Fixează MD-ul înainte de JSON, fără hashul propriului JSON în MD. Nu există scor literar nou și nu există al patrulea audit recursiv.
Pentru fiecare: rezultat true/false și dovadă verificabilă. Verifică și proporționalitatea notelor, lipsa probelor inventate, concordanța raportului lizibil cu JSON și închiderea reală a problemelor. Nu modifica notele altora. Dacă problema aparține raportului, îl returnezi auditorului; dacă aparține produsului, redeschizi măsura. Verdict inițial: NEEMIS.

## Regula r03 — probe din arhive anterioare

Nu declarați căi din 08_ARHIVA în evidence_files sau supplemental_evidence_files ale rapoartelor curente: arhivatorul interzice ingestia arhivelor vechi. Pentru verificarea unui index anterior folosiți o copie plată, byte-identică, păstrată în afara 08_ARHIVA, cu proveniență și SHA-256; declarați copia în contract sau în propriul supliment. Menționarea unei arhive în text nu o transformă în probă arhivabilă.

Rapoartele r02 originale care au provocat OBS-MANAGER-002 rămân păstrate; revizia de ambalare v02 folosește copii plate fără schimbarea concluziilor semantice. Într-o rundă nouă se verifică atât validarea porții, cât și arhivarea și recuperarea efectivă înaintea autorizării etapei următoare.
