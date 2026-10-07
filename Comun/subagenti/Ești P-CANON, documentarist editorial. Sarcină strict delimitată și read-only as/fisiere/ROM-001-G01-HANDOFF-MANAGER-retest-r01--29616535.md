# ROM-001-G01 — retest punctual al predării managerului — r01

Statut: DRAFT; control intern de producție, executat separat de autorul documentelor, nu audit independent sau verdict.
Autor: P-CANON, ID real `01a0d0d7-e865-7b71-9707-be8786099512`.
Data: 24.09.2026, Europe/Bucharest.

## Rezultat și obiect

HM-P01, HM-P02 și clarificarea HM-T15 sunt tratate în FI-nou L60, respectiv TR-nou L19/L30. Nu am identificat o abatere materială nouă în modificările retestate. Această constatare privește exclusiv cele două documente manageriale, nu produsul editorului sau acceptarea G01.

ROOT = `D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000`. Căile din §Surse sunt relative la ROOT; L = linie fizică Markdown; P = paragraf nevid H, conform metodei F L14.

Am citit integral mandatul M, planul PL, înregistrarea Δ și proveniența PR; am comparat toate diferențele dintre copiile vechi și documentele noi și recitit paragrafele modificate cu context: FI L57–L62; TR L16–L22/L27–L33. Am reconsultat C L1–L22/L42–L68 și F L37–L44/L101–L106.

Lecturile integrale FI/TR din controlul C sunt reutilizate pentru textul nemodificat, după potrivirea copiilor vechi cu hashurile documentate atunci. Pentru H/F sunt reutilizate probele anterioare după verificarea hashurilor. Cele 26 P recitite direct în C sunt P3882–P3892, P3931–P3939, P3954–P3955, P3981–P3984. În acest retest: **zero paragrafe H nou recitite**; nu declar o nouă lectură integrală sau reluarea tuturor controalelor.

## Teste proprii și rezultate

| ID / observație | Test și probe | Rezultat în aria retestată |
|---|---|---|
| HR-01 — baza comparației | Hashurile FI-vechi/TR-vechi coincid cu cele ale obiectelor controlate în C și consemnate în PR. Δ indică exact hashul C. | Proveniența comparației este concordantă; copiile vechi nu sunt confundate cu actualele documente corectate. |
| HR-02 — HM-P01 | FI L60 separă plicul nedeschis și custodia Isabellei de cercetarea viitoare. F F07–F09, L41–L43: H P3882–P3892/P3954; registrul P3931–P3938. | Stările deja relatate rămân fapte; informația registrului este atribuită documentului din ficțiune, nu declarată biografie completă. |
| HR-03 — HM-P02, adresă | TR L19 păstrează „Room 14, Hotel Rue des Âmes”, inițiala M. pe verso și necunoscutele privind persoanele/conținutul. F F07; H P3886–P3887/P3892. | Adresa materială cunoscută nu mai intră în aceeași categorie cu persoana destinatară necunoscută. Nu se atribuie autor sau destinatar. |
| HR-04 — HM-P01/HM-P02, referenți | FI L60/TR L19 se confruntă cu F L102–L106: mărturia Odettei H P396–P401; registrul P3932–P3938; asocierea Isabellei P3939. | Două referințe nu certifică două persoane distincte sau identitate comună. Nicio fuziune, separare biografică ori soluție a misterului nu este introdusă. |
| HR-05 — promisiuni și limite | FI L60/TR L19 versus F F09/F10: H P3944–P3948/P3954–P3955/P3981–P3984, din lectura reutilizată. | Cercetarea, solicitarea opțiunii și dezvoltarea poveștii rămân viitoare. Intenția de a cere acordul nu devine acord obținut; custodia nu devine permisiune. Afirmația existentă despre sarcina timpurie/fără copil născut este păstrată, nu extinsă; limitele F F03 rămân aplicabile. |
| HR-06 — HM-T15 | TR L30 versus C HM-T15, L44: 29 fișe de referenți/roluri, opt intrări instituționale, 37 teste în aria declarată. | Unitatea este explicitată: nu se certifică 29 persoane distincte. Nu am renumărat ori recertificat controlul de afiliere. |
| HR-07 — regresie integrală a diferențelor | Comparație integrală vechi/nou; fiecare text „before” din Δ apare o singură dată. Aplicarea numai a celor trei înlocuiri în memorie reproduce exact hashurile fișierelor noi. | FI: 62 linii, schimbată numai L60. TR: 77 linii, schimbate numai L19/L30. Restul este identic la nivel de octeți, inclusiv contextul conservat; nu există alte diferențe ascunse prin normalizarea liniilor. |
| HR-08 — stabilitatea intrărilor | Recalcularea celor 11 hashuri la 12:01:26 și 12:05:17, UTC+03:00. | Toate intrările au rămas neschimbate între verificări. Obiectul controlat este fixat prin amprentele de mai jos. |

