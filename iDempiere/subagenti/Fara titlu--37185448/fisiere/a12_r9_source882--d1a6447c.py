from a12_r9_orig import *
from functools import lru_cache
import hashlib,json
prev=E/'R8_pregatire/Index_883_relectura_surse.json';pr={z['criterion']:z for z in rd(prev)['records']};ev8=rd(R8/'Dovezi_criterii.json')['evidence'];con=rd(E/'A11_control_A06_oracole_postR8.json')['confirmed_delimited_criteria'];mine=['T04.07-R3-001','T04.08-R3-001','T04.09-R3-001','T35.08-R3-001','T35.09-R3-001']
@lru_cache(maxsize=500)
def contents(name,oid):
 if len(oid)==40 and re.fullmatch(r'[0-9a-f]{40}',oid):
  raw=fetch_oid(oid)
  assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==oid
  return raw
 p=Path(name)if Path(name).is_absolute()else B/name
 raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==oid,(name,oid);return raw
@lru_cache(maxsize=250)
def parse(name,oid):return json.loads(contents(name,oid).decode('utf-8-sig'))
def point(x,p):
 # legacy Fisa "finalizate/19/copii/7/" points at a record, not an atom under it
 for t in p.strip('/').split('/')if p.strip('/')else[]:
  x=x[int(t)]if isinstance(x,list)else x[t.replace('~1','/').replace('~0','~')]
 return x
def extract(x,ps):
 if isinstance(ps,int):
  ss=x.decode('utf-8-sig').splitlines()
  if not 1<=ps<=len(ss):raise ValueError('linia depășește blobul')
  return ss[ps-1]
 raise ValueError
def check():
 shape=collections.Counter();new=[]
 for row in no:
  id=row['criterion'];sr=r7map[id]['source_row'];name=sr['source_file'];pr0=sr['source_position'];oid=sr['sha_or_git_blob'];before=pr[id];kind=('git_text'if isinstance(pr0,int)else'git_json'if len(oid)==40 else'manual_json'if Path(name).is_absolute()else'captured_json'if name.startswith('capturi')else'other_json')
  try:
   z=contents(name,oid)
   if isinstance(pr0,int):val=extract(z,pr0)
   else:
    ps=str(pr0);m=re.search(r':line\s*(\d+)$',ps)
    if m:ps=ps[:m.start()]
    val=point(parse(name,oid),ps)
    if m:val=val.splitlines()[int(m[1])-1]
   vs=json.dumps(val,ensure_ascii=False,sort_keys=True,separators=(',',':'));ok='SOURCE_LOCATED';key=list(val)[:9]if isinstance(val,dict)else[];typ=type(val).__name__;digest=hashlib.sha256(vs.encode()).hexdigest();size=len(vs)
  except (FileNotFoundError,ValueError,KeyError,IndexError,TypeError,AssertionError)as e:ok='SOURCE_POINTER_NOT_VERIFIED';key=[];typ=None;digest=None;size=None
  shape[(kind,ok)]+=1
  data={'criterion':id,'canonical':row['canonical'],'owner':row['owner'],'task':row['task'],'primary_source_type':kind,'location':name,'original_pointer':pr0,'file_SHA_or_Git_oid':oid,'value_verified':ok,'object_type':typ,'object_field_names_if_record':key,'value_sha256_canonical_JSON':digest,'value_length':size,'preexisting_search_candidates':len(before.get('local_candidates',[])),'previous_anchor_state':before.get('state'),'status_within_882':'SUBCONDITION_PREVIOUSLY_ACCEPTED_A06'if id in con else'SUBCONDITION_A12_R9'if id in mine else'ANCHOR_ONLY_NO_NEW_VERIFIED_ORACLE','missing_if_not_claimed':'Rândul sau obiectul identificat poate fi descriere, unitate, obligație ori istoric. Un comparator plus ipoteză falsificabilă trebuie stabilite independent înainte de acceptare.'}
  new.append(data)
 f=P9/'Relectura_882_pointeri.json';wr(f,{'utc':now(),'basis':source(prev),'R8_registry':source(R8/'Registru_reexecutare_R8.json'),'all_882':len(new),'readback_stats':[{'kind':k,'result':o,'rows':n}for(k,o),n in shape.items()],'four_A06_five_A12_unique':con+mine,'rows':new,'norm':'Citirea pointerului nu acordă un rezultat de produs. O valoare JSON sau text nu este un etalon de acceptare fără condiții și oracol.'});print(sha(f),shape);print([(z['criterion'],z['original_pointer'])for z in new if z['value_verified']!='SOURCE_LOCATED'][:10])
if __name__=='__main__':check()

