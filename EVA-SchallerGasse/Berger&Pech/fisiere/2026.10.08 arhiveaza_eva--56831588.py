from pathlib import Path
import json,re,hashlib,urllib.request,urllib.parse,concurrent.futures,datetime
from email.message import EmailMessage
from email.utils import format_datetime

ROOT=Path(__file__).resolve().parent.parent
TMP=Path('C:/Users/User/.codex/visualizations/2026/10/01/01a0f6eb-c105-7760-973e-241d6f6be8c1/2026.10.08 Eva manifest temporar.json')
M=json.loads(TMP.read_text(encoding='utf-8'))
OUT=ROOT/'08. Corespondenta'/'2026.10.08 Verificare zilnica'
OUT.mkdir(exist_ok=True)
PARTNERS={'64ef7967-215d-409a-863a-92d07e05bb2b':'Weigl','871127cd-1d04-4cae-866e-d666b76fd868':'Schmitt + Sohn','7297d88d-378c-4d49-95f0-12838396fbdd':'SCHAUERLEUTE','ff7cdedf-319b-4bf2-abba-ebd235dfbfa0':'Fuglister','97799dc8-4942-4fd9-9142-003a0954f058':'STURM'}
def safe(s):return re.sub(r'[<>:"/\\|?*\x00-\x1f]',' ',s).strip().rstrip('. ')
def unpack(r):
    if r.get('structuredContent') is not None:return r['structuredContent']
    for c in r.get('content',[]):
        if c.get('type')=='text':
            try:return json.loads(c['text'])
            except ValueError:pass
    return r
registry=json.loads((ROOT/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.07 Registru comunicatii.json').read_text(encoding='utf-8-sig'))
old_ids={e['id'] for e in registry['comunicatii']}
for e in M['emails']:
    d=e['data']; base='2026.10.08 PRIMIT '+PARTNERS[e['id']]+' '+e['id'][:8]
    (OUT/(base+'.json')).write_text(json.dumps({'data_lizibila_verificare':'2026.10.08','statut':'PRIMIT','email_original_api':d,'raspuns_tehnic':e['raw']},ensure_ascii=False,indent=2),encoding='utf-8')
    original=d.get('text') or ''
    metadata='\n'.join(['2026.10.08 | Export Eva-Mail','Statut: PRIMIT','Data originală: '+str(d.get('received_at')),'Expeditor: '+d.get('from_address',''),'Destinatari: '+', '.join(d.get('to',[])),'CC: '+', '.join(d.get('cc',[])),'Subiect: '+d.get('subject',''),'ID Eva-Mail: '+e['id'],'Corp trunchiat de API: '+str(d.get('truncated',False)),'Export API text; nu copie MIME integrală.','\nTEXT ORIGINAL\n'])
    (OUT/(base+'.txt')).write_text(metadata+original,encoding='utf-8')
    em=EmailMessage();em['From']=d.get('from_address','');em['To']=', '.join(d.get('to',[]))
    if d.get('cc'):em['Cc']=', '.join(d['cc'])
    em['Subject']=d.get('subject','').replace('\r','').replace('\n',' ')
    em['Date']=format_datetime(datetime.datetime.fromisoformat(d['received_at'].replace('Z','+00:00')))
    em['X-Eva-Mail-ID']=e['id'];em['X-Eva-Export']='API reconstructed text; not original MIME'
    em.set_content(original)
    (OUT/(base+'.eml')).write_bytes(em.as_bytes())
    for a in d.get('attachments',[]):
        if a.get('text') is not None:
            (OUT/('2026.10.08 Extras API '+a['id'][:8]+' '+safe(a['name'])+'.txt')).write_text(a['text'],encoding='utf-8')
proof={'data_lizibila':'2026.10.08','mailboxes':M['mailboxes'],'cautari':M['searches'],'comparatie_iduri':[{'id':e['id'],'deja_arhivat':e['id'] in old_ids} for e in M['emails']], 'nota':'Toate rezultatele au fost preluate; fiecare total este sub limita paginii de 50. Nu s-au trimis mesaje.'}
(OUT/'2026.10.08 Dovezi cautari si sincronizare.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf-8')
def download(a):
    d=a['data'];url=d.get('url','')
    if urllib.parse.urlsplit(url).hostname!='api.eva-org.com':return {'id':a['id'],'stare':'eroare host'}
    name=safe(d.get('filename') or a['name']);path=OUT/('2026.10.08 ORIGINAL '+a['id'][:8]+' '+name)
    try:
        if path.exists() and path.stat().st_size==int(d.get('size') or a['size']):data=path.read_bytes()
        else:
            request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(request,timeout=90) as response:data=response.read()
            if len(data)!=int(d.get('size') or a['size']):raise ValueError('size')
            path.write_bytes(data)
        return {'id':a['id'],'email_id':a['email_id'],'data':'2026.10.08','partener':PARTNERS[a['email_id']],'nume_original':name,'octeti':len(data),'sha256':hashlib.sha256(data).hexdigest(),'cale':path.relative_to(ROOT).as_posix(),'stare':'salvat original integral'}
    except Exception as ex:return {'id':a['id'],'email_id':a['email_id'],'nume_original':name,'stare':'eroare descarcare '+type(ex).__name__}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(download,M['downloads']))
(OUT/'2026.10.08 Registru descarcari.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'mesaje':len(M['emails']),'noi':sum(e['id'] not in old_ids for e in M['emails']),'originale_salvate':sum(r['stare']=='salvat original integral' for r in results),'descarcari':results},ensure_ascii=False))
