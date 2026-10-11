from collect_free import *
import html
rows=json.loads((ROOT/'fma_listings.json').read_text('utf8'))
bad_words=['a cappella','noise','drone','death','scream','fuck','shit','bitch','gangsta','freestyle','track 6','track 7','podcast','sample pack']
preferred={
 'Jazz & lounge':{'Lounge':0,'Easy_Listening':1,'Jazz':2},
 'Disco & funk':{'Funk':0,'Disco':1},
 'Pop de petrecere':{'Pop':0,'Dance':2},
 "Rock'n'roll & retro":{'Rockabilly':0,'Surf':1,'Rock_Opera':10},
 'Latino & world':{'Salsa':0,'Latin_America':1}}
selected=[];seen=set()
for cat in groups:
 artist_count=collections.Counter();cands=[r for r in rows if r['category']==cat]
 cands.sort(key=lambda r:r['rank']+preferred.get(cat,{}).get(r['listing_genre'],0)*12)
 for r in cands:
  if r['id'] in seen or r['listing_genre']=='Rock_Opera':continue
  if any(w in (r['artist']+' '+r['title']).lower() for w in bad_words):continue
  if artist_count[r['artist']]>=5:continue
  selected.append(r);seen.add(r['id']);artist_count[r['artist']]+=1
  if sum(1 for t in selected if t['category']==cat)>=85:break
(ROOT/'fma_cache').mkdir(exist_ok=True)
def detail(row):
 f=ROOT/'fma_cache'/f"{row['id']}.json"
 if f.exists():return json.loads(f.read_text('utf8'))
 try:
  time.sleep(.12)
  s=BeautifulSoup(get(row['page']).text,'html.parser');txt=s.get_text(' ',strip=True)
  m=re.search(r'Released\s+([A-Za-z]+ \d{1,2}, (\d{4}))',txt)
  row['year']=int(m.group(2)) if m else None
  row['release_date']=m.group(1) if m else None
  license_links=[a for a in s.select('a[href]') if 'creativecommons.org/' in a['href']]
  if license_links:
   a=license_links[0];row['license_url']=a['href'];row['license']=a.get_text(' ',strip=True)
  elif 'FMA_License' in str(s):row['license']='Licență FMA';row['license_url']='https://freemusicarchive.org/FMA_License'
  else:row['license']='Condițiile paginii artistului';row['license_url']=row['page']
  row['genres']=re.search(r'Track info.*?Genres (.*?) Instrumental ',txt).group(1) if re.search(r'Track info.*?Genres (.*?) Instrumental ',txt) else row['listing_genre']
  row['ai']='AI generated? Yes' in txt
  row['explicit']='Explicit Explicit' in txt
  row['download_present']='downloadOverlay' in str(s)
  row['access']='Cont FMA gratuit necesar'
  row['title']=html.unescape(row['title']);row['album']=html.unescape(row['album']);row['artist']=html.unescape(row['artist'])
 except Exception as e:row['error']=str(e)
 f.write_text(json.dumps(row,ensure_ascii=False,indent=2),'utf8');return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 out=[]
 for i,r in enumerate(pool.map(detail,selected),1):
  out.append(r)
  if i%75==0:print('Details',i,'/',len(selected),flush=True)
(ROOT/'fma_details.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),'utf8')
print('COUNTS',collections.Counter(r['category'] for r in out),flush=True)
print('BAD',collections.Counter('error' if r.get('error') else 'no-year' if not r.get('year') else 'AI' if r.get('ai') else 'explicit' if r.get('explicit') else 'ok' for r in out),flush=True)
