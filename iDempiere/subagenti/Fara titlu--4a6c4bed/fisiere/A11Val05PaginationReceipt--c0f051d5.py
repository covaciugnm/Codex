import pathlib,json,hashlib,gzip,zipfile,datetime,collections
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';L=B/'A08_Catalog_paginare_lot05';A=L/'Laborator_arhivat_v1';O=B/'A11/Val05_loturi'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p)}
checks=[]
def ck(n,b,detail=None):checks.append({'check':n,'ok':bool(b),'detail':detail});assert b,(n,detail)
m=L/'MANIFEST_A08_paginare_lot05_v1.json';report=L/'Raport_A08_paginare_lot05_v3.json';fi=L/'Fise_16_surse_paginare_v2.json';res=L/'Rezultate_paginare_v1.json'
ck('Sigiliu manifest final',sha(m)=='b8d60193a2429057dcd860813141c578c29e2234d0c3225c4efb686fe724cad7');ck('Raport autoritativ',sha(report)=='4b44bf0d258639747e9c2976f1340cbdcc2cf7a3f3d732e63aa344144a19050d')
manifest=j(m);ck('183 artefacte distincte',len(manifest['files'])==len({x['path'] for x in manifest['files']})==183)
for x in manifest['files']:
 f=R/x['path'];ck('Manifest '+x['path'],sha(f)==x['sha256'] and f.stat().st_size==x['bytes'])
mapping=j(L/'Mapare_arhivare_laborator_v1.json')['files'];ck('137 adrese de laborator',len(mapping)==len({x['original_runtime_path'] for x in mapping})==137)
with zipfile.ZipFile(L/'Laborator_complet_v1.zip') as z:
 ck('137 intrări ZIP distincte',len(z.namelist())==len(set(z.namelist()))==137)
 for x in mapping:
  f=R/x['archived']['path'];n=f.relative_to(A).as_posix();ck('Arhivă/copie '+n,hashlib.sha256(z.read(n)).hexdigest()==sha(f)==x['sha256']==x['archived']['sha256'])
dispatch={x['path']:x for x in map(json.loads,gzip.decompress((R/'executie/R12_plan_delta/Dispatch_tehnic_integral_R12.jsonl.gz').read_bytes()).decode().splitlines())}
fiches=j(fi)['rows'];ck('16 căi distincte',len(fiches)==len({x['path'] for x in fiches})==16)
for f in fiches:
 p=R/f['source']['path'];v=p.read_bytes();d=dispatch[f['path']]
 ck('Sursă SHA/OID/dispatch '+f['path'],sha(p)==f['source']['sha256'] and hashlib.sha1(b'blob '+str(len(v)).encode()+b'\0'+v).hexdigest()==f['git_oid']==d['git_object'])
 ck('Rutare catalog '+f['path'],d['owner']==f['owner_catalog'] and d['peer']==f['planned_peer_catalog'] and d['id']==f['file_id'])
 ck('Fără închidere '+f['path'],not f['whole_file_acceptance'] and not f['task_acceptance'])
 if f['compiled']:ck('Copie javac '+f['path'],sha(A/'source'/f['path'])==sha(p))
before=j(A/'logs/business_v2.before.json');after=j(A/'logs/business_v2.after.json')
for k in ['fixture','sources','classes']:
 ck('Inventar neschimbat '+k,before[k]==after[k])
