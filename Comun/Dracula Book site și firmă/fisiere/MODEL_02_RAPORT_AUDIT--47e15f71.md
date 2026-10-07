# Raport de audit — MODEL, fără scoruri
Audit ID / livrabil / versiune / dată: DE_COMPLETAT
Auditor, rol și ID real: DE_COMPLETAT
Declarație de independență față de producători: DE_COMPLETAT
Fișiere exacte și checksum-uri: DE_COMPLETAT
Acoperire efectivă a lecturii/testării: DE_COMPLETAT
| Criteriu | Pondere | Scor0–1000 | Dovezi localizate | Constatări |
|---|---|---|---|---|
| DE_COMPLETAT | DE_COMPLETAT | NECOMPLETAT | DE_COMPLETAT | DE_COMPLETAT |
Verdict: NEEMIS; PASS numai dacă toate criteriile>=951, zero constatări deschise și condițiile obligatorii îndeplinite.
Limitări reale, fără a pretinde lecturi/teste neefectuate: DE_COMPLETAT
Reauditul produce alt raport; acest document nu se suprascrie după depunere.

Schema JSON v2: version_id și contract trebuie să coincidă cu depunerea. Fiecare evidence are path, sha256 și anchor conform README. Probe noi ale auditorului (acest MD, jurnalul testelor) se declară în supplemental_evidence_files și rămân neschimbate după emiterea JSON-ului. MD-ul nu conține hashul propriului JSON viitor, pentru a evita autohash circular. Metaauditorul verifică exact ambele forme și justificarea lor; nu converti un raport r01 în r02 schimbând doar versiunea sau nota.
Nu cita STATUS/agents/deliverables live ca surse istorice cu hash; citează fotografiile înghețate ale contextului. Verificarea identităților curente în validator rămâne obligatorie.

## Regula r03 — probe din arhive anterioare

Nu declarați căi din 08_ARHIVA în evidence_files sau supplemental_evidence_files ale rapoartelor curente: arhivatorul interzice ingestia arhivelor vechi. Pentru verificarea unui index anterior folosiți o copie plată, byte-identică, păstrată în afara 08_ARHIVA, cu proveniență și SHA-256; declarați copia în contract sau în propriul supliment. Menționarea unei arhive în text nu o transformă în probă arhivabilă.

Rapoartele r02 originale care au provocat OBS-MANAGER-002 rămân păstrate; revizia de ambalare v02 folosește copii plate fără schimbarea concluziilor semantice. Într-o rundă nouă se verifică atât validarea porții, cât și arhivarea și recuperarea efectivă înaintea autorizării etapei următoare.
