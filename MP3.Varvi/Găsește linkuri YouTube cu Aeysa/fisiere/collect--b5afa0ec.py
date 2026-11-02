import urllib.request, re, html, json
from pathlib import Path
out=Path(__file__).parent
records={}
for page in range(1,7):
    url='https://aeysa.com/videos/all/'+('' if page==1 else f'?page={page}')
    raw=urllib.request.urlopen(url,timeout=30).read().decode()
    (out/f'source_{page}.html').write_text(raw,encoding='utf-8')
    for kind,vid,href,body in re.findall(r'<a class="vc-(clip|song)" data-video-id="([\w-]+)" href="([^"]+)"[^>]*>(.*?)</a>',raw,re.S):
        def clean(x): return html.unescape(re.sub('<[^>]+>','',x)).strip()
        title=re.search(r'<h3>(.*?)</h3>' if kind=='clip' else r'<span class="vc-song-name">(.*?)</span>',body,re.S)
        duration=re.search(r'<span class="vc-(?:duration|song-time)">(.*?)</span>',body,re.S)
        date=re.search(r'datetime="([^"]+)"',body)
        name=clean(title[1])
        records[vid]={'id':vid,'title':name,'kind':'Piesă integrală' if kind=='song' else ('Live / radio' if '24/7 LIVE' in name else 'Clip scurt'),'duration':clean(duration[1]) if duration and clean(duration[1])!='Video' else '', 'date':date[1] if date else '', 'url':'https://www.youtube.com/watch?v='+vid,'source':'https://aeysa.com'+html.unescape(href)}
rows=sorted(records.values(),key=lambda r:0 if r['kind']=='Piesă integrală' else 1)
assert len(rows)==76, len(rows)
assert sum(r['kind']=='Piesă integrală' for r in rows)==11
(out/'records.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'AEYSA_linkuri_YouTube.txt').write_text('\n'.join(r['url'] for r in rows)+'\n',encoding='utf-8')
print(json.dumps({'total':len(rows),'categories':{k:sum(r['kind']==k for r in rows) for k in set(r['kind'] for r in rows)}},ensure_ascii=False))