for x in before['fixture']:ck('Fixture arhivată '+x['path'],sha(A/'fixture'/x['path'])==x['sha256'])
cmd=j(A/'logs/business_v2.json');compile_cmd=j(A/'logs/compile_v3.json');ck('Execuție completă și core absent runtime',cmd['returncode']==0 and 'adempiere' not in cmd['command'][cmd['command'].index('-cp')+1]);ck('Compilare strictă originală',compile_cmd['returncode']==0 and '-proc:none' in compile_cmd['command'] and '-implicit:none' in compile_cmd['command'])
ck('12 surse javac plus 2 harness',len([x for x in compile_cmd['command'] if x.endswith('.java')])==14)
stdout=(A/'logs/business_v2.stdout.txt').read_text(encoding='utf8');lines=stdout.splitlines();raw_cases=[json.loads(x.split('|',1)[1]) for x in lines if x.startswith('CASE|')];rs=j(res);rows=rs['rows'];ck('16 CASE unice',len(raw_cases)==len(rows)==len({x['id'] for x in rows})==16)
ck('Ordine originală Q01–12 și L01–04',[x['id'] for x in rows]==[f'Q{i:02d}' for i in range(1,13)]+[f'L{i:02d}' for i in range(1,5)])
fail=[];oracle=[]
for row,raw in zip(rows,raw_cases):
 ck('Sortie brute '+row['id'],raw==row['actual'])
 page=max(1,row['input']['page']);per=min(96,max(1,row['input']['per_page'])) if row['entry']=='query' else min(200,max(1,row['input']['per_page']))
 products=['P1','P2','P3'] if row['fixture']=='valid' else [];offset=(page-1)*per;expected={'product_ids':products[offset:offset+per],'total':len(products),'page':1 if row['fixture']=='absent' else page,'per_page':per}
 if row['entry']=='query':expected['has_more']=offset+per<len(products)
 ck('Oracol propriu '+row['id'],row['expected']==expected,expected)
 ok=raw['outcome']=='RETURN' and all(raw.get(k)==v for k,v in expected.items())
 ck('Clasificare independentă '+row['id'],row['contract_result']==('PASS_LIMITED' if ok else 'FAIL_CONTRACT'))
 if not ok:fail.append(row['id'])
 oracle.append({'id':row['id'],'expected_independent':expected,'unbounded_offset':offset,'actual_outcome':raw['outcome'],'conformant':ok})
ck('Cele șase abateri exacte',fail==['Q07','Q08','Q09','Q11','L03','L04'])
for x in rows:
 if x['id'] in ['Q07','Q08','Q11','L03']:ck('Cauză concretă '+x['id'],x['actual']['exception_class']=='java.lang.IndexOutOfBoundsException' and 'JsonCatalogSource.' in x['actual']['stacktrace'])
 if x['id'] in ['Q09','L04']:ck('Revenire la prima pagină '+x['id'],x['actual']['product_ids']==['P1','P2','P3'] and oracle[[z['id'] for z in oracle].index(x['id'])]['unbounded_offset']==3*2**32)
ck('9 canari, 8 refuzuri',len(rs['canaries'])==9 and sum('|DENIED|' in x for x in rs['canaries'])==8 and rs['canaries'][0]=='CANARY|fixture_read|ALLOWED')
ck('Index construit valid și gol',rs['index_witness']=={'valid_ids':['P1','P2','P3'],'absent_readable':False,'valid_total':3,'empty_total':0,'empty_constructed':True})
ck('Serializer Unicode/escape/null',rs['serializer_witness']=={'unicode':'Română țară Ω','escaped':'quote" slash\\ newline\n tab\t','null':None,'list':[1,2.5,True,False,None,'x']} and 'SERIALIZER_NEGATIVE|true' in stdout)
ck('Nicio eroare index mascată în seria finală','index build failed' not in stdout.lower())
classlog=(A/'logs/business_v2.classload.log').read_text();levels=collections.Counter(f['coverage_level'] for f in fiches)
ck('Număr de niveluri distincte',levels=={'ORIGINAL_COMPONENT_PARTIAL':2,'ORIGINAL_VALUE_TYPE_PARTIAL':1,'ORIGINAL_TRANSITIVE_PATH_PARTIAL':2,'COMPILE_ONLY_NO_METHOD_CREDIT':5,'ORIGINAL_DIAGNOSTIC_PATH_PARTIAL':1,'ORIGINAL_FIXTURE_BINDING_PARTIAL':1,'STATIC_CONTEXT_ONLY':4})
for f in fiches:
 if f['compiled']:
  cls=f['path'].split('/src/',1)[1][:-5].replace('/','.')
  ck('Încărcare nominală '+cls,(cls+' source:' in classlog)==f['observed_class_loaded'])
