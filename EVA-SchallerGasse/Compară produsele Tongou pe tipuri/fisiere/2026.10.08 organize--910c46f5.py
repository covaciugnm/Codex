from pathlib import Path
from bs4 import BeautifulSoup
import requests,json,hashlib,time,re,shutil,urllib.parse
from pypdf import PdfReader
WORK=Path(__file__).parent
BUILDING=Path('D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)')
DEST=BUILDING/'04. Firme + Executie/08. Ofertanti electrice/Tongou - Conex Electronic/2026.10.08 Catalog comparativ'
links={}; products=[]
for f in WORK.glob('2026.10.08 produs-*.html'):
    soup=BeautifulSoup(f.read_text(encoding='utf-8'),'html.parser')
    sku=f.stem.split('-')[-1]
    shutil.copy2(f,DEST/'Surse web'/f.name)
    desc=soup.select_one('#description')
    detail=soup.select_one('#details')
    text=soup.h1.parent.get_text('\n',strip=True)+'\n'+ '\n'.join(x.get_text('\n',strip=True) for x in [desc,detail] if x)
    (DEST/'Surse web'/f'2026.10.08 produs-{sku}.txt').write_text(text,encoding='utf-8')
    objs=[]
    for sc in soup.find_all('script',type='application/ld+json'):
        obj=json.loads(sc.string);objs.extend(obj if isinstance(obj,list) else [obj])
    p=next(x for x in objs if x.get('@type')=='Product')
    files=[]
    container=soup.select_one('#associated-files')
    for a in container.select('a[href]') if container else []:
        url=a['href'];files.append(url)
        links.setdefault(url,{'url':url,'title':a.get_text(' ',strip=True),'skus':[]})['skus'].append(sku)
    stock=soup.select_one('.product-summary__info--stock .info-value')
    qty=int(stock.get_text(strip=True)) if stock and stock.get_text(strip=True).isdigit() else None
    if 'OutOfStock' in p.get('offers',{}).get('availability',''):qty=0
    products.append({'sku':sku,'url':soup.find('link',rel='canonical')['href'],'structured':p,'text':text,'description':desc.get_text('\n',strip=True) if desc else '', 'detail':detail.get_text('\n',strip=True) if detail else '', 'files':files,'stock_qty':qty,'stock_source':'Pagina produsului, câmp Stoc' if stock else 'Disponibilitate declarată în pagina produsului'})
for f in WORK.glob('2026.10.08 catalog-*.html'):shutil.copy2(f,DEST/'Surse web'/f.name)
for i,(url,item) in enumerate(links.items(),1):
    filename='2026.10.08 '+urllib.parse.unquote(url.rsplit('/',1)[-1])
    filename=re.sub(r'[<>:"/\\|?*]','-',filename)
    path=DEST/'Datasheet si manuale'/filename
    item['path']=str(path.relative_to(DEST));item['original_filename']=url.rsplit('/',1)[-1]
    try:
        if not path.exists():
            for wait in [2,5,12,20]:
                resp=requests.get(url,timeout=45)
                if resp.status_code!=429:break
                time.sleep(wait)
            resp.raise_for_status()
            if not resp.content.startswith(b'%PDF'):raise ValueError('Nu este PDF')
            path.write_bytes(resp.content)
        item['sha256']=hashlib.sha256(path.read_bytes()).hexdigest();item['bytes']=path.stat().st_size
        pdf=PdfReader(path);item['pages']=len(pdf.pages);item['status']='DESCARCAT'
        (DEST/'Date structurate'/(path.stem+'.txt')).write_text('\n'.join(f'PAGINA {n+1}\n{p.extract_text()}' for n,p in enumerate(pdf.pages)),encoding='utf-8')
        print('MANUAL',filename,item['pages'],item['skus'],flush=True)
    except Exception as e:item['status']='EROARE';item['error']=str(e);print('ERROR',url,str(e),flush=True)
(DEST/'Date structurate'/'2026.10.08 registru manuale.json').write_text(json.dumps(list(links.values()),ensure_ascii=False,indent=2),encoding='utf-8')
(DEST/'Date structurate'/'2026.10.08 produse-sursa.json').write_text(json.dumps(products,ensure_ascii=False,indent=2),encoding='utf-8')
print('PRODUSE',len(products),'MANUALE',len(links))
