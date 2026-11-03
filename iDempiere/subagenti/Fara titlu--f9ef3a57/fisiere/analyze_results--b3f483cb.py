import pathlib,json,hashlib,datetime,re,shutil,zipfile
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');OUT=R/'executie/R12_fisiere/A08_Catalog_paginare_lot05';LAB=pathlib.Path(__file__).parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(R).as_posix() if p.is_relative_to(R) else p.as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,x):assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
protocol=load(OUT/'Protocol_paginare_JSON_v1.json');text=(LAB/'logs/business_v2.stdout.txt').read_text(encoding='utf8',errors='strict');lines=text.splitlines();cases=[json.loads(x[5:]) for x in lines if x.startswith('CASE|')]
checks=[]
def ck(name,ok,detail=None):checks.append({'check':name,'ok':bool(ok),'detail':detail});assert ok,(name,detail)
ck('16 identități distincte în ordinea protocolului',[x['id'] for x in cases]==[x['id'] for x in protocol['cases']])
canaries=[x for x in lines if x.startswith('CANARY|')];ck('9 canari cu 8 refuzuri',len(canaries)==9 and sum('|DENIED|' in x for x in canaries)==8 and canaries[0]=='CANARY|fixture_read|ALLOWED')
serializer=json.loads(next(x.split('|',1)[1] for x in lines if x.startswith('SERIALIZER_WITNESS|')))
ck('Emitter validat independent Unicode și escape/null',serializer=={'unicode':'Română țară Ω','escaped':'quote" slash\\ newline\n tab\t','null':None,'list':[1,2.5,True,False,None,'x']})
ck('Emitter respinge tip necunoscut','SERIALIZER_NEGATIVE|true' in lines)
index=json.loads(next(x.split('|',1)[1] for x in lines if x.startswith('INDEX_WITNESS|')));ck('Index original valid/gol distinct de absent',index=={'valid_ids':['P1','P2','P3'],'absent_readable':False,'valid_total':3,'empty_total':0,'empty_constructed':True})
ck('Nicio eroare indexare înghițită','nu pot indexa catalogul' not in text and '\ufffd' not in text)
ck('16 cazuri și politică activă la ieșire',json.loads(next(x[5:] for x in lines if x.startswith('DONE|')))=={'cases':16,'policy_active':True})
rows=[]
for c,p in zip(cases,protocol['cases']):
 page=max(1,p['page_input']);per=min(96,max(1,p['per_page_input'])) if p['entry']=='query' else min(200,p['per_page_input'] if p['per_page_input']>0 else 48);total=3 if p['tenant_fixture']=='valid' else 0;offset=(page-1)*per;ids=['P1','P2','P3'][offset:offset+per] if total else []
 expected={'product_ids':ids,'total':total,'page':1 if p['tenant_fixture']=='absent' else page,'per_page':per}
 if p['entry']=='query':expected['has_more']=offset+per<total
 comparisons={k:{'expected':v,'actual':c.get(k),'ok':c.get(k)==v} for k,v in expected.items()} if c['outcome']=='RETURN' else {}
 match=c['outcome']=='RETURN' and all(x['ok'] for x in comparisons.values())
 if c['outcome']=='THROW':ck('Excepție concretă index '+c['id'],c['exception_class']=='java.lang.IndexOutOfBoundsException' and 'JsonCatalogSource.' in c['stacktrace'])
 rows.append({'id':c['id'],'entry':p['entry'],'fixture':p['tenant_fixture'],'input':{'page':p['page_input'],'per_page':p['per_page_input']},'oracle_unbounded_offset':offset,'expected':expected,'actual':c,'comparisons':comparisons,'contract_result':'PASS_LIMITED' if match else 'FAIL_CONTRACT','product_score':None})
ck('10 conforme și 6 neconforme',sum(x['contract_result']=='PASS_LIMITED' for x in rows)==10 and sum(x['contract_result']=='FAIL_CONTRACT' for x in rows)==6)
ck('4 excepții și 2 liste incorecte',sum(x['actual']['outcome']=='THROW' for x in rows)==4 and [x['id'] for x in rows if x['contract_result']=='FAIL_CONTRACT' and x['actual']['outcome']=='RETURN']==['Q09','L04'])
before=load(LAB/'logs/business_v2.before.json');after=load(LAB/'logs/business_v2.after.json');ck('Fixture neschimbată',before['fixture']==after['fixture'] and after['fixtures_unchanged']);ck('Surse neschimbate',before['sources']==after['sources']);ck('Clase neschimbate',before['classes']==after['classes'])
for p in load(LAB/'Preparation_v3.json')['sources']:
 s=LAB/'source'/p.get('repository_path',p.get('path'));ck('Identitate sursă '+s.name,sha(s)==p['sha256'])
classlog=(LAB/'logs/business_v2.classload.log').read_text(encoding='utf8');loaded=[]
for l in classlog.splitlines():
 if 'com.eva.ro.webshop' in l:loaded.append(l)
ck('Core nu este classpath runtime',load(LAB/'logs/business_v2.admission.json')['core_runtime_present'] is False and 'org.adempiere.base' not in ' '.join(load(LAB/'logs/business_v2.admission.json')['runtime_classpath']))
ck('Fără clasă fiscală/core observată în jurnal',not any(x in classlog for x in ['com.eva.ro.webshop.data.RegistruLegal ','org.compiere.','org.adempiere.']))
qa={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'summary':{'unique_cases':16,'passes_limited':10,'fail_contract':6,'exceptions':4,'wrong_pages':2,'finding_mechanisms':1,'original_sites':2,'whole_file_task_contract_acceptance':0},'first_attempt':'business_v1 a executat 9 canari și 2 build-uri CatalogIndex, apoi emitterul a refuzat accessDeclaredMembers; zero CASE. Nu este etichetat zero produs.','source_compile_history':'Prima compilare v1 a eșuat din lipsa SeoEngine. v2 a compilat cele 12 originale, iar v3 a recompilat aceleași originale cu emitterul harnessului corectat.','loaded_product_class_lines':loaded,'loaded_class_limit':'Jurnalul de încărcare și classpath-ul se corelează cu harnessul și callsite-urile; absența numelui din jurnal nu este singură o dovadă universală de neexecutare.'}
dump(OUT/'Rezultate_paginare_v1.json',{'utc':qa['utc'],'protocol':ref(OUT/'Protocol_paginare_JSON_v1.json'),'rows':rows,'serializer_witness':serializer,'index_witness':index,'canaries':canaries,'run_source':ref(LAB/'logs/business_v2.json')});dump(OUT/'QA_executie_paginare_v1.json',qa)
print(json.dumps({'results':ref(OUT/'Rezultate_paginare_v1.json'),'qa':ref(OUT/'QA_executie_paginare_v1.json'),'summary':qa['summary']},ensure_ascii=False))
