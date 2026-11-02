import json,hashlib,pathlib,re,collections,gzip,datetime
O=pathlib.Path(__file__).parent; E=O.parent; R=E.parent; F=E/'R3'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ev=rd(F/'Dovezi_criterii.json')['evidence'];blob=pathlib.Path('D:/CodexWork/A12_evidence_20261102/blobs');code=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102');jsoncache={};files={};stats=collections.Counter();issues=[];samples={};checks=[]
def pointer(node,loc):
 for x in loc[1:].split('/'):
  x=x.replace('~1','/').replace('~0','~')
  node=node[int(x)] if isinstance(node,list) else node[x]
 return node
for id,v in ev.items():
 if not id.startswith('EV3-'):continue
 source=v['source'];rawid=v['sha_or_oid'];pos=v['pointer'];p=pathlib.Path(source);mode='';content=None
 if re.fullmatch('[0-9a-f]{40}',rawid or ''):
  if rawid not in files:
   local=blob/(rawid+'.gz');fp=code/p
   if local.exists():data=gzip.decompress(local.read_bytes())
   elif fp.is_file():data=fp.read_bytes()
   else:issues.append((id,'NO_BLOB',source,rawid));continue
   digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();files[rawid]=(digest,data)
  digest,content=files[rawid];mode='git'
 elif re.fullmatch('[0-9a-f]{64}',rawid or ''):
  options=[p] if p.is_absolute() else [R/p,E/p,F/p,code/p,F/'inputs'/p.name,E/'R2/inputs'/p.name]
  checked=[]
  for path in options:
   pk=path.as_posix()
   if path.is_file():
    if pk not in files: raw=path.read_bytes();files[pk]=(hashlib.sha256(raw).hexdigest(),raw)
    dg,dt=files[pk];checked.append((str(path),dg))
    if dg==rawid:digest,content=dg,dt;break
  if content is None:issues.append((id,'NO_EXACT_FILE',source,rawid,checked));continue
  mode='file'
 else:issues.append((id,'NO_FINGERPRINT',source,rawid));continue
 if digest!=rawid:issues.append((id,'DIGEST_MISMATCH',source,digest,rawid));continue
 stats[mode+'_hash_ok']+=1
 text=content.decode('utf-8-sig','replace')
 try:
  if isinstance(pos,int) or str(pos).isnumeric():
   n=int(pos);assert n>0; text.splitlines()[n-1]; label='line'
  elif str(pos).startswith('/') and p.suffix.lower()=='.json':
   if rawid not in jsoncache:jsoncache[rawid]=json.loads(text)
   pointer(jsoncache[rawid],pos);label='json_pointer'
  elif re.fullmatch(r'L?\d+\s*[-–]\s*L?\d+',str(pos)):
   n,m=map(int,re.findall(r'\d+',str(pos)));assert 0<n<=m<=len(text.splitlines());label='line_range'
  else:label='method_locator'
  stats[label]+=1
 except (LookupError,TypeError,ValueError,AssertionError) as err:stats['composite_or_unresolved_locator']+=1;samples.setdefault(str(pos),[id,source,str(pos)])
 checks.append({'id':id,'sha_ok':True,'source':source})
out={'sha_r3':h(F/'A12_raport.json'),'EV3_examined':sum(k.startswith('EV3-') for k in ev),'num_real_files_or_oids':len(files),'stats':dict(stats),'source_issues':issues,'not_plain_locator_examples':list(samples.values()),'scope':'Pour les ancres composites, le hash certifie le fichier et non la véracité de l’oracle. EV2 a déjà été audité dans A11 R2; la comparaison individuelle R2/R3 est menée séparément.'}
out['scope']='Pentru ancore compuse, hashul confirmă fișierul, nu rezultatul pretins. EV2 a fost verificat în A11 R2; comparația individuală R2/R3 este separată.'
(O/'A11_provenienta_EV3.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(out['EV3_examined'],out['stats'],len(issues),issues[:2])

