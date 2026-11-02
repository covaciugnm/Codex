import pathlib,json,urllib.request,urllib.error,subprocess,time
w=pathlib.Path('/tmp/codex-a05.ObWQES');exec((w/'fixture.py').read_text().split('if __name__')[0]);token=auth('GardenAdmin','GardenAdmin',11,102,11)
pg=(w/'auditor-pg').read_text().strip();assert pg.startswith('eva-test-p01-t355-auditor-pg-')
def sql(q):
    assert q.startswith('SELECT')
    return subprocess.run(['docker','exec',pg,'psql','-U','postgres','-d','idempiere','-X','-Atc',q],capture_output=True,text=True,check=True).stdout.strip()
def nonce_request(tag,typ,key):
    body={'M_Warehouse_ID':103,'EVA_TipNota':typ,'M_Product_ID':1000004,'Qty':1,'M_Locator_ID':1000002,'PP_Product_BOM_ID':1000000}
    r=urllib.request.Request('https://'+ip+':8443/api/v1/processes/eva_notasetwms',data=json.dumps(body).encode(),method='POST',headers={'Content-Type':'application/json','Accept':'application/json','Authorization':'Bearer '+token,'Idempotency-Key':key})
    try:
        with op.open(r,timeout=45) as f:c=f.status;j=json.load(f)
    except urllib.error.HTTPError as e:
        c=e.code
        try:j=json.load(e)
        except Exception:j={}
    print(tag,c,j.get('AD_PInstance_ID',j.get('id')),j.get('summary',j.get('detail','')))
    print('set balance:',sql('SELECT coalesce(sum(qty),0) FROM adempiere.eva_stocwms WHERE ad_client_id=11 AND m_warehouse_id=1000000 AND m_product_id=1000004'))
    return c
assert sql('SELECT coalesce(sum(qty),0)::integer FROM adempiere.eva_stocwms WHERE ad_client_id=11 AND m_warehouse_id=1000000 AND m_product_id=1000004')=='1'
nonce_request('independent assembly (real operation)',1,'a05-new-pack-3')
nonce_request('disassembly A accepted',2,'a05-disassembly-same-key')
nonce_request('disassembly A retry after commit',2,'a05-disassembly-same-key')

