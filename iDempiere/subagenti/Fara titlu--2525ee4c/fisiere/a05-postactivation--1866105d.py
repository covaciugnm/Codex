import pathlib,subprocess
w=pathlib.Path('/tmp/codex-a05.ObWQES');exec((w/'fixture.py').read_text().split('if __name__')[0]);t=auth('GardenAdmin','GardenAdmin',11,102,11)
pg=(w/'auditor-pg').read_text().strip();assert pg.startswith('eva-test-p01-t355-auditor-pg-')
def q(sql):
  assert sql.startswith('SELECT')
  return subprocess.run(['docker','exec',pg,'psql','-U','postgres','-d','idempiere','-Atc',sql],check=True,capture_output=True,text=True).stdout.strip()
def api(m,r,b):
  s,j=request(m,r,b,t);print(m,r,s,j.get('id'),j.get('DocStatus'),str(j.get('detail',''))[:190]);return s,j
c,v=request('GET','models/M_Inventory/1000000',token=t); ref=lambda x:x.get('id') if isinstance(x,dict) else x
g1="SELECT sum(qtyonhand) FROM adempiere.m_storageonhand WHERE ad_client_id=11 AND m_product_id=123 AND m_locator_id=101 AND m_attributesetinstance_id=0"
g2="SELECT sum(qty) FROM adempiere.eva_stocwms WHERE ad_client_id=11 AND m_product_id=123 AND m_warehouse_id=1000000"
print('known settled warehouse: before G1,G2',q(g1),q(g2))
s,h=api('POST','models/M_Inventory',{'AD_Org_ID':11,'C_DocType_ID':ref(v['C_DocType_ID']),'M_Warehouse_ID':103,'MovementDate':'2026-11-02','Description':'A05 inventory once pair active'});assert s in(200,201)
s,l=api('POST','models/M_InventoryLine',{'AD_Org_ID':11,'M_Inventory_ID':h['id'],'M_Locator_ID':101,'M_Product_ID':123,'QtyBook':13,'QtyCount':12,'Line':10});assert s in(200,201)
s,j=api('PUT','models/M_Inventory/'+str(h['id']),{'doc-action':'CO'})
print('after G1,G2',q(g1),q(g2))
print('mirror movements for document',q("SELECT count(*) FROM adempiere.eva_miscarewms WHERE ad_client_id=11 AND ad_table_id=(SELECT ad_table_id FROM adempiere.ad_table WHERE tablename='M_Inventory') AND record_id="+str(h['id'])))

