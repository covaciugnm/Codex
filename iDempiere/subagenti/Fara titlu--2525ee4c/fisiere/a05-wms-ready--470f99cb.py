import pathlib, subprocess, json, concurrent.futures, threading, time
w=pathlib.Path('/tmp/codex-a05.ObWQES');exec((w/'fixture.py').read_text().split('if __name__')[0])
pg=(w/'auditor-pg').read_text().strip(); assert pg.startswith('eva-test-p01-t355-auditor-pg-')
def sql(q):
    assert q.startswith('SELECT')
    p=subprocess.run(['docker','exec','-i',pg,'psql','-X','-v','ON_ERROR_STOP=1','-U','postgres','-d','idempiere','-At','-c',q],capture_output=True,text=True,check=True)
    return p.stdout.strip()
def snap(tag):
    info=sql("SELECT m_product_id,m_attributesetinstance_id,pp_product_bom_id,sum(qty) FROM adempiere.eva_stocwms WHERE ad_client_id=11 AND m_product_id IN (123,124,125,1000004) GROUP BY 1,2,3 ORDER BY 1,2,3")
    print(tag,'physical=',info.replace('\n',','),flush=True)
def process(tag,route,body):
    t=auth('GardenAdmin','GardenAdmin',11,102,11)
    s,j=request('POST','processes/'+route,body,t)
    print(tag,'http',s,'instance',j.get('adPInstanceId',j.get('AD_PInstance_ID',j.get('id'))),'isError',j.get('isError'),'summary',str(j.get('summary',j.get('detail',j.get('message',''))))[:300],flush=True)
    return s,j
for n in range(35):
    available=sql("SELECT (to_regclass('adempiere.eva_stocwms') IS NOT NULL AND to_regclass('adempiere.eva_perechewms') IS NOT NULL AND to_regclass('adempiere.eva_validareprodusinv') IS NOT NULL AND EXISTS (SELECT FROM adempiere.ad_process WHERE value='EVA_NotaSetWms' AND isactive='Y'))")
    if available=='t':break
    if n%5==0: print('wait for all WMS components',n,sql("SELECT count(*) FROM adempiere.ad_table WHERE tablename ILIKE 'EVA_%'"),flush=True)
    time.sleep(8)
else:raise SystemExit('EVA dictionary not yet complete within observation window')
t=auth('GardenAdmin','GardenAdmin',11,102,11)
for i,raw in enumerate((123,124,125),1):
    s,j=request('POST','models/PP_Product_BOMLine',{'AD_Org_ID':11,'PP_Product_BOM_ID':1000000,'M_Product_ID':raw,'C_UOM_ID':100,'QtyBOM':6,'Line':i*10,'ComponentType':'CO'},t)
    print('BOM input',raw,'http',s,'id',j.get('id'),'detail',str(j.get('detail',''))[:180],flush=True)
    if s not in (200,201):raise SystemExit('BOM input failed without changing further lines')
s,j=process('Activate native/EVA process','eva_activarewms',{'M_Warehouse_ID':103})
pair=sql("SELECT eva_gestiunewms_id,eva_locatorneamplasat_id,eva_locatorexpediere_id FROM adempiere.eva_perechewms WHERE ad_client_id=11 AND m_warehouse_id=103")
if not pair:raise SystemExit('Activation unavailable. HTTP above; no WMS row for G1')
wh,loc,exp=map(int,pair.split('|')); print('fixture pair',wh,loc,exp,flush=True)
snap('baseline')
body={'M_Warehouse_ID':103,'EVA_TipNota':1,'M_Product_ID':1000004,'Qty':1,'M_Locator_ID':loc,'PP_Product_BOM_ID':1000000}
def stock():
    return int(sql("SELECT coalesce(sum(qty),0)::integer FROM adempiere.eva_stocwms WHERE ad_client_id=11 AND m_warehouse_id=%d AND m_product_id=1000004" % wh))
s,j=process('Assemble one initial set','eva_notasetwms',body)
snap('after one');assert stock()==1,'single set not persisted'
# Assembling a second real unit is distinct from re-delivery, and is needed to expose duplicate disassembly in the next call.
s,j=process('Assemble second genuine operation','eva_notasetwms',body);snap('two physical operations');assert stock()==2
req_body=dict(body,EVA_TipNota=2);bar=threading.Barrier(2)
def run_retry(i):
    bar.wait(timeout=10);return process('Disassemble replay '+str(i),'eva_notasetwms',dict(req_body))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:list(executor.map(run_retry,[1,2]))
snap('after concurrent disassembly retry')
print('expected stable set stock 1, observed',stock(),flush=True)
print('journal by process instance',sql("SELECT record_id,eva_tipmiscarewms,count(*) FROM adempiere.eva_miscarewms WHERE ad_client_id=11 AND eva_tipmiscarewms IN ('AMBALARE','DEZAMBALARE') GROUP BY 1,2 ORDER BY 1,2").replace('\n',','),flush=True)

