from pathlib import Path
import json,re

UI={
 'auth.verified':{'ro':'Adresa de email a fost confirmată.','en':'Your email address has been verified.','de':'Ihre E-Mail-Adresse wurde bestätigt.'},
 'product.preview':{'ro':'În pregătire','en':'Coming soon','de':'In Vorbereitung'},
 'product.preview_note':{'ro':'Descoperă conceptul. Acest produs este în pregătire și nu poate fi comandat încă.','en':'Discover the concept. This product is in preparation and cannot be ordered yet.','de':'Entdecken Sie das Konzept. Dieses Produkt ist in Vorbereitung und kann noch nicht bestellt werden.'},
 'product.dossier':{'ro':'Detalii. Poveste. Inspirație.','en':'Details. Story. Inspiration.','de':'Details. Geschichte. Inspiration.'},
 'collection.preview':{'ro':'Descoperă colecția în pregătire','en':'Discover the upcoming collection','de':'Die kommende Kollektion entdecken'},
 'collection.preview_intro':{'ro':'Colecția în pregătire. Imagini de prezentare și fișe documentate; specificațiile comerciale finale se confirmă înainte de vânzare.','en':'The upcoming collection. Presentation images and researched product dossiers; final commercial specifications are confirmed before sale.','de':'Die kommende Kollektion. Präsentationsbilder und recherchierte Produktdossiers; endgültige Verkaufsangaben werden vor dem Verkauf bestätigt.'},
}

PRODUCT='''function product(p){
 if(!p)return empty('error.not_found');
 const ready=!p.is_preview&&p.available>0;
 return `<section class="page product-detail"><div class="detail-photo"><button data-action="image" data-id="${p.id}" aria-label="${t('product.fullimage')}">${image(p,'',false)}</button></div><div class="detail-copy"><p class="eyebrow">${t('collection.eyebrow')}</p><h1>${esc(p.name)}</h1><p class="intro">${esc(p.description)}</p><div class="detail-price">${productPrice(p)}</div>${p.is_preview?`<p class="notice">${t('product.preview_note')}</p>`:`<p class="stock">${t(ready?'product.available':'product.unavailable')}</p><div class="purchase-row"><label>${t('product.quantity')}<input type="number" id="quantity" min="1" max="${p.available}" value="1"></label>${favourite(p)}</div><button class="button-primary" data-action="buy" data-id="${p.id}" ${ready?'':'disabled'}>${icon('buy')}${t('product.buy')}</button><button class="button-outline full" data-action="add" data-id="${p.id}" ${ready?'':'disabled'}>${icon('bag')}${t('product.add')}</button><p class="fineprint">${t('product.price_note')}</p>`}<p class="fineprint">${t('product.code')}: ${esc(p.sku)}</p><details><summary>${t('product.care')}</summary><p>${t('product.caretext')}</p></details><details><summary>${t('product.delivery')}</summary><p>${t('product.deliverytext')}</p>${link('/pages/returns',t('product.delivery'))}</details></div></section><section class="section product-dossier"><p class="eyebrow">${esc(p.sku)}</p><h2>${t('product.dossier')}</h2><div class="dossier-content">${rich(p.details)}</div></section><section class="section"><h2>${t('product.related')}</h2><div class="product-grid related">${state.data.products.filter(x=>x.id!==p.id).slice(0,3).map(card).join('')}</div></section>`;
}'''

