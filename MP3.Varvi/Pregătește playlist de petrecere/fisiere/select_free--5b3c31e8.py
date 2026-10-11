from collect_free import *
import unicodedata,html
fma=json.loads((ROOT/'fma_details.json').read_text('utf8'))
ia=json.loads((ROOT/'archive_tracks.json').read_text('utf8'))
ro=json.loads((ROOT/'romanian_tracks.json').read_text('utf8'))
def norm(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
def key(r):return norm(r['artist'])+'|'+norm(r['title'].split(' (')[0])
for r in ro:
 r['license']='CC BY-NC-ND 4.0';r['license_url']='https://creativecommons.org/licenses/by-nc-nd/4.0/'
for r in fma:
 if r.get('license_url') and 'creativecommons.org/licenses/' in r['license_url']:
  r['license']='CC '+r['license_url'].split('/licenses/')[1].strip('/').upper().replace('/',' ')
targets={'Jazz & lounge':10800,'Soul & R&B':7200,'Disco & funk':9900,'Pop de petrecere':9900,'Balade & acustic':9000,'Blues':9000,'Rock & pop-rock':9000,"Rock'n'roll & retro":7200,'Latino & world':9000,'Românești':5400}
favorites={'Charles Bradley','Raphael Saadiq','Fitz & The Tantrums','The Immaculates','Choklate','BJ Block & Dawn Pemberton','JC Brooks + The Uptown Sound','Jasmine Jordan','Pierce Murphy','Niki J Crawford','Leo Bowers','Johnny Weltraum','Fhernando','CSC Funk Band','Chicano Batman','Satellite 4','Juanitos','Orgone','Jahzzar','Kevin MacLeod','Café Del Chillia','Jazz Friends','Angus & Friends','Matti Paalanen','Ocean Shiver','Serge Quadrado','Pk jazz Collective','Jazz at Mladost Club','The Vow','Forget the Whale','Emerald Park','The Easton Ellises','Michael Ellis','Roy Smiles','Stefan Kartenberg','Laura Stevenson','Finn Anderson','Bedouine','Rachel Ries','Badly Drawn Boy','Damien Jurado','Mason Jennings','Julie Byrne','T-Model Ford','Mud Dogs',"Nobody's Bizness",'Cullah','Delta Dreambox','The Brothers','DOCTOR BLUES','Kenny Brown','Blind Boy Paxton','Color Out','Phil Twite','Icarus Crash','Big Sandy and His Fly-Rite Boys','The Riptones','Blue Wave Theory','Frankie & the Pool Boys','Daddy Long Legs','Marshall Scott Warner','SONGO 21','Frank Guerrero y Su Grupo Aché','Conjunto Guantanamo','Pistolera','Novalima','Los Amigos Invisibles','Cuban Cowboys','Mundo Armenta','COA','Julioblasco'}
block_artists={'UndErgrOUnd tEchnO - rOAchEs pItchEs - Techno Wizard t__hiroto','Carlos Carty','The Superfools','Cooper-Moore & Assif Tsahar','Loren Connors and Bill Orcutt','No Neck Blues Band','Here Comes A Big Black Cloud!!','Rod','Yeah Music','Fottuto Bianco','Erothug','Artificial Intelligence','Ergo Phizmiz and the Midnight Florists'}
def usable(r):
 if r.get('error') or not r.get('year') or r.get('ai') or r.get('explicit'):return False
 if r['artist'] in block_artists:return False
 if r.get('source')=='Free Music Archive' and not r.get('download_present'):return False
 if r.get('license')=='Condițiile paginii artistului':return False
 if any(t in r['title'].lower() for t in ['fuck','shit','bitch','motherf','underscore','trailer','corpse','funeral','drunk','a cappella']):return False
 bad=r.get('genres','').lower()
 if any(t in bad for t in ['noise','industrial','experimental pop','loud-rock','free-jazz','improv','hardcore','punk','drone','breakcore','dubstep']):return False
 if 'metal' in bad and r['category']!='Balade & acustic':return False
 return True
pool=[r for r in ia+fma+ro if usable(r)]
for r in pool:
 r['selection_score']=(50 if r['artist'] in favorites else 0)+(15 if r['source']=='Jamendo / Internet Archive' else 0)-r.get('rank',0)/20
 if r['artist']=='Manuel de la patagonia' and r['category']!='Latino & world':r['selection_score']-=50
 if r['category']=='Jazz & lounge' and any(t in r['title'].lower() for t in ['blues bomb','groove','funk']):r['selection_score']-=25
 if r['category']=='Balade & acustic' and any(t in r['title'].lower() for t in ['rock','fight','power','war']):r['selection_score']-=25
pool.sort(key=lambda r:-r['selection_score'])
selected=[];seen=set();ac=collections.Counter();cc=collections.Counter();total=0
for cat,target in targets.items():
 secs=0
 for r in pool:
  if r['category']!=cat or key(r) in seen:continue
  limit=25 if cat=='Românești' else 6
  if ac[r['artist']]>=limit or cc[(cat,r['artist'])]>=(25 if cat=='Românești' else 5):continue
  if secs+r['seconds']>target:continue
  selected.append(r);seen.add(key(r));ac[r['artist']]+=1;cc[(cat,r['artist'])]+=1;secs+=r['seconds']
 print(cat,len([r for r in selected if r['category']==cat]),secs/3600,flush=True)
 total+=secs
remaining=86400-total
# Finish the 24-hour duration with whole, unused songs; no cuts or repetitions.
dp={0:[]}
for r in pool:
 if key(r) in seen or r['category']=='Românești' or ac[r['artist']]>=7:continue
 for value,seq in list(dp.items())[::-1]:
  nxt=value+r['seconds']
  if nxt<=remaining and nxt not in dp:dp[nxt]=seq+[r]
 if remaining in dp:break
add=dp.get(remaining,dp[max(dp)])
selected+=add
selected.sort(key=lambda r:(list(targets).index(r['category']),-r['selection_score']))
(ROOT/'selected_unchecked.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2),'utf8')
print('FINAL',len(selected),sum(r['seconds'] for r in selected),collections.Counter(r['source'] for r in selected),flush=True)
def verify(r):
 if r['source']!='Jamendo / Internet Archive':r['checked']='Pagina și oferta de descărcare verificate';return r
 try:
  h=sess().head(r['download'],allow_redirects=True,timeout=20)
  r['http_status']=h.status_code;r['content_type']=h.headers.get('Content-Type','')
  r['checked']='MP3 accesibil (HTTP '+str(h.status_code)+')'
 except Exception as e:r['checked']='Verificare HTTP indisponibilă';r['http_error']=str(e)
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 verified=[]
 for i,r in enumerate(ex.map(verify,selected),1):
  verified.append(r)
  if i%75==0:print('Links',i,flush=True)
(ROOT/'free_tracks.json').write_text(json.dumps(verified,ensure_ascii=False,indent=2),'utf8')
print('HTTP',collections.Counter(r.get('http_status','page') for r in verified),flush=True)
