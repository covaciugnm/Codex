"""Dracula storefront API on the existing CESIRO admin and PostgreSQL model."""
import hashlib
import json
import os
import re
import time
from collections import defaultdict, deque
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory, make_response
from sqlalchemy import text
from pydantic import Field, ValidationError
from .config import get_settings
from .db import session_scope, set_session_context
from .repositories.tenant_repo import get_tenant_id, get_tenant_settings, delivery_methods, payment_methods, delivery_price, allowed_countries
from .repositories import CartRepo, SalesRepo, OutOfStock, PriceChanged
from .repositories.cms_repo import CmsRepo
from .commerce_readiness import database_readiness
from .api import storefront as sf
from .api.checkout_schemas import CheckoutIn
from .api.admin import admin_bp
from .api.admin.deps import require_role, tenant_db
from .api.errors import ApiError
from .api import register_error_handlers

ROOT=Path(__file__).resolve().parents[1]
HITS=defaultdict(deque)

class DraculaCheckoutIn(CheckoutIn):
    expected_total_ron: float = Field(ge=0, allow_inf_nan=False, strict=True)


def demo():
    return os.environ.get('COMMERCE_MODE','demo') != 'live'

def context():
    return sf._open_ctx()

def load_bootstrap(locale=None):
    scope,ctx=context()
    try:
        cfg=get_tenant_settings(ctx.session,ctx.tenant_id)
        preview_available=demo() and bool(cfg.get('settings',{}).get('dracula_preview_drafts'))
        preview_mode=preview_available and request.args.get('preview')=='1'
        locales=cfg['languages']
        default=cfg['default_language']
        locale=locale if locale in locales else default
        cms=CmsRepo(ctx.session,ctx.tenant_id)
        translations=cms.ui_translations()
        ui={key:(v.get(locale) or v.get(default) or v.get('en') or key) for key,v in translations.items() if not key.startswith('admin.')}
        rows=ctx.session.execute(text('''SELECT p.id,p.external_id,p.sku,p.status,p.price_ron,p.stock_quantity,p.stock_reserved,p.is_in_stock,
          COALESCE(NULLIF(tr.name,''),base.name) name,COALESCE(NULLIF(tr.slug,''),base.slug) slug,
          COALESCE(NULLIF(tr.short_description,''),base.short_description) description,
          COALESCE(NULLIF(tr.description,''),base.description) details,
          (SELECT source_url FROM catalog.product_images i WHERE i.product_id=p.id ORDER BY position LIMIT 1) image,
          (SELECT external_id FROM catalog.categories c WHERE c.id=p.primary_category_id AND c.is_active) category,
          ARRAY(SELECT c.external_id FROM catalog.product_categories pc JOIN catalog.categories c ON c.id=pc.category_id WHERE pc.product_id=p.id AND c.is_active) categories
          FROM catalog.products p LEFT JOIN catalog.product_translations tr ON tr.product_id=p.id AND tr.locale=:lang
          LEFT JOIN catalog.product_translations base ON base.product_id=p.id AND base.locale=:base
          WHERE p.tenant_id=:t AND (p.status='published' OR (:preview AND p.status='draft')) ORDER BY p.sku'''),{'lang':locale,'base':default,'t':ctx.tenant_id,'preview':preview_mode}).mappings()
        products=[dict(r,id=str(r['id']),is_preview=r['status']!='published',price=float(r['price_ron']),available=max(0,r['stock_quantity']-r['stock_reserved'])) for r in rows]
        categories=ctx.session.execute(text('''SELECT c.external_id code,COALESCE(tr.name,base.name,c.external_id) name FROM catalog.categories c
          LEFT JOIN catalog.category_translations tr ON tr.category_id=c.id AND tr.locale=:lang
          LEFT JOIN catalog.category_translations base ON base.category_id=c.id AND base.locale=:base
          WHERE c.tenant_id=:t AND c.is_active ORDER BY c.position'''),{'lang':locale,'base':default,'t':ctx.tenant_id}).mappings().all()
        pages=[]
        variables={**cfg.get('legal',{}),**cfg.get('seller',{}),'company_name':cfg.get('legal',{}).get('company_name',''),'address':cfg.get('legal',{}).get('address','')}
        def interpolate(value):
            return re.sub(r'\{\{([a-z_]+)\}\}',lambda m:str(variables.get(m[1]) or ui.get('legal.pending','—')),value or '')
        for page in cms.legal_pages():
            pages.append({'slug':page['slug'],'kind':page['kind'],'title':page['title'].get(locale) or page['title'].get(default),'body':interpolate(page['body'].get(locale) or page['body'].get(default))})
        return {'locale':locale,'languages':locales,'defaultLocale':default,'ui':ui,'products':products,'pages':pages,'categories':[dict(c) for c in categories],
          'brand':cfg['brand'],'seller':cfg['seller'],'legal':cfg['legal'],'currency':cfg['currency'],
          'images':cfg.get('settings',{}).get('dracula_images',{}),'demo':demo(),'preview_available':preview_available,'preview_mode':preview_mode,'countries':allowed_countries(cfg),
          'shipping':cfg.get('shipping_rules',{}),'payments':payment_methods(cfg)}
    finally:
        sf._close_ctx(scope)

