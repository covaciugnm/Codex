from pathlib import Path
import hashlib,json
E=Path(__file__).resolve().parent.parent;R=E.parent;Z=E/'R3_zone/A08'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rd(p):return json.loads(p.read_bytes())
def ptr(x,key):
 for a in key.strip('#/').split('/'):
  if a:a=a.replace('~1','/').replace('~0','~');x=x[int(a)]if isinstance(x,list)else x[a]
 return x
e=rd(Z/'Erata_F03_R3.json');i=rd(Z/'Manifest_erata_F03_R3.json');base=rd(Z/'A08_raport.json')
for v in e['inputs']+i['inputs']:
 p=R/v['path'];assert h(p)==v['sha256']
for v in e['pointers'].values():
 f,pt=v.split('#');assert ptr(rd(R/f),pt) is not None
for v in e['anchors']:
 p=next(R/z['path']for z in e['inputs']if z['id']==v['input']);l=p.read_text(encoding='utf8').splitlines()[v['line']-1];assert v['text'].strip()in l
cm={x['id']:x for x in i['effective_control_index']};pm={x['id']:x for x in i['effective_pipeline_index']};f={x['id']:x for x in i['reverse_local_finding_index']}
for k,x in f.items():assert set(x['controls'])=={c['id']for c in cm.values()if k in c['findings']};assert set(x['pipelines'])=={p['id']for p in pm.values()if k in p['findings']};assert x['controls'] and x['pipelines']
assert f['A08-F03']['controls']==['A08-C05']and f['A08-F03']['pipelines']==['A08-P03'];assert 'A08-C05'in pm['A08-P03']['controls']and 'A08-P03'in cm['A08-C05']['pipeline_ids']and 'A08-P01'in cm['A08-C05']['pipeline_ids']
assert not i['new_functional_tests'];report={'previous_source_sha':h(Z/'A08_raport.json'),'previous_decision_sha':h(E/'A11_control_A08_R3.json'),'erratum_sha':h(Z/'Erata_F03_R3.json'),'effective_index_sha':h(Z/'Manifest_erata_F03_R3.json'),'verdict':'ACCEPTAT_A08R3-Q1_ÎNCHIS','previous_R3_quality_immutable':6.6,'new_global_score':None,'counts':{'controls':len(cm),'pipelines':len(pm),'local_findings':len(f),'orphan_findings':0,'new_tests':0},'decision':'Subcazul OWN-W-GUEST leagă F03 strict de C05 și P03. Legătura C05–P01 rămâne context. Există hash pentru sursa W, proba anonimă și locatorul. A08R3-Q2 și Q3 rămân deschise.'}
p=E/'A11_control_erata_A08_F03_R3.json';p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(h(p))

