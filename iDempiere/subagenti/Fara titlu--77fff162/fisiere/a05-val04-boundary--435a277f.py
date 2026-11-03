from pathlib import Path
import datetime
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import zipfile

ROOT=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
OUT=ROOT/'executie/R11_fisiere/A05/Val_04'
OUT.mkdir(parents=True,exist_ok=True)
GIT=Path('D:/CodexWork/eva-audit-p01-src-20261101')
LOCAL=Path('D:/CodexWork/eva-audit-p01-readonly-20261102')
NATIVE=Path('D:/CodexWork/eva-audit-secondary-20261102')
HEAD='2fe90ed3f128c33dff7cf9f8674e664a70679390'
hash_bytes=lambda value:hashlib.sha256(value).hexdigest()
hash_file=lambda path:hash_bytes(path.read_bytes())
oid=lambda data:hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
read=lambda path:json.loads(path.read_text(encoding='utf-8-sig'))
def execute(args,input=None,timeout=45):
    return subprocess.run([str(x) for x in args],input=input,capture_output=True,timeout=timeout)

gate=ROOT/'executie/R11_plan_delta/A11_verdict_plan_delta_R11_v3.json'
assert hash_file(gate)=='57b63643abcea8fcb1c716465a9dcb86e9f89a59ec3940d42035df940db2dd14'
assert read(gate)['candidate']==HEAD and read(gate)['quality_score_plan']==10
with gzip.open(ROOT/'executie/R11_plan_delta/Dispatch_tehnic_integral.jsonl.gz','rt',encoding='utf8') as stream:
    dispatch={row['path']:row for row in map(json.loads,stream)}
prefix='idempiere/plugins/com.eva.ro.contab/'
classes=['src/com/eva/ro/contab/EvaActivator.java','src/com/eva/ro/contab/setup/EvaMetadata.java',
         'src/com/eva/ro/contab/component/EvaNotaSetBomEvents.java',
         'src/com/eva/ro/contab/corelare/NotaSetWmsProces.java','src/com/eva/ro/contab/corelare/SetLista.java',
         'src/com/eva/ro/contab/wms/ListaMaterialeWms.java','src/com/eva/ro/contab/wms/StocWms.java',
         'src/com/eva/ro/contab/wms/NotaSetWms.java','src/com/eva/ro/contab/wms/ModelWms.java',
         'src/com/eva/ro/contab/form/DialogNotaSetWms.java']
sources=[]
for relative in classes:
    name=prefix+relative
    meta=execute(['git','-C',GIT,'rev-parse',HEAD+':'+name])
    if meta.returncode:
        raise RuntimeError('Missing declared source '+name)
    key=meta.stdout.decode().strip()
    body=(LOCAL/name).read_bytes() if (LOCAL/name).is_file() else b''
    if oid(body)!=key:
        process=execute(['git','-C',GIT,'cat-file','blob',key]);assert process.returncode==0;body=process.stdout
    assert oid(body)==key
    target=OUT/'surse'/relative
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(body)
    d=dispatch.get(name,{})
    sources.append({'file':name,'oid':key,'sha256':hash_bytes(body),'owner':d.get('owner'),'peer':d.get('peer'),'control':d.get('control'),'file_id':d.get('id')})

native_jar=NATIVE/'org.adempiere.base_13.0.0.202603090043.jar'
assert hash_file(native_jar)=='86c82f54299f55e8f5089e0c48f13dc29432fdecec205a51560eb48dc54ac8c3'
native_sources=[]
native_files=['org/eevolution/model/MPPProductBOM.java','org/eevolution/model/MPPProductBOMLine.java','org/compiere/model/PO.java','org/compiere/model/ModelValidationEngine.java','org/compiere/model/ModelValidator.java','org/compiere/model/Query.java']
with zipfile.ZipFile(native_jar) as archive:
    for relative in native_files:
        native_source=NATIVE/'native/org.adempiere.base/src'/relative
        target=OUT/'surse_native'/relative
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(native_source.read_bytes())
        cname=relative[:-5].replace('/','.')
        bytecode=execute(['C:/Program Files/Java/jdk-21/bin/javap.exe','-classpath',native_jar,'-p','-c',cname])
        assert bytecode.returncode==0
        target.with_suffix('.javap.txt').write_bytes(bytecode.stdout)
        native_sources.append({'file':'org.adempiere.base/src/'+relative,'source_commit':'da0730aec42f3e9f5f671e81a70ff71e24d5e534','source_sha256':hash_file(native_source),'mounted_class_sha256':hash_bytes(archive.read(relative[:-5]+'.class')),'javap_sha256':hash_bytes(bytecode.stdout),'scope':'Sursă oficială release-13; binar instalat martie 2026, analizat separat. Nu presupune echivalența integrală.'})

