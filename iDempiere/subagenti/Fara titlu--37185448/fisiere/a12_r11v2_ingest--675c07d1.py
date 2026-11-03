from a12_r11v2_buildbase import *
state=read(B/'Runda_11_stare.json');struct=set();textonly=set()
for rr in state['code_scan']['distinct_batch_sources']:
 sf=B/rr['file'];j=source(sf,rr['sha256']);assert j.get('head',j.get('target'))==head
 for i,r in enumerate(j['rows']):
  path=r['path'];assert R[path]['git_oid']==r.get('git_oid',r.get('git_object'))
  if r['result']=='TEXT_READ_ONLY':textonly.add(path)
  else:struct.add(path)
  if any(e['source_file']==rel(sf)and e['pointer']=='/rows/'+str(i)for e in R[path]['evidence']):continue
  entry(path,sf,'/rows/'+str(i),'COORDONATOR',['inspected']if r['result']=='TEXT_READ_ONLY'else['static'],'Conținut citit fără contract executabil'if r['result']=='TEXT_READ_ONLY'else'Verificare gramaticală/structură/format la octeții Git, cu limita de metodă a rândului; aplicația nu este invocată.',r['result'],r.get('boundary',j.get('limits',j.get('note',j.get('scope')))))
assert len(struct)==6683 and len(textonly)==26 and len(struct|textonly)==6709 and not struct&textonly
M={'A02':('Manifest_A02_R11_DB.json','e6aa9dfbe105ce1561228f7a4b683587aa5dc31d13cddf91ee38c97374ca2a48'),'A03':('Manifest_A03_R11_v2.json','2cddec953d1586d5889e0790cf76fa7be07e10dd7c12f463e4bddcac7533cf36'),'A04':('Manifest_A04_R11.json','dbc02967d3868518b10e47f9815501e38939a1e899f655550ba9355e4b5a4b3d'),'A05':('Manifest_A05_R11_WMS.json','9d9cfc69d67862742a5422fc4e91860784705ecbecf7e5890a55408c096cbbef'),'A07':('Manifest_A07_R11.json','461ad4f63705a8bbccf8a2410a6123dbebc6a87f7480221de10675a4837122a6'),'A08':('Manifest_A08_R11.json','a42b50a33be821afef6c6bb1cdcd16db935c02f4d656fd0ae5bca0dc23c76288')}
for zone,(name,h)in M.items():manifest(O/zone/name,h)
# SQL refusals are triaged per dialect/template; the initial parser result remains part of the record.
s=O/'A02/Triaj_nominal_174_SQL.json';j=source(s)
for i,row in enumerate(j['rows']):
 assert d[row['file']]['git_object']==row['git_oid']
 entry(row['file'],s,'/rows/'+str(i),'A02',['inspected','static'],'Clasificare nominală a refuzului SQL, dialect și parametri, cu citirea rândului.',row['classification'],row['disposition'])
s=O/'A02/Raport_A02_R11_DB.json';j=source(s)
for i,row in enumerate(j['file_records']):
 assert d[row['path']]['git_object']==row['git_oid']
 entry(row['path'],s,'/file_records/'+str(i),'A02',['inspected','static','exercised','reproduced'],'Seed original sau DDL în PostgreSQL16 clonat; martor pozitiv/negativ și commit/reader separat.',j['findings'][0 if i<2 else 1],j['scope_limits'])
for s in sorted((O/'A03').glob('Fisa_*.json')):
 j=source(s);path=j['source_path'];assert d[path]['git_object']==j['identity']['blob']
 ax=['inspected','static']+(['exercised','bindingVerified','reproduced']if path.endswith('/ValidatorAnaf.java')else[])
 entry(path,s,'/coverage','A03',ax,'ValidatorAnaf executat în JAR, configurare adaptată la clonă.'if path.endswith('/ValidatorAnaf.java')else'Apelant/namespace/perioadă/seed urmărite în sursă; generarea integrală nu a fost invocată.',j['mutation_differential']if path.endswith('/ValidatorAnaf.java')else j['coverage']['behavior'],j['coverage'])
for s in sorted((O/'A04').glob('Fisa_*.json')):
 j=source(s);p=j['physical'];path=p['path'];assert d[path]['git_object']==p['git_object']
 entry(path,s,'/oracles','A04',['inspected','static','exercised','bindingVerified','reproduced'],j['method'],j['oracles'],{'effect':j['persistent_effect'],'gap':j['gap']})
for s in sorted((O/'A05').glob('Fisa_*.json')):
 j=source(s);path=j['nominal']['file'];assert d[path]['git_object']==j['nominal']['git_object']
 exercised=not s.name in ['Fisa_NotaSetWmsProces.json','Fisa_ListaMaterialeWms.json']
 ax=['inspected','static']+(['exercised','reproduced']if exercised else[])
 entry(path,s,'/status','A05',ax,j['method'],j['persistent_effect']if exercised else j['status'],{'scope':j['scope'],'status':j['status'],'whole_native_event_binding':False})
