import requests, json, re, unicodedata, time, concurrent.futures, pathlib, threading
from difflib import SequenceMatcher
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ROOT=pathlib.Path(__file__).parent
local=threading.local()
def session():
    if not hasattr(local,'s'):
        local.s=requests.Session(); local.s.verify=False
        local.s.headers.update({'User-Agent':'Mozilla/5.0','Accept-Language':'en-US,en;q=0.9'})
    return local.s
def get(url,**kw):
    for attempt in range(3):
        try:
            r=session().get(url,timeout=30,**kw); r.raise_for_status(); return r
        except Exception:
            if attempt==2: raise
            time.sleep(1+attempt)
def norm(t):
    t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]','',t)
def sim(a,b): return SequenceMatcher(None,norm(a),norm(b)).ratio()
aliases={'Bill Withers':'Grover Washington, Jr.','Bruno Mars':'Mark Ronson','Amy Winehouse':'Mark Ronson','Gloria Estefan':'Miami Sound Machine'}
def artist_score(a,b):
    x,y=norm(a),norm(b)
    if x in y or y in x:return 1
    if norm(aliases.get(a,'NONE')) in y:return 0.96
    return sim(a,b)
def score(t,row):
    title=t.get('title_short',t['title'])
    s=5*sim(row['title'],title)+3*artist_score(row['artist'],t['artist']['name'])+2*sim(row['album_hint'],t['album']['title'])
    alltext=t['title'].lower()
    if any(v in alltext for v in ['karaoke','tribute','sped up','slowed','instrumental version']):s-=12
    if 'live' in alltext and 'live' not in row['album_hint'].lower() and row['title']!='Layla':s-=2
    if 'remix' in alltext:s-=1
    if not 90<=t['duration']<=660:s-=5
    return s
def textval(v):
    if not v:return ''
    return v.get('simpleText','') or ''.join(x.get('text','') for x in v.get('runs',[]))
def walk(obj):
    if isinstance(obj,dict):
        if 'videoRenderer' in obj:yield obj['videoRenderer']
        for v in obj.values():yield from walk(v)
    elif isinstance(obj,list):
        for v in obj:yield from walk(v)
def youtube(row):
    q=row['artist']+' '+row['title']+' official'
    if row['title']=='Layla':q+=' unplugged'
    html=get('https://www.youtube.com/results',params={'search_query':q}).text
    m=re.search(r'(?:var\s+)?ytInitialData\s*=\s*(\{.*?\});',html)
    if not m:return {'youtube_error':'no search data'}
    vids=[]; seen=set()
    for v in walk(json.loads(m.group(1))):
        vid=v.get('videoId')
        if not vid or vid in seen:continue
        seen.add(vid)
        title=textval(v.get('title')); channel=textval(v.get('ownerText')); length=textval(v.get('lengthText'))
        try: secs=sum(int(x)*60**i for i,x in enumerate(reversed(length.split(':'))))
        except:continue
        if secs<70 or secs>900:continue
        n=norm(title); title_n=norm(row['title']); artist_n=norm(row['artist'])
        title_match=title_n in n or sim(row['title'],title)>0.60
        words=[norm(w) for w in re.split(r'[\s,&]+',row['artist']) if len(norm(w))>3]
        artist_match=artist_n in norm(title+' '+channel) or any(w in norm(title+' '+channel) for w in words)
        s=4*title_match+3*artist_match+2*(('official' in title.lower()) or ('topic' in channel.lower()))
        dur=row.get('seconds',0)
        if dur:s+=max(-2,1-abs(secs-dur)/60)
        if any(x in title.lower() for x in ['karaoke','reaction','tutorial','cover by','tribute','sped up','slowed']):s-=8
        if 'live' in title.lower() and 'live' not in row['album_hint'].lower() and row['title']!='Layla':s-=2
        if row['title']=='Layla' and 'unplugged' in title.lower():s+=3
        vids.append({'id':vid,'title':title,'channel':channel,'seconds':secs,'score':round(s,2),'title_match':title_match,'artist_match':artist_match})
        if len(vids)>=15:break
    vids.sort(key=lambda v:-v['score'])
    if not vids:return {'youtube_error':'no videos'}
    best=vids[0]
    return {'youtube':'https://www.youtube.com/watch?v='+best['id'],'video_title':best['title'],'video_channel':best['channel'],'video_seconds':best['seconds'],'video_score':best['score'],'video_candidates':vids[:3]}
def collect(row):
    file=ROOT/'cache'/f"{row['id']:03}.json"
    if file.exists():return json.loads(file.read_text('utf8'))
    try:
        candidates=[]
        artist=row['artist'].split(',')[0]
        queries=[f'artist:"{artist}" track:"{row["title"]}"',row['artist']+' '+row['title']]
        for q in queries:
            data=get('https://api.deezer.com/search',params={'q':q,'limit':25}).json().get('data',[])
            candidates+=data
            if data and max(score(t,row) for t in data)>8:break
        if candidates:
            t=max(candidates,key=lambda t:score(t,row))
            row.update({'match_score':round(score(t,row),2),'catalog_artist':t['artist']['name'],'catalog_title':t['title'],'album':t['album']['title'],'album_id':t['album']['id'],'seconds':t['duration'],'source':t['link'],'api_source':'https://api.deezer.com/track/'+str(t['id'])})
            album=get('https://api.deezer.com/album/'+str(t['album']['id'])).json()
            row['year']=int(album.get('release_date','0000')[:4])
            row['album_date']=album.get('release_date','')
        else:row['metadata_error']='No match'
        row.update(youtube(row))
    except Exception as e:row['error']=str(e)
    file.write_text(json.dumps(row,ensure_ascii=False,indent=2),'utf8')
    return row
rows=[]; cat=''
for line in (ROOT/'selection.txt').read_text('utf8').splitlines():
    if line.startswith('## '):cat=line[3:];continue
    if not line:continue
    a,t,album,year=line.split('|')
    rows.append(dict(id=len(rows)+1,category=cat,artist=a,title=t,album_hint=album,year_hint=int(year)))
(ROOT/'cache').mkdir(exist_ok=True)
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    for i,row in enumerate(pool.map(collect,rows),1):
        results.append(row)
        if i%25==0:print(f'{i}/{len(rows)} collected',flush=True)
results.sort(key=lambda r:r['id'])
(ROOT/'tracks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),'utf8')
print(json.dumps({'tracks':len(results),'hours':sum(r.get('seconds',0) for r in results)/3600,'missing_meta':[r['id'] for r in results if not r.get('seconds')],'missing_youtube':[r['id'] for r in results if not r.get('youtube')],'low_meta':[r['id'] for r in results if r.get('match_score',0)<7.4],'low_video':[r['id'] for r in results if r.get('video_score',0)<8]},ensure_ascii=False),flush=True)
