import os, sys
T, OUT = sys.argv[1], sys.argv[2]

tasks = [
    dict(id='SRV-013', slug='help-server-aplicatie', exe='SERVER', sol='PROPRIETAR', st='în lucru', pr='P1', dep='—',
         contract='feat/help: HELP_ARHITECTURA.md, HELP_INTEGRARE.md (migrarea 016)',
         ce='Help pe server pentru APLICAȚIE și pentru SERVER/site, în 7 limbi:\n- portal /ajutor/ cu căutare;\n- help-ul aplicației redat din app_i18n (cele 14 capitole din HelpModels.swift);\n- capitole noi pentru site, cont, bibliotecă, admin, scenă, magazie, setări și API;\n- API /api/help, /api/help/tips, /api/help/search;\n- help.js: butonul „?” pe fiecare pagină și clic dreapta pe orice element → „Ce e asta / Ce face” (Shift + clic dreapta = meniul nativ; apăsare lungă pe touch).\n\nUn agent permanent (task programat orar) scrie și actualizează help-ul la fiecare funcție nouă, atât pe server, cât și pentru aplicație.',
         dece='Cerința proprietarului: help disponibil pe server pentru aplicație și server, cu „?” pe fiecare ecran și „ce e asta / ce face” la clic dreapta.',
         acc='- fiecare pagină are „?”;\n- fiecare element interactiv are tip în 7 limbi (script de acoperire);\n- toate cele 14 capitole ale aplicației sunt redate;\n- audit 10/10.',
         liv='Merge + deploy /ajutor/; HELP_INTEGRARE.md final → deblochează IOS-009.'),
    dict(id='IOS-009', slug='help-aplicatie-intrebare-clic-dreapta', exe='IOS', sol='SERVER', st='propusă', pr='P1', dep='SRV-013 (lista de chei tip.* din HELP_INTEGRARE.md)',
         contract='Site/docs/HELP_INTEGRARE.md pe feat/help (devine final după audit 10/10 + merge)',
         ce='În aplicație, pe FIECARE ecran (toate cele ~45 de *View.swift):\n1. butonul „?” (HelpButton există deja) către capitolul ecranului; pentru ecranele fără capitol, se adaugă capitole noi în HelpCatalog + cheile help.* în 7 limbi;\n2. „Ce e asta / Ce face” pe fiecare element interactiv: `.contextMenu` / apăsare lungă pe iPhone, iar pe iPad cu mouse sau trackpad clic dreapta (pointer secundar). Arată tip.<ecran>.<element>.what și .does + „Mai mult în ajutor” (deschide capitolul local sau https://3dscan.eva-org.com/ajutor/app/<topic>);\n3. cheile tip.* le adaugi în Resources/i18n (7 limbi) și le sincronizezi în seed-ul Site/db/app-i18n/, ca serverul să le redea pe /ajutor/.\n\nAgentul de help al serverului îți propune textele în §Discuție, la fiecare ecran nou.',
         dece='Cerința proprietarului: același help pe telefon și pe server, cu explicații contextuale pentru fiecare element.',
         acc='- 0 ecrane fără „?”;\n- 0 elemente interactive fără tip în 7 limbi (un script de verificare pe *View.swift);\n- /ajutor/app/ de pe server afișează aceleași texte ca aplicația.',
         liv='Commit pe app + sincronizarea seed-ului i18n + capturi.'),
    dict(id='SRV-014', slug='test-final-comun-wan-multi', exe='SERVER', sol='PROPRIETAR', st='acceptată', pr='P0', dep='SRV-001, SRV-002, SRV-004, SRV-006, IOS-003, IOS-005, IOS-006',
         contract='toate contractele finale',
         ce='Testul final comun, cu proprietarul de față, al conexiunii telefon ↔ server, în trei configurații:\n- (A) în LAN;\n- (B) în afara LAN (date mobile 4G/5G sau altă rețea Wi-Fi), prin https://3dscan.eva-org.com (Cloudflare Tunnel, inclusiv WebSocket /api/scene/ingest);\n- (C) mai multe telefoane: același utilizator pe 2+ telefoane și utilizatori diferiți pe telefoane diferite, simultan.\n\nSERVER pregătește: planul de test scris (TEST_FINAL_PLAN.md în acest folder), conturi de test, monitorizarea live în /admin/ (cine e conectat, de unde, ce fluxuri), colectarea dovezilor (sha256, latențe, contoare de cadre), probe de izolare între utilizatori.',
         dece='Cerința proprietarului: „la final să testăm împreună că funcționează conexiunea telefon–server și în afara LAN, nu doar în LAN, pentru același user, dar și pentru mai multe telefoane”.',
         acc='Pentru fiecare dintre A, B, C:\n- login;\n- sync inventar/bibliotecă convergent pe toate telefoanele aceluiași user, cu cursor seq, fără pierderi la offline → online;\n- fluxuri brute cu sha256 identic trimis = stocat;\n- latență și debit măsurate și raportate;\n- magazie: pachet exportat de pe telefonul 1 și încărcat pe telefonul 2;\n- telemetria vizibilă live în /admin/ per dispozitiv;\n- izolarea: userul X nu vede datele userului Y (test negativ);\n- reconectare după schimbarea rețelei (Wi-Fi ↔ 4G) fără pierderi.\n\nLimitele Cloudflare Tunnel pentru debitul brut se măsoară și se raportează onest.',
         liv='TEST_FINAL_RAPORT.md cu dovezi, semnat de ambele echipe; problemele găsite devin sarcini noi.'),
    dict(id='IOS-010', slug='test-final-comun-wan-multi', exe='IOS', sol='SERVER', st='propusă', pr='P0', dep='SRV-014',
         contract='TEST_FINAL_PLAN.md (îl scrie SERVER)',
         ce='Partea iOS a testului final SRV-014:\n- build instalat pe toate telefoanele disponibile (câte și ce modele: de raportat);\n- un mod de diagnostic în aplicație care arată rețeaua (LAN/WAN), latența către server, starea fiecărui flux și cursorul seq, ca să citim împreună rezultatele;\n- comutarea Wi-Fi ↔ 4G în timpul unei sesiuni;\n- pentru fiecare pas al planului: execuție + dovezi (capturi, id-uri) în TEST_FINAL_RAPORT.md.',
         dece='Testul final comun cerut de proprietar.',
         acc='Toate punctele din TEST_FINAL_PLAN.md executate, cu dovezi; ce nu se poate face (de exemplu, un singur telefon disponibil) e marcat not_run, cu motivul.',
         liv='Secțiunea iOS din TEST_FINAL_RAPORT.md.'),
]
for t in tasks:
    extra = ' Te rog să o treci în `acceptată` / `în discuție` / `blocată` și să răspunzi aici.' if t['exe'] == 'IOS' else ''
    body = f"""# {t['id']}: {t['slug'].replace('-', ' ')}

| Câmp | Valoare |
|---|---|
| ID | {t['id']} |
| Executant | {t['exe']} |
| Solicitant | {t['sol']} |
| Stare | {t['st']} |
| Prioritate | {t['pr']} |
| Depinde de | {t['dep']} |
| Contract | {t['contract']} |
| Creată | {T} |
| Ultima actualizare | {T} |

## Ce
{t['ce']}

## De ce
{t['dece']}

## Criterii de acceptare (pass/fail, măsurabile)
{t['acc']}

## Livrabil
{t['liv']}

## Discuție

### {T} — SERVER
Sarcină creată conform [PROTOCOL.md](../PROTOCOL.md).{extra}
"""
    with open(os.path.join(OUT, f"{t['id']}_{t['slug']}.md"), 'w', encoding='utf-8', newline='\n') as f:
        f.write(body)
print('\n'.join(f"| [{t['id']}](sarcini/{t['id']}_{t['slug']}.md) | {t['slug'].replace('-', ' ')} | {t['exe']} | {t['st']} | {t['pr']} | {t['dep']} |" for t in tasks))
