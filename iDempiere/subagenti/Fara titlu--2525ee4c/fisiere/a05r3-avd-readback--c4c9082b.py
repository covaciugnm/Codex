from lab import *
x=json.loads((W/'avd21-fixture.json').read_text());did=x['draft'];li=x['line'];key=x['key'];pid=x['product'];whid=x['warehouse']
data={'key':key,'captured_utc':now(),'doc':did,'line':li,'payload_sha256':x['payload_hash'],'state':query_snapshot(whid,pid,did),'line_rows':rows(f'SELECT m_inventoryline_id,m_product_id,m_locator_id,m_attributesetinstance_id,qtybook,qtycount,updated FROM adempiere.m_inventoryline WHERE m_inventory_id={did} ORDER BY m_inventoryline_id;'),'key_journal':rows(f"SELECT ad_client_id,eva_idempotencykey,eva_starehttp,eva_rezultat,eva_amprentacerere,created,updated FROM adempiere.eva_jurnalmobil WHERE eva_idempotencykey='{key}' ORDER BY 1;"),'active_schedulers':int(sql("SELECT count(*) FROM adempiere.ad_scheduler WHERE isactive='Y';"))}
print(json.dumps(data,ensure_ascii=False))

