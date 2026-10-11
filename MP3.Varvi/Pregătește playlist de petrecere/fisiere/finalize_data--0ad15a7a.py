import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
exec((Path(__file__).parent/'collect.py').read_text('utf8').split("rows=[]; cat=''")[0])
rows=json.loads((ROOT/'tracks.json').read_text('utf8'))
def fix(r):
    if r.get('seconds') and r.get('match_score',0)>=7.4:return r
    candidates=[]
    for q in [r['artist'].split(',')[0]+' '+r['title'],f'track:"{r["title"]}"']:
        time.sleep(.7)
        try:
            response=get('https://api.deezer.com/search',params={'q':q,'limit':20}).json()
            if 'error' in response:
                time.sleep(3); response=get('https://api.deezer.com/search',params={'q':q,'limit':20}).json()
            candidates+=response.get('data',[])
            if candidates and max(score(t,r) for t in candidates)>7.5:break
        except Exception:pass
    if candidates:
        t=max(candidates,key=lambda t:score(t,r))
        if artist_score(r['artist'],t['artist']['name'])>.55 and sim(r['title'],t.get('title_short',t['title']))>.58:
            r.update({'match_score':round(score(t,r),2),'catalog_artist':t['artist']['name'],'catalog_title':t['title'],'album':t['album']['title'],'album_id':t['album']['id'],'seconds':t['duration'],'source':t['link'],'api_source':'https://api.deezer.com/track/'+str(t['id'])})
            time.sleep(.3)
            album=get('https://api.deezer.com/album/'+str(t['album']['id'])).json()
            r['year']=int(album.get('release_date','0000')[:4]); r['album_date']=album.get('release_date','')
    return r
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    out=[]
    for i,r in enumerate(pool.map(fix,rows),1):
        out.append(r)
        if i%50==0:print('Checked',i,flush=True)
rows=out
for r in rows:
    if not r.get('youtube'):
        try:r.update(youtube(r))
        except:pass
(ROOT/'repaired.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),'utf8')
print('MISSING',[(r['id'],r['artist'],r['title']) for r in rows if not r.get('seconds') or not r.get('year')],flush=True)
print('SUSPECT',[(r['id'],r['artist'],r['title'],r.get('catalog_artist'),r.get('catalog_title')) for r in rows if r.get('match_score',0)<7.4],flush=True)
print('VIDEO REVIEW',[(r['id'],r['artist'],r['title'],r.get('video_title')) for r in rows if r.get('video_score',0)<6],flush=True)
print('HOURS',sum(r.get('seconds',r.get('video_seconds',0)) for r in rows)/3600,flush=True)
