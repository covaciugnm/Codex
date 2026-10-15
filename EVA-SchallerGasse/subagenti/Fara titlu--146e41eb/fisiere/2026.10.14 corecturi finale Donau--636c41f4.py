from pathlib import Path
import re
d=Path('05. Asigurari/Asigurare cladire/2026.10.14 Analiza juridica Donau')
for p in sorted(d.glob('2026.10.14 0[12]*.txt')):
 t=p.read_text(encoding='utf8')
 fixes={'§ 39alin.3':'§ 39 alin.3','globaleDONAU':'globale DONAU','până în2036':'până în 2036','expresABS':'expres ABS','DacăDONAU':'Dacă DONAU','Exporturi în05':'Exporturi în 05','trimisID':'trimis ID ','primitID':'primit ID ','Scrisoare17sept':'Scrisoarea 2026.09.17','1416imputare':'1416 imputare','p. 2principiu':'p.2, principiu','cu22':'cu 22','WEG2002':'WEG 2002','2026.02.03,89':'2026.02.03, 89','nu mai enumeră § 91':'nu enumeră § 91','SHA-256fc':'SHA-256 fc','SHA-25696':'SHA-256 96','SHA-2561af':'SHA-256 1af','SHA-256237':'SHA-256 237','§§ 1,36, 38,39, 39a, 40, 41a, 42,68':'§§ 1, 36, 38, 39, 39a, 40, 41a, 41b, 42, 68','[L2, L3]':'[L1 § 41b; L2, L3]','în acest sens':'în acest sens'}
 for a,b in fixes.items():t=t.replace(a,b)
 # Legal paragraph formatting outside verbatim quotes only.
 pieces=re.split('(„[^”]*”)',t)
 for i,s in enumerate(pieces):
  if s.startswith('„'):continue
  s=re.sub(r'\balin\.(?=\d)', 'alin. ',s)
  s=re.sub(r'\bp\.(?=\d)','p. ',s)
  s=re.sub(r'\b[aA]rt\.(?=\d)',lambda m:m[0]+' ',s)
  s=s.replace('§§ 5c,191c','§§ 5c, 191c').replace('§§ 1052,1431,1432','§§ 1052, 1431, 1432')
  pieces[i]=s
 p.write_text(''.join(pieces),encoding='utf8')
