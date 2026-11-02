from a12_r3_survey import *
from functools import lru_cache
import gzip,os
R=E/'R5';p=E/'R5_pregatire/Localizatori_EV4.json';assert sha(p)=='1e32892e700caee01abb4cf25f254930f21a13ecee22aaf2343480e73d5d65ea';d=rd(p);old=rd(E/'R4/Dovezi_criterii.json')['evidence'];idx={};bykind=collections.Counter();ex=[]
@lru_cache(maxsize=4096)
def content(src,h):
 if len(h)==40:
  b=gzip.decompress((D/'blobs'/(h+'.gz')).read_bytes());assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==h
 else:
  f=B/src;b=f.read_bytes();assert hashlib.sha256(b).hexdigest()==h,(src,h)
 return b
@lru_cache(maxsize=4096)
def parsed(src,h):return json.loads(content(src,h).decode('utf-8-sig'))
@lru_cache(maxsize=4096)
def lns(src,h):return content(src,h).decode('utf-8-sig',errors='replace').splitlines()
def pointer(node,ptr):
 if ptr=='':return node
 assert ptr.startswith('/'); 
 for bit in ptr.split('/')[1:]:
  field=bit.replace('~1','/').replace('~0','~');node=node[int(field)]if isinstance(node,list)else node[field]
 return node
def canon(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
for r in d['records']:
 i=r['id'];assert old[i]['sha_or_oid']==r['hash'];src=r['source'];h=r['hash'];out=[]
 for z in r['locators']:
  if z['kind']=='json-pointer':
   obj=pointer(parsed(src,h),z['pointer']);assert canon(obj)==z['canonical_value_sha256'],(i,z)
  elif z['kind']=='text-line':
   ll=lns(src,h);assert 1<=z['line']<=len(ll) and hashlib.sha256(ll[z['line']-1].encode()).hexdigest()==z['line_sha256'],(i,z)
  else:raise ValueError(z)
  bykind[z['kind']]+=1;out.append(z)
 assert out;idx[i]={'source':src,'primary_bytes_sha256_or_git_oid':h,'old_human_annotation':r['old_notation'],'confirmed_locators':out}
assert set(idx)=={i for i in old if i.startswith('EV4-')}and len(idx)==1220
wr(R/'probe/locatori_EV4_verificați.json',{'method':'Independently resolved UTF-8 source / actual Git blob by SHA-1 or bytes by SHA-256. Every pointer was decoded RFC6901 and value rehashed as sorted-key compact UTF-8 JSON. Every text line rehashed; human shorthand retained only as an annotation. New R5 claims use strict addresses, without writing in R4.','input_sha256':sha(p),'resolved_ids':len(idx),'locator_instances':dict(bykind),'by_id':idx});print(len(idx),bykind)

