import requests,json,math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
BASE=Path(__file__).parent
QUERY={'bool':{'must':[{'term':{'type':'1'}},{'term':{'language':'en'}},{'range':{'deadlineDate':{'gte':'2026-10-01T00:00:00.000+0000'}}}]}}
def page(n):
    r=requests.post('https://api.tech.ec.europa.eu/search-api/prod/rest/search',params={'apiKey':'SEDIA','text':'***','pageSize':100,'pageNumber':n},files={'query':(None,json.dumps(QUERY),'application/json')},timeout=50)
    r.raise_for_status();return r.json()
d=page(1);results=d['results'];total=d['totalResults'];size=d['pageSize']
with ThreadPoolExecutor(max_workers=4) as pool:
    for f in as_completed([pool.submit(page,n) for n in range(2,math.ceil(total/size)+1)]):
        results+=f.result()['results']
unique={x['metadata'].get('identifier',[x['reference']])[0]:x for x in results}
(BASE/'portal_all.json').write_text(json.dumps({'query':QUERY,'totalResults':total,'uniqueResults':len(unique),'results':list(unique.values())},ensure_ascii=False,indent=2),encoding='utf8')
from collections import Counter
print('TOTAL',total,'UNIQUE',len(unique))
print(Counter(k.split('-')[0] for k in unique))
for k,x in unique.items():
    if not k.startswith('HORIZON'): print(k,x['metadata'].get('deadlineDate'),x['metadata'].get('status'))
