# EVA-3dScan — perspectiva meșterului

Data: 2 octombrie 2026. Autor: agent `tradesperson_v2`. Stare: evaluare de conținut finalizată, recomandări trimise pentru integrare. Aceasta este o perspectivă simulată; nu reprezintă interviuri cu meseriași sau validare pe șantier.

## Ce trebuie să înțeleg ca să încerc aplicația

Vin la client să verific un gol pentru o ușă, un perete pentru mobilier sau o cameră care trebuie renovată. Vreau să văd imediat ce măsor, unde apare rezultatul și ce pot păstra pentru discuția despre lucrare. Modelul 3D și exportul CAD au sens după această explicație.

| Întrebarea mea | Răspunsul care trebuie să apară pe site |
|---|---|
| 1. Pot verifica lățimea golului sau înălțimea peretelui? | Aleg două puncte și văd distanța cu unitatea de măsură. Un exemplu arată clar punctele și cota. |
| 2. Telefonul înregistrează tot când măsor? | Măsurarea pe imagine este temporară implicit, fără salvare automată. Proiectul de camere este un mod separat. |
| 3. Cum notez ce trebuie reparat? | Zonele și observațiile sunt introduse manual în fluxul propus. Imaginea cu maistrul explică documentarea situației, nu diagnosticarea automată. |
| 4. Ce rezultat pot discuta cu clientul? | O referință cotată a camerei și observații asociate în fluxul propus. Site-ul oferă acum un plan DXF sintetic, etichetat ca exemplu. |
| 5. Pot comanda materialul sau calcula prețul direct? | Verific cotele importante la fața locului. Cantitățile, pierderile de material, prețurile și soluția de reparație cer evaluare separată; nu există un deviz automat demonstrat. |

## Poveste de utilizare

**Situație:** un client vrea să monteze un corp de mobilier pe un perete și să repare o zonă deteriorată.

1. Aleg măsurarea pe imagine și verific orientativ lățimea disponibilă. Rezultatul apare lângă punctele alese, cu unitatea explicită.
2. Pentru documentarea lucrării, trec la proiectul de cameră. Păstrez contextul și introduc manual observația despre zona care necesită intervenție, în fluxul planificat al aplicației.
3. Verific dimensiunile de montaj cu instrumentul potrivit. Revizuiesc observațiile cu clientul și pregătesc separat soluția, cantitățile și oferta.

Site-ul trebuie să arate această succesiune într-o singură zonă. Un buton spre toate cele 36 de utilizări este util după ce am înțeles rezultatul meu.

## Evaluarea propunerii inspectate

Au fost citite `content/redesign-v2-source.json`, `public/product-story.js` și `docs/REDESIGN_V2_BRIEF.md`. Nu au fost modificate fișierele de implementare.

**Ce funcționează:** selectorul „O dimensiune”, desenul cotat al peretelui, succesiunea captură–rezultat–utilizare, rolul distinct de meșter și imaginea maistrului cu clientul. Formularea despre verificarea cotelor importante este necesară lângă pași. Exemplele sunt identificate ca sintetice, iar aplicația ca fiind în dezvoltare.

**Corecții concrete pentru integrare:**

| Prioritate | Element | Propunere în română | Motiv |
|---|---|---|---|
| P1 | `v2.measureResult` | „O distanță afișată temporar peste imagine, fără salvare automată” | Explică diferența cerută dintre măsurare și proiectul salvat. |
| P1 | `v2.builderNeed` | „Pregătește renovarea cu dimensiunile camerei și note introduse manual despre zonele de reparat.” | Clarifică cine stabilește reparațiile; imaginea nu devine promisiune de detecție automată. |
| P2 | `v2.builderTitle` | „Măsori spațiul. Pregătești lucrarea.” | Spune activitatea meșterului fără a implica diagnostic prin telefon. |
| P2 | `v2.sampleDownload` | „Deschide planul exemplu (DXF)” | Fișierul comun tuturor rolurilor reprezintă un plan, nu un deviz ori un raport de reparații. |
| P2 | Etapele meșterului | „Măsori peretele sau golul / Notezi manual observațiile în proiect / Verifici cotele de montaj la fața locului” | Leagă măsurarea de rezultatul util și de controlul necesar înaintea execuției. |

Notele și salvarea propuse trebuie prezentate în cadrul statutului de produs în dezvoltare; evaluarea nu confirmă că aceste funcții există într-o aplicație iPhone executabilă.

## Cinci criterii de acceptare

| ID | Criteriu măsurabil | Verificare necesară |
|---|---|---|
| M-01 | Modul de măsurare arată minimum două puncte, o cotă și unitatea; precizează caracterul temporar și lipsa salvării automate. | Inspecția modului pe desktop și mobil. |
| M-02 | Traseul meșterului conține trei pași, dintre care unul pentru observații manuale și unul pentru verificarea cotelor de montaj. | Citirea textelor în toate cele șapte limbi. |
| M-03 | Zero afirmații despre detecție automată a defectelor, deviz automat sau precizie numerică validată fără dovezi. | Audit de text și imagini, inclusiv legende. |
| M-04 | Linkul pentru exemplu numește formatul DXF și tipul de rezultat, iar avertizarea imediat alăturată spune că planul 4 × 3 m este sintetic. | Click pe fișier și verificarea conținutului exemplului. |
| M-05 | În maximum două acțiuni de pe prima pagină, vizitatorul poate selecta „Meșter” și deschide exemplul; textul și acțiunea rămân accesibile la 390 px. | Test browser cu click și tastatură, captură mobilă. |

Aceste criterii sunt propuse pentru auditul integrării; acest agent nu a executat teste de browser. Nu declarăm că un meșter real înțelege produsul în cinci secunde fără un studiu efectiv.

## Reluare și responsabilitate

Intrările au fost citite și recomandările au fost trimise managerului. Următorul pas este integrarea selectivă în textele sursă și în cele șapte localizări, apoi verificarea M-01–M-05 de către implementare/audit. Logul aferent este `redesign-v2-tradesperson.jsonl`.
