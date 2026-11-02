# Rezultate — Găsește emailurile de la EximBank

Răspunsuri și rezultate disponibile în istoricul local; fără limită de lungime aplicată de export.

## Asistent

Caut emailurile de la EximBank în contul conectat.


## mcpToolCall

````json
{
  "type": "mcpToolCall",
  "id": "exec-45cf3735-5128-4de1-9895-7eb170e4239f",
  "server": "codex_apps",
  "tool": "eva_mail.eva_search_emails",
  "status": "completed",
  "arguments": {
    "link_id": "link_6ae19b6ebad08191ba9bbfe616469187",
    "sender": "exim",
    "is_sent": false,
    "limit": 50
  },
  "appContext": {
    "connectorId": "asdk_app_6aa3eadee6ec8191a9bc3b9608c0f1bc",
    "linkId": "link_6ae19b6ebad08191ba9bbfe616469187",
    "resourceUri": null,
    "appName": "Eva-Mail",
    "actionName": "eva_search_emails"
  },
  "mcpAppUi": null,
  "pluginId": null,
  "readOnlyHint": true,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\n  \"items\": [\n    {\n      \"id\": \"089fff65-07de-42e3-b788-571a3a5fe356\",\n      \"account_email\": \"covaciu.gnm@gmail.com\",\n      \"subject\": \"Exim Banca Romaneasca Secure File Share CESIRO PRODUCTION SRL-COVACIU COSMIN ADRIAN\",\n      \"from_name\": \"sftp@eximbank.ro\",\n      \"from_address\": \"sftp@eximbank.ro\",\n      \"to\": [\n        \"covaciu.gnm@gmail.com\"\n      ],\n      \"received_at\": \"2026-10-23T07:38:32Z\",\n      \"snippet\": \"Ai primit access catre Exim Banca Romaneasca Secure File Share de la Exim Banca Romaneasca. Linkul va expira la Monday, October 26, 2026 10:30 AM. https://sftp.eximbank.ro/WebClientNew/index.html/?\",\n      \"category\": \"fyi\",\n      \"labels\": [\n        \"UNREAD\",\n        \"CATEGORY_PERSONAL\",\n        \"Label_43995\",\n        \"INBOX\",\n        \"3: Fyi\"\n      ],\n      \"folder\": \"Exim Banca Romaneasca\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": false,\n      \"attachment_names\": []\n    },\n    {\n      \"id\": \"e95452c5-a822-4aab-aa07-4c1987b82689\",\n      \"account_email\": \"cosmin.covaciu@ipec.ro\",\n      \"subject\": \"Acțiune necesară: confirmați contul dvs. până la 29 septembrie\",\n      \"from_name\": \"Exim Banca Românească | Actualizare cont\",\n      \"from_address\": \"bounces-xccd6m@localhost.co.uk\",\n      \"to\": [\n        \"cosmin.covaciu@ipec.ro\"\n      ],\n      \"received_at\": \"2026-09-18T10:46:48Z\",\n      \"snippet\": \"ATENȚIE: Acest e-mail provine din afara companiei. Nu dati click pe linkuri și nu deschideți atașame\",\n      \"category\": \"fyi\",\n      \"labels\": [\n        \"4: Notification\"\n      ],\n      \"folder\": \"Exim Banca Românească | Actualizare cont\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": false,\n      \"attachment_names\": []\n    },\n    {\n      \"id\": \"a0e8245f-6636-40ed-8e78-d1c87fe7b17d\",\n      \"account_email\": \"cosmin.covaciu@ipec.ro\",\n      \"subject\": \"Acțiune necesară: confirmați contul dvs. până la 29 septembrie\",\n      \"from_name\": \"Exim Banca Românească | Actualizare cont\",\n      \"from_address\": \"bounces-mswzva@localhost.co.uk\",\n      \"to\": [\n        \"cosmin.covaciu@ipec.ro\"\n      ],\n      \"received_at\": \"2026-09-18T08:28:42Z\",\n      \"snippet\": \"ATENȚIE: Acest e-mail provine din afara companiei. Nu dati click pe linkuri și nu deschideți atașame\",\n      \"category\": \"fyi\",\n      \"labels\": [\n        \"4: Notification\"\n      ],\n      \"folder\": \"Exim Banca Românească | Actualizare cont\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": false,\n      \"attachment_names\": []\n    },\n    {\n      \"id\": \"50371f1f-88da-4ab8-96ad-34677ae28388\",\n      \"account_email\": \"cosmin.covaciu@ipec.ro\",\n      \"subject\": \"Acțiune necesară: confirmați contul dvs. până la 29 septembrie\",\n      \"from_name\": \"Exim Banca Românească | Actualizare cont\",\n      \"from_address\": \"bounces-dr3s5o@aucouventdescollines.be\",\n      \"to\": [\n        \"cosmin.covaciu@ipec.ro\"\n      ],\n      \"received_at\": \"2026-09-16T19:24:30Z\",\n      \"snippet\": \"ATENȚIE: Acest e-mail provine din afara companiei. Nu dati click pe linkuri și nu deschideți atașame\",\n      \"category\": \"fyi\",\n      \"labels\": [\n        \"4: Notification\"\n      ],\n      \"folder\": \"Exim Banca Românească | Actualizare cont\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": false,\n      \"attachment_names\": []\n    },\n    {\n      \"id\": \"e6390cf2-5f03-4d91-bb88-1927a2229533\",\n      \"account_email\": \"cosmin.covaciu@cesiro.com\",\n      \"subject\": \"Notificare de actualizare a datelor\",\n      \"from_name\": \"noreply | Exim Banca Romaneasca\",\n      \"from_address\": \"noreply@eximbank.ro\",\n      \"to\": [\n        \"cosmin.covaciu@cesiro.com\"\n      ],\n      \"received_at\": \"2026-09-01T05:00:24Z\",\n      \"snippet\": \"Stimate client,\\r\\n\\r\\n*In conformitate cu prevederile Regulamentului BNR nr. 2/2019 privind prevenirea \",\n      \"category\": \"fyi\",\n      \"labels\": [\n        \"1: To respond\"\n      ],\n      \"folder\": \"noreply | Exim Banca Romaneasca\",\n      \"is_read\": false,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": false,\n      \"attachment_names\": []\n    },\n    {\n      \"id\": \"f5d088df-8379-445d-92b3-15ff00efeeef\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"CESIRO PRODUCTION - identificare CONT PROIECT \",\n      \"from_name\": \"Oana Baciu\",\n      \"from_address\": \"oana.baciu@eximbank.ro\",\n      \"to\": [\n        \"covaciu.gnm@gmail.com\"\n      ],\n      \"received_at\": \"2026-07-03T12:48:27Z\",\n      \"snippet\": \"Continut Intern Buna ziua Domnule Cosmin va trimit identificare fiscala si documentele ce au stat la baza deschiderii ac\",\n      \"category\": \"fyi\",\n      \"labels\": [\n        \"3: Fyi\"\n      ],\n      \"folder\": \"Oana Baciu\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": true,\n      \"attachment_names\": [\n        \"image001.jpg\",\n        \"CESIRO - Aga (1).pdf\",\n        \"CESIRO - F40 - Solicitare deschidere cont + fond.pdf\",\n        \"IDENTIFICARE FISCALA.pdf\"\n      ]\n    },\n    {\n      \"id\": \"44eb4fbe-3ed7-4d7d-afa7-283b28d085c5\",\n      \"account_email\": \"cosmin.covaciu@cesiro.com\",\n      \"subject\": \"Undeliverable: Re: FW: CESIRO PRODUCTION SRL - Extrase de cont \",\n      \"from_name\": \"postmaster@eximbank.ro\",\n      \"from_address\": \"postmaster@eximbank.ro\",\n      \"to\": [\n        \"cosmin.covaciu@cesiro.com\"\n      ],\n      \"received_at\": \"2026-05-08T07:57:37Z\",\n      \"snippet\": \"[https://products.office.com/en-us/CMSImages/Office365Logo_Orange.png?version=b8d100a9-0a8b-8e6a-88e\",\n      \"category\": \"fyi\",\n      \"labels\": [\n        \"4: Notification\"\n      ],\n      \"folder\": \"postmaster@eximbank.ro\",\n      \"is_read\": false,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": true,\n      \"attachment_names\": [\n        \"CI Cosmin Adrian Covaciu (1).pdf\"\n      ]\n    },\n    {\n      \"id\": \"29b1a295-23ce-45db-9303-cde3d3d27033\",\n      \"account_email\": \"cosmin.covaciu@cesiro.com\",\n      \"subject\": \"RE: FW: CESIRO PRODUCTION SRL - Extrase de cont \",\n      \"from_name\": \"Diana Marcu\",\n      \"from_address\": \"diana.marcu@eximbank.ro\",\n      \"to\": [\n        \"cosmin.covaciu@cesiro.com\"\n      ],\n      \"received_at\": \"2026-05-08T07:24:10Z\",\n      \"snippet\": \"Continut Intern\\r\\n\\r\\nBuna ziua,\\r\\n\\r\\nVa transmit atasat extrasele de cont pentru CESIRO PRODUCTION SRL ,\",\n      \"category\": \"fyi\",\n      \"labels\": [\n        \"5: Finance\"\n      ],\n      \"folder\": \"Diana Marcu\",\n      \"is_read\": false,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": true,\n      \"attachment_names\": [\n        \"image001.jpg\",\n        \"extras cont cesiune.pdf\",\n        \"estras cont  ron.pdf\"\n      ]\n    },\n    {\n      \"id\": \"efeb0d7e-c1ef-4f73-bbe3-5b3e81a38a38\",\n      \"account_email\": \"cosmin.covaciu@cesiro.com\",\n      \"subject\": \"FW: CESIRO PRODUCTION SRL - Extrase de cont \",\n      \"from_name\": \"Diana Marcu\",\n      \"from_address\": \"diana.marcu@eximbank.ro\",\n      \"to\": [\n        \"cosmin.covaciu@cesiro.com\",\n        \"cosmina.stanciu@ipec.ro\"\n      ],\n      \"received_at\": \"2026-04-28T05:10:17Z\",\n      \"snippet\": \"Continut Intern\\r\\n\\r\\nBuna ziua,\\r\\n\\r\\nRevenim cu aceasta rugaminte.\\r\\n\\r\\nPentru inchiderea contului avem ru\",\n      \"category\": \"1: To respond\",\n      \"labels\": [\n        \"INBOX\",\n        \"1: To respond\"\n      ],\n      \"folder\": null,\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": true,\n      \"attachment_names\": [\n        \"F14-III-CLI-CP Cerere inchidere cont_produse si servicii\\r\\n   (7).docx\",\n        \"image001.jpg\"\n      ]\n    },\n    {\n      \"id\": \"f7773cfe-e7f2-46ac-a043-d53b43730121\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"CESIRO PRODUCTION SRL - consultare formulare\",\n      \"from_name\": \"Mihai Martis\",\n      \"from_address\": \"Mihai.Martis@eximbank.ro\",\n      \"to\": [\n        \"covaciu.gnm@gmail.com\"\n      ],\n      \"received_at\": \"2024-12-18T09:28:38Z\",\n      \"snippet\": \"Buna Cosmin, Atasate regasesti, spre consultare, formularele de deschidere cont. Multumesc, Mihai Mihai MARȚIȘ Director \",\n      \"category\": \"fyi\",\n      \"labels\": [\n        \"3: Fyi\"\n      ],\n      \"folder\": \"Mihai Martis\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": true,\n      \"attachment_names\": [\n        \"image001.jpg\",\n        \"_F40-III-CLI-CP Formular solicitare desch ct curent (3).pdf\",\n        \"Anexa 1 Fisa specimene de semnatura (39).pdf\",\n        \"Anexa 3 FATCA CRS   (4).pdf\",\n        \"Anexa1 Lista depozitelor excluse la garantare (21).pdf\",\n        \"F02-III-INF-CP Termeni-conditii-utilizarea_e-xim Banking (4).pdf\",\n        \"F32-III-INF-CP Fisa utilizator e-ximBanking (16).pdf\",\n        \"F41-III.1-CLI-CP Conditii-Generale-de-Afaceri (13).pdf\",\n        \"F02-III-INF-CP Anexa 1 Termeni si conditii_Functionalitati\\r\\n e-ximBanking (4).pdf\",\n        \"Anexa2 CGA Formular pentru informatiile oferite deponentilor\\r\\n (21).pdf\"\n      ]\n    },\n    {\n      \"id\": \"fd9a0a37-7530-4a0e-acce-c0b4a2a1c43c\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"FACTURA TAXA REC VAIDA ELENA\",\n      \"from_name\": \"Albaco Exim\",\n      \"from_address\": \"office@albacoexim.ro\",\n      \"to\": [\n        \"covaciu.gnm@gmail.com\"\n      ],\n      \"received_at\": \"2024-07-04T06:55:24Z\",\n      \"snippet\": \"Buna ziua,Va rugam achitati si trimiteti dovada platii SC ALBACO EXIM SRLstr. Biruintei nr. 46A, Alba Iulia, Jud Alba, R\",\n      \"category\": null,\n      \"labels\": [\n        \"10: Invoices\"\n      ],\n      \"folder\": \"Albaco Exim\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": true,\n      \"attachment_names\": [\n        \"Factura TS9000000066362.pdf.pdf\"\n      ]\n    },\n    {\n      \"id\": \"5d852459-cb6c-42b4-9fb3-bcda8b7b78af\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"Re: Factura taxa emitere atr Vaida Elena\",\n      \"from_name\": \"Albaco Exim\",\n      \"from_address\": \"office@albacoexim.ro\",\n      \"to\": [\n        \"covaciu.gnm@gmail.com\"\n      ],\n      \"received_at\": \"2024-07-02T07:48:38Z\",\n      \"snippet\": \"Buna ziua,O sa va trimitem o factura de taxa de receptie(probabil maine), depunem un dosar de instalatie interioara(azi)\",\n      \"category\": \"fyi\",\n      \"labels\": [\n        \"1: To respond\"\n      ],\n      \"folder\": \"Albaco Exim\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": false,\n      \"attachment_names\": []\n    },\n    {\n      \"id\": \"8cd5913e-282c-43b2-9b99-92e92e7d50c0\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"Factura taxa emitere atr Vaida Elena\",\n      \"from_name\": \"Albaco Exim\",\n      \"from_address\": \"office@albacoexim.ro\",\n      \"to\": [\n        \"covaciu.gnm@gmail.com\"\n      ],\n      \"received_at\": \"2024-06-28T05:58:13Z\",\n      \"snippet\": \"Buna ziua,Atasat va transmit factura pentru taxa emitere atr Vaida ElenaVa rugam achitati si trimiteti dovada platiiCu s\",\n      \"category\": null,\n      \"labels\": [\n        \"10: Invoices\"\n      ],\n      \"folder\": \"Albaco Exim\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": true,\n      \"attachment_names\": [\n        \"Factura TS9000000064268.pdf.pdf\"\n      ]\n    },\n    {\n      \"id\": \"78332dee-6b30-4f4d-90db-0153141dc341\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"Fw: CERERE SPOR DE PUTERE VAIDA ELENA/NR.REG.7040240503281/30.05.2024\",\n      \"from_name\": \"Albaco Exim\",\n      \"from_address\": \"office@albacoexim.ro\",\n      \"to\": [\n        \"covaciu.gnm@gmail.com\"\n      ],\n      \"received_at\": \"2024-05-30T04:57:30Z\",\n      \"snippet\": \"Buna dimineata, Inregistrarea documentelor, CB SC ALBACO EXIM SRLstr. Biruintei nr. 46A, Alba Iulia, Jud Alba, RO-510003\",\n      \"category\": null,\n      \"labels\": [\n        \"3: Fyi\"\n      ],\n      \"folder\": \"Albaco Exim\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": true,\n      \"attachment_names\": [\n        \"image001.jpg\",\n        \"CERERE SPOR DE PUTERE VAIDA ELENA\\r\\n SEMNAT.pdf\"\n      ]\n    },\n    {\n      \"id\": \"15cb32d0-0001-45bd-a29c-3a1cc57b4576\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"CERERE SPOR DE PUTERE VAIDA ELENA\",\n      \"from_name\": \"Albaco Exim\",\n      \"from_address\": \"office@albacoexim.ro\",\n      \"to\": [\n        \"daniela.balint@distributie-energie.ro\"\n      ],\n      \"received_at\": \"2024-05-29T08:59:58Z\",\n      \"snippet\": \"Buna ziua,Va rugam inregistrati cererea atasataVa multumim SC ALBACO EXIM SRLstr. Biruintei nr. 46A, Alba Iulia, Jud Alb\",\n      \"category\": null,\n      \"labels\": [\n        \"3: Fyi\"\n      ],\n      \"folder\": \"Albaco Exim\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": true,\n      \"attachment_names\": [\n        \"CERERE SPOR DE PUTERE VAIDA ELENA SEMNAT.pdf\"\n      ]\n    },\n    {\n      \"id\": \"4ac1436f-e1fc-4c34-9315-841943e5b8bb\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"Re: Proiect trifazic\",\n      \"from_name\": \"Albaco Exim\",\n      \"from_address\": \"office@albacoexim.ro\",\n      \"to\": [\n        \"covaciu.gnm@gmail.com\"\n      ],\n      \"received_at\": \"2024-05-29T04:30:32Z\",\n      \"snippet\": \"Buna ziua,Atasat va transmitem cererea de spor de putere Vaida ElenaVa rugam verificati, semnati si retrimitetiCu stima,\",\n      \"category\": \"fyi\",\n      \"labels\": [\n        \"1: To respond\"\n      ],\n      \"folder\": \"Albaco Exim\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": true,\n      \"attachment_names\": [\n        \"CERERE SPOR DE PUTERE VAIDA ELENA.pdf\"\n      ]\n    },\n    {\n      \"id\": \"9b2b949f-a324-48de-8c43-0e6fe0a9f08e\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"{Spam?} Rezervare\",\n      \"from_name\": \"observatii-externe@eximtur.ro\",\n      \"from_address\": \"observatii-externe@eximtur.ro\",\n      \"to\": [\n        \"cosmin@ipec.ro\"\n      ],\n      \"received_at\": \"2010-11-09T11:19:54Z\",\n      \"snippet\": \"Eximtur - Vacante in strainatate Cererea dvs. a fost preluata la EXIMTUR ! Numarul cererii este: 25442. Detalii cerere: \",\n      \"category\": null,\n      \"labels\": [\n        \"6: Travel\"\n      ],\n      \"folder\": \"observatii-externe@eximtur.ro\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": false,\n      \"attachment_names\": []\n    },\n    {\n      \"id\": \"5934b747-54af-42d5-a00f-0b9fd0ec18e6\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"INTREBARE.\",\n      \"from_name\": \"Metex Imp\",\n      \"from_address\": \"meteximp@yahoo.com\",\n      \"to\": [\n        \"cosmin@ipec.ro\"\n      ],\n      \"received_at\": \"2010-07-12T11:56:31Z\",\n      \"snippet\": \"BUNA ZIUA, VA RUGAM SA NE COMUNICATI CE ATI HOTARAT IN LEGATURA CU PLASA ANTIGRINDINA. Cu stima, Bejan Crisan SC METEX I\",\n      \"category\": null,\n      \"labels\": [\n        \"3: Fyi\"\n      ],\n      \"folder\": \"Metex Imp\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": false,\n      \"attachment_names\": []\n    },\n    {\n      \"id\": \"0a7e1370-21ef-40cd-89ad-a86fdc747d5f\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"Fw: RASPUNS  PROVIZORIU\",\n      \"from_name\": \"Metex Imp\",\n      \"from_address\": \"meteximp@yahoo.com\",\n      \"to\": [\n        \"cosmin@ipec.ro\"\n      ],\n      \"received_at\": \"2010-06-01T16:49:57Z\",\n      \"snippet\": \"BUNA ZIUA, ASA CUM AM PROMIS, AM CAUTAT UN PRET MAI MIC SI AM GASIT PLASA ANTIGRINDINA LA 0,32 EURO/MP. PRETUL INCLUDE T\",\n      \"category\": null,\n      \"labels\": [\n        \"3: Fyi\"\n      ],\n      \"folder\": \"Metex Imp\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": false,\n      \"attachment_names\": []\n    },\n    {\n      \"id\": \"84a0e248-0ddc-4f01-baea-9af962966f57\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"SISTEME  DE  PROTECTIE  ANTIGRINDINA  SI  DE ADUMBRIRE.\",\n      \"from_name\": \"Metex Imp\",\n      \"from_address\": \"meteximp@yahoo.com\",\n      \"to\": [\n        \"cosmin@ipec.ro\"\n      ],\n      \"received_at\": \"2010-05-26T18:19:28Z\",\n      \"snippet\": \"SISTEME DE PROTECTIE ANTIGRINDINA SI DE ADUMBRIRE.\",\n      \"category\": null,\n      \"labels\": [\n        \"3: Fyi\"\n      ],\n      \"folder\": \"Metex Imp\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": true,\n      \"attachment_names\": [\n        \"imag 1.jpg\",\n        \"model SIKURO HAIL 1.jpg\",\n        \"model SIKURO HAIL 2.jpg\",\n        \"model SIKURO HAIL PLUS 1.jpg\",\n        \"model SIKURO HAIL PLUS 2.jpg\",\n        \"model SIKURO HAIL PLUS.jpg\",\n        \"model SIKURO HAIL pt vita de vie 1.jpg\",\n        \"model SIKURO HAIL pt vita de vie 2.jpg\",\n        \"model SIKURO HAIL pt vita de vie.jpg\",\n        \"model SIKURO HAIL.jpg\"\n      ]\n    },\n    {\n      \"id\": \"42d82229-1bd0-418f-b383-d46b025b3367\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"Fw: RASPUNS  PROVIZORIU\",\n      \"from_name\": \"Metex Imp\",\n      \"from_address\": \"meteximp@yahoo.com\",\n      \"to\": [\n        \"cosmin@ipec.ro\"\n      ],\n      \"received_at\": \"2010-05-26T18:06:52Z\",\n      \"snippet\": \"BUNA ZIUA, PENTRU A VA FACE OFERTA CORECT, VA RUGAM SA NE TRANSMITETI NUMELE SOCIETATII ( SAU ALTA FORMA JURIDICA)CARE D\",\n      \"category\": \"fyi\",\n      \"labels\": [\n        \"3: Fyi\"\n      ],\n      \"folder\": \"Metex Imp\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": false,\n      \"attachment_names\": []\n    },\n    {\n      \"id\": \"295fd16d-ec48-4183-a45e-5d92c447264b\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"DESCRIERE POZE  PLASA  ANTIGRINDINA  -- KOPERTURA.\",\n      \"from_name\": \"Metex Imp\",\n      \"from_address\": \"meteximp@yahoo.com\",\n      \"to\": [\n        \"cosmin@ipec.ro\"\n      ],\n      \"received_at\": \"2010-05-26T16:56:35Z\",\n      \"snippet\": \"BUNA ZIUA, VA PREZENTAM CATEVA FOTOGRAFII DE MONTARE PLASA ANTIGRINDINA.PRETUL OFERIT SE REFERA STRICT LA PLASA, FARA SI\",\n      \"category\": null,\n      \"labels\": [\n        \"3: Fyi\"\n      ],\n      \"folder\": \"Metex Imp\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": true,\n      \"attachment_names\": [\n        \"ancora.JPG\",\n        \"ancora 2.JPG\",\n        \"plasa antigrindina.JPG\",\n        \"SIKURO HAIL.JPG\",\n        \"SIKURO SOLE.JPG\",\n        \"sistem de acoperire.JPG\",\n        \"untitledplasa antigrindina 2.JPG\"\n      ]\n    },\n    {\n      \"id\": \"9661073c-e683-478e-8391-5a2aed300fbf\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"PRECIZARI\",\n      \"from_name\": \"Metex Imp\",\n      \"from_address\": \"meteximp@yahoo.com\",\n      \"to\": [\n        \"cosmin@ipec.ro\"\n      ],\n      \"received_at\": \"2010-05-26T03:55:18Z\",\n      \"snippet\": \"BUNA ZIUA, DATORITA FAPTULUI CA AVEM MAI MULTI PRODUCATORI DE PLASA ANTIGRINDINA DIN ITALIA CU CARE COLABORAM, VA RUGAM \",\n      \"category\": null,\n      \"labels\": [\n        \"3: Fyi\"\n      ],\n      \"folder\": \"Metex Imp\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": false,\n      \"attachment_names\": []\n    },\n    {\n      \"id\": \"04fae46c-3071-42d0-95aa-4394fe3e5d65\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"PRECIZARI\",\n      \"from_name\": \"Metex Imp\",\n      \"from_address\": \"meteximp@yahoo.com\",\n      \"to\": [\n        \"cosmin@ipec.ro\"\n      ],\n      \"received_at\": \"2010-05-25T18:04:29Z\",\n      \"snippet\": \"BUNA ZIUA, Pentru a va oferi un pret cat mai corect, va rugam sa aveti amabilitatea sa ne comunicati numarul randurilor,\",\n      \"category\": null,\n      \"labels\": [\n        \"3: Fyi\"\n      ],\n      \"folder\": \"Metex Imp\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": false,\n      \"attachment_names\": []\n    },\n    {\n      \"id\": \"49c60097-7375-443e-aacd-0aacdc695f8e\",\n      \"account_email\": \"covaciu.gnm@eva-org.com\",\n      \"subject\": \"Rezervare Italia, 3-10 jan\",\n      \"from_name\": \"Claudiu Dina\",\n      \"from_address\": \"claudiu.dina@eximtur.ro\",\n      \"to\": [\n        \"covaciu.gnm@gmail.com\"\n      ],\n      \"received_at\": \"2008-12-18T13:19:10Z\",\n      \"snippet\": \"Stimate domnule Covaciu, Intrucat la Park hotel Folgarida nu mai sunt camere disponibile pentru perioada 3-10 jan 09, va\",\n      \"category\": null,\n      \"labels\": [\n        \"6: Travel\"\n      ],\n      \"folder\": \"Claudiu Dina\",\n      \"is_read\": true,\n      \"is_starred\": false,\n      \"is_sent\": false,\n      \"has_attachments\": false,\n      \"attachment_names\": []\n    }\n  ],\n  \"total\": 25,\n  \"limit\": 50,\n  \"offset\": 0\n}"
      }
    ],
    "structuredContent": {
      "items": [
        {
          "id": "089fff65-07de-42e3-b788-571a3a5fe356",
          "account_email": "covaciu.gnm@gmail.com",
          "subject": "Exim Banca Romaneasca Secure File Share CESIRO PRODUCTION SRL-COVACIU COSMIN ADRIAN",
          "from_name": "sftp@eximbank.ro",
          "from_address": "sftp@eximbank.ro",
          "to": [
            "covaciu.gnm@gmail.com"
          ],
          "received_at": "2026-10-23T07:38:32Z",
          "snippet": "Ai primit access catre Exim Banca Romaneasca Secure File Share de la Exim Banca Romaneasca. Linkul va expira la Monday, October 26, 2026 10:30 AM. https://sftp.eximbank.ro/WebClientNew/index.html/?",
          "category": "fyi",
          "labels": [
            "UNREAD",
            "CATEGORY_PERSONAL",
            "Label_43995",
            "INBOX",
            "3: Fyi"
          ],
          "folder": "Exim Banca Romaneasca",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": false,
          "attachment_names": []
        },
        {
          "id": "e95452c5-a822-4aab-aa07-4c1987b82689",
          "account_email": "cosmin.covaciu@ipec.ro",
          "subject": "Acțiune necesară: confirmați contul dvs. până la 29 septembrie",
          "from_name": "Exim Banca Românească | Actualizare cont",
          "from_address": "bounces-xccd6m@localhost.co.uk",
          "to": [
            "cosmin.covaciu@ipec.ro"
          ],
          "received_at": "2026-09-18T10:46:48Z",
          "snippet": "ATENȚIE: Acest e-mail provine din afara companiei. Nu dati click pe linkuri și nu deschideți atașame",
          "category": "fyi",
          "labels": [
            "4: Notification"
          ],
          "folder": "Exim Banca Românească | Actualizare cont",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": false,
          "attachment_names": []
        },
        {
          "id": "a0e8245f-6636-40ed-8e78-d1c87fe7b17d",
          "account_email": "cosmin.covaciu@ipec.ro",
          "subject": "Acțiune necesară: confirmați contul dvs. până la 29 septembrie",
          "from_name": "Exim Banca Românească | Actualizare cont",
          "from_address": "bounces-mswzva@localhost.co.uk",
          "to": [
            "cosmin.covaciu@ipec.ro"
          ],
          "received_at": "2026-09-18T08:28:42Z",
          "snippet": "ATENȚIE: Acest e-mail provine din afara companiei. Nu dati click pe linkuri și nu deschideți atașame",
          "category": "fyi",
          "labels": [
            "4: Notification"
          ],
          "folder": "Exim Banca Românească | Actualizare cont",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": false,
          "attachment_names": []
        },
        {
          "id": "50371f1f-88da-4ab8-96ad-34677ae28388",
          "account_email": "cosmin.covaciu@ipec.ro",
          "subject": "Acțiune necesară: confirmați contul dvs. până la 29 septembrie",
          "from_name": "Exim Banca Românească | Actualizare cont",
          "from_address": "bounces-dr3s5o@aucouventdescollines.be",
          "to": [
            "cosmin.covaciu@ipec.ro"
          ],
          "received_at": "2026-09-16T19:24:30Z",
          "snippet": "ATENȚIE: Acest e-mail provine din afara companiei. Nu dati click pe linkuri și nu deschideți atașame",
          "category": "fyi",
          "labels": [
            "4: Notification"
          ],
          "folder": "Exim Banca Românească | Actualizare cont",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": false,
          "attachment_names": []
        },
        {
          "id": "e6390cf2-5f03-4d91-bb88-1927a2229533",
          "account_email": "cosmin.covaciu@cesiro.com",
          "subject": "Notificare de actualizare a datelor",
          "from_name": "noreply | Exim Banca Romaneasca",
          "from_address": "noreply@eximbank.ro",
          "to": [
            "cosmin.covaciu@cesiro.com"
          ],
          "received_at": "2026-09-01T05:00:24Z",
          "snippet": "Stimate client,\r\n\r\n*In conformitate cu prevederile Regulamentului BNR nr. 2/2019 privind prevenirea ",
          "category": "fyi",
          "labels": [
            "1: To respond"
          ],
          "folder": "noreply | Exim Banca Romaneasca",
          "is_read": false,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": false,
          "attachment_names": []
        },
        {
          "id": "f5d088df-8379-445d-92b3-15ff00efeeef",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "CESIRO PRODUCTION - identificare CONT PROIECT ",
          "from_name": "Oana Baciu",
          "from_address": "oana.baciu@eximbank.ro",
          "to": [
            "covaciu.gnm@gmail.com"
          ],
          "received_at": "2026-07-03T12:48:27Z",
          "snippet": "Continut Intern Buna ziua Domnule Cosmin va trimit identificare fiscala si documentele ce au stat la baza deschiderii ac",
          "category": "fyi",
          "labels": [
            "3: Fyi"
          ],
          "folder": "Oana Baciu",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": true,
          "attachment_names": [
            "image001.jpg",
            "CESIRO - Aga (1).pdf",
            "CESIRO - F40 - Solicitare deschidere cont + fond.pdf",
            "IDENTIFICARE FISCALA.pdf"
          ]
        },
        {
          "id": "44eb4fbe-3ed7-4d7d-afa7-283b28d085c5",
          "account_email": "cosmin.covaciu@cesiro.com",
          "subject": "Undeliverable: Re: FW: CESIRO PRODUCTION SRL - Extrase de cont ",
          "from_name": "postmaster@eximbank.ro",
          "from_address": "postmaster@eximbank.ro",
          "to": [
            "cosmin.covaciu@cesiro.com"
          ],
          "received_at": "2026-05-08T07:57:37Z",
          "snippet": "[https://products.office.com/en-us/CMSImages/Office365Logo_Orange.png?version=b8d100a9-0a8b-8e6a-88e",
          "category": "fyi",
          "labels": [
            "4: Notification"
          ],
          "folder": "postmaster@eximbank.ro",
          "is_read": false,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": true,
          "attachment_names": [
            "CI Cosmin Adrian Covaciu (1).pdf"
          ]
        },
        {
          "id": "29b1a295-23ce-45db-9303-cde3d3d27033",
          "account_email": "cosmin.covaciu@cesiro.com",
          "subject": "RE: FW: CESIRO PRODUCTION SRL - Extrase de cont ",
          "from_name": "Diana Marcu",
          "from_address": "diana.marcu@eximbank.ro",
          "to": [
            "cosmin.covaciu@cesiro.com"
          ],
          "received_at": "2026-05-08T07:24:10Z",
          "snippet": "Continut Intern\r\n\r\nBuna ziua,\r\n\r\nVa transmit atasat extrasele de cont pentru CESIRO PRODUCTION SRL ,",
          "category": "fyi",
          "labels": [
            "5: Finance"
          ],
          "folder": "Diana Marcu",
          "is_read": false,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": true,
          "attachment_names": [
            "image001.jpg",
            "extras cont cesiune.pdf",
            "estras cont  ron.pdf"
          ]
        },
        {
          "id": "efeb0d7e-c1ef-4f73-bbe3-5b3e81a38a38",
          "account_email": "cosmin.covaciu@cesiro.com",
          "subject": "FW: CESIRO PRODUCTION SRL - Extrase de cont ",
          "from_name": "Diana Marcu",
          "from_address": "diana.marcu@eximbank.ro",
          "to": [
            "cosmin.covaciu@cesiro.com",
            "cosmina.stanciu@ipec.ro"
          ],
          "received_at": "2026-04-28T05:10:17Z",
          "snippet": "Continut Intern\r\n\r\nBuna ziua,\r\n\r\nRevenim cu aceasta rugaminte.\r\n\r\nPentru inchiderea contului avem ru",
          "category": "1: To respond",
          "labels": [
            "INBOX",
            "1: To respond"
          ],
          "folder": null,
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": true,
          "attachment_names": [
            "F14-III-CLI-CP Cerere inchidere cont_produse si servicii\r\n   (7).docx",
            "image001.jpg"
          ]
        },
        {
          "id": "f7773cfe-e7f2-46ac-a043-d53b43730121",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "CESIRO PRODUCTION SRL - consultare formulare",
          "from_name": "Mihai Martis",
          "from_address": "Mihai.Martis@eximbank.ro",
          "to": [
            "covaciu.gnm@gmail.com"
          ],
          "received_at": "2024-12-18T09:28:38Z",
          "snippet": "Buna Cosmin, Atasate regasesti, spre consultare, formularele de deschidere cont. Multumesc, Mihai Mihai MARȚIȘ Director ",
          "category": "fyi",
          "labels": [
            "3: Fyi"
          ],
          "folder": "Mihai Martis",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": true,
          "attachment_names": [
            "image001.jpg",
            "_F40-III-CLI-CP Formular solicitare desch ct curent (3).pdf",
            "Anexa 1 Fisa specimene de semnatura (39).pdf",
            "Anexa 3 FATCA CRS   (4).pdf",
            "Anexa1 Lista depozitelor excluse la garantare (21).pdf",
            "F02-III-INF-CP Termeni-conditii-utilizarea_e-xim Banking (4).pdf",
            "F32-III-INF-CP Fisa utilizator e-ximBanking (16).pdf",
            "F41-III.1-CLI-CP Conditii-Generale-de-Afaceri (13).pdf",
            "F02-III-INF-CP Anexa 1 Termeni si conditii_Functionalitati\r\n e-ximBanking (4).pdf",
            "Anexa2 CGA Formular pentru informatiile oferite deponentilor\r\n (21).pdf"
          ]
        },
        {
          "id": "fd9a0a37-7530-4a0e-acce-c0b4a2a1c43c",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "FACTURA TAXA REC VAIDA ELENA",
          "from_name": "Albaco Exim",
          "from_address": "office@albacoexim.ro",
          "to": [
            "covaciu.gnm@gmail.com"
          ],
          "received_at": "2024-07-04T06:55:24Z",
          "snippet": "Buna ziua,Va rugam achitati si trimiteti dovada platii SC ALBACO EXIM SRLstr. Biruintei nr. 46A, Alba Iulia, Jud Alba, R",
          "category": null,
          "labels": [
            "10: Invoices"
          ],
          "folder": "Albaco Exim",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": true,
          "attachment_names": [
            "Factura TS9000000066362.pdf.pdf"
          ]
        },
        {
          "id": "5d852459-cb6c-42b4-9fb3-bcda8b7b78af",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "Re: Factura taxa emitere atr Vaida Elena",
          "from_name": "Albaco Exim",
          "from_address": "office@albacoexim.ro",
          "to": [
            "covaciu.gnm@gmail.com"
          ],
          "received_at": "2024-07-02T07:48:38Z",
          "snippet": "Buna ziua,O sa va trimitem o factura de taxa de receptie(probabil maine), depunem un dosar de instalatie interioara(azi)",
          "category": "fyi",
          "labels": [
            "1: To respond"
          ],
          "folder": "Albaco Exim",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": false,
          "attachment_names": []
        },
        {
          "id": "8cd5913e-282c-43b2-9b99-92e92e7d50c0",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "Factura taxa emitere atr Vaida Elena",
          "from_name": "Albaco Exim",
          "from_address": "office@albacoexim.ro",
          "to": [
            "covaciu.gnm@gmail.com"
          ],
          "received_at": "2024-06-28T05:58:13Z",
          "snippet": "Buna ziua,Atasat va transmit factura pentru taxa emitere atr Vaida ElenaVa rugam achitati si trimiteti dovada platiiCu s",
          "category": null,
          "labels": [
            "10: Invoices"
          ],
          "folder": "Albaco Exim",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": true,
          "attachment_names": [
            "Factura TS9000000064268.pdf.pdf"
          ]
        },
        {
          "id": "78332dee-6b30-4f4d-90db-0153141dc341",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "Fw: CERERE SPOR DE PUTERE VAIDA ELENA/NR.REG.7040240503281/30.05.2024",
          "from_name": "Albaco Exim",
          "from_address": "office@albacoexim.ro",
          "to": [
            "covaciu.gnm@gmail.com"
          ],
          "received_at": "2024-05-30T04:57:30Z",
          "snippet": "Buna dimineata, Inregistrarea documentelor, CB SC ALBACO EXIM SRLstr. Biruintei nr. 46A, Alba Iulia, Jud Alba, RO-510003",
          "category": null,
          "labels": [
            "3: Fyi"
          ],
          "folder": "Albaco Exim",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": true,
          "attachment_names": [
            "image001.jpg",
            "CERERE SPOR DE PUTERE VAIDA ELENA\r\n SEMNAT.pdf"
          ]
        },
        {
          "id": "15cb32d0-0001-45bd-a29c-3a1cc57b4576",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "CERERE SPOR DE PUTERE VAIDA ELENA",
          "from_name": "Albaco Exim",
          "from_address": "office@albacoexim.ro",
          "to": [
            "daniela.balint@distributie-energie.ro"
          ],
          "received_at": "2024-05-29T08:59:58Z",
          "snippet": "Buna ziua,Va rugam inregistrati cererea atasataVa multumim SC ALBACO EXIM SRLstr. Biruintei nr. 46A, Alba Iulia, Jud Alb",
          "category": null,
          "labels": [
            "3: Fyi"
          ],
          "folder": "Albaco Exim",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": true,
          "attachment_names": [
            "CERERE SPOR DE PUTERE VAIDA ELENA SEMNAT.pdf"
          ]
        },
        {
          "id": "4ac1436f-e1fc-4c34-9315-841943e5b8bb",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "Re: Proiect trifazic",
          "from_name": "Albaco Exim",
          "from_address": "office@albacoexim.ro",
          "to": [
            "covaciu.gnm@gmail.com"
          ],
          "received_at": "2024-05-29T04:30:32Z",
          "snippet": "Buna ziua,Atasat va transmitem cererea de spor de putere Vaida ElenaVa rugam verificati, semnati si retrimitetiCu stima,",
          "category": "fyi",
          "labels": [
            "1: To respond"
          ],
          "folder": "Albaco Exim",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": true,
          "attachment_names": [
            "CERERE SPOR DE PUTERE VAIDA ELENA.pdf"
          ]
        },
        {
          "id": "9b2b949f-a324-48de-8c43-0e6fe0a9f08e",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "{Spam?} Rezervare",
          "from_name": "observatii-externe@eximtur.ro",
          "from_address": "observatii-externe@eximtur.ro",
          "to": [
            "cosmin@ipec.ro"
          ],
          "received_at": "2010-11-09T11:19:54Z",
          "snippet": "Eximtur - Vacante in strainatate Cererea dvs. a fost preluata la EXIMTUR ! Numarul cererii este: 25442. Detalii cerere: ",
          "category": null,
          "labels": [
            "6: Travel"
          ],
          "folder": "observatii-externe@eximtur.ro",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": false,
          "attachment_names": []
        },
        {
          "id": "5934b747-54af-42d5-a00f-0b9fd0ec18e6",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "INTREBARE.",
          "from_name": "Metex Imp",
          "from_address": "meteximp@yahoo.com",
          "to": [
            "cosmin@ipec.ro"
          ],
          "received_at": "2010-07-12T11:56:31Z",
          "snippet": "BUNA ZIUA, VA RUGAM SA NE COMUNICATI CE ATI HOTARAT IN LEGATURA CU PLASA ANTIGRINDINA. Cu stima, Bejan Crisan SC METEX I",
          "category": null,
          "labels": [
            "3: Fyi"
          ],
          "folder": "Metex Imp",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": false,
          "attachment_names": []
        },
        {
          "id": "0a7e1370-21ef-40cd-89ad-a86fdc747d5f",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "Fw: RASPUNS  PROVIZORIU",
          "from_name": "Metex Imp",
          "from_address": "meteximp@yahoo.com",
          "to": [
            "cosmin@ipec.ro"
          ],
          "received_at": "2010-06-01T16:49:57Z",
          "snippet": "BUNA ZIUA, ASA CUM AM PROMIS, AM CAUTAT UN PRET MAI MIC SI AM GASIT PLASA ANTIGRINDINA LA 0,32 EURO/MP. PRETUL INCLUDE T",
          "category": null,
          "labels": [
            "3: Fyi"
          ],
          "folder": "Metex Imp",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": false,
          "attachment_names": []
        },
        {
          "id": "84a0e248-0ddc-4f01-baea-9af962966f57",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "SISTEME  DE  PROTECTIE  ANTIGRINDINA  SI  DE ADUMBRIRE.",
          "from_name": "Metex Imp",
          "from_address": "meteximp@yahoo.com",
          "to": [
            "cosmin@ipec.ro"
          ],
          "received_at": "2010-05-26T18:19:28Z",
          "snippet": "SISTEME DE PROTECTIE ANTIGRINDINA SI DE ADUMBRIRE.",
          "category": null,
          "labels": [
            "3: Fyi"
          ],
          "folder": "Metex Imp",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": true,
          "attachment_names": [
            "imag 1.jpg",
            "model SIKURO HAIL 1.jpg",
            "model SIKURO HAIL 2.jpg",
            "model SIKURO HAIL PLUS 1.jpg",
            "model SIKURO HAIL PLUS 2.jpg",
            "model SIKURO HAIL PLUS.jpg",
            "model SIKURO HAIL pt vita de vie 1.jpg",
            "model SIKURO HAIL pt vita de vie 2.jpg",
            "model SIKURO HAIL pt vita de vie.jpg",
            "model SIKURO HAIL.jpg"
          ]
        },
        {
          "id": "42d82229-1bd0-418f-b383-d46b025b3367",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "Fw: RASPUNS  PROVIZORIU",
          "from_name": "Metex Imp",
          "from_address": "meteximp@yahoo.com",
          "to": [
            "cosmin@ipec.ro"
          ],
          "received_at": "2010-05-26T18:06:52Z",
          "snippet": "BUNA ZIUA, PENTRU A VA FACE OFERTA CORECT, VA RUGAM SA NE TRANSMITETI NUMELE SOCIETATII ( SAU ALTA FORMA JURIDICA)CARE D",
          "category": "fyi",
          "labels": [
            "3: Fyi"
          ],
          "folder": "Metex Imp",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": false,
          "attachment_names": []
        },
        {
          "id": "295fd16d-ec48-4183-a45e-5d92c447264b",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "DESCRIERE POZE  PLASA  ANTIGRINDINA  -- KOPERTURA.",
          "from_name": "Metex Imp",
          "from_address": "meteximp@yahoo.com",
          "to": [
            "cosmin@ipec.ro"
          ],
          "received_at": "2010-05-26T16:56:35Z",
          "snippet": "BUNA ZIUA, VA PREZENTAM CATEVA FOTOGRAFII DE MONTARE PLASA ANTIGRINDINA.PRETUL OFERIT SE REFERA STRICT LA PLASA, FARA SI",
          "category": null,
          "labels": [
            "3: Fyi"
          ],
          "folder": "Metex Imp",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": true,
          "attachment_names": [
            "ancora.JPG",
            "ancora 2.JPG",
            "plasa antigrindina.JPG",
            "SIKURO HAIL.JPG",
            "SIKURO SOLE.JPG",
            "sistem de acoperire.JPG",
            "untitledplasa antigrindina 2.JPG"
          ]
        },
        {
          "id": "9661073c-e683-478e-8391-5a2aed300fbf",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "PRECIZARI",
          "from_name": "Metex Imp",
          "from_address": "meteximp@yahoo.com",
          "to": [
            "cosmin@ipec.ro"
          ],
          "received_at": "2010-05-26T03:55:18Z",
          "snippet": "BUNA ZIUA, DATORITA FAPTULUI CA AVEM MAI MULTI PRODUCATORI DE PLASA ANTIGRINDINA DIN ITALIA CU CARE COLABORAM, VA RUGAM ",
          "category": null,
          "labels": [
            "3: Fyi"
          ],
          "folder": "Metex Imp",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": false,
          "attachment_names": []
        },
        {
          "id": "04fae46c-3071-42d0-95aa-4394fe3e5d65",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "PRECIZARI",
          "from_name": "Metex Imp",
          "from_address": "meteximp@yahoo.com",
          "to": [
            "cosmin@ipec.ro"
          ],
          "received_at": "2010-05-25T18:04:29Z",
          "snippet": "BUNA ZIUA, Pentru a va oferi un pret cat mai corect, va rugam sa aveti amabilitatea sa ne comunicati numarul randurilor,",
          "category": null,
          "labels": [
            "3: Fyi"
          ],
          "folder": "Metex Imp",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": false,
          "attachment_names": []
        },
        {
          "id": "49c60097-7375-443e-aacd-0aacdc695f8e",
          "account_email": "covaciu.gnm@eva-org.com",
          "subject": "Rezervare Italia, 3-10 jan",
          "from_name": "Claudiu Dina",
          "from_address": "claudiu.dina@eximtur.ro",
          "to": [
            "covaciu.gnm@gmail.com"
          ],
          "received_at": "2008-12-18T13:19:10Z",
          "snippet": "Stimate domnule Covaciu, Intrucat la Park hotel Folgarida nu mai sunt camere disponibile pentru perioada 3-10 jan 09, va",
          "category": null,
          "labels": [
            "6: Travel"
          ],
          "folder": "Claudiu Dina",
          "is_read": true,
          "is_starred": false,
          "is_sent": false,
          "has_attachments": false,
          "attachment_names": []
        }
      ],
      "total": 25,
      "limit": 50,
      "offset": 0
    },
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "EVA",
        "title": "EVA — asistentul tău de email",
        "version": "1.0.0",
        "websiteUrl": "https://mail.eva-org.com",
        "icons": [
          {
            "src": "https://mail.eva-org.com/icons/icon-512.png",
            "mimeType": "image/png",
            "sizes": [
              "512x512"
            ]
          },
          {
            "src": "https://mail.eva-org.com/icons/icon-192.png",
            "mimeType": "image/png",
            "sizes": [
              "192x192"
            ]
          }
        ]
      }
    }
  },
  "error": null,
  "durationMs": 812
}
````

