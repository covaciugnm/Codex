from a12_r3_survey import *
from collections import defaultdict,Counter
from functools import lru_cache
from datetime import datetime,UTC
from pathlib import Path
R=E/'R5';P=E/'R5_pregatire';R4=E/'R4'
evdoc=rd(R4/'Dovezi_criterii.json');ev=evdoc['evidence']; rev=defaultdict(list)
fields=rd(R/'probe/locatori_EV4_verificați.json')['by_id']
for eid,x in fields.items():
 d=ev[eid];d['legacy_R4_human_annotation']=d.pop('pointer',None);d['strict_primary_locators']=x['confirmed_locators'];first=x['confirmed_locators'][0];d['pointer']=first.get('pointer') if first['kind']=='json-pointer' else None;d['line']=first.get('line')
def H(b):return hashlib.sha256(b).hexdigest()
def J(v):return H(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
def esc(v):return str(v).replace('~','~0').replace('/','~1')
def date():return datetime.now(UTC).isoformat()
@lru_cache(maxsize=4096)
def digest(p):return sha(p)
@lru_cache(maxsize=96)
def jsondata(p):return rd(p)
def pointer(v,t):
 if not t:return v
 assert t.startswith('/')
 for a in t[1:].split('/'):
  a=a.replace('~1','/').replace('~0','~');v=v[int(a)] if isinstance(v,list)else v[a]
 return v
def new(path,ptr,level,value,limit,line=False):
 path=Path(path);src=path.relative_to(B).as_posix();filehash=digest(path)
 if line:
  lit=path.read_bytes().decode('utf-8-sig',errors='replace').splitlines()[ptr-1];loc={'kind':'text-line','line':ptr,'line_sha256':H(lit.encode())}
 else:loc={'kind':'json-pointer','pointer':ptr,'canonical_value_sha256':J(pointer(jsondata(path),ptr))}
 kind=(src,loc.get('line',loc.get('pointer')),level);eid='EV5-'+H(json.dumps(kind,ensure_ascii=False).encode())[:22]
 ev[eid]={'source':src,'sha_or_oid':filehash,'level':level,'pointer':loc.get('pointer'),'line':loc.get('line'),'strict_primary_locators':[loc],'content_or_observation':value,'limit':limit}
 return eid
obs=defaultdict(list)
def obsadd(cid,eid,msg,part,limit,route,expect=None,params=None):
 if eid not in [r['evidence']for r in obs[cid]]:obs[cid].append({'evidence':eid,'result':msg,'layer':part,'scope_limit':limit,'entry':route,'explicit_expected':expect,'case_input':params})
suite_limit='Aserțiunea se referă la acest JAR și această fixtură; starea generală, rolul ERP sau un click netestat se verifică separat.'
for x in rd(R/'probe/executii_corelate.json')['records']:
 path=E/x['source'];assert digest(path)==x['source_sha256']; eid=new(path,x['line'],'EXECUȚIE_COMPONENTĂ_ASERȚIUNE',x['literal'],suite_limit,True);obsadd(x['criterion'],eid,x['target']+' · '+x['literal'],x['tier'],suite_limit,x['suite'],params=x['header'])
root_sql=P/'Interogari_criterii_R5.json';root_grep=P/'Comenzi_grep_criterii_R5.json'
for i,x in enumerate(rd(root_sql)['cases']):
 if not x.get('observed_on_GardenWorld'):continue
 dt=x['observed_on_GardenWorld'];eid=new(root_sql,'/cases/'+str(i),'SQL_CABINET_SINTETIC',dt,x['limits']);obsadd(x['criterion'],eid,'GardenWorld · '+str(dt.get('sample')), 'interogare PostgreSQL',x['limits'],x['source_command'],x['oracle_original'],x['source'])
for i,x in enumerate(rd(root_grep)['cases']):
 dt=x['result']; eid=new(root_grep,'/cases/'+str(i),'MĂSURĂ_TEXT_PE_COD_FIXAT',{k:v for k,v in dt.items()if k!='files'},'Măsurare de cod, fără execuție a funcției sau a ecranului.');obsadd(x['criterion'],eid,'Măsurat '+str(dt.get('actual'))+' · '+str(dt.get('measure')),'cod Git',ev[eid]['limit'],x['recipe'],x['original_oracle'],x['source_location'])
vpath=R/'vectors/rezultate.json'
vector_map={'T330-R2-003':['days/'],'T330-R2-004':['lot/2','lot/4','lot/9','lot/11','lot/0'],'T330-R2-009':['expires/','reverse/'],'T190-R2-004':['xsd/NivelStudii']}
for i,v in enumerate(rd(vpath)):
 for cid,pr in vector_map.items():
  for tag,res in v['observed'].items():
   if not any(tag==p or (p.endswith('/') and tag.startswith(p))for p in pr):continue
   eid=new(vpath,'/'+str(i)+'/observed/'+esc(tag),'FUNCȚIE_CU_ORACOL_INDEPENDENT',res,'Intrări predeclarate în vectors/oracole.json. Nu include dialogul nativ, contabilizarea sau comparația cu sursa istorică a comenzii.');obsadd(cid,eid,v['target']+' · '+tag+' = '+str(res['observed']),'JVM proprie A12',ev[eid]['limit'],'Fefo' if cid.startswith('T330') else 'RegesXsd.valori',res['expected'],tag)
# SQL: only named semantics that actually match a criterion. Each specific raw assertion is credited to one criterion on each target.
sqlmap={'TestT217FiltruSql':{'T217-R2-004':[1,2,3,4,5,6,7,8,9]},'TestT190StudiiSql':{'T190-R2-020':[2,3,4,5,6,7,8,9,10,11,12],'T190-R2-025':[1]},'TestT354Sql':{'T354-R2-013':[1,2,3,4,5,6,7,8,9,10,11,12,13],'T354-R2-021':[14,17,18,19,20],'T354-R2-022':[15,16,21,22,23]},'TestT220CorelezSql':{'T220-R2-008':[1,2,3,4,5,6]}}
for q in [R/'sql_batch/executii.json',R/'sql_batch/recalibrare/executii.json']:
 for x in rd(q):
  if x['task_suite']not in sqlmap or not x.get('pglog')or x.get('psql_exit')!=0:continue
  p=q.parent/x['pglog'];assert digest(p)==x['pglog_sha']
  for cid,sel in sqlmap[x['task_suite']].items():
   for row in x['actual_assertions']:
    if row['line']not in sel:continue
    key=(x['task_suite'],x['target'],row['assertion_and_observed'])
    eid=new(p,row['line'],'SQL_PRODUS_PORTAT_POSTGRESQL',row['assertion_and_observed'],suite_limit,True)
    if any(e['source']==ev[eid]['source']and e.get('line')==row['line']and i!=eid for i,e in ev.items() if i.startswith('EV5-')):continue
    obsadd(cid,eid,x['target']+' · '+row['state']+' '+row['assertion_and_observed'],'SQL JAR într-o bază dedicată',suite_limit,x['java_source'],params=x['sql'])
zones={}
def zon(zone,part,scopes):
 p=E/('R2_zone/'+zone+'/'+zone+'_raport.json')
 w=rd(p)
 for i,f in enumerate(w[part]):
  fi=f['finding_id'];z={'id':fi,'title':f['title'],'observation':f.get('observed')or f.get('observed_fact'),'producer':zone,'controls_or_evidence':f['evidence_ids'],'limit':f.get('limits')or f.get('limitations')or f.get('decision'),'attributed_to':scopes.get(fi,[]),'source':p.relative_to(E).as_posix(),'sha':digest(p),'pointer':'/'+part+'/'+str(i)};zones[fi]=z
  for cid in z['attributed_to']:
   eid=new(p,z['pointer'],'REPRODUCERE_EXECUTOR_NOMINALĂ',z['observation'],str(z['limit']));obsadd(cid,eid,fi+' · '+z['observation'],'comportament pe ruta executorului; observație diferențiată',str(z['limit']),fi,params=z['controls_or_evidence'])
zon('A07','changed_findings',{'A07-F03':['T216-R3-001'] if False else ['T216-R2-008'],'A07-F04':['T216-R2-009']})
zon('A08','findings',{'A08-F02':['T216-R2-008']})
zon('A10','findings',{})
# R3 additional criteria can carry R3 IDs instead of R2. Resolve by exact normative content when named; never fallback chapter.
zs={}
for a in ['T216']:
 ac=rd(R4/('taskuri/Fisa_'+a+'.json')); ac=sum([ac[k] for k in ['operative_criteria_and_audit_criteria','R3_new_criteria','R4_new_criteria']],[])
 for old,key in [('T216-R2-008','adresa de facturare'),('T216-R2-009','livrarea reală')]:
  ids=[c['id']for c in ac if key.casefold()in c['normative_content'].casefold()]
  if old not in [c['id']for c in ac]and len(ids)==1:
   obs[ids[0]].extend(obs.pop(old,[]))
   for z in zones.values():z['attributed_to']=[ids[0] if n==old else n for n in z['attributed_to']]
# Signed source comparison; namespace & closure stay disjoint.
sup=E/'supliment_CESIRO1';plan=sup/'Plan_CESIRO1_R3.json';glob={}
summary_keys={'EX01':'route_registry','EX02':'bounded_results','EX03':'actual','EX04':'positive','EX05':'verdict_by_boundary','EX06':'final','EX07':'policy_matrix','EX08':'latency'}
for key,field in summary_keys.items():
 src=sup/'probe'/(key+'.json');d=rd(src); peers=sorted((sup/'probe').glob(key+'_peer_*.json'));q={'file':src.relative_to(B).as_posix(),'sha256':digest(src),'result_pointer':'/'+field,'result_sha256':J(d[field]),'producer_disposition':d.get('status',d.get('state',d.get('verdict'))),'peer_receipts':[{'file':p.relative_to(B).as_posix(),'sha256':digest(p)}for p in peers],'independent_status':'AVIZ_EXECUȚIE_INDEPENDENT_NEÎNREGISTRAT_ÎN_ACEST_INSTANTANEU','plan_sha':digest(plan)}
 glob[key]=q
related={x['technical']:{'record':x,'related_results':{k:glob[k]for k in x['EX']},'limitation':'Dovezi curente despre limitele precise C/W; relațiile părinte→succesor și starea administrativă nu validează material implementarea la închidere.'}for x in rd(plan)['origin_criteria']}
wr(R/'probe/comparatie_C_W.json',{'capture':date(),'winning_plan':digest(plan),'cases':glob,'task_scope':related})
wr(R/'probe/observatii_zone_nominale.json',{'sources':'R2 A07/A08/A10. Doar ID-urile asociate nominal se atribuie; celelalte au rol de indiciu de zonă. A03 R3 delimitează proprietarii și cerințele; nu constituie probă de funcționare individuală.','records':zones})
sp=P/'Simulatoare/Verificare_T219_T320_simulator.json'
if sp.is_file():
 data=rd(sp); assert digest(sp)=='8f7bc83c1532ab5ff7059076eb1d3c9154b874324a530229ba50dbd1e603bf38'
 for cid,sub in data['criteria'].items():
  if cid=='T211.06-R2-002':continue
  historical=cid=='T219-R2-003'; rows=data['tests']['checks'];chosen=next((i for i,l in enumerate(rows) if ('okazii' in l.lower() and ('scri' in l.lower() or 'refuz' in l.lower()))),None)if cid=='T320-R2-003' else 2
  if not historical and chosen is None:continue
  ptr='/criteria/'+esc(cid) if historical else '/tests/checks/'+str(chosen);msg='8/8 obiecte la commit '+data['origin_commit'] if historical else rows[chosen]
  limit=sub.get('current_criteria_limitation')or sub['scope'];eid=new(sp,ptr,'ARBORE_GIT_ISTORIC' if historical else 'SIMULATOR_HTTP_LOOPBACK',msg,limit)
  obsadd(cid,eid,msg,'istoric Git' if historical else 'simulator HTTP',limit,data['origin_commit'] if historical else data['tests']['cli'],sub.get('norm'),data['tests']['summary'] if not historical else sub['historical_git_tree'])