ck('Core și fiscal neobservate runtime',' org.compiere.' not in classlog and ' org.adempiere.' not in classlog and 'com.eva.ro.webshop.data.RegistruLegal source:' not in classlog)
counter=O/'Contraoracol_A11_paginare_v1.json';ck('Contraoracol independent sigilat',sha(counter)=='cac02e5e63d92f303be1c82c23ebe8b492a6cabf120047599d5d76ad32a2dce2')
cleanup=L/'Cleanup_final_v1.json';own_cleanup=O/'Cleanup_A11_paginare_v1.json';ck('Ambele evidențe cleanup păstrate',sha(cleanup)=='46a6140354f281d45ea2ec673ed78fc225e6d3877253dbdccd7b1cd62e1b841b' and sha(own_cleanup)=='cd0ec8187f066f4565ac09c94490b520dabd4acae1b4d682f5f8b3f49afe191a')
per_source=[]
for f in fiches:
 per_source.append({'path':f['path'],'file_id':f['file_id'],'git_oid':f['git_oid'],'owner':dispatch[f['path']]['owner'],'planned_peer':dispatch[f['path']]['peer'],'executor':'A08','independent_reviewer':'A11','disposition':'ADMIS_LIMITAT' if f['coverage_level'] not in ['COMPILE_ONLY_NO_METHOD_CREDIT','STATIC_CONTEXT_ONLY'] else 'FARA_CREDIT_EXECUTIE','level':f['coverage_level'],'methods':f['methods_in_scope'],'events':f['events'],'evidence_kind':f['method_evidence_type'],'persistent_effect':'Nicio scriere persistentă atribuită. Fixture byte-identică; numai ieșiri și diagnostic în laborator.','finding_assigned':f['path'].endswith('/JsonCatalogSource.java'),'whole_acceptance':False,'limits':f['limits']})
