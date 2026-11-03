from pathlib import Path
import json,gzip,hashlib,datetime,copy,collections
from concurrent.futures import ThreadPoolExecutor
B=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
O=B/'executie/R11_fisiere';V=O/'A12/Val_03';PREV=O/'A12/Val_02'
HEAD='2fe90ed3f128c33dff7cf9f8674e664a70679390'
inputs={};cache={};events=[];checks=[];now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(B).as_posix()
def ref(p,pt=None):
 r={'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size}
 if pt is not None:r['pointer']=pt
 return r
def source(p,h=None):
 p=Path(p);k=rel(p)
 if k not in cache:
  data=p.read_bytes();hs=hashlib.sha256(data).hexdigest()
  inputs[k]={'path':k,'sha256':hs,'bytes':len(data)}
  cache[k]=json.loads(data.decode('utf-8-sig')) if p.suffix=='.json' else data
 if h:assert inputs[k]['sha256']==h,(k,inputs[k]['sha256'],h)
 return cache[k]
def ptr(j,p):
 if p=='':return j
 assert p.startswith('/')
 for t in p[1:].split('/'):
  t=t.replace('~1','/').replace('~0','~')
  j=j[int(t)]if isinstance(j,list)else j[t]
 return j
def save(n,j):
 p=V/n;assert not p.exists(),p
 p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return p
def verify_manifest(p,h):
 m=source(p,h)
 for q in m['files']:
  t=B/q['path'];assert sha(t)==q['sha256'],q['path']
 checks.append({'manifest':ref(p),'members_verified':len(m['files'])})
 return m
verify_manifest(PREV/'MANIFEST_val_02_v2.json','46571dac6326bff593a3ad8c05741593156954541b5a421be26cd575821a85a7')
prior=source(PREV/'Handoff_val_02_v2.json','6a400efbe6e44b798fdd6f3fd06b4ea5d77d1ffc28a805deb6f91f8a8ae714af')
raw=source(PREV/'Registru_6709_val_02.jsonl.gz','d2aafde70917551072ef0367fe5fdabd8a9608dde29c1091655555c637eb9ba4')
R={r['path']:r for r in map(json.loads,gzip.decompress(raw).decode().splitlines())};assert len(R)==6709
matrix=copy.deepcopy(source(PREV/'Matrice_criterii_task_probe.json'));assert len(matrix['task_rows'])==652 and len(matrix['criterion_rows'])==2619
contracts=copy.deepcopy(source(PREV/'Contracte_17_si_capitole.json'))
chkf=O/'A11/Checklist_A11_dupa_val02_v2.json';chk=source(chkf,'ec6038418138529c71d72d543d2b2193cbfc6b7b5a0fa091cf99a7f48f03b035')
checkpoint=O/'A11/Verdict_A11_R11_checkpoint_val02_v2.json';source(checkpoint,'85275d454eb9be92c338cd3ca721c94f548172fdad78a554190db0149aadcadd')
delta=B/'executie/delta/2026-11-02T22-21-42-843Z/Comparatie_ultimul_checkpoint.json'
ds=source(delta);assert ds['head']==HEAD and ds['changes']==[] and ds['p01']==693
verdict=O/'A11/Verdict_A11_R11_lot_04_v1.json';lot=source(verdict,'b79f462d3ef6064732f0d8dd7e47790fbae52c3399ae0802dcf83cae6bf5564a')
seal=O/'A11/Sigiliu_A11_R11_lot_04_v1.json';source(seal,'99b6d7faa6fd9c63df1b804252e582c4cbf14fc1d513e56fb658cf830c868e1b')
for p,h in lot['dovezi'].items():source(O/p,h)
peer=O/'Control_harness_root/Peer_A01_harness_v7.json';pj=source(peer,'aaa8d9c9ee6a2318862ce909f88b043a685432fb5b98e0615b2f66f705675b69')
# The immutable peer manifest is located from the exact known peer directory.
peer_man=next(p for p in peer.parent.glob('*Manifest*json') if sha(p)=='cb27129f50b8750d70333cb64601162c1872e39fed535f4a53f9f8e9167dd49a') if any(peer.parent.glob('*Manifest*json')) else None
if peer_man:source(peer_man,'cb27129f50b8750d70333cb64601162c1872e39fed535f4a53f9f8e9167dd49a')
confile=O/'Suite_originale_reconciliate/Consolidare_55_suite.json';con=source(confile,'5327fb83f221673210051b7b583f8ad2414cf6c7bdd6cacc499d5a6fb37603e3')
assert con['head']==HEAD and len(con['rows'])==len({x['file']for x in con['rows']})==55
srcmanifest=O/'Suite_originale_API_portal_v10/Surse_izolate_Git.json'
sm=source(srcmanifest,'96c7b681d99d406afaf0787145f4cd434f649d642f0923e5753f5e3987e820bf')
sm_by_path={r['file']:r for r in sm['rows']}
def add(path,f,p,executor,axes,scope,observed,limit):
 assert path in R,(path,f)
 obj=source(f);ptr(obj,p)
 event={'executor':executor,'source_file':rel(f),'source_sha256':inputs[rel(f)]['sha256'],'pointer':p,'scope':scope,'result':observed,'axes':axes,'limits_and_own_axis_values':limit,'candidate':HEAD}
 event['event_id']='R11V3-'+hashlib.sha256(json.dumps(event,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:24]
 assert event['event_id']not in {x.get('event_id')for x in R[path]['evidence']}
 R[path]['evidence'].append(event)
 for a in axes:R[path]['axis'][a]='OBSERVED_ONLY_AT_LINKED_SCOPE'
 R[path]['qualifying_executor']=sorted({e['executor']for e in R[path]['evidence']})
 events.append({**event,'path':path,'file_id':R[path]['id'],'git_oid':R[path]['git_oid']})
def one(suffix):
 p=[p for p in R if p.endswith(suffix)];assert len(p)==1,(suffix,p);return p[0]
def paths(*suffix):return[one(s)for s in suffix]
maps=[
 paths('backend/saga-migration/f_bootstrap_client.py'),
 paths('frontend/app.py'),
 paths('/corelare/TrimiteFacturaSite.java'),
 paths('/corelare/TrimiteFacturaSite.java','com.eva.ro.contab_13.0.0.jar'),
 paths('seed_eva_doctype_sequences_ro.sql','seed_eva_doctype_sequences_ro_addendum.sql'),
 paths('amn_schema_alter_table.sql'),
 paths('/anaf/ValidatorAnaf.java','d101_20250214.xsd','d112_10102024.xsd'),
 paths('/form/WSagaIntrariForm.java','/efactura/AsociereEFactura.java'),
 paths('tools/saga_plugin_gen/build_plugin.sh','com.eva.ro.saga.theme/build.sh')
]
reviews=[]
for i,c in enumerate(lot['constatari']):
 assert len(maps)==len(lot['constatari'])
 rr={'finding':c['id'],'verdict':ref(verdict,'/constatari/'+str(i)),'statement':c['verdict'],'observed':c['observation'],'limit':c['boundary'],'next':c['next'],'files':maps[i],'new_task_acceptance':False}
 reviews.append(rr)
 for path in maps[i]:
  axes=['inspected']
  if i in [0,2,3]:axes+=['exercised','reproduced']
  add(path,verdict,'/constatari/'+str(i),'A11',axes,'Recepție independentă lot04 la subcondiția indicată; nu verificare integrală a fișierului.',c['observation'],{'boundary':c['boundary'],'next':c['next'],'native_pipeline_complete':False})
  R[path].setdefault('independent_reviews',[]).append(rr)
# Add actual independent experiments explicitly, with SQL/native transport limits.
for path,f,p in [
 (maps[0][0],O/'A11/A11_martor_bootstrap_lot_04.json','/cases'),
 (maps[2][0],O/'A11/A11_martor_documente_lot_04.json','/starvation_controls'),
 (maps[3][1],O/'A11/A11_martor_documente_lot_04.json','/confirmate_JAR_vs_oracol_tupla')]:
 add(path,f,p,'A11',['exercised','reproduced'],'Martor independent componentă pe SQL sau JAR; domeniu nominal.',ptr(source(f),p),'Nu este execuție OSGi, ZK sau emitere nativă a unui document.')
# Keep independent acceptance attached to the existing T216 partial claim, without new criteria.
for ca in matrix['cases']:
 if ca['case']=='A07.SENT.CONFIRMATION':
  ca['Val03_independent_review']=[ref(verdict,'/constatari/2'),ref(verdict,'/constatari/3')]
  ca['Val03_limit']='Punct de plecare TRIMIS; selecție lot și recunoaștere identitate numai. Nu dovedește emiterea facturii/plății/OSGi.'
for link in matrix['nominal_links']:
 if link['case']=='A07.SENT.CONFIRMATION':
  link['Val03_independent_review']=[ref(verdict,'/constatari/2'),ref(verdict,'/constatari/3')]
# Per-suite reconciliation is not a repeated execution or additive pass counter.
suite_rows=[];V10receipt=None
for i,c in enumerate(con['rows']):
 f=B/c['source_receipt'];receipt=source(f,c['receipt_sha256'])
 assert c['file']in R and R[c['file']]['git_oid']==c['git_blob']
 assert sm_by_path[c['file']]['git_blob']==c['git_blob'] and sm_by_path[c['file']]['sha256']==c['source_sha256']
 matched=[(k,x)for k,x in enumerate(receipt['rows'])if x.get('file')==c['file']or (('backend/'if c['file'].startswith('backend/')else'frontend/')+x.get('source',''))==c['file']]
 # storefront source names are interpreted relative to their recorded suite root.
 if not matched:matched=[(k,x)for k,x in enumerate(receipt['rows'])if c['file'].endswith('/'+x.get('source','NONE'))]
 assert len(matched)==1,(c['file'],len(matched))
 ri,r=matched[0]
 counts=collections.Counter(x['stage']+'|'+x['outcome']for x in r.get('cases',[]))
 calls=sum(n for k,n in counts.items()if k.startswith('call|')and not k.endswith('|skipped'))
 isv10='v10'in str(f)
 called=calls>0
 if c['mode']=='main':called=c['file'].endswith('test_theme_project_contracts.py') and r.get('returncode')==0
 effective='EXECUTAT_PARTIAL_REZULTATE_NOMINALE'if called else'INCERCARE_FARA_CALL_FUNCTIONAL'
 id_counts=collections.Counter(x['id']for x in r.get('cases',[]))
 row={'file':c['file'],'git_oid':c['git_blob'],'source_sha256':c['source_sha256'],'raw_consolidation':ref(confile,'/rows/'+str(i)),'original_receipt':ref(f,'/rows/'+str(ri)),'phase_counts':dict(counts),'reported_events_original':r.get('cases',[]),'distinct_reported_nodeids':len(id_counts),'nodeid_multiplicity_gt1':{k:v for k,v in id_counts.items()if v>1},'exit':c['exit'],'raw_classification':c['classification'],'effective_classification':effective,'actual_nonskipped_call_events':calls,'source_exercised_at_test_scope':called,'historical_v7_preserved':True,'new_execution_for_val03':isv10,'review_state':'ASTEPTARE_A11_V10_NODE'if isv10 else'PEER_ADAPTOR_V7_CU_LIMITE','product_verdict':None,'limit':c['reason']or'ERP și contextul autoritar sunt dubluri originale; SQLite fără crash/fsync. Exit0 nu este verdict de task.','counting_limit':'Număr evenimente pytest, nu teste distincte. Subtestele multilingve pot avea același nodeid fără parametrul lang; evenimentele sunt păstrate integral.'}
 if c['file'].endswith('test_tenant_isolation_116.py'):
  assert calls==0 and sum(counts.values())==20
  row['correction']='Consolidarea păstrată spune PASS; aici20skip/0call/exit0 înseamnă încercare fără probă funcțională.'
  assert R[c['file']]['axis']['exercised']=='UNVERIFIED'
 suite_rows.append(row)
 add(c['file'],confile,'/rows/'+str(i),'A12',[],'Reconciliere nominală a evidenței, nu o execuție suplimentară.',row,'Etichetele brute nu acordă credit funcțional ori integrare ERP.')
 if isv10:
  V10receipt=f;add(c['file'],f,'/rows/'+str(ri),'COORDONATOR',['exercised']if called else[],'Original T58 V10 pe fixture/Node; recepția independentă este separată.',row,'Fără backend ERP real, identitate actor nativă sau contabilizare; așteaptă A11.')
# The peer on harness cannot grant any new runtime axis to a product file.
for row in suite_rows:
 if not row['new_execution_for_val03']:
  R[row['file']].setdefault('harness_reviews',[]).append({'source':ref(peer),'scope':'Autenticitate/receptor V7, nu rerularea celor55 de suite.','limit':'tenant_context/ERP mock, SQLite,500 permis pe T32 citiri;20skip izolare.'})
print('PREPARED',len(events),len(suite_rows),len(reviews),'new_v10',rel(V10receipt))
phase_totals=collections.Counter()
for sr in suite_rows:phase_totals.update(sr['phase_counts'])
assert dict(phase_totals)==con['pytest_events_by_phase'],(phase_totals,con['pytest_events_by_phase'])
assert sum(s['exit']==0 for s in suite_rows)==43 and sum(s['exit']==1 for s in suite_rows)==12

