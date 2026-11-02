import pathlib,json,hashlib,gzip,re,collections,datetime
O=pathlib.Path(__file__).parent;E=O.parent;F=E/'R5';R=E.parent;git=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102');cache=pathlib.Path('D:/CodexWork/A12_evidence_20261102/blobs')
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ptr(x,key):
 if not key:return x
 assert key.startswith('/')
 for t in key[1:].split('/'):
  t=t.replace('~1','/').replace('~0','~');x=x[int(t)] if isinstance(x,list)else x[t]
 return x
old=rd(E/'R4/Dovezi_criterii.json')['evidence'];c=rd(F/'Dovezi_criterii.json')['evidence'];datas={};jsons={};n=collections.Counter();issues=[]
for id,v in c.items():
 if id.startswith('EV4-'):
  assert v['source']==old[id]['source'] and v['sha_or_oid']==old[id]['sha_or_oid'] and v['content_or_observation']==old[id]['content_or_observation']
 elif not id.startswith('EV5-'):continue
 path=v['source'];sha=v['sha_or_oid'];k=sha
 if sha not in datas:
  if len(sha)==40:
   p=cache/(sha+'.gz');raw=gzip.decompress(p.read_bytes()) if p.is_file() else (git/path).read_bytes()
   dg=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
  else:
   ps=pathlib.Path(path);opts=[ps]if ps.is_absolute()else[R/ps,E/ps,F/ps,F/'inputs'/ps.name];p=next((x for x in opts if x.is_file() and h(x)==sha),None)
   if not p:issues.append([id,'NoHash',path,sha]);continue
   raw=p.read_bytes();dg=hashlib.sha256(raw).hexdigest()
  assert dg==sha;datas[k]=raw
 raw=datas[k];ls=v['strict_primary_locators'];assert ls;grp=id[:3];n[(grp,'evidence')]+=1
 for l in ls:
  if l['kind']=='json-pointer':
   if k not in jsons:jsons[k]=json.loads(raw.decode('utf-8-sig'))
   value=ptr(jsons[k],l['pointer']);assert canonical(value)==l['canonical_value_sha256'],(id,l['pointer'])
  else:
   assert l['kind']=='text-line';line=raw.decode('utf-8-sig',errors='replace').splitlines()[l['line']-1];assert hashlib.sha256(line.encode()).hexdigest()==l['line_sha256'],(id,l['line'])
  n[(grp,l['kind'])]+=1
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'counts':{'|'.join(k):v for k,v in n.items()},'issues':issues,'unique_files_or_blobs':len(datas),'remark':'Rezolvate la valoarea JSON canonică sau la octeții liniei text. Origini R4 păstrate. Validitatea locatorului nu confirmă singură implementarea sau rezultatul comercial.'};(O/'strict_reproduced.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(out)

