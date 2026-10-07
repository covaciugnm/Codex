from pathlib import Path
import json,urllib.request,urllib.error
p=Path(__file__).parent/'2026.09.30 descarcari EVA temporare.json'
r=json.loads(p.read_text(encoding='utf-8'))[0]['result']
try:
    resp=urllib.request.urlopen(urllib.request.Request(r['url'],headers={'User-Agent':'Mozilla/5.0'}),timeout=30)
    print(resp.status,resp.headers.get('Content-Type'))
except urllib.error.HTTPError as e:print(e.code,dict(e.headers),e.read(700).decode(errors='replace'))
