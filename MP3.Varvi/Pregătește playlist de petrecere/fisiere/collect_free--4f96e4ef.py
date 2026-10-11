import requests,json,re,time,pathlib,concurrent.futures,threading,urllib.parse,collections
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ROOT=pathlib.Path(__file__).parent
local=threading.local()
def sess():
 if not hasattr(local,'s'):
  local.s=requests.Session();local.s.verify=False;local.s.headers.update({'User-Agent':'Mozilla/5.0'})
 return local.s
def get(url,**kw):
 r=sess().get(url,timeout=25,**kw);r.raise_for_status();return r
groups={
 'Jazz & lounge':['Jazz','Easy_Listening','Lounge'],
 'Soul & R&B':['Soul-RB'],
 'Disco & funk':['Funk','Disco'],
 'Pop de petrecere':['Pop','Dance'],
 'Balade & acustic':['Singer-Songwriter'],
 'Blues':['Blues'],
 'Rock & pop-rock':['Rock'],
 "Rock'n'roll & retro":['Rockabilly','Surf','Rock_Opera'],
 'Latino & world':['Latin_America','Salsa','Bossa_Nova']}
def listing(task):
 cat,genre=task
 try:
  soup=BeautifulSoup(get('https://freemusicarchive.org/genre/'+genre,params={'pageSize':200,'sort':'_score','d':0}).text,'html.parser')
  rows=[]
  for rank,item in enumerate(soup.select('[data-track-info]')):
   d=json.loads(item['data-track-info']);text=item.get_text(' ',strip=True)
   duration=re.findall(r'\b(\d{1,2}):(\d{2})\b',text)
   if not duration:continue
   sec=int(duration[-1][0])*60+int(duration[-1][1])
   if not 150<=sec<=480:continue
   album=item.select_one('.ptxt-album');genres=item.select_one('.ptxt-genre')
   rows.append(dict(id=d['id'],artist=d['artistName'],title=d['title'],album=album.get_text(' ',strip=True) if album else 'Single',seconds=sec,page=d['url'],download=d['downloadUrl'],category=cat,listing_genre=genre,rank=rank,source='Free Music Archive'))
  print(cat,genre,len(rows),flush=True);return rows
 except Exception as e:print(genre,str(e),flush=True);return []
if __name__=='__main__':
 tasks=[(c,g) for c,gs in groups.items() for g in gs]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: allrows=[r for rs in pool.map(listing,tasks) for r in rs]
 (ROOT/'fma_listings.json').write_text(json.dumps(allrows,ensure_ascii=False,indent=2),'utf8')
 print('TOTAL',len(allrows),flush=True)
