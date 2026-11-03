from pathlib import Path
import json

base = Path('D:/CodexWork')
source = (base / 'p01-r11-original-suites-v10.py').read_text(encoding='utf-8-sig')
source = source.replace('Suite_originale_API_portal_v10', 'Suite_originale_config_sintetice_v11')
source = source.replace("back=['t58_close_month']", 'back=[]')
source = source.replace('front=[]', "front=['event_theme_admin','storefront_admin_i18n']")
source = source.replace('stores=[]', "stores=['event_themes','seasonal_themes','audit_regressions']")
source = source.replace("prefix='p01-r11-tests-v10-'", "prefix='p01-r11-config-v11-'")
source = source.replace(";shutil.copytree(base/'frontend',fixture/'frontend')", '')
needle = "  ev={k:os.environ[k]"
fixture = '''  # Configuration is synthetic; theme metadata comes from verified Git manifests.
  portal = fixture/'frontend'
  shop = portal/'storefront'
  project_index = rd(shop/'themes/theme-projects.json')
  themes = [rd(shop/item['manifest']) for item in project_index['projects']]
  langs = ['ro','en','de','hu','bg','el']
  def write_json(relative, value):
   target = portal/relative
   target.parent.mkdir(parents=True, exist_ok=True)
   target.write_text(json.dumps(value, ensure_ascii=False), encoding='utf8')
  labels = lambda value: {lang:value+' '+lang for lang in langs}
  site = {'id':'cesiro1','tenant_slug':'cesiro1','seller_tenant_cui':'AUDIT001',
          'cabinet_cui':'AUDIT001','domain':'cesiro1.example.invalid',
          'brand_name':'Audit synthetic','status':'active','active_theme':'marketplace_pro',
          'allowed_themes':[item['id'] for item in themes],
          'languages':langs,'default_language':'ro','currency':'RON'}
  write_json('data/storefront_sites.json', {'sites':[site],'active_by_user':{},'themes':themes})
  write_json('storefront/data/theme_registry.json', {'themes':themes})
  config = dict(site, tenant='cesiro1', settings={'logo_text':'AUDIT'},
                seller={'public_name':'Audit synthetic','legal_name':'Audit synthetic','cui':'AUDIT001'})
  write_json('storefront/data/tenants/cesiro1/storefront.json', config)
  product = {'id':'audit-primary-01','sku':'AUDIT-SKU-01','ean':'AUDIT-EAN-01',
             'name':labels('Produs sintetic'),'slug':labels('produs-sintetic'),
             'description':labels('Descriere sintetica'),'price':12.5,'price_ron':12.5,
             'currency':'RON','stock_quantity':3,'is_in_stock':True,
             'categories':['Audit'],'category_ids':['audit-category'],'images':[]}
  catalog = {'categories':[{'id':'audit-category','name':labels('Audit'),'slug':labels('audit')}],
             'collections':[],'products':[product]}
  write_json('storefront/data/tenants/cesiro1/catalog.json', catalog)
  write_json('storefront/data/tenants/cesiro1/translations.json', {})
  write_json('storefront/data/tenants/cesiro1/legal_pages.json',
             {'pages':[{'slug':'audit-legal','title':labels('Conditii sintetice'),
                        'content':labels('Text de laborator')}]})
  fixture_sources = []
  for f in sorted(portal.rglob('*.json')):
   if '/data/' in f.as_posix():
    fixture_sources.append({'file':f.relative_to(fixture).as_posix(),'sha256':h(f.read_bytes())})
'''
assert source.count(needle) == 1
source = source.replace(needle, fixture + needle)
source = source.replace("'source_sha256':h(src.read_bytes()),'git_blob':oid(src.read_bytes())", "'source_sha256':h(src.read_bytes()),'git_blob':oid(src.read_bytes()),'synthetic_fixture_files':fixture_sources")
source = source.replace("'origin':'original Git test suites", "'synthetic_config_scope':'Theme metadata copied from exact Git manifests; site/catalog/legal text synthetic; translation content, operational config and native ERP are not certified. Runtime files and original assertions unchanged.', 'origin':'original Git test suites")
(base / 'p01-r11-original-config-v11.py').write_text(source, encoding='utf8')
print('Created configuration wave runner; original source/tests unchanged.')
