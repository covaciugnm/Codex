import pathlib,json,subprocess,urllib.request,urllib.error,urllib.parse,ssl,os,uuid,time,datetime,concurrent.futures,threading,hashlib
W=pathlib.Path(__file__).resolve().parent
assert W.name.startswith('eva-contab-codex-a05-r2.')
def cmd(args,body=None):
 p=subprocess.run(args,input=body,capture_output=True,text=True,timeout=180); 
 if p.returncode:raise ValueError(p.stderr[-550:])
 return p.stdout.strip()
PG=(W/'auditor-pg').read_text().strip()
AP=(W/'auditor-app').read_text().strip()
assert cmd(['docker','inspect','--format','{{index .Config.Labels "eva.sesiune"}}',PG])=='eva-contab-codex-a05r2'
IP=(W/'ip').read_text().strip()
assert IP.startswith('10.') or IP.startswith('172.')
ROOT='https://'+IP+':8443'
# TLS exception is restricted to this explicitly owned, private, self-signed test endpoint.
cx=ssl.create_default_context();cx.check_hostname=False;cx.verify_mode=ssl.CERT_NONE
op=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPSHandler(context=cx))
def sql(q):
 return cmd(['docker','exec','-i',PG,'psql','-v','ON_ERROR_STOP=1','-X','-U','postgres','-d','idempiere','-At'],q)
def rows(q):return [x.split('|') for x in sql(q).splitlines() if x]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(b):return hashlib.sha256(b).hexdigest()
def wire(data):return json.dumps(data,ensure_ascii=False,separators=(',',':'),sort_keys=True).encode('utf-8')
def http(method,route,body=None,token=None,headers=None):
 assert route.startswith('/') and '://' not in route
 h={'Content-Type':'application/json','Accept':'application/json'}
 if token:h['Authorization']='Bearer '+token
 if headers:h.update(headers)
 raw=None if body is None else wire(body);r=urllib.request.Request(ROOT+route,data=raw,method=method,headers=h)
 try:
  with op.open(r,timeout=160) as v: code=v.status; data=v.read()
 except urllib.error.HTTPError as e:code=e.code;data=e.read()
 try:j=json.loads(data)
 except:j={'non_json':data.decode('utf8','replace')[:290]}
 return code,j
def auth(user,cl,role,org):
 # Standard GardenWorld demo accounts; no production credentials retrieved.
 if user=='GardenAdmin' or user=='GardenUser' or user=='System': pwd=user
 else:pwd=os.environ.get('A05_SYNTHETIC_USER_PASSWORD') or (W/'demo-secret').read_text().strip()
 c,d=http('POST','/api/v1/auth/tokens',{'userName':user,'password':pwd});assert c==200,(c,'login '+user)
 c,d=http('PUT','/api/v1/auth/tokens',{'clientId':cl,'roleId':role,'organizationId':org},d['token']);assert c==200,(c,'select role '+user,d.get('detail'))
 return d['token']
def api(t,m,route,body=None):return http(m,'/api/v1/'+route,body,t)
def check_resp(c,j):assert c in(200,201),str([c,j.get('detail',str(j)[:300])])[:600]
def new(t,tab,data):
 c,j=api(t,'POST','models/'+tab,data);check_resp(c,j);return int(j['id'])
def get(t,tab,id):
 c,j=api(t,'GET','models/'+tab+'/'+str(id));check_resp(c,j);return j
def put(t,tab,id,body):
 c,j=api(t,'PUT','models/'+tab+'/'+str(id),body);check_resp(c,j);return j
def process(t,proc,data):
 c,j=api(t,'POST','processes/'+proc,data);return {'http':c,'instance':j.get('adPInstanceId',j.get('AD_PInstance_ID',j.get('id'))),'error':j.get('isError'),'summary':j.get('summary',j.get('detail',j.get('message','')))}
