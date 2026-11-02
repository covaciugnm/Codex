import pathlib
w=pathlib.Path('/tmp/codex-a05.ObWQES');exec((w/'fixture.py').read_text().split('if __name__')[0])
tok=auth('GardenAdmin','GardenAdmin',11,102,11)
s,b=request('GET','models/M_Product/123',token=tok);assert s==200
ref=lambda val: val.get('id') if isinstance(val,dict) else val
f={'M_Product_Category_ID':ref(b['M_Product_Category_ID']),'C_TaxCategory_ID':ref(b['C_TaxCategory_ID']),'C_UOM_ID':ref(b['C_UOM_ID']),'ProductType':'I','IsStocked':True,'IsActive':True,'AD_Org_ID':11}
def create(value,name):
    s,j=request('POST','models/M_Product',dict(f,Value=value,Name=name),tok)
    print('create',value,'HTTP',s,'id',j.get('id'),'detail',str(j.get('detail',''))[:160]);return s,j.get('id')
code,first=create('A05-CPP-0001','A05 CPP primary');assert code in (200,201)
code,cpa=create('A05-CPA-0001','A05 CPA packaged');assert code in (200,201)
s,j=request('PUT','models/M_Product/'+str(first),{'IsActive':False},tok);print('deactivate',s)
code,duplicate=create('A05-CPP-0001','New product duplicate current value');assert code not in (200,201)
s,j=request('PUT','models/M_Product/'+str(first),{'Value':'A05-ARCHIVED-0001'},tok);print('rename original',s,j.get('id'),j.get('detail',''))
code,second=create('A05-CPP-0001','A05 different product with old value');print('old value reused on different id?',code in (200,201) and first!=second)

