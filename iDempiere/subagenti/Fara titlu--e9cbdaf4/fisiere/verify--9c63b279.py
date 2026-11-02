import pathlib,json,hashlib,gzip,re,collections
O=pathlib.Path(__file__).parent;E=O.parent;R=E.parent;F=E/'R4';git=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102');blobs=pathlib.Path('D:/CodexWork/A12_evidence_20261102/blobs')
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,default=str),encoding='utf8')
cache={};bincache={};jcache={};counts=collections.Counter();notes=[];issues=[];semantic=[];ev=rd(F/'Dovezi_criterii.json')['evidence']
for eid,v in ev.items():
 if not eid.startswith('EV4-'):continue
 path=v['source'];sh=v['sha_or_oid'];pos=v['pointer'];level=v['level'];key=None
 if re.fullmatch('[0-9a-f]{40}',sh or ''):
  key=sh;kind='git';pt=git/path
  if key not in bincache:
   bz=blobs/(sh+'.gz')
   if bz.is_file():raw=gzip.decompress(bz.read_bytes())
   elif pt.is_file():raw=pt.read_bytes()
   else:issues.append((eid,'no local blob',path,sh));continue
   if hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=sh:issues.append((eid,'bad blob',path));continue
   bincache[key]=raw
  raw=bincache[key]
 else:
  kind='file';ps=pathlib.Path(path); options=[ps]if ps.is_absolute()else[R/ps,E/ps,F/ps,F/'inputs'/ps.name]
  for t in options:
   if not t.is_file():continue
   pk=t.as_posix()
   if pk not in bincache:bincache[pk]=t.read_bytes()
   raw=bincache[pk]
   if hashlib.sha256(raw).hexdigest()==sh:key=pk;break
  if not key:issues.append([eid,'missing_moved',path,sh]);continue
 counts[kind+'_verified']+=1;txt=raw.decode('utf-8-sig',errors='replace')
 try:
  if isinstance(pos,int) or str(pos).isnumeric():
   line=txt.splitlines()[int(pos)-1]; counts['line']+=1
   lit=v['content_or_observation'];lit=lit.get('literal') if isinstance(lit,dict)else lit
   if isinstance(lit,str) and line==lit:counts['literal_line_equal']+=1
  elif str(pos).startswith('/') and path.lower().endswith('.json'):
   if key not in jcache:jcache[key]=json.loads(txt)
   obj=jcache[key]
   for k in pos[1:].split('/'):
    k=k.replace('~1','/').replace('~0','~');obj=obj[int(k)] if isinstance(obj,list)else obj[k]
   counts['json_pointer_valid']+=1
  else:counts['descriptive_anchor']+=1
 except (ValueError,KeyError,TypeError,IndexError):counts['composite_or_invalid_pointer']+=1;notes.append([eid,path,pos])
src=rd(F/'T259_ZK/test_original_versionat.json');dev=rd(F/'T259_ZK/cautare_test_versionat.json')
for role,role_id in [('GardenAdmin',102),('GardenUser',103)]:
 v=rd(F/'T259_ZK'/(role+'.json')); png=F/'T259_ZK'/(role+'_tab.png'); assert h(png)==v['screenshot_sha256'] and v['exact_pairs_equal'];assert len(next(t['rows'] for t in v['visible_tables'] if 'Denumire' in t['headers']))==4;rep={'role':role,'rows':next(t['rows'] for t in v['visible_tables'] if 'Denumire' in t['headers']),'png_sha':h(png),'source':str(v.get('fixture'))[:170]};semantic.append(rep)
seven=rd(F/'probe/T07_03_7_GET.json')['rows'];assert len(seven)==7 and all(z['http']==200 and z['matched_line_count']==0 for z in seven)
manifest=rd(F/'A12_raport.json');inputs={name:(h(F/'inputs'/name)==s)for name,s in manifest['current_input_hashes'].items()};assert all(inputs.values())
out={'EV4_new':sum(k.startswith('EV4-')for k in ev),'computed':dict(counts),'issues':issues,'non_simple_locators':notes,'binary_sources_or_blobs':len(bincache),'frozen_input_hashes':inputs,'T259_two_roles':semantic,'historical_test_files_declared':len(src),'T07_7_GET_literal_count':len(seven),'scope':'Dovezile hash sunt ale fișierelor și ancorelor declarate: nu înlocuiesc testul operațional. Ancorele compuse au fost păstrate distinct.'}
wr(O/'EV4_provenance.json',out);print(out['EV4_new'],counts,len(issues),issues[:2],len(src),len(notes))

