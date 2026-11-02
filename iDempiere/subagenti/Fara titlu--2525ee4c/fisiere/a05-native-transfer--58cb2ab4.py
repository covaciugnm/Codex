import pathlib,subprocess,threading,concurrent.futures,json
w=pathlib.Path('/tmp/codex-a05.ObWQES');exec((w/'fixture.py').read_text().split('if __name__')[0]);tok=auth('GardenAdmin','GardenAdmin',11,102,11)
pg=(w/'auditor-pg').read_text().strip(); assert pg.startswith('eva-test-p01-t355-auditor-pg-')
def query(q):
    assert q.startswith('SELECT')
    return subprocess.run(['docker','exec',pg,'psql','-U','postgres','-d','idempiere','-Atc',q],capture_output=True,text=True,check=True).stdout.strip().replace('\n',',')
def api(m,r,data):
    c,b=request(m,r,data,tok);print(m,r,c,'id',b.get('id'), 'status',b.get('DocStatus'),'summary',str(b.get('detail',b.get('summary','')))[:260],flush=True);return c,b
c,b=api('POST','processes/eva_activarewms',{'M_Warehouse_ID':50000})
api('POST','processes/eva_activarewms',{'M_Warehouse_ID':50000})
print('pair rows 2nd warehouse',query("SELECT count(*) FROM adempiere.eva_perechewms WHERE ad_client_id=11 AND m_warehouse_id=50000"))
def snapshot(tag):
 print(tag,'G1',query("SELECT l.m_warehouse_id,sum(qtyonhand) FROM adempiere.m_storageonhand s JOIN adempiere.m_locator l ON l.m_locator_id=s.m_locator_id WHERE s.ad_client_id=11 AND s.m_product_id=123 AND l.m_warehouse_id IN(103,50000) GROUP BY 1 ORDER BY 1"),'G2',query("SELECT p.m_warehouse_id,sum(qty) FROM adempiere.eva_stocwms s JOIN adempiere.eva_perechewms p ON s.m_warehouse_id=p.eva_gestiunewms_id WHERE s.ad_client_id=11 AND s.m_product_id=123 GROUP BY 1 ORDER BY 1"),flush=True)
snapshot('before')
c,b=api('POST','models/M_Movement',{'AD_Org_ID':11,'C_DocType_ID':143,'MovementDate':'2026-11-02','Description':'A05 native movement test 5 pieces'})
assert c in (200,201);mid=b['id']
c,b=api('POST','models/M_MovementLine',{'AD_Org_ID':11,'M_Movement_ID':mid,'Line':10,'M_Product_ID':123,'M_Locator_ID':101,'M_LocatorTo_ID':50000,'MovementQty':5})
assert c in (200,201)
api('PUT','models/M_Movement/'+str(mid),{'doc-action':'CO'})
snapshot('after');print('transactions',query("SELECT t.m_locator_id,t.movementqty FROM adempiere.m_transaction t JOIN adempiere.m_movementline l ON l.m_movementline_id=t.m_movementline_id WHERE l.m_movement_id="+str(mid)+" ORDER BY 1"))
print('GL',query("SELECT count(*),coalesce(sum(amtacctdr),0),coalesce(sum(amtacctcr),0) FROM adempiere.fact_acct WHERE ad_table_id=(SELECT ad_table_id FROM adempiere.ad_table WHERE tablename='M_Movement') AND record_id="+str(mid)))
print('mirror delta',query("SELECT m_warehouse_id,eva_tipmiscarewms,qty FROM adempiere.eva_miscarewms WHERE ad_client_id=11 AND ad_table_id=(SELECT ad_table_id FROM adempiere.ad_table WHERE tablename='M_Movement') AND record_id="+str(mid)+" ORDER BY 1"))