for folder in ('dracula-design-office','dracula-food'):
 root=Path('outputs')/folder
 path=root/'backend/app/dracula.py';s=path.read_text(encoding='utf-8')
 s=s.replace('from .repositories.cms_repo import CmsRepo','from .repositories.cms_repo import CmsRepo\nfrom .commerce_readiness import database_readiness')
 s=s.replace("        locales=cfg['languages']", "        preview_available=demo() and bool(cfg.get('settings',{}).get('dracula_preview_drafts'))\n        preview_mode=preview_available and request.args.get('preview')=='1'\n        locales=cfg['languages']")
 s=s.replace('SELECT p.id,p.external_id,p.sku,p.price_ron','SELECT p.id,p.external_id,p.sku,p.status,p.price_ron')
 s=s.replace("WHERE p.tenant_id=:t AND p.status='published' ORDER BY p.sku'''),{'lang':locale,'base':default,'t':ctx.tenant_id}","WHERE p.tenant_id=:t AND (p.status='published' OR (:preview AND p.status='draft')) ORDER BY p.sku'''),{'lang':locale,'base':default,'t':ctx.tenant_id,'preview':preview_mode}")
 s=s.replace("dict(r,id=str(r['id']),price=", "dict(r,id=str(r['id']),is_preview=r['status']!='published',price=")
 s=s.replace("'images':cfg.get('settings',{}).get('dracula_images',{}),'demo':demo()", "'images':cfg.get('settings',{}).get('dracula_images',{}),'demo':demo(),'preview_available':preview_available,'preview_mode':preview_mode")
 s=s.replace("            if data.address.country not in allowed_countries(cfg)","            if not demo() and not database_readiness(ctx.session,ctx.tenant_id,cfg)['ready']:return jsonify({'error':'shop_not_ready'}),409\n            if data.address.country not in allowed_countries(cfg)")
 s=s.replace("if not demo() and not result['awaiting_payment']:","if (not demo() or os.environ.get('MAIL_CAPTURE_ONLY')=='true') and not result['awaiting_payment']:")
 path.write_text(s,encoding='utf-8')
 path=root/'backend/app/repositories/tenant_repo.py';s=path.read_text(encoding='utf-8')
 s=s.replace('return float((settings.get("tax") or {}).get("vat_rate") or 0.21)', 'value = (settings.get("tax") or {}).get("vat_rate")\n        return float(0.21 if value is None else value)')
 path.write_text(s,encoding='utf-8')
 path=root/'backend/public/shop.js';s=path.read_text(encoding='utf-8')
 s=s.replace("function card(p,index=0)","function productPath(p){return (p.is_preview?'/preview/product/':'/product/')+p.external_id;}\nfunction productPrice(p){return p.is_preview?t('product.preview'):money(p.price)+(state.data.demo?` <small>${t('demo.price')}</small>`:'');}\nfunction bootstrapPath(){return '/api/dracula/bootstrap'+(location.pathname.split('/').includes('preview')?'?preview=1':'');}\nfunction card(p,index=0)")
 s=s.replace("'/product/'+p.external_id",'productPath(p)')
 s=s.replace("(p.is_preview?'/preview/product/':productPath(p))", "(p.is_preview?'/preview/product/':'/product/')+p.external_id") if False else s
 s=s.replace("${money(p.price)} ${state.data.demo?`<small>${t('demo.price')}</small>`:''}","${productPrice(p)}")
 s=s.replace("${p.available<1?'disabled':''}","${p.is_preview||p.available<1?'disabled':''}")
 s=s.replace('class="icon-button ${saved(p)?\'selected\':\'\'}" data-action="favorite"', 'class="icon-button ${saved(p)?\'selected\':\'\'}" ${p.is_preview?\'disabled\':\'\'} data-action="favorite"')
 s=s.replace('return `<div class="collection-tools">', 'return `${state.data.preview_available&&!state.data.preview_mode?link(\'/preview\',t(\'collection.preview\')+\' ↗\',\'text-link preview-link\'):\'\'}<div class="collection-tools">')
 s=re.sub(r'^function product\(p\).*$',PRODUCT,s,flags=re.M)
 s=s.replace("else if(path==='/collection')", "else if(path==='/collection'||path==='/preview')")
 s=s.replace('${collection()}</section>`;else if(path.startsWith(\'/product/\'))body=product(state.data.products.find(p=>p.external_id===path.split(\'/\')[2]));', "${state.data.preview_mode?`<p class=\"notice\">${t('collection.preview_intro')}</p>`:''}${collection()}</section>`;else if(path.startsWith('/product/')||path.startsWith('/preview/product/'))body=product(state.data.products.find(p=>p.external_id===path.split('/').pop()));")
 s=s.replace("history.pushState({},'',path);await render();", "history.pushState({},'',path);if(Boolean(state.data.preview_mode)!==location.pathname.split('/').includes('preview')){state.data=await api(bootstrapPath());state.filter='all';}await render();")
 s=s.replace("api('/api/dracula/bootstrap')",'api(bootstrapPath())')
 s=s.replace("async function start(){try{const segment", "async function start(){try{const verificationUrl=new URL(location.href);const verificationToken=verificationUrl.pathname.endsWith('/account')?verificationUrl.searchParams.get('verify'):null;if(verificationToken){verificationUrl.searchParams.delete('verify');history.replaceState({},'',verificationUrl.pathname+verificationUrl.search+verificationUrl.hash);}const segment")
 s=s.replace("state.locale=state.data.locale;await refresh();await render();}catch", "state.locale=state.data.locale;await refresh();await render();if(verificationToken){try{await api('/api/account/verify-email','POST',{token:verificationToken});await refresh();await render();toast(state.data.ui['auth.verified']);}catch(error){toast(errorMessage(error));}}}catch")
 s=s.replace("'BLOCKQUOTE','A'", "'BLOCKQUOTE','A','SECTION','TABLE','THEAD','TBODY','TR','TH','TD','CAPTION'")
 path.write_text(s,encoding='utf-8')
 path=root/'backend/public/shop.css'
 s=path.read_text(encoding='utf-8')+'''\n.product-dossier{border-top:1px solid #33291f}.product-dossier>h2{margin:12px 0 45px}.dossier-content{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:45px 6%;color:#c1b5a3;font-size:14px;line-height:1.85}.dossier-content>section{min-width:0;border-top:1px solid #33291f;padding-top:25px}.dossier-content>section:last-child{grid-column:1/-1}.dossier-content h3{font-size:27px;color:#d7c39e;margin:0 0 20px}.dossier-content h4{font-size:20px;color:#d7c39e}.dossier-content p{margin:14px 0}.dossier-content ul,.dossier-content ol{padding-left:20px}.dossier-content a{color:#c9ab72;text-decoration:underline;overflow-wrap:anywhere}.dossier-content table{width:100%;border-collapse:collapse;font-size:13px}.dossier-content th,.dossier-content td{padding:11px 8px;border-bottom:1px solid #33291f;text-align:left;vertical-align:top;overflow-wrap:anywhere}.dossier-content th{font-weight:400;color:#d7c39e;width:42%}.preview-link{display:inline-block;margin:20px 0}.product-dossier li{margin-bottom:10px}@media(max-width:700px){.dossier-content{grid-template-columns:minmax(0,1fr);gap:30px}.dossier-content>section:last-child{grid-column:auto}.product-dossier{padding:40px 6%}.dossier-content table{font-size:12px}}\n'''
 path.write_text(s,encoding='utf-8')
 path=root/'backend/dracula-content.json';d=json.loads(path.read_text(encoding='utf-8'));d['ui'].update(UI);path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (root/'backend/stage_ui.json').write_text(json.dumps(UI,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Stage integration prepared for both storefronts.')