host='saga-server@192.168.100.151'
base_sql="BEGIN READ ONLY; SET LOCAL statement_timeout='10s'; SET LOCAL search_path TO adempiere,pg_catalog; "
queries=[
    "SELECT ad_process_id,value,classname,isactive FROM ad_process WHERE value='EVA_NotaSetWms' ORDER BY ad_process_id",
    "SELECT t.tablename, t.ad_table_id, t.isactive, t.accesslevel FROM ad_table t WHERE t.tablename IN ('PP_Product_BOM','PP_Product_BOMLine','EVA_StocWms','EVA_MiscareWms') ORDER BY 1",
    "SELECT c.relname,t.tgname,pg_get_triggerdef(t.oid) FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='adempiere' AND c.relname IN ('pp_product_bom','pp_product_bomline','eva_stocwms','eva_miscarewms') AND NOT t.tgisinternal ORDER BY 1,2",
    "SELECT tablename,columnname FROM ad_column c JOIN ad_table t ON t.ad_table_id=c.ad_table_id WHERE t.tablename IN ('PP_Product_BOM','PP_Product_BOMLine','EVA_StocWms','EVA_MiscareWms') AND (lower(c.columnname) LIKE '%version%' OR lower(c.columnname) LIKE '%lock%' OR c.columnname IN ('PP_Product_BOM_ID','M_Locator_ID','M_Warehouse_ID','Qty','QtyBOM')) ORDER BY 1,2",
    "SELECT t.tablename, v.eventmodelvalidator, v.isactive FROM ad_table_scriptvalidator v JOIN ad_table t ON t.ad_table_id=v.ad_table_id WHERE t.tablename IN ('PP_Product_BOM','PP_Product_BOMLine') ORDER BY 1,2"
]
observed=[]
for query in queries:
    process=execute(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=8',host,"docker exec -i eva-postgres-cesiro sh -c 'exec psql -X -qAt -v ON_ERROR_STOP=1 -U \"$POSTGRES_USER\" -d idempiere'"],(base_sql+query+'; ROLLBACK;\n').encode())
    observed.append({'sql':query,'exit':process.returncode,'rows':process.stdout.decode('utf8','replace').splitlines(),'error':process.stderr.decode('utf8','replace')[:900]})
mounted=execute(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=8',host,'docker exec eva-idempiere-cesiro sha256sum /opt/idempiere/plugins/org.adempiere.base_13.0.0.202603090043.jar /opt/idempiere/plugins/com.eva.ro.contab_13.0.0.jar'])
readback={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':'Read only; schema and dictionary metadata, no business row values. No Docker mutation.','queries':observed,'mounted_jar_sha':mounted.stdout.decode('utf8','replace').splitlines(),'exit_mounted':mounted.returncode}
(OUT/'Citiri_native_metadata.json').write_text(json.dumps(readback,ensure_ascii=False,indent=2),encoding='utf8')

work=Path('D:/CodexWork/a05-native-boundary-val04').resolve()
assert work.parent==Path('D:/CodexWork').resolve() and work.name=='a05-native-boundary-val04'
process=execute(['C:/Program Files/Java/jdk-21/bin/java.exe','-Djava.security.manager=allow','-Duser.home='+str(work),'-cp',str(work)+';D:/CodexWork/a12-r5-classes/all_deps/*','A05NativeBomBoundary'])
assert process.returncode==0
(OUT/'Native_boundary_stdout.txt').write_bytes(process.stdout)
(OUT/'Native_boundary_stderr.txt').write_bytes(process.stderr)
assert b'network_denied|0' in process.stdout and b'persistent_PO_effect|NONE' in process.stdout
shutil.copyfile('D:/CodexWork/A05NativeBomBoundary.java',OUT/'A05NativeBomBoundary.java')
shutil.copyfile(__file__,OUT/Path(__file__).name)
shutil.rmtree(work)
assert not work.exists()
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':HEAD,'sources':sources,'native_sources':native_sources,'native_base_jar_sha256':hash_file(native_jar),'metadata_sha256':hash_file(OUT/'Citiri_native_metadata.json'),'boundary_stdout_sha256':hash_file(OUT/'Native_boundary_stdout.txt'),'boundary_stderr_sha256':hash_file(OUT/'Native_boundary_stderr.txt'),'cleanup':{'temporary_classes_removed':not work.exists(),'local_service_started':False,'native_PO_saved':False,'network_connections_in_java':0},'source_script_sha256':hash_file(OUT/Path(__file__).name),'boundary_helper_sha256':hash_file(OUT/'A05NativeBomBoundary.java')}
(OUT/'Provenienta_si_probe.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'sources':len(sources),'native_sources':len(native_sources),'query_exit_codes':[row['exit'] for row in observed],'sha':hash_file(OUT/'Provenienta_si_probe.json')},ensure_ascii=False))
