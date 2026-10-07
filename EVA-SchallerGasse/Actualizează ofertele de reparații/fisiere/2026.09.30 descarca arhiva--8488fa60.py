from pathlib import Path
import json,urllib.request,hashlib,re,concurrent.futures,sys
ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'08. Corespondenta'/'2026.09.30 Arhiva Eva-Mail'
rows={}
reg=BASE/'2026.09.30 Registru atasamente.json'
if reg.exists():rows={r['id']:r for r in json.loads(reg.read_text(encoding='utf-8'))}
meta={}; parties={}
ns={'__file__':str(ROOT/'folder map'/'2026.09.30 actualizeaza jurnale.py')}
exec((ROOT/'folder map'/'2026.09.30 actualizeaza jurnale.py').read_text(encoding='utf-8').split('\ndata={}')[0],ns)
for f in sorted((BASE/'Surse').glob('*.json')):
 for e in json.loads(f.read_text(encoding='utf-8')):
  parties[e['id']]=ns['classify'](e)[0]
  for a in e.get('attachments',[]):meta[a['id']]=dict(a,email_id=e['id'],date=e['received_at'])
partners={}
pr=BASE/'2026.09.30 Registru comunicatii.json'
if pr.exists():partners={e['id']:e['partener'] for e in json.loads(pr.read_text(encoding='utf-8'))['comunicatii']}
paths=[Path(x) for x in sys.argv[1:]] or [ROOT/'folder map'/'2026.09.30 descarcari prioritare.json']
urls=[]
for p in paths:urls.extend(json.loads(p.read_text(encoding='utf-8')))
def safe(s,n=60):return re.sub(r'[<>:"/\\|?*\r\n]','_',s)[:n].strip(' .')
def get(r):
 a=meta.get(r['id'],{});date=(a.get('date','2026-09-30')[:10]).replace('-','.')
 party=parties.get(a.get('email_id'),partners.get(a.get('email_id'),'Altele'))
 filename=Path(r['filename']);name=date+' '+r['id'][:8]+' '+safe(filename.stem,52)+filename.suffix
 target=BASE/'Atasamente'/safe(party,35)/name;target.parent.mkdir(parents=True,exist_ok=True)
 previous=rows.get(r['id'],{})
 try:
  if previous.get('cale') and (ROOT/previous['cale']).exists():
   b=(ROOT/previous['cale']).read_bytes();target=ROOT/previous['cale']
  else:
   request=urllib.request.Request(r['url'],headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(request,timeout=90) as response:b=response.read()
   if r.get('size') is not None and len(b)!=r['size']:raise ValueError('Dimensiune diferita fata de Eva-Mail')
   target.write_bytes(b)
  digest=hashlib.sha256(b).hexdigest()
  return {'id':r['id'],'email_id':a.get('email_id'),'data':date,'partener':party,'nume_original':r['filename'],'octeti':len(b),'sha256':digest,'cale':target.relative_to(ROOT).as_posix(),'stare':'salvat original integral'}
 except Exception as ex:return {'id':r['id'],'email_id':a.get('email_id'),'data':date,'partener':party,'nume_original':r['filename'],'stare':'eroare descarcare','eroare':str(ex)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 for result in pool.map(get,urls):rows[result['id']]=result
reg.write_text(json.dumps(list(rows.values()),ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'total':len(rows),'salvate':sum(r['stare']=='salvat original integral' for r in rows.values()),'erori':[r for r in rows.values() if r['stare']!='salvat original integral']},ensure_ascii=False))
