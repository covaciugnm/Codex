from pathlib import Path
import re,urllib.request,urllib.error,json,concurrent.futures,datetime
R=Path(r'D:\00. Downloads\Dracula Book\DRACULA-COMICS-CODEX-G0-20260924'); D=Path(__file__).resolve().parent
s=(R/'01_CANON/00_CANON_NUCLEU.md').read_text(encoding='utf-8')
urls=sorted(set(re.findall(r'https?://[^\s`<>]+',s)))
def get(u):
 attempts=[]
 for n in range(2):
  try:
   req=urllib.request.Request(u,headers={'User-Agent':'CanonReferenceCheck/1.0'})
   with urllib.request.urlopen(req,timeout=8) as response:
    status=response.status; dest=response.url; response.read(1024)
  except urllib.error.HTTPError as e:status=e.code;dest=u
  except Exception as e:status=type(e).__name__;dest=u
  attempts.append(status)
  if isinstance(status,int) and 200<=status<400:break
 return {'url':u,'status':status,'final_url':dest,'incercari':attempts}
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:data=list(pool.map(get,urls))
(D/'stare_url.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(D/'stare_url.txt').write_text('UTC '+datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n'+'\n'.join(f"{x['status']} {x['url']} incercari={x['incercari']}" for x in data),encoding='utf-8')
print('URL:',len(data),'neconfirmate:',sum(x['status']!=200 for x in data))
