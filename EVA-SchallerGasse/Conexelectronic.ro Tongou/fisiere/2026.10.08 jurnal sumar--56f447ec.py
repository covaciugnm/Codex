from pathlib import Path
R=Path.cwd();A=R/'Acasa';D='2026.10.08'
entry='''

2026.10.08 | ACASA — NECESAR ȘI STOC + DOCUMENTAȚIE ACCESIBILĂ
Status scurt: adăugată fila Necesar si stoc în Excelul existent; 47 grupuri de inventar, centralizare prin formule pe SKU. Scenariu condiționat: 59 necesare, 5 acoperite de stoc, 54 ulterior. 43080: 17/1; 43082: 40/3; 43081: 1/2; 43074: 1/0 (necesar/stoc). Diferența totală stoc-necesar -53 nu este lipsa de 54 bucăți, deoarece există un excedent de 1 buc. la alt SKU; surplusul nu substituie alt modul.
Ultimul răspuns: utilizatorul a cerut în chat tabel simplu, centralizator pentru comandă și acces la fișe tehnice; PRIMIT, expeditor utilizator, destinatar asistent, CC/ID Eva-Mail nu se aplică. Nu există comunicare nouă de la furnizor.
Documentație: 12 PDF-uri originale copiate integral în Acasa/Documentatie Tongou/PDF producator; pagină HTML index cu 29 produse și câte o fișă HTML de sinteză per SKU. Sintezele sunt marcate explicit, nu sunt datasheet-uri oficiale. Documentele de familie/certificatele nu confirmă automat SKU exact. Verificate 131 linkuri locale; valorile, stilurile celulelor, tabelele și panourile înghețate ale celor patru foi inițiale păstrate.
Următorul pas: validarea echivalențelor și cantităților fizice înainte de comandă; actualizarea stocului la achiziție. Piesele ilizibile și componentele fără echivalent nu intră în necesarul SKU. Stocul este captura 2026.10.08, nerezervat. Nicio comandă, achiziție, publicare online sau trimitere.
Sursă: Acasa/2026.10.08 Acasa inventar si echivalente.xlsx; Acasa/Documentatie Tongou/2026.10.08 Documentatie Tongou.html; registrul JSON aferent. Versiunea anterioară Excel păstrată în Lucru.
'''
for p in [A/f'{D} Jurnal Acasa.txt',R/f'{D} Log progres proiect.txt',R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri'/f'{D} Log discutii - Tongou Conex Electronic.txt']:
 old=p.read_text('utf8')
 if 'ACASA — NECESAR ȘI STOC + DOCUMENTAȚIE ACCESIBILĂ' not in old:p.write_text(old+entry,encoding='utf8')
p=A/f'{D} Citeste intai.txt';old=p.read_text('utf8')
if 'Fila nouă' not in old:p.write_text(old+'\nFila nouă „Necesar si stoc”: tabel simplu și centralizator provizoriu, cu formule pentru diferență, cantitate acoperită și lipsă.\nFișe accesibile: Documentatie Tongou/2026.10.08 Documentatie Tongou.html — 29 sinteze HTML + 12 PDF-uri originale.\n',encoding='utf8')
p=R/'folder map/README.md';old=p.read_text('utf8')
if 'Acasa/Documentatie Tongou' not in old:p.write_text(old+'\nActualizare Acasa: Excelul include fila „Necesar si stoc”. Documentația este accesibilă prin ../Acasa/Documentatie Tongou/2026.10.08 Documentatie Tongou.html (29 sinteze, 12 PDF-uri originale). Necesarul este provizoriu, după validare tehnică.\n',encoding='utf8')
(A/'Surse'/f'{D} Cereri sumar si documentatie.txt').write_text('''2026.10.08 | Mesaje PRIMITE în chat
Expeditor: utilizator; destinatar: asistent; CC/ID Eva-Mail: nu se aplică

creaza un tab in fisier simplu cu prima coloana ce aiidentificat - cate bucati - echivalent utilizabil - stoc
la final o lista cu prima coloana modulul Tongue - stocul - necesar - diferenta - sa vedem ce se poate comanda si si ce trebuie cumparati si comandat ulterior

nu vad fise tehnice -pentru fiecare echipament de la tongue - daca nu gasesti creazad in pagina Web ?
''',encoding='utf8')
print('Jurnale actualizate')
