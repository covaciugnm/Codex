from pathlib import Path
import json, urllib.request,hashlib,re,fitz,email
from email import policy
R=Path(__file__).resolve().parent.parent
P=R/'08. Corespondenta/2026.09.30 Raspuns Commerz - analiza Donau 2616052'
P.mkdir(exist_ok=True)
D=json.loads((R/'folder map/2026.09.30 Donau raspuns surse.json').read_text(encoding='utf-8'))
records=[]
for x in D['attachments']:
 a=x['metadata']; name='2026.09.30 '+a['name'];p=P/name
 if not p.exists():
  with urllib.request.urlopen(x['download']['url'],timeout=60) as f: b=f.read()
  assert len(b)==a['size'];p.write_bytes(b)
 b=p.read_bytes();records.append({'id':a['id'],'nume_original':a['name'],'cale':p.relative_to(R).as_posix(),'size':len(b),'sha256':hashlib.sha256(b).hexdigest(),'status':'PRIMIT; original integral'})
 if p.suffix.lower()=='.pdf':
  doc=fitz.open(p);text='\n'.join(f'PAGINA {i+1}\n'+pg.get_text() for i,pg in enumerate(doc));(P/(p.stem+' - text.txt')).write_text(text,encoding='utf-8')
  print(p.name,'pagini',len(doc),text[:15000]);doc[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(R/'folder map'/('2026.09.30 verificare '+a['id'][:8]+'.png'))
 elif p.suffix.lower()=='.eml':
  msg=email.message_from_bytes(b,policy=policy.default)
  print(p.name,dict((k,str(msg[k])) for k in ['From','To','Date','Subject']))
  print('EML continut:',[(part.get_content_type(),part.get_filename()) for part in msg.walk()])
for e in D['emails']:
 status='TRIMIS' if e['is_sent'] else 'PRIMIT';title='2026.09.30 '+status+' '+('Revenire Maritczak' if e['is_sent'] else 'Raspuns Stefanie Gruber')
 (P/(title+'.json')).write_text(json.dumps(e,ensure_ascii=False,indent=2),encoding='utf-8')
 header=f"2026.09.30 | {status}\nData tehnica: {e['received_at']}\nDe la: {e['from_address']}\nCatre: {', '.join(e['to'])}\nCC: {', '.join(e['cc']) or '—'}\nSubiect: {e['subject']}\nID Eva-Mail: {e['id']}\nTrunchiat de Eva-Mail: {e['truncated']}\nExport de text; nu este MIME original.\n\n"
 (P/(title+'.txt')).write_text(header+e['text'],encoding='utf-8-sig')
(P/'2026.09.30 Registru anexe.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print('SALVAT',P)
