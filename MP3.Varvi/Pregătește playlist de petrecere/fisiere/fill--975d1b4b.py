import json,pathlib,concurrent.futures,time
P=pathlib.Path(__file__).parent
env={'__file__':str(P.parent/'party_20261008/collect.py')}
exec((P.parent/'party_20261008/collect.py').read_text('utf8').split("rows=[]; cat=''")[0],env)
charts=json.loads((P/'chart_artists.json').read_text('utf8'));rows=json.loads((P/'enriched.json').read_text('utf8'))
artists=['Gary Moore','Joe Cocker','Chris Rea','Eric Clapton','Alannah Myles','Chris Farlowe','Santana','Ricky Martin','Enrique Iglesias','Jennifer Lopez','UB40','Elvis Presley','Chuck Berry','Little Richard','Jerry Lee Lewis','The Beatles','Queen','Scorpions','Bryan Adams','Rod Stewart','Sting','Simply Red','Andy Williams','Engelbert Humperdinck']
tasks=[]
for a in charts:
 if a['artist'] in artists:
  tasks+=sorted(a['songs'],key=lambda s:s['peak'])[:8]
def go(s):
 try:
  d=env['get']('https://api.deezer.com/search',params={'q':'artist:"'+s['artist']+'" track:"'+s['title']+'"','limit':10}).json().get('data',[])
  matches=[r for r in d if env['sim'](r.get('title_short',r['title']),s['title'])>.94 and env['artist_score'](s['artist'],r['artist']['name'])>.9 and not any(x in r['title'].lower() for x in ['live','remix','demo'])]
  if not matches:return None
  m=matches[0]
  if not 100<m['duration']<540:return None
  album=env['get']('https://api.deezer.com/album/'+str(m['album']['id'])).json()
  s.update(title=m.get('title_short',m['title']),album=m['album']['title'],year=int(album.get('release_date','0000')[:4]),seconds=m['duration'],metadata_source=m['link'],youtube='',preferred=False,category=s['default_category'])
  if not s['year']:return None
  return s
 except:return None
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for i,s in enumerate(pool.map(go,tasks)):
  if s:rows.append(s)
  if i%20==0:print(i,len(tasks),flush=True)
seen=set();out=[]
for r in rows:
 k=(r['artist'],env['norm'](r['title']))
 if k in seen:continue
 seen.add(k);out.append(r)
(P/'enriched.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),'utf8')
print('DONE',len(out),flush=True)
