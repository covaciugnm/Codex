from a03_r8_base import *
from decimal import Decimal as N
import difflib
def bulk(pp):
 request=''.join(sha+':'+p+'\n' for p in pp).encode()
 r=ssh('cd '+repo+' && git cat-file --batch',request,timeout=90);assert r.returncode==0;rbytes=r.stdout;i=0;ans={}
 for p in pp:
  j=rbytes.index(b'\n',i);line=rbytes[i:j].decode();fields=line.split();assert fields[1]=='blob',line; z=int(fields[2]); body=rbytes[j+1:j+1+z];assert H(body) and hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==fields[0];ans[p]=(fields[0],body);i=j+z+2
 assert i==len(rbytes);return ans
def archive():
 q=json.loads((out.parents[2]/'Coada_reverificari_P01.json').read_text(encoding='utf8')); rows=[r for r in q['rows'] if r['category'].startswith('FIX') and r['owner']=='A03']
 extra=['dovezi-04-proba/'+fold+'/'+p for fold in ['A','B'] for p in [fold+'1_2023-06.txt',fold+'2_2023-02.txt',fold+'3_2023-02.txt',fold+'4_nota.txt','izolare_inainte_'+fold+'.txt','izolare_dupa_'+fold+'.txt','pinstance_'+fold+'.txt',fold+'0_2023-02.txt',fold+'0b_2023-02.txt',fold+'0b_nota.txt','baleiaj_'+fold+'.txt','C-18_marcaje_'+fold+'.txt','C-11_text_fereastra.txt','C-7_text_fereastra.txt','start_'+fold+'.txt']]
 extra=[path('T196',p) for p in extra if path('T196',p) in paths]
 selected={};pstart={t:[p for p in paths if '/'+t+'-' in p and p.endswith(('.txt','.tsv','.json'))] for t in set(r['task'] for r in rows)}
 for r in rows:
  t=r['task'];token=r['source']['text'].split(' — ')[0].strip()
  if not re.fullmatch(r'(?:K|C|R)-[\d]+[a-z]?',token):continue
  pat=re.compile(r'(?<![A-Za-z0-9])'+re.escape(token)+r'(?![0-9a-z])',re.I)
  ls=[p for p in pstart[t] if pat.search(p.rsplit('/',1)[-1]) and '/auto-verificare/' in p or pat.search(p.rsplit('/',1)[-1]) and ('/dovezi-' in p and re.search(r'/dovezi-(?:95-proba-p3/varf-1358b7329a|2x-poarta2|66-aud-cod-r1|04-proba|30-proba)/',p) and not re.search(r'incercarea|rulare[123]|/varf-3b',p))]
  def pr(p):return (0 if '66-aud-cod' in p or '95-proba-p3' in p or t=='T256' and '/auto-verificare/' in p else 1,0 if '1bis' in p else 1,len(p))
  if ls:selected[r['criterion']]=sorted(ls,key=pr)[:3]
 allp=sorted(set(sum(selected.values(),[]))|set(extra)); blobs=bulk(allp)
 def ref(p):a,b=blobs[p];return {'path':p,'git_blob_sha1':a,'sha256':H(b),'bytes':len(b),'lines':len(b.splitlines())}
 J(out/'Index_istoric.json',{'utc':UTC(),'sha':sha,'scope':'Obiecte Git verificate prin recalculul hashului de blob și SHA256. Asocierea după numele criteriului indexează documentație, nu este verdict sau rulare nouă a aplicației.','relatii':{k:[ref(p) for p in v] for k,v in selected.items()}})
 def by(p):return blobs[path('T196','dovezi-04-proba/'+p)][1]
 def source(*p):return [ref(path('T196','dovezi-04-proba/'+v)) for v in p]
 outrows=[]
 def pair(id,a,b):
  l=by(a);r=by(b);outrows.append({'criterion':id,'input':source(a,b),'equals_bytes':l==r,'different_lines_context_free':sum(v.startswith(('+','-')) for v in list(difflib.unified_diff(l.decode().splitlines(),r.decode().splitlines()))[2:])});return l
 pair('T196-R2-004','A/A1_2023-06.txt','B/B1_2023-06.txt');s=pair('T196-R2-005','A/A2_2023-02.txt','B/B2_2023-02.txt')
 snap=s.decode().splitlines();outrows[-1]['FISE']=[x for x in snap if x.startswith('FISE|')]
 rows196=[l.split('|') for l in snap]; cats={'SAL_BRUT','CAS','CASS','IMPOZIT','NET','DED_PERS'};cnt=collections.Counter(l[2] for l in rows196 if len(l)>2 and l[0]=='FISA' and l[2] in cats);outrows.append({'criterion':'T196-R2-007','input':source('A/A2_2023-02.txt'),'six_concepts':cnt,'n':sum(cnt.values()),'distinct_employees':len({l[1] for l in rows196 if len(l)>2 and l[0]=='FISA' and l[2] in cats})})
 u=pair('T196-R2-008','A/A3_2023-02.txt','B/B3_2023-02.txt');gettot=lambda b:N(next(l.split('|')[2] for l in b.decode().splitlines() if l.startswith('TOTAL|AJUSTARE_MANUALA_V|')));outrows[-1].update({'total_initial':str(gettot(s)),'total_final':str(gettot(u)),'delta':str(gettot(u)-gettot(s))})
 pair('T196-R2-009','A/A0_2023-02.txt','A/A0b_2023-02.txt')
 a=pair('T196-R2-012','A/A4_nota.txt','B/B4_nota.txt');notes=[l.split('|') for l in a.decode().splitlines()];outrows.append({'criterion':'T196-R2-011','input':source('A/A4_nota.txt'),'header_and_fact':[l for l in notes if l[0] in ('NOTA','FACT')],'sums_independent':[str(sum((N(l[i]) for l in notes if l[0]=='LINIE'),N(0))) for i in (2,3)],'lines':sum(l[0]=='LINIE' for l in notes)})
 for f in ['A','B']:
  pair('T196-R2-015',f+'/izolare_inainte_'+f+'.txt',f+'/izolare_dupa_'+f+'.txt')
 J(out/'T196_recalcul_arhiva.json',{'utc':UTC(),'sha':sha,'scope':'Compararea independentă a instantaneelor originale capturate la rularea declarată de sursă, proces salariați A din UI vs B procesul auxiliar. Linia FACT provine din istoric; aplicația, butoanele și baza nu au fost reexecutate pentru aceste comparații. Am comparat număr și solduri, fără identificatori de persoane. Reproducerea actuală privește comparația din criteriu, nu proveniența nativă la SHA 6df998a.','results':outrows})
if __name__=='__main__':
 import collections
 archive()

