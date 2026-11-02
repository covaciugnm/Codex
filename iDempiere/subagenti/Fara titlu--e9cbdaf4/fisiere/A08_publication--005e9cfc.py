import pathlib,json,hashlib
O=pathlib.Path(__file__).parent;E=O.parent
h=(E/'A11_reproduceri_lot2/store.py').read_text(encoding='utf8');head=h.split(" result={'time'")[0]
actions="""
 outc=[]
 for ver in [3,5,4,4,8]:
  body={'version':ver,'products':[{'id':'v-z','sku':'a11-check','name':{'ro':f'A11v{ver}'},'slug':{'ro':'a11'},'price_ron':16}]}
  cb=cat.read_bytes();rb=app.test_client().post('/admin/api/tenants/a11b/import/json',base_url='https://cesiro1.eva-contab.ro',json=body);bf=other/'catalog.json';bval=rd(bf);outc.append((ver,rb.status_code,bval['products'][0]['name']['ro'],hashlib.sha256(bf.read_bytes()).hexdigest(),cat.read_bytes()==cb))
 assert [x[2] for x in outc]==['A11v3','A11v5','A11v4','A11v4','A11v8'] and all(x[1]==200 and x[4] for x in outc)
 wr(O/'A08_catalog_sequence.json',{'fixture':'Pinned Flask storefront, two distinct tenants, ephemeral files, network blocked. No external CESIRO1 checkout or production HTTP.','sent_versions':[3,5,4,4,8],'observations':outc,'external_attempts':calls})
 print(outc)
"""
exec(compile(head+actions,'A11_zero_egress_storefront','exec'))

