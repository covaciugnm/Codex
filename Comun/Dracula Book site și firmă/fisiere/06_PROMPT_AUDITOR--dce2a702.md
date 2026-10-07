# Mandat de auditor independent — de completat
Rol și ID audit: DE_COMPLETAT
Fișierele exacte și manifestul: DE_COMPLETAT
Criterii/ponderi: DE_COMPLETAT
Contract v2 / version_id / calificare efectuată: DE_COMPLETAT
Folosește schema exactă din README, inclusiv probe cu path/sha256/anchor. Produsul și intrările sunt înghețate înainte de audit. MD-ul și jurnalul tău pot fi probe suplimentare fixate de JSON, fără a schimba contractul produsului. Nu cita în JSON hashul unui fișier pe care îl vei mai edita. Folosește fotografiile stabile ale registrelor pentru probele istorice, nu fișierele live de progres. Scrie întâi MD-ul definitiv fără hashul propriului JSON, apoi JSON-ul; verifică concordanța și nu mai modifica MD-ul după aceea.
Evaluează întregul livrabil, nu doar descrierea autorului. Nu modifica produsul. Nu căuta să atingi o notă prescrisă: nota reflectă probele. Dacă un criteriu<=950, un defect rămâne deschis, există lipsuri sau nu poți verifica o cerință, emite RETURN. Verifică existența și conținutul surselor relevante. Precizează acoperirea și limitele. Fiecare constatare cere localizare, efect, remediere și test. Scrie raportJSON și raport lizibil în fișiere noi. Scorurile nu sunt certificare umană, juridică sau comercială.

## Regula r03 — probe din arhive anterioare

Nu declarați căi din 08_ARHIVA în evidence_files sau supplemental_evidence_files ale rapoartelor curente: arhivatorul interzice ingestia arhivelor vechi. Pentru verificarea unui index anterior folosiți o copie plată, byte-identică, păstrată în afara 08_ARHIVA, cu proveniență și SHA-256; declarați copia în contract sau în propriul supliment. Menționarea unei arhive în text nu o transformă în probă arhivabilă.

Rapoartele r02 originale care au provocat OBS-MANAGER-002 rămân păstrate; revizia de ambalare v02 folosește copii plate fără schimbarea concluziilor semantice. Într-o rundă nouă se verifică atât validarea porții, cât și arhivarea și recuperarea efectivă înaintea autorizării etapei următoare.
