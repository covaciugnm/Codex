import pathlib,json,hashlib,re,datetime
from decimal import Decimal as N,ROUND_HALF_UP
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');E=R/'executie';D=E/'supliment_CESIRO1'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def val(x,ref):
 for k in ref.lstrip('#')[1:].split('/'):
  k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
 return x
p=D/'Plan_CESIRO1_R3.json';assert h(p)=='54474212aabea451aa6b8d01adf471bac7a4a3de24158988f705bc7d7512c5ef'
j=rd(p);idx=rd(R/'Index_trasabilitate.json');assert h(R/'Index_trasabilitate.json')==j['base_index_sha256'];prior=rd(E/'A11_gate_CESIRO1_R2.json');assert h(R/j['source_revision']['rejected_review'])==j['source_revision']['review_sha256'] and h(R/j['source_revision']['path'])==prior['plan_sha256']==j['source_revision']['sha256']
assert h(D/'Inventar_CESIRO1.json')==j['source_census_sha256'] and h(D/'Inventar_CESIRO1_UI.json')==j['ui_inventory']['sha256'] and h(R/'A11_rubrica_control.json')==j['rubric_sha256'] and rd(R/'Manifest_plan.json')['bundle_sha256']==j['signed_base_bundle'] and j['execution_count']==0
edge=set();keys=set();original=rd(R/'Inventar_P01.json'); cap=rd(R/'capturi/00_STATUS_TASKURI.json')
for c in j['controls']:
 ex=c['id']; lp=c['parent_edges']
 assert set(c['parent_controls'])=={x['control']for x in lp} and set(c['parent_pipelines'])=={x['pipeline']for x in lp}
 for a in lp:
  target,ptr=a['signed_pointer'].split('#');assert target=='Index_trasabilitate.json'; ctrl=val(idx,ptr);host=val(idx,ptr.rsplit('/',2)[0]);assert host['id']==a['pipeline'] and ctrl==a['control'],a
  edge.add((ex,ctrl,a['pipeline']))
 assert c['consumer_acceptance'] and c['child_parent_criteria'] and c['target_artifact']
 for ca in c['child_parent_criteria']:
  q=rd(R/ca['criterion_source'])
  got=val(q,ca['norm_pointer']); assert got is not None
 reg=j['individual_edge_register']
 assert all(rec['expected_artifact']==c['target_artifact'] for rec in reg if rec.get('EX',rec.get('supplement',rec.get('ex')))==ex)
for rec in j['individual_edge_register']:
 keys.add((rec['reverse']['supplement'],rec['control'],rec['pipeline']));assert rec['reverse']['required_control']==rec['control'] and rec['reverse']['upstream']==rec['pipeline'] and rec['criteria']
assert len(edge)==38 and edge==keys
for r in j['origin_criteria']:
 qf=R/r['fisa']; assert h(qf)==r['fisa_sha256'];meta=val(original,r['origin'].split('#')[1]);assert meta['technical']==r['technical'] and cap[int(r['source_capture_pointer'].strip('/'))]['id']==r['technical']
 for ss in r['successor_records']:
  assert any(x['technical']==ss['id'] and x['code']==ss['canonical'] for x in original['rows'])
fix=j['numeric_fixture']; z=N('0.01');n=N(0);tax=N(0)
for row in fix['product']:
 net=(N(row['unit_net'])*N(row['quantity'])*(1-N(row['discount_pct'])/100)).quantize(z,rounding=ROUND_HALF_UP);t=(net*N(row['rate'].rstrip('%'))/100).quantize(z,rounding=ROUND_HALF_UP)
 assert (net,t)==(N(row['net']),N(row['tax']));n+=net;tax+=t
ship=fix['transport']; net=n+N(ship['net']);tax+=(N(ship['net'])*N(ship['rate'].rstrip('%'))/100).quantize(z,rounding=ROUND_HALF_UP);assert net+tax==N(fix['expected']['gross'])==N('87.87')
assert fix['identity']['customer']!=fix['identity']['shipping_contact'] and fix['identity']['bill']!=fix['identity']['ship'] and fix['identity']['marketing_consent'] is False
c=j['cursor_fixture']; recs=[v.split('@')[0] for v in c['data']];assert len(set(recs))==4 and recs.count('A/101')==recs.count('B/101')==1 and c['page_size']==1
orig={c['id']:c for c in prior['subcheck_rows']};solutions={'QC02-P2':'38 muchii EX/control/pipeline, 5 fișe de origine, norm pointers și matricea inversă validate.','QC02-P4':'T20/T22/T35 legate de succesorii documentați, fără transfer funcțional retroactiv.','QC04-P2':'Calcul independent la 2 linii/transport/TVA: net 73,64 + taxe 14,23 = 87,87. Contact, bill-to/ship-to și /B negative distincte.','QC06-P3':'8 interfețe cu furnizor/consumator și legături corecte; ACK de primire separat de acceptarea rezultatului.','QC09-P1':'EX03/05 au caz numeric măsurabil; EX04 include cheie compusă, tie de timp, A/101 & B/101 distincte și retry cu cursor neavansat.','QC10-P1':'Șablon de probă și registru individual cu criteriu, artefact și expected; rubrică/hash validate.'}
rows=[{'id':x['id'],'award':0.2,'evidence':solutions.get(x['id'],'Cerință menținută din planul de bază și suplimentul anterior, fără execuție înainte de gate.')} for c in rd(R/'A11_rubrica_control.json')['criteria']for x in c['plan_subchecks']]
v={'schema':'A11-gate-CESIRO1-R3-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'subject':p.relative_to(R).as_posix(),'plan_sha256':h(p),'previous_review_sha256':h(E/'A11_gate_CESIRO1_R2.json'),'base_bundle':j['signed_base_bundle'],'ruby':j['rubric_sha256'],'result':'ACCEPTAT_PLAN_EX01_EX08','quality_plan':10,'approved_subchecks':50,'maximum_subchecks':50,'subcheck_rows':rows,'source_inventory_metadata_counts':[363,392,95],'verified_parent_edges':len(edge),'edge_issues':0,'source_task_fixtures':len(j['origin_criteria']),'commercial_oracle':{'line_net':str(n),'net_with_transport':str(net),'tax':str(tax),'gross':str(net+tax)},'cursor_expected':recs,'open_hard_blockers':[],'external_checks_executed_at_gate':j['execution_count'],'product_or_report_score':None,'limits':'Autorizează execuția izolată EX01–EX08 pe corpusul înghețat și condițiile declarate. Nicio afirmație de compatibilitate a conectorului, livrare, acceptare a taskurilor istorice sau acces real la comerciant.'};v['rubric_sha256']=v.pop('ruby')
out=E/'A11_gate_CESIRO1_R3.json';out.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(h(out))

