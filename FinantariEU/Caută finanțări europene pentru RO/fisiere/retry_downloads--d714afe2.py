import json,time,shutil,hashlib,re
from concurrent.futures import ThreadPoolExecutor,as_completed
from downloads import BASE,BIN,OUT,download,clean
from urllib.parse import urlparse
m=json.loads((BASE/'manifest.json').read_text(encoding='utf8'))
urls={d['url']:d for d in m if not d['ok']}
retry=[u for u,d in urls.items() if '429 ' in d.get('error','') or 'SSL' in d.get('error','')]
print('RETRY',len(retry),flush=True)
results={}
for i,u in enumerate(retry,1):
    res=download(u,retry=True);results[u]=res
    if i%5==0:print('RETRY_PROGRESS',i,'/',len(retry),'OK',sum(x['ok'] for x in results.values()),flush=True)
    if urlparse(u).hostname=='eeagrants.org':time.sleep(1.0)
cat=json.loads((BASE/'catalogue.json').read_text(encoding='utf8'));byid={r['id']:r for r in cat}
for d in m:
    if d['url'] not in results or not results[d['url']]['ok']:continue
    d.update(results[d['url']]);r=byid[d['program']]
    sub='0.ARHIVA' if d['archive'] else '1.DOCUMENTE OFICIALE'
    if any(w in d['label'].lower() for w in ['annex','anexa','form','declaration','declarat','bugetul','budget table']):sub+='/ANEXE'
    targetdir=OUT/r['folder']/sub;targetdir.mkdir(exist_ok=True,parents=True)
    maxlen=max(12,244-len(str(targetdir))-1-len(d['ext'])-9)
    name=clean(re.split(r' Latest version| English Download| Download \(',d['label'])[0],min(60,maxlen))+'_'+d['sha256'][:8]+d['ext']
    target=targetdir/name;shutil.copy2(d['file'],target);d['relative_path']=str(target.relative_to(OUT)).replace('\\','/')
(BASE/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8')
print('RETRY_FINISHED',sum(x['ok'] for x in results.values()),'/',len(retry),flush=True)
