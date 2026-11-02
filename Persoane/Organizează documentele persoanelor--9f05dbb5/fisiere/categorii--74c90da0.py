import re,unicodedata
def categoria(t):
 t=' '+re.sub('[^A-Z0-9]+',' ',unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().upper())+' '
 for k,rx in [
 ('08. CV si declaratii',r'\b(CV|CURRICULUM VITAE|DECLARATIE|DECLARATII)\b'),
 ('02. Certificate civile',r'\b(NASTERE|CASATORIE|DECES|DIVORT)\b'),
 ('07. Permise si auto',r'\b(PERMIS DE CONDUCERE|PERMIS CONDUCERE|TALON AUTO|CERTIFICAT DE INMATRICULARE AUTO|CARTE DE IDENTITATE A VEHICULULUI)\b'),
 ('01. CI si Pasaport',r'\b(CI|BULETIN|PASAPORT|PASSPORT|CARTE DE IDENTITATE|CARTE IDENTITATE)\b'),
 ('03. Diplome si Cursuri',r'\b(DIPLOM\w*|BACALAUREAT|LICENT[AE]\w*|ACREDITAR\w*|CERTIFICAT (?:DE )?(?:ABSOLVIRE|CALIFICARE|COMPETENT\w*|FORMARE|SPECIALIZARE)|CURSURI|ATESTAT\w*)\b'),
 ('06. EORI',r'\bEORI\b'),
 ('05. Contracte personale',r'\b(CIM|CONTRACT\w*)\b')]:
  if re.search(rx,t):return k
 return '09. Alte documente'
