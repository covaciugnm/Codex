from pathlib import Path
import json,requests,hashlib
import pypdfium2 as pdfium
R=Path.cwd();D=Path(__file__).parent
j=json.loads((D/'2026.10.14 Surse EVA.json').read_text('utf8'));manifest=[]
for i,d in enumerate(j['downloads']):
 name='2026.10.08 Oferta Conex OFR000012370.pdf' if i==0 else '2026.05.22 Oferta istorica Conex OFR000011675.pdf'
 r=requests.get(d['url'],timeout=60);r.raise_for_status();assert r.content.startswith(b'%PDF');assert len(r.content)==d['size'];(D/name).write_bytes(r.content)
 manifest.append({'file':name,'id':d['id'],'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest()})
 doc=pdfium.PdfDocument(D/name);doc[0].render(scale=1.5).to_pil().save(D/('2026.10.14 Control oferta '+str(i+1)+'.png'))
for m in j['emails']:
 date=m['received_at'][:10].replace('-','.')
 name=date+' Email '+m['id'][:8]
 (D/(name+'.json')).write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8')
 header=f"Data: {date}\nSubiect: {m['subject']}\nExpeditor: {m['from_address']}\nDestinatari: {', '.join(m['to'])}\nCC: {', '.join(m['cc'])}\nCont: {m['account_email']}\nID Eva-Mail: {m['id']}\nStatut: PRIMIT (în căsuța consultată)\nEtichete: {m['labels']}\nExport text API; nu este MIME original.\n\n"
 (D/(name+'.txt')).write_text(header+m['text'],encoding='utf8')
(D/'2026.10.14 Manifest atasamente.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(manifest))
