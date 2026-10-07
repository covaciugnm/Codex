import requests, json, re, sys, hashlib
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed
BASE=Path(__file__).parent
CACHE=BASE/'research_cache'; CACHE.mkdir(exist_ok=True)
def fetch(item):
    key,url=item
    out={'key':key,'url':url,'ok':False}
    try:
        r=requests.get(url,timeout=45,headers={'User-Agent':'Mozilla/5.0'}); r.raise_for_status()
        r.encoding='utf-8'
        out.update(ok=True,url_final=r.url)
        (CACHE/(key+'.html')).write_text(r.text,encoding='utf-8')
        s=BeautifulSoup(r.text,'html.parser')
        for e in s(['script','style']): e.decompose()
        body=s.find('main') or s
        out['title']=s.title.get_text(' ',strip=True) if s.title else key
        out['text']=body.get_text('\n',strip=True)
        links=[]; seen=set()
        for a in s.select('a[href]'):
            u=urljoin(r.url,a['href']); label=a.get_text(' ',strip=True)
            if u in seen or not u.startswith('https://'): continue
            seen.add(u)
            ext=re.search(r'\.(pdf|docx?|xlsx?|zip)(?:[?#]|$)',u,re.I)
            if ext or '/document/download/' in u or '/api/files/' in u or 'download' in label.lower():
                context=a.parent.get_text(' ',strip=True)[:600]
                wrapper=a.find_parent(class_='file-wrapper')
                if wrapper: context=wrapper.get_text(' ',strip=True)
                wrapper=a.find_parent(class_='ecl-file')
                if wrapper: context=wrapper.get_text(' ',strip=True)[:600]
                links.append({'url':u,'label':label,'context':context,'ext':ext.group(1).lower() if ext else ''})
        out['documents']=links
        for tag in s.select('eac-download[url]'):
            links.append({'url':urljoin(r.url,tag['url']),'label':tag.get('title',''),'context':tag.get('title','')+' '+tag.get('language',''),'ext':'pdf'})
        out['links']=[{'url':urljoin(r.url,a['href']),'label':a.get_text(' ',strip=True)} for a in s.select('a[href]')]
    except Exception as e: out['error']=str(e)[:250]
    (CACHE/(key+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    return {'key':key,'ok':out['ok'],'documents':len(out.get('documents',[])),'error':out.get('error','')}
if __name__=='__main__':
    sources=json.loads((BASE/sys.argv[1]).read_text(encoding='utf-8'))
    with ThreadPoolExecutor(max_workers=8) as pool:
        for f in as_completed([pool.submit(fetch,i) for i in sources.items()]): print(json.dumps(f.result(),ensure_ascii=True),flush=True)
