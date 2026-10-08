import requests, bs4, json, pathlib, concurrent.futures, re, time
ROOT=pathlib.Path(__file__).parent
BASE='https://www.conexelectronic.ro'
URL=BASE+'/catalog/q/tongou?sort_by=price_desc'
def get(url):
    for pause in [2,5,12,20]:
        r=requests.get(url,timeout=45)
        if r.status_code!=429: break
        time.sleep(pause)
    r.raise_for_status(); return r.text
html=(ROOT/'2026.10.08 catalog-1.html').read_text(encoding='utf-8') if (ROOT/'2026.10.08 catalog-1.html').exists() else get(URL)
(ROOT/'2026.10.08 catalog-1.html').write_text(html,encoding='utf-8')
s=bs4.BeautifulSoup(html,'html.parser')
pages=[URL]+list(dict.fromkeys(a['href'] for a in s.select('a[href]') if re.search(r'/catalog/q/tongou/p\d+',a['href'])))
links=[]
for i,url in enumerate(pages):
    cache=ROOT/f'2026.10.08 catalog-{i+1}.html'
    h=cache.read_text(encoding='utf-8') if cache.exists() else get(url)
    (ROOT/f'2026.10.08 catalog-{i+1}.html').write_text(h,encoding='utf-8')
    soup=bs4.BeautifulSoup(h,'html.parser')
    for script in soup.find_all('script',type='application/ld+json'):
        for obj in json.loads(script.string):
            if obj.get('@type')=='ItemList':
                print('CATALOG',i+1,obj['numberOfItems'],len(obj['itemListElement']))
                links.extend(x['url'] for x in obj['itemListElement'])
links=list(dict.fromkeys(links))
def extract(url):
    cache=next((f for f in ROOT.glob('2026.10.08 produs-*.html') if url in f.read_text(encoding='utf-8')[:15000]),None)
    h=cache.read_text(encoding='utf-8') if cache else get(url)
    soup=bs4.BeautifulSoup(h,'html.parser')
    objs=[]
    for sc in soup.find_all('script',type='application/ld+json'):
        o=json.loads(sc.string); objs.extend(o if isinstance(o,list) else [o])
    p=next(x for x in objs if x.get('@type')=='Product')
    sku=p['sku']; text=soup.h1.parent.get_text('\n',strip=True)+'\n'+ '\n'.join(soup.select_one(sel).get_text('\n',strip=True) for sel in ['#description','#details'] if soup.select_one(sel))
    (ROOT/f'2026.10.08 produs-{sku}.html').write_text(h,encoding='utf-8')
    (ROOT/f'2026.10.08 produs-{sku}.txt').write_text(text,encoding='utf-8')
    print('OK',sku,flush=True)
    return {'sku':sku,'url':url,'structured':p,'text':text,'files':[{'title':a.get_text(' ',strip=True),'url':a['href']} for a in soup.select('a[href]') if '.pdf' in a['href']]}
products=[]
for url in links:
    try: products.append(extract(url))
    except Exception as e: print('ERROR',url,str(e),flush=True)
(ROOT/'2026.10.08 produse-sursa.json').write_text(json.dumps(products,ensure_ascii=False,indent=2),encoding='utf-8')
print('TOTAL',len(products))
for p in products:
    print('\n###',p['sku'],p['structured']['name']); print(p['text'][p['text'].find('Descriere\n'):])
