import pathlib,json,hashlib,collections
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');E=R/'executie'; here=pathlib.Path(__file__).parent
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
idx=rd(R/'Index_trasabilitate.json');out={}
expected=['da58f0a2cde15dee163c06ff7a61e896fb685bdbafb3358f66d26dc2a089a4f6','4d7ef81968dd14e44803da5f252facc278fa20aedbc8e11a2018eb5ac834dff6','2b01142eeec982c6e75b3b3f43b27100579af4f2edcfa3c7d218be5c21a51bf8','d1950b3eb92043ba76509d85f4ff1b193e52bf474972b091294db870a912d476','40833fecdadb06db25013d28c6f4f6cfa2380e0ce00b138026d0bbeeeb6aa9aa']
for z,sha in zip(['A06','A07','A08','A09','A10'],expected):
 f=E/(z+'_raport.json');j=rd(f);assert h(f)==sha
 att=[];err=[]
 def check(item):
  if isinstance(item,dict):
   if 'sha256' in item:
    path=next((item[k] for k in ('path','file','raw_artifact_path','artifact') if k in item and isinstance(item[k],str)),None)
    if path:
     pp=pathlib.Path(path);options=[pp] if pp.is_absolute() else [R/pp,E/pp,E/z/pp]; hit=next((x for x in options if x.is_file()),None)
     if not hit or h(hit)!=item['sha256']:err.append([path,str(hit) if hit else None,item['sha256'],h(hit) if hit else None])
     att.append(path)
   for v in item.values():check(v)
  elif isinstance(item,list):
   for v in item:check(v)
 check(j['evidence_index']);check(j.get('scripts',[]))
 def idlist(nodes):return [x.get('control_id') or x.get('pipeline_id') or x.get('id') for x in nodes]
 cont=set(idlist(j['controls']));pipes=set([v.get('id') or v.get('pipeline_id') for v in j['pipelines']]);source_c={v['id'] for v in idx['controls'] if v['zone']==z};source_p={v['id'] for v in idx['pipelines'] if v['zone']==z}
 out[z]={'sha256':sha,'controls':len(j['controls']),'pipelines':len(j['pipelines']),'control_ids_missing':sorted(source_c-cont),'control_ids_extra':sorted(cont-source_c),'pipeline_ids_missing':sorted(source_p-pipes),'pipeline_ids_extra':sorted(pipes-source_p),'evidence_hashes_read':len(att),'evidence_hash_errors':err,'states':dict(collections.Counter(x.get('status','?') for x in j['controls'])),'findings':[x['finding_id'] for x in j['findings']],'typed_id_overlap_pipeline_finding':sorted(pipes&set(x['finding_id'] for x in j['findings']))}
(here/'integrity.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(out,ensure_ascii=False))

