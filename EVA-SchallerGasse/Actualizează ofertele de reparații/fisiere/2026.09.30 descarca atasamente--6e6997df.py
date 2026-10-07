from pathlib import Path
import json,urllib.request,hashlib,re,concurrent.futures
ROOT=Path(__file__).resolve().parent.parent
src=ROOT/'folder map'/'2026.09.30 descarcari EVA temporare.json'
entries=json.loads(src.read_text(encoding='utf-8'))
dest=ROOT/'08. Corespondenta'/'BAU-WERTE'/'Atasamente';dest.mkdir(parents=True,exist_ok=True)
def dl(x):
 a=x['attachment'];r=x['result'];r=r[0] if isinstance(r,list) else r
 name=re.sub(r'[<>:"/\\|?*]','_',a['name']);p=Path(name)
 stem=(a['date'][:10].replace('-','.')+' '+a['id'][:8]+' '+p.stem)[:85]
 target=dest/(stem+p.suffix)
 try:
  if not target.exists():
   with urllib.request.urlopen(urllib.request.Request(r['url'],headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as response:b=response.read()
   if len(b)!=a['size']:raise ValueError('size mismatch')
   target.write_bytes(b)
  b=target.read_bytes()
  if len(b)!=a['size']:raise ValueError('size mismatch existing')
  return dict(a,cale=target.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(b).hexdigest(),stare='salvat original integral')
 except Exception as e:return dict(a,stare='eroare',eroare=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:out=list(pool.map(dl,entries))
p=ROOT/'08. Corespondenta'/'BAU-WERTE'/'2026.09.30 Registru atasamente.json'
p.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'fisiere':len(out),'salvate':sum(x['stare']!='eroare' for x in out),'erori':[x for x in out if x['stare']=='eroare']},ensure_ascii=False))
