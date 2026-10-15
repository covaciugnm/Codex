from pathlib import Path
import json,hashlib
from openpyxl import load_workbook
R=Path.cwd();A=R/'Acasa';D='2026.10.08'
data=json.loads((A/'Surse'/f'{D} Inventar si echivalente.json').read_text('utf8'))
w=load_workbook(A/f'{D} Acasa inventar si echivalente.xlsx',data_only=False)
assert w['Inventar foto'].max_row==len(data['inventory'])+5
assert w['Echivalente propuse'].max_row==len(data['equivalents'])+5
assert len({r['ID'] for r in data['inventory']})==len(data['inventory'])
assert all(hashlib.sha256((A/p['salvat']).read_bytes()).hexdigest()==p['sha256'] for p in data['photos'])
assert all(c.data_type!='e' for s in w for row in s for c in row)
checks={'fotografii_originale_hash_verificat':7,'pozitii_inventar':len(data['inventory']),'echivalari_corelate':len(data['equivalents']),'foi':w.sheetnames,'erori_excel':0,'cantitatile_nu_reprezinta_deviz':True}
(A/'Lucru'/f'{D} Verificari.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf8')
sources='''2026.10.08 — Surse tehnice pentru criterii, nu certificare a instalației
Schneider Electric — Electrical Installation Guide
Dimensionarea protecției și conductorului: https://www.electrical-installation.org/enwiki/Practical_values_for_a_protective_scheme
Protecție suplimentară de înaltă sensibilitate: https://www.electrical-installation.org/enwiki/Additional_measure_of_protection_against_direct_contact
Selectarea RCD în prezența componentelor DC: https://www.electrical-installation.org/enwiki/RCDs_selection_in_presence_of_DC_earth_leakage_currents
Fotovoltaic / tip diferențial conform invertorului: https://www.electrical-installation.org/enwiki/Power_quality_-_impact_of_solar_self-consumption
Siemens: exemplu de fișă pentru 3RT1054-1LA06, NU identificarea aparatului din poze: https://support.industry.siemens.com/teddatasheet/?caller=SIOS&format=pdf&language=en&mlfbs=3RT1054-1LA06
Sursele Tongou specifice SKU sunt în Excel/JSON și în catalogul arhivat, cu manualele originale. Niciun nominal sau cod complet nu a fost atribuit aparatului existent numai dintr-un exemplu online.
'''
(A/'Surse'/f'{D} Surse tehnice.txt').write_text(sources,encoding='utf8')
entry='''

2026.10.08 | ACASA — INVENTAR FOTO ȘI ECHIVALENTE TONGOU
Status scurt: 7 fotografii originale salvate cu hash; 139 poziții de inventar vizual, inclusiv accesorii și poziții deduse. Excel, două liste CSV și date JSON. Preferință Zigbee apoi Wi-Fi; echivalențe condiționate, diferențe și stoc documentate. Nu este listă de comandă sau proiect de execuție.
Ultimul răspuns: cerere și fotografii PRIMITE de la utilizator în chat. Nicio comunicare nouă a furnizorului. Expeditor: utilizator; destinatar: asistent; CC și ID Eva-Mail: nu se aplică. Data capturării pozelor și amplasamentul instalației nu sunt confirmate.
Următorul pas: fotografii apropiate ale etichetelor ascunse, identificarea circuitelor și verificarea de către electrician a nominalelor, RCD, capacității de rupere, selectivității și sarcinilor. C80/C100 și contactoarele nu au echivalent direct verificat în selecția Tongou.
Sursă: Acasa/2026.10.08 Acasa inventar si echivalente.xlsx; Acasa/Poze originale; Acasa/Surse/2026.10.08 Manifest fotografii.json; catalogul Tongou arhivat 2026.10.08.
Acoperire: toate cele 7 imagini; componentele acoperite/ilizibile sunt marcate, nu identificate prin presupuneri. Nu se presupune că fiecare fotografie reprezintă un tablou distinct. Fără trimitere, comandă, rezervare de stoc sau intervenție fizică.
'''
for p in [R/f'{D} Log progres proiect.txt',R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri'/f'{D} Log discutii - Tongou Conex Electronic.txt']:
 old=p.read_text('utf8');
 if 'ACASA — INVENTAR FOTO ȘI ECHIVALENTE TONGOU' not in old:
  (A/'Lucru'/f'{D} Istoric {p.name}').write_text(old,encoding='utf8');p.write_text(old+entry,encoding='utf8')
(A/f'{D} Jurnal Acasa.txt').write_text(entry,encoding='utf8')
p=R/'folder map/README.md';old=p.read_text('utf8')
if '## 2026.10.08 — Acasa: inventar foto' not in old:p.write_text(old+'\n\n## 2026.10.08 — Acasa: inventar foto\nDosar: ../Acasa/. Intrare: 2026.10.08 Citeste intai.txt și 2026.10.08 Acasa inventar si echivalente.xlsx. Șapte originale, inventar vizual, echivalente Tongou condiționate și protecții de verificat; două liste CSV. Cantitățile sunt observații, nu deviz. Codurile acoperite și amplasamentul instalației nu sunt confirmate.\n',encoding='utf8')
print(json.dumps(checks,ensure_ascii=False))
