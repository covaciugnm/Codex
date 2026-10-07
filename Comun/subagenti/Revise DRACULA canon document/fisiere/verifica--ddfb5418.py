"""Verificări de autor, nu audit independent. Doar rădăcina izolată este permisă."""
from pathlib import Path
import re,json,hashlib,sys,unicodedata,collections,csv
R=Path(r'D:\00. Downloads\Dracula Book\DRACULA-COMICS-CODEX-G0-20260924'); D=Path(__file__).resolve().parent
P=Path(sys.argv[1]) if len(sys.argv)>1 else R/'01_CANON/00_CANON_NUCLEU.md'
assert P.resolve().is_relative_to(R.resolve())
s=P.read_text(encoding='utf-8-sig'); lines=s.splitlines(); results=[]
starts=list(re.finditer(r'^## (\d+)\. ',s,re.M)); sec={int(m[1]):s[m.start():starts[i+1].start() if i+1<len(starts) else len(s)] for i,m in enumerate(starts)}
def table(prefix):
 start=next(i for i,l in enumerate(lines) if l.startswith(prefix)); out=[]
 for l in lines[start+2:]:
  if not l.startswith('|'):break
  out.append([x.strip() for x in l.strip('|').split('|')])
 return out
def check(n,name,ok,detail='',limit=''):
 results.append(dict(code=f'VC{n}',test=name,result='OK' if ok else 'ECHEC',detail=detail,limita=limit))
def norm(t): return ''.join(c for c in unicodedata.normalize('NFD',t.casefold()) if unicodedata.category(c)!='Mn')
badpat=r'contele noptii|val[eé]ri|dra[ck]on|count of the night'
check(1,'Titlu și nume eliminate',not re.search(badpat,norm(s)),limit='Contextul soției este verificat semantic, nu interzis ca șir: negarea și trecutul sunt corecte.')
core=''.join(v for k,v in sec.items() if k not in (16,17,18))
old=['Dragomir','Vlase','a 17-a generație','Marna']
check(2,'Forme vechi normative',not any(w in core for w in old))
check(3,'Diacritice și ghilimele',not any(c in s for c in 'şţŞŢã') and s.count('„')==s.count('”'),[s.count('„'),s.count('”')])
subs=set(re.findall(r'^### (\d+\.\d+) ',s,re.M)); refs=set(re.findall(r'§(\d+(?:\.\d+)?)',s)); missing=refs-{str(k) for k in sec}-subs-{'304','3344.1','5.4','5.5'} # articole juridice ?i subsec?iuni ale jurnalului, marcate ?n context
check(4,'Secțiuni și trimiteri',set(sec)==set(range(1,21)) and not missing,sorted(missing))
check(5,'R1–R10; art. 1–8',len(re.findall(r'^\d+\. \*\*R\d+',sec[6],re.M))==10 and len(table('| Art. | Textul |'))==8)
bad=[]; group=[]
for i,l in enumerate(lines+['']):
 if l.lstrip().startswith('|'):group.append((i+1,l.strip().count('|')))
 elif group:
  bad.extend([(n,c) for n,c in group if c!=group[0][1]]);group=[]
check(6,'Coloane de tabel',not bad,bad)
t5=table('| # | Ani | Oraș |'); t51=table('| # | Ani | Identitățile succesive'); t52=table('| # | Moda epocii')
check(7,'Traseu 24/24/24',[len(t5),len(t51),len(t52)]==[24,24,24])
ident=[]
for row in t51:
 if row[0] in ('1','22'):continue
 intervals=re.findall(r'\((?:decembrie )?(\d{4})–(\d{4})',row[2])
 ages=re.findall(r'(\d+) → (\d+)',row[3])
 for idx,(a,b) in enumerate(intervals):
  x,y=map(int,ages[idx]); duration=int(b)-int(a)
  # Prezentul: tabelul arată vârsta în 2026 și plafonul în 2038.
  if row[0]=='24':y=45
  exception=row[0]=='23' and idx==1
  valid=duration<=25 and x>=21 and y-x==duration and (y<=45 or exception and y<=50)
  valid=valid and (x<=33 if duration<=12 else abs(x-(45-duration))<=1)
  ident.append(dict(popas=int(row[0]),inceput=int(a),sfarsit=int(b),durata=duration,varsta_initiala=x,varsta_finala=y,exceptie=exception,valid=valid))