def ref(x):return int(x['id'] if isinstance(x,dict) else x)
def save(name,obj): (W/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
def wh(t,name):
 d=get(t,'M_Warehouse',103);wid=new(t,'M_Warehouse',{'AD_Org_ID':11,'C_Location_ID':ref(d['C_Location_ID']),'Value':name,'Name':name});loc=new(t,'M_Locator',{'AD_Org_ID':11,'M_Warehouse_ID':wid,'Value':name+'-L','X':name+'-X','Y':'1','Z':'1','IsDefault':True});return wid,loc
def inv(t,wh,loc,prod,book,count,desc,asi=0):
 dt=int(sql("SELECT min(c_doctype_id) FROM adempiere.c_doctype WHERE ad_client_id=11 AND docbasetype='MMI' AND docsubtypeinv='PI' AND isactive='Y';"))
 did=new(t,'M_Inventory',{'AD_Org_ID':11,'C_DocType_ID':dt,'M_Warehouse_ID':wh,'MovementDate':'2026-11-02','Description':desc})
 line=new(t,'M_InventoryLine',{'AD_Org_ID':11,'M_Inventory_ID':did,'M_Product_ID':prod,'M_Locator_ID':loc,'M_AttributeSetInstance_ID':asi,'QtyBook':book,'QtyCount':count,'Line':10})
 return did,line
def doc(t,tab,id,act):
 c,j=api(t,'PUT','models/'+tab+'/'+str(id),{'doc-action':act});return {'http':c,'id':id,'status':(j.get('DocStatus') or {}).get('id'),'detail':j.get('detail','')}
def g1(wh,prod):
 return sql(f"SELECT coalesce(sum(s.qtyonhand),0) FROM adempiere.m_storageonhand s JOIN adempiere.m_locator l ON l.m_locator_id=s.m_locator_id WHERE l.m_warehouse_id={wh} AND s.m_product_id={prod} AND s.ad_client_id=11;")
def g2(wh,prod):
 return sql(f"SELECT coalesce(sum(s.qty),0) FROM adempiere.eva_stocwms s JOIN adempiere.eva_perechewms p ON p.eva_gestiunewms_id=s.m_warehouse_id WHERE p.m_warehouse_id={wh} AND s.m_product_id={prod} AND s.ad_client_id=11;")
def dbtx(did):
 return rows(f"SELECT t.m_transaction_id,t.m_locator_id,t.m_product_id,t.m_attributesetinstance_id,t.movementqty,t.xmin::text FROM adempiere.m_transaction t JOIN adempiere.m_inventoryline l ON l.m_inventoryline_id=t.m_inventoryline_id WHERE l.m_inventory_id={did} ORDER BY 1;")
def dbfacts(did):
 return rows(f"SELECT fact_acct_id,c_acctschema_id,account_id,amtacctdr,amtacctcr,record_id,line_id,xmin::text FROM adempiere.fact_acct WHERE ad_table_id=(SELECT ad_table_id FROM adempiere.ad_table WHERE tablename='M_Inventory') AND record_id={did} ORDER BY 1;")
def mirror(did):
 return rows(f"SELECT eva_miscarewms_id,m_product_id,qty,eva_tipmiscarewms,xmin::text FROM adempiere.eva_miscarewms WHERE ad_table_id=(SELECT ad_table_id FROM adempiere.ad_table WHERE tablename='M_Inventory') AND record_id={did} ORDER BY 1;")
def query_snapshot(wh,prod,did):
 return {'read_at_utc':now(),'wal_pos':sql('SELECT pg_current_wal_lsn(),txid_current_snapshot();'),'g1':g1(wh,prod),'g2':g2(wh,prod),'inventory':rows(f"SELECT docstatus,processed,posted,xmin::text FROM adempiere.m_inventory WHERE m_inventory_id={did};"),'transactions':dbtx(did),'facts':dbfacts(did),'mirror':mirror(did)}

