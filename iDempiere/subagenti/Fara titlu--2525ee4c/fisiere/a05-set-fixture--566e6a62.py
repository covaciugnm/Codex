import pathlib,json
w=pathlib.Path('/tmp/codex-a05.ObWQES');exec((w/'fixture.py').read_text().split('if __name__')[0]);tok=auth('GardenAdmin','GardenAdmin',11,102,11)
def post(table,body):
    s,j=request('POST','models/'+table,body,tok)
    print(table,'status',s,'id',j.get('id'),'detail',str(j.get('detail',j.get('message','')))[:250]);assert s in (200,201),(s,j.get('detail'))
    return j['id']
s,p=request('GET','models/M_Product/123',token=tok);assert s==200
ref=lambda v:v.get('id') if isinstance(v,dict) else v
setid=post('M_Product',{'AD_Org_ID':11,'M_Product_Category_ID':ref(p['M_Product_Category_ID']),'C_TaxCategory_ID':ref(p['C_TaxCategory_ID']),'C_UOM_ID':ref(p['C_UOM_ID']),'ProductType':'I','Value':'A05-S1','Name':'A05 S1 reversible WMS fixture','IsStocked':False,'IsBOM':True})
bom=post('PP_Product_BOM',{'AD_Org_ID':11,'M_Product_ID':setid,'Name':'A05 S1 formula','Value':'A05-S1-B1','BOMType':'A','BOMUse':'A','C_UOM_ID':ref(p['C_UOM_ID'])})
for i,raw in enumerate((123,124,125),1):
    post('PP_Product_BOMLine',{'AD_Org_ID':11,'PP_Product_BOM_ID':bom,'M_Product_ID':raw,'C_UOM_ID':ref(p['C_UOM_ID']),'QtyBOM':6,'Line':i*10,'ComponentType':'CO'})
(w/'bom.json').write_text(json.dumps({'set':setid,'bom':bom}))

