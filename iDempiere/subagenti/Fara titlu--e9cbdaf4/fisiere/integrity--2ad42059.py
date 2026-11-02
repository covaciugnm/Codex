import pathlib,json,hashlib,collections
O=pathlib.Path(__file__).parent;E=O.parent;R=E.parent
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cont=rd(R/'Index_trasabilitate.json');result={}
for zone,f,exp in [('A01','R2_zone/A01/A01_raport.json','8eafcf97bf0a56dee6017f2c2f02128a2da884fd7e5b47d70552c4869ea74b40'),('A05','R2_zone/A05_raport.json','fd871b4a22b753ea42d25ecb6935426d4612f76ed05a531d4aa97b9e189f9a26'),('A06','R2_zone/A06/A06_raport.json','a910d1d6d72550dea69d0e6514cb98d954183d28c2328bcc6b895abbdfe48def')]:
 p=E/f;j=rd(p);assert h(p)==exp
 evid=j['evidence_manifest_external'] if zone=='A01' else j['evidence_manifest'] if zone=='A05' else j['evidence_index']
 rows=[]; seen=set(); issues=[]; aliases=[]
 def scan(obj):
  if isinstance(obj,list):
   for item in obj:scan(item)
  elif isinstance(obj,dict):
   if 'sha256' in obj:
    path=next((obj[x] for x in ('path_relative_to_executie','path_relative_to_report','path','file','artifact') if x in obj and isinstance(obj[x],str)),None)
    if not path:return
    options=[p.parent/path,E/path,R/path,E/'R2_zone'/path]
    match=next((x for x in options if x.is_file() and h(x)==obj['sha256']),None)
    if not match:issues.append({'path':str(path),'expected':obj['sha256'],'existing':[[x.as_posix(),h(x)] for x in options if x.is_file()]})
    rows.append({'path':path,'bytes_verified':bool(match),'sha256':obj['sha256']})
   else:
    for v in obj.values():scan(v)
 scan(evid)
 if zone=='A01':scan(j['local_artifacts'])
 rr=set(v['id'] for v in cont['controls'] if v['zone']==zone); rp=set(v['id'] for v in cont['pipelines'] if v['zone']==zone)
 def key(c,t):
  for n in (['control_id','id'] if t=='c' else ['id','pipeline_id']):
   if n in c:return c[n]
 qc=[key(c,'c') for c in j['controls']];qp=[key(c,'p') for c in j['pipelines']]
 stateq=collections.Counter(c.get('status') or c.get('status_R2') or '?' for c in j['controls'])
 result[zone]={'path':f,'report_sha256':h(p),'controls':len(qc),'pipelines':len(qp),'control_missing':sorted(rr-set(qc)),'control_extra':sorted(set(qc)-rr),'pipeline_missing':sorted(rp-set(qp)),'pipeline_extra':sorted(set(qp)-rp),'evidence_hashes':len(rows),'hash_errors':issues,'evidence_checks':rows,'status_counts':dict(stateq),'finding_count':len(j['findings']),'finding_dispositions':{x.get('id') or x.get('finding_id'):x.get('status') for x in j['findings']}}
 print(zone,len(qc),len(qp),len(rows),issues[:2],result[zone]['control_missing'],result[zone]['pipeline_missing'])
(O/'integrity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')

