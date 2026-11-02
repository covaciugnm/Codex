import pathlib,concurrent.futures,threading
w=pathlib.Path('/tmp/codex-a05.ObWQES');exec((w/'fixture.py').read_text().split('if __name__')[0])
tok=auth('GardenAdmin','GardenAdmin',11,102,11)
code,line=request('POST','models/M_InventoryLine',{'AD_Org_ID':11,'M_Inventory_ID':1000000,'M_Product_ID':123,'M_Locator_ID':101,'QtyBook':20,'QtyCount':18,'Line':10},tok)
print('create line',code,'id',line.get('id'),'quantity',line.get('QtyCount'),'problem',line.get('detail'))
assert code in (200,201);barrier=threading.Barrier(2)
def complete(which):
    barrier.wait(timeout=5)
    c,d=request('PUT','models/M_Inventory/1000000',{'doc-action':'CO'},tok)
    print('concurrent completion',which,'HTTP',c,'docStatus',d.get('DocStatus'),'detail',d.get('detail',d.get('message','')))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
    list(ex.map(complete,[1,2]))
c,d=request('GET','models/M_Inventory/1000000',token=tok);print('readback',c,'docStatus',d.get('DocStatus'),'Processed',d.get('Processed'),'Posted',d.get('Posted'))