check(8,'Durata identităților și numărătoare',len(ident)==32 and all(i['durata']<=25 for i in ident),len(ident))
check(9,'Testul anilor: capcane explicite',all(x in sec[5] for x in ['1600–1603','1869','1958–1960','1724–1725']),limit='Verifică interdicțiile; istoria fiecărui obiect rămâne lectură AU-C, nu deducție din simpla prezență a anului.')
cal=re.search(r'Calendarul celor 11 întâlniri:\*\* (.*?)\. Cele zece',s)[1]; years=list(map(int,re.findall(r'\b(?:15|16|17|18|19|20)\d{2}\b',cal)))
check(10,'Calendar armistițiu',years==list(range(1526,2027,50)),years)
m=re.search(r'\*\*Într-o frază .*?\*\* \((\d+) de cuvinte\): \*(.*?)\*',s)
check(11,'Loglinie numărată',bool(m) and int(m[1])==len(m[2].split())<=45,[int(m[1]),len(m[2].split())] if m else [])
check(12,'Data transformării',all(x in s for x in ['26 spre 27 decembrie 1476','4 spre 5 ianuarie 1477']))
check(13,'Fără placeholdere',not re.search(r'\b(TODO|TBD|FIXME|XXX)\b|lorem',s,re.I))
check(14,'Statut prezent',all(x in sec[8] for x in ['din 1794 nu e soția lui','Paris','1794']),limit='Nu transformă mențiunile istorice ale căsătoriei în fals pozitiv.')
check(15,'Hanzer: generații', 'a 14-a generație' in sec[8] and '13 Hanzeri' in sec[8])
check(16,'Pivoturi',all(f'Ep. {i}' in sec[12] for i in (1,5,10,15,20)))
check(17,'Decizie 10', 'Un set-piece de zi' in sec[12] and 'aproximativ de 5 ori' in sec[6])
check(18,'Cele 7 pietre','7 pietre ale zorilor' in sec[6] and 'al șaselea inel' in sec[6])
check(19,'Cod stabil', [r[0] for r in table('| Art. | Textul |')]==[str(n) for n in range(1,9)])
check(20,'R8 și minorii',all(x in sec[6] for x in ['statura','Ilinca (16','Sânziana (~28']))
check(21,'Treziri și cost', all(x in sec[8] for x in ['1462','1794','1916','pierde Zilele Babei din anul următor']) and 'ca în fiecare martie' not in s)
fashion=[(r[0],len(r[1].split(' · '))) for r in t52]
check(22,'Costume: 3 segmente',all(n==3 for _,n in fashion) and all('ochelari' in r[1] or 'lentile' in r[1] for r in t52),fashion, 'Anii garderobei separați de prioritățile istorice; accentele se citesc în tabel.')
rule=re.search(r'Pentru identitățile de peste 12 ani,.*?termenul-limită\.',sec[4])[0]
check(23,'Vârste și regulă identică',all(i['valid'] for i in ident) and rule in sec[19],[i for i in ident if not i['valid']])
badgap=[]
for a,b in zip(ident,ident[1:]):
 if a['popas']==b['popas'] and a['sfarsit']==b['inceput'] and a['popas']!=23:badgap.append(a['popas'])
