from pathlib import Path
import subprocess,json,hashlib,datetime,sys,time
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps');import psycopg
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_G3_nativ_lot04');W=Path('D:/CodexWork/a05-g3-harness')
C=Path('D:/CodexWork/a05-r12-native-cache');F=C/'org.eclipse.osgi_3.18.500.v20230801-1826.jar';L=Path('D:/CodexWork/a05-r12-native-lab-g3-20261103')
label=sys.argv[1];mode=sys.argv[2] if len(sys.argv)>2 else 'business';assert not(O/(label+'.json')).exists();assert L.is_dir()
args=['C:/Program Files/Java/jdk-21/bin/java.exe','-Djava.security.manager=allow','-Dsun.stdout.encoding=UTF-8','-Dsun.stderr.encoding=UTF-8','-cp',str(W)+';'+str(F),'A05G3Launcher',str(L),str(C)+';D:/CodexWork/a05-n05-extra-cache','56455',mode,str(W/'a05-g3-probe.jar')]
for f in W.glob('*.java'):(O/(label+'.'+f.name)).write_bytes(f.read_bytes())
readbacks=[];seen=set();error=None
if (L/'g3-request.txt').exists():seen.add((L/'g3-request.txt').read_text().split('|')[0])
def snapshot(parts):
 token,tag,case,product,warehouse,source=parts;product=int(product);warehouse=int(warehouse);source=int(source);assert product>0 and warehouse>0 and source>0
 rows={}
 with psycopg.connect(host='127.0.0.1',port=56455,user='a05lab',password='[CREDENTIAL_REDACTED]',dbname='idempiere',autocommit=True)as conn:
  with conn.cursor(row_factory=psycopg.rows.dict_row)as c:
   c.execute('SET search_path=adempiere,pg_catalog');c.execute('SET default_transaction_read_only=on')
   def q(k,s,p=None):c.execute(s,p);rows[k]=c.fetchall()
   q('session',"SELECT pg_backend_pid(),current_setting('transaction_read_only') AS readonly, current_setting('transaction_isolation') AS isolation")
   q('reservation','SELECT * FROM m_storagereservation WHERE m_product_id=%s AND m_warehouse_id=%s ORDER BY issotrx,m_attributesetinstance_id',(product,warehouse))
   q('stock','SELECT s.*,l.m_warehouse_id,l.m_locatortype_id,coalesce(lt.isavailableforreservation,\'Y\') AS eligible FROM m_storageonhand s JOIN m_locator l USING(m_locator_id) LEFT JOIN m_locatortype lt USING(m_locatortype_id) WHERE s.m_product_id=%s ORDER BY l.m_warehouse_id,s.m_attributesetinstance_id',(product,))
   q('product','SELECT m_product_id,ad_client_id,ad_org_id,value,isactive,isbom,isstocked,producttype,m_attributeset_id FROM m_product WHERE m_product_id=%s',(product,))
   q('warehouse','SELECT m_warehouse_id,ad_client_id,ad_org_id,value,isactive,eva_tipevidenta FROM m_warehouse WHERE m_warehouse_id=%s',(warehouse,))
   q('attributes','SELECT a.m_attributeset_id,a.ad_client_id,a.isinstanceattribute,a.islot,i.m_attributesetinstance_id,i.lot FROM m_attributeset a LEFT JOIN m_attributesetinstance i USING(m_attributeset_id) WHERE a.m_attributeset_id=(SELECT m_attributeset_id FROM m_product WHERE m_product_id=%s) ORDER BY i.m_attributesetinstance_id',(product,))
   q('source','SELECT eva_sursasite_id,ad_client_id,ad_org_id,eva_sursa,isactive,eva_gestiunistoc,eva_stocrezerva,m_warehouse_id,eva_vanzarionline,eva_scrierepermisa,eva_fisaspresite,eva_stocspresite,eva_urlapi FROM eva_sursasite WHERE eva_sursasite_id=%s',(source,))
   q('auxiliary',"SELECT (SELECT count(*) FROM eva_comandasitelinie WHERE m_product_id=%s) AS site_rows,(SELECT count(*) FROM c_orderline WHERE m_product_id=%s) AS order_lines,(SELECT count(*) FROM fact_acct WHERE m_product_id=%s) AS fixture_facts,(SELECT count(*) FROM fact_acct) AS global_fact_count",(product,product,product))
   assert rows['session'][0]['readonly']=='on'
   assert rows['product'][0]['ad_client_id']==11 and rows['warehouse'][0]['ad_client_id']==11 and rows['source'][0]['ad_client_id']==11
   assert rows['auxiliary'][0]['site_rows']==0 and rows['auxiliary'][0]['order_lines']==0 and rows['auxiliary'][0]['fixture_facts']==0
   assert rows['source'][0]['eva_urlapi'] is None and all(rows['source'][0][k]=='N' for k in ['eva_vanzarionline','eva_scrierepermisa','eva_fisaspresite','eva_stocspresite'])
   assert all(x['eligible']=='Y' for x in rows['stock'])
 name=f'{label}.readback_{len(readbacks)+1:02d}_{case}.json';f=O/name;assert not f.exists()
 doc=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),token=token,tag=tag,case=case,product=product,warehouse=warehouse,source=source,read_only=True,rows=rows)
 f.write_text(json.dumps(doc,default=str,ensure_ascii=False,indent=2),encoding='utf8');readbacks.append(dict(path=name,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 (L/'g3-response.txt').write_text(token,encoding='utf8')
with(O/(label+'.stdout.txt')).open('wb')as a,(O/(label+'.stderr.txt')).open('wb')as b:
 child=subprocess.Popen(args,stdout=a,stderr=b);deadline=time.monotonic()+240
 try:
  while child.poll() is None:
   request=L/'g3-request.txt'
   if request.exists():
    parts=request.read_text().split('|')
    if len(parts)==6 and parts[0] not in seen:
     seen.add(parts[0]);snapshot(parts)
   if time.monotonic()>deadline:raise TimeoutError('240 seconds')
   time.sleep(.025)
  rc=child.returncode
 except BaseException as e:
  error=repr(e);child.kill();child.wait();rc='HARNESS_ORACLE_ERROR';raise
 finally:
  (O/(label+'.json')).write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),args=args,exit=rc,sources={f.name:hashlib.sha256(f.read_bytes()).hexdigest()for f in W.glob('*.java')},probe_jar_sha256=hashlib.sha256((W/'a05-g3-probe.jar').read_bytes()).hexdigest(),readbacks=readbacks,error=error),indent=2),encoding='utf8')
print('exit',rc,'readbacks',len(readbacks));print((O/(label+'.stdout.txt')).read_text(errors='replace')[-2500:]);print((O/(label+'.stderr.txt')).read_text(errors='replace')[-1600:])
