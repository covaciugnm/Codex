from pathlib import Path
import json, urllib.request, hashlib, re, concurrent.futures, shutil, datetime, base64
from email.message import EmailMessage
from email.policy import SMTP
root=Path.cwd(); out=root/'08. Corespondenta/2026.10.29 Capra Baupolizei';out.mkdir(exist_ok=True)
p=json.loads((root/'folder map/2026.10.29 Capra colectare.json').read_text(encoding='utf-8'))
parts={a['id']:a for a in json.loads((root/'folder map/2026.10.29 Capra octeti.json').read_text())}
reuse=json.loads((root/'folder map/2026.10.29 Capra reutilizare.json').read_text(encoding='utf-8'))
def fetch(a):
 d=a['download']; dest=out/'Atasamente'/(a['date'][:10].replace('-','.')+' '+a['id'][:8]+' '+re.sub(r'[<>:"/\\|?*]','_',a['name']))
 dest.parent.mkdir(exist_ok=True)
 if not dest.exists():
  if a['id'] in reuse: shutil.copy2(root/reuse[a['id']],dest)
  else: dest.write_bytes(base64.b64decode(parts[a['id']]['content_base64']))
 assert dest.stat().st_size==d['size'],str(dest)
 return {'id':a['id'],'email_id':a['email_id'],'path':dest.relative_to(root).as_posix(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'size':dest.stat().st_size,'reused_source':reuse.get(a['id']),'verification':'Existing original: unchanged SHA256 versus index, size and initial 65536 bytes versus EVA' if a['id'] in reuse else 'Complete EVA base64'}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: files=list(pool.map(fetch,p['downloads']))
byid={a['id']:a for a in files}
for e in p['emails']:
 date=e['received_at'][:10].replace('-','.');status='TRIMIS' if e.get('is_sent') else 'PRIMIT';stem=date+' '+status+' '+e['id'][:8]
 (out/(stem+'.json')).write_text(json.dumps(e,ensure_ascii=False,indent=2),encoding='utf-8')
 meta='Data lizibila: '+date+'\nStatut in casuta: '+status+'\nID EVA: '+e['id']+'\nExpeditor: '+e.get('from_address','')+'\nDestinatari: '+str(e.get('to',[]))+'\nCC: '+str(e.get('cc',[]))+'\nSubiect: '+e['subject']+'\nTrunchiat API: '+str(e.get('truncated'))+'\n\n'
 (out/(stem+'.txt')).write_text(meta+e.get('text',''),encoding='utf-8')
 m=EmailMessage(policy=SMTP);m['From']=e.get('from_address','');m['To']=', '.join(e.get('to',[]));m['Subject']=e['subject'].replace('\r','').replace('\n',' ');m['X-Eva-ID']=e['id'];m['X-Archive-Note']='Reconstructed export from EVA; see JSON for exact metadata and truncation';m.set_content(e.get('text',''))
 for a in e.get('attachments',[]):
  f=root/byid[a['id']]['path'];mt=(a.get('content_type') or 'application/octet-stream').split('/',1);m.add_attachment(f.read_bytes(),maintype=mt[0],subtype=mt[-1],filename=a['name'])
 (out/(stem+'.eml')).write_bytes(m.as_bytes())
p.pop('downloads');p['attachments_saved']=files
(out/'2026.10.29 Dovezi cautari si acoperire.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'emails':len(p['emails']),'attachments':len(files),'archives':[f['path'] for f in files if f['path'].endswith('.7z')]},ensure_ascii=False))