## mcpToolCall

````json
{
  "type": "mcpToolCall",
  "id": "exec-6947e57b-7902-4db0-9edd-66f9f18594e2",
  "server": "codex_apps",
  "tool": "eva_mail.eva_search_emails",
  "status": "completed",
  "arguments": {
    "link_id": "link_6ae19c4ed7888191a5d7002d96ef4b95",
    "sender": "exim",
    "is_sent": false,
    "limit": 50
  },
  "appContext": {
    "connectorId": "asdk_app_6aa3eadee6ec8191a9bc3b9608c0f1bc",
    "linkId": "link_6ae19c4ed7888191a5d7002d96ef4b95",
    "resourceUri": null,
    "appName": "Eva-Mail",
    "actionName": "eva_search_emails"
  },
  "mcpAppUi": null,
  "pluginId": null,
  "readOnlyHint": true,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\n  \"items\": [],\n  \"total\": 0,\n  \"limit\": 50,\n  \"offset\": 0\n}"
      }
    ],
    "structuredContent": {
      "items": [],
      "total": 0,
      "limit": 50,
      "offset": 0
    },
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "EVA",
        "title": "EVA — asistentul tău de email",
        "version": "1.0.0",
        "websiteUrl": "https://mail.eva-org.com",
        "icons": [
          {
            "src": "https://mail.eva-org.com/icons/icon-512.png",
            "mimeType": "image/png",
            "sizes": [
              "512x512"
            ]
          },
          {
            "src": "https://mail.eva-org.com/icons/icon-192.png",
            "mimeType": "image/png",
            "sizes": [
              "192x192"
            ]
          }
        ]
      }
    }
  },
  "error": null,
  "durationMs": 2474
}
````

