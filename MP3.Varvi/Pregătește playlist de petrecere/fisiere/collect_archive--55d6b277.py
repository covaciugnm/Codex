from collect_free import *
import html
queries={
'Jazz & lounge':'(subject:smoothjazz OR subject:lounge) AND subject:Album',
'Soul & R&B':'(subject:soul OR subject:rnb) AND subject:Album',
'Disco & funk':'(subject:disco OR subject:funk) AND subject:Album',
'Pop de petrecere':'subject:pop AND (subject:upbeat OR subject:happy) AND subject:Album',
'Balade & acustic':'(subject:rockballad OR subject:ballad OR subject:acousticrock) AND (subject:rock OR subject:poprock OR subject:folk) AND subject:Album',
'Blues':'subject:blues AND subject:Album',
'Rock & pop-rock':'(subject:classicrock OR subject:poprock) AND subject:Album',
"Rock'n'roll & retro":'(subject:rockabilly OR subject:rocknroll OR subject:surfrock)',
'Latino & world':'(subject:latin OR subject:bossanova OR subject:salsa OR subject:flamenco) AND subject:Album'}
tasks=[]
for cat,q in queries.items():
 try:
  q='collection:jamendo-albums AND '+q+' AND date:[1990-01-01 TO 2023-12-31]'
  docs=get('https://archive.org/advancedsearch.php',params={'q':q,'output':'json','rows':18,'sort[]':'downloads desc','fl[]':['identifier','title','creator']}).json()['response']['docs']
  tasks.extend((cat,d['identifier']) for d in docs)
 except Exception as e:print(cat,e,flush=True)
(ROOT/'ia_cache').mkdir(exist_ok=True)
def album(task):
 cat,ident=task;f=ROOT/'ia_cache'/(ident+'.json')
 try:
  if f.exists():d=json.loads(f.read_text('utf8'))
  else:
   d=get('https://archive.org/metadata/'+ident).json();f.write_text(json.dumps(d,ensure_ascii=False),'utf8')
  m=d['metadata'];lic=m.get('licenseurl','')
  if 'creativecommons.org/' not in lic:return []
  bad=' '.join(m.get('subject',[])).lower()
  if any(x in bad for x in ['deathmetal','blackmetal','hardcore','noise','drone','children','hiphop','rap ']):return []
  rows=[]
  for t in d.get('files',[]):
   if not t['name'].lower().endswith('.mp3') or not t.get('title') or not t.get('length'):continue
   try:sec=round(float(t['length']))
   except:continue
   if not 150<=sec<=480:continue
   if any(x in t['title'].lower() for x in ['30sec','60sec','loop','logo','trailer','intro','jingle','teaser']):continue
   rows.append(dict(id=ident+'/'+t['name'],artist=t.get('artist',m.get('creator')),title=t['title'],album=t.get('album',m['title']),year=int(m['date'][:4]),seconds=sec,category=cat,genres=', '.join(m.get('subject',[])),page='https://archive.org/details/'+ident,download='https://archive.org/download/'+ident+'/'+urllib.parse.quote(t['name']),source='Jamendo / Internet Archive',license_url=lic,license=lic.split('/licenses/')[-1].strip('/').upper(),access='MP3 direct, fără cont',origin=m.get('source',''),rank=0))
  return rows
 except Exception as e:print(ident,e,flush=True);return []
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:out=[r for rs in pool.map(album,tasks) for r in rs]
(ROOT/'archive_tracks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),'utf8')
print('ARCHIVE',collections.Counter(r['category'] for r in out),flush=True)
# Artist's own Bandcamp pages: free album downloads at a zero minimum price.
romanian=[]
for slug in ['forbidden-drama','a-kind-of-alchemy']:
 url='https://byron.bandcamp.com/album/'+slug
 s=BeautifulSoup(get(url).text,'html.parser');el=s.select_one('[data-tralbum]');d=json.loads(el['data-tralbum'])
 if d['current'].get('minimum_price')!=0:continue
 year=int(re.search(r'\b(\d{4})\b',d['album_release_date']).group(1))
 for t in d['trackinfo']:
  sec=round(t['duration'])
  if not 150<=sec<=480:continue
  romanian.append(dict(id='byron-'+str(t.get('track_id',t['title'])),artist='byron',title=t['title'],album=d['current']['title'],year=year,seconds=sec,category='Românești',genres='Art rock / alternative rock; artist român, versuri în engleză',page='https://byron.bandcamp.com'+t['title_link'],download=url,source='Bandcamp — pagina artistului',license='CC BY-NC-ND 3.0',license_url='https://creativecommons.org/licenses/by-nc-nd/3.0/',access='Album: preț 0; adresă de e-mail cerută',origin=url,rank=0))
(ROOT/'romanian_tracks.json').write_text(json.dumps(romanian,ensure_ascii=False,indent=2),'utf8')
print('ROMANIAN',len(romanian),sum(r['seconds'] for r in romanian)/3600,flush=True)
