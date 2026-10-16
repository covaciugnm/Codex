import json, pathlib, shutil, urllib.request, hashlib, sys, base64
from pypdf import PdfReader
import openpyxl
sys.stdout.reconfigure(encoding='utf-8')
work=pathlib.Path(__file__).parent
root=pathlib.Path(r'Z:\00. Proiecte 2025\AFIR FotoVoltaic 1\50. Fabrica Nuci\nuttechnology.com')
for d in ['01_Comunicatii','02_Oferte','03_Cataloage','04_Fise_electrice_propuse','05_Documente_interne','06_Media','07_Centralizatoare','08_Dosar_tehnic']:
 (root/d).mkdir(exist_ok=True)
for p in list(root.glob('*.pdf')): shutil.move(str(p),str(root/'03_Cataloage'/p.name))
for p in list(root.glob('*.xlsx')): shutil.move(str(p),str(root/'05_Documente_interne'/p.name))
emails=json.loads((work/'emails.json').read_text(encoding='utf-8'))
downloads=json.loads((work/'downloads.json').read_text(encoding='utf-8'))
for e in emails:
 name=e['received_at'][:10]+'_'+e['id'][:8]+'.txt'
 e['local']='01_Comunicatii/'+name
 (root/e['local']).write_text('Export text EVA (nu fisier EML original)\nID: '+e['id']+'\nData UTC: '+e['received_at']+'\nDe la: '+e['from_address']+'\nCatre: '+', '.join(e['to'])+'\nCC: '+', '.join(e.get('cc',[]))+'\nSubiect: '+e['subject']+'\nAtasamente: '+', '.join(a['name'] for a in e['attachments'])+'\n\n'+e['text'],encoding='utf-8')
for d in downloads:
 name=d['filename']
 folder='02_Oferte' if name.startswith('Oferta') else '04_Fise_electrice_propuse' if name.startswith('Fisa') else '05_Documente_interne'
 dest=root/folder/(d['id'][:8]+'_'+name)
 if not dest.exists():
  chunks=work/(d['id']+'.chunks.json')
  if chunks.exists(): dest.write_bytes(b''.join(base64.b64decode(c) for c in json.loads(chunks.read_text())))
  else:
   matches=[p for p in (root.parent/'TechnoMS').rglob('*') if p.is_file() and p.stat().st_size==d['size']]
   if len(matches)!=1: raise ValueError((name,matches))
   shutil.copy2(matches[0],dest)
 d['local']=str(dest.relative_to(root))
for p in (root.parent/'TechnoMS').glob('*'):
 if p.is_file() and p.suffix.lower() in ['.docx','.mp4']:
  target=root/('06_Media' if p.suffix.lower()=='.mp4' else '05_Documente_interne')/p.name
  if not target.exists(): shutil.copy2(p,target)
(root/'01_Comunicatii'/'Emailuri_export.json').write_text(json.dumps(emails,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(work/'chats.json',root/'01_Comunicatii'/'WhatsApp_export.json')
(work/'downloads.json').write_text(json.dumps(downloads,ensure_ascii=False),encoding='utf-8')
(work/'emails.json').write_text(json.dumps(emails,ensure_ascii=False),encoding='utf-8')
wb=openpyxl.load_workbook(next((root/'05_Documente_interne').glob('Nuttechnology*.xlsx')),data_only=True)
data={s.title:[[v if not hasattr(v,'isoformat') else v.isoformat() for v in row] for row in s.values] for s in wb}
(work/'existing.json').write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
for name,rows in data.items():
 print('\nSHEET',name)
 for row in rows[:8]: print(row)
pdfs=[]
for p in root.rglob('*.pdf'):
 r=PdfReader(p)
 pages=[pg.extract_text() or '' for pg in r.pages]
 pdfs.append({'path':str(p.relative_to(root)),'pages':pages,'hash':hashlib.sha256(p.read_bytes()).hexdigest()})
(work/'pdfs.json').write_text(json.dumps(pdfs,ensure_ascii=False),encoding='utf-8')
for p in pdfs:
 if '02_Oferte' in p['path']: print('\nOFFER',p['path'],'\n',p['pages'][0])

