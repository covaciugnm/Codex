import pathlib,json,re,collections,hashlib
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');E=R/'executie';D=E/'R2';src=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102')
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
allcode=[p.relative_to(src).as_posix() for p in src.rglob('*') if p.is_file() and p.suffix in ('.java','.py','.md','.kt','.ts','.js','.sh','.sql')];evid=rd(D/'Dovezi_criterii.json')['evidence'];sha={};textj={};categories=collections.Counter();srcerrors=[];res={}
for eid,v in evid.items():
 path=v['source']; raw=pathlib.Path(path);fp=raw if raw.is_absolute() else src/raw if path.startswith('Documentatie/') else R/raw
 expected=v['sha_or_oid']
 if pathlib.Path(fp).is_file() and re.fullmatch('[0-9a-f]{40}|[0-9a-f]{64}',expected or ''):
  key=fp.as_posix(); sha.setdefault(key,None)
  if not sha[key]:
   b=fp.read_bytes();sha[key]=(hashlib.sha256(b).hexdigest(),hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()); 
  if expected not in sha[key]:
   alt=D/'inputs'/fp.name
   if not alt.exists() or h(alt)!=expected: srcerrors.append([eid,path,expected,sha[key][0]])
  else:categories['file_bytes_match']+=1
  if fp.suffix=='.json' and str(v['pointer']).startswith('/'):
   try:
    if key not in textj:textj[key]=rd(fp)
    node=textj[key]
    for k in v['pointer'][1:].split('/'):
     k=k.replace('~1','/').replace('~0','~');node=node[int(k)] if isinstance(node,list) else node[k]
    categories['concrete_json_pointer_resolved']+=1
   except (ValueError,TypeError,KeyError,IndexError):categories['json_mixed_pointer_requires_review']+=1
 else:categories['historical_or_nonfilesystem_label']+=1
for t in rd(D/'A12_raport.json')['records']:
 if not t['functional_source_unidentified']:continue
 j=rd(D/t['file']);task=j['task'];desc=j['source_literal'].get('raw_descriere','') or '';cand=re.findall(r'[^.!?]*\b(?:se (?:corectează|blochează|adaugă|implementează|verifică|cere|solicită|interzice)|trebuie să)[^.!?]*(?:[.!?]|$)',desc,re.I)
 pat=re.compile(r'(?<![A-Za-z0-9.])'+re.escape(task)+r'(?![0-9.])|(?<=Test)'+re.escape(task)+r'(?![0-9.])',re.I)
 files=[x for x in allcode if pat.search('/'+x)]
 res[task]={'title':t['title'],'normative_phrases_in_descriptions_to_classify':[x.strip() for x in cand],'possible_nominal_artifacts_to_examine':files[:20],'artifacts_matched_total':len(files),'notes':'Recherche nominale sémantique à qualifier, pas un résultat de test.'}
out={'raw_sources':dict(categories),'source_hash_mismatches_or_mutable_paths':srcerrors,'records_awaiting_normative_origin':len(res),'with_description_candidate':sum(bool(x['normative_phrases_in_descriptions_to_classify']) for x in res.values()),'with_nominal_artifact_candidate':sum(bool(x['possible_nominal_artifacts_to_examine']) for x in res.values()),'specific_errors':{'T257':'Descrierea stabilește blocare/corecție repostare, balanță neschimbată; TestT257Repostare.java:33,261–271 și GardaRepostareImport. Originalul proprietarului încă nedeterminat.','T259':'Descrierea stabilește schimbarea Value→Name și test de deschidere; la commitul/linia dosarului activității T158 menționate, plus TestT259Contracte.java:23,30,80. Un checker de bytecode/coloane singur nu este deschidere a ecranului.','T161.01':'Citat comun proprietar conține obiectiv de domeniu «producția cu execuție mai lungă de o lună». Separați porțiunea metodologică de obiectiv și de oracolul propus ulterior; nu inventați efecte la închidere.'},'possible_only':res}
path=pathlib.Path(__file__).parent/'A12_semantic_R2_rechecks.json';path.write_text(json.dumps(out,ensure_ascii=False,indent=2).replace('Recherche nominale sémantique à qualifier, pas un résultat de test.','Indiciu nominal de calificat semantic. Nu reprezintă test executat.'),encoding='utf8');print(h(path),{x:out[x] for x in ('raw_sources','records_awaiting_normative_origin','with_description_candidate','with_nominal_artifact_candidate')},'mismatches',len(srcerrors))

