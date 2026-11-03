import pathlib,json,hashlib,datetime,gzip,collections,functools
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';S=B/'A08_Storefront_catalog_lot04';O=B/'A11/Val04_loturi';U=S/'Run_2026-11-03T02-00-34Z'
@functools.lru_cache(None)
def raw(p):return pathlib.Path(p).read_bytes()
def sha(p):return hashlib.sha256(raw(p)).hexdigest()
@functools.lru_cache(None)
def j(p):return json.loads(raw(p).decode('utf-8-sig'))
def oid(p):b=raw(p);return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':len(raw(p))}
def write(p,x):assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
checks=[];refs=[]
def ck(n,b,d=None):checks.append({'check':n,'ok':bool(b),'details':d});assert b,(n,d)
def resolve(x):
 p=pathlib.Path(x['path']);p=p if p.is_absolute() else (R if x['path'].startswith('executie/') else S/'Sources' if x['path'].startswith(('idempiere/','frontend/')) else S)/p
 ck('reference '+x['path'],sha(p)==x['sha256'] and ('bytes'not in x or len(raw(p))==x['bytes']));refs.append(x)
def walk(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and 'sha256'in x:resolve(x)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
mp=S/'MANIFEST_A08_catalog_lot04_v1.json';cp=S/'MANIFEST_corectii_A08_v2.json';rp=S/'Raport_A08_catalog_lot04_v2.json';hp=S/'Handoff_A08_lot04_v1.json'
for p,h in [(mp,'d630c72829aee0c45fc8d507e8378a0509c9352735417238a02c5b852463f792'),(cp,'fe4d054f4d2cd707768539b24a14e86c0f27a26a8ac161cc14d66063dc6d5e8b'),(rp,'01e12ffc81d665f6ba4432e0d8250e164fda4dc74f0e44dd669787a734ecb8db'),(hp,'c01caf69a1aa1c7c428a18ca38ff40e80bedef5eae3bb26d992f1947da212030')]:ck('fixed '+p.name,sha(p)==h)
for p in [mp,cp,hp,S/'MANIFEST_lectura_A08_v3.json',U/'MANIFEST_RUN.json',S/'QA_presentation_v3/MANIFEST_QA.json']:walk(j(p))
d=j(rp);run=j(U/'Rezultate.json');r={c['id']:c for c in run['cases']};pr=j(S/'Protocol_A08_catalog_v1.json')
ck('exact10case identities',len(run['cases'])==len(r)==10 and set(r)=={c['id'] for c in pr['cases']})
for k,c in r.items():
 ck('case raw '+k,j(U/k/'Evidence.json')==c)
 ck('case noinfra '+k,c['infrastructure_failure'] is None and c['execution']=='ORIGINAL_JS_ON_SYNTHETIC_DOM' and not c['blocked_nonfixture_requests'])
 for q in c['requests']:assert q['delivered'] and q['url'].startswith('https://audit.invalid/api/catalog/products?') and q['method']=='GET'
 for im in c['screenshots']:ck('png '+im,raw(S/im).startswith(b'\x89PNG\r\n\x1a\n'))
snap=lambda c,label:next(s for s in r[c]['snapshots'] if s['label']==label)
last=lambda c:r[c]['snapshots'][-1]
ck('S01 pagination2/3 unique cards',len(r['S01']['requests'])==2 and [x['params']['page'] for x in r['S01']['requests']]==[['2'],['3']] and last('S01')['cardIds']==['SEED','PAGE2','PAGE3'])
ck('S02 sequential categories',[(x['params']['category_id'],x['params']['page']) for x in r['S02']['requests']]==[(['A'],['1']),(['B'],['1'])] and last('S02')['cardIds']==['B'] and last('S02')['title']=='Categoria B')
e=snap('S03','valid_empty');ck('S03 legitimateempty/restore',not e['cardIds'] and not e['emptyHidden'] and e['emptyText']=='Niciun produs găsit pentru căutare' and e['loadMoreHidden'] and last('S03')['cardIds']==['FOUND'] and last('S03')['emptyHidden'])
ck('S04 singleinflight',len(r['S04']['requests'])==1 and last('S04')['cardIds']==['SEED','ONCE'])
for c in ['N01','N02']:
 ck(c+' exception suppression exact',len(r[c]['requests'])==1 and len(r[c]['page_errors'])==1 and last(c)['active']==['B'] and last(c)['title']=='Categoria B' and last(c)['cardIds']==['SEED'])
ck('N01abortN02JSONdistinct',r['N01']['requests'][0]['response_spec']['mode']=='abort' and r['N02']['requests'][0]['response_spec']['mode']=='text' and r['N01']['page_errors']!=r['N02']['page_errors'])
e=snap('N03','http500_as_displayed');ck('N03errorasemptyandrecovery',r['N03']['requests'][0]['response_spec']['status']==500 and not e['cardIds'] and not e['emptyHidden'] and e['emptyText']=='Niciun produs în această categorie' and e['summary']=='Rezultate: 0' and e['loadMoreHidden'] and last('N03')['cardIds']==['B'] and len(r['N03']['requests'])==2)
ck('N04categorymismatch',len(r['N04']['requests'])==1 and r['N04']['requests'][0]['params']['category_id']==['A'] and last('N04')['active']==['B'] and last('N04')['title']=='Categoria B' and last('N04')['cardIds']==['A'])
ck('N05querymismatch',len(r['N05']['requests'])==1 and r['N05']['requests'][0]['params']['q']==['QUERY-A'] and last('N05')['query']==last('N05')['title']=='QUERY-B' and last('N05')['cardIds']==['QUERY-A'])
ck('S05Caftercompleted',len(r['S05']['requests'])==2 and r['S05']['requests'][1]['params']['category_id']==['C'] and last('S05')['active']==['C'] and last('S05')['cardIds']==['C'])
ck('5positive5negative',collections.Counter(c['oracle_met'] for c in r.values())=={True:5,False:5} and all((c['id'].startswith('S'))==c['oracle_met'] for c in r.values()))
ck('reportcountsrawmatch',d['counts']==run['summary'] and d['resources']==run['resources'] and run['resources']['contexts_created']==run['resources']['contexts_closed']==10 and run['resources']['browser_closed'])
f=j(S/'Fise_7_cai_A08_v2.json');ck('7nominalpaths',len(f)==len({x['path'] for x in f})==7 and all(x['peer_catalog']=='A06' for x in f))
walk(f)
for x in f:
 p=S/'Sources'/x['path'];ck('sourceidentity '+x['path'],sha(p)==x['sha256'] and oid(p)==x['git_oid'])
 if x['role']=='original_component_to_execute':
  assert len(x['per_case_evidence'])==10
  for t in x['per_case_evidence']:assert j(R/t['evidence']['path'])==r[t['case_id']]
 else:assert x['test_evidence'] is None and not x['positive_cases'] and not x['counterexample_cases']
ck('2JSoneblob5static',sum(x['role']=='original_component_to_execute' for x in f)==2 and f[0]['git_oid']==f[1]['git_oid'] and run['executed_blobs']==1)
ck('originalharnesssame',sha(U/'Harness.py')=='f9957d9b4e745942cc1f5e44ac21c0f9d0367c1cd8b1419185c0c6ed4bbd7a6a')
counter=O/'Contraoracol_A11_catalog_componenta_v1.json';ck('independentcounter',sha(counter)=='dc0b38d9b8a28500b53079217fc900960fa72fac7e770903ec5fa94804ad4d79' and j(counter)['unique_case_identities']==5 and j(counter)['all_independent_predicates'])
for name in ['A11CatalogComponentCounter_v2.mjs','A11CatalogReceipt.py']:
 p=O/('Runner_'+name);assert not p.exists();p.write_bytes(pathlib.Path('D:/CodexWork',name).read_bytes())
qa=O/'QA_A11_catalog_lot04_v1.json';write(qa,{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'reference_instances':len(refs),'unique_reference_paths':len({x['path'] for x in refs}),'verified_executor_case_identities':10,'independent_component_case_identities':5,'runtime_level':'Executor Chromium syntheticDOM; A11 independent Node exactfunctions, no browser rerun','visual_inspection':['N01/retry_categoryB.png','N03/http500_as_displayed.png','N04/A_response_under_B_title.png'],'source_unchanged':True})
out={'schema':'A11.R12.Val04.frontend.receipt.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11 independent','candidate':run['head'],'report':ref(rp),'handoff':ref(hp),'original_manifest':ref(mp),'additive_correction':ref(cp),'QA':ref(qa),'independent_counterexample':ref(counter),
 'decision':'RECEPȚIE LIMITATĂ A PROBELOR: trei mecanisme de defect confirmate pentru JS original în condițiile declarate; fără recepție integrală de frontend/backend/site/task.',
 'dispositions':[{'finding':'A08.R12.CATALOG.1','accepted':True,'priority':'P2_PROPUS_COMPONENTA','reason':'Abortfetch și JSONinvalid lasă încărcarea blocată. Douăerori distincte, aceeașicauză; A08browserșiA11componentă concordă. Loading intern dinbrowser este deducție din sursă/cererisupresate; observat direct în martorulA11.'},{'finding':'A08.R12.CATALOG.2','accepted':True,'priority':'P2_PROPUS_CONDITIONAL_HTTP_ERROR_SHAPE','reason':'HTTP500JSON {error} este consumat ca rezultatgol; retryreușește. Formaeroarei este sintetică, nu contractrealAPI demonstrat.'},{'finding':'A08.R12.CATALOG.3','accepted':True,'priority':'P2_PROPUS_COMPONENTA','reason':'SchimbareaB în timpceAesteîn zbor modificătitlul dar nugenereazăcerereB; cardurileAapasubB. S05confirmărecuperareCdupăsucces; nublocajpermanent.'}],
 'counts':{'original_JS_blobs_executed':1,'equal_path_identities':2,'static_only_paths':5,'executor_case_identities':10,'executor_limited_positive_controls':5,'executor_counterexamples':5,'finding_mechanisms':3,'independent_A11_component_witnesses':5,'independent_A11_calibration_attempts':1,'whole_file_acceptances':0,'task_acceptances':0},
 'calibration':'A11v1a eșuat la propria așteptare a promise-urilor între contexteVM;v2așteaptă un tur de eventloop. Nici funcțiile produsului, nici oracolul n-au fost schimbate; v1păstrat, fără credit/defect de produs. Verificatorul metadataA11 a necesitat distincția dintre caleGit și cale deartefact Sources; prima încercare s-a oprit înaintea verdictului, nu la produs. ExecutorA08nu are tentativăinfra în seria predată.',
 'source_dispositions':[{'path':x['path'],'oid':x['git_oid'],'scope':'ORIGINAL_JS_METHODS_SYNTHETIC_DOM_ONE_SHARED_BLOB' if x['role']=='original_component_to_execute' else 'STATIC_ROUTE_CONTEXT_ONLY','planned_peer':'A06','actual_peer':'A11 independent limited receipt','full_file_accepted':False} for x in f],
 'required_next_tests':['Întărește oracolele de regresie N04/N05: nu ajunge negarea unei singure stări rele. Cere explicit ultimulfiltru=cerere=IDproduse sau refuzvizibil coerent; N01/N02 trebuie să ceară și mesajeroare, nu numai recuperare. Probele actuale demonstrează defectele negative, nu sunt o suită completă de recepție a remedierii.','După adaptarea funcției existente: catch/finally și response.ok/schema, corelare generațiecerere/abort ori coadă ultimafiltare; păstrează starea și paginarea corecte, inclusiv răspunsvechi sosit după unulnou.','Rulează templatele complete cu CSSreal, etichete/traduceri, debounce280ms, sort/filtre/reset, tastatură/focus și mobile; acestea nu sunt acoperite aici.','Pentru efectpipeline real: APIversiune/JSONschema și sursaDB/JSON/G3, rolpublic/comisionar/ownership, erori realecontrolate și corelare documente; fără deducțieERPdin DOM.','Ipoteza overflow backend rămâne separat NEEXECUTATĂ și are protocol viitor, fără a explica automat erorile simulate.'],
 'limits':['StateUIesteefemeră;nuDB/ERP/Postare/DocAction/C_Order ori mutațieoperațională.','UnfișierJS încărcat integral nuînseamnă toatefuncțiile exercitate; douăcăi identice nuînseamnă20cazuri.','S05repetă precondițiaconcurență și dovedește recuperarea; nu a patra cauză. Capturiidentice N01/N02 reflectă DOMidentic, dar erorile suntdistincte; nu confirmă douădefecte.','Poarta10/10este protocol; cele5contraexemple sunt eșecuri ale contractuluideprodus, nu PASS.','C27numaiproveniențălocală, nu bindingversiuniioperative. P07NEEXECUTAT. C19/P02/D10nuînchiseintegral.','A06peerplanificat, recenzieefectivăA11; corecțiav2 păstrată alături dev1.'],
 'resources':{'executor':run['resources'],'A11':'Node process finished exit0; no service/browser/DB/scratch created. Only reports and runners retained. Existing6blocked roots untouched.','global_cleanup_claim':False},'product_score':None,'full_audit_score':None,'open_contracts':17}
vp=O/'Verdict_A11_catalog_lot04_v1.json';write(vp,out)
seal=O/'SIGILIU_A11_catalog_lot04_v1.json';write(seal,{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[ref(vp),ref(qa),ref(counter),ref(O/'Runner_A11CatalogComponentCounter_v2.mjs'),ref(O/'Runner_A11CatalogReceipt.py'),ref(O/'Runner_A11_catalog_componenta_calibrare_v1.mjs')],'immutable':True})
print(json.dumps({'verdict':ref(vp),'seal':ref(seal),'checks':len(checks)},ensure_ascii=False))