## Asistent

Am găsit **7 emailuri cu expeditor @eximbank.ro** în conturile conectate:

| Data | Expeditor | Subiect / conținut |
|---|---|---|
| **23.10.2026** | sftp@eximbank.ro | **Secure File Share – CESIRO PRODUCTION SRL–COVACIU COSMIN ADRIAN**. Acces la fișiere; linkul avea expirarea la 26 octombrie. |
| **01.09.2026** | noreply@eximbank.ro | **Notificare de actualizare a datelor** — necitit. |
| **03.07.2026** | Oana Baciu | **CESIRO PRODUCTION – identificare CONT PROIECT**. Atașamente: identificare fiscală, AGA și solicitare deschidere cont. |
| **08.05.2026** | postmaster@eximbank.ro | **Undeliverable: Re: FW: CESIRO PRODUCTION SRL – Extrase de cont** — notificare de nelivrare, necitită. |
| **08.05.2026** | Diana Marcu | **RE: FW: CESIRO PRODUCTION SRL – Extrase de cont**. Atașate extrasele de cont de cesiune și în RON — necitit. |
| **28.04.2026** | Diana Marcu | **FW: CESIRO PRODUCTION SRL – Extrase de cont**. Revenire privind închiderea contului, cu formular atașat. |
| **18.12.2024** | Mihai Martiș | **CESIRO PRODUCTION SRL – consultare formulare**. Formulare pentru deschiderea contului și e-ximBanking. |

Au mai apărut **3 mesaje suspecte**, din 16 și 18 septembrie 2026, cu numele „Exim Banca Românească” și subiectul „Acțiune necesară: confirmați contul dvs. până la 29 septembrie”, dar trimise de pe domenii străine băncii: `localhost.co.uk` și `aucouventdescollines.be`.
