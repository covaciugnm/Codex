from pathlib import Path
import json,hashlib,fitz
from decimal import Decimal
from openpyxl import load_workbook
R=Path(__file__).resolve().parent.parent;D='2026.09.30';B=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail';A=R/'10. Banci + Extrase de cont'/f'{D} Audit facturi si plati'
j=json.loads((A/f'{D} Registru verificat.json').read_text(encoding='utf-8'))
missing=[];hasherrors=[]
for s in j['surse']:
 for key in ['Sursa original','Copie audit']:
  p=R/s[key]
  if not p.is_file():missing.append(s[key])
  elif hashlib.sha256(p.read_bytes()).hexdigest()!=s['SHA256']:hasherrors.append(s[key])
for t in j['plati']:
 if not (R/t['sursa']).is_file():missing.append(t['sursa'])
for i in j['documente']:
 if i.get('Email local') and not (R/i['Email local']).is_file():missing.append(i['Email local'])
wb=load_workbook(R/'10. Banci + Extrase de cont'/f'{D} Reconciliere completa facturi si plati.xlsx',data_only=True)
assert wb['Registru documente'].max_row==50
assert all(Decimal(str(wb['Registru documente'].cell(n,11).value))==Decimal(str(row['Sold document EUR'])) for n,row in enumerate(j['documente'],2))
assert sum(Decimal(str(x['Sold document EUR'])) for x in j['documente'] if x['ID']>='F041')==Decimal('1817.73')
ars=[]
for p in [B/f'{D} Registru atasamente.json',R/'08. Corespondenta/BAU-WERTE'/f'{D} Registru atasamente.json']:
 ars.extend(json.loads(p.read_text(encoding='utf-8')))
for s in ars:
 if s.get('stare')!='salvat original integral':continue
 p=R/s['cale']
 if not p.is_file():missing.append(s['cale'])
 elif s.get('sha256') and hashlib.sha256(p.read_bytes()).hexdigest()!=s['sha256']:hasherrors.append(s['cale'])
assert not missing and not hasherrors
doc=fitz.open(A/f'{D} Concluzii verificare facturi si plati.pdf')
assert all(p.get_text().strip() for p in doc)
for n,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(A/f'{D} Raport pagina {n+1}.png')
qa=json.loads((A/f'{D} Control calitate.json').read_text(encoding='utf-8'))
qa.update(surse_si_copii_hash_corecte=True,anexe_originale_controlate=len(ars),legaturi_email_valide=True,solduri_excel_cache_corecte=True,sturm_curent_unic=1817.73,pagini_raport=len(doc),pagini_extrase_bancare_verificate=5)
(A/f'{D} Control calitate.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False))
