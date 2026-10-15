from pathlib import Path
R=Path.cwd()
entry='''\n\n2026.10.14 | CONEX — COMPARAȚIE OFERTĂ ȘI STOC LIVE
Status scurt: toate cele 4 SKU ofertate verificate live. 43067: 5 buc/289 lei; 43068: 3 buc/519 lei; 43079: 5 buc/510 lei; 43081: 2 buc/719 lei (prețuri site cu TVA). Cele 8 Wi-Fi disponibile costă 3.002 lei la site sau 2.622 lei dacă Conex menține prețurile ofertei pentru livrare parțială; economie condiționată 380 lei. 7 RCBO Zigbee disponibile costă 3.988 lei la site; oferta din mai este doar reper istoric (3.589,20 lei pentru aceleași 7 bucăți).
Ultimul răspuns: nicio comunicare nouă; surse comerciale publice verificate 2026.10.14 și cele două PDF-uri primite anterior. Cererea de comparație a fost PRIMITĂ în chat de la utilizator către asistent; CC/ID Eva-Mail nu se aplică.
Următorul pas: reconfirmarea discountului, valabilității și livrării parțiale, plus alegerea MCB Wi-Fi versus RCBO Zigbee. Fără comandă sau rezervare. Stocul poate varia după verificare.
Sursă: 04. Firme + Executie/08. Ofertanti electrice/Tongou - Conex Electronic/2026.10.14 Comparatie oferta si stoc/2026.10.14 Comparatie tabelara Conex.txt; 4 pagini HTML originale și date JSON din același dosar.
'''
for p in [R/'2026.10.14 Log progres proiect.txt',R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.14 Log discutii - Tongou Conex Electronic.txt']:
 old=p.read_text('utf8')
 if 'CONEX — COMPARAȚIE OFERTĂ ȘI STOC LIVE' not in old:p.write_text(old+entry,encoding='utf8')
p=R/'folder map/README.md';old=p.read_text('utf8')
if '## 2026.10.14 — Comparație Conex' not in old:p.write_text(old+'\n\n## 2026.10.14 — Comparație Conex\nStoc și prețuri live pentru 4 SKU, comparate cu ofertele originale în ../04. Firme + Executie/08. Ofertanti electrice/Tongou - Conex Electronic/2026.10.14 Comparatie oferta si stoc/. 8 Wi-Fi: site 3.002 lei vs ofertă condiționată 2.622 lei. 7 RCBO Zigbee: site 3.988 lei. Fără comandă; prețurile ofertate necesită reconfirmare.\n',encoding='utf8')
print('Actualizat')
