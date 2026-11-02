import pathlib,json,hashlib,collections,decimal,itertools
O=pathlib.Path(__file__).parent;E=O.parent;R=E.parent
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf8')
expected={'A07':'1f65dab4c56d1f1aa3523e8e1e6c879e33ada2182a347ae7a974a29b243d233d','A08':'7b3af4169f25a6b3aee05965c0a7b5904ef645cc452e1042adedb92c04a873ff','A10':'9289e25f8abfa5a72ea9570fa8302ccb9d75192708d73e8b599745483e83481f','A01':'ccdd07ee02778eaa874f6fe276aa41c4f83c831562e33e1c5a4e853eab979026','A03':'dee84c287b3e4f979e24ee49ce3c5b8d0151f78478ae9ffe4e519ca16f421ccb'}
idx=rd(R/'Index_trasabilitate.json');output={}
for z,sha in expected.items():
 rev='R3' if z in ('A01','A03') else 'R2';p=E/(rev+'_zone')/z/(z+'_raport.json');assert h(p)==sha;d=rd(p);rec=[];errors=[]
 def put(name,ef):
  matches=[p.parent/name,E/name,R/name]
  if pathlib.Path(name).is_absolute():matches=[pathlib.Path(name)]
  found=next((v for v in matches if v.is_file() and h(v)==ef),None);rec.append({'file':name,'expected':ef,'verified':bool(found)})
  if not found:errors.append({'file':name,'expected':ef,'found':[(v.as_posix(),h(v)) for v in matches if v.is_file()]})
 def scan(o):
  if isinstance(o,list):
   for v in o:scan(v)
  elif isinstance(o,dict):
   if 'sha256' in o:
    name=next((o.get(k) for k in ('file','path','raw_artifact_path')if o.get(k)),None)
    if name:put(name,o['sha256'])
   else:
    for v in o.values():scan(v)
 if z=='A01':
  for n,ef in [*d['external_manifest'].items(),*d['local_manifest'].items()]:put(n,ef)
 else:scan(d['evidence_index']);scan(d.get('scripts',[]))
 q1={t['id']for t in idx['controls']if t['zone']==z};q2={t['id']for t in idx['pipelines']if t['zone']==z};cs={x.get('control_id')or x.get('id')for x in d['controls']};ps={x.get('pipeline_id')or x.get('id')for x in d['pipelines']};assert cs==q1 and ps==q2
 output[z]={'file':p.relative_to(E).as_posix(),'sha256':h(p),'controls':len(cs),'pipelines':len(ps),'used_file_hashes':len(rec),'errors':errors,'sources':rec}
 print(z,len(rec),'errors',[(x['file'],x['expected'][:9])for x in errors][:5])
 if z=='A10':
  expectedtyped={'PIPE:'+x['pipeline_id']for x in d['pipelines']};fnd={'FIND:'+x['finding_id'] for x in d['findings']}
  assert expectedtyped=={x['typed_id']for x in d['pipelines']} and fnd=={x['typed_id']for x in d['findings']} and not expectedtyped&fnd
 if z=='A03':
  revc=d['revision_consolidated'];task=rd(E/revc['task_index']);assert h(E/revc['task_index'])==revc['task_index_sha256'];nr=ni=0; unresolved=[]; changed=[]
  for t in task['tasks']:
   fr=E/t['file']; assert h(fr)==t['sha256']; recf=rd(fr); br=recf['operative_criteria_and_audit_criteria']+recf['R3_new_criteria']+recf['R4_new_criteria'];k={x['id']for x in br}
   rows=t['source_criteria'];nr+=1;ni+=len(rows)
   for v in rows:
    id=v.get('id')or v.get('criterion'); 
    path,ix=v['pointer'][1:].split('/'); ac=recf[path][int(ix)]; assert ac['id']==id and v['authority_source']==ac['source_evidence_id'] and v['expected']==ac['expected_oracle'] and v['requirement']==ac['normative_content']; if_missing=(id not in k);
    if if_missing:unresolved.append([t['task'],id])
  output[z]['reconciled_task_count']=nr; output[z]['reconciled_criterion_edges']=ni;output[z]['unresolved_crosswalk']=unresolved
 if z=='A01':
  g=rd(p.parent/'write_gate_results.json');pop=g['protected']+g['public'];assert len(g['protected'])==258 and len(g['public'])==5 and len({(r['route'],r['method'])for r in pop})==263 and sum(len(gg['outcomes'])for gg in pop)==1841
  for x in g['protected']:assert [x['outcomes'][u]for u in ['absent','wrong_signature','refresh','expired']]==[401]*4 and [x['outcomes'][u]for u in ['revoked_member','service','valid_member']]==['PASS_TO_DOWNSTREAM']*3
  output[z]['write_gate']={'protected':258,'pub':5,'actor_observations':1841,'limit':'Middleware intercept to downstream sentinel; 258 acceptances to downstream do not mean 258 unauthorized writes.'}
wr(O/'integrity.json',output)
native=rd(E/'Reverificare_retur_concurent_colete.json');assert native['source']['qty']==2 and sum(decimal.Decimal(v[3])for v in native['rma_after'])==4 and sum(decimal.Decimal(v[4])for v in native['rma_after'])==0
r=rd(E/'Reverificare_import_catalog_prin_proxy.json');assert len(r['routed'])==19 and not any(x['target_catalog_changed']for x in r['routed']) and r['control_direct']['target_catalog_changed']
a=rd(E/'Reverificare_crash_PG_ERP.json');assert len({a[x]['native_records']for x in ['crash','retry','second_retry']})==1 and all(a[x]['http']==500 and a[x]['local_mirror']==a[x]['local_idem']==0 for x in ['crash','retry','second_retry']) and a['task_results']==2
wr(O/'cross.json',{'rma_two_CO_qty2':native['rma_after'],'original_shipped':native['source']['qty'],'zero_physically_received':True,'proxy_direct':r['control_direct'],'reachable_staging_hosts_with_mutation':sum(1 for x in r['routed']if x['target_catalog_changed']),'tested_hosts':len(r['routed']),'crash_orphaned_one_native_partner':a['crash'],'replay_twice':[(a[x]['http'],a[x]['local_mirror'],a[x]['local_idem'])for x in ('retry','second_retry')],'worker_results':a['task_results']})

