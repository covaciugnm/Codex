import pathlib,json,hashlib,datetime,re,zipfile
L=pathlib.Path(__file__).parent;R=L.parents[2]
def load(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
def dump(p,v):assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
f=load(L/'Fise_16_surse_paginare_v1.json');classlog=(L/'Laborator_arhivat_v1/logs/business_v2.classload.log').read_text(encoding='utf8')
for row in f['rows']:
 row['planned_peer']=row['planned_peer_catalog'];name=pathlib.Path(row['path']).name.removesuffix('.java');package=row['path'].split('/src/')[-1].replace('/','.').removesuffix('.java')
 row['compiled']=row['coverage_level']!='STATIC_CONTEXT_ONLY'
 row['observed_class_loaded']=any((' '+package+' ' in line or ' '+package+'$' in line) for line in classlog.splitlines()) if row['path'].endswith('.java') else False
 row['classload_evidence']=ref(L/'Laborator_arhivat_v1/logs/business_v2.classload.log')
 row['direct_method_call_in_harness']=name in ['JsonCatalogSource','CatalogIndex','CatalogSource','StoreConfig']
 row['method_evidence_type']='APEL_DIRECT_SI_REZULTAT' if row['direct_method_call_in_harness'] else 'CALE_TRANZITIVA_CORELATA_STATIC_CU_IESIREA' if row['methods_in_scope'] else 'FARA_APEL_DE_METODA_DEMONSTRAT'
 if not row['methods_in_scope']:
  row['positive']='Neexecutat nominal pentru această sursă. Hashul și rolul de compilare/context sunt singurele probe.'
  row['counterexample']='Niciun contraexemplu atribuit acestei dependențe.'
 elif name!='JsonCatalogSource':
  row['counterexample']='Nicio constatare atribuită acestei surse; cazurile neconforme apar în calculul JsonCatalogSource.'
  if name=='CatalogIndex':row['positive']='INDEX_WITNESS: build original valid=3, gol=0; identități P1/P2/P3 și materializare în pagini.'
  elif name=='CatalogSource':row['positive']='L01/L02: ProductQuery și Page originale, pagina/dimensiunea/totalul din rezultat. Fără apelul default queryProducts.'
  elif name=='StoreConfig':row['positive']='Constructor sintetic și getter tenant folosite la alegerea directorului fixture; nu reprezintă validare configurație de firmă.'
  elif name=='WebshopLog':row['positive']='Mesajele originale de indexare și sursă JSON sunt păstrate integral; numai cale diagnostică observată.'
  else:row['positive']='Ramurile tranzitive pe datele sintetice în limba ro sunt corelate cu obiectele complete arhivate; nu există matrice dedicată acestei dependențe.'
f['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();f['previous']=ref(L/'Fise_16_surse_paginare_v1.json');f['clarification']='V2 explicitează compilat/încărcat/apelat, planned_peer și martorii nominali; nu adaugă execuții.'
dump(L/'Fise_16_surse_paginare_v2.json',f)
r=load(L/'Raport_A08_paginare_lot05_v1.json');r['utc']=f['utc'];r['previous_report']=ref(L/'Raport_A08_paginare_lot05_v1.json');r['source_fiches']=ref(L/'Fise_16_surse_paginare_v2.json');r['scope'][0]='12 surse originale nemodificate: ținta și 11 dependențe de compilare, după cele două addendumuri A11. JDK21 și Gson2.9.0 fixate; core13 numai la javac, exclus din runtime. Nici JAR instalat, nici OSGi.';r['no_new_runs_in_v2']=True;r['archive_reference_rule']='Căile D:/... din documentele de pregătire sunt istorice; Mapare_arhivare_laborator_v1.json indică autoritativ copiile arhivate byte-exact.';dump(L/'Raport_A08_paginare_lot05_v2.json',r)
p=(L/'Raport_A08_paginare_lot05_lectura_v1.html').read_text(encoding='utf8');p=p.replace('Raport_A08_paginare_lot05_v1.json','Raport_A08_paginare_lot05_v2.json').replace('Fise_16_surse_paginare_v1.json','Fise_16_surse_paginare_v2.json');(L/'Raport_A08_paginare_lot05_lectura_v2.html').write_text(p,encoding='utf8')
mapping=load(L/'Mapare_arhivare_laborator_v1.json')['files'];expected={pathlib.Path(x['archived']['path']).relative_to(L.relative_to(R)/'Laborator_arhivat_v1').as_posix():x['sha256'] for x in mapping}
with zipfile.ZipFile(L/'Laborator_complet_v1.zip') as z:
 assert set(z.namelist())==set(expected)
 for n in z.namelist():assert hashlib.sha256(z.read(n)).hexdigest()==expected[n]
q={'utc':f['utc'],'archive_entries':len(expected),'archive_all_hashes_match':True,'source_fiches':16,'compiled':sum(x['compiled'] for x in f['rows']),'class_loaded':sum(x['observed_class_loaded'] for x in f['rows']),'method_paths_observed':sum(bool(x['methods_in_scope']) for x in f['rows']),'direct_harness_sources':sum(x['direct_method_call_in_harness'] for x in f['rows']),'warning':'Numărătorii au sensuri diferite. Patru surse directe nu sunt patru fișiere integral testate. Trei căi tranzitive/diagnostice sunt limitate la ramurile fixturei.','no_global_score':True};dump(L/'QA_arhiva_si_fise_v2.json',q)
print(json.dumps({'report':ref(L/'Raport_A08_paginare_lot05_v2.json'),'fiches':ref(L/'Fise_16_surse_paginare_v2.json'),'QA':q},ensure_ascii=False))
