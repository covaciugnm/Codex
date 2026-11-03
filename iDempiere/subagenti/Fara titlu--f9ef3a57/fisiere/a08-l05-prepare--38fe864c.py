import pathlib,json,hashlib,gzip,datetime,shutil
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');L=R/'executie/R12_fisiere/A08_Catalog_paginare_lot05';LAB=pathlib.Path('D:/CodexWork/a08-catalog-json-l05-20261103');repo=pathlib.Path('D:/CodexWork/a12-r11-p01/repo')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(R).as_posix() if p.is_relative_to(R) else p.as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
def write(p,x):
 assert not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
src='idempiere/plugins/com.eva.ro.webshop/src/com/eva/ro/webshop/data/RegistruLegal.java';p=repo/src;b=p.read_bytes();oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
dispatch={x['path']:x for x in map(json.loads,gzip.decompress((R/'executie/R12_plan_delta/Dispatch_tehnic_integral_R12.jsonl.gz').read_bytes()).decode().splitlines())};assert dispatch[src]['git_object']==oid
dest=L/'Sources'/src;assert not dest.exists();dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
core=pathlib.Path('D:/CodexWork/a05-r12-native-cache/org.adempiere.base_13.0.0.202603090043.jar');assert sha(core)=='86c82f54299f55e8f5089e0c48f13dc29432fdecec205a51560eb48dc54ac8c3'
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':'STATIC_PREFLIGHT_NO_COMPILE_NO_PRODUCT','source':dict(ref(dest),repository_path=src,git_oid=oid,dispatch=dispatch[src]),'core_compile_classpath':ref(core),'reason':'StoreConfig.java:149 referă RegistruLegal.fractie; RegistruLegal importă DB pentru lambda neapelată de testul de paginare. Nu se modifică sursa pentru a o elimina.','proposal':'Compilăm a 11-a sursă exactă și folosim core13 original numai pentru rezoluția DB; cotaLegala, RegistruLegal și hook pentruTeste nu sunt apelate. Fără OSGi/DB. Core se află în classpath, nu este activat ca bundle.','runtime_guard':'Jurnalul de încărcare stabilește clasele efectiv încărcate; dacă apare rută fiscală/DB sau o dependență nouă, se oprește și se declară.','no_new_business_scope':True,'new_product_executions':0,'approval_pending':True}
ap=L/'Addendum_dependenta_RegistruLegal_v1.json';write(ap,out);seal=L/'SIGILIU_addendum_dependenta_v1.json';write(seal,{'utc':out['utc'],'files':[ref(ap),ref(dest)],'immutable':True});print(json.dumps({'addendum':ref(ap),'seal':ref(seal)},ensure_ascii=False))
