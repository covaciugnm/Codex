import pathlib,json,hashlib,gzip,datetime
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';S=B/'A08_Catalog_lectura_statica_lot04';O=B/'A11/Val04_loturi';O.mkdir(exist_ok=True)
def raw(p):return p.read_bytes()
def sha(p):return hashlib.sha256(raw(p)).hexdigest()
def oid(p):b=raw(p);return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def j(p):return json.loads(raw(p).decode('utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':len(raw(p))}
def write(p,d):assert not p.exists(),p;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
checks=[]
def ck(n,b):checks.append({'check':n,'ok':bool(b)});assert b,n
sp=S/'SIGILIU_lectura_statica_v2.json';ck('seal',sha(sp)=='7d3c70215edb11730c365be4890d0543b1b94122b6e5502e53b75bfceb95a7b4')
s=j(sp)
for r in [s['previous_manifest'],s['report_current']]:ck(r['path'],sha(R/r['path'])==r['sha256'])
m=j(R/s['previous_manifest']['path']);p=R/s['report_current']['path'];d=j(p)
for e in m['files']:ck('file '+e['path'],sha(R/e['path'])==e['sha256'] and len(raw(R/e['path']))==e['bytes'])
dispatch={x['path']:x for x in map(json.loads,gzip.decompress(raw(R/'executie/R12_plan_delta/Dispatch_tehnic_integral_R12.jsonl.gz')).decode().splitlines())}
for e in d['entries']:
 q=S/'Sources'/e['path'];ck('source SHA/OID '+e['path'],sha(q)==e['sha256'] and oid(q)==e['git_oid']==dispatch[e['path']]['git_object'])
 ck('owner/peer '+e['path'],e['responsabil_catalog']==dispatch[e['path']]['owner'] and e['peer_catalog']==dispatch[e['path']]['peer'])
 lines=raw(q).decode('utf8').splitlines();expected=[]
 for a,b in e['intervale_citite']:expected.extend(str(i)+': '+lines[i-1] for i in range(a,b+1))
 lp=S/(q.name+'.lectura.txt');ck('line rendering '+q.name,lp.read_text(encoding='utf8').splitlines()==expected)
 if e['fisier_integral_citit']:ck('complete line scope '+q.name,e['intervale_citite']==[[1,len(lines)]] and len(lines)==164)
 ck('no runtimecredit '+q.name,e['peer_realizat'] is False and e['rezultat']=='LECTURA_STATICA_PARTIALA; IPOTEZA_PENTRU_PROTOCOL_VIITOR')
v1=j(S/'Raport_lectura_statica_v1.json');ck('v2 only declared metadata changes',all({k:v for k,v in a.items() if k!='peer_catalog'}=={k:v for k,v in b.items() if k!='peer_catalog'} for a,b in zip(v1['entries'],d['entries'])) and v1['ipoteza']==d['ipoteza'])
out={'schema':'A11.R12.Val04.static.catalog.peer.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11 independent','report':ref(p),'source_seal':ref(sp),'checks':checks,'method':'Independent reading of the four declared exact source ranges, Git blob/SHA/catalog checks and fragment-to-source equality; no compilation, Java/Python business call, arithmetic-expression execution, servlet or network test.',
 'decision':'ACCEPTAT CA LECTURĂ STATICĂ ȘI IPOTEZĂ DE TEST, CU ZERO CONSTĂTĂRI RUNTIME CONFIRMATE.',
 'source_dispositions':[{'path':e['path'],'oid':e['git_oid'],'read_ranges':e['intervale_citite'],'whole_source_read':e['fisier_integral_citit'],'execution':False,'whole_file_accepted':False} for e in d['entries']],
 'reasoning':['JsonCatalogSource.queryProducts normalizează pag≥1/perPag1…96, apoi multiplică int la516 și folosește de/la în subList523. Un intpage valid foarte mare poate depăși domeniul offsetului; limita perPage nu este suficientă singură. Ipoteza are ancoră statică directă.','Dacă indexul este null, metoda revine la430–438 înaintea paginării; trebuie separat catalogabsent de catalogprezentgol în testul viitor.','CatalogSources.catalogSource alege DB numai dacă setareaDB și db.isAvailable suntadevărate; înrestJSON. Această lectură nu probează disponibilitateaDB ori configurația activă a vreunui canal.','WebshopServlet.intParam întoarce un intmarevalid fărăplafon, dar revine laimplicit pentru numărîn afaraint sau neparsabil. StatusulHTTP efectiv nu este testat; declarația throwsException nu este un500 măsurat.','cms.py folosește intPython/slice; comportamentul comparat este raționament static, nu rezultat de funcție executată.','Celepatru căi nu sunt patru defecte. Ipoteza unică rămâne A08.CATALOG.PAGINATION.INT.CANDIDATE, severitate neacordată. Nicio cauzalitate cu erorileHTTP simulate în catalogulJS.'],
 'future_protocol_checklist':['Fixează sursa și clasa efectivă, StoreConfig, fișiercatalog/index și fallbackulJSON; fără catalog operațional.','Pozitive: prima/a doua pagină, ultima, pagina imediatdupăsfârșit, total mic; schema de răspuns și has_more independente.','Contra: pragulpage44739244/per48, vecinii pragului, MAX_VALUE, perPage1/96; indexabsent separat de indexprezentgol.','Clasifică excepția originală la exactcalea dinqueryProducts; nu predeclara HTTP500 dintr-un apelcomponentă.','APIservlet și sursaDB necesită probe separate dacă se solicită efectHTTP ori comparațiebackend.','Adaptă mecanismul de paginare existent cu tipoffset suficient și intervalvalid înainte de index; păstrează contractulresponse și nu introduce motorcatalognou.'],
 'execution_credit':0,'confirmed_runtime_findings':0,'product_score':None,'whole_file_or_task_closed':0,'operational_writes':0,'resources':'Only audit artifacts written; no browser/runtime/lab created.'}
op=O/'Peer_A11_catalog_lectura_statica_v2.json';write(op,out)
seal=O/'SIGILIU_Peer_A11_catalog_static_v1.json';write(seal,{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[ref(op)],'immutable':True})
print(json.dumps({'peer':ref(op),'seal':ref(seal),'checks':len(checks)},ensure_ascii=False))
ap=B/'A08_Storefront_catalog_lot04/Addendum_metoda_A08_v1.json';gp=B/'A05_G3_nativ_lot04/Clarificare_ordine_fixture_G3_v1.json'
assert sha(ap)=='31588c73dd1ea473ce02485c6e1e7774b248ddcfd020c1994fdbb8659e1a372c';assert sha(gp)=='17d91252dcc59932afb1033baa0f9981205efa25d7fc81f02b806f9c14ebceab'
mp=B/'A11/Val04_preflight/Recepție_clarificari_metoda_v1.json';write(mp,{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11','references':[ref(ap),ref(gp)],'decision':'Ambele clarificări se încadrează în protocoalele și condițiile recepționate; nicio schimbare de obiectiv/oracol.','frontend':'Valoareinputfixture fărăinput, apoiEnterreal; debounce280ms nu primeștecredit. S05contextnou cu A/B/C este scenariurecuperare, nu unnoudefect.','G3':'MasterdataPOcomisă și recitită înainte de MProduct.get fărătrx; stockcomis înainte de rezervări. ASI/ownership persistente și argumente corecte; niciun testnou dovedit numai de aceastăordine.','product_executions':0,'product_score':None})
ms=B/'A11/Val04_preflight/SIGILIU_clarificari_metoda_v1.json';write(ms,{'files':[ref(mp)],'immutable':True});print(json.dumps({'methods':ref(mp),'seal':ref(ms)},ensure_ascii=False))