## Surse și SHA-256

Numai materialele folosite aici; nu se reproduce inventarul extins din C.

| Cod | Cale relativă | SHA-256 |
|---|---|---|
| M | `06_REGISTRU/PROMPTURI/ROM-001-G01-P-CANON-handoff-retest-r01.md` | `2d166427eb013fbb6a33817b273a84674155e320df854bdb143d8ff74140fcee` |
| C | `06_REGISTRU/MASURI/ROM-001-G01-HANDOFF-MANAGER-controle-r01.md` | `9aa802c960d5e510d3b864aeddb86c79b1574f449ff8df4015248fe01ce79dad` |
| PL | `06_REGISTRU/MASURI/ROM-001-G01-HANDOFF-MANAGER-masuri-r01.md` | `06dcc5aeda0bfe31748d2ad0a45d547a4eec990324431c129b2fd03c0ade3042` |
| Δ | `06_REGISTRU/REZULTATE/ROM-001-G01-HANDOFF-MANAGER-modificari-r01.json` | `71b108bfd7104780b5b1d5fe0c31a80094f40a6f2ce1e69bf0b7c8a208033f7d` |
| PR | `07_ROMANE/ROM-001/00_BRIEF/ISTORIC_PREDEPUNERE_r02/provenienta.json` | `67456e096f4698e764f611f2e00def53eb9b4c2b9dc37d8a843f6de4ef0409ca` |
| FI-vechi | `07_ROMANE/ROM-001/00_BRIEF/ISTORIC_PREDEPUNERE_r02/FISA_LIVRABIL_G01_r02.md` | `d904b796016405c01bda89e08348309b18b4526b4aff57a4ef20f1433450de6d` |
| TR-vechi | `07_ROMANE/ROM-001/00_BRIEF/ISTORIC_PREDEPUNERE_r02/TRASABILITATE_DEPUNERE_r02.md` | `8be176331540a3aeac22782ccdbca2c8257210b94c72d7b99fefcabd15b6ca22` |
| FI-nou | `07_ROMANE/ROM-001/00_BRIEF/FISA_LIVRABIL_G01_r02.md` | `cf6581c9f8c70b091e8eb2d13b35993f97e973d8409c09ace04a47517383b5b5` |
| TR-nou | `07_ROMANE/ROM-001/00_BRIEF/TRASABILITATE_DEPUNERE_r02.md` | `bd69bdd3310a53ee8a1cf7e8d8ac66f0970232b126f2c13ca246a32fb95cfcc5` |
| F | `07_ROMANE/ROM-001/01_CANON/r01/CANON_FACTUAL.md` | `0635d163992d0c63d0b1d815df000816f8b9320c84e33c732cb899dd6eebd3ab` |
| H | `02_DOCUMENTARE/INTRARI_REFERINTA/H.docx` | `a9940d5776380cb40b105429f6976219440f3ea74fb8ebc1d1b4481e9da068c3` |

## Limite și predare

Rezultatul nu închide formal `ROM-001-G01-A-CANON-F01` sau `META-ROM-001-G01-r01-F01`; G01 rămâne neacceptat. Planul și raportul de control anterior sunt păstrate ca documente istorice, fără actualizarea retroactivă a stărilor lor. Nu am recitit produsele editoriale r03, refăcut infrastructura, verificat recuperarea arhivistică sau folosit snapshotul STATUS ca probă nouă de stare.

Nu am modificat cele două documente manageriale, copiile anterioare, sursele/H, canonul, contractele, manifestele ori site-ul. Nu am redactat proză, G02+, scoruri sau aprobări și nu am creat subagenți.

Predau exclusiv acest raport pentru integrarea managerului. Orice modificare ulterioară a obiectelor controlate necesită verificarea propriei diferențe; concluzia prezentă nu se transferă automat versiunilor viitoare. Scrierile se opresc după salvarea și verificarea acestui unic livrabil.

