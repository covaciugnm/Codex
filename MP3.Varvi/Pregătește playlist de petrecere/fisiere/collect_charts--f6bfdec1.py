import requests,json,re,pathlib,threading,concurrent.futures,unicodedata,time
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ROOT=pathlib.Path(__file__).parent
(ROOT/'chart_cache').mkdir(exist_ok=True)
local=threading.local()
def sess():
 if not hasattr(local,'s'):
  local.s=requests.Session();local.s.verify=False;local.s.headers.update({'User-Agent':'Mozilla/5.0'})
 return local.s
def slug(s):
 s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower().replace('&','and')
 s=re.sub(r"['’!.,()/]",'',s);return re.sub(r'[^a-z0-9]+','-',s).strip('-')
def html(url):
 name=slug(url.replace('https://www.officialcharts.com/',''))+'.html';p=ROOT/'chart_cache'/name
 if p.exists():return p.read_text('utf8')
 r=sess().get(url,timeout=22)
 if r.status_code==200:p.write_text(r.text,'utf8');return r.text
 return ''
orig=json.loads(pathlib.Path('D:/MP3.Varvi/outputs/party_20261008/repaired.json').read_text('utf8'))
artists={}
for r in orig:artists.setdefault(r['artist'],[]).append(r)
extra={
'Elton John':('Your Song','Balade rock'),
'Billy Joel':('Uptown Girl','Pop de petrecere'),
'Rod Stewart':('Maggie May','Rock clasic'),
'Phil Collins':('In the Air Tonight','Balade rock'),
'Sting':('Englishman in New York','Jazz & lounge'),
'Simply Red':('Holding Back the Years','Jazz & lounge'),
'Seal':('Kiss from a Rose','Jazz & lounge'),
'George Michael':('Careless Whisper','Jazz & lounge'),
'Luther Vandross':('Never Too Much','Soul & Motown'),
'Diana Ross':('Upside Down','Disco & funk'),
'Barry White':("You're the First the Last My Everything",'Soul & Motown'),
'George Benson':('Give Me the Night','Jazz & lounge'),
'Shirley Bassey':('Diamonds Are Forever','Jazz & lounge'),
'Andy Williams':('Music to Watch Girls By','Jazz & lounge'),
'Dean Martin':('Little Ole Wine Drinker Me','Jazz & lounge'),
'Petula Clark':('Downtown','Rock\'n\'roll & oldies'),
'Engelbert Humperdinck':('Release Me','Jazz & lounge'),
'Gerry Rafferty':('Baker Street','Jazz & lounge'),
'Chris Farlowe':('Out of Time','Blues'),
'Alannah Myles':('Black Velvet','Blues'),
'Robert Palmer':('Addicted to Love','Rock clasic'),
'The Animals':('House of the Rising Sun','Blues'),
'The Kinks':('You Really Got Me','Rock clasic'),
'The Doors':('Light My Fire','Rock clasic'),
'U2':('With or Without You','Rock clasic'),
'INXS':('Need You Tonight','Rock clasic'),
'Duran Duran':('Rio','Pop de petrecere'),
'Depeche Mode':('Enjoy the Silence','Pop de petrecere'),
'Pet Shop Boys':('West End Girls','Pop de petrecere'),
'Bananarama':('Venus','Pop de petrecere'),
'Kylie Minogue':("Can't Get You Out of My Head",'Pop de petrecere'),
'UB40':('Red Red Wine','Latino & internațional'),
'Bob Marley':('Could You Be Loved','Latino & internațional'),
'Shakira':('Whenever Wherever','Latino & internațional'),
'Lou Bega':('Mambo No 5','Latino & internațional'),
'Baccara':('Yes Sir I Can Boogie','Disco & funk'),
'Ottawan':('DISCO','Disco & funk'),
'Black Box':('Ride on Time','Pop de petrecere'),
'Snap':('Rhythm Is a Dancer','Pop de petrecere'),
'Ace of Base':('The Sign','Pop de petrecere'),
'Dr Alban':("It's My Life",'Pop de petrecere')}
for a,(t,c) in extra.items():artists.setdefault(a,[]).append({'title':t,'artist':a,'category':c})
def collect(task):
 artist,candidates=task;records=[];artisturl=None
 for c in candidates[:3]:
  u='https://www.officialcharts.com/songs/'+slug(artist)+'-'+slug(c['title'])+'/'
  try:
   h=html(u)
   if not h:continue
   s=BeautifulSoup(h,'html.parser');a=next((a for a in s.select('a[href]') if a['href'].startswith('/artist/')),None)
   if a:artisturl='https://www.officialcharts.com'+a['href'];break
  except Exception:continue
 if not artisturl:return {'artist':artist,'error':'No artist page','songs':[]}
 try:
  s=BeautifulSoup(html(artisturl),'html.parser');items=s.select('.chart-items')
  if not items:return {'artist':artist,'error':'No chart list','songs':[]}
  for item in items[0].select('.chart-item'):
   a=item.select_one('a[href^="/songs/"]')
   if not a:continue
   text=item.get_text(' ',strip=True);m=re.search(r'Peak:\s*(\d+)',text)
   if not m or int(m.group(1))>20:continue
   title=a.get_text(' ',strip=True)
   if '/' in title or 'CHRISTMAS' in title or 'MEDLEY' in title:continue
   # Dates on the site are rendered as one-character spans.
   before=text.split(title)[0];compact=before.replace(' ','');date=re.search(r'(\d{2})([A-Za-z]{3})(\d{4})',compact)
   year=int(date.group(3)) if date else None
   if year and year>2015:continue
   records.append({'artist':artist,'title':title.title(),'chart_title':title,'chart':'UK Official Singles Chart','peak':int(m.group(1)),'chart_entry':''.join(date.groups()) if date else '', 'chart_year':year,'chart_source':'https://www.officialcharts.com'+a['href'],'artist_source':artisturl,'default_category':candidates[0]['category']})
  return {'artist':artist,'songs':records}
 except Exception as e:return {'artist':artist,'error':str(e),'songs':[]}
if __name__=='__main__':
 out=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for i,r in enumerate(pool.map(collect,artists.items()),1):
   out.append(r)
   if i%20==0:print('Artists',i,'of',len(artists),flush=True)
 (ROOT/'chart_artists.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),'utf8')
 print('SONGS',sum(len(r['songs']) for r in out),flush=True)
 print('FAILED',[r['artist'] for r in out if r.get('error')],flush=True)
