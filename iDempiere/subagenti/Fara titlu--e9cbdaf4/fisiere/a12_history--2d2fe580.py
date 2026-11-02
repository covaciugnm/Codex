import json,pathlib,hashlib,gzip,collections,re
E=pathlib.Path(__file__).parent.parent;R=E.parent;O=pathlib.Path(__file__).parent; e=json.loads((E/'R2/Dovezi_criterii.json').read_text(encoding='utf8'))['evidence'];blob=pathlib.Path('D:/CodexWork/A12_evidence_20261102/blobs');cache={};stat=collections.Counter();manual=[]
def resolving(root,s):
 for k in s.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');root=root[int(k)] if isinstance(root,list) else root[k]
 return root
for k,v in e.items():
 if not v['source'].startswith('Documentatie/'):continue
 oid=v['sha_or_oid']; assert re.fullmatch('[a-f0-9]{40}',oid)
 if oid not in cache:
  p=blob/(oid+'.gz')
  if p.exists():data=gzip.decompress(p.read_bytes());assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==oid; cache[oid]=data.decode('utf8','replace')
 if oid not in cache:manual.append([k,oid,v['pointer'],'blob indisponibil']);continue
 stat['git_blob_checked']+=1;text=cache[oid];where=v['pointer'];obs=v['content_or_observation']
 try:
  if isinstance(where,int) or str(where).isdigit():n=int(where);assert n>0;actual=text.splitlines()[n-1]
  elif str(where).startswith('/'):actual=resolving(json.loads(text.lstrip('\ufeff')),where)
  elif re.fullmatch(r'(?:L)?\d+\s*[-–:]\s*(?:L)?\d+',str(where)):
   lo,hi=map(int,re.findall(r'\d+',str(where)));actual='\n'.join(text.splitlines()[lo-1:hi])
  else:stat['descriptive_anchor']+=1;continue
  stat['locator_resolves']+=1
  if obs==actual:stat['literal_equal']+=1
  else:stat['observation_projection_or_excerpt']+=1
 except Exception as x:manual.append([k,oid,where,type(x).__name__])
out={'checks':dict(stat),'manual':manual,'counted':sum(x['source'].startswith('Documentatie/') for x in e.values()),'scope':'Blob Git recalculat pentru fiecare referință nominală din Documentatie; o ancoră rezolvată sau un extras imperfect nu înseamnă efect de business. Proiecțiile neidentice se verifică semantic dacă susțin constatarea.'}
(O/'A12_git_R2.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(out['checks'],'manual',len(manual))