for zone in ['A07','A08']:
 for s in sorted((O/zone).glob('fise/*.json')if zone=='A07'else(O/zone).glob('Fisa_*.json')):
  j=source(s);f=j['file'];p=f['path_exact'];assert f['git_oid']==d[p]['git_object']
  for i,c in enumerate(j['controls']):
   if zone=='A08':
    aa=c['axes'];ax=['inspected','static','exercised','bindingVerified','reproduced']
   else:ax=['inspected','static','exercised','bindingVerified','reproduced']
   entry(p,s,'/controls/'+str(i),zone,ax,c.get('entry_route',c.get('purpose')),c.get('observed',c.get('actual_terminal')),j.get('coverage'))
s=O/'Controale_si_fixturi/Martor_requirements_v2.json';j=source(s,'93009f5849c77ab830bce2b4276f8f8a4d067681c5a6c056d4abe6b526d96d18')
for i,row in enumerate(j['rows']):
 assert R[row['path']]['git_oid']==row['git_object']
 entry(row['path'],s,'/rows/'+str(i),'COORDONATOR',['static'],'Recalibrarea martorului PEP508, după tratarea comentariilor inline în stil pip.',row['result'],j['purpose'])
manifest(O/'A09/Manifest_A09_R11.json','1a05b26434bbfd0877c17c4c112cdfd59bbed596001371d7bdaed2806dd77e76')
for s in sorted((O/'A09/fise').glob('*.json')):
 j=source(s);path=j['file'];assert d[path]['git_object']==j['source']['git_object']
 dynamic=j['functional_evidence'] is not None
 ax=['inspected','static']+(['exercised','bindingVerified','reproduced']if dynamic else[])
 entry(path,s,'/six_axes','A09',ax,'Endpoint original și main bootstrap executate cu receptori sintetici; SQL original PG16.'if dynamic else'Citire suport/configurație și ancore sursă; efectul din proba receptorului nu este atribuit acestui fișier.',j['six_axes']if dynamic else j['line_anchors'],{'unverified':j['unverified'],'task_relation':j['task_relation'],'flow_executed':dynamic})
manifest(O/'A10/Manifest_A10_R11.json','874982c61225f1938c1b922764c2d003ec6e4c7b7d42ba39c115e0788f95b40b')
for s in sorted((O/'A10').glob('Fisa_*.json')):
 j=source(s);f=j['file'];path=f['path_exact'];assert d[path]['git_object']==f['git_oid']
 for i,c in enumerate(j['controls']):
  ax=[k for k,v in c['axes'].items()if v.get('observed')is True]
  entry(path,s,'/controls/'+str(i),'A10',ax,j['coverage']['method'],c['actual_terminal'],j['reconciliation']['limits'])
s=O/'Suite_originale_API_portal_v7/Rezultate_suite_originale.json';j=source(s,'737446e418f77f0e7acc1173782585fa3e91d88e25f1806c2ef5303192e56617')
source(s.parent/'Surse_izolate_Git.json',j['manifest_sha256'])
assert sha(s.parent/'p01-r11-test-isolated-child-v7.py')==j['runner_sha256']
suite_states=[]
for i,row in enumerate(j['rows']):
 path=row['file'];assert R[path]['git_oid']==row['git_blob']
 ncall=sum(c['stage']=='call'and c['outcome']!='skipped'for c in row['cases'])
 has_call=ncall>0 or (row['mode']=='main'and row['exit']==0 and 'theme project page contracts: PASS'in row['summary'])
 ax=['exercised']if has_call else[]
 disposition='CAZURI_EXERCITATE_CU_REZULTAT_NOMINAL'if has_call else'INCERCARE_FARA_CAZ_FUNCȚIONAL_EXECUTAT'
 suite_states.append({'file':path,'executor':'COORDONATOR','actual_cases_called':ncall,'result':disposition,'stage_outcomes':dict(collections.Counter(c['stage']+'::'+c['outcome']for c in row['cases'])),'entry_was_exercised':has_call,'exit':row['exit']})
 entry(path,s,'/rows/'+str(i),'COORDONATOR',ax,'Suita originală în copie separată cu SQLite și adapter socketpair Windows verificat; numără numai cazurile call executate ori main ajuns la oracolul explicit.',suite_states[-1],{'native_ERP':False,'output_sha256':row['output_sha256'],'diagnostic':row['summary'],'suite_nonzero_is_product_verdict':False,'operator_roles_and_native_engine':'Deschise pe fiecare caz; triajul nonzero se recepționează separat.','source_suite_unchanged':True})
if __name__=='__main__':
 print('records',len(R),'new',len(events),'struct',len(struct),'text',len(textonly));print('axes',collections.Counter(a for r in R.values()for a in axes if r['axis'][a]!='UNVERIFIED'))

