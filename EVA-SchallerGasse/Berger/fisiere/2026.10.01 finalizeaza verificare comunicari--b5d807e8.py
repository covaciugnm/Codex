from pathlib import Path
import json,hashlib
from email import policy
from email.parser import BytesParser
from openpyxl import load_workbook
import fitz
R=Path(__file__).resolve().parent.parent
P=R/'08. Corespondenta/2026.10.01 Actualizare comunicari'
B=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
data=json.loads((P/'2026.10.01 Dovezi Eva-Mail.json').read_text(encoding='utf-8'))
reg=json.loads((B/'2026.10.01 Registru comunicatii.json').read_text(encoding='utf-8'))
att=json.loads((B/'2026.10.01 Registru atasamente.json').read_text(encoding='utf-8'))
idx={x['cale']:x for x in json.loads((R/'folder map/inventar.json').read_text(encoding='utf-8'))}
newids={e['id'] for e in data['emails']}
newatt=[a for a in att if a['email_id'] in newids]
assert len(reg['comunicatii'])==786 and len(newids)==6 and len(newatt)==7
for a in newatt:
 raw=(R/a['cale']).read_bytes()
 assert len(raw)==a['size'] and hashlib.sha256(raw).hexdigest()==a['sha256']
for row in reg['comunicatii']:
 if row['id'] not in newids:continue
 p=(R/row['cale']).with_suffix('.eml')
 m=BytesParser(policy=policy.default).parsebytes(p.read_bytes())
 assert m['X-Eva-Mail-ID']==row['id'] and m['X-Unsent'] is None
 assert len(list(m.iter_attachments()))==row['atasamente']
 assert m['X-Eva-Status']==('SENT' if row['sens']=='TRIMIS' else 'RECEIVED')
w=load_workbook(R/'2026.10.01 Log progres proiect.xlsx')
assert w['Comunicatii'].max_row==787
assert set(newids).issubset({row[9] for row in w['Comunicatii'].values})
pdf=P/'2026.10.01 Atasamente/2026.10.01 91b2e1fd 2026-10-01 Werkvertrag TOMS - Entwurf AG v3.pdf'
with fitz.open(pdf) as f:
 text='\n'.join(pg.get_text() for pg in f)
 assert len(f)==22 and all(v in text for v in ['37.900','25.000','1.500','8.000','3.400','Entwurf'])
audit=[]
backups=sorted(P.glob('2026.10.01 Istoric inainte de verificare *'))
for backup in backups:
 for p in backup.rglob('*'):
  if not p.is_file():continue
  relative=p.relative_to(backup).as_posix();e=idx.get(relative)
  if e:
   sha=hashlib.sha256(p.read_bytes()).hexdigest()
   audit.append({'cale':relative,'copie_istorica':p.relative_to(R).as_posix(),'hash_identic_index':sha==e['sha256'],'sha256':sha})
output={'data':'2026.10.01','mesaje_noi':6,'originale_verificate':7,'mesaje_total':786,'fisiere_verificate_fata_de_index':audit,'atasamente_originale':newatt,'original_TOMS_verificat':{'cale':pdf.relative_to(R).as_posix(),'pagini':22,'net_structura_verificare':'25.000 + 1.500 + 8.000 = 34.500 EUR','net_Bauwerksbuch':'3.400 EUR','total_net':'37.900 EUR','status':'Propunere trimisa; acceptare/semnare neconfirmata'},'EML':'Export reconstruit API cu toate anexele reale; statut si ID verificate; nu este MIME original.'}
(P/'2026.10.01 Audit verificare.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
print('Verificat: 6 exporturi TXT/JSON/EML, 7 originale SHA-256, 786 comunicatii; PDF TOMS si jurnal Excel conforme.')
