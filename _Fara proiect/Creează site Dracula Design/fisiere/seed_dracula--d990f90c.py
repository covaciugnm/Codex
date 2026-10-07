"""Idempotent first-install data. Does not reset edited products, pages or passwords."""
import json
import os
from pathlib import Path
from sqlalchemy import create_engine,text
from sqlalchemy.orm import Session
from app.config import get_settings
from app.seed import seed_admin_owner,ensure_host_map

def main():
    dsn=os.environ['SUPERUSER_DATABASE_URL'].replace('postgresql://','postgresql+psycopg://')
    content=json.loads((Path(__file__).parent/'dracula-content.json').read_text(encoding='utf-8'))
    engine=create_engine(dsn)
    with Session(engine) as session,session.begin():
        slug=os.environ.get('DEFAULT_TENANT','dracula-design')
        session.execute(text("INSERT INTO core.tenants(slug,display_name,status,default_locale,currency,active_theme_id) VALUES(:slug,'Dracula Design Office','active','ro','RON','dracula_exclusive') ON CONFLICT(slug) DO NOTHING"),{'slug':slug})
        tid=session.execute(text('SELECT id FROM core.tenants WHERE slug=:s'),{'s':slug}).scalar_one()
        for n,lang in enumerate(['ro','en','de']):
            session.execute(text('INSERT INTO core.tenant_locales(tenant_id,locale,is_enabled,position) VALUES(:t,:l,true,:n) ON CONFLICT DO NOTHING'),{'t':tid,'l':lang,'n':n})
        settings={'logo_asset':'/assets/brand/dracula-design-logo-auriu.jpeg','favicon_asset':'/assets/brand/dracula-design-logo-auriu.jpeg','primary_color':'#090909','accent_color':'#b89a64','logo_text':'Dracula Design','demo_prices':True,'theme_compare_public':False,'dracula_images':{'hero':'/assets/atmosfera/dracula-design-editorial-feminin.jpeg','collection':'/assets/colectii/dracula-design-colectie-business.jpeg','scarf':'/assets/produse/dracula-design-esarfa-signature.jpeg'},'onboarding':{'completed':False}}
        legal={'company_name':'Dracula-Company','address':'Dracula-Castel (Castelul-Dracula)','cui':'','registration':'','email':'','phone':'','website':'','iban':'','bank':''}
        seller={'legal_name':'Dracula-Company','public_name':'Dracula Design Office','address':legal['address']}
        shipping={'countries':['RO','DE'],'rules':[{'country':'RO','price_ron':25},{'country':'DE','price_ron':65}], 'delivery_methods':[{'code':'courier','label_key':'checkout.delivery.courier'}],'payment_methods':[{'code':'cash_on_delivery','label_key':'payment.cash_on_delivery'}]}
        session.execute(text('''INSERT INTO core.tenant_settings(tenant_id,settings,legal,seller,brand,tax,shipping_rules,allowed_themes)
          VALUES(:t,CAST(:settings AS jsonb),CAST(:legal AS jsonb),CAST(:seller AS jsonb),CAST(:brand AS jsonb),CAST(:tax AS jsonb),CAST(:shipping AS jsonb),ARRAY['dracula_exclusive']) ON CONFLICT DO NOTHING'''),{'t':tid,'settings':json.dumps(settings),'legal':json.dumps(legal),'seller':json.dumps(seller),'brand':json.dumps({'name':'Dracula Design','logo_url':settings['logo_asset']}),'tax':json.dumps({'vat_rate':0.21,'prices_include_vat':True,'requires_review':True}),'shipping':json.dumps(shipping)})
        cats={}
        for n,(code,names) in enumerate(content['categories']):
            session.execute(text('INSERT INTO catalog.categories(tenant_id,external_id,position) VALUES(:t,:code,:n) ON CONFLICT DO NOTHING'),{'t':tid,'code':code,'n':n})
            cid=session.execute(text('SELECT id FROM catalog.categories WHERE tenant_id=:t AND external_id=:c'),{'t':tid,'c':code}).scalar_one();cats[code]=cid
            for lang,name in names.items():session.execute(text('INSERT INTO catalog.category_translations(category_id,tenant_id,locale,name,slug) VALUES(:c,:t,:l,:n,:s) ON CONFLICT DO NOTHING'),{'c':cid,'t':tid,'l':lang,'n':name,'s':code})
        for p in content['products']:
            session.execute(text('''INSERT INTO catalog.products(tenant_id,external_id,sku,status,currency,price_ron,manage_stock,stock_quantity,is_in_stock,needs_price_review,primary_category_id)
              VALUES(:t,:ext,:sku,'published','RON',:price,true,20,true,true,:cat) ON CONFLICT DO NOTHING'''),{'t':tid,'ext':p['id'],'sku':p['sku'],'price':p['price'],'cat':cats[p['category']]})
            pid=session.execute(text('SELECT id FROM catalog.products WHERE tenant_id=:t AND external_id=:e'),{'t':tid,'e':p['id']}).scalar_one()
            for lang in ['ro','en','de']:
                session.execute(text('''INSERT INTO catalog.product_translations(product_id,tenant_id,locale,name,slug,short_description,description,seo_title,seo_description,translation_status)
                  VALUES(:p,:t,:l,:n,:s,:desc,:details,:seo,:desc,'manual') ON CONFLICT DO NOTHING'''),{'p':pid,'t':tid,'l':lang,'n':p['name'][lang],'s':p['id'],'desc':p['description'][lang],'details':p['details'][lang],'seo':p['name'][lang]+' — Dracula Design'})
            session.execute(text('INSERT INTO catalog.product_images(product_id,tenant_id,source_url,position,alt) VALUES(:p,:t,:u,0,CAST(:alt AS jsonb)) ON CONFLICT DO NOTHING'),{'p':pid,'t':tid,'u':'/assets/produse/dracula-design-'+p['image']+'.jpeg','alt':json.dumps(p['name'])})
            session.execute(text('INSERT INTO catalog.product_categories(product_id,category_id,tenant_id,is_primary) VALUES(:p,:c,:t,true) ON CONFLICT DO NOTHING'),{'p':pid,'c':cats[p['category']],'t':tid})
            for code in p.get('additional_categories',[]):
                session.execute(text('INSERT INTO catalog.product_categories(product_id,category_id,tenant_id,is_primary) VALUES(:p,:c,:t,false) ON CONFLICT DO NOTHING'),{'p':pid,'c':cats[code],'t':tid})
        for key,values in content['ui'].items():
            session.execute(text('INSERT INTO core.ui_translations(tenant_id,key,values) VALUES(:t,:k,CAST(:v AS jsonb)) ON CONFLICT DO NOTHING'),{'t':tid,'k':key,'v':json.dumps(values)})
        for n,page in enumerate(content['pages']):
            session.execute(text("INSERT INTO cms.legal_pages(tenant_id,slug,kind,position,status) VALUES(:t,:s,:k,:n,'published') ON CONFLICT DO NOTHING"),{'t':tid,'s':page['slug'],'k':page['kind'],'n':n})
            pid=session.execute(text('SELECT id FROM cms.legal_pages WHERE tenant_id=:t AND slug=:s'),{'t':tid,'s':page['slug']}).scalar_one()
            for lang in ['ro','en','de']:session.execute(text("INSERT INTO cms.legal_page_translations(legal_page_id,tenant_id,locale,title,body,translation_status) VALUES(:p,:t,:l,:title,:body,'manual') ON CONFLICT DO NOTHING"),{'p':pid,'t':tid,'l':lang,'title':page['title'][lang],'body':page['body'][lang]})
        seed_admin_owner(session)
        ensure_host_map(session,str(tid),slug)
    engine.dispose()
    print('Dracula seeded: 5 products, 14 pages, RO/EN/DE; existing data preserved.')

if __name__=='__main__':main()
