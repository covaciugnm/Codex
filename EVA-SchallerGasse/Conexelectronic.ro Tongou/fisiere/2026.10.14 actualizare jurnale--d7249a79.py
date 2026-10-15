from pathlib import Path
R=Path.cwd();D=Path(__file__).parent
entry='''\n\n2026.10.14 | CONEX — OFERTĂ IDENTIFICATĂ ÎN SPAM
Status scurt: descărcată și verificată oferta OFR000012370 (datată 2026.10.07, primită 2026.10.08), 20 × 2P Wi-Fi SKU43067 + 5 × 3P Wi-Fi SKU43068, total 7.485,00 lei cu TVA. 5 + 3 buc. declarate din stoc în ofertă; termen nespecificat pentru alte 15 + 2. OP avans, valabilitate 7 zile; reconfirmare necesară. Oferta nu este acceptată și nu este comandă.
Ultimul răspuns: 2026.10.09, office@cesiro.ro anunță că mai studiază și alte modele; citează solicitarea de feedback Conex. Email original ofertă 989e6cb3-2af4-45cd-91b5-113a795f4ef1, contact@conexelectronic.ro → office@cesiro.ro, CC covaciu.gnm@gmail.com; PRIMIT, SPAM. Și oferta veche Zigbee OFR000011675 de 11.768,40 lei cu TVA a fost arhivată separat.
Următorul pas: clarificarea variantei Zigbee/RCBO față de Wi-Fi ofertat, termenelor pentru cantitățile fără termen și actualizarea disponibilității/valabilității. Pentru verificarea tuturor celor trei autentificări EVA: este necesar acces la cesiro.horeca@gmail.com (team, necăutabil) și office@eva-org.com (neexpus). Nu a fost trimis niciun email.
Acoperire: căutări globale în cele 17 căsuțe căutabile și documentele accesibile. API-ul de căutare email nu returnează ofertele etichetate SPAM nici cu category=spam; ele au fost regăsite prin documente și citite după ID. Nu se afirmă verificare exhaustivă a celor trei conturi EVA. Datele ultimei sincronizări sunt în sursele salvate.
Sursă: 04. Firme + Executie/08. Ofertanti electrice/Tongou - Conex Electronic/2026.10.14 Oferta primita Conex/2026.10.14 Rezultat verificare Conex.txt și PDF-urile originale. Cerere primită în chat de la utilizator către asistent; CC/ID Eva-Mail ale cererii nu se aplică.
'''
for p in [R/'2026.10.14 Log progres proiect.txt',R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.14 Log discutii - Tongou Conex Electronic.txt']:
 old=p.read_text('utf8') if p.exists() else ''
 if 'CONEX — OFERTĂ IDENTIFICATĂ ÎN SPAM' not in old:p.write_text(old+entry,encoding='utf8')
(D/'2026.10.14 Jurnal verificare.txt').write_text(entry,encoding='utf8')
p=R/'folder map/README.md';old=p.read_text('utf8')
if '## 2026.10.14 — Oferta Conex' not in old:p.write_text(old+'\n\n## 2026.10.14 — Oferta Conex\nOfertă primită 2026.10.08 în SPAM: OFR000012370, Wi-Fi, 7.485,00 lei cu TVA. Dosar: ../04. Firme + Executie/08. Ofertanti electrice/Tongou - Conex Electronic/2026.10.14 Oferta primita Conex/. Originalele PDF și 4 mesaje salvate. Limită: cesiro.horeca@gmail.com necăutabil, office@eva-org.com neexpus; nu se afirmă verificare completă a tuturor autentificărilor. Oferta din mai este istoric.\n',encoding='utf8')
(D/'2026.10.14 Cerere utilizator.txt').write_text('Data: 2026.10.14\nExpeditor: utilizator în chat\nDestinatar: asistent\nCC/ID Eva-Mail: nu se aplică\nStatut: PRIMIT\n\ncei de la conex au trimis ceva email cu oferta pentru echipamente verifica pe cele trei conturi de EVA - \ncovaciu.gnm@gmail.com / cesiro.horeca@gmail.com / office@eva-org.com - ele au mai multe contrui de email in aplicatie - sa verifici pe toarte conturile dupa adresa de email\n',encoding='utf8')
print('Jurnale actualizate')
