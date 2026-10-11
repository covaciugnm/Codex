import json,pathlib,re,unicodedata,requests,urllib3,concurrent.futures,time
urllib3.disable_warnings()
P=pathlib.Path(__file__).parent
(P/'metadata').mkdir(exist_ok=True)
def norm(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower().replace('&','and'))
old=json.loads((P.parent/'party_20261008/final_tracks.json').read_text('utf8'))
orig={(norm(r['artist']),norm(r['title'])):r for r in old}
artists=json.loads((P/'chart_artists.json').read_text('utf8'))
def process(a):
 songs=a.get('songs',[])
 if not songs:return []
 name=a['artist']; f=P/'metadata'/(norm(name)+'.json')
 try:
  if f.exists():data=json.loads(f.read_text('utf8'))
  else:
   data=requests.get('https://itunes.apple.com/search',params={'term':name,'entity':'song','limit':100,'country':'US'},verify=False,timeout=35).json().get('results',[]);f.write_text(json.dumps(data),'utf8')
 except Exception:return []
 out=[];seen=set()
 for s in songs:
  key=norm(s['title'])
  if key in seen or re.search(r'\{|remix|live|mix\)|medley',s['title'],re.I):continue
  seen.add(key)
  matches=[]
  for r in data:
   artist=norm(r.get('artistName',''));title=r.get('trackName','');base=re.split(r'\s*[([]',title)[0]
   if norm(name)!=artist and norm(name) not in artist:continue
   if norm(base)!=key and norm(title)!=key:continue
   if re.search(r'live|karaoke|tribute|demo|instrumental|re.?record',title+' '+r.get('collectionName',''),re.I):continue
   secs=round(r.get('trackTimeMillis',0)/1000)
   if not 100<secs<540:continue
   score=0
   if 'remix' in title.lower():score-=5
   if 'greatest' in r.get('collectionName','').lower():score-=1
   matches.append((score,r,secs))
  if not matches:continue
  _,m,sec=max(matches,key=lambda z:z[0]);o=orig.get((norm(name),key))
  s.update(title=re.split(r'\s*[([]',m['trackName'])[0],album=m['collectionName'],year=int(m['releaseDate'][:4]),seconds=sec,metadata_source=m['trackViewUrl'],youtube=o.get('youtube','') if o else '',category=o['category'] if o else s['default_category'],preferred=bool(o))
  out.append(s)
 return out
out=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for i,rows in enumerate(pool.map(process,artists)):
  out+=rows
  if i%20==0:print(i,len(out),flush=True)
(P/'enriched.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),'utf8')
print('DONE',len(out),sum(x['seconds'] for x in out)/3600,flush=True)