check(24,'Succesiuni același oraș',not badgap,badgap,'Popasul 23 schimbă orașul; absența de câteva luni este regula normativă pentru anii consecutivi.')
brandbad=[x for x in ['Orient Express','Super Chief','Train Bleu','Golden Eagle'] if x in sec[5]]
check(25,'Vehicule fără mărci reale din lista auditului',not brandbad and 'documentele de lucru' in sec[14],brandbad,'Nu este cercetare exhaustivă de marcă; H1 rămâne deschis.')
prod=(R/'01_CANON/01_DECIZII_PRODUCATOR.md').read_text(encoding='utf-8-sig')
check(26,'Nume blocat și clauză','Ioana Mureșan' in prod and 'Ioana Mureșan' in sec[9] and 'numai prin decizia Producătorului' in sec[14])
patterns=[r'val[eé]ri',r'dra[ck]on',r'taina Nopții',r'Lord Vlad',r'Lord Victor',r'Dracott Jr',r'Bond nu are trecut',r'citește lăcomia',r'reconstruiește averea',r'Opționale, până la 4']
check(27,'Șiruri extinse',not any(re.search(p,s,re.I) for p in patterns),[p for p in patterns if re.search(p,s,re.I)])
check(28,'Însoțitori și excepție',all('Hanzer' in r[-1] for r in t51 if int(r[0]) in range(3,22)) and '1915–1916' in sec[8])
check(29,'Întâlniri Sânziana','Viena, 1815; Iași, 1916–1917; București, 1989' in sec[8] and 'fără să se întâlnească' in t51[15][-1] and 'nu se văd' in t51[16][-1])
ids=list(map(int,re.findall(r'^\| V4-(\d+) \|',sec[16],re.M)))
check(30,'Registru continuu; OBS-8',ids==list(range(1,88)) and 'OBS-8' in sec[16] and all(x in sec[16] for x in ['B-B8','B-B11','C-P15','B-B6']), {'randuri':len(ids)},'Acoperirea integrală jurnal→canon este în matrice; nu declară actualizarea jurnalului altui autor.')
check(31,'15 decizii',len(re.findall(r'^\| \d+ \|',s[:s.index('**Cuprins.')],re.M))==15 and '00_PROCEDURA_PIPELINE_v4.js' in s)
http=D/'stare_url.json'
if http.exists():
 data=json.loads(http.read_text(encoding='utf-8')); problematic=[x for x in data if x['status'] in (404,410) or isinstance(x['status'],int) and x['status']>=500]
 check(32,'Acces URL',not problematic,{'total':len(data),'erori_persistente':len(problematic),'alte_statusuri':dict(collections.Counter(str(x['status']) for x in data))},'403/429/timeout nu confirmă validitatea; listate separat. HTTP 200 nu dovedește afirmația.')
else: results.append(dict(code='VC32',test='Acces URL',result='NEEXECUTAT',detail='Rulați verifica_url.py',limita=''))
quick=s[s.index('## Fișa rapidă'):s.index('## Ghidul de citire')]
check(33,'Buget cuvinte',len(s.split())<=25000 and len(quick.split())<=400,{'total':len(s.split()),'fisa':len(quick.split())})
check(34,'Aparat 28/32 și foileton', '0 sau 4 pagini' in sec[12] and 'Ep. 11 și 16 au 3 tranșe' in sec[12] and 'prima zi lucrătoare' in sec[12])
trains=[r[0] for r in t52 if re.search(r'tren|expresul',r[2]) and any(x in r[2] for x in ['lux','Golden Meridian','Nocturne','Couronne'])]
check(35,'Trenuri glamour',len(trains)>=5 and '14' in trains and '24' in trains,trains)
no_urls=re.sub(r'https?://\S+','',s); no_code=re.sub(r'`[^`]*`','',no_urls)
check(36,'Finisaj tipografic',"'" not in no_code and not re.search(r'\b(roadster|CCTV)\b',no_code),limit='Nu pretinde detectarea automată a tuturor anglicismelor; termenii de lucru au glosar.')
check(37,'Trimiteri echipe','la orice divergență prevalează canonul' in s)
check(38,'Comparabile; R3',all(x in sec[15] for x in ['Lucifer','Besson','2014–2015']) and 'Imunitatea e exclusă' in sec[6])
check(39,'Istoria ochelarilor și existența obiectivelor','nu priorități de invenție' in sec[5] and 'obiectivul trebuie să mai existe atunci' in sec[5],limit='Nu substituie verificarea istorică integrală AU-C.')
check(40,'Paleta zilei',len(re.findall(r'#[A-F0-9]{6}',sec[13].split('**Culorile de zi**')[1].split('**Codul vestimentar')[0]))>=2)
payload={'fisier':str(P),'sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'cuvinte_pe_sectiune':{str(k):len(v.split()) for k,v in sec.items()},'teste':results,'ERORI':[x['code'] for x in results if x['result']=='ECHEC'],'limita':'Autoverificare reproductibilă; fără note independente sau PASS de poartă.'}
(D/'rezultat_verificari.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
(D/'identitati.json').write_text(json.dumps(ident,ensure_ascii=False,indent=2),encoding='utf-8')
(D/'rezultat_verificari.txt').write_text('\n'.join(f"{x['code']} {x['result']} {x['test']}: {x['detail']} {x['limita']}" for x in results),encoding='utf-8')
# Martori de sensibilitate ai căutării, fără a scrie forme eliminate în canon.
assert all(re.search(badpat,norm(x)) for x in ['CONTELE NOPȚII','Valerian','DRACON'])
print(json.dumps({'sha256':payload['sha256'],'ERORI':payload['ERORI'],'status':dict(collections.Counter(x['result'] for x in results))},ensure_ascii=False))