out={'schema':'A11.R12.Val05.pagination.receipt.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11 independent','head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','decision':'ADMIS LOTUL CA DOVADĂ LIMITATĂ DE COMPONENTĂ; CONFIRMAT DEFECTUL DE PAGINARE JSON. RECEPȚIA PRODUSULUI, HTTP, DB ȘI PIPELINEULUI RĂMÂNE DESCHISĂ.','input_manifest':ref(m),'report':ref(report),'fiches':ref(fi),'results':ref(res),'independent_counteroracle':ref(counter),'method':'Rehash complet, arhivă ZIP confruntată cu 137 copii, 16 identități SHA/OID/dispatch, interpretare independentă a fiecărei ieșiri față de întregi fără overflow, lectură harness/policy/compilare/classload, plus reproducere A11 cu propriile fixture/harness/compilare (6 apeluri separate).','checks':checks,'independent_oracles':oracle,'counts':{'executor_cases_unique':16,'executor_conformant_limited':10,'executor_nonconformant':6,'exception_events':4,'wrong_page_events':2,'finding_mechanisms':1,'source_sites':2,'A11_calls_separate':6,'A11_controls':2,'A11_counterexamples':4,'compiled_original_sources':12,'source_paths_with_partial_observation':7,'compile_only_sources':5,'static_context_paths':4,'whole_files_tasks_contracts':0},'source_level_counts':dict(levels),'per_source':per_source,'finding':{'id':'R12-CATALOG-JSON-PAGINATION-01','disposition':'CONFIRMAT LA METODELE ORIGINALE, ÎN FIXTURE SINTETICĂ','promotes_candidate':'A08.CATALOG.PAGINATION.INT.CANDIDATE','priority':'P2','priority_scope':'Eroare de corectitudine a componentei la valori extreme acceptate; frecvența operațională și statusul HTTP nu sunt măsurate.','requirement':'V04-N04 / A08-P02 / D10: paginare coerentă a catalogului existent.','actor':'Vizitator public ca actor funcțional; apel direct de metodă, fără login ori cerere HTTP.','normal_route':'Servlet → CatalogSources → JsonCatalogSource condiționat de alegerea sursei JSON, documentat numai static; listProducts este altă intrare directă, fără expunere UI demonstrată.','mechanism':'(page-1)*perPage este evaluat în int înainte de limitarea la dimensiune. Pragul 44739244/48 devine negativ; 268435457/48 revine la zero.','persistent_effect':'Niciun fișier fixture modificat; nicio DB/cerere HTTP. Rezultate incorecte sau excepții observate.','native_first':'Adaptați cele două calcule ale cititorului existent, cu offset long limitat înainte de cast și capăt/has_more coerente. Nu este justificat un nou motor de catalog sau o extensie ERP pentru această aritmetică.','repair_oracle':'Cele 16 cazuri exacte trebuie să respecte listele/totalurile/page/per_page/has_more; toate cele 6 extreme trebuie să fie goale, nu doar să nu arunce. Adăugați separat limita 200 listProducts, pageCount, filtre și integrarea HTTP/DB dacă aceasta este revendicată.'},'accepted':['16 cazuri și o singură constatare în două situri, fără dublarea cu 6 apeluri A11.','Două componente, două căi tranzitive limitate, un diagnostic, un tip de valoare și o configurare, la nivelurile nominale.','Q12 este caracterizarea ieșirii timpurii când indexul lipsește; nu validează indexarea și nu înlocuiește Q10/Q11 pentru index gol valid.','Compilările și emitterul nereușite sunt calibrări păstrate. business_v1 a executat readiness CatalogIndex, fără CASE; nu este zero produs.'], 'rejected_claims':['12 fișiere testate integral sau 7 componente comerciale integral validate','HTTP 500, cauzalitate cu erorile mock frontend Val04, DB source, OSGi/JAR instalat ori fiscal executat','rc0 al colectorului ca trecere produs; cele 6 FAIL_CONTRACT rămân abateri','Credit automat pentru classload, compilare, default CatalogSource.queryProducts, pageCount sau metode neatinse','Zero resturi de laborator: ștergerile au fost respinse automat'], 'resource_status':{'A08_retained_root':'D:/CodexWork/a08-catalog-json-l05-20261103','A08_files_retained':137,'A11_retained_root':'D:/CodexWork/a11-catalog-oracle-l05-20261103','A11_files_retained':54,'reason':'Remove-Item literal respins înainte de execuție: blocked by policy. Fără reîncercare sau ocolire.','previous_retained_roots':6,'total_retained_roots':8,'active_JVM_of_these_lots':0,'operational_writes':0,'A05_other_lab':'În lucru separat; nu este inclus în zero JVM al acestor două loturi.'},'remaining':['A12: integrare nominală și deduplicare cu Val04, fără credit din simpla compilare.','A05: finalizarea readiness/migrare nominală apoi DocAction/generator în poarta admisă; recepție separată.','Frontend: filtru = cerere = produse și recuperare cu eroare vizibilă după remediere.','G3: SO/PO, capacitate comună, rezervări în pipeline complet; nicio închidere din paginare.','N05/G1: BOM concurent, costuri și Fact_Acct cu consum o singură dată; CPP/CPA distincte și nereutilizare.','Cele 17 contracte rămân deschise; toate sigiliile anterioare rămân imuabile.'],'product_score':None,'audit_quality_full_score':None,'whole_acceptance':False}
op=O/'Verdict_A11_paginare_lot05_v1.json';assert not op.exists();op.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');rp=O/'Runner_A11_paginare_lot05_v1.py';assert not rp.exists();rp.write_bytes(pathlib.Path(__file__).read_bytes());sp=O/'SIGILIU_A11_paginare_lot05_v1.json';assert not sp.exists();sp.write_text(json.dumps({'utc':out['utc'],'files':[ref(op),ref(rp)],'immutable':True},ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'verdict':ref(op),'seal':ref(sp),'checks':len(checks),'failures':0},ensure_ascii=False))
