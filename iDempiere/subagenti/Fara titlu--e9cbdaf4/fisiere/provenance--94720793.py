import pathlib,json,collections,hashlib,datetime,re,decimal
O=pathlib.Path(__file__).parent;E=O.parent;R=E.parent
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf8')
def inventory(z,j,expected):
 p=E/'R2_zone'/z/(z+'_raport.json');assert h(p)==expected;Q=rd(R/'Index_trasabilitate.json');C={x['id']for x in Q['controls'] if x['zone']==z};P={x['id']for x in Q['pipelines'] if x['zone']==z};cids={c.get('control_id')or c['id'] for c in j['controls']};ps={c.get('pipeline_id')or c['id'] for c in j['pipelines']};assert C==cids and P==ps
 evidence=j['evidence_index'].values() if isinstance(j['evidence_index'],dict) else j['evidence_index'];probes=[];issues=[]
 for i in evidence:
  if not isinstance(i,dict):continue
  label=i.get('path')or i.get('file'); sh=i.get('sha256')
  if not (label and sh):continue
  pp=pathlib.Path(label); opts=[pp] if pp.is_absolute()else [E/pp,R/pp,p.parent/pp];hit=next((n for n in opts if n.is_file() and h(n)==sh),None); 
  if not hit:issues.append({'source':label,'expected':sh,'resolved_others':[(x.as_posix(),h(x))for x in opts if x.is_file()]})
  probes.append((label,sh,hit is not None))
 relations=[]; controls=j['controls']
 for f in j['findings']:
  fid=f.get('finding_id')or f['id']; declared=set(f.get('control_ids')or f.get('controls')or [])
  inverse={x.get('control_id')or x['id'] for x in controls if fid in (x.get('findings')or x.get('finding_ids')or [])}
  relations.append({'finding':fid,'declared':sorted(declared),'observed_inverse':sorted(inverse),'declared_but_no_inverse':sorted(declared-inverse),'inverse_not_declared':sorted(inverse-declared)})
 return {'path':p.relative_to(E).as_posix(),'sha256':h(p),'controls':len(C),'pipelines':len(P),'sources_checked':len(probes),'errors':issues,'sources':probes,'rel':relations}
fix={'A02':'c39a7d3eaa3c21c906680e637a2f7172d8d1ec4b85ad31409446b5e37a7bdd1c','A03':'3baf5eb40efef5885ebe3583007466717f222df5b0a0d266846d3459768813c1','A04':'c6735a465847be3f0fd42056cbc85ec7815382aa04f84c91949511a5a110d154'};r={}
for z,sha in fix.items():r[z]=inventory(z,rd(E/'R2_zone'/z/(z+'_raport.json')),sha);print(z,r[z]['sources_checked'],r[z]['errors'],sum(len(x['declared_but_no_inverse']) for x in r[z]['rel']))
wr(O/'zone_integrity.json',r)
saga=rd(E/'Reverificare_SAGA_schema_secundara.json');source=rd(E/'Reverificare_import_factura_SAGA.json');assert saga['source_sha256']==h(E/'Reverificare_import_factura_SAGA.json'); data=saga['observations'];assert set(data[0]['by_schema'])=={'101','200000'} and [list(v['by_schema']) for v in data[1:]]==[['101'],['101']]
v=rd(E/'Reverificare_inchidere_GL_doua_scheme.json');ev=[x for x in v['runs'] if x.get('new_headers')];assert ev
n=rd(E/'R2_zone/A04/native-return.json');assert n['eight_vs_seven']['http']==500 and n['eight_vs_seven']['accepted_line'] is None
zip=rd(O/'a04_zip_recomputed.json');assert [c['http']for c in zip['cases']]==[200,200,200,400];assert [(c['summary'].get('partner')or{}).get('total') for c in zip['cases']][:3]==[2,1,1]
new={'SAGA':{'raw_observations':data,'scope':'L8 preserves accounting rows in 101 and 200000, L12 replaces them with 2 entries in primary scheme, repeated L12 stable. Secondary-scheme admissibility depends on declared accounting policy. Same event in A03-F05 and A04-F06, counted once cross-zone.'},'closing_gl':[{'summary':x['summary'],'new_headers':x['new_headers'],'lines':x['lines']}for x in ev],'A04_return':{'ids':n['ids'],'over8from7':n['eight_vs_seven'],'snapshot_labels':[str(k)for k in n.get('snapshots',{})] if isinstance(n.get('snapshots',{}),dict)else [i.get('stage')for i in n.get('snapshots',[])]},'ZIP_dryrun':[(x['case'],x['http'],(x['summary'].get('partner')or{}).get('total'))for x in zip['cases']]}
wr(O/'cross.json',new)

