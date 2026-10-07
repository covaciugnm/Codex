import json,re
from pathlib import Path
root=Path('outputs/dracula-design-office')
path=root/'backend/dracula-content.json'
data=json.loads(path.read_text(encoding='utf-8'))
new=[['haine',{'ro':'Haine','en':'Clothing','de':'Bekleidung'}],['accesorii',{'ro':'Accesorii','en':'Accessories','de':'Accessoires'}]]
data['categories']=[['business',{'ro':'Business','en':'Business','de':'Business'}],['everyday',{'ro':'Esențiale','en':'Essentials','de':'Essentials'}],['women',{'ro':'Feminin','en':'Women','de':'Damen'}]]+new
for p in data['products']: p['additional_categories']=['accesorii']
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=root/'backend/seed_dracula.py'
seed=path.read_text(encoding='utf-8')
seed=re.sub(r"for n,\(code,names\) in enumerate\(\[.*?\]\):", "for n,(code,names) in enumerate(content['categories']):", seed)
needle="            session.execute(text('INSERT INTO catalog.product_categories(product_id,category_id,tenant_id,is_primary) VALUES(:p,:c,:t,true) ON CONFLICT DO NOTHING'),{'p':pid,'c':cats[p['category']],'t':tid})"
assert needle in seed
seed=seed.replace(needle,needle+"\n            for code in p.get('additional_categories',[]):\n                session.execute(text('INSERT INTO catalog.product_categories(product_id,category_id,tenant_id,is_primary) VALUES(:p,:c,:t,false) ON CONFLICT DO NOTHING'),{'p':pid,'c':cats[code],'t':tid})")
path.write_text(seed,encoding='utf-8')

sql=['BEGIN;']
def q(s): return "'"+s.replace("'","''")+"'"
for pos,(code,names) in enumerate(new,start=3):
    sql.append(f"INSERT INTO catalog.categories(tenant_id,external_id,position) SELECT id,{q(code)},{pos} FROM core.tenants WHERE slug='dracula-design' ON CONFLICT DO NOTHING;")
    for lang,name in names.items():
        sql.append(f"INSERT INTO catalog.category_translations(category_id,tenant_id,locale,name,slug) SELECT c.id,c.tenant_id,{q(lang)},{q(name)},{q(code)} FROM catalog.categories c JOIN core.tenants t ON t.id=c.tenant_id WHERE t.slug='dracula-design' AND c.external_id={q(code)} ON CONFLICT DO NOTHING;")
ids=','.join(q(p['id']) for p in data['products'])
sql.append(f"INSERT INTO catalog.product_categories(product_id,category_id,tenant_id,is_primary) SELECT p.id,c.id,t.id,false FROM core.tenants t JOIN catalog.products p ON p.tenant_id=t.id JOIN catalog.categories c ON c.tenant_id=t.id AND c.external_id='accesorii' WHERE t.slug='dracula-design' AND p.external_id IN ({ids}) ON CONFLICT DO NOTHING;")
sql.append('COMMIT;')
(root/'backend/apply_design_categories.sql').write_text('\n'.join(sql)+'\n',encoding='utf-8')

for folder in (root,Path('outputs/dracula-food')):
    path=folder/'backend/app/dracula.py'
    source=path.read_text(encoding='utf-8')
    needle='(SELECT external_id FROM catalog.categories c WHERE c.id=p.primary_category_id) category'
    assert needle in source
    source=source.replace(needle,needle+",\n          ARRAY(SELECT c.external_id FROM catalog.product_categories pc JOIN catalog.categories c ON c.id=pc.category_id WHERE pc.product_id=p.id) categories")
    path.write_text(source,encoding='utf-8')
    path=folder/'backend/public/shop.js'
    source=path.read_text(encoding='utf-8')
    source=source.replace("p.category===state.filter)","p.category===state.filter||p.categories?.includes(state.filter))")
    path.write_text(source,encoding='utf-8')
    path=folder/'backend/public/shop.css'
    source=path.read_text(encoding='utf-8')
    path.write_text(source+'\n/* Keep long translated headings inside narrow screens. */\n.page h1 { overflow-wrap: anywhere; }\n',encoding='utf-8')
print('Design categories, accessory membership, shared filters and responsive headings prepared.')