@admin_bp.get('/dracula/inquiries')
@require_role('viewer')
def inquiries_admin():
    with tenant_db() as (session,tid,_):
        rows=session.execute(text('SELECT id,kind,name,email,body,locale,status,created_at FROM cms.dracula_inquiries WHERE tenant_id=:t ORDER BY created_at DESC LIMIT 200'),{'t':tid}).mappings()
        return jsonify({'items':[dict(r,id=str(r['id']),created_at=r['created_at'].isoformat()) for r in rows]})

@admin_bp.patch('/dracula/inquiries/<uuid:inquiry_id>')
@require_role('editor')
def inquiry_update(inquiry_id):
    status=(request.get_json(silent=True) or {}).get('status')
    if status not in ('new','in_progress','closed'):raise ApiError('Invalid status',code='validation_failed',status=400)
    with tenant_db('editor') as (session,tid,_):
        result=session.execute(text('UPDATE cms.dracula_inquiries SET status=:s WHERE id=:id AND tenant_id=:t'),{'s':status,'id':inquiry_id,'t':tid})
        if not result.rowcount:raise ApiError('Not found',code='not_found',status=404)
    return jsonify({'status':'ok'})

def create_app():
    app=Flask(__name__,static_folder=str(ROOT/'public'),static_url_path='/assets-unused')
    app.secret_key=os.environ['SECRET_KEY']
    app.config['MAX_CONTENT_LENGTH']=64*1024*1024
    app.config['JSON_AS_ASCII']=False
    from .factory import _register_admin_api
    _register_admin_api(app)
    sf.register_storefront_api(app)
    register_error_handlers(app,prefixes=('/api/',))

    @app.before_request
    def safeguards():
        if request.method in ('POST','PUT','PATCH','DELETE') and request.path != '/api/payments/stripe/webhook':
            origin=request.headers.get('Origin')
            if origin and origin.rstrip('/') != request.host_url.rstrip('/') and origin.rstrip('/') != os.environ.get('PUBLIC_BASE_URL','').rstrip('/'):
                return jsonify({'error':'origin_rejected'}),403
        if request.path.startswith('/api/account/') and request.method=='POST' or request.path=='/api/dracula/inquiry':
            key=(request.remote_addr,request.path)
            now=time.monotonic();hits=HITS[key]
            while hits and hits[0]<now-300:hits.popleft()
            if len(hits)>=30:return jsonify({'error':'rate_limited'}),429
            hits.append(now)
        if request.path=='/api/payments/stripe/session' and demo():
            return jsonify({'error':'demo_payment_disabled'}),409

    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['Referrer-Policy']='same-origin'
        response.headers['X-Frame-Options']='SAMEORIGIN'
        if request.path.startswith('/api/'):
            response.headers['Cache-Control']='no-store'
        return response

    @app.get('/health')
    def health():
        with session_scope() as session:session.execute(text('SELECT 1'))
        return jsonify({'status':'ok','store':get_settings().default_tenant,'demo':demo()})

    @app.get('/api/dracula/bootstrap')
    def bootstrap():
        return jsonify(load_bootstrap(request.args.get('lang')))

    @app.get('/api/dracula/admin-content')
    def admin_content():
        scope,ctx=context()
        try:
            return jsonify({key[6:]:values for key,values in CmsRepo(ctx.session,ctx.tenant_id).ui_translations().items() if key.startswith('admin.')})
        finally:sf._close_ctx(scope)

    app.add_url_rule('/api/account/login','customer_login',sf.login_customer,methods=['POST'])
    app.add_url_rule('/api/account/change-password','customer_password',sf.change_password,methods=['POST'])
    app.add_url_rule('/api/account/returns','customer_return_create',sf.create_return,methods=['POST'])

    @app.post('/api/orders')
    def place_order():
        if not demo() and os.environ.get('COMMERCE_READY')!='true':
            return jsonify({'error':'shop_not_ready'}),409
        raw=request.get_json(silent=True) or {}
        try:data=DraculaCheckoutIn.model_validate(raw)
        except ValidationError:return jsonify({'error':'validation_failed'}),400
        request_key=request.headers.get('Idempotency-Key','')
        if not re.fullmatch(r'[a-zA-Z0-9_-]{16,100}',request_key):return jsonify({'error':'idempotency_required'}),400
        fingerprint=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        try:scope,ctx=sf._open_ctx(require_user=True)
        except PermissionError:return jsonify({'error':'login_required'}),401
        try:
            ctx.session.execute(text('SELECT pg_advisory_xact_lock(hashtextextended(:key,0))'),{'key':ctx.user_id+request_key})
            existing=ctx.session.execute(text('SELECT request_hash,result FROM sales.dracula_checkout_requests WHERE tenant_id=:t AND user_id=:u AND request_key=:k'),{'t':ctx.tenant_id,'u':ctx.user_id,'k':request_key}).first()
            if existing:
                if existing.request_hash!=fingerprint:return jsonify({'error':'idempotency_conflict'}),409
                return jsonify(existing.result)
            cfg=get_tenant_settings(ctx.session,ctx.tenant_id)
            if not demo() and not database_readiness(ctx.session,ctx.tenant_id,cfg)['ready']:return jsonify({'error':'shop_not_ready'}),409
            if data.address.country not in allowed_countries(cfg):return jsonify({'error':'invalid_country'}),400
            if data.payment_method not in {m['code'] for m in payment_methods(cfg)}:return jsonify({'error':'invalid_payment_method'}),400
            if data.delivery_method not in {m['code'] for m in delivery_methods(cfg,data.address.country)}:return jsonify({'error':'invalid_delivery_method'}),400
            if demo() and data.payment_method=='card':return jsonify({'error':'demo_payment_disabled'}),409
            cart=CartRepo(ctx.session,ctx.tenant_id,ctx.tenant_slug)
            cart_id=cart.find_open(user_id=ctx.user_id,token_hash=None)
            if not cart_id:return jsonify({'error':'empty_cart'}),400
            locked=ctx.session.execute(text('SELECT id FROM sales.carts WHERE id=:id AND status=\'open\' FOR UPDATE'),{'id':cart_id}).first()
            if not locked:return jsonify({'error':'empty_cart'}),409
            cart_data=sf._cart_payload(ctx,str(cart_id),sf._locale())
            if not cart_data['items']:return jsonify({'error':'empty_cart'}),400
            expected=data.expected_total_ron
            shipping=delivery_price(cfg,data.delivery_method,data.address.country,cart_data['products_gross_ron'])
            if expected is None or abs(float(expected)-(cart_data['products_gross_ron']+shipping))>=0.01:return jsonify({'error':'price_changed'}),409
            shipping_address=data.address.as_dict()
            customer={'name':data.customer.full_name,'first_name':data.customer.first_name,'last_name':data.customer.last_name,'email':data.customer.email,'phone':data.customer.phone,'country':data.address.country,'address':data.address.as_text(),'customer_type':'individual'}
            order=SalesRepo(ctx.session,ctx.tenant_id).create_order(lines=[{'product_id':i['product_id'],'qty':i['qty'],'expected_price':i['unit_price_gross_ron']} for i in cart_data['items']],customer=customer,shipping_address=shipping_address,billing_address=(data.billing_address or data.address).as_dict(),payment_method=data.payment_method,settings=cfg,user_id=ctx.user_id,locale=sf._locale(),cart_id=str(cart_id),seller=cfg.get('seller'),delivery_method=data.delivery_method,shipping_override=shipping,accepted_terms=True,user_comments=data.notes,is_guest_order=False)
            ctx.session.execute(text('UPDATE sales.orders SET is_test=:demo WHERE id=:id'),{'demo':demo(),'id':order['order_id']})
            result={'status':'ok','order_number':order['order_number'],'order_id':order['order_id'],'awaiting_payment':order.get('status')=='pending_payment','demo':demo()}
            ctx.session.execute(text('INSERT INTO sales.dracula_checkout_requests(tenant_id,user_id,request_key,request_hash,result) VALUES(:t,:u,:k,:h,CAST(:r AS jsonb))'),{'t':ctx.tenant_id,'u':ctx.user_id,'k':request_key,'h':fingerprint,'r':json.dumps(result)})
            if (not demo() or os.environ.get('MAIL_CAPTURE_ONLY')=='true') and not result['awaiting_payment']:
                from .mail import notify
                notify.order_placed(ctx.session,tenant_id=ctx.tenant_id,order=order,customer=customer,shipping=shipping_address,billing=(data.billing_address or data.address).as_dict(),locale=sf._locale(),order_id=order['order_id'],user_id=ctx.user_id)
        except (OutOfStock,PriceChanged) as exc:
            ctx.session.rollback();return jsonify({'error':str(exc)}),409
        except ValueError as exc:
            ctx.session.rollback();return jsonify({'error':str(exc)}),400
        finally:sf._close_ctx(scope)
        return jsonify(result),201

    @app.post('/api/dracula/inquiry')
    def inquiry():
        data=request.get_json(silent=True) or {}
        if not isinstance(data,dict) or any(not isinstance(data.get(key),str) for key in ('email','name','body','kind')):return jsonify({'error':'validation_failed'}),400
        if data.get('website'):return jsonify({'error':'validation_failed'}),400
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',str(data.get('email',''))) or not 2<=len(str(data.get('name','')))<=150 or not 10<=len(str(data.get('body','')))<=5000 or data.get('kind') not in ('contact','complaint','withdrawal','privacy'):
            return jsonify({'error':'validation_failed'}),400
        scope,ctx=context()
        try:
            ctx.session.execute(text('INSERT INTO cms.dracula_inquiries(tenant_id,user_id,kind,name,email,body,locale) VALUES(:t,:u,:kind,:name,:email,:body,:locale)'),{'t':ctx.tenant_id,'u':ctx.user_id,'kind':data['kind'],'name':data['name'],'email':data['email'],'body':data['body'],'locale':sf._locale()})
        finally:sf._close_ctx(scope)
        return jsonify({'status':'received'}),201

    @app.get('/assets/<path:filename>')
    def assets(filename):return send_from_directory(ROOT/'public/assets',filename)

    @app.get('/media/brand/<tenant>/<filename>')
    def brand_media(tenant,filename):
        if tenant!=get_settings().default_tenant:return jsonify({'error':'not_found'}),404
        return send_from_directory(ROOT/'data/tenants'/tenant/'brand',filename)

    @app.get('/media/<tenant>/<path:filename>')
    def uploaded_media(tenant,filename):
        if tenant!=get_settings().default_tenant:return jsonify({'error':'not_found'}),404
        return send_from_directory(ROOT/'data/media'/tenant,filename)

    @app.get('/<path:route>')
    @app.get('/')
    def storefront(route=''):
        if route in ('shop.js','shop.css','styles.css'):return send_from_directory(ROOT/'public',route)
        if route.startswith(('api/','admin/')):return jsonify({'error':'not_found'}),404
        return send_from_directory(ROOT/'public','index.html')

    return app
