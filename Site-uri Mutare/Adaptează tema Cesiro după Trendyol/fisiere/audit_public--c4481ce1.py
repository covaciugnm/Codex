import requests, json, pathlib, re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

out=pathlib.Path(__file__).parent/'evidence'; out.mkdir(parents=True,exist_ok=True)
paths={'home':'/','product_cup':'/p/ceasca-cu-farfurioara-220-ml-maro-decorat-cu-flori-si-spic-de-grau','product_set':'/p/set-masa-4-pers-9-piese-cana-roz-200-ml-bol-tava-termorezistenta-portelan-cu-trandafiri-roz','about':'/legal/despre-cesiro','faq':'/legal/intrebari-frecvente','returns':'/legal/politica-de-retur-si-garantie','mystery':'/legal/mistery-box','robots':'/robots.txt','sitemap':'/sitemap.xml'}
report={}
for key,path in paths.items():
    try:
        r=requests.get('https://cesiro.com'+path,timeout=25)
        s=BeautifulSoup(r.text,'html.parser')
        blocks=[]
        for el in s.select('script[type="application/ld+json"], script[type="application/json"]'):
            try:
                data=json.loads(el.string or el.get_text())
                blocks.append({'id':el.get('id'),'type':el.get('type'),'data':data})
            except Exception: pass
        text=s.get_text('\n',strip=True)
        (out/(key+'.txt')).write_text(text,encoding='utf-8')
        record={'url':r.url,'status':r.status_code,'title':s.title.get_text() if s.title else '', 'headings':[x.get_text(' ',strip=True) for x in s.select('h1,h2,h3')], 'meta':[{k:x.get(k) for k in ['name','property','content']} for x in s.select('meta[name],meta[property]')], 'canonical':[(x.get('rel'),x.get('href'),x.get('hreflang')) for x in s.select('link[rel="canonical"],link[rel="alternate"]')], 'json':blocks,'images':len(s.select('img'))}
        report[key]=record
        print(key, r.status_code, len(r.content), 'HEADINGS',record['headings'][:12])
        if key=='home':
            print('JSON',[(b['id'],type(b['data']).__name__,list(b['data'])[:15] if isinstance(b['data'],dict) else len(b['data'])) for b in blocks])
        elif key.startswith('product'):
            start=text.find(record['headings'][0]) if record['headings'] else 0
            print(text[start:start+11000])
        elif key in ['robots','sitemap']: print(text[:1600])
    except Exception as e:
        report[key]={'error':str(e)};print(key,str(e))
(out/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
