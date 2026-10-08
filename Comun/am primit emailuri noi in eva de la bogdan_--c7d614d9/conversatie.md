# am primit emailuri noi in eva de la bogdan?

ID: `01a0a69c-8e39-7d52-bddb-90fbc7d614d9`  
Proiect: Comun  
Export UTC: 2026-10-08T14:13:28.280906+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Utilizator

am primit emailuri noi in eva de la bogdan?

## Asistent

Verific în EVA emailurile recente de la Bogdan.

## Asistent

[external_agent_tool_call: ToolSearch]
input: {"query":"select:mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_search_emails,mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_search_contacts","max_results":5}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_search_emails]
input: {"sender":"bogdan","is_sent":false,"date_from":"2026-09-07","limit":20}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
{"items":[{"id":"6b7b1131-4ea1-482b-985c-deb6ec06fae8","account_email":"office@ac-wohnart.at","subject":"Notificare Creanta | Somatie de plata  | Schreiben A&C Wohnart\r\n [COVACIU/42222000]","from_name":"Capra Bogdan","from_address":"Bogdan.Capra@cerhahempel.com","to":["covaciu.gnm@gmail.com","office@ac-wohnart.at","cosmin.covaciu@ipec.ro"],"received_at":"2026-09-14T13:26:58Z","snippet":"Buna ziua,\r\n\r\nVă trimit acest e-mail pentru a vă informa cu privire la o scrisoare de somație primit","category":"fyi","labels":["1: To respond"],"folder":"Capra Bogdan","is_read":false,"is_starred":false,"is_sent":false,"has_attachments":true,"attachment_names":["image001.jpg","image002.jpg","image003.jpg","Mitteilung Commerz-Inkasso_A&C Wohnart.pdf"]},{"id":"bc17f5d2-08df-4f9a-87ea-22c520642896","account_email":"covaciu.gnm@gmail.com","subject":"Notificare Creanta | Somatie de plata  | Schreiben A&C Wohnart [COVACIU/42222000]","from_name":"Capra Bogdan","from_address":"Bogdan.Capra@cerhahempel.com","to":["covaciu.gnm@gmail.com","office@ac-wohnart.at","cosmin.covaciu@ipec.ro"],"received_at":"2026-09-14T13:25:39Z","snippet":"Buna ziua, Vă trimit acest e-mail pentru a vă informa cu privire la o scrisoare de somație primită astăzi, 14 septembrie 2026, la sediul CERHA HEMPEL, adresată societății A&amp;C Wohnart Immobilien","category":"fyi","labels":["UNREAD","CATEGORY_PERSONAL","INBOX","1: To respond","Label_38276"],"folder":"Capra Bogdan","is_read":false,"is_starred":false,"is_sent":false,"has_attachments":true,"attachment_names":["image001.jpg","image002.jpg","image003.jpg","Mitteilung Commerz-Inkasso_A&C Wohnart.pdf"]},{"id":"6fd019ac-52b7-4fcb-a569-2a9f3f54e9d1","account_email":"cosmin.covaciu@ipec.ro","subject":"Notificare Creanta | Somatie de plata  | Schreiben A&C Wohnart [COVACIU/42222000]","from_name":"Capra Bogdan","from_address":"Bogdan.Capra@cerhahempel.com","to":["covaciu.gnm@gmail.com","office@ac-wohnart.at","cosmin.covaciu@ipec.ro"],"received_at":"2026-09-14T10:27:06Z","snippet":"ATENȚIE: Acest e-mail provine din afara companiei. Nu dati click pe linkuri și nu deschideți atașame","category":"fyi","labels":["1: To respond"],"folder":"Capra Bogdan","is_read":true,"is_starred":false,"is_sent":false,"has_attachments":true,"attachment_names":["image001.jpg","image002.jpg","image003.jpg","Mitteilung Commerz-Inkasso_A&C Wohnart.pdf"]}],"total":3,"limit":20,"offset":0}
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: ToolSearch]
input: {"query":"select:mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_get_email","max_results":1}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_get_email]
input: {"email_id":"bc17f5d2-08df-4f9a-87ea-22c520642896"}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
{"id":"bc17f5d2-08df-4f9a-87ea-22c520642896","account_email":"covaciu.gnm@gmail.com","subject":"Notificare Creanta | Somatie de plata  | Schreiben A&C Wohnart [COVACIU/42222000]","from_name":"Capra Bogdan","from_address":"Bogdan.Capra@cerhahempel.com","to":["covaciu.gnm@gmail.com","office@ac-wohnart.at","cosmin.covaciu@ipec.ro"],"cc":[],"received_at":"2026-09-14T13:25:39Z","text":"Buna ziua,\r\n\r\nVă trimit acest e-mail pentru a vă informa cu privire la o scrisoare de somație primită astăzi, 14 septembrie 2026, la sediul CERHA HEMPEL, adresată societății A&C Wohnart Immobilien GmbH.\r\n\r\nScrisoarea a fost emisă de COMMERZ Inkasso GmbH (cu sediul în Vogelweiderstrasse 55, 5020 Salzburg) și poartă numărul de referință 2616052 (Poliță nr. X712261-2). Aceasta a fost trimisă la solicitarea cabinetului de avocatură Dr. Maritzcak (Postgasse 19/21, 1010 Viena), în numele Donau Versicherung AG (Schottenring 15, 1010 Viena).\r\n\r\nTermenul limită de plată este 21 septembrie 2026.\r\n\r\nVă rog să luați la cunoștiință.\r\n\r\nSalutari,\r\nBogdan\r\n\r\nMag. Bogdan Capra\r\nRechtsanwalt\r\n\r\nCERHA HEMPEL\r\nRechtsanwälte GmbH\r\nA-1010 Wien, Parkring 2\r\nTel.: +43/1/514 35-427\r\nMobil: +43/664/156 50 85\r\n\r\nbogdan.capra@cerhahempel.com<mailto:bogdan.capra@cerhahempel.com>\r\nwww.cerhahempel.com<http://www.cerhahempel.com/>\r\n\r\nSind Sie an CERHA HEMPEL Legal Updates interessiert? Dann melden Sie sich hier<http://www.cerhahempel.com/de/subscribe-to-updates> an.\r\n\r\n[Ein Bild, das Text, Vektorgrafiken, ClipArt enthält.    Automatisch generierte Beschreibung]<https://www.linkedin.com/company/2413345> [cid:image002.jpg@01DD445D.4B8222D0] <https://www.facebook.com/CERHAHEMPELWien>  [cid:image003.jpg@01DD445D.4B8222D0] <https://www.instagram.com/cerha_hempel/>\r\n\r\nCERHA  HEMPEL  Österreich   Bulgarien   Rumänien   Slowakei   Slowenien   Tschechische Republik   Ungarn\r\n\r\nDieses Email ist vertraulich. Details sind unter www.cerhahempel.com/disclaimer<http://www.cerhahempel.com/disclaimer> ersichtlich.\r\nFür sämtliche Leistungen von CERHA HEMPEL gelten unsere Allgemeinen Geschäftsbedingungen (siehe AGB<https://www.cerhahempel.com/de/agb>).\r\nRechtsform: GmbH, Sitz: Wien, FN 452529i, Handelsgericht Wien, Datenschutzerklärung<http://www.cerhahempel.com/de/datenschutz>\r\n\r\nVon: Berlakovich Bianka <Bianka.Berlakovich@cerhahempel.com>\r\nGesendet: Montag, 14. September 2026 15:18\r\nAn: Capra Bogdan <Bogdan.Capra@cerhahempel.com>\r\nBetreff: Eingelangt: Schreiben A&C Wohnart\r\n\r\nLieber Bogdan,\r\n\r\nAnbei ein Schreiben, das heute für A&C Wohnart eingelangt ist.\r\n\r\nLG\r\nBianka\r\n","truncated":false,"labels":["UNREAD","CATEGORY_PERSONAL","INBOX","1: To respond","Label_38276"],"category":"fyi","folder":"Capra Bogdan","thread_id":"1a0a01974bf2e7ce","is_read":false,"is_sent":false,"attachments":[{"id":"aee13271-73ef-479c-859b-75f96d387569","name":"image001.jpg","size":763,"content_type":"image/jpeg","has_text":false,"text_chars":0,"page_count":null,"text":null},{"id":"a4e660e4-30f7-49d7-94dd-235d72a92ae4","name":"image002.jpg","size":758,"content_type":"image/jpeg","has_text":false,"text_chars":0,"page_count":null,"text":null},{"id":"b22d1235-46fe-4229-aef3-8f05332ec19c","name":"image003.jpg","size":785,"content_type":"image/jpeg","has_text":false,"text_chars":0,"page_count":null,"text":null},{"id":"98a408cd-2d69-45ac-ac14-baacdfca87da","name":"Mitteilung Commerz-Inkasso_A&C Wohnart.pdf","size":224052,"content_type":"application/pdf","has_text":true,"text_chars":7894,"page_count":null,"text":"Commerz-In\nllllllllllllllllllllllllllllllllllSSCEINGELANGT\n14,$EP.7026\nCERHAHEMPELCerhaHempelRechtsanwälteGmbHCOMMERZInkassoGmbH\nVogelweiderstrasse55\n5020Salzburg\nTel.:+43/(662)875346-0\nFax:+43/(662)875346-22\noffice@commerz-inkasso.at\nFN54397x·UID:ATU33878300\nA&CWohnartImmobilienGmbH\nParkrina2\n1010Wien\nSalzburg,09.09.2026\nAktenzeichen:2616052Polizzennr:X712261-2\nNr:2044001194BEAUFTRAGTDURCH:\nKanzleiDr.Maritzcak,P...
[/external_agent_tool_result]

## Asistent

Da — ai un email nou de la **Bogdan Capra (CERHA HEMPEL)**, primit azi, 14 septembrie, pe toate cele trei adrese (covaciu.gnm@gmail.com, office@ac-wohnart.at și cosmin.covaciu@ipec.ro — e același mesaj, trimis către toate). E necitit și marcat de EVA cu „1: To respond".

**Subiect:** Notificare Creanță | Somație de plată | Schreiben A&C Wohnart

Pe scurt, ce anunță Bogdan:

- La sediul CERHA HEMPEL a sosit azi o **somație de plată adresată A&C Wohnart Immobilien GmbH**, emisă de firma de recuperări **COMMERZ Inkasso GmbH** din Salzburg (dosar 2616052, poliță X712261-2), la cererea cabinetului Dr. Maritzcak, în numele **Donau Versicherung AG**.
- Din PDF-ul atașat („Mitteilung Commerz-Inkasso_A&C Wohnart.pdf"): datoria este pentru **prime restante la asigurarea de locuință DONAU (Wohnhausversicherung)** — 2 × 1.591,81 € scadente la 09.09.2026, plus taxe și costuri de recuperare.
- **Total de plată: 3.734,34 €**, exclusiv în contul Commerz Inkasso (IBAN AT11 3500 0000 0310 7703, Raiffeisenverband Salzburg), cu mențiunea dosarului 2616052.
- **Termen limită: 21 septembrie 2026** — adică peste o săptămână; la depășire se adaugă costuri suplimentare.

Bogdan cere doar să iei la cunoștință. Dacă vrei, îți pot pregăti o ciornă de răspuns către el sau un rezumat al defalcării sumelor din somație.

## Utilizator

citeste atasamentul si salveazal in folderul de asigurare pentru Schaller gasse .
cauta firma Avocatului Kanzlei Dr. Maritzcak, Postgasse 19/21, 1010 Wien si pregateste un email p[rin care sa ii informezi asupra adresei noastre actuale si asupra detelor de contact telefon si email, si sa ii rogi sa ne trimita toate actele doveditoare pe care se bazeaza Forderung - DONAU Wohnhausversicherung fällig seit 09.09.2026
+ Betreibungskosten des Auftraggebers
+ Erhebungskosten
+ Allgemeine Bearbeitungsgebühr It. BGBI Nr. 141/1996
+ Mahnkosten It. BGBI Nr. 141/1996
+ Evidenzhaltungskosten It. BGBI Nr. 141/1996
+ Barauslagen
+8,00 % Verzugszinsen
Gesamt
€
€
€
€
€
€
€
€
€
3.183,62
30,00
14,40
308,50
124,26
49,68
4,74
19,14
3.734,34
de la Forderung - DONAU Wohnhausversicherung fällig seit 09.09.2026 ??? 
Sa ne trimita profesionist toate actele aferente si dovada semnari de catre noi cu firma Donau ... a unei asigurari

## Utilizator

[Request interrupted by user]

## Utilizator

citeste atasamentul si salveazal in folderul de asigurare pentru Schaller gasse .
cauta firma Avocatului Kanzlei Dr. Maritzcak, Postgasse 19/21, 1010 Wien si pregateste un email p[rin care sa ii informezi asupra adresei noastre actuale si asupra detelor de contact telefon si email, si sa ii rogi sa ne trimita toate actele doveditoare pe care se bazeaza Forderung - DONAU Wohnhausversicherung fällig seit 09.09.2026

* Betreibungskosten des Auftraggebers
* Erhebungskosten
* Allgemeine Bearbeitungsgebühr It. BGBI Nr. 141/1996
* Mahnkosten It. BGBI Nr. 141/1996
* Evidenzhaltungskosten It. BGBI Nr. 141/1996
* Barauslagen
+8,00 % Verzugszinsen
Gesamt
€
€
€
€
€
€
€
€
€
3.183,62
30,00
14,40
308,50
124,26
49,68
4,74
19,14
3.734,34
de la Forderung - DONAU Wohnhausversicherung fällig seit 09.09.2026 ???
Sa ne trimita profesionist toate actele aferente si dovada semnari de catre noi cu firma Donau ... a unei asigurari

## Asistent

Încep prin a-mi aminti datele firmei A&C Wohnart și a găsi folderul de asigurări pentru Schallergasse.

## Asistent

[external_agent_tool_call: Read]
file: C:\Users\User\.claude\projects\--192-168-100-169-Comun-\memory\ac-wohnart-firma-website.md
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
<system-reminder>This memory is 11 days old. Memories are point-in-time observations, not live state — claims about code behavior or file:line citations may be outdated. Verify against current code before asserting as fact.</system-reminder>
1	---
2	name: ac-wohnart-firma-website
3	description: Date firma A&C Wohnart Immobilien GmbH (FN 668224h) + pagina de prezentare creata pt. ac-wohnart.at (Schallergasse 35)
4	metadata: 
5	  node_type: memory
6	  type: project
7	  originSessionId: 90278fcb-fc07-402a-b633-f284ef895158
8	  modified: 2026-09-03T10:29:03.675Z
9	---
10	
11	**A&C Wohnart Immobilien GmbH** — firma austriaca a proiectului [[schallergasse-35-materiale]]:
12	- FN 668224h, Handelsgericht Wien, capital EUR 10.000, infiintata 03.12.2025 (Errichtungserklärung)
13	- Gesellschafter unic 100%: Cosmin-Adrian Covaciu (n. 19.10.1972)
14	- Geschäftsführer: Cosmin-Adrian Covaciu + Anastasia-Elena-Ekaterina Covaciu (n. 11.04.2001), ambii selbständig
15	- Geschäftsanschrift (Firmenbuch la 01.04.2026): Schallergasse 35, 1120 Wien; pe site-ul ac-wohnart.at apare Parkring 2, 1010 Wien
16	- Proprietar 1/1 al Schallergasse 35 (KG 01305, EZ 2235, TZ 466/2026, Kaufvertrag 20.02.2026)
17	- Acte firma: `D:\00. Downloads\Apartamente Viena\A&C Wohnart Immobilien GmbH\Acte Firma\`
18	
19	**Site de prezentare** (02.09.2026, HTML pur + style.css, stil identic cu index_de.html: Cinzel+Montserrat, auriu #c9a84c, fundal #faf9f7, fonturi si poze locale = merge offline):
20	- Folder de upload: `D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\Website\schallergasse35\` (index.html/projekte.html = DE, index_en.html/projects_en.html = EN cu switch „DE | EN" hardcoded, style.css, images\, fonts\)
21	- Se urca langa index_de.html → https://ac-wohnart.at/schallergasse35/
22	- Contact public: office@ac-wohnart.at, +43 665 670 550 45, Parkring 2, 1010 Wien (ca pe antetul firmei; butoane mailto)
23	- Oferta Schallergasse pe pagina: 8 apartamente de vanzare EG–3.OG (65–120 m²), Yoga-Studio de inchiriat, mansarda M1+M2 conform planselor, „in curand randari cu toate apartamentele"
24	
25	**Preferinta utilizator (cerinta explicita):** pe pagina publica se mentioneaza doar Cosmin-Adrian Covaciu; **Anastasia NU se mentioneaza**. Ton laudativ, obiective de viitor vagi („weitere Projekte in Wien"), fara numar/detalii concrete despre proiectele viitoare.
26	
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Read]
file: C:\Users\User\.claude\projects\--192-168-100-169-Comun-\memory\schallergasse-35-materiale.md
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
<system-reminder>This memory is 35 days old. Memories are point-in-time observations, not live state — claims about code behavior or file:line citations may be outdated. Verify against current code before asserting as fact.</system-reminder>
1	---
2	name: schallergasse-35-materiale
3	description: "Proiect renovare+mansardare Schallergasse 35 Wien - livrabile materiale Dedeman generate 05.08.2026, metodologie si contradictii de proiect"
4	metadata: 
5	  node_type: memory
6	  type: project
7	  originSessionId: eb7d487f-47dd-4d1a-aa04-a424862df570
8	  modified: 2026-08-10T11:15:21.721Z
9	---
10	
11	Proiect: renovare + mansardare imobil Schallergasse 35, 1120 Wien (Meidling), beneficiar Cosmin Covaciu / A&C Wohnart Immobilien GmbH. Arhitect: Madalina Giurgiu (MLINE SQUARE, Cluj).
12	
13	**ATENTIE cale schimbata (reorganizare 2026.08.10)**: folderul principal a fost reorganizat in 11 categorii (00.Proiect, 00.Claude, 01-09). `Arhitectura Madalina` a fost MUTAT in `...\03. Proiectare\Arhitectura Madalina`. Deci plansele+livrabilele Materiale sunt acum in `...\03. Proiectare\Arhitectura Madalina\2026.07.29\Materiale`. Index in `_INDEX_STRUCTURA.md`, jurnal reversibil in `_ORGANIZARE_manifest_2026-08-10.txt` (root). Nimic sters. NB: mutarea cu shutil.move a esuat pe Arhitectura Madalina (fisier blocat de Word deschis) -> recuperat (copie completa verificata in 03, ramasita duplicata stearsa); restul mutat cu os.rename atomic.
14	
15	**Livrabile generate 05.08.2026** in subfolderul `...\2026.07.29\Materiale`:
16	- `Lista_Materiale_Dedeman.xlsx` — 13 sheets (REZUMAT + 12 capitole), ~279 produse verificate pe dedeman.ro cu linkuri+preturi la 05.08.2026; total ~1.019.656 lei fara TVA / ~1.233.776 lei cu TVA (21%)
17	- `Materiale_Alternative_Premium.xlsx` — 279 produse recomandate + 462 alternative premium/super-premium
18	- `Deviz_General_pe_Incaperi.xlsx` — 332 linii pe 18 zone (deviz materiale principale ~838 mii lei)
19	- `Descriere_Centralizator_pe_Taburi.docx`, `Tehnologia_de_Aplicare.docx`, `Fise_Tehnice_Materiale.docx` (279 fise)
20	
21	**Metodologie-cheie**: plansa A.03 = etaj TIP -> cantitatile Ap.1/Ap.2 din Centralizator_cantitati.xlsx se multiplica x3 (etaje I-III); la fel IE03/IT03. TVA 21%. Pereti noi tip Z.1 = gips 1.5+vata bazaltica 10+gips 1.5 (GKBI la demisol/parter).
22	
23	**Contradictii de proiect nerezolvate** (marcate in livrabile, de urmarit):
24	1. Incalzire mansarda: Centralizator=UFH (tacker+sapa incalzita 257 mp) vs planse IT 06.2026="PLAN IN LUCRU", 65 radiatoare+12 CT gaz vs Baubeschreibung 2022 aprobat=pompe de caldura+UFH. Pozitiile marcate VARIANTA A/B.
25	2. Z.2 pe A.02 fara stratificatie in legenda.
26	3. Numerotare Top 8-11 (planse) vs Top 20-23 (autorizatie).
27	4. Recompartimentarile+yoga depasesc autorizatia -> Planwechsel MA37 obligatoriu; termen start lucrari ~aprilie/mai 2027 (§74 BO, neprelungibil).
28	
29	**Completari 05.08.2026 (dupa-amiaza)**: (1) `Nota_Clarificare_Sistem_Incalzire.docx` pentru arhitect (citate originale din cele 3 surse); (2) cap. 13_OTEL_STRUCTURAL informativ in lista; (3) toate livrabilele Madalinei copiate in `00.Proiect` (04. Ausfuehrungsplanung / 05. Haustechnik / 07.02 Materiallisten) cu denumiri GERMANE + sufix " M.v.3"; (4) cele 20 de planse PDF M.v.3 au textul romanesc TRADUS IN GERMANA in fisier (PyMuPDF, ~1.020 span-uri; Schnitt A-A nu are text de tradus - doar cote); (5) `Cerere_Oferta_Dedeman_Simplificata.xlsx` (258 pozitii pe producator A-Z) pentru reprezentantul de vanzari. Utilizatorul NU vrea Planwechsel - cere delimitarea legala BO Wien (§60/62/62a) a lucrarilor posibile fara schimbare de plan.
30	
31	**DESCOPERIRE MAJORA (analiza Bescheid 05.08.2026)**: planurile VIZATE ale autorizatiei (P2041, planse 004-008) contin deja recompartimentarea parterului (TOP 1+2) si DOUA VARIANTE de recompartimentare pt. etajele 1-3 (V1: 3 loc./etaj, V2: 2 loc./etaj) desenate ca lucrari noi => recompartimentarile se pot executa FARA Planwechsel daca urmeaza o varianta vizat...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: PowerShell]
description: List folder categories for Schallergasse 35 project
command: Get-ChildItem "D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)" -Directory | Select-Object -ExpandProperty Name
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
00.Claude
00.Proiect
01. Proprietate + Acte
02. Autorizatie + Planse oficiale
03. Proiectare
04. Firme + Executie
05. Asigurari
06. Utilitati
07. Poze + Video
08. Corespondenta
09. Arhiva ZIP-uri mari
Inbox
Website
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: PowerShell]
description: List contents of insurance folder
command: Get-ChildItem "D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari" -Recurse | Select-Object FullName, Length | Format-Table -AutoSize | Out-String -Width 300
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
FullName                                                                                                                                                                            Length 
--------                                                                                                                                                                            ------ 
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire                                                                    
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Gebäudeversicherung                                                                  
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\001 P2041_C_01 230420.dwg                                   1439926
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\002 P2041_C_02 230420.dwg                                   4015808
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\20260526163520179.pdf                                       386468 
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\20260526163644896.pdf                                       2073444
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\20260526163650446.pdf                                       1796793
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\20260526163655179.pdf                                       1791863
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\20260526163700146.pdf                                       1798103
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\20260526163706298.pdf                                       1836892
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\20260526163714572.pdf                                       1802398
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\20260526163719642.pdf                                       1819710
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\20260526163724473.pdf                                       1799439
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\20260526163729167.pdf                                       1790110
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\20260526163733983.pdf                                       1840340
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\814BC40FC7831FE197E21FDA1089ECC3_Polizzenkopie.pdf          262935 
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\814BC40FC7831FE197E21FDA108A0CC3_Polizzenkopie.pdf          202317 
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\B7280016C9961FE1988F3ADAC750FA7E_FolgeprämieStufe01.pdf     127487 
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\Firmă de administrare (Hausverwaltung).docx                 19741  
D:\00. Downloads\Apartamente...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: ToolSearch]
input: {"query":"select:mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_get_download_link,mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_list_mailboxes,mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_create_draft,WebSearch,WebFetch","max_results":6}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_get_download_link]
input: {"document_id":"98a408cd-2d69-45ac-ac14-baacdfca87da"}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_call: WebSearch]
input: {"query":"Kanzlei \"Maritzcak\" Rechtsanwalt Postgasse 19 1010 Wien Kontakt email"}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
Web search results for query: "Kanzlei "Maritzcak" Rechtsanwalt Postgasse 19 1010 Wien Kontakt email"

Links: [{"title":"Rechtsanwalt Ihor-Andrij MARITCZAK - (Allgemeinpraxis in )","url":"https://www.rechteasy.at/anwalt/ihor-andrij-maritczak/"},{"title":"Kanzlei Dr. Maritczak","url":"https://edikte.justiz.gv.at/edikte/ex/exedi3.nsf/0/e496ed8a7978e748c1258dc600372e58/$file/Beilagen%20komplett.pdf"},{"title":"Immo Gutachter und Sachverständiger - Schätzung von Immobilien - IMPRESSUM","url":"http://www.gutachter-immo.at/impressum/"},{"title":"Maraszto Milisits Rechtsanwälte OG | kontakt","url":"https://www.maraszto.at/de_kontakt.html"},{"title":"Dr. Maritczak Ihor-Andrij in 1010 Wien 1 (Innere Stadt) | herold.at","url":"https://www.herold.at/gelbe-seiten/wien/BSzH7/dr-maritczak-ihor-andrij/"},{"title":"ᐅ Rechtsanwalt Kanzlei Dr. Maritczak, Wien in Wien 8. Bezirk (Josefstadt)","url":"https://www.firma.at/www.maritczak.at_Wien-8-Bezirk-Josefstadt-Rechtsanwalt-Kanzlei-Dr-Maritczak-Wien-Treuhandbuch-Schadenersatzansprueche-Arbeitsrecht-Sozialrecht-Rechtsanwalt-Wien-Gesellschaftsrecht-Schuldnerberatung-Privatkonkurs-Rechtsberatung-Familienrecht-Immobilienrecht-Schu-_a027a7c4419e163ebaf2647a3f11f270"},{"title":"Dr. Maritczak, Rechtsanwalt Wien - Impressum | Rechtsanwalt Maritczak","url":"https://www.maritczak.at/impressum/"},{"title":"Kontakt aufnehmen - Rechtsanwalt Maritczak","url":"https://www.maritczak.at/kontakt/"},{"title":"Individuelle Rechtsberatung bei Dr. Maritczak, Rechtsanwalt Wien","url":"https://www.maritczak.at/"},{"title":"Ritter %26 Beck Rechtsanw%C3%A4lte","url":"https://en.wikipedia.org/wiki/Ritter_%26_Beck_Rechtsanw%C3%A4lte"}]

Based on the web search results, here is the contact information for Kanzlei Maritczak:

**Address:** Postgasse 19/21, A – 1010 Wien

**Telephone:** 01 – 715 20 09

**Fax:** 01 – 715 20 09 66

**Email:** office@maritczak.at

**Office Hours:** Mo-Fr, 9.00-14.00 Uhr or by appointment

The law office is headed by Dr. Ihor-Andrij Maritczak, MBA, Rechtsanwalt (Attorney at Law).


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
[/external_agent_tool_result]

## Asistent

[external_agent_tool_result]
{"url":"https://api.eva-org.com/api/v1/files/eyJkIjoiOThhNDA4Y2QtMmQ2OS00NWFjLWFjMTQtYmFhY2RmY2E4N2RhIiwiZSI6MTc4OTQ4MjIzMCwicyI6InRlbmFudF9jb3ZhY2l1X2dubV9nbWFpbF9jb20iLCJ1IjoiNDA0ZDliMTUtOWYzZS00ZWFkLThhZjgtMjA0YmVhNzJhZWQ3In0.9e80S1gq-O1IQgvANgyyRNVuVgL4onLPti4Po66Oxrc","expires_at":"2026-09-15T14:23:50Z","filename":"Mitteilung Commerz-Inkasso_A&C Wohnart.pdf","size":224052,"mime":"application/pdf","note":"Arată-i userului acest link ca adresă pe care o poate deschide direct."}
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: PowerShell]
description: Download somație PDF into Schallergasse insurance folder
command: Invoke-WebRequest -Uri "https://api.eva-org.com/api/v1/files/eyJkIjoiOThhNDA4Y2QtMmQ2OS00NWFjLWFjMTQtYmFhY2RmY2E4N2RhIiwiZSI6MTc4OTQ4MjIzMCwicyI6InRlbmFudF9jb3ZhY2l1X2dubV9nbWFpbF9jb20iLCJ1IjoiNDA0ZDliMTUtOWYzZS00ZWFkLThhZjgtMjA0YmVhNzJhZWQ3In0.9e80S1gq-O1IQgvANgyyRNVuVgL4onLPti4Po66Oxrc" -OutFile "D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\2026.09.14 Somatie Commerz-Inkasso 2616052 (Mitteilung Commerz-Inkasso_A&C Wohnart).pdf"; (Get-Item "D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\2026.09.14 Somatie Commerz-Inkasso 2616052 (Mitteilung Commerz-Inkasso_A&C Wohnart).pdf").Length
[/external_agent_tool_call]

## Asistent

[external_agent_tool_call: WebFetch]
input: {"url":"https://www.maritczak.at/kontakt/","prompt":"Extract the full contact details of this law office: name, address, phone, fax, email, office hours."}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
224052
[/external_agent_tool_result]

## Asistent

[external_agent_tool_result]
I appreciate your request, but I'm unable to extract the contact details you're looking for. The webpage content provided appears to be truncated with "[Content truncated due to length...]" shown where the actual contact information would be.

To help you find Rechtsanwalt Maritczak's contact details, I would need:
- The complete webpage content, or
- Direct access to their full contact page

If you can provide the untruncated content, I'll be happy to extract the name, address, phone, fax, email, and office hours following your specified guidelines.
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: WebFetch]
input: {"url":"https://www.maritczak.at/impressum/","prompt":"Extract the full contact details and legal info of this law office: name of lawyer, firm name, address, phone, fax, email."}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
I appreciate your request, but I need to be transparent: the web page content you provided appears to be truncated or incomplete. The excerpt shows only:

`Dr. Maritczak, Rechtsanwalt Wien - Impressum | Rechtsanwalt Maritczak`

This header alone doesn't contain the detailed contact information you're seeking. To extract the full details (lawyer name, firm name, address, phone, fax, email), I would need access to the complete page content, particularly the Impressum (legal notice) section, which typically contains this information.

**What I can confirm from the snippet:**
- Lawyer name: Dr. Maritczak
- Location: Wien (Vienna)
- Professional title: Rechtsanwalt (attorney)

To provide you with the complete contact details you need, please share the full web page content, especially the Impressum/legal information section.
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_create_draft]
input: {"account_email":"office@ac-wohnart.at","to":["office@maritczak.at"],"subject":"Aktenzeichen 2616052 / Polizzennr. X712261-2 (Donau Versicherung AG) – A&C Wohnart Immobilien GmbH: aktuelle Kontaktdaten und Ersuchen um Übermittlung sämtlicher anspruchsbegründender Unterlagen","body":"Sehr geehrter Herr Dr. Maritczak,\n\nwir nehmen Bezug auf das Schreiben der COMMERZ Inkasso GmbH vom 09.09.2026 (Aktenzeichen 2616052, Polizzennr. X712261-2, Nr. 2044001194), das in Ihrem Auftrag im Namen der Donau Versicherung AG an die A&C Wohnart Immobilien GmbH gerichtet wurde. Das Schreiben wurde an die Adresse Parkring 2, 1010 Wien zugestellt und hat uns erst am 14.09.2026 erreicht.\n\nZunächst dürfen wir Sie über unsere aktuellen Kontaktdaten informieren und ersuchen Sie, sämtliche künftige Korrespondenz in dieser Angelegenheit ausschließlich an diese zu richten:\n\n- A&C Wohnart Immobilien GmbH (FN 668224h, Handelsgericht Wien)\n- Geschäftsanschrift: Schallergasse 35, 1120 Wien\n- E-Mail: office@ac-wohnart.at\n- Telefon: +43 665 670 550 45\n\nWeiters ersuchen wir Sie höflich, uns sämtliche anspruchsbegründenden Unterlagen und Nachweise zu übermitteln, auf die sich die geltend gemachte Forderung in Höhe von insgesamt EUR 3.734,34 stützt, im Einzelnen:\n\n- Forderung DONAU Wohnhausversicherung, fällig seit 09.09.2026: EUR 3.183,62\n- Betreibungskosten des Auftraggebers: EUR 30,00\n- Erhebungskosten: EUR 14,40\n- Allgemeine Bearbeitungsgebühr lt. BGBl Nr. 141/1996: EUR 308,50\n- Mahnkosten lt. BGBl Nr. 141/1996: EUR 124,26\n- Evidenzhaltungskosten lt. BGBl Nr. 141/1996: EUR 49,68\n- Barauslagen: EUR 4,74\n- 8,00 % Verzugszinsen: EUR 19,14\n\nInsbesondere ersuchen wir um Übermittlung folgender Unterlagen:\n\n- des vollständigen Versicherungsvertrages samt Versicherungsantrag und Polizze,\n- des Nachweises des Vertragsabschlusses, insbesondere der von der A&C Wohnart Immobilien GmbH unterfertigten Vertragsunterlagen mit der Donau Versicherung AG,\n- der zugrunde liegenden Prämienvo...
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
{"id":"eedbb8b0-2488-4637-9cfb-0b798989217d","kind":"new","source":"chatgpt","status":"pending","account_id":"476c2aa5-b01c-48d1-9647-4e8b4be4ad61","account_email":"office@ac-wohnart.at","to":["office@maritczak.at"],"cc":[],"bcc":[],"subject":"Aktenzeichen 2616052 / Polizzennr. X712261-2 (Donau Versicherung AG) – A&C Wohnart Immobilien GmbH: aktuelle Kontaktdaten und Ersuchen um Übermittlung sämtlicher anspruchsbegründender Unterlagen","body":"Sehr geehrter Herr Dr. Maritczak,\n\nwir nehmen Bezug auf das Schreiben der COMMERZ Inkasso GmbH vom 09.09.2026 (Aktenzeichen 2616052, Polizzennr. X712261-2, Nr. 2044001194), das in Ihrem Auftrag im Namen der Donau Versicherung AG an die A&C Wohnart Immobilien GmbH gerichtet wurde. Das Schreiben wurde an die Adresse Parkring 2, 1010 Wien zugestellt und hat uns erst am 14.09.2026 erreicht.\n\nZunächst dürfen wir Sie über unsere aktuellen Kontaktdaten informieren und ersuchen Sie, sämtliche künftige Korrespondenz in dieser Angelegenheit ausschließlich an diese zu richten:\n\n- A&C Wohnart Immobilien GmbH (FN 668224h, Handelsgericht Wien)\n- Geschäftsanschrift: Schallergasse 35, 1120 Wien\n- E-Mail: office@ac-wohnart.at\n- Telefon: +43 665 670 550 45\n\nWeiters ersuchen wir Sie höflich, uns sämtliche anspruchsbegründenden Unterlagen und Nachweise zu übermitteln, auf die sich die geltend gemachte Forderung in Höhe von insgesamt EUR 3.734,34 stützt, im Einzelnen:\n\n- Forderung DONAU Wohnhausversicherung, fällig seit 09.09.2026: EUR 3.183,62\n- Betreibungskosten des Auftraggebers: EUR 30,00\n- Erhebungskosten: EUR 14,40\n- Allgemeine Bearbeitungsgebühr lt. BGBl Nr. 141/1996: EUR 308,50\n- Mahnkosten lt. BGBl Nr. 141/1996: EUR 124,26\n- Evidenzhaltungskosten lt. BGBl Nr. 141/1996: EUR 49,68\n- Barauslagen: EUR 4,74\n- 8,00 % Verzugszinsen: EUR 19,14\n\nInsbesondere ersuchen wir um Übermittlung folgender Unterlagen:\n\n- des vollständigen Versicherungsvertrages samt Versicherungsantrag und Polizze,\n- des Nachweises des Vertragsabschlusses, insbesondere der von der A&C Wohnart Immobilien GmbH unterfertigten Vertragsunterlagen mit der Donau Versicherung AG,\n- der zugrunde liegenden Prämienvorschreibungen und Mahnungen samt Zustellnachweisen,\n- einer nachvollziehbaren Aufschlüsselung samt Rechtsgrundlage der einzelnen Kosten- und Gebührenpositionen.\n\nBis zur vollständigen Übermittlung und Prüfung dieser Unterlagen betrachten wir die Forderung als nicht nachgewiesen und behalten uns sämtliche Rechte vor. Wir ersuchen zugleich um entsprechende Fristerstreckung hinsichtlich des im Schreiben genannten Zahlungstermins 21.09.2026, bis uns die angeforderten Unterlagen vollständig vorliegen.\n\nWir danken für Ihre Bemühungen und stehen für Rückfragen gerne zur Verfügung.\n\nMit freundlichen Grüßen\n\nCosmin Adrian Covaciu","attachments":[],"reply_to_email_id":null,"created_at":"2026-09-14T14:26:05.760380Z","updated_at":"2026-09-14T14:26:05.760380Z","note":"Salvată în EVA → Drafts; trimiterea se face din EVA."}
[/external_agent_tool_result]

## Asistent

Gata — ambele sarcini sunt finalizate.

**1. Atașamentul salvat.** Somația (224 KB) e acum în:
[2026.09.14 Somatie Commerz-Inkasso 2616052 (Mitteilung Commerz-Inkasso_A&C Wohnart).pdf](D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\05. Asigurari\Asigurare cladire\2026.09.14 Somatie Commerz-Inkasso 2616052 (Mitteilung Commerz-Inkasso_A&C Wohnart).pdf)

**2. Cabinetul avocatului găsit.** Ortografia corectă este **Dr. Ihor-Andrij Maritczak** (în somație e scris greșit „Maritzcak"): Postgasse 19/21, 1010 Wien, tel. 01-715 20 09, e-mail **office@maritczak.at**.

**3. Ciorna creată** în EVA → Drafts, de pe **office@ac-wohnart.at** către office@maritczak.at, în germană. Conține:
- datele actuale de contact: A&C Wohnart Immobilien GmbH (FN 668224h), Schallergasse 35, 1120 Wien, office@ac-wohnart.at, +43 665 670 550 45, cu rugămintea ca toată corespondența viitoare să meargă acolo;
- cererea de a primi toate actele doveditoare pentru fiecare poziție din defalcarea de 3.734,34 € (creanța DONAU 3.183,62 € + toate taxele și dobânzile, enumerate exact);
- explicit: contractul de asigurare complet cu cererea de asigurare (Antrag) și polița, **dovada semnării de către A&C Wohnart a contractului cu Donau Versicherung**, somațiile/facturile de primă cu dovezi de comunicare, și temeiul legal al fiecărei taxe;
- o cerere de prelungire a termenului de plată (21.09.2026) până la primirea și verificarea actelor.

O trimiți din EVA → Drafts.

**Un lucru de știut înainte să trimiți:** în folderul de asigurări ai deja acte pentru exact polița din somație — două fișiere „Polizzenkopie", unul „FolgeprämieStufe01" și scrisoarea ta „Polizze Nr. 2044001194 – Ersuchen um prämienreduzierte...". Deci polița DONAU 2044001194 există și o cunoașteți (probabil preluată odată cu cumpărarea imobilului — în Austria asigurarea clădirii trece automat la cumpărător, § 69 VersVG). Cererea de acte rămâne perfect legitimă, dar argumentul „nu am semnat nimic cu Donau" ar putea fi ușor contrat de ei; e bine să verifici acele PDF-uri înainte. Dacă vrei, le pot citi și îți fac un rezumat: cine figurează ca deținător al poliței, de când și pe ce sume.

Surse: [maritczak.at/kontakt](https://www.maritczak.at/kontakt/), [herold.at](https://www.herold.at/gelbe-seiten/wien/BSzH7/dr-maritczak-ihor-andrij/)

## Utilizator

@"D:\00. Downloads\Apartamente Viena/" @"C:\Users\User/"
am atasat folderul unde gasesti datele despre proprietate 
D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)
si in folderul 
D:\00. Downloads\Apartamente Viena
gasesti toate discutiile legate de AC Wohnart  si alte inverstitii 

aici gasesti actele firmei 
D:\00. Downloads\Apartamente Viena\A&C Wohnart Immobilien GmbH

## Asistent

Mulțumesc — am acces acum la toate cele trei locații. Continui cu ce am propus: citesc actele poliței DONAU din folderul de asigurări ca să vedem exact cine figurează ca titular, de când și pe ce sume — ca să știm cât de solidă e poziția noastră înainte să trimiți emailul către Dr. Maritczak.

## Asistent

[external_agent_tool_call: Read]
file: C:\Users\User\.claude\projects\--192-168-100-169-Comun-\memory\ocr-doc-tooling.md
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
<system-reminder>This memory is 68 days old. Memories are point-in-time observations, not live state — claims about code behavior or file:line citations may be outdated. Verify against current code before asserting as fact.</system-reminder>
1	---
2	name: ocr-doc-tooling
3	description: Unelte instalate pe mașina User pt. extragere text + OCR din PDF/DOC/DOCX (util la scanări)
4	metadata: 
5	  node_type: memory
6	  type: reference
7	  originSessionId: 38a50c93-7709-4592-b527-89911c8a415b
8	---
9	
10	Pe această mașină (Windows, `\\192.168.100.169\Comun`, drive `Z:`) sunt disponibile permanent unelte de extragere text și OCR:
11	
12	- **python 3.12**: `C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe` (în PATH ca `python`; NU `python3`). PowerShell NU e disponibil ca tool — folosește Bash (Git Bash).
13	- **pdftotext** și **antiword** în `/mingw64/bin` (Git Bash) — text din PDF cu strat de text, respectiv `.doc` vechi.
14	- **OCR instalat prin pip** (pentru PDF-uri scanate fără text): `rapidocr-onnxruntime` + `pymupdf` (fitz) + opencv/onnxruntime. Pipeline: PyMuPDF randează pagina → RapidOCR citește. Funcționează offline, citește bine română.
15	- docx/xlsx/odt = citite ca zip (xml). CNP validabil cu cifra de control (ponderi 2795 1463 5827 9).
16	
17	Notă: Z: e mare (~500k fișiere) — `find /z` durează câteva minute; rulează în background. „CV" în denumiri poate însemna și **Contract Vânzare-Cumpărare**, nu doar Curriculum Vitae — verifică conținutul.
18	
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: List correspondence folder structure
command: ls "D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/08. Corespondenta"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
20250825195435103.pdf
Rfk10069MM202500328.pdf
eml
s.schwarz@lv-r.at
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Check eml subfolder naming convention
command: ls "D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/08. Corespondenta/eml" 2>/dev/null | head -30
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/08. Corespondenta/eml
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Write]
file: D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\08. Corespondenta\2026.09.14 Somatie Commerz-Inkasso (Donau)\2026.09.14 Email primit - Capra Bogdan (CERHA HEMPEL) - Notificare somatie.txt
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
File created successfully at: D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\08. Corespondenta\2026.09.14 Somatie Commerz-Inkasso (Donau)\2026.09.14 Email primit - Capra Bogdan (CERHA HEMPEL) - Notificare somatie.txt (file state is current in your context — no need to Read it back)
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Write]
file: D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\08. Corespondenta\2026.09.14 Somatie Commerz-Inkasso (Donau)\2026.09.14 Email trimis (ciorna EVA) - catre Dr. Maritczak - cerere acte doveditoare.txt
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
File created successfully at: D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\08. Corespondenta\2026.09.14 Somatie Commerz-Inkasso (Donau)\2026.09.14 Email trimis (ciorna EVA) - catre Dr. Maritczak - cerere acte doveditoare.txt (file state is current in your context — no need to Read it back)
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Copy somație PDF into correspondence folder and list it
command: cp "D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/05. Asigurari/Asigurare cladire/2026.09.14 Somatie Commerz-Inkasso 2616052 (Mitteilung Commerz-Inkasso_A&C Wohnart).pdf" "D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/08. Corespondenta/2026.09.14 Somatie Commerz-Inkasso (Donau)/" && ls "D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/08. Corespondenta/2026.09.14 Somatie Commerz-Inkasso (Donau)/"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
2026.09.14 Email primit - Capra Bogdan (CERHA HEMPEL) - Notificare somatie.txt
2026.09.14 Email trimis (ciorna EVA) - catre Dr. Maritczak - cerere acte doveditoare.txt
2026.09.14 Somatie Commerz-Inkasso 2616052 (Mitteilung Commerz-Inkasso_A&C Wohnart).pdf
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_search_emails]
input: {"query":"Donau Versicherung","limit":50}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_call: mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_search_emails]
input: {"query":"2044001194","limit":50}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
{"items":[{"id":"eedbb8b0-2488-4637-9cfb-0b798989217d","account_email":"office@ac-wohnart.at","subject":"Aktenzeichen 2616052 / Polizzennr. X712261-2 (Donau Versicherung AG) – A&C Wohnart Immobilien GmbH: aktuelle Kontaktdaten und Ersuchen um Übermittlung sämtlicher anspruchsbegründender Unterlagen","from_name":"office@ac-wohnart.at","from_address":"office@ac-wohnart.at","to":["office@maritczak.at"],"received_at":"2026-09-14T14:26:05.864278Z","snippet":"Sehr geehrter Herr Dr. Maritczak,\n\nwir nehmen Bezug auf das Schreiben der COMMERZ Inkasso GmbH vom 0","category":null,"labels":["DRAFT"],"folder":"Drafts","is_read":true,"is_starred":false,"is_sent":false,"has_attachments":false,"attachment_names":[]},{"id":"6b7b1131-4ea1-482b-985c-deb6ec06fae8","account_email":"office@ac-wohnart.at","subject":"Notificare Creanta | Somatie de plata  | Schreiben A&C Wohnart\r\n [COVACIU/42222000]","from_name":"Capra Bogdan","from_address":"Bogdan.Capra@cerhahempel.com","to":["covaciu.gnm@gmail.com","office@ac-wohnart.at","cosmin.covaciu@ipec.ro"],"received_at":"2026-09-14T13:26:58Z","snippet":"Buna ziua,\r\n\r\nVă trimit acest e-mail pentru a vă informa cu privire la o scrisoare de somație primit","category":"fyi","labels":["1: To respond"],"folder":"Capra Bogdan","is_read":false,"is_starred":false,"is_sent":false,"has_attachments":true,"attachment_names":["image001.jpg","image002.jpg","image003.jpg","Mitteilung Commerz-Inkasso_A&C Wohnart.pdf"]},{"id":"bc17f5d2-08df-4f9a-87ea-22c520642896","account_email":"covaciu.gnm@gmail.com","subject":"Notificare Creanta | Somatie de plata  | Schreiben A&C Wohnart [COVACIU/42222000]","from_name":"Capra Bogdan","from_address":"Bogdan.Capra@cerhahempel.com","to":["covaciu.gnm@gmail.com","office@ac-wohnart.at","cosmin.covaciu@ipec.ro"],"received_at":"2026-09-14T13:25:39Z","snippet":"Buna ziua, Vă trimit acest e-mail pentru a vă informa cu privire la o scrisoare de somație primită astăzi, 14 septembrie 2026, la sediul CERHA HEMPEL, adresată societății A&amp;C Wohnart Immobilien","category":"fyi","labels":["UNREAD","CATEGORY_PERSONAL","INBOX","1: To respond","Label_38276"],"folder":"Capra Bogdan","is_read":true,"is_starred":false,"is_sent":false,"has_attachments":true,"attachment_names":["image001.jpg","image002.jpg","image003.jpg","Mitteilung Commerz-Inkasso_A&C Wohnart.pdf"]},{"id":"6fd019ac-52b7-4fcb-a569-2a9f3f54e9d1","account_email":"cosmin.covaciu@ipec.ro","subject":"Notificare Creanta | Somatie de plata  | Schreiben A&C Wohnart [COVACIU/42222000]","from_name":"Capra Bogdan","from_address":"Bogdan.Capra@cerhahempel.com","to":["covaciu.gnm@gmail.com","office@ac-wohnart.at","cosmin.covaciu@ipec.ro"],"received_at":"2026-09-14T10:27:06Z","snippet":"ATENȚIE: Acest e-mail provine din afara companiei. Nu dati click pe linkuri și nu deschideți atașame","category":"fyi","labels":["1: To respond"],"folder":"Capra Bogdan","is_read":true,"is_starred":false,"is_sent":false,"has_attachments":true,"attachment_names":["image001.jpg","image002.jpg","image003.jpg","Mitteilung Commerz-Inkasso_A&C Wohnart.pdf"]},{"id":"1bc16469-dcb3-4cf3-819a-9a75f081bbc1","account_email":"office@ac-wohnart.at","subject":"WG: Prämienzahlung Partnernummer: 2923354322 Polizze: 2044001194","from_name":"Loschy Cornelia","from_address":"C.Loschy@donauversicherung.at","to":["office@ac-wohnart.at"],"received_at":"2026-07-20T10:19:53Z","snippet":"Sehr geehrte Damen und Herren,\r\n\r\nwir haben auf Ihre beiliegende Nachricht vom 01.07.2026 am 10.07.2","category":"fyi","labels":["3: Fyi"],"folder":"Loschy Cornelia","is_read":true,"is_starred":false,"is_sent":false,"has_attachments":true,"attachment_names":["Polizze Nr. 2044001194 – Ersuchen um prämienreduzierte.pdf"]},{"id":"d10bdd3f-8439-45f0-a061-e222c9290266","account_email":"cosmin@ig.ro","subject":"WG: WG: A&C Wohnart Immobilien GmbH 2044001194 Sonstiges ID:12828728","from_name":"Pfeiffer Mario","from_address":"M.Pfeiffer@donauversicherung.at","to":["cosmin@ig.ro"],"received_at":"2026-07-14T0...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Search Apartamente Viena folder for Donau/policy files
command: cd "D:/00. Downloads/Apartamente Viena" && find . -iname "*donau*" -not -path "*/.tmp.driveupload/*" 2>/dev/null; echo "---DON_SHU/polizze---"; find . -iname "*polizze*" -o -iname "*DON_SHU*" -o -iname "*X712261*" -o -iname "*2044001194*" 2>/dev/null | grep -v ".tmp.driveupload" | head -40; echo "---Asigurare Austria 2026---"; ls "Asigurare Austria 2026" 2>/dev/null
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
{"items":[{"id":"eedbb8b0-2488-4637-9cfb-0b798989217d","account_email":"office@ac-wohnart.at","subject":"Aktenzeichen 2616052 / Polizzennr. X712261-2 (Donau Versicherung AG) – A&C Wohnart Immobilien GmbH: aktuelle Kontaktdaten und Ersuchen um Übermittlung sämtlicher anspruchsbegründender Unterlagen","from_name":"office@ac-wohnart.at","from_address":"office@ac-wohnart.at","to":["office@maritczak.at"],"received_at":"2026-09-14T14:26:05.864278Z","snippet":"Sehr geehrter Herr Dr. Maritczak,\n\nwir nehmen Bezug auf das Schreiben der COMMERZ Inkasso GmbH vom 0","category":null,"labels":["DRAFT"],"folder":"Drafts","is_read":true,"is_starred":false,"is_sent":false,"has_attachments":false,"attachment_names":[]},{"id":"1bc16469-dcb3-4cf3-819a-9a75f081bbc1","account_email":"office@ac-wohnart.at","subject":"WG: Prämienzahlung Partnernummer: 2923354322 Polizze: 2044001194","from_name":"Loschy Cornelia","from_address":"C.Loschy@donauversicherung.at","to":["office@ac-wohnart.at"],"received_at":"2026-07-20T10:19:53Z","snippet":"Sehr geehrte Damen und Herren,\r\n\r\nwir haben auf Ihre beiliegende Nachricht vom 01.07.2026 am 10.07.2","category":"fyi","labels":["3: Fyi"],"folder":"Loschy Cornelia","is_read":true,"is_starred":false,"is_sent":false,"has_attachments":true,"attachment_names":["Polizze Nr. 2044001194 – Ersuchen um prämienreduzierte.pdf"]},{"id":"d10bdd3f-8439-45f0-a061-e222c9290266","account_email":"cosmin@ig.ro","subject":"WG: WG: A&C Wohnart Immobilien GmbH 2044001194 Sonstiges ID:12828728","from_name":"Pfeiffer Mario","from_address":"M.Pfeiffer@donauversicherung.at","to":["cosmin@ig.ro"],"received_at":"2026-07-14T04:54:54Z","snippet":"Sehr geehrter Herr Covaciu,\r\n\r\nbezugnehmend auf Ihre untenstehende Nachricht kann ich Ihnen mitteile","category":"fyi","labels":["1: To respond"],"folder":"Pfeiffer Mario","is_read":true,"is_starred":false,"is_sent":false,"has_attachments":false,"attachment_names":[]},{"id":"6706f86a-b245-495b-8637-f692156e29c7","account_email":"cosmin@ig.ro","subject":"WG: WG: A&C Wohnart Immobilien GmbH 2044001194 Sonstiges ID:12828728","from_name":"Loschy Cornelia","from_address":"C.Loschy@donauversicherung.at","to":["cosmin@ig.ro"],"received_at":"2026-07-10T10:59:21Z","snippet":"Sehr geehrter Herr Covaciu,\r\n\r\nWir beziehen uns auf Ihr Schreiben zum Vertrag mit der Polizzennummer","category":"fyi","labels":["3: Fyi"],"folder":"Loschy Cornelia","is_read":true,"is_starred":false,"is_sent":false,"has_attachments":false,"attachment_names":[]},{"id":"2dd29262-8d57-41c2-81e5-80e3b909d32e","account_email":"cosmin@ig.ro","subject":"Re: WG: A&C Wohnart Immobilien GmbH 2044001194 Sonstiges ID:12828728","from_name":"cosmin@ig.ro","from_address":"cosmin@ig.ro","to":["C.Loschy@donauversicherung.at"],"received_at":"2026-07-01T04:42:36.971285Z","snippet":"Betreff: Polizze Nr. 2044001194 – Ersuchen um prämienreduzierte Basisdeckung ab 01.07.2026 / Zahlung","category":"fyi","labels":["SENT","1: To respond"],"folder":"C.Loschy@donauversicherung.at","is_read":true,"is_starred":false,"is_sent":true,"has_attachments":false,"attachment_names":[]},{"id":"30da3512-03a0-4d68-b25b-a7c58ac482d8","account_email":"cosmin@ig.ro","subject":"Re: WG: A&C Wohnart Immobilien GmbH 2044001194 Sonstiges ID:12828728","from_name":"Cosmin Covaciu","from_address":"cosmin@ig.ro","to":["C.Loschy@donauversicherung.at"],"received_at":"2026-07-01T04:42:35Z","snippet":"Betreff: Polizze Nr. 2044001194 – Ersuchen um prämienreduzierte Basisdeckung ab 01.07.2026 / Zahlung","category":"fyi","labels":["SENT","1: To respond"],"folder":"C.Loschy@donauversicherung.at","is_read":true,"is_starred":false,"is_sent":true,"has_attachments":false,"attachment_names":[]},{"id":"16a82de2-ecdb-4c4a-ac9b-17a67ab3f24f","account_email":"cosmin@ig.ro","subject":"WG: A&C Wohnart Immobilien GmbH 2044001194 Sonstiges ID:12828728","from_name":"Loschy Cornelia","from_address":"C.Loschy@donauversicherung.at","to":["cosmin@ig.ro"],"received_at":"2026-06-10T05:09:18Z","snippet":"Seh...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_result]
./00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/08. Corespondenta/2026.09.14 Somatie Commerz-Inkasso (Donau)
---DON_SHU/polizze---
./00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/05. Asigurari/Asigurare cladire/814BC40FC7831FE197E21FDA1089ECC3_Polizzenkopie.pdf
./00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/05. Asigurari/Asigurare cladire/814BC40FC7831FE197E21FDA108A0CC3_Polizzenkopie.pdf
./00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/05. Asigurari/Asigurare cladire/Polizze Nr. 2044001194 – Ersuchen um prämienreduzierte.docx
./00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/05. Asigurari/Asigurare cladire/Polizze Nr. 2044001194 – Ersuchen um prämienreduzierte.pdf
./00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/05. Asigurari/Asigurare cladire/Schalle_1080_DON_SHU_2044001194_2939905718.pdf
./00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/05. Asigurari/Asigurare cladire/Traducere Schalle_1080_DON_SHU_2044001194_2939905718 ro.pdf
---Asigurare Austria 2026---
SKM_C300i25102310011 (002).pdf
SVS.pdf
WKS.pdf
desktop.ini
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_get_email]
input: {"email_id":"16a82de2-ecdb-4c4a-ac9b-17a67ab3f24f"}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_call: mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_get_email]
input: {"email_id":"d10bdd3f-8439-45f0-a061-e222c9290266"}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
{"id":"16a82de2-ecdb-4c4a-ac9b-17a67ab3f24f","account_email":"cosmin@ig.ro","subject":"WG: A&C Wohnart Immobilien GmbH 2044001194 Sonstiges ID:12828728","from_name":"Loschy Cornelia","from_address":"C.Loschy@donauversicherung.at","to":["cosmin@ig.ro"],"cc":[],"received_at":"2026-06-10T05:09:18Z","text":"Sehr geehrter Herr Covaciu,\r\n\r\nbezugnehmend auf Ihre untenstehende Nachricht teilen wir Ihnen mit, dass gegenständlicher Vertrag bereits auf die A&C Wohnart Immobilien GmbH umgeschrieben wurde.\r\n\r\nIm Anhang senden wir Ihnen die entsprechenden Änderungspolizzen, welche Sie auch auf dem Postweg erhalten. Beiliegend ebenfalls der Zahlschein.\r\n\r\nDie aktuelle Forderung setzt sich aus der Vorschreibung 01.04.2026 – 01.07.2026 + Vorschreibung 01.07.2026 – 01.10.2026 zusammen.\r\n\r\nDa zum Zeitpunkt der Vertragsumstellung die Prämie offen war, wurde auch automatisch ein entsprechendes Mahnschreiben versandt. – siehe bitte letzter Anhang.\r\n\r\nBitte den offenen Betrag bis spätestens 18.06.2026 begleichen, da sonst kein Versicherungsschutz mehr besteht.\r\n\r\nWir hoffen hiermit behilflich gewesen zu sein.\r\nFreundliche Grüße\r\nCornelia Loschy\r\nVertragsverwaltung Gewerbe | Fachabteilung SHU\r\nDONAU Versicherung AG\r\nVienna Insurance Group\r\nGeneraldirektion\r\n1010 Wien, Schottenring 15\r\nTelefon  +43 50 330 – 72689\r\nE-Mail    c.loschy@donauversicherung.at<mailto:c.loschy@donauversicherung.at>\r\n\r\nIch will zur DONAU.\r\nFacebook<https://www.facebook.com/DONAUVersicherungAG> | Instagram<https://www.instagram.com/donauversicherung/> | LinkedIn<https://at.linkedin.com/company/donau-versicherung-ag---vienna-insurance-group> | Xing<https://www.xing.com/companies/donauversicherungagviennainsurancegroup> | kununu<https://www.kununu.com/at/donau-versicherung-vienna-insurance-group3> | Youtube<https://www.youtube.com/channel/UCBi9pKhXpXM1jfNQrTOmlyw>\r\n\r\nHier geht´s zu Meine DONAU<https://www.meinedonau.at/>\r\n\r\n\r\nFirmensitz: 1010 Wien, Schottenring 15\r\nHandelsgericht Wien, FN 32002m\r\nwww.donauversicherung.at/<http://www.donauversicherung.at/>\r\nDatenschutzinformation<https://www.donauversicherung.at/datenschutz/>\r\n\r\n\r\n\r\n----------Ursprüngliche Nachricht----------\r\n\r\nVon: Cosmin Covaciu [mailto:cosmin@ig.ro]\r\nGesendet: Mo 8. Jun 2026, 17:43:19\r\nAn: donau@donauversicherung.at<mailto:donau@donauversicherung.at>\r\nBetreff: Eigentümerwechsel und Klärung des Versicherungsstatus – Polizze Nr. 2044001194 / X712261 – Schallergasse 35, 1120 Wien\r\n\r\nWichtigkeit: Dringlich\r\n\r\nSehr geehrte Damen und Herren,\r\n\r\nwir wenden uns an Sie als neue Eigentümerseite der Liegenschaft Schallergasse 35, 1120 Wien, um die bestehende Versicherungssituation rasch, sachlich und rechtssicher zu klären.\r\n\r\nDie Liegenschaft wurde von der A&C Wohnart Immobilien GmbH, FN 668224 h, erworben.\r\nDer Eigentumserwerb ergibt sich aus dem Kaufvertrag 405/2026 vom 20.02.2026 sowie aus der grundbücherlichen Eintragung des Eigentumsrechts.\r\nDen aktuellen Grundbuchsauszug sowie die aktuellen Firmenbuchdaten der A&C Wohnart Immobilien GmbH übermitteln wir Ihnen in der Anlage.\r\n\r\nUns liegt die DONAU Wohnhausversicherung zur Polizze Nr. 2044001194 / bisherige Polizze Nr. X712261, Rahmenvertragsnummer 2900010498, betreffend die Liegenschaft Schallergasse 35, 1120 Wien, vor. Laut Polizze ist als Versicherungsnehmerin jedoch weiterhin die Schallergasse 35 Immobilienbesitz GmbH & Co KG, c/o Hofhans Immobilienmanagement GmbH, Albertgasse 32/9, 1080 Wien, angeführt.\r\n\r\nHiermit zeigen wir Ihnen den Eigentümerwechsel der Liegenschaft formal an.\r\n\r\nNach den uns vorliegenden Unterlagen und der Korrespondenz mit der früheren Verwaltung wurde uns mitgeteilt, dass gebäudebezogene Verträge insbesondere mit der Versicherung und dem Winterdienst bestanden haben. Zugleich wurde uns schriftlich mitgeteilt, dass die gegenständliche Versicherungspolizze nach damaligem Verständnis bereits durch die frühere Eigentümerseite h...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_result]
{"id":"d10bdd3f-8439-45f0-a061-e222c9290266","account_email":"cosmin@ig.ro","subject":"WG: WG: A&C Wohnart Immobilien GmbH 2044001194 Sonstiges ID:12828728","from_name":"Pfeiffer Mario","from_address":"M.Pfeiffer@donauversicherung.at","to":["cosmin@ig.ro"],"cc":["geko.wien@donauversicherung.at"],"received_at":"2026-07-14T04:54:54Z","text":"Sehr geehrter Herr Covaciu,\r\n\r\nbezugnehmend auf Ihre untenstehende Nachricht kann ich Ihnen mitteilen, dass wir die Sparten Leitungswasser und Mieten-BU aufgrund Risikowegfall ausschließen könnten.\r\nBitte dazu um Übermittlung folgender Unterlagen:\r\n\r\n-              Baubewilligung,\r\n-              Baubeschreibung\r\n-              Bestätigung eines Installateurs über die abgesperrte bzw. gesicherte wasserführende Installation\r\n\r\nFür weitere Fragen stehe ich gerne zur Verfügung.\r\n\r\nFreundliche Grüße\r\n\r\nMario Pfeiffer\r\nGewerbekoordinator  |  LD Wien\r\n\r\nDONAU Versicherung AG\r\nVienna Insurance Group\r\nLandesdirektion Wien\r\n1010 Wien, Schottenring 15\r\n\r\nTelefon   +43 50 330 – 72707\r\nMobil      +43 50 330 90 - 72707\r\nE-Mail     m.pfeiffer@donauversicherung.at<mailto:m.pfeiffer@donauversicherung.at>\r\n\r\nIch will zur DONAU.\r\nFacebook<https://www.facebook.com/DONAUVersicherungAG> | Instagram<https://www.instagram.com/donauversicherung/> | LinkedIn<https://at.linkedin.com/company/donau-versicherung-ag---vienna-insurance-group> | Xing<https://www.xing.com/companies/donauversicherungagviennainsurancegroup> | kununu<https://www.kununu.com/at/donau-versicherung-vienna-insurance-group3> | Youtube<https://www.youtube.com/channel/UCBi9pKhXpXM1jfNQrTOmlyw>\r\n\r\nHier geht´s zum Maklerportal<https://www.donauversicherung.at/maklerportal/>\r\n\r\n\r\nFirmensitz: 1010 Wien, Schottenring 15\r\nHandelsgericht Wien, FN 197733i\r\nwww.donauversicherung.at/<http://www.donauversicherung.at/>\r\nDatenschutzinformation<https://www.donauversicherung.at/datenschutz/>\r\n\r\n\r\n\r\n\r\n\r\n\r\nVon: Loschy Cornelia <C.Loschy@donauversicherung.at<mailto:C.Loschy@donauversicherung.at>>\r\nGesendet: Mittwoch, 1. Juli 2026 12:42\r\nAn: Donau LD Wien GEKO <geko.wien@donauversicherung.at<mailto:geko.wien@donauversicherung.at>>\r\nBetreff: WG: WG: A&C Wohnart Immobilien GmbH 2044001194 Sonstiges ID:12828728\r\n\r\n\r\nVon: Cosmin Covaciu <cosmin@ig.ro<mailto:cosmin@ig.ro>>\r\nGesendet: Mittwoch, 1. Juli 2026 09:43\r\nAn: Loschy Cornelia <C.Loschy@donauversicherung.at<mailto:C.Loschy@donauversicherung.at>>\r\nBetreff: Re: WG: A&C Wohnart Immobilien GmbH 2044001194 Sonstiges ID:12828728\r\n\r\nBetreff: Polizze Nr. 2044001194 – Ersuchen um prämienreduzierte Basisdeckung ab 01. 07. 2026 / Zahlung nach Neuberechnung Sehr geehrte Frau Loschy, vielen Dank für Ihre bisherigen Rückmeldungen sowie für die Übermittlung der Änderungspolizzen\r\n\r\nBetreff: Polizze Nr. 2044001194 – Ersuchen um prämienreduzierte Basisdeckung ab 01.07.2026 / Zahlung nach Neuberechnung\r\n\r\n\r\n\r\nSehr geehrte Frau Loschy,\r\n\r\n\r\n\r\nvielen Dank für Ihre bisherigen Rückmeldungen sowie für die Übermittlung der Änderungspolizzen und des Zahlscheins zur Polizze Nr. 2044001194 betreffend die Liegenschaft Schallergasse 35, 1120 Wien.\r\n\r\n\r\n\r\nWir möchten den Versicherungsschutz für die Liegenschaft grundsätzlich geordnet und ohne unnötige Deckungslücke klären. Gleichzeitig ersuchen wir um Verständnis, dass wir vor einer Zahlung zunächst die tatsächliche aktuelle Risikosituation und den gewünschten Versicherungsumfang richtig abgebildet haben möchten.\r\n\r\n\r\n\r\nNach unserem Verständnis wurde die bestehende Polizze aufgrund des Eigentümerwechsels auf die A&C Wohnart Immobilien GmbH umgeschrieben. Die Bekanntgabe des neuen Eigentümers sollte jedoch nicht als aktiver Neuabschlussantrag oder als ausdrückliche Zustimmung zur unveränderten Fortführung sämtlicher bisheriger Deckungsbausteine verstanden werden.\r\n\r\n\r\n\r\nDie aktuelle Situation der Liegenschaft stellt sich wie folgt dar:\r\n\r\n\r\n\r\n...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Extract text from Folgeprämie and Polizzenkopie PDFs
command: cd "D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/05. Asigurari/Asigurare cladire" && pdftotext -layout "B7280016C9961FE1988F3ADAC750FA7E_FolgeprämieStufe01.pdf" - 2>/dev/null | head -60; echo "=====POLIZZE1====="; pdftotext -layout "814BC40FC7831FE197E21FDA1089ECC3_Polizzenkopie.pdf" - 2>/dev/null | head -80
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
Retouren an Postfach 330, 1375 Wien                                                                          F�r Sie da
                                                                                                            Serviceline
A&C Wohnart Immobilien GmbH                                                            Telefon: +43 (0)50 330 330
Parkring 2                                                                         donau@donauversicherung.at
1010 Wien

Polizze Nr. 2044001194 / bisherige Polizze Nr. X712.261-2                          05.06.2026
offene Pr�mie: EUR 1.591,81 Mahnspesen: EUR 20,00

ACHTUNG: Ihr Versicherungsschutz ist in Gefahr!

Guten Tag!

Die Pr�mie zu dem oben angef�hrten Versicherungsvertrag ist leider noch nicht bei uns eingegangen.
Zahlen Sie die offene Pr�mie bitte innerhalb der n�chsten zwei Wochen ein (� 39 Versicherungs-
vertragsgesetz).

Tritt nach Ablauf dieser Frist ein Versicherungsfall ein und sind Sie auch dann noch mit der Zahlung der
offenen Pr�mie schuldhaft in Verzug, sind wir von der Verpflichtung zur Leistung frei.

Wir weisen Sie au�erdem darauf hin, dass der Versicherer das Versicherungsverh�ltnis mit sofortiger
Wirkung k�ndigen kann, wenn die/der VersicherungsnehmerIn auch nach Ablauf der angesetzten Frist mit
der Zahlung in Verzug ist.

Die K�ndigung wird wirkungslos, wenn die Pr�mienzahlung innerhalb eines Monats nach der K�ndigung
nachgeholt wird und bis dahin noch kein Versicherungsfall eingetreten ist.

Bitte zahlen Sie die offene Pr�mie mit dem beiliegenden Zahlschein ein.

Wenn Sie die Pr�mie in der Zwischenzeit bezahlt haben, betrachten Sie dieses Schreiben bitte als
gegenstandslos.

Haben Sie Fragen?
Die MitarbeiterInnen unserer Serviceline sind gerne jederzeit telefonisch unter 050 330 330 oder via E-Mail
unter donau@donauversicherung.at f�r Sie da. Au�erdem k�nnen Sie uns per Live Chat oder Video Chat
auf unserer Website donauversicherung.at erreichen.

Freundliche Gr��e

DONAU Versicherung AG
Vienna Insurance Group

ppa. Fuhs                            i.A. Mag. Riegler

Beilage: Zahlschein

Generaldirektion, Schottenring 15, 1010 Wien
Serviceline: +43 50 330 330, donau@donauversicherung.at, donauversicherung.at
Creditor-ID: AT34ZZZ00000003107, IBAN: AT67 2011 1403 1004 1414, BIC: GIBAATWWXXX

DONAU Versicherung AG Vienna Insurance Group
Sitz in 1010 Wien, Schottenring 15, FN 32002m, Handelsgericht Wien
=====POLIZZE1=====
Wohnhausversicherung

Retouren an Postfach 330, 1375 Wien

A&C Wohnart Immobilien GmbH
Parkring 2
1010 Wien

Polizze Nr. 2044001194 / bisherige Polizze Nr. X712261                             03.06.2026

Rahmenvertragsnummer: 2900010498

Guten Tag!
Mit Ausstellung dieser Polizze best�tigen wir die aktuellen �nderungen zu diesem Versicherungsvertrag.

DONAU Wohnhausversicherung

Ausstellungsgrund
�nderung Partner/ Adresse (�nderung Versicherungsnehmer (Eigent�merwechsel))

Vertragsdauer
�nderung ab: 28.05.2026 0:00 Uhr, Ablauf: 01.01.2036 0:00 Uhr, Hauptf�lligkeit: 01.01.

VersicherungsnehmerIn
A&C Wohnart Immobilien GmbH
Parkring 2, 1010 Wien

Versicherungsort
Schallergasse 35, 1120 Wien

Sachversicherung

ohne Wertanpassung

Versicherte Objekte (Betr�ge in EUR)

GEB�UDE:            Wohngeb�ude

Landesdirektion Wien, Schottenring 15, 1010 Wien, Telefon: +43 50330 72149          11400074984720
Serviceline: +43 50 330 330, donau@donauversicherung.at, donauversicherung.at
Creditor-ID: AT34ZZZ00000003107, IBAN: AT67 2011 1403 1004 1414, BIC: GIBAATWWXXX  Seite 1 von 9

DONAU Versicherung AG Vienna Insurance Group
Sitz in 1010 Wien, Schottenring 15, FN 32002m, Handelsgericht Wien
Wohnhausversicherung

Polizze Nr. 2044001194

Geb�udesumme:                 3.315.306,00
Versicherte Sparten:          Feuerversicherung Geb�ude, Sturmversicherung Geb�ude,
                              Leitungswasser Geb�ude
Risikoadresse:                Schallerg...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_get_email]
input: {"email_id":"6706f86a-b245-495b-8637-f692156e29c7"}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
{"id":"6706f86a-b245-495b-8637-f692156e29c7","account_email":"cosmin@ig.ro","subject":"WG: WG: A&C Wohnart Immobilien GmbH 2044001194 Sonstiges ID:12828728","from_name":"Loschy Cornelia","from_address":"C.Loschy@donauversicherung.at","to":["cosmin@ig.ro"],"cc":[],"received_at":"2026-07-10T10:59:21Z","text":"Sehr geehrter Herr Covaciu,\r\n\r\nWir beziehen uns auf Ihr Schreiben zum Vertrag mit der Polizzennummer 2044001194.\r\n\r\nWir informieren Sie darüber, dass gemäß § 69 Versicherungsvertragsgesetz durch die Veräußerung der versicherten Liegenschaft Schallergasse 35, 1120 Wien der Versicherungsvertrag mit allen Rechten und Pflichten auf A&C Wohnart Immobilien GmbH über gegangen ist.\r\n\r\nDie/der ErwerberIn der Liegenschaft ist berechtigt, innerhalb eines Monats nach dem Erwerb das Versicherungsverhältnis zu kündigen. Das Eigentum an der Liegenschaft ist bereits mit dem 10.03.2026 übergegangen.\r\n\r\nEine Kündigung aufgrund Eigentümerwechsel kann daher nicht mehr ausgesprochen werden.\r\n\r\nBezüglich der gewünschten Vertragsanpassung werden Sie gesondert verständigt. Ich habe ihr Ansuchen bereits intern weitergeleitet.\r\n\r\nWegen eines Prämienrückstands weisen wir nochmal daraufhin, dass derzeit kein Versicherungsschutz besteht.\r\n\r\nFür weitere Fragen stehen wir Ihnen gerne zur Verfügung.\r\nFreundliche Grüße\r\nCornelia Loschy\r\nVertragsverwaltung Gewerbe | Fachabteilung SHU\r\nDONAU Versicherung AG\r\nVienna Insurance Group\r\nGeneraldirektion\r\n1010 Wien, Schottenring 15\r\nTelefon  +43 50 330 – 72689\r\nE-Mail    c.loschy@donauversicherung.at<mailto:c.loschy@donauversicherung.at>\r\n\r\nIch will zur DONAU.\r\nFacebook<https://www.facebook.com/DONAUVersicherungAG> | Instagram<https://www.instagram.com/donauversicherung/> | LinkedIn<https://at.linkedin.com/company/donau-versicherung-ag---vienna-insurance-group> | Xing<https://www.xing.com/companies/donauversicherungagviennainsurancegroup> | kununu<https://www.kununu.com/at/donau-versicherung-vienna-insurance-group3> | Youtube<https://www.youtube.com/channel/UCBi9pKhXpXM1jfNQrTOmlyw>\r\n\r\nHier geht´s zu Meine DONAU<https://www.meinedonau.at/>\r\n\r\n\r\nFirmensitz: 1010 Wien, Schottenring 15\r\nHandelsgericht Wien, FN 32002m\r\nwww.donauversicherung.at/<http://www.donauversicherung.at/>\r\nDatenschutzinformation<https://www.donauversicherung.at/datenschutz/>\r\n\r\nVon: Cosmin Covaciu <cosmin@ig.ro<mailto:cosmin@ig.ro>>\r\nGesendet: Mittwoch, 1. Juli 2026 09:43\r\nAn: Loschy Cornelia <C.Loschy@donauversicherung.at<mailto:C.Loschy@donauversicherung.at>>\r\nBetreff: Re: WG: A&C Wohnart Immobilien GmbH 2044001194 Sonstiges ID:12828728\r\n\r\nBetreff: Polizze Nr. 2044001194 – Ersuchen um prämienreduzierte Basisdeckung ab 01. 07. 2026 / Zahlung nach Neuberechnung Sehr geehrte Frau Loschy, vielen Dank für Ihre bisherigen Rückmeldungen sowie für die Übermittlung der Änderungspolizzen\r\n\r\nBetreff: Polizze Nr. 2044001194 – Ersuchen um prämienreduzierte Basisdeckung ab 01.07.2026 / Zahlung nach Neuberechnung\r\n\r\n\r\n\r\nSehr geehrte Frau Loschy,\r\n\r\n\r\n\r\nvielen Dank für Ihre bisherigen Rückmeldungen sowie für die Übermittlung der Änderungspolizzen und des Zahlscheins zur Polizze Nr. 2044001194 betreffend die Liegenschaft Schallergasse 35, 1120 Wien.\r\n\r\n\r\n\r\nWir möchten den Versicherungsschutz für die Liegenschaft grundsätzlich geordnet und ohne unnötige Deckungslücke klären. Gleichzeitig ersuchen wir um Verständnis, dass wir vor einer Zahlung zunächst die tatsächliche aktuelle Risikosituation und den gewünschten Versicherungsumfang richtig abgebildet haben möchten.\r\n\r\n\r\n\r\nNach unserem Verständnis wurde die bestehende Polizze aufgrund des Eigentümerwechsels auf die A&C Wohnart Immobilien GmbH umgeschrieben. Die Bekanntgabe des neuen Eigentümers sollte jedoch nicht als aktiver Neuabschlussantrag oder als ausdrückliche Zustimmung zur unveränderten Fortführung sämtlicher bisheriger Deckungsbausteine verstanden werden.\r\n\r\n\r\n\r\nDie aktuelle ...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_get_email]
input: {"email_id":"1bc16469-dcb3-4cf3-819a-9a75f081bbc1"}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
{"id":"1bc16469-dcb3-4cf3-819a-9a75f081bbc1","account_email":"office@ac-wohnart.at","subject":"WG: Prämienzahlung Partnernummer: 2923354322 Polizze: 2044001194","from_name":"Loschy Cornelia","from_address":"C.Loschy@donauversicherung.at","to":["office@ac-wohnart.at"],"cc":[],"received_at":"2026-07-20T10:19:53Z","text":"Sehr geehrte Damen und Herren,\r\n\r\nwir haben auf Ihre beiliegende Nachricht vom 01.07.2026 am 10.07.2026 geantwortet.\r\n\r\nIm zweiten Anhang senden wir Ihnen gerne nochmal unsere entsprechende Rückmeldung.\r\nFreundliche Grüße\r\nCornelia Loschy\r\nVertragsverwaltung Gewerbe | Fachabteilung SHU\r\nDONAU Versicherung AG\r\nVienna Insurance Group\r\nGeneraldirektion\r\n1010 Wien, Schottenring 15\r\nTelefon  +43 50 330 – 72689\r\nE-Mail    c.loschy@donauversicherung.at<mailto:c.loschy@donauversicherung.at>\r\n\r\nIch will zur DONAU.\r\nFacebook<https://www.facebook.com/DONAUVersicherungAG> | Instagram<https://www.instagram.com/donauversicherung/> | LinkedIn<https://at.linkedin.com/company/donau-versicherung-ag---vienna-insurance-group> | Xing<https://www.xing.com/companies/donauversicherungagviennainsurancegroup> | kununu<https://www.kununu.com/at/donau-versicherung-vienna-insurance-group3> | Youtube<https://www.youtube.com/channel/UCBi9pKhXpXM1jfNQrTOmlyw>\r\n\r\nHier geht´s zu Meine DONAU<https://www.meinedonau.at/>\r\n\r\nFirmensitz: 1010 Wien, Schottenring 15\r\nHandelsgericht Wien, FN 32002m\r\nwww.donauversicherung.at/<http://www.donauversicherung.at/>\r\nDatenschutzinformation<https://www.donauversicherung.at/datenschutz/>\r\n\r\nVon: office@ac-wohnart.at <office@ac-wohnart.at>\r\nGesendet: Montag, 13. Juli 2026 12:37\r\nBetreff: Prämienzahlung Partnernummer: 2923354322 Polizze: 2044001194\r\n\r\nGuten Tag! A&C Wohnart Immobilien GmbH\r\nE-Mail: <office@ac-wohnart.at<mailto:office@ac-wohnart.at>>\r\nPartner#: 2923354322\r\n\r\n  *   ↪ Prämienzahlung Partnernummer: 2923354322 Polizze: 2044001194 // 09.07.2026 17:03\r\nSehr geehrte Damen und Herren,\r\n\r\nanbei übermitteln wir Ihnen unser Schreiben betreffend die Liegenschaft 1120 Wien, Schallergasse 35, mit der Bitte um Kenntnisnahme und entsprechende Bearbeitung.\r\n\r\nWir ersuchen Sie, den Inhalt des beigefügten Schreibens bei der weiteren Bearbeitung des Versicherungsfalles zu berücksichtigen und uns den Erhalt dieser E-Mail sowie der beigefügten Unterlagen kurz zu bestätigen.\r\n\r\nSollten für die weitere Bearbeitung zusätzliche Unterlagen oder Informationen erforderlich sein, ersuchen wir um entsprechende Mitteilung. Wir werden Ihnen diese selbstverständlich unverzüglich zur Verfügung stellen.\r\n\r\nFür Rückfragen stehen wir jederzeit gerne zur Verfügung und bedanken uns im Voraus für Ihre Unterstützung.\r\n\r\nMit freundlichen Grüßen\r\n\r\nA&C Wohnart Immobilien GmbH\r\nSchallergasse 35\r\n1120 Wien\r\nE-Mail: office@ac-wohnart.at<mailto:office@ac-wohnart.at>\r\n📎 Polizze Nr. 2044001194 – Ersuchen um prämienreduzierte.pdf\r\nSehr geehrter Herr Covaciu,\r\n\r\n\r\n\r\nWir beziehen uns auf Ihr Schreiben zum Vertrag mit der Polizzennummer 2044001194.\r\n\r\n\r\n\r\nWir informieren Sie darüber, dass gemäß § 69 Versicherungsvertragsgesetz durch die Veräußerung der versicherten Liegenschaft Schallergasse 35, 1120 Wien der Versicherungsvertrag mit allen Rechten und Pflichten auf A&C Wohnart Immobilien GmbH über gegangen ist.\r\n\r\n\r\n\r\nDie/der ErwerberIn der Liegenschaft ist berechtigt, innerhalb eines Monats nach dem Erwerb das Versicherungsverhältnis zu kündigen. Das Eigentum an der Liegenschaft ist bereits mit dem 10.03.2026 übergegangen.\r\n\r\n\r\n\r\nEine Kündigung aufgrund Eigentümerwechsel kann daher nicht mehr ausgesprochen werden.\r\n\r\n\r\n\r\nBezüglich der gewünschten Vertragsanpassung werden Sie gesondert verständigt. Ich habe ihr Ansuchen bereits intern weitergeleitet.\r\n\r\n\r\n\r\nWegen eines Prämienrückstands weisen wir nochmal daraufhin, dass derzeit kein Versicherungsschutz besteht.\r\n\r\n\r\n\r\nFür weitere Fragen stehen...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: ToolSearch]
input: {"query":"select:mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_update_draft","max_results":1}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_update_draft]
input: {"draft_id":"eedbb8b0-2488-4637-9cfb-0b798989217d","body":"Sehr geehrter Herr Dr. Maritczak,\n\nwir nehmen Bezug auf das Schreiben der COMMERZ Inkasso GmbH vom 09.09.2026 (Aktenzeichen 2616052, Polizzennr. X712261-2, Nr. 2044001194), das in Ihrem Auftrag im Namen der Donau Versicherung AG an die A&C Wohnart Immobilien GmbH gerichtet wurde. Das Schreiben wurde an die Adresse Parkring 2, 1010 Wien zugestellt und hat uns erst am 14.09.2026 erreicht.\n\nZunächst dürfen wir Sie über unsere aktuellen Kontaktdaten informieren und ersuchen Sie, sämtliche künftige Korrespondenz in dieser Angelegenheit ausschließlich an diese zu richten:\n\n- A&C Wohnart Immobilien GmbH (FN 668224h, Handelsgericht Wien)\n- Geschäftsanschrift: Schallergasse 35, 1120 Wien\n- E-Mail: office@ac-wohnart.at\n- Telefon: +43 665 670 550 45\n\nDer Vollständigkeit halber weisen wir darauf hin, dass zwischen der A&C Wohnart Immobilien GmbH und der Donau Versicherung AG seit Mai 2026 laufende Korrespondenz zu dieser Polizze besteht (u.a. ID:12.780.689, ID:12.828.728). Mit Schreiben vom 01.07.2026 haben wir eine Umstellung der Polizze auf eine prämienreduzierte Basisdeckung ab 01.07.2026 beantragt. Mit E-Mail vom 14.07.2026 hat Herr Mario Pfeiffer (Gewerbekoordinator LD Wien) den Ausschluss der Sparten Leitungswasser und Mieten-BU aufgrund Risikowegfalls in Aussicht gestellt und Unterlagen angefordert. Eine abschließende Erledigung dieses Anpassungsantrags, die uns mit E-Mail vom 10.07.2026 gesondert zugesagt wurde, liegt uns bis heute nicht vor. Die nunmehr im Inkassoweg geltend gemachte Prämienforderung betrifft somit einen Deckungsumfang, der Gegenstand eines noch offenen Anpassungsverfahrens ist.\n\nZudem hat die Donau Versicherung AG mit E-Mails vom 10.06.2026 und 10.07.2026 selbst schriftlich mitgeteilt, dass wegen des Prämienrückstands derzeit kein Versicherungsschutz besteht. Wir ersuchen daher auch um Aufklärung, für welche Zeiträume tatsächlich Versicherungsschutz bestand und inwieweit für Ze...
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
{"id":"eedbb8b0-2488-4637-9cfb-0b798989217d","kind":"new","source":"chatgpt","status":"pending","account_id":"476c2aa5-b01c-48d1-9647-4e8b4be4ad61","account_email":"office@ac-wohnart.at","to":["office@maritczak.at"],"cc":[],"bcc":[],"subject":"Aktenzeichen 2616052 / Polizzennr. X712261-2 (Donau Versicherung AG) – A&C Wohnart Immobilien GmbH: aktuelle Kontaktdaten und Ersuchen um Übermittlung sämtlicher anspruchsbegründender Unterlagen","body":"Sehr geehrter Herr Dr. Maritczak,\n\nwir nehmen Bezug auf das Schreiben der COMMERZ Inkasso GmbH vom 09.09.2026 (Aktenzeichen 2616052, Polizzennr. X712261-2, Nr. 2044001194), das in Ihrem Auftrag im Namen der Donau Versicherung AG an die A&C Wohnart Immobilien GmbH gerichtet wurde. Das Schreiben wurde an die Adresse Parkring 2, 1010 Wien zugestellt und hat uns erst am 14.09.2026 erreicht.\n\nZunächst dürfen wir Sie über unsere aktuellen Kontaktdaten informieren und ersuchen Sie, sämtliche künftige Korrespondenz in dieser Angelegenheit ausschließlich an diese zu richten:\n\n- A&C Wohnart Immobilien GmbH (FN 668224h, Handelsgericht Wien)\n- Geschäftsanschrift: Schallergasse 35, 1120 Wien\n- E-Mail: office@ac-wohnart.at\n- Telefon: +43 665 670 550 45\n\nWeiters ersuchen wir Sie höflich, uns sämtliche anspruchsbegründenden Unterlagen und Nachweise zu übermitteln, auf die sich die geltend gemachte Forderung in Höhe von insgesamt EUR 3.734,34 stützt, im Einzelnen:\n\n- Forderung DONAU Wohnhausversicherung, fällig seit 09.09.2026: EUR 3.183,62\n- Betreibungskosten des Auftraggebers: EUR 30,00\n- Erhebungskosten: EUR 14,40\n- Allgemeine Bearbeitungsgebühr lt. BGBl Nr. 141/1996: EUR 308,50\n- Mahnkosten lt. BGBl Nr. 141/1996: EUR 124,26\n- Evidenzhaltungskosten lt. BGBl Nr. 141/1996: EUR 49,68\n- Barauslagen: EUR 4,74\n- 8,00 % Verzugszinsen: EUR 19,14\n\nInsbesondere ersuchen wir um Übermittlung folgender Unterlagen:\n\n- des vollständigen Versicherungsvertrages samt Versicherungsantrag und Polizze,\n- des Nachweises des Vertragsabschlusses, insbesondere der von der A&C Wohnart Immobilien GmbH unterfertigten Vertragsunterlagen mit der Donau Versicherung AG,\n- der zugrunde liegenden Prämienvorschreibungen und Mahnungen samt Zustellnachweisen,\n- einer nachvollziehbaren Aufschlüsselung samt Rechtsgrundlage der einzelnen Kosten- und Gebührenpositionen.\n\nBis zur vollständigen Übermittlung und Prüfung dieser Unterlagen betrachten wir die Forderung als nicht nachgewiesen und behalten uns sämtliche Rechte vor. Wir ersuchen zugleich um entsprechende Fristerstreckung hinsichtlich des im Schreiben genannten Zahlungstermins 21.09.2026, bis uns die angeforderten Unterlagen vollständig vorliegen.\n\nWir danken für Ihre Bemühungen und stehen für Rückfragen gerne zur Verfügung.\n\nMit freundlichen Grüßen\n\nCosmin Adrian Covaciu","attachments":[],"reply_to_email_id":null,"created_at":"2026-09-14T14:26:05.760380Z","updated_at":"2026-09-14T14:26:05.760380Z","note":"Salvată în EVA → Drafts; trimiterea se face din EVA."}
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: ToolSearch]
input: {"query":"select:mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_get_draft","max_results":1}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: mcp__090946e4-21b8-41b4-9ba6-b8b5e95b5405__eva_get_draft]
input: {"draft_id":"eedbb8b0-2488-4637-9cfb-0b798989217d"}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
{"id":"eedbb8b0-2488-4637-9cfb-0b798989217d","kind":"new","source":"chatgpt","status":"pending","account_id":"476c2aa5-b01c-48d1-9647-4e8b4be4ad61","account_email":"office@ac-wohnart.at","to":["office@maritczak.at"],"cc":[],"bcc":[],"subject":"Aktenzeichen 2616052 / Polizzennr. X712261-2 (Donau Versicherung AG) – A&C Wohnart Immobilien GmbH: aktuelle Kontaktdaten und Ersuchen um Übermittlung sämtlicher anspruchsbegründender Unterlagen","body":"Sehr geehrter Herr Dr. Maritczak,\n\nwir nehmen Bezug auf das Schreiben der COMMERZ Inkasso GmbH vom 09.09.2026 (Aktenzeichen 2616052, Polizzennr. X712261-2, Nr. 2044001194), das in Ihrem Auftrag im Namen der Donau Versicherung AG an die A&C Wohnart Immobilien GmbH gerichtet wurde. Das Schreiben wurde an die Adresse Parkring 2, 1010 Wien zugestellt und hat uns erst am 14.09.2026 erreicht.\n\nZunächst dürfen wir Sie über unsere aktuellen Kontaktdaten informieren und ersuchen Sie, sämtliche künftige Korrespondenz in dieser Angelegenheit ausschließlich an diese zu richten:\n\n- A&C Wohnart Immobilien GmbH (FN 668224h, Handelsgericht Wien)\n- Geschäftsanschrift: Schallergasse 35, 1120 Wien\n- E-Mail: office@ac-wohnart.at\n- Telefon: +43 665 670 550 45\n\nDer Vollständigkeit halber weisen wir darauf hin, dass zwischen der A&C Wohnart Immobilien GmbH und der Donau Versicherung AG seit Mai 2026 laufende Korrespondenz zu dieser Polizze besteht (u.a. ID:12.780.689, ID:12.828.728). Mit Schreiben vom 01.07.2026 haben wir eine Umstellung der Polizze auf eine prämienreduzierte Basisdeckung ab 01.07.2026 beantragt. Mit E-Mail vom 14.07.2026 hat Herr Mario Pfeiffer (Gewerbekoordinator LD Wien) den Ausschluss der Sparten Leitungswasser und Mieten-BU aufgrund Risikowegfalls in Aussicht gestellt und Unterlagen angefordert. Eine abschließende Erledigung dieses Anpassungsantrags, die uns mit E-Mail vom 10.07.2026 gesondert zugesagt wurde, liegt uns bis heute nicht vor. Die nunmehr im Inkassoweg geltend gemachte Prämienforderung betrifft somit einen Deckungsumfang, der Gegenstand eines noch offenen Anpassungsverfahrens ist.\n\nZudem hat die Donau Versicherung AG mit E-Mails vom 10.06.2026 und 10.07.2026 selbst schriftlich mitgeteilt, dass wegen des Prämienrückstands derzeit kein Versicherungsschutz besteht. Wir ersuchen daher auch um Aufklärung, für welche Zeiträume tatsächlich Versicherungsschutz bestand und inwieweit für Zeiträume ohne Versicherungsschutz Prämien in voller Höhe gefordert werden.\n\nWeiters ersuchen wir Sie höflich, uns sämtliche anspruchsbegründenden Unterlagen und Nachweise zu übermitteln, auf die sich die geltend gemachte Forderung in Höhe von insgesamt EUR 3.734,34 stützt, im Einzelnen:\n\n- Forderung DONAU Wohnhausversicherung, fällig seit 09.09.2026: EUR 3.183,62\n- Betreibungskosten des Auftraggebers: EUR 30,00\n- Erhebungskosten: EUR 14,40\n- Allgemeine Bearbeitungsgebühr lt. BGBl Nr. 141/1996: EUR 308,50\n- Mahnkosten lt. BGBl Nr. 141/1996: EUR 124,26\n- Evidenzhaltungskosten lt. BGBl Nr. 141/1996: EUR 49,68\n- Barauslagen: EUR 4,74\n- 8,00 % Verzugszinsen: EUR 19,14\n\nInsbesondere ersuchen wir um Übermittlung folgender Unterlagen:\n\n- des vollständigen Versicherungsvertrages samt ursprünglichem Versicherungsantrag und Polizze sowie der Rahmenvereinbarung 2900010498,\n- des Nachweises des Vertragsabschlusses bzw. der Vertragsübernahme, insbesondere sämtlicher von der A&C Wohnart Immobilien GmbH unterfertigten Vertragsunterlagen mit der Donau Versicherung AG,\n- der zugrunde liegenden Prämienvorschreibungen und Mahnungen samt Zustellnachweisen, mit genauer Angabe der jeweiligen Verrechnungszeiträume,\n- einer nachvollziehbaren Aufschlüsselung samt Rechtsgrundlage der einzelnen Kosten- und Gebührenpositionen.\n\nBis zur vollständigen Übermittlung und Prüfung dieser Unterlagen betrachten wir die Forderung als nicht nachgewiesen und behalten uns sämtliche Rechte und Einwendungen vor. Wir ersuchen zugleich um entsprechende Fristerstreckung hinsichtlich des im Schreiben genannten Za...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Edit]
file: D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\08. Corespondenta\2026.09.14 Somatie Commerz-Inkasso (Donau)\2026.09.14 Email trimis (ciorna EVA) - catre Dr. Maritczak - cerere acte doveditoare.txt
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
The file D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\08. Corespondenta\2026.09.14 Somatie Commerz-Inkasso (Donau)\2026.09.14 Email trimis (ciorna EVA) - catre Dr. Maritczak - cerere acte doveditoare.txt has been updated successfully. (file state is current in your context — no need to Read it back)
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Edit]
file: D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\08. Corespondenta\2026.09.14 Somatie Commerz-Inkasso (Donau)\2026.09.14 Email trimis (ciorna EVA) - catre Dr. Maritczak - cerere acte doveditoare.txt
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
The file D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\08. Corespondenta\2026.09.14 Somatie Commerz-Inkasso (Donau)\2026.09.14 Email trimis (ciorna EVA) - catre Dr. Maritczak - cerere acte doveditoare.txt has been updated successfully. (file state is current in your context — no need to Read it back)
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Extract text from Hofhans letter and original policy
command: cd "D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/05. Asigurari" && pdftotext -layout "Gebäudeversicherung/Hofhans 2026.05.27.pdf" - 2>/dev/null | head -80; echo "=====ORIGINAL POLICY====="; pdftotext -layout "Asigurare cladire/Schalle_1080_DON_SHU_2044001194_2939905718.pdf" - 2>/dev/null | head -50
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
=====ORIGINAL POLICY=====
Wohnhausversicherung                                                                        Vermittelt durch
                                                        Seipt & Partner Versicherungsmakler GmbH
Retouren an Postfach 330, 1375 Wien
                                                                                               office@seipt.at
Schallergasse 35 Immobilienbesitz GmbH &
Co KG
v.d. Hofhans Immobilienmanagement GmbH
Albertgasse 32/9
1080 Wien

Polizze Nr. 2044001194 / bisherige Polizze Nr. X712261                             03.02.2026

Rahmenvertragsnummer: 2900010498

Sehr geehrte Damen und Herren!
Mit Ausstellung dieser Polizze best�tigen wir die aktuellen �nderungen zu diesem Versicherungsvertrag.

DONAU Wohnhausversicherung

Ausstellungsgrund
Ersatzvertrag

Vertragsdauer
�nderung ab: 01.01.2026 0:00 Uhr, Ablauf: 01.01.2036 0:00 Uhr, Hauptf�lligkeit: 01.01.

VersicherungsnehmerIn
Schallergasse 35 Immobilienbesitz GmbH & Co KG
c/o v.d. Hofhans Immobilienmanagement GmbH, Albertgasse 32/9, 1080 Wien

Versicherungsort
Schallergasse 35, 1120 Wien

Sachversicherung

ohne Wertanpassung

Versicherte Objekte (Betr�ge in EUR)

GEB�UDE:            Wohngeb�ude

Landesdirektion Wien, Schottenring 15, 1010 Wien, Telefon: +43 50330 72149            11400070586369
Serviceline: +43 50 330 330, donau@donauversicherung.at, donauversicherung.at
Creditor-ID: AT34ZZZ00000003107, IBAN: AT67 2011 1403 1004 1414, BIC: GIBAATWWXXX  Seite 1 von 11

DONAU Versicherung AG Vienna Insurance Group
Sitz in 1010 Wien, Schottenring 15, FN 32002m, Handelsgericht Wien
Wohnhausversicherung

Polizze Nr. 2044001194
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: OCR Hofhans letter and extract Hausverwaltung docx text
command: cd "D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/05. Asigurari" && python -c "
import fitz
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
doc = fitz.open('Gebäudeversicherung/Hofhans 2026.05.27.pdf')
print('pages:', len(doc))
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=200)
    img = pix.tobytes('png')
    res, _ = ocr(img)
    if res:
        print(f'--- page {i+1} ---')
        print('\n'.join(r[1] for r in res))
" 2>/dev/null; echo "=====DOCX====="; python -c "
import zipfile, re
z = zipfile.ZipFile('Asigurare cladire/Firmă de administrare (Hausverwaltung).docx')
xml = z.read('word/document.xml').decode('utf-8')
text = re.sub(r'<w:p [^>]*>|<w:p>', '\n', xml)
text = re.sub(r'<[^>]+>', '', text)
print(text[:3000])
"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result: error]
Exit code 1
pages: 1
--- page 1 ---
=====DOCX=====
Traceback (most recent call last):
  File "<string>", line 7, in <module>
  File "C:\Users\User\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u0103' in position 9: character maps to <undefined>
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Retry OCR and docx extraction with UTF-8 output
command: cd "D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/05. Asigurari" && PYTHONIOENCODING=utf-8 python -c "
import fitz
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
doc = fitz.open('Gebäudeversicherung/Hofhans 2026.05.27.pdf')
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=250)
    res, _ = ocr(pix.tobytes('png'))
    print(f'--- page {i+1}: {len(res) if res else 0} lines ---')
    if res:
        print('\n'.join(r[1] for r in res))
" 2>/dev/null; echo "=====DOCX====="; PYTHONIOENCODING=utf-8 python -c "
import zipfile, re
z = zipfile.ZipFile('Asigurare cladire/Firmă de administrare (Hausverwaltung).docx')
xml = z.read('word/document.xml').decode('utf-8')
text = re.sub(r'<w:p [^>]*>|<w:p>', chr(10), xml)
text = re.sub(r'<[^>]+>', '', text)
import html
print(html.unescape(text)[:3500])
"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
--- page 1: 46 lines ---
onau
VIENNAINSURANCEGROUP
hofhans
26. Mai 2026
FurSie da
RetourenanPostfach330,1375Wien
EINGELANGT
Serviceline
Schallergasse35ImmobilienbesitzGmbH
Telefon:+43(0)50330330
Co KG
donau@donauversicherung.at
v.d.HofhansImmobilienmanagementGmbH
Albertgasse32/9
1080Wien
PolizzeNr.2044001194/bisherigePolizzeNr.X712.261-2
20.05.2026
offenePramie:EUR1.591,81Mahnspesen:EUR10,00
ACHTUNG:IhrVersicherungsschutzistinGefahr!
GutenTag!
DiePramiezudemobenangefuhrtenVersicherungsvertragistleidernochnichtbeiunseingegangen.
ZahlenSiedieoffenePramiebitteinnerhalbvoneinemMonatein(S39Versicherungsvertragsgesetz).
-0-0-0-0/583492-19735696
TrittnachAblaufdieserFristeinVersicherungsfalleinund sindSieauchdannnochmitderZahlungder
offenenPramieschuldhaftinVerzug,sindwirvonderVerpflichtungzurLeistungfrei.
WirweisenSieauBerdemdaraufhin,dassderVersichererdasVersicherungsverhaltnismitsofortiger
Wirkungkundigenkann,wenndie/derVersicherungsnehmerlnauchnachAblaufderangesetztenFristmit
derZahlunginVerzugist.
DieKundigungwirdwirkungslos,wenndiePramienzahlunginnerhalbeinesMonatsnachderKundigung
BittezahlenSiedieoffenePramiemitdembeiliegendenZahlscheinein.
WennSiediePramieinderZwischenzeitbezahlthaben,betrachtenSiediesesSchreibenbitteals
gegenstandslos.
HabenSieFragen?
DieMitarbeiterlnnenunsererServicelinesindgernejederzeittelefonischunter050330330oderviaE-Mail
unterdonau@donauversicherung.atfurSieda.AuBerdemkonnenSieunsperLiveChatoderVideoChat
aufunsererWebsitedonauversicherung.aterreichen.
FreundlicheGruBe
DONAUVersicherungAG
ViennaInsuranceGroup
ppa.Fuhs
i.A.Mag.Riegler
Beilage:Zahlschein
Generaldirektion,Schottenring15,1010Wen
Creditor-ID:AT34ZZZ00000003107,IBAN:AT672011140310041414,BIC:GIBAATWWXXX
DONAUVersicherungAGViennaInsuranceGroup
Sitzin1010Wen,Schottenring15,FN32002m，HandelsgerichtWien
=====DOCX=====


Firmă de administrare (Hausverwaltung) - A&C Wohnart Immobilien GmbH, în calitate de nou proprietar al imobilului din Schallergasse 35, Viena, gestionarea proprietății implică respectarea legislației austriece (în special MRG - Mietrechtsgesetz și WEG - Wohnungseigentumsgesetz).
Iată răspunsurile detaliate la întrebările tale:
1. De ce ai nevoie de o firmă de administrare (Hausverwaltung) și ce spune legea?
În Austria, obligativitatea angajării unei firme de administrare depinde de structura de proprietate:
Dacă ești proprietar unic (Alleineigentümer / Zinshaus): Legea NU te obligă să ai o firmă de administrare externă. Poți administra clădirea în regie proprie. Totuși, este extrem de riscant fără expertiză, deoarece legea chiriei (MRG) este foarte strictă în Austria, iar erorile în calculul chiriei sau al costurilor de întreținere (Betriebskosten) pot duce la procese costisitoare.
Dacă clădirea este împărțită în apartamente cu proprietari diferiți (Wohnungseigentum - WEG): Administrarea este obligatorie prin lege dacă majoritatea proprietarilor o cer.
De ce ești obligat „practic” să ai administrare (sau să preiei sarcinile lor):
Răspunderea pentru siguranță (Verkehrssicherungspflicht): Proprietarul este responsabil civil și penal dacă cineva se rănește pe proprietate (ex: gheață pe trotuar, țiglă căzută, balustradă defectă).
Norma ÖNORM B 1300 / B 1301: Acestea sunt norme austriece care impun verificări periodice de siguranță ale clădirii. O firmă de administrare preia această responsabilitate și documentează controalele pentru a te proteja de răspundere legală.
Gestiunea fiscală: Administrarea trebuie să raporteze corect TVA-ul și să gestioneze fondul de rezervă (Instandhaltungsrücklage).

2. Lista completă de servicii (Hausverwaltung)
Serviciile unei firme de administrare în Viena sunt, de regulă, împărțite în trei categorii: Administrative/Comerciale, Tehnice și Juridice.
Denumire Serviciu
Explicație Serviciu
Gestiunea Chiriilor (Mietzinsverwaltung)
Facturarea lunară a chiriei și a costurilor administrative (Betriebskosten) către chiriași, monitorizarea plățilo...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Check if python-docx is installed
command: python -c "import docx; print('python-docx OK')" 2>&1 | tail -1
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
python-docx OK
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Write]
file: C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\fa0414ae-212a-4028-8738-a547b7043014\scratchpad\analiza_juridica.py
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
File created successfully at: C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\fa0414ae-212a-4028-8738-a547b7043014\scratchpad\analiza_juridica.py (file state is current in your context — no need to Read it back)
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Generate legal analysis DOCX document
command: PYTHONIOENCODING=utf-8 python "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/fa0414ae-212a-4028-8738-a547b7043014/scratchpad/analiza_juridica.py"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
saved: D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\08. Corespondenta\2026.09.14 Somatie Commerz-Inkasso (Donau)\2026.09.14 Analiza juridica - Somatie Commerz-Inkasso 2616052 (Donau 2044001194).docx
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: SendUserFile]
input: {"files":["D:\\00. Downloads\\Apartamente Viena\\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\\08. Corespondenta\\2026.09.14 Somatie Commerz-Inkasso (Donau)\\2026.09.14 Analiza juridica - Somatie Commerz-Inkasso 2616052 (Donau 2044001194).docx"],"caption":"Analiza juridică a somației — concluzie: prima de asigurare e datorată (§69 VersVG), dar costurile de Inkasso și cuantumul trimestrului Q3 sunt contestabile.","status":"normal","display":"attach"}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
1 file delivered to user.
  D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\08. Corespondenta\2026.09.14 Somatie Commerz-Inkasso (Donau)\2026.09.14 Analiza juridica - Somatie Commerz-Inkasso 2616052 (Donau 2044001194).docx → file_uuid: e299d5d1-ab7e-4ec2-982d-4835c48d6ea8
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Write]
file: C:\Users\User\.claude\projects\--192-168-100-169-Comun-\memory\donau-polita-somatie.md
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
File created successfully at: C:\Users\User\.claude\projects\--192-168-100-169-Comun-\memory\donau-polita-somatie.md
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Edit]
file: C:\Users\User\.claude\projects\--192-168-100-169-Comun-\memory\MEMORY.md
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
The file C:\Users\User\.claude\projects\--192-168-100-169-Comun-\memory\MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
[/external_agent_tool_result]

## Asistent

Gata — am parcurs toate documentele din foldere și toată corespondența Donau de pe cele 4 conturi de email, iar concluzia e importantă și nuanțată.

## Concluzia juridică, pe scurt

**Creanța principală (3.183,62 € = 2 prime trimestriale) este, cel mai probabil, întemeiată.** Polița a trecut **prin efectul legii** (§ 69 VersVG austriac) asupra A&C Wohnart la cumpărarea imobilului — fără să fie nevoie de vreo semnătură. Dreptul tău de reziliere ca dobânditor (§ 70 VersVG, 1 lună) a expirat în aprilie 2026: proprietatea s-a transferat la 10.03.2026, polița v-a fost transmisă de Bogdan la 19.03.2026, iar primul contact cu Donau a fost abia la 27.05.2026. Donau v-a comunicat deja în scris exact acest lucru (10.06 și 10.07.2026). Argumentul „nu am semnat nimic cu Donau" **nu ține** — nu-l recomand ca linie principală.

**Ce este însă contestabil:**
- **Costurile de Inkasso (550,72 €)** — Donau a promis la 10.07.2026 un răspuns separat la cererea voastră de reducere a acoperirii din 01.07.2026 și nu l-a dat niciodată; Mario Pfeiffer a confirmat la 14.07.2026 că poate exclude Leitungswasser + Mieten-BU. Să predea dosarul la Inkasso cu o cerere pendinte nesoluționată face aceste costuri atacabile (BGBl 141/1996, § 1333 ABGB).
- **Cuantumul trimestrului 01.07–01.10** — numai asigurarea de apă costă 3.128 €/an din prima totală de 6.367 €/an; dacă excluderea se aplică de la 01.07, trimestrul se înjumătățește.

**Punct critic descoperit:** cele 3 documente cerute de Pfeiffer la 14.07.2026 (Baubewilligung, Baubeschreibung, confirmarea instalatorului că apa e închisă) **nu apar ca fiind trimise vreodată** — de aceea reducerea nu s-a finalizat. Și atenție: Donau a declarat în scris că **imobilul nu are în prezent acoperire** — o clădire din 1905, goală, în pre-șantier, neasigurată, e un risc mai mare decât somația însăși. Contractul curge până în **2036**, deci problema nu dispare prin neplată.

## Ce am făcut concret

1. **Toate documentele salvate** în [08. Corespondenta\2026.09.14 Somatie Commerz-Inkasso (Donau)](D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)\08. Corespondenta\2026.09.14 Somatie Commerz-Inkasso (Donau)): somația PDF, emailul primit de la Bogdan (txt), ciorna către avocat (txt) și **documentul de analiză juridică** (.docx, trimis și mai sus în conversație) — cu cronologia completă din 03.02.2026 până azi, temeiurile legale, analiza fiecărei poziții din defalcare și recomandările de acțiune.

2. **Ciorna din EVA către Dr. Maritczak actualizată** cu istoricul real: menționează acum cererea de adaptare pendinte (01.07), oferta lui Pfeiffer (14.07), declarațiile Donau „kein Versicherungsschutz", și cere prelungirea termenului până la soluționarea cererii de adaptare — pe lângă adresa actuală și actele doveditoare. E în EVA → Drafts, o trimiți de acolo.

3. **Verificare completă foldere + EVA:** 23 de emailuri Donau găsite (martie–iulie 2026, pe cosmin@ig.ro, office@ac-wohnart.at, gmail și ipec.ro); în foldere, polițele și somațiile sunt în `05. Asigurari\Asigurare cladire` („Hofhans 2026.05.27.pdf" s-a dovedit a fi, după OCR, somația Donau din 20.05 către vechiul proprietar — nu o scrisoare Hofhans).

**Recomandarea practică nr. 1 pentru săptămâna asta:** pe lângă emailul către avocat, trimiteți urgent lui Pfeiffer cele 3 documente cerute (Baubewilligung o aveți în `02. Autorizatie`), cu cererea de aplicare retroactivă de la 01.07 — și propuneți plata primei necontestate în schimbul renunțării la costurile de Inkasso. Pot pregăti și această ciornă către Pfeiffer, dacă vrei.

## Asistent

<EXTERNAL SESSION IMPORTED>
