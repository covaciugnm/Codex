"""API-ul public al magazinului, pe PostgreSQL.

Rute NOI (path-uri care nu existau): coșul persistent și înregistrarea de cont.
Rutele vechi (`/api/orders`, `/api/account/*`) își păstrează path-ul și forma
răspunsului; sunt deservite din `factory.py`, care delegă aici când
`STORAGE_BACKEND=postgres`.

Contractul implementat de storefront.js (P3) — `scratchpad/p3_storefront_diff.md`:
  GET    /api/cart
  POST   /api/cart/sync      {items:[{product_id, qty}]}
  POST   /api/cart/items     {product_id, qty}
  PATCH  /api/cart/items/<product_id>   {qty}   (qty=0 = ștergere)
  DELETE /api/cart/items/<product_id>
  POST   /api/cart/merge
  POST   /api/account/register
"""
from __future__ import annotations

import hashlib
import logging
import os
import re
import secrets
import sys
import time
from typing import Any

from urllib.parse import quote

from flask import Blueprint, jsonify, make_response, request
from sqlalchemy import text

from .. import currency_rates
from ..config import get_settings
from ..db import session_scope
from ..repositories import CartRepo, IdentityRepo, OutOfStock, PriceChanged, SalesRepo
from ..repositories.cart_repo import hash_cart_token, new_cart_token
from ..repositories.identity_repo import (compose_address, normalize_email,
                                           valid_email)
from ..repositories.tenant_repo import (
    allowed_countries,
    delivery_methods,
    delivery_price,
    get_tenant_id,
    get_tenant_settings,
    payment_methods,
    shipping_for_country,
    vat_rate,
)
from .checkout_schemas import CheckoutIn, format_errors

log = logging.getLogger(__name__)

storefront_bp = Blueprint("storefront_api", __name__)

CART_COOKIE = "dracula_cart"
SESSION_COOKIE = "dracula_session"
COOKIE_MAX_AGE = 30 * 24 * 3600


# ───────────────────────────── infrastructură ───────────────────────────────

def postgres_mode() -> bool:
    settings = get_settings()
    return settings.postgres_enabled and settings.storage_backend == "postgres"


def _tenant_slug() -> str:
    return get_settings().default_tenant


def _client_ip() -> str | None:
    raw = (
        request.headers.get("CF-Connecting-IP")
        or (request.headers.get("X-Forwarded-For") or "").split(",")[0].strip()
        or request.remote_addr
        or ""
    )
    return raw or None


def _body() -> dict[str, Any]:
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def _error(code: str, status: int = 400, **extra: Any):
    payload = {"status": "error", "error": code}
    payload.update(extra)
    return jsonify(payload), status


def _session_token() -> str:
    """Tokenul de sesiune al clientului: cookie HttpOnly sau, pentru compatibilitate,
    `customer_token` din corpul cererii (cum trimite storefront.js azi)."""
    cookie = request.cookies.get(SESSION_COOKIE, "")
    if cookie:
        return cookie
    body = _body()
    return str(body.get("customer_token") or body.get("token") or "")


def _cart_token() -> str:
    return request.cookies.get(CART_COOKIE, "")


def _with_cart_cookie(response, token: str):
    settings = get_settings()
    response.set_cookie(
        CART_COOKIE, token, max_age=COOKIE_MAX_AGE, httponly=True,
        secure=settings.cookie_secure, samesite="Lax", path="/",
    )
    return response


def _with_session_cookie(response, token: str):
    settings = get_settings()
    response.set_cookie(
        SESSION_COOKIE, token, max_age=COOKIE_MAX_AGE, httponly=True,
        secure=settings.cookie_secure, samesite="Lax", path="/",
    )
    return response


# ───────────────────────────── CSRF ─────────────────────────────────────────

CSRF_COOKIE = "dracula_csrf"
CSRF_HEADER = "X-CSRF-Token"
#: Rute fără CSRF: nu există încă sesiune de protejat, iar cookie-urile de sesiune sunt
#: `SameSite=Lax`, deci un POST cross-site nu le-ar trimite oricum.
CSRF_EXEMPT = frozenset({
    "/api/account/login",
    "/api/account/register",
    "/api/account/forgot-password",
    "/api/account/reset-password",
    "/api/account/verify-email",
    "/api/account/resend-verification",
    # Bannerul de cookie-uri: apel „trimite și uită", fără corp de răspuns. Sub CSRF, un
    # header lipsă însemna 403 și consimțământul se pierdea TĂCUT — adică exact dovada
    # GDPR. Nu există sesiune de protejat, iar abuzul e limitat separat, pe hash de IP.
    "/api/consent",
    # Webhook-ul Stripe: apel server-la-server, fără cookie și fără antet CSRF. Se
    # autentifică prin `Stripe-Signature` (HMAC cu STRIPE_WEBHOOK_SECRET), verificată
    # de rută ÎNAINTE de orice altceva — o cerere nesemnată primește 400 de acolo.
    # Pe 21.09.2026 CSRF-ul a respins cu 403 plata ORD-2026-000052 (comanda a rămas
    # `pending_payment` deși era plătită). Doar ruta exactă, nu un prefix.
    "/api/payments/stripe/webhook",
})

#: Câte consimțământuri acceptăm de la același IP într-o oră. Peste prag, cererea
#: primește tot 204 (bannerul nu trebuie să se blocheze), dar nu se mai scrie nimic.
CONSENT_RATE_LIMIT_PER_HOUR = 30
#: Contor în proces pentru limita de mai sus. `ip_hash` din tabel include `consent_id`,
#: deci un atacator fără cookie ar avea un hash nou la fiecare cerere și verificarea din
#: bază nu l-ar prinde; aici cheia e doar IP-ul (tot ca hash, niciodată în clar).
#: Memoria unui worker gunicorn — se pierde la restart, ceea ce e acceptabil pentru o
#: limită anti-inundare, nu pentru o regulă de business.
_CONSENT_HITS: dict[str, list[float]] = {}


def _consent_flood(ip: str) -> bool:
    """True dacă IP-ul a trimis deja prea multe consimțământuri în ultima oră."""
    import time as _time

    if not ip:
        return False
    key = hashlib.sha256(ip.encode("utf-8")).hexdigest()
    now = _time.time()
    hits = [t for t in _CONSENT_HITS.get(key, []) if now - t < 3600]
    if len(_CONSENT_HITS) > 5000:                      # plafon de memorie
        _CONSENT_HITS.clear()
    if len(hits) >= CONSENT_RATE_LIMIT_PER_HOUR:
        _CONSENT_HITS[key] = hits
        return True
    hits.append(now)
    _CONSENT_HITS[key] = hits
    return False
UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def csrf_enforced() -> bool:
    """Verificarea e comandată de `CSRF_ENFORCE` (implicit **oprită**).

    Se aprinde după ce front-end-ul trimite headerul pe toate cererile de scriere;
    altfel ar bloca exact fluxurile pe care le protejează. Token dublu: cookie
    `eva_csrf` (citibil de JS) + header `X-CSRF-Token` cu aceeași valoare.
    """
    raw = os.environ.get("CSRF_ENFORCE", "")
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _issue_csrf_cookie(response):
    if request.cookies.get(CSRF_COOKIE):
        return response
    token = secrets.token_urlsafe(24)
    response.set_cookie(
        CSRF_COOKIE, token, max_age=12 * 3600, httponly=False,   # JS trebuie să-l citească
        secure=get_settings().cookie_secure, samesite="Lax", path="/",
    )
    return response


def check_csrf():
    """`before_request` pentru rutele publice de scriere."""
    if request.method not in UNSAFE_METHODS:
        return None
    path = request.path.rstrip("/") or "/"
    # `/admin/api/*` (rutele legacy) intră și ele sub verificare: nu încep cu `/api/`,
    # deci erau complet descoperite. Adminul nou (`/api/admin/v1`) folosește Bearer,
    # care nu se trimite automat cross-site, deci nu e expus CSRF.
    if path.startswith("/api/admin/"):
        return None
    if not path.startswith("/api/") and not path.startswith("/admin/api/"):
        return None
    if path in CSRF_EXEMPT:
        return None
    if not csrf_enforced():
        return None
    cookie = request.cookies.get(CSRF_COOKIE, "")
    header = request.headers.get(CSRF_HEADER, "")
    if not cookie or not header or not secrets.compare_digest(cookie, header):
        log.warning("CSRF respins pe %s", path)
        return _error("csrf_failed", 403)
    return None


class _Ctx:
    """Contextul unei cereri de storefront: tenant, sesiune de DB, user curent."""

    def __init__(self, session, tenant_id: str, tenant_slug: str,
                 user: dict[str, Any] | None) -> None:
        self.session = session
        self.tenant_id = tenant_id
        self.tenant_slug = tenant_slug
        self.user = user

    @property
    def user_id(self) -> str | None:
        return self.user["user_id"] if self.user else None


def _open_ctx(require_user: bool = False, cart_token: str | None = None):
    """Deschide o tranzacție cu `app.tenant_id` (+ `app.user_id` dacă e logat)."""
    slug = _tenant_slug()
    scope = session_scope()
    session = scope.__enter__()
    try:
        tenant_id = get_tenant_id(session, slug)
        if tenant_id is None:
            raise LookupError("unknown_tenant")
        from ..db import set_session_context

        set_session_context(session, tenant_id=tenant_id)
        identity = IdentityRepo(session, tenant_id)
        user = identity.user_from_session(_session_token())
        if user:
            set_session_context(session, user_id=user["user_id"], actor_type="customer",
                                actor_id=user["user_id"])
        elif require_user:
            raise PermissionError("missing_customer_session")
        # Politica `own_cart` a vizitatorului compară `cart_token_hash` cu acest
        # parametru de sesiune, deci trebuie setat ÎNAINTE de a citi/crea coșul —
        # inclusiv pentru tokenul proaspăt generat, care nu e încă în cookie.
        effective_token = cart_token or _cart_token()
        if effective_token:
            set_session_context(
                session, cart_token_hash=hash_cart_token(effective_token).hex()
            )
        return scope, _Ctx(session, tenant_id, slug, user)
    except Exception:
        scope.__exit__(*sys.exc_info())
        raise


ORDER_COOKIE = "dracula_orders"
#: Cât timp un vizitator mai poate deschide pagina de confirmare a comenzii lui.
ORDER_COOKIE_MAX_AGE = 7 * 24 * 3600
#: Câte comenzi ține cookie-ul (cineva poate comanda de mai multe ori fără cont).
ORDER_COOKIE_KEEP = 5


def _order_secret() -> str:
    """Cheia cu care se semnează cookie-ul. `SECRET_KEY` e obligatoriu în producție;
    `JWT_SECRET` e rezerva, ca aplicația să pornească și într-o instalare minimală."""
    return (os.environ.get("SECRET_KEY") or get_settings().jwt_secret or "").strip()


def _order_serializer():
    from itsdangerous import URLSafeTimedSerializer

    secret = _order_secret()
    if not secret:
        raise RuntimeError("SECRET_KEY lipsește: nu pot semna accesul la comandă")
    return URLSafeTimedSerializer(secret, salt="eva-order-access")


def recent_order_numbers() -> list[str]:
    """Comenzile pe care cererea curentă are dreptul să le vadă fără cont.

    Valoarea e **semnată** cu `SECRET_KEY`: altfel oricine ar putea scrie un număr de
    comandă în cookie și ar citi adresa și telefonul unui străin. Semnătura expiră
    odată cu cookie-ul.
    """
    raw = request.cookies.get(ORDER_COOKIE, "")
    if not raw:
        return []
    try:
        value = _order_serializer().loads(raw, max_age=ORDER_COOKIE_MAX_AGE)
    except Exception:                                        # noqa: BLE001
        return []
    return [str(item) for item in value][:ORDER_COOKIE_KEEP] if isinstance(value, list) else []


def _remember_order(response, order_number: str):
    """Adaugă comanda la lista semnată din cookie, păstrând ultimele câteva.

    Dacă semnarea nu e posibilă (fără `SECRET_KEY`), comanda se plasează oricum —
    doar pagina de confirmare pentru vizitatori nu va funcționa.
    """
    if not order_number:
        return response
    try:
        _order_serializer()
    except RuntimeError:
        log.warning("fără SECRET_KEY: confirmarea de comandă nu va fi accesibilă vizitatorului")
        return response
    numbers = [order_number] + [n for n in recent_order_numbers() if n != order_number]
    response.set_cookie(
        ORDER_COOKIE, _order_serializer().dumps(numbers[:ORDER_COOKIE_KEEP]),
        max_age=ORDER_COOKIE_MAX_AGE, httponly=True,
        secure=get_settings().cookie_secure, samesite="Lax", path="/",
    )
    return response


def _clear_session_cookies(response):
    """Șterge `eva_session` și `eva_cart` cu ACELEAȘI atribute cu care au fost puse.

    Un `Set-Cookie` de ștergere trebuie să repete `Secure`, `SameSite` și `Path`;
    altfel unele browsere îl consideră alt cookie, îl păstrează pe cel original și
    userul rămâne autentificat până la expirare.

    `eva_cart` pleacă odată cu sesiunea: coșul de vizitator a fost deja fuzionat în
    contul lui la autentificare, iar pe un calculator partajat următorul vizitator ar
    prelua coșul celui dinainte.
    """
    settings = get_settings()
    for cookie in (SESSION_COOKIE, CART_COOKIE):
        response.delete_cookie(cookie, path="/", secure=settings.cookie_secure,
                               samesite="Lax", httponly=True)
    return response


def _close_ctx(scope) -> None:
    import sys
    scope.__exit__(*sys.exc_info())


def session_user_or_none() -> dict[str, Any] | None:
    """Clientul logat din cookie-ul `eva_session`, sau `None`.

    Variantă „ieftină” pentru paginile HTML randate de `factory.py` (login,
    register, …): nu are nevoie de coș, nu aruncă niciodată și, dacă baza nu e
    disponibilă, răspunde `None` — pagina de login se afișează oricum, în loc
    să dea 500.
    """
    if not postgres_mode():
        return None
    token = request.cookies.get(SESSION_COOKIE, "")
    if not token:
        return None
    try:
        scope, ctx = _open_ctx()
    except Exception:                                        # noqa: BLE001
        return None
    try:
        return ctx.user
    except Exception:                                        # noqa: BLE001
        return None
    finally:
        _close_ctx(scope)


# ───────────────────────────── imagini ──────────────────────────────────────

def _thumbnail(tenant_slug: str, item: dict[str, Any]) -> str:
    """Prima imagine a produsului, ca URL public servibil (`/media/products-static/…`).

    Coșul și comenzile țineau până acum doar URL-ul brut din import (`cesiro.ro/wp-content/…`),
    care nu se poate afișa: e pe alt domeniu, fără WebP și fără redimensionare. Refolosim
    exact convenția din catalog (`cms.public_product_media_urls`), ca poza din coș să fie
    fix cea din listă și din fișa produsului — deci deja în cache-ul browserului.
    """
    from .. import cms

    raw = item.get("image") or item.get("image_url") or ""
    if raw.startswith('/assets/') or raw.startswith('/media/'+tenant_slug+'/'):
        return raw
    seed = {
        "id": item.get("id") or item.get("external_id") or "",
        "sku": item.get("sku") or "",
        "images": [raw] if raw else [],
    }
    if not seed["images"]:
        return ""
    urls = cms.public_product_media_urls(tenant_slug, seed)
    return urls[0] if urls else cms.public_media_url(raw)


def _with_thumbnails(tenant_slug: str, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for item in items or []:
        item["image_url"] = _thumbnail(tenant_slug, item)
    return items or []


def _with_display_dates(order: dict[str, Any], locale: str) -> dict[str, Any]:
    """Adaugă `*_display` lângă datele ISO.

    ISO rămâne (front-end-ul poate avea nevoie de ea pentru sortare), dar formatul
    citibil vine din același loc ca în șabloane — altfel aceeași comandă ar apărea cu
    două date diferite în pagină și în JSON.
    """
    from .. import cms, order_labels

    if not order:
        return order
    # etichetele de status pentru client (card plătit → „Confirmată"), derivate la
    # citire; se aplică înaintea datelor, ca rândul sintetic „Plată confirmată" să
    # primească şi el `created_at_display`
    order_labels.apply(order, locale)
    for key in ("created_at", "updated_at", "paid_at"):
        if order.get(key):
            order[f"{key}_display"] = cms.localized_datetime(order[key], locale)
    for event in order.get("status_history") or []:
        if event.get("created_at"):
            event["created_at_display"] = cms.localized_datetime(event["created_at"], locale)
            event["at_display"] = event["created_at_display"]   # numele citit de shop.js
    return order


# ───────────────────────────── coș ──────────────────────────────────────────

def _cart_payload(ctx: _Ctx, cart_id: str, locale: str) -> dict[str, Any]:
    repo = CartRepo(ctx.session, ctx.tenant_id, ctx.tenant_slug)
    data = repo.read(cart_id, locale)
    _with_thumbnails(ctx.tenant_slug, data.get("items"))
    settings = get_tenant_settings(ctx.session, ctx.tenant_id)
    country = str(request.args.get("country") or "RO").upper()
    shipping = round(shipping_for_country(settings, country), 2) if data["items"] else 0.0
    # reducerea progresivă: DOAR campania activă pe server (niciodată tema aleasă)
    from .. import promotions

    promo = promotions.for_lines(
        ctx.session, ctx.tenant_id,
        [{"product_id": i["product_id"], "qty": i["qty"],
          "unit_price_gross_ron": i["unit_price_gross_ron"]} for i in data["items"]],
        locale,
    )
    subtotal = data["products_gross_ron"]
    promo_lines = (promo or {}).get("lines") or {}
    gross = 0.0
    for item in data["items"]:
        deal = promo_lines.get(str(item["product_id"])) or {}
        unit = round(float(deal.get("unit_price_gross_ron", item["unit_price_gross_ron"])), 2)
        item["discounted_unit_price_gross_ron"] = unit
        item["discount_ron"] = round(float(deal.get("discount_ron") or 0), 2)
        item["promotion_eligible"] = bool(deal.get("eligible")) if promo else False
        gross += round(unit * int(item["qty"]), 2)
    gross = round(gross, 2) if promo else subtotal
    discount = round(subtotal - gross, 2)
    data["promotion"] = promotions.public(promo)
    if data["promotion"] is not None:
        data["promotion"]["discount_ron"] = discount
    vat = vat_rate(settings)
    net = round(gross / (1 + vat), 2) if gross else 0.0
    rates = currency_rates.get_rates()
    currency = currency_rates.currency_for_country(country)
    total_ron = round(gross + shipping, 2)
    data["totals"] = {
        # `products_subtotal_ron` = la preţ de catalog; `products_gross_ron` = după
        # reducerea progresivă (ce se plăteşte), ca în comanda salvată
        "products_subtotal_ron": subtotal,
        "discount_total_ron": discount,
        "products_gross_ron": gross,
        "products_net_ron": net,
        "vat_total_ron": round(gross - net, 2),
        "shipping_ron": shipping,
        "total_ron": total_ron,
        "total_display": currency_rates.convert_from_ron(total_ron, currency, rates),
        "currency": currency,
        "vat_rate": vat,
    }
    data["locale"] = locale
    return data


def _locale() -> str:
    from .. import cms

    lang = str(request.args.get("lang") or (_body().get("lang") if request.is_json else "") or "")
    lang = lang.strip().lower()
    from ..dracula_locales import enabled_locales
    if lang in enabled_locales():
        return lang
    # fără `lang` explicit (URL-uri curate, 23.09): cookie `eva_lang` → Accept-Language →
    # limba implicită a tenantului — aceeași regulă ca paginile HTML
    try:
        from ..factory import request_lang

        return request_lang()
    except Exception:                                    # noqa: BLE001
        return cms.DEFAULT_LANG


@storefront_bp.get("/api/cart")
def get_cart():
    if not get_settings().postgres_enabled:
        return _error("cart_unavailable", 503)
    token = _cart_token() or new_cart_token()
    try:
        scope, ctx = _open_ctx(cart_token=token)
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        repo = CartRepo(ctx.session, ctx.tenant_id, ctx.tenant_slug)
        cart_id = repo.get_or_create(
            user_id=ctx.user_id,
            token_hash=hash_cart_token(token),
            locale=_locale(),
        )
        # prețurile liniilor = catalog + oferta automată de ACUM (idempotent)
        changes = repo.reprice(cart_id, _locale())
        payload = _cart_payload(ctx, cart_id, _locale())
        _merge_warnings(payload, changes)
    finally:
        _close_ctx(scope)
    return _with_cart_cookie(make_response(jsonify(payload), 200), token)


def _merge_warnings(payload: dict[str, Any], changes: list[dict[str, Any]]) -> None:
    """Avertismentele `price_changed` găsite de `CartRepo.reprice` (după rescriere,
    `read` nu le mai vede, fiindcă prețul salvat e deja cel nou)."""
    if not changes:
        return
    warnings = payload.setdefault("warnings", [])
    seen = {(w.get("code"), w.get("product_id")) for w in warnings}
    for change in changes:
        if (change.get("code"), change.get("product_id")) not in seen:
            warnings.append(change)


@storefront_bp.post("/api/cart/items")
def add_cart_item():
    return _mutate_cart("add")


@storefront_bp.patch("/api/cart/items/<product_ref>")
def patch_cart_item(product_ref: str):
    return _mutate_cart("set", product_ref)


@storefront_bp.delete("/api/cart/items/<product_ref>")
def delete_cart_item(product_ref: str):
    return _mutate_cart("remove", product_ref)


@storefront_bp.delete("/api/cart")
def clear_cart():
    return _mutate_cart("clear")


@storefront_bp.post("/api/cart/sync")
def sync_cart():
    """Urcă un coș din localStorage când cel din DB e gol (o singură dată, la boot)."""
    return _mutate_cart("sync")


@storefront_bp.post("/api/cart/merge")
def merge_cart():
    """Fuzionează coșul de vizitator în cel al userului logat, imediat după login."""
    if not get_settings().postgres_enabled:
        return _error("cart_unavailable", 503)
    token = _cart_token()
    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        repo = CartRepo(ctx.session, ctx.tenant_id, ctx.tenant_slug)
        if not ctx.user_id:
            return _error("missing_customer_session", 403)
        user_cart = repo.get_or_create(user_id=ctx.user_id, token_hash=None, locale=_locale())
        guest_cart = (
            repo.find_open(user_id=None, token_hash=hash_cart_token(token)) if token else None
        )
        if guest_cart and str(guest_cart) != user_cart:
            repo.merge(guest_cart_id=str(guest_cart), user_cart_id=user_cart)
        changes = repo.reprice(user_cart, _locale())
        payload = _cart_payload(ctx, user_cart, _locale())
        _merge_warnings(payload, changes)
    finally:
        _close_ctx(scope)
    return jsonify(payload)


def _cart_quantity(value: Any, *, allow_zero: bool = False) -> int:
    """Accept integer quantities without truncating fractions or coercing booleans."""
    if type(value) is int:
        qty = value
    elif isinstance(value, str) and re.fullmatch(r"[0-9]+", value):
        qty = int(value)
    else:
        raise ValueError("invalid_quantity")
    if qty < (0 if allow_zero else 1):
        raise ValueError("invalid_quantity")
    return qty


def _mutate_cart(action: str, product_ref: str | None = None):
    if not get_settings().postgres_enabled:
        return _error("cart_unavailable", 503)
    token = _cart_token() or new_cart_token()
    body = _body()
    # Validate before even opening a tenant/cart context; invalid sync batches
    # must not leave a partially imported cart.
    incoming = []
    try:
        if action == "add":
            qty = _cart_quantity(body.get("qty", 1))
        elif action == "set":
            qty = _cart_quantity(body.get("qty"), allow_zero=True)
        elif action == "sync":
            raw_items = body.get("items") or []
            if not isinstance(raw_items, list):
                return _error("invalid_items", 400)
            incoming = [
                {**item, "qty": _cart_quantity(item.get("qty", 1))}
                for item in raw_items[:100] if isinstance(item, dict)
            ]
    except ValueError:
        return _error("invalid_quantity", 400)
    locale = _locale()
    try:
        scope, ctx = _open_ctx(cart_token=token)
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        repo = CartRepo(ctx.session, ctx.tenant_id, ctx.tenant_slug)
        cart_id = repo.get_or_create(
            user_id=ctx.user_id, token_hash=hash_cart_token(token), locale=locale
        )

        if action == "clear":
            repo.clear(cart_id)
        elif action == "sync":
            current = repo.read(cart_id, locale)
            if not current["items"]:
                for item in incoming:
                    product = _resolve(repo, item)
                    if product:
                        repo.set_qty(cart_id, str(product["id"]),
                                     item["qty"],
                                     float(product["price_ron"] or 0),
                                     offer=product.get("offer"))
        else:
            ref = {"product_id": product_ref} if product_ref else body
            product = _resolve(repo, {**body, **ref}, allow_unpublished=action == "remove" or (action == "set" and qty == 0))
            if product is None:
                return _error("unknown_product", 404)
            pid = str(product["id"])
            price = float(product["price_ron"] or 0)
            # `price_ron` din `resolve_product` e deja prețul cu oferta automată
            if action == "add":
                repo.add(cart_id, pid, qty, price,
                         offer=product.get("offer"))
            elif action == "set":
                repo.set_qty(cart_id, pid, qty, price,
                             offer=product.get("offer"))
            elif action == "remove":
                repo.remove(cart_id, pid)

        payload = _cart_payload(ctx, cart_id, locale)
    finally:
        _close_ctx(scope)
    return _with_cart_cookie(make_response(jsonify(payload), 200), token)


def _resolve(repo: CartRepo, data: dict[str, Any], *, allow_unpublished: bool = False) -> dict[str, Any] | None:
    """Acceptă `product_id` (uuid), `id` (`wp-<n>`, cum trimite JS-ul azi) sau `sku`."""
    raw = str(data.get("product_id") or "").strip()
    external = str(data.get("external_id") or data.get("id") or "").strip()
    sku = str(data.get("sku") or "").strip()
    if raw and "-" in raw and len(raw) == 36:
        product = repo.resolve_product(product_id=raw)
        if product:
            return product if allow_unpublished or product.get("status") == "published" else None
    if raw and not external:
        external = raw
    product = repo.resolve_product(external_id=external or None, sku=sku or None)
    return product if product and (allow_unpublished or product.get("status") == "published") else None


# ───────────────────────────── cont ─────────────────────────────────────────

@storefront_bp.post("/api/account/register")
def register_account():
    if not get_settings().postgres_enabled:
        return _error("register_unavailable", 503)
    body = _body()
    if body.get("website"):                       # honeypot, ca la /api/orders
        return _error("spam_detected", 400)

    email = normalize_email(body.get("email"))
    password = str(body.get("password") or "")
    full_name = str(body.get("full_name") or body.get("name") or "").strip()
    if not valid_email(email):
        return _error("invalid_email", 400)
    if len(password) < 10:
        return _error("weak_password", 400)
    if body.get("password_confirm") is not None and body.get("password_confirm") != password:
        return _error("password_mismatch", 400)
    if not full_name:
        return _error("missing_name", 400)
    if not body.get("accept_terms"):
        return _error("terms_required", 400)
    phone_value, phone_error = _phone_field(body)
    if phone_error is not None:
        return phone_error

    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        try:
            created = identity.register(
                email=email,
                password=password,
                full_name=full_name,
                phone=phone_value,
                locale=_locale(),
                customer_type=str(body.get("customer_type") or "individual"),
                company={
                    "name": str(body.get("company_name") or ""),
                    "vat": str(body.get("company_vat") or ""),
                    "reg": str(body.get("company_reg") or ""),
                },
                newsletter=bool(body.get("newsletter")),
                ip=_client_ip(),
                user_agent=request.headers.get("User-Agent", ""),
            )
        except ValueError as exc:
            if str(exc) == "email_taken":
                return _error("email_taken", 409)
            raise

        session_token = identity.create_session(
            created["user_id"], ip=_client_ip(),
            user_agent=request.headers.get("User-Agent", ""),
        )
        # același motiv ca la login: contextul RLS înaintea oricărei operații pe coș
        set_session_context_for_user(ctx, created["user_id"])
        cart_token = _cart_token()
        if cart_token:
            repo = CartRepo(ctx.session, ctx.tenant_id, ctx.tenant_slug)
            guest = repo.find_open(user_id=None, token_hash=hash_cart_token(cart_token))
            if guest:
                user_cart = repo.get_or_create(user_id=created["user_id"], token_hash=None,
                                               locale=_locale())
                if str(guest) != user_cart:
                    repo.merge(guest_cart_id=str(guest), user_cart_id=user_cart)

        from ..mail import notify

        notify.account_created(ctx.session, tenant_id=ctx.tenant_id, to_email=email,
                               name=full_name, locale=_locale(),
                               user_id=created["user_id"])
        notify.email_verification(
            ctx.session, tenant_id=ctx.tenant_id, to_email=email,
            token=created["verify_token"], name=full_name, locale=_locale(),
            user_id=created["user_id"],
        )
        payload = {
            "status": "ok",
            "account_id": created["user_id"],
            "email": email,
            "name": full_name,
            "customer_token": session_token,       # compat cu storefront.js
            "account_type": "store_customer",
            "must_change_password": False,
            "email_verification_required": True,
            "shipping_addresses": [],
            "active_shipping_address_id": "",
        }
    finally:
        _close_ctx(scope)
    return _with_session_cookie(make_response(jsonify(payload), 201), session_token)


@storefront_bp.post("/api/account/verify-email")
def verify_email():
    if not get_settings().postgres_enabled:
        return _error("register_unavailable", 503)
    token = str(_body().get("token") or request.args.get("token") or "")
    if not token:
        return _error("missing_token", 400)
    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        ok = _verify_email_in_ctx(ctx, token)
    finally:
        _close_ctx(scope)
    if not ok:
        return _error("invalid_token", 400)
    return jsonify({"status": "ok"})


def _verify_email_in_ctx(ctx, token: str) -> bool:
    """Consumă tokenul și marchează adresa confirmată.

    `mark_email_verified` trebuie rulat CU `app.user_id` setat: politica RLS
    `own_profile` de pe identity.users altfel ascunde rândul și UPDATE-ul nu atinge
    nimic (tokenul se consuma, dar adresa rămânea neconfirmată)."""
    from ..db import set_session_context

    identity = IdentityRepo(ctx.session, ctx.tenant_id)
    user_id = identity.consume_token(token, "email_verify")
    if not user_id:
        return False
    set_session_context(ctx.session, user_id=user_id, actor_type="customer", actor_id=user_id)
    identity.mark_email_verified(user_id)
    return True


def verify_email_token(token: str) -> bool:
    """Pentru linkul din e-mail (GET /?verify=…), procesat de `factory.home`."""
    if not token or not get_settings().postgres_enabled:
        return False
    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return False
    try:
        return _verify_email_in_ctx(ctx, token)
    finally:
        _close_ctx(scope)


@storefront_bp.post("/api/account/resend-verification")
def resend_verification():
    """Retrimite e-mailul de confirmare a adresei.

    Răspunde **mereu 200**, indiferent dacă adresa există sau e deja confirmată —
    altfel endpoint-ul ar deveni un instrument de enumerare a conturilor.
    Verificarea adresei NU blochează autentificarea: e un indicator, nu o poartă.
    """
    if not get_settings().postgres_enabled:
        return jsonify({"status": "ok"})
    email = normalize_email(_body().get("email"))
    if not valid_email(email):
        return _error("invalid_email", 400)
    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        row = identity.lookup_for_login(email)
        if row is not None and row.email_verified_at is None and not identity.is_guest(
                str(row.user_id)):
            from ..mail import notify

            token = identity.issue_token(str(row.user_id), "email_verify")
            notify.email_verification(
                ctx.session, tenant_id=ctx.tenant_id, to_email=email, token=token,
                name=row.full_name or "", locale=_locale(), user_id=str(row.user_id),
            )
            log.info("retrimitere confirmare e-mail pentru un cont neconfirmat")
        else:
            log.info("cerere de retrimitere fără efect (cont inexistent sau deja confirmat)")
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok"})


CONSENT_COOKIE = "eva_consent"


def _require_user_ctx():
    """Deschide contextul cerând un client autentificat; întoarce (scope, ctx) sau (None, răspuns)."""
    try:
        return _open_ctx(require_user=True), None
    except LookupError:
        return None, _error("unknown_tenant", 404)
    except PermissionError:
        return None, _error("missing_customer_session", 403)


# ───────────────────────────── comenzi (citire) ─────────────────────────────

@storefront_bp.get("/api/account/orders")
def list_orders_get():
    """Aceleași comenzi ca `POST /api/account/orders`, dar cu verbul corect.

    Vechea rută POST rămâne (o cheamă `storefront.js` de azi); asta e cea pe care o
    folosesc paginile noi `/account` și `/account/comenzi/<nr>`.
    """
    from ..factory import request_tenant                     # noqa: F401  (context)

    return list_customer_orders()


@storefront_bp.get("/api/account/returns")
def list_returns_route():
    """Retururile clientului.

    Exista funcția (`list_returns`), exista și metoda din repository, dar nicio rută
    nu ducea la ele: clientul putea CERE un retur și nu mai afla niciodată ce s-a
    întâmplat cu el. Ruta doar expune ce era deja scris.
    """
    return list_returns()


@storefront_bp.get("/api/account/orders/<order_number>")
def get_order_detail(order_number: str):
    """Detaliul unei comenzi PROPRII: produse cu poze, totaluri, adrese, istoric.

    Doar comenzile utilizatorului autentificat — filtrul e și în SQL, nu doar în RLS.
    """
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        order = SalesRepo(ctx.session, ctx.tenant_id).get_for_user(
            ctx.user_id, str(order_number).strip()
        )
        if order is None:
            return _error("order_not_found", 404)
        _with_thumbnails(ctx.tenant_slug, order.get("items"))
        _with_display_dates(order, _locale())
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "order": order})


# ── ajutoare pentru paginile HTML randate de `factory.py` ───────────────────

def cart_has_items() -> bool:
    """True dacă cererea curentă are un coș cu cel puțin un produs.

    Folosit de `/checkout` ca să nu deschidă un formular de livrare peste un coș gol.
    Nu aruncă: la orice problemă răspunde `False` și apelantul decide.
    """
    if not postgres_mode():
        return False
    try:
        scope, ctx = _open_ctx()
    except Exception:                                        # noqa: BLE001
        return False
    try:
        repo = CartRepo(ctx.session, ctx.tenant_id, ctx.tenant_slug)
        cart_id = None
        if ctx.user_id:
            found = repo.find_open(user_id=ctx.user_id, token_hash=None)
            cart_id = str(found) if found else None
        if cart_id is None and _cart_token():
            found = repo.find_open(user_id=None,
                                   token_hash=hash_cart_token(_cart_token()))
            cart_id = str(found) if found else None
        if cart_id is None:
            return False
        return bool(repo.read(cart_id, _locale())["items"])
    except Exception:                                        # noqa: BLE001
        return False
    finally:
        _close_ctx(scope)


def order_for_current_user(order_number: str) -> dict[str, Any] | None:
    """Comanda cerută, dar numai dacă e a clientului autentificat."""
    if not postgres_mode() or not order_number:
        return None
    try:
        scope, ctx = _open_ctx(require_user=True)
    except Exception:                                        # noqa: BLE001
        return None
    try:
        order = SalesRepo(ctx.session, ctx.tenant_id).get_for_user(
            ctx.user_id, order_number
        )
        if order is not None:
            _with_thumbnails(ctx.tenant_slug, order.get("items"))
            _with_display_dates(order, _locale())
        return order
    except Exception:                                        # noqa: BLE001
        return None
    finally:
        _close_ctx(scope)


def order_for_confirmation(order_number: str) -> dict[str, Any] | None:
    """Comanda pentru pagina de „Mulțumim".

    Două căi de acces, ambele dovedite:
      * clientul logat — e comanda lui (`get_for_user`);
      * vizitatorul — numărul comenzii e în cookie-ul **semnat** pus chiar la plasarea
        ei (`_remember_order`). Fără semnătură, oricine ar putea încerca numere la
        rând și ar citi numele, adresa și telefonul unui străin.
    """
    if not postgres_mode() or not order_number:
        return None
    mine = order_for_current_user(order_number)
    if mine is not None:
        return mine
    if order_number not in recent_order_numbers():
        return None
    try:
        scope, ctx = _open_ctx()
    except Exception:                                        # noqa: BLE001
        return None
    try:
        # RLS: un vizitator nu are `app.user_id`, deci politica `own_orders` nu i-ar
        # întoarce niciun rând — pagina de confirmare se golea și trimitea omul înapoi
        # pe prima pagină, deși tocmai comandase. Deschidem accesul strict la numărul
        # DOVEDIT de cookie-ul semnat, nu la comenzile lui în general (migrația 0017).
        from ..db import set_session_context

        set_session_context(ctx.session, order_number=order_number)
        order = SalesRepo(ctx.session, ctx.tenant_id).get_by_number(order_number)
        if order is not None:
            _with_thumbnails(ctx.tenant_slug, order.get("items"))
            _with_display_dates(order, _locale())
        return order
    except Exception:                                        # noqa: BLE001
        return None
    finally:
        _close_ctx(scope)


# ───────────────────────────── profil ───────────────────────────────────────

@storefront_bp.get("/api/account/profile")
def get_profile():
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        profile = identity.get_profile(ctx.user_id)
        if profile is None:
            return _error("account_not_found", 404)
        profile["addresses"] = identity.list_addresses(ctx.user_id)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "profile": profile})


@storefront_bp.put("/api/account/profile")
@storefront_bp.patch("/api/account/profile")
def update_profile():
    body = _body()
    customer_type = str(body.get("customer_type") or "").strip()
    if customer_type and customer_type not in {"individual", "company"}:
        return _error("invalid_customer_type", 400)
    if customer_type == "company" and not (body.get("company_name") and body.get("company_vat")):
        return _error("missing_company", 400)
    if "phone" in body:
        value, phone_error = _phone_field(body)
        if phone_error is not None:
            return phone_error
        body = {**body, "phone": value}
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        identity.update_profile(ctx.user_id, body)
        profile = identity.get_profile(ctx.user_id)
        profile["addresses"] = identity.list_addresses(ctx.user_id)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "profile": profile})


@storefront_bp.delete("/api/account")
def delete_account():
    """Ștergerea contului în sensul GDPR.

    Comenzile NU se șterg (sunt documente contabile), dar datele personale din ele se
    anonimizează. Contul devine imposibil de folosit și toate sesiunile cad.
    Confirmarea explicită `{"confirm": true}` e obligatorie.
    """
    if not _body().get("confirm"):
        return _error("confirmation_required", 400)
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        IdentityRepo(ctx.session, ctx.tenant_id).anonymize(ctx.user_id)
    finally:
        _close_ctx(scope)
    return _clear_session_cookies(make_response(jsonify({"status": "ok"}), 200))


# ───────────────────────────── adrese ───────────────────────────────────────

@storefront_bp.get("/api/account/addresses")
def list_addresses():
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        addresses = IdentityRepo(ctx.session, ctx.tenant_id).list_addresses(ctx.user_id)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "addresses": addresses})


@storefront_bp.post("/api/account/addresses")
def create_address():
    body = _body()
    if not str(body.get("address") or body.get("line1") or "").strip():
        return _error("missing_address", 400)
    if body.get("phone"):
        value, phone_error = _phone_field(body)
        if phone_error is not None:
            return phone_error
        body = {**body, "phone": value}
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        payload = dict(body)
        # `address` e textul compus, folosit de e-mailuri și de șabloanele vechi. Îl
        # lăsăm pe seama repository-ului (`compose_address`): dacă l-am pune aici
        # egal cu `line1`, adresa salvată ar pierde blocul, orașul și codul poștal.
        payload.setdefault("postcode", body.get("postal_code"))
        existing = identity.list_addresses(ctx.user_id)
        address_id = identity.upsert_address(
            ctx.user_id, payload,
            make_default=bool(body.get("is_default")) or not existing,
        )
        addresses = identity.list_addresses(ctx.user_id)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "id": address_id, "addresses": addresses}), 201


@storefront_bp.put("/api/account/addresses/<address_id>")
@storefront_bp.patch("/api/account/addresses/<address_id>")
def update_address(address_id: str):
    body = _body()
    if body.get("phone"):
        value, phone_error = _phone_field(body)
        if phone_error is not None:
            return phone_error
        body = {**body, "phone": value}
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        payload = dict(body)
        if not body.get("address") and any(
                body.get(field) for field in ("line1", "line2", "city", "county",
                                              "postal_code", "postcode")):
            # s-a schimbat un câmp al adresei → recompunem și textul, ca cele două
            # reprezentări să nu se contrazică
            current = next((a for a in identity.list_addresses(ctx.user_id)
                            if a["id"] == address_id), {})
            merged = {**current, **{k: v for k, v in body.items() if v is not None}}
            payload["address"] = compose_address(merged)
        if not identity.update_address(ctx.user_id, address_id, payload):
            return _error("address_not_found", 404)
        addresses = identity.list_addresses(ctx.user_id)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "addresses": addresses})


@storefront_bp.delete("/api/account/addresses/<address_id>")
def delete_address(address_id: str):
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        if not identity.delete_address(ctx.user_id, address_id):
            return _error("address_not_found", 404)
        addresses = identity.list_addresses(ctx.user_id)
        # dacă am șters adresa implicită, prima rămasă devine implicită
        if addresses and not any(a["is_default"] for a in addresses):
            identity.set_default_address(ctx.user_id, addresses[0]["id"])
            addresses = identity.list_addresses(ctx.user_id)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "addresses": addresses})


# ─────────────────────────── firmele mele ───────────────────────────────────
#
# Clientul care comandă pe firmă completa aceleaşi date la fiecare comandă, iar în
# cont nu rămânea nimic. Acum firmele stau în `identity.customer_companies` (o listă
# proprie, ca adresele) şi se salvează singure la plasarea comenzii.

def _company_errors(body: dict[str, Any], partial: bool = False) -> list[dict[str, Any]]:
    """Aceleaşi reguli ca la checkout (`CompanyIn`), ca să nu existe două adevăruri.

    La `PUT` parţial se validează doar câmpurile trimise: un client care schimbă
    numai IBAN-ul nu trebuie să retrimită CUI-ul.
    """
    from .checkout_schemas import CUI_RE, REG_COM_RE

    errors: list[dict[str, Any]] = []
    name = " ".join(str(body.get("name") or "").split())
    cui = re.sub(r"[\s.\-]", "", str(body.get("cui") or "")).upper()
    reg = " ".join(str(body.get("reg_com") or body.get("reg") or "").split())
    if not partial or "name" in body:
        if len(name) < 2:
            errors.append({"loc": ["name"], "msg": "Denumirea firmei e obligatorie"})
    if not partial or "cui" in body:
        if not cui:
            errors.append({"loc": ["cui"], "msg": "CUI-ul e obligatoriu"})
        elif not CUI_RE.fullmatch(cui):
            errors.append({"loc": ["cui"], "msg": "CUI invalid (ex. RO12345678)"})
    if reg and not REG_COM_RE.fullmatch(reg):
        errors.append({"loc": ["reg_com"],
                       "msg": "Număr de registru invalid (ex. J40/1234/2020)"})
    if body.get("contact_phone"):
        from .. import phone as phone_rules

        _value, error = phone_rules.validate(body.get("contact_phone"),
                                             locale=_form_locale(body),
                                             field="contact_phone")
        if error is not None:
            errors.append(error)
    return errors


def _company_payload(body: dict[str, Any]) -> dict[str, Any]:
    """Normalizează corpul: CUI fără separatoare, registru cu majuscule, ţară ISO."""
    payload = {key: value for key, value in body.items()
               if key in IdentityRepo.COMPANY_FIELDS}
    if body.get("cui"):
        payload["cui"] = re.sub(r"[\s.\-]", "", str(body["cui"])).upper()
    reg = body.get("reg_com") or body.get("reg")
    if reg:
        payload["reg_com"] = " ".join(str(reg).split()).upper().replace(" ", "")
    if body.get("country"):
        payload["country"] = str(body["country"]).upper()[:2]
    if body.get("contact_phone"):
        from .. import phone as phone_rules

        payload["contact_phone"] = phone_rules.normalize_or_keep(body["contact_phone"])
    return payload


@storefront_bp.get("/api/account/companies")
def list_companies():
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        companies = IdentityRepo(ctx.session, ctx.tenant_id).list_companies(ctx.user_id)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "companies": companies, "count": len(companies)})


@storefront_bp.post("/api/account/companies")
def create_company():
    body = _body()
    errors = _company_errors(body)
    if errors:
        return _validation_error(errors)
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        company_id, created = identity.save_company(
            ctx.user_id, _company_payload(body),
            make_default=bool(body.get("is_default")),
        )
        companies = identity.list_companies(ctx.user_id)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "id": company_id, "created": created,
                    "companies": companies}), (201 if created else 200)


@storefront_bp.put("/api/account/companies/<company_id>")
@storefront_bp.patch("/api/account/companies/<company_id>")
def update_company(company_id: str):
    body = _body()
    errors = _company_errors(body, partial=True)
    if errors:
        return _validation_error(errors)
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        payload = _company_payload(body)
        payload["is_default"] = bool(body.get("is_default"))
        if not identity.update_company(ctx.user_id, company_id, payload):
            return _error("company_not_found", 404)
        companies = identity.list_companies(ctx.user_id)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "companies": companies})


@storefront_bp.post("/api/account/companies/<company_id>/set-default")
def set_default_company(company_id: str):
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        if not any(c["id"] == company_id for c in identity.list_companies(ctx.user_id)):
            return _error("company_not_found", 404)
        identity.set_default_company(ctx.user_id, company_id)
        companies = identity.list_companies(ctx.user_id)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "companies": companies})


@storefront_bp.delete("/api/account/companies/<company_id>")
def delete_company(company_id: str):
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        if not identity.delete_company(ctx.user_id, company_id):
            return _error("company_not_found", 404)
        companies = identity.list_companies(ctx.user_id)
        # dacă am șters firma implicită, prima rămasă îi ia locul
        if companies and not any(c["is_default"] for c in companies):
            identity.set_default_company(ctx.user_id, companies[0]["id"])
            companies = identity.list_companies(ctx.user_id)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "companies": companies})


# ───────────────────────────── favorite ─────────────────────────────────────

def _favorites_payload(ctx, identity: IdentityRepo) -> list[dict[str, Any]]:
    from .. import theme_offers

    items = identity.list_favorites(ctx.user_id, _locale())
    # același preț ca în listă/coș: oferta automată a temei efective
    items = theme_offers.decorate_products(ctx.session, ctx.tenant_id, ctx.tenant_slug,
                                           items, _locale())
    _with_thumbnails(ctx.tenant_slug, items)
    return items


def _resolve_product_ref(ctx, body_or_ref: Any) -> str | None:
    """Acceptă `product_id` (uuid), `external_id` (`wp-123`) sau `sku`.

    Frontendul ține în `localStorage` id-ul public al produsului (`external_id`),
    nu uuid-ul intern, deci ambele trebuie să meargă pe aceeași rută.
    """
    if isinstance(body_or_ref, dict):
        raw_id = str(body_or_ref.get("product_id") or "").strip()
        external = str(body_or_ref.get("external_id") or body_or_ref.get("id") or "").strip()
        sku = str(body_or_ref.get("sku") or "").strip()
    else:
        raw = str(body_or_ref or "").strip()
        raw_id, external, sku = raw, raw, raw
    if not (raw_id or external or sku):
        return None
    cart = CartRepo(ctx.session, ctx.tenant_id, ctx.tenant_slug)
    # uuid-urile se dau lui `product_id`; orice altceva e external_id/sku
    looks_uuid = len(raw_id) == 36 and raw_id.count("-") == 4
    product = cart.resolve_product(
        product_id=raw_id if looks_uuid else None,
        external_id=external or None,
        sku=sku or None,
    )
    return str(product["id"]) if product else None


@storefront_bp.get("/api/account/favorites")
def list_favorites():
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        items = _favorites_payload(ctx, identity)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "items": items, "count": len(items)})


@storefront_bp.post("/api/account/favorites")
def add_favorite():
    body = _body()
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        product_id = _resolve_product_ref(ctx, body)
        if product_id is None:
            return _error("product_not_found", 404)
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        created = identity.add_favorite(ctx.user_id, product_id)
        items = _favorites_payload(ctx, identity)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "product_id": product_id, "created": created,
                    "items": items}), (201 if created else 200)


@storefront_bp.delete("/api/account/favorites/<product_ref>")
def delete_favorite(product_ref: str):
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        product_id = _resolve_product_ref(ctx, product_ref)
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        if product_id is None or not identity.remove_favorite(ctx.user_id, product_id):
            return _error("favorite_not_found", 404)
        items = _favorites_payload(ctx, identity)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "items": items, "count": len(items)})


@storefront_bp.post("/api/account/favorites/merge")
def merge_favorites():
    """Unește favoritele de vizitator (din `localStorage`) în cont, la login.

    Ca la coș: nu șterge nimic din ce are deja contul, doar adaugă. Referințele
    necunoscute (produse dispărute din catalog) se raportează în `skipped`, nu dau
    eroare — altfel un singur id vechi ar bloca toată unirea.
    """
    body = _body()
    raw_items = body.get("items") or body.get("product_ids") or body.get("favorites") or []
    if not isinstance(raw_items, list):
        return _error("invalid_items", 400)
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        added, skipped = 0, []
        for raw in raw_items[:200]:
            product_id = _resolve_product_ref(ctx, raw)
            if product_id is None:
                skipped.append(raw if isinstance(raw, str) else str(raw))
                continue
            if identity.add_favorite(ctx.user_id, product_id):
                added += 1
        items = _favorites_payload(ctx, identity)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "added": added, "skipped": skipped,
                    "items": items, "count": len(items)})


@storefront_bp.post("/api/consent")
def record_consent():
    """Înregistrează alegerea din bannerul de cookie-uri (dovadă GDPR).

    Pentru un client logat, alegerea se scrie ȘI în `identity.user_consents`, ca să
    fie legată de persoană. Pentru un vizitator, se folosește un id de cookie propriu
    (`eva_consent`), iar IP-ul se stochează doar ca hash — dovada nu are nevoie de
    adresa în clar.
    """
    if not get_settings().postgres_enabled:
        return make_response("", 204)
    body = _body()
    analytics = bool(body.get("analytics"))
    marketing = bool(body.get("marketing"))
    policy_version = str(body.get("policy_version") or "1.0")[:20]

    consent_id = request.cookies.get(CONSENT_COOKIE) or secrets.token_urlsafe(18)
    ip = _client_ip() or ""
    ip_hash = hashlib.sha256(f"{consent_id}:{ip}".encode("utf-8")).hexdigest() if ip else None
    if _consent_flood(ip):
        log.warning("consimțăminte peste prag de la același IP — cerere ignorată")
        return make_response("", 204)

    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        if ip_hash is not None:
            recent = ctx.session.execute(
                text(
                    """
                    SELECT count(*) FROM core.cookie_consents
                     WHERE tenant_id = CAST(:t AS uuid) AND ip_hash = :ip_hash
                       AND created_at > now() - interval '1 hour'
                    """
                ),
                {"t": ctx.tenant_id, "ip_hash": ip_hash},
            ).scalar() or 0
            if recent >= CONSENT_RATE_LIMIT_PER_HOUR:
                log.warning("consimțăminte peste prag de la același IP — cerere ignorată")
                return make_response("", 204)
        ctx.session.execute(
            text(
                """
                INSERT INTO core.cookie_consents
                       (tenant_id, consent_id, user_id, necessary, analytics, marketing,
                        policy_version, ip_hash, user_agent, locale)
                VALUES (CAST(:t AS uuid), :consent_id, CAST(:user_id AS uuid), true,
                        :analytics, :marketing, :version, :ip_hash, :ua, :locale)
                """
            ),
            {"t": ctx.tenant_id, "consent_id": consent_id, "user_id": ctx.user_id,
             "analytics": analytics, "marketing": marketing, "version": policy_version,
             "ip_hash": ip_hash,
             "ua": (request.headers.get("User-Agent") or "")[:400],
             "locale": _locale()},
        )
        if ctx.user_id:
            for kind, granted in (("cookies", True), ("marketing", marketing)):
                ctx.session.execute(
                    text(
                        """
                        INSERT INTO identity.user_consents
                               (user_id, tenant_id, kind, granted, version, ip, user_agent)
                        VALUES (CAST(:u AS uuid), CAST(:t AS uuid), :kind, :granted,
                                :version, CAST(:ip AS inet), :ua)
                        """
                    ),
                    {"u": ctx.user_id, "t": ctx.tenant_id,
                     "kind": "cookies" if kind == "cookies" else "newsletter",
                     "granted": granted, "version": policy_version, "ip": ip or None,
                     "ua": (request.headers.get("User-Agent") or "")[:400]},
                )
    finally:
        _close_ctx(scope)

    response = make_response("", 204)
    settings = get_settings()
    response.set_cookie(
        CONSENT_COOKIE, consent_id, max_age=365 * 24 * 3600, httponly=True,
        secure=settings.cookie_secure, samesite="Lax", path="/",
    )
    return response


@storefront_bp.post("/api/account/forgot-password")
def forgot_password():
    """Trimite linkul de resetare. Răspunde **mereu 200**, ca să nu se poată afla
    dacă o adresă are cont (enumerare)."""
    if not get_settings().postgres_enabled:
        return jsonify({"status": "ok"})
    email = normalize_email(_body().get("email"))
    if not valid_email(email):
        return _error("invalid_email", 400)
    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        row = identity.lookup_for_login(email)
        if row is not None and row.status == "active" and not identity.is_guest(str(row.user_id)):
            from ..mail import notify

            token = identity.issue_token(str(row.user_id), "password_reset")
            notify.password_reset(
                ctx.session, tenant_id=ctx.tenant_id, to_email=email, token=token,
                name=row.full_name or "", locale=_locale(), user_id=str(row.user_id),
            )
            log.info("resetare de parolă cerută pentru un cont existent")
        else:
            log.info("resetare cerută pentru o adresă fără cont activ (răspuns identic)")
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok"})


@storefront_bp.post("/api/account/reset-password")
def reset_password():
    """Setează parola nouă pe baza tokenului primit pe e-mail (valabil 48 h).

    La succes se revocă TOATE sesiunile contului: dacă cineva îi avea sesiunea
    deschisă, o pierde odată cu schimbarea parolei.
    """
    if not get_settings().postgres_enabled:
        return _error("unavailable", 503)
    body = _body()
    token = str(body.get("token") or "")
    new_password = str(body.get("new_password") or body.get("password") or "")
    if not token:
        return _error("missing_token", 400)
    if len(new_password) < 10:
        return _error("weak_password", 400)
    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        user_id = identity.consume_token(token, "password_reset")
        if not user_id:
            return _error("invalid_token", 400)
        identity.set_password(user_id, new_password, revoke_sessions=True)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok"})


@storefront_bp.post("/api/account/logout")
def logout_account():
    if not get_settings().postgres_enabled:
        return jsonify({"status": "ok"})
    token = _session_token()
    if token:
        try:
            scope, ctx = _open_ctx()
        except LookupError:
            return _error("unknown_tenant", 404)
        try:
            IdentityRepo(ctx.session, ctx.tenant_id).revoke_session(token)
        finally:
            _close_ctx(scope)
    return _clear_session_cookies(make_response(jsonify({"status": "ok"}), 200))


@storefront_bp.get("/api/checkout/options")
def checkout_options():
    """Metodele de livrare/plată și țările permise, din setările magazinului.

    Nimic hardcodat: totul vine din `core.tenant_settings.shipping_rules`.
    Etichetele sunt CHEI de traducere (`label_key`), ca front-end-ul să le treacă
    prin aceleași traduceri ca restul paginii.
    """
    if not get_settings().postgres_enabled:
        return _error("checkout_unavailable", 503)
    country = str(request.args.get("country") or "RO").upper()
    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        settings = get_tenant_settings(ctx.session, ctx.tenant_id)
        payload = {
            "delivery_methods": delivery_methods(settings, country),
            "payment_methods": payment_methods(settings),
            "countries": allowed_countries(settings),
            "currency": settings.get("currency") or "RON",
            "vat_rate": vat_rate(settings),
        }
    finally:
        _close_ctx(scope)
    return jsonify(payload)


def _autologin_window_minutes() -> int:
    try:
        return max(1, int((os.environ.get("AUTOLOGIN_WINDOW_MINUTES") or "30").strip()))
    except ValueError:
        return 30


def _form_locale(body: dict[str, Any] | None = None) -> str:
    lang = str((body or {}).get("lang") or "").lower()
    return lang if lang in ("ro", "en", "de", "hu", "bg", "el") else _locale()


def _phone_field(body: dict[str, Any], key: str = "phone", *,
                 required: bool = False):
    """Telefonul din corp, normalizat la E.164; (valoare, răspuns 400 sau None)."""
    from .. import phone as phone_rules

    value, error = phone_rules.validate(body.get(key), required=required,
                                        locale=_form_locale(body), field=key)
    if error is not None:
        return "", _validation_error([error], code=error["code"])
    return value, None


def _validation_error(errors: list[dict[str, Any]], code: str = "validation_failed"):
    """400 cu erori pe câmp. `code` permite un cod mai precis (`email_rejected`…),
    ca front-end-ul să poată afișa un mesaj dedicat, nu doar „date invalide"."""
    return jsonify({"status": "error", "error": code, "details": errors}), 400


def _remember_checkout_details(identity: IdentityRepo, user_id: str, data: Any,
                               company: dict[str, Any], *, shipping: dict[str, Any],
                               billing: dict[str, Any], same_billing: bool) -> None:
    """Salvează în contul clientului firma şi adresele folosite la comandă.

    Nimic din asta nu are voie să strice o comandă deja înregistrată: orice eroare se
    loghează şi se trece mai departe. Clientul şi-a primit comanda; o adresă care nu
    s-a salvat în cont e o neplăcere, nu un incident.
    """
    try:
        if company:
            identity.save_company(user_id, {
                "name": company.get("name", ""),
                "cui": company.get("vat", ""),
                "reg_com": company.get("reg", ""),
                # adresa de facturare a comenzii e adresa firmei
                "address_line": ", ".join(
                    part for part in (billing.get("line1"), billing.get("line2")) if part),
                "city": billing.get("city", ""),
                "county": billing.get("county", ""),
                "postal_code": billing.get("postal_code", ""),
                "country": billing.get("country", "RO"),
                "contact_email": getattr(data.customer, "email", ""),
                "contact_phone": getattr(data.customer, "phone", ""),
            })
    except Exception:                                     # noqa: BLE001
        log.exception("firma de facturare nu a putut fi salvată în cont")
    try:
        phone = getattr(data.customer, "phone", "")
        identity.save_address_if_new(
            user_id, {**shipping, "phone": phone},
            kind="both" if same_billing else "shipping")
        if not same_billing:
            identity.save_address_if_new(user_id, {**billing, "phone": phone},
                                         kind="billing")
    except Exception:                                     # noqa: BLE001
        log.exception("adresele comenzii nu au putut fi salvate în cont")


def _checkout_guest(body: dict[str, Any]):
    """`POST /api/orders` în formatul nou: comandă de vizitator, cu sau fără cont."""
    from pydantic import ValidationError

    try:
        data = CheckoutIn.model_validate(body)
    except ValidationError as exc:
        return _validation_error(format_errors(exc, _form_locale(body)))

    if data.website:                                   # honeypot
        return _error("spam_detected", 400)

    # Verificarea adresei se face aici, nu în schemă: are nevoie de rețea (MX, callout
    # SMTP) și trebuie să poată întoarce o SUGESTIE de corectare, nu doar un „invalid".
    # Nu cerem clientului niciun cod și nicio confirmare: dacă adresa pare bună, trece.
    from .contact_checks import check_email

    verdict = check_email(data.customer.email)
    if not verdict["ok"]:
        message = ("Domeniul adresei de e-mail nu primește mesaje"
                   if verdict["code"] == "invalid_domain"
                   else "Adresa de e-mail nu există la furnizorul de e-mail")
        detail: dict[str, Any] = {"loc": ["customer", "email"], "msg": message}
        if verdict.get("suggestion"):
            detail["suggestion"] = verdict["suggestion"]
            detail["msg"] = f"{message}. Ai vrut să scrii {verdict['suggestion']}?"
        return _validation_error([detail], code=verdict["code"])

    locale = _locale()
    # La easybox nu se cere adresă de livrare: rămâne doar cea de facturare, iar
    # „adresa de livrare" a comenzii devine lockerul (vezi `_locker_address`).
    shipping = data.address
    billing = data.billing_address or shipping

    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        settings = get_tenant_settings(ctx.session, ctx.tenant_id)

        # metodele se validează față de configurația magazinului, nu față de o listă fixă
        valid_delivery = {m["code"] for m in delivery_methods(settings, shipping.country)}
        valid_payment = {m["code"] for m in payment_methods(settings)}
        errors: list[dict[str, Any]] = []
        if data.delivery_type:
            pass                  # livrare v2: se validează cu tarifele şi lockerul
        elif data.delivery_method not in valid_delivery:
            errors.append({"loc": ["delivery_method"],
                           "msg": f"Metodă de livrare indisponibilă "
                                  f"({', '.join(sorted(valid_delivery))})"})
        if data.payment_method not in valid_payment:
            errors.append({"loc": ["payment_method"],
                           "msg": f"Metodă de plată indisponibilă "
                                  f"({', '.join(sorted(valid_payment))})"})
        if shipping.country not in allowed_countries(settings):
            errors.append({"loc": ["shipping_address", "country"],
                           "msg": "Nu livrăm în această țară"})
        if errors:
            return _validation_error(errors)

        cart_repo = CartRepo(ctx.session, ctx.tenant_id, ctx.tenant_slug)
        identity = IdentityRepo(ctx.session, ctx.tenant_id)

        lines, cart_id, err = _resolve_lines(ctx, cart_repo, data.cart_id, data.items, locale)
        if err is not None:
            return err

        # ── livrare v2: opţiunea aleasă trebuie să existe pentru adresa clientului ──
        delivery_v2: dict[str, Any] = {}
        shipping_dict = shipping.as_dict()
        if data.delivery_type:
            delivery_v2, v2_error = _resolve_delivery_v2(ctx, data, shipping, lines, locale)
            if v2_error is not None:
                return v2_error
            if delivery_v2.get("locker"):
                # adresa de livrare a comenzii = lockerul (AWB, admin, cont, e-mail,
                # WhatsApp, Baselinker citesc toate de aici)
                shipping_dict = _locker_address(delivery_v2["locker"],
                                                phone=data.customer.phone)

        # ── identitatea cumpărătorului ──────────────────────────────────────
        company = (
            {"name": data.customer.company.name, "vat": data.customer.company.cui,
             "reg": data.customer.company.reg}
            if data.customer.company else {}
        )
        session_token = None
        account_created = False
        # Flux card v2 (regula proprietarului, 21.09.2026): la plata cu cardul NU se
        # creează cont, NU se deschide sesiune şi NU pleacă nimic până la plata
        # confirmată. Datele clientului rămân pe comandă (snapshot) şi contul se face
        # din ele în webhook — `_finalize_paid_order`. Ramburs / transfer: neschimbat.
        is_card = data.payment_method == "card"
        # se reține ÎNAINTE de a lega tranzacția de userul guest, altfel verificările
        # de mai jos ar crede că vizitatorul era deja autentificat
        was_logged_in = bool(ctx.user_id)
        if was_logged_in:
            user_id = ctx.user_id
        elif is_card:
            user_id = None
        else:
            user_id, _is_new = identity.ensure_guest(
                email=data.customer.email, full_name=data.customer.full_name,
                phone=data.customer.phone, locale=locale, company=company,
                ip=_client_ip(),
            )
            set_session_context_for_user(ctx, user_id)

        # ── contul se creează ÎNTOTDEAUNA ──────────────────────────────────
        # Decizia proprietarului (17.09.2026): nu mai există „comandă ca vizitator".
        # Clientul își vede comenzile fără să se înregistreze separat, iar parola și-o
        # alege când vrea, din Setări cont — parola generată aici nu se trimite nicăieri
        # și nu o știe nimeni (`password_set_by_user = false`).
        account_existing = False
        if not was_logged_in and not is_card:
            if identity.is_guest(user_id):
                identity.promote_guest(
                    user_id, secrets.token_urlsafe(24),
                    full_name=data.customer.full_name, phone=data.customer.phone,
                    ip=_client_ip(), user_agent=request.headers.get("User-Agent", ""),
                    password_set_by_user=False,
                )
                # în cont se salvează adresa clientului, nu lockerul
                identity.upsert_address(user_id, shipping.as_dict(), make_default=True)
                session_token = identity.create_session(
                    user_id, ip=_client_ip(),
                    user_agent=request.headers.get("User-Agent", ""),
                )
                account_created = True
            else:
                # Adresa are deja cont. Comanda se leagă de el, dar NU deschidem
                # sesiunea: altfel oricine ar putea intra în contul altcuiva comandând
                # pe adresa lui. Clientul se autentifică singur, din e-mail sau din site.
                account_existing = True

        # ── totaluri și comandă ─────────────────────────────────────────────
        rates = currency_rates.get_rates()
        display_currency = currency_rates.currency_for_country(shipping.country)
        rate = float(currency_rates.convert_from_ron(1.0, display_currency, rates) or 1.0)

        sales = SalesRepo(ctx.session, ctx.tenant_id)
        customer_payload = {
            "customer_type": "company" if company else "individual",
            "name": data.customer.full_name,
            "first_name": data.customer.first_name,
            "last_name": data.customer.last_name,
            "phone": data.customer.phone,
            "email": data.customer.email,
            "country": shipping.country,
            "address": shipping.as_text(),
            "delivery_address": shipping_dict.get("address", ""),
            "company_name": company.get("name", ""),
            "company_vat": company.get("vat", ""),
            "company_reg": company.get("reg", ""),
        }
        if is_card:
            # tot ce trebuie ca să facem contul la plată, exact ca fluxul de acum
            customer_payload["checkout"] = {
                "same_billing": data.billing_address is None,
                "logged_in": was_logged_in,
                "ip": _client_ip(),
                "user_agent": (request.headers.get("User-Agent", "") or "")[:400],
            }
        try:
            order = sales.create_order(
                lines=lines,
                customer=customer_payload,
                shipping_address=shipping_dict,
                billing_address=billing.as_dict(),
                payment_method=data.payment_method,
                settings=settings,
                user_id=user_id,
                locale=locale,
                cart_id=cart_id,
                seller=settings.get("seller") or {},
                display_currency=display_currency,
                exchange_rate=rate,
                exchange_rate_date=(rates or {}).get("date"),
                ip=_client_ip(),
                delivery_method=(delivery_v2.get("delivery_method")
                                 or data.delivery_method),
                user_comments=data.notes,
                want_invoice=bool(company),
                shipping_override=(
                    delivery_v2["price"] if delivery_v2 else delivery_price(
                        settings, data.delivery_method, shipping.country,
                        sum(float(line.get("expected_price") or 0) for line in lines) or 0.0,
                    )
                ),
                is_guest_order=False,
                accepted_terms=True,
                delivery_type=delivery_v2.get("delivery_type"),
                courier_code=delivery_v2.get("courier", ""),
                delivery_point=delivery_v2.get("locker"),
                shipping_eta=delivery_v2.get("eta", ""),
            )
        except OutOfStock as exc:
            return _error("out_of_stock", 409, items=exc.items)
        except PriceChanged as exc:
            return _error("price_changed", 409, items=exc.items)
        except ValueError as exc:
            return _error(str(exc), 400)

        # ── ce a completat clientul rămâne în contul lui ────────────────────
        # Până acum, datele de facturare şi adresele introduse la checkout se pierdeau:
        # comanda le păstra, contul nu. Se salvează DUPĂ ce comanda a reuşit (dacă
        # `create_order` cade, nu rămânem cu o firmă salvată pentru o comandă care nu
        # există) şi cu dedublare, ca a zecea comandă la aceeaşi adresă să nu producă
        # al zecelea rând identic.
        if not is_card:
            _remember_checkout_details(
                identity, user_id, data, company,
                shipping=shipping.as_dict(), billing=billing.as_dict(),
                same_billing=(data.billing_address is None
                              or data.shipping_address is None),
            )

        from ..mail import notify

        # Ordinea contează: întâi „ai cont", apoi confirmarea comenzii — altfel clientul
        # citește despre o comandă într-un cont despre care încă nu știe că există.
        # (La card ambele sunt False aici: contul se face abia la plată.)
        if account_created or account_existing:
            notify.account_ready(
                ctx.session, tenant_id=ctx.tenant_id, to_email=data.customer.email,
                name=data.customer.full_name, locale=locale, user_id=user_id,
                existing=account_existing, phone=data.customer.phone,
            )

        # Plata cu cardul: comanda aşteaptă banii (`pending_payment`). Confirmarea,
        # WhatsApp-ul, copia magazinului şi Baselinker pleacă abia din webhook-ul
        # Stripe, după încasare (`_finalize_paid_order`). Ramburs / transfer: ca înainte.
        if not order.get("awaiting_payment"):
            notify.order_placed(
                ctx.session, tenant_id=ctx.tenant_id, order=order,
                customer=customer_payload, shipping=shipping_dict,
                billing=billing.as_dict(), locale=locale,
                order_id=order["order_id"], user_id=user_id,
            )
            _queue_baselinker(ctx, {**order, "customer": customer_payload},
                              order["order_id"], shipping=shipping_dict,
                              billing=billing.as_dict())
        payload = {
            "status": "ok",
            "order_number": order["order_number"],
            "id": order["order_number"],
            "order_status": order.get("status", "placed"),
            "payment_status": order.get("payment_status", "unpaid"),
            "awaiting_payment": bool(order.get("awaiting_payment")),
            "totals": order["totals"],
            "items": order["items"],
            "customer": customer_payload,
            "shipping_address": shipping_dict,
            "billing_address": billing.as_dict(),
            "delivery_method": order.get("delivery_method") or data.delivery_method,
            "delivery": order.get("delivery"),
            "payment_method": data.payment_method,
            "account_created": account_created,
            "account_existing": account_existing,
            # Nu mai există comenzi „de vizitator": fiecare comandă are un cont.
            "guest_order": False,
        }
        if session_token:
            payload["customer_token"] = session_token
            payload["account_id"] = user_id
    finally:
        _close_ctx(scope)

    response = make_response(jsonify(payload), 201)
    if session_token:
        _with_session_cookie(response, session_token)
    _remember_order(response, str(payload.get("order_number") or ""))
    return response


def _locker_address(locker: dict[str, Any], phone: str = "") -> dict[str, Any]:
    """Lockerul, în forma unei adrese de livrare (aceleaşi chei ca `AddressIn.as_dict`).

    Aşa îl văd, fără nicio modificare, AWB-ul, adminul, contul clientului, e-mailurile,
    WhatsApp-ul şi Baselinker — comanda la easybox NU are adresa clientului la livrare.
    """
    from ..delivery import locker_text

    name = str(locker.get("name") or "")
    parts = [name, locker.get("address"), locker.get("city"), locker.get("county"),
             locker.get("postal_code")]
    return {
        "label": name,
        "line1": str(locker.get("address") or name),
        "line2": name,
        "address": ", ".join(str(p).strip() for p in parts if p and str(p).strip()),
        "city": locker.get("city") or "",
        "county": locker.get("county") or "",
        "postal_code": locker.get("postal_code") or "",
        "postcode": locker.get("postal_code") or "",
        "country": "RO",
        "phone": phone or "",
        # marcajul punctului de livrare (citit de AWB şi de Baselinker)
        "delivery_point": True,
        "locker_id": str(locker.get("locker_id") or ""),
        "courier": locker.get("courier") or "",
        "locker_text": locker_text(locker),
    }


def _resolve_delivery_v2(ctx: "_Ctx", data: Any, shipping: Any,
                         lines: list[dict[str, Any]], locale: str):
    """Opţiunea de livrare v2 validată pe server (preţ din tarife, locker existent).

    Întoarce `(delivery, None)` sau `(None, răspuns_de_eroare)`. Preţul NU vine din
    browser: se recalculează din tarife, cu greutatea coletelor şi subtotalul coşului.
    """
    from .. import lockers

    courier = str(data.courier or "sameday").strip().lower()
    repo = CartRepo(ctx.session, ctx.tenant_id, ctx.tenant_slug)
    items = []
    for line in lines:
        price = float(line.get("expected_price") or 0)
        if not price:
            # liniile din `items[]` (compatibilitate) nu au preţ: îl luăm din catalog
            found = repo.resolve_product(product_id=str(line["product_id"])) or {}
            price = float(found.get("price_ron") or 0)
        items.append({"product_id": str(line["product_id"]), "qty": int(line.get("qty") or 1),
                      "unit_price_gross_ron": price})
    # la easybox, destinaţia e lockerul (judeţul lui decide tariful), nu adresa clientului
    locker = None
    county, city, country = shipping.county, shipping.city, shipping.country
    if data.delivery_type == "locker":
        found = lockers.get(ctx.session, courier, str(data.locker_id or "").strip())
        if found is None:
            return None, _validation_error([{"loc": ["locker_id"],
                                             "msg": "Lockerul ales nu mai este disponibil"}])
        locker = {k: found.get(k) for k in ("courier", "locker_id", "name", "address", "city",
                                            "county", "postal_code", "lat", "lng")}
        county, city, country = locker["county"], locker["city"], "RO"
    quote = shipping_quote(ctx, county=county, city=city, country=country, locale=locale,
                           items=items)
    option = next((o for o in quote["options"]
                   if o["courier"] == courier and o["delivery_type"] == data.delivery_type),
                  None)
    if option is None:
        return None, _validation_error([{
            "loc": ["delivery_type"],
            "msg": "Opțiunea de livrare nu este disponibilă pentru această adresă",
            "available": [o["code"] for o in quote["options"]]}])
    return {"delivery_type": data.delivery_type, "courier": courier, "price": option["price"],
            "eta": option["eta"], "locker": locker,
            "delivery_method": "locker" if data.delivery_type == "locker" else "courier",
            "parcels": quote["parcels"]}, None


def validate_order():
    """`POST /api/orders/validate` — verifică payload-ul de checkout FĂRĂ efecte.

    Rulează exact aceleași verificări ca `POST /api/orders` până **înainte** de
    orice scriere: schema pydantic (nume, e-mail, telefon, adresă completă, date de
    firmă), verificarea adresei de e-mail (MX / typo / callout SMTP) și potrivirea
    metodei de livrare, a metodei de plată și a țării cu configurația magazinului.

    Nu creează cont, nu creează comandă, nu trimite e-mail, nu atinge Baselinker și
    nu scrie nimic în bază (tranzacția se închide fără commit). Există ca să poată fi
    testată validarea — și ca formularul să poată verifica un pas înainte de „Trimite
    comanda" — fără să genereze comenzi reale.

    Răspuns: `200 {"status": "ok", "valid": true}` sau
    `400 {"status": "error", "error": "validation_failed"|"invalid_domain"|…,
          "details": [{"loc": [...], "msg": "..."}]}`.
    """
    from pydantic import ValidationError

    body = _body()
    try:
        data = CheckoutIn.model_validate(body)
    except ValidationError as exc:
        return _validation_error(format_errors(exc, _form_locale(body)))

    if data.website:                                   # honeypot
        return _error("spam_detected", 400)

    from .contact_checks import check_email

    verdict = check_email(data.customer.email)
    if not verdict["ok"]:
        message = ("Domeniul adresei de e-mail nu primește mesaje"
                   if verdict["code"] == "invalid_domain"
                   else "Adresa de e-mail nu există la furnizorul de e-mail")
        detail: dict[str, Any] = {"loc": ["customer", "email"], "msg": message}
        if verdict.get("suggestion"):
            detail["suggestion"] = verdict["suggestion"]
            detail["msg"] = f"{message}. Ai vrut să scrii {verdict['suggestion']}?"
        return _validation_error([detail], code=verdict["code"])

    shipping = data.address
    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        settings = get_tenant_settings(ctx.session, ctx.tenant_id)
        valid_delivery = {m["code"] for m in delivery_methods(settings, shipping.country)}
        valid_payment = {m["code"] for m in payment_methods(settings)}
        errors: list[dict[str, Any]] = []
        if data.delivery_type:
            pass                  # livrare v2: se validează cu tarifele şi lockerul
        elif data.delivery_method not in valid_delivery:
            errors.append({"loc": ["delivery_method"],
                           "msg": f"Metodă de livrare indisponibilă "
                                  f"({', '.join(sorted(valid_delivery))})"})
        if data.payment_method not in valid_payment:
            errors.append({"loc": ["payment_method"],
                           "msg": f"Metodă de plată indisponibilă "
                                  f"({', '.join(sorted(valid_payment))})"})
        if shipping.country not in allowed_countries(settings):
            errors.append({"loc": ["shipping_address", "country"],
                           "msg": "Nu livrăm în această țară"})
        if errors:
            return _validation_error(errors)
        # livrare v2: aceleaşi verificări ca la plasare (tarif disponibil + locker activ),
        # tot fără nicio scriere
        delivery_v2: dict[str, Any] = {}
        delivery_address = shipping.as_dict()
        if data.delivery_type:
            cart_repo = CartRepo(ctx.session, ctx.tenant_id, ctx.tenant_slug)
            lines, _cart_id, _err = _resolve_lines(ctx, cart_repo, data.cart_id, data.items,
                                                   _locale())
            delivery_v2, v2_error = _resolve_delivery_v2(ctx, data, shipping, lines, _locale())
            if v2_error is not None:
                return v2_error
            if delivery_v2.get("locker"):
                delivery_address = _locker_address(delivery_v2["locker"],
                                                   phone=data.customer.phone)
        normalized = {
            "customer": {
                "email": data.customer.email,
                "first_name": data.customer.first_name,
                "last_name": data.customer.last_name,
                "phone": data.customer.phone,
            },
            # la easybox: adresa de livrare a comenzii e lockerul
            "shipping_address": delivery_address,
            "customer_address": shipping.as_dict(),
            "billing_address": (data.billing_address or shipping).as_dict(),
            "delivery_type": data.delivery_type,
            "delivery": ({"courier": delivery_v2.get("courier"),
                          "delivery_type": delivery_v2.get("delivery_type"),
                          "price": delivery_v2.get("price"), "eta": delivery_v2.get("eta"),
                          "locker": delivery_v2.get("locker")} if delivery_v2 else None),
            "customer_type": "company" if data.customer.company else "individual",
        }
        if data.customer.company:
            normalized["customer"]["company"] = {
                "name": data.customer.company.name,
                "cui": data.customer.company.cui,
                "reg_com": data.customer.company.reg,
            }
    finally:
        # fără commit: ruta e strict read-only
        _close_ctx(scope)
    return jsonify({"status": "ok", "valid": True, "dry_run": True,
                    "normalized": normalized})


def _queue_baselinker(ctx: "_Ctx", order: dict[str, Any], order_id: str,
                      *, shipping: dict[str, Any] | None = None,
                      billing: dict[str, Any] | None = None) -> None:
    """Pune comanda în coada Baselinker, în aceeași tranzacție cu comanda.

    Doar în coadă — apelul HTTP îl face workerul. Dacă Baselinker e picat, comanda
    clientului se plasează oricum; asta e tot rostul cozii. Orice eroare de aici se
    înghite: o integrare nu are voie să rupă o vânzare.
    """
    try:
        from ..integrations.baselinker import settings as bl_settings, sync as bl_sync

        config = bl_settings.load(ctx.session, ctx.tenant_id)
        if not config.get("enabled"):
            return
        payload_order = dict(order)
        payload_order.setdefault("shipping_address", shipping or {})
        payload_order.setdefault("billing_address", billing or shipping or {})
        product_map = bl_sync.inventory_product_map(
            ctx.session, ctx.tenant_id, config,
            [str(item.get("sku") or "") for item in (payload_order.get("items") or [])],
        )
        bl_sync.enqueue(
            ctx.session, tenant_id=ctx.tenant_id, order_id=order_id,
            payload=bl_sync.build_order_payload(payload_order, config, product_map),
        )
    except Exception:                                        # noqa: BLE001
        log.exception("comanda nu a putut fi pusă în coada Baselinker")


def set_session_context_for_user(ctx: "_Ctx", user_id: str) -> None:
    """Leagă tranzacția de userul nou creat, ca politicile RLS să-l accepte."""
    from ..db import set_session_context

    set_session_context(ctx.session, user_id=user_id, actor_type="customer",
                        actor_id=user_id)
    ctx.user = {"user_id": user_id}


def _resolve_lines(ctx: "_Ctx", cart_repo: CartRepo, cart_id: str | None,
                   items: list[dict[str, Any]] | None, locale: str):
    """Liniile comenzii: din coșul din DB sau din `items[]` (compatibilitate)."""
    if cart_id is None and ctx.user_id:
        found = cart_repo.find_open(user_id=ctx.user_id, token_hash=None)
        cart_id = str(found) if found else None
    if cart_id is None and _cart_token():
        found = cart_repo.find_open(user_id=None, token_hash=hash_cart_token(_cart_token()))
        cart_id = str(found) if found else None

    lines: list[dict[str, Any]] = []
    if cart_id:
        cart_repo.reprice(cart_id, locale)      # oferta automată de ACUM, pe linii
        for item in cart_repo.read(cart_id, locale)["items"]:
            lines.append({"product_id": item["product_id"], "qty": item["qty"],
                          "expected_price": item["unit_price_gross_ron"]})
    if not lines:
        for item in items or []:
            if not isinstance(item, dict):
                continue
            product = _resolve(cart_repo, item)
            if product is None:
                return [], None, _error("unknown_product", 400)
            lines.append({"product_id": str(product["id"]),
                          "qty": int(item.get("qty") or 1)})
    if not lines:
        return [], None, _error("empty_cart", 400)
    return lines, cart_id, None


# ── implementările pentru rutele vechi, apelate din factory.py ──────────────

def login_customer():
    body = _body()
    email = normalize_email(body.get("email"))
    password = str(body.get("password") or "")
    if not email or not password:
        return _error("missing_login", 400)
    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        try:
            account = identity.authenticate(email, password)
        except ValueError as exc:
            # `account_disabled` se ridică numai după ce parola s-a dovedit corectă
            # (vezi `IdentityRepo.authenticate`), deci nu divulgă nimic unui străin.
            if str(exc) == "account_disabled":
                return _error("account_disabled", 403)
            return _error("invalid_login", 400)
        session_token = identity.create_session(
            account["user_id"], ip=_client_ip(),
            user_agent=request.headers.get("User-Agent", ""),
        )
        # ATENȚIE: contextul RLS trebuie setat ÎNAINTE de a atinge coșurile. Altfel
        # politica `own_cart` ascunde coșul userului (nu știe încă cine e), `find_open`
        # întoarce None și inserarea cade pe `carts_open_user_uk`.
        set_session_context_for_user(ctx, account["user_id"])
        cart_token = _cart_token()
        if cart_token:
            repo = CartRepo(ctx.session, ctx.tenant_id, ctx.tenant_slug)
            guest = repo.find_open(user_id=None, token_hash=hash_cart_token(cart_token))
            user_cart = repo.get_or_create(user_id=account["user_id"], token_hash=None,
                                           locale=_locale())
            if guest and str(guest) != user_cart:
                repo.merge(guest_cart_id=str(guest), user_cart_id=user_cart)
        addresses = identity.list_addresses(account["user_id"])
        payload = {
            "status": "ok",
            "account_id": account["user_id"],
            "email": account["email"],
            "name": account["name"],
            "customer_token": session_token,
            "account_type": "store_customer",
            "must_change_password": account["must_change_password"],
            "shipping_addresses": addresses,
            "active_shipping_address_id": next(
                (a["id"] for a in addresses if a["is_default"]), ""
            ),
        }
    finally:
        _close_ctx(scope)
    return _with_session_cookie(make_response(jsonify(payload), 200), session_token)


def list_customer_orders():
    try:
        scope, ctx = _open_ctx(require_user=True)
    except LookupError:
        return _error("unknown_tenant", 404)
    except PermissionError:
        return _error("missing_customer_session", 403)
    try:
        orders = SalesRepo(ctx.session, ctx.tenant_id).list_for_user(ctx.user_id)
        locale = _locale()
        for order in orders:
            _with_display_dates(order, locale)
            order["image_url"] = _thumbnail(ctx.tenant_slug, {
                "id": order.pop("id_for_image", ""), "sku": order.get("sku") or "",
                "image": order.get("image") or "",
            })
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "account_type": "store_customer", "orders": orders})


def create_return():
    """`POST /api/account/returns` pe Postgres."""
    body = _body()
    order_ref = str(body.get("order_id") or body.get("order_number") or "").strip()
    reason = str(body.get("reason") or "").strip()
    if not order_ref or len(reason) < 5:
        return _error("invalid_return_request", 400)
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        sales = SalesRepo(ctx.session, ctx.tenant_id)
        try:
            result = sales.create_return(user_id=ctx.user_id, order_number=order_ref,
                                         reason=reason, locale=_locale())
        except ValueError as exc:
            code = str(exc)
            status = 404 if code == "order_not_found" else 409
            return _error(code, status)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "id": result["return_number"],
                    "return_status": result["status"],
                    "order_id": result["order_number"]})


def list_returns():
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        items = SalesRepo(ctx.session, ctx.tenant_id).list_returns(ctx.user_id)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "returns": items})


def change_password():
    """`POST /api/account/change-password` pe Postgres (sesiunea curentă rămâne validă)."""
    body = _body()
    current = str(body.get("current_password") or "")
    new_password = str(body.get("new_password") or body.get("password") or "")
    if len(new_password) < 10:
        return _error("invalid_password_change", 400)
    opened, error = _require_user_ctx()
    if error is not None:
        return error
    scope, ctx = opened
    try:
        identity = IdentityRepo(ctx.session, ctx.tenant_id)
        profile = identity.get_profile(ctx.user_id) or {}
        # Contul creat automat la prima comandă are o parolă generată, pe care nu o
        # știe nimeni — nici clientul. A-i cere „parola veche" ar fi o ușă fără cheie:
        # singura cale ar rămâne „am uitat parola", pentru o parolă pe care n-a avut-o.
        needs_current = bool(profile.get("password_set_by_user", True))
        if needs_current:
            try:
                identity.authenticate(ctx.user["email"], current)
            except ValueError:
                return _error("invalid_login", 400)
        identity.set_password(ctx.user_id, new_password, password_set_by_user=True)
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "must_change_password": False,
                    "password_set_by_user": True,
                    "current_password_required": needs_current})


def create_order():
    from .. import cms

    body = _body()
    # Formatul NOU (checkout de vizitator) se recunoaște după `accept_terms` /
    # `customer.first_name`. Formatul vechi (storefront.js actual) rămâne suportat.
    customer_body = body.get("customer") or {}
    if "accept_terms" in body or "first_name" in customer_body:
        return _checkout_guest(body)
    if body.get("website") or (body.get("customer") or {}).get("website"):
        return _error("spam_detected", 400)
    customer = body.get("customer") or {}
    locale = _locale()

    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        settings = get_tenant_settings(ctx.session, ctx.tenant_id)
        cart_repo = CartRepo(ctx.session, ctx.tenant_id, ctx.tenant_slug)

        # 1) sursa liniilor: cart_id (nou) sau items[] (compatibilitate)
        cart_id = str(body.get("cart_id") or "") or None
        lines: list[dict[str, Any]] = []
        if cart_id is None and ctx.user_id:
            found = cart_repo.find_open(user_id=ctx.user_id, token_hash=None)
            cart_id = str(found) if found else None
        if cart_id is None and _cart_token():
            found = cart_repo.find_open(user_id=None, token_hash=hash_cart_token(_cart_token()))
            cart_id = str(found) if found else None
        if cart_id:
            cart_repo.reprice(cart_id, locale)
            for item in cart_repo.read(cart_id, locale)["items"]:
                lines.append({"product_id": item["product_id"], "qty": item["qty"]})
        if not lines:
            for item in body.get("items") or []:
                if not isinstance(item, dict):
                    continue
                product = _resolve(cart_repo, item)
                if product is None:
                    return _error("unknown_product", 400)
                lines.append({"product_id": str(product["id"]),
                              "qty": int(item.get("qty") or 1)})
        if not lines:
            return _error("empty_cart", 400)

        # 2) validări de client (aceleași reguli ca în cms.save_order)
        shipping_address = cms.normalize_shipping_address(customer, body.get("shipping_address"))
        if not customer.get("name") or not customer.get("phone") or not customer.get("email") \
                or not shipping_address.get("address"):
            return _error("missing_customer", 400)
        if not valid_email(normalize_email(customer.get("email"))):
            return _error("invalid_email", 400)
        customer_type = str(customer.get("customer_type") or "individual")
        if customer_type not in {"individual", "company"}:
            return _error("invalid_customer_type", 400)
        if customer_type == "company" and (not customer.get("company_name")
                                           or not customer.get("company_vat")):
            return _error("missing_company", 400)

        country = str(shipping_address.get("country") or "RO").upper()
        rates = currency_rates.get_rates()
        display_currency = currency_rates.currency_for_country(country)
        rate = float(currency_rates.convert_from_ron(1.0, display_currency, rates) or 1.0)

        sales = SalesRepo(ctx.session, ctx.tenant_id)
        try:
            order = sales.create_order(
                lines=lines,
                customer={
                    "customer_type": customer_type,
                    "name": str(customer.get("name") or ""),
                    "phone": str(customer.get("phone") or ""),
                    "email": normalize_email(customer.get("email")),
                    "country": country,
                    "address": shipping_address.get("address", ""),
                    "company_name": str(customer.get("company_name") or ""),
                    "company_vat": str(customer.get("company_vat") or ""),
                    "company_reg": str(customer.get("company_reg") or ""),
                },
                shipping_address=shipping_address,
                billing_address=body.get("billing_address") or shipping_address,
                payment_method=str(customer.get("payment_method")
                                   or body.get("payment_method") or ""),
                settings=settings,
                user_id=ctx.user_id,
                locale=locale,
                cart_id=cart_id,
                seller=settings.get("seller") or {},
                display_currency=display_currency,
                exchange_rate=rate,
                exchange_rate_date=(rates or {}).get("date"),
                ip=_client_ip(),
                delivery_method=str(body.get("delivery_method") or ""),
                user_comments=str(body.get("user_comments") or ""),
                want_invoice=bool(body.get("want_invoice")),
            )
        except OutOfStock as exc:
            return _error("out_of_stock", 409, items=exc.items)
        except PriceChanged as exc:
            return _error("price_changed", 409, items=exc.items)
        except ValueError as exc:
            return _error(str(exc), 400)

        from ..mail import notify

        if not order.get("awaiting_payment"):       # cardul: abia după plată
            notify.order_placed(
                ctx.session, tenant_id=ctx.tenant_id, order=order,
                customer=order.get("customer") or {
                    "email": normalize_email(customer.get("email")),
                    "name": customer.get("name")},
                shipping=shipping_address,
                billing=body.get("billing_address") or shipping_address, locale=locale,
                order_id=order["order_id"], user_id=ctx.user_id,
            )
            _queue_baselinker(ctx, order, order["order_id"], shipping=shipping_address,
                              billing=body.get("billing_address") or shipping_address)
        # `status` rămâne "ok" (contractul vechi al storefront.js); statusul comenzii
        # se întoarce separat, ca JS-ul să poată afișa eticheta tradusă.
        order["order_status"] = order.pop("status", "placed")
        payload = {"status": "ok", **order}
    finally:
        _close_ctx(scope)
    return _remember_order(make_response(jsonify(payload), 200),
                           str(payload.get("order_number") or ""))


# ───────────────────────────── livrare v2 ────────────────────────────────────

def _float_arg(name: str) -> float | None:
    try:
        raw = request.args.get(name)
        return float(raw) if raw not in (None, "") else None
    except ValueError:
        return None


@storefront_bp.get("/api/shipping/lockers")
def shipping_lockers():
    """Lockere active (easybox; FANbox când va exista): filtre + cele mai apropiate primele.

    `?county=&city=&q=&lat=&lng=&courier=&page=&per_page=` (max 100/pagină).
    `near_county=&near_city=` (doar cu `q`): preferinţă de ordonare, nu filtru — întâi
    oraşul, apoi judeţul, apoi restul (`lat/lng` rămâne prioritar).
    Răspuns: `{items, total, page, per_page, has_more, fallback}`; `fallback: "county"`
    când filtrul oraş+judeţ (fără `q`) n-a dat nimic şi s-au întors lockerele judeţului.
    """
    if not get_settings().postgres_enabled:
        return _error("unavailable", 503)
    from .. import lockers

    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        result = lockers.search(
            ctx.session, courier=str(request.args.get("courier") or "").strip().lower(),
            county=str(request.args.get("county") or "").strip(),
            city=str(request.args.get("city") or "").strip(),
            q=str(request.args.get("q") or "").strip(),
            near_county=str(request.args.get("near_county") or "").strip(),
            near_city=str(request.args.get("near_city") or "").strip(),
            lat=_float_arg("lat"), lng=_float_arg("lng"),
            page=int(request.args.get("page") or 1),
            per_page=int(request.args.get("per_page") or 20))
    finally:
        _close_ctx(scope)
    response = make_response(jsonify(result), 200)
    response.headers["Cache-Control"] = "public, max-age=600"
    return response


def _cart_lines_for_shipping(ctx: "_Ctx", locale: str) -> list[dict[str, Any]]:
    repo = CartRepo(ctx.session, ctx.tenant_id, ctx.tenant_slug)
    cart_id = None
    if ctx.user_id:
        found = repo.find_open(user_id=ctx.user_id, token_hash=None)
        cart_id = str(found) if found else None
    if cart_id is None and _cart_token():
        found = repo.find_open(user_id=None, token_hash=hash_cart_token(_cart_token()))
        cart_id = str(found) if found else None
    if not cart_id:
        return []
    return repo.read(cart_id, locale)["items"]


def shipping_quote(ctx: "_Ctx", *, county: str, city: str, country: str, locale: str,
                   items: list[dict[str, Any]]) -> dict[str, Any]:
    """Opţiunile de livrare pentru coşul dat: greutatea din colete + subtotalul la
    preţ de catalog (pragul de transport gratuit)."""
    from .. import packaging, shipping_rates

    settings = get_tenant_settings(ctx.session, ctx.tenant_id)
    parcels = packaging.for_lines(
        ctx.session, settings,
        [{"product_id": i["product_id"], "qty": i["qty"], "sku": i.get("sku") or "",
          "name": i.get("name") or ""} for i in items]) if items else None
    weight = (parcels or {}).get("total_weight_kg") or 1.0
    subtotal = round(sum(float(i.get("unit_price_gross_ron") or 0) * int(i.get("qty") or 0)
                         for i in items), 2)
    options = shipping_rates.options(ctx.session, ctx.tenant_id, county=county, city=city,
                                     weight=weight, subtotal=subtotal, locale=locale,
                                     country=country)
    return {"options": options, "weight_kg": weight, "subtotal_ron": subtotal,
            "parcels": {"count": (parcels or {}).get("count", 0),
                        "total_weight_kg": weight},
            "destination": {"county": county, "city": city, "country": country}}


@storefront_bp.get("/api/checkout/shipping-options")
def checkout_shipping_options():
    """`?county=&city=&postal_code=&country=RO&lang=` → opţiunile pentru coşul curent.

    Fiecare opţiune: `{code: "sameday:home", courier, courier_name, delivery_type, label,
    price, price_before_free, free, free_over_ron, eta, requires_locker}`.
    """
    if not get_settings().postgres_enabled:
        return _error("unavailable", 503)
    locale = _locale()
    try:
        scope, ctx = _open_ctx(cart_token=_cart_token() or None)
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        items = _cart_lines_for_shipping(ctx, locale)
        result = shipping_quote(
            ctx, county=str(request.args.get("county") or "").strip(),
            city=str(request.args.get("city") or "").strip(),
            country=str(request.args.get("country") or "RO").upper(), locale=locale,
            items=items)
        result["postal_code"] = str(request.args.get("postal_code") or "").strip()
    finally:
        _close_ctx(scope)
    return jsonify(result)


@storefront_bp.get("/api/offers/active")
def active_offers():
    """Ofertele automate ale temei EFECTIVE (calendar/manual) — nu ale `?theme=`/cookie.

    Excepție: previzualizarea semnată din admin (cookie `eva_preview`, `app.theme_preview`)
    → ofertele temei previzualizate, cu `"preview": true` și `Cache-Control: no-store`.

    `{"theme_id", "preview": bool, "offers": [{id, label, percent, all}]}`
    """
    from .. import cms, theme_offers
    from ..db import session_scope, set_session_context
    from ..repositories.tenant_repo import get_tenant_id

    lang = _locale()
    slug = _tenant_slug()
    with session_scope() as session:
        tenant_id = get_tenant_id(session, slug)
        if tenant_id is None:
            return _error("unknown_tenant", 404)
        set_session_context(session, tenant_id=tenant_id)
        preview_theme = theme_offers.display_theme_id()
        if preview_theme:
            theme_id = preview_theme
        else:
            try:
                theme_id = theme_offers.effective_theme_id(session, tenant_id, slug)
            except Exception:                            # noqa: BLE001
                theme_id = None
        offers = theme_offers.display_offers(session, tenant_id, slug) if theme_id else []
    body = {"theme_id": theme_id, "preview": bool(preview_theme),
            "offers": [{**{k: v for k, v in theme_offers.public_offer(o, lang).items()
                           if k in ("id", "label", "percent")},
                        "all": bool((o.get("selector") or {}).get("all"))} for o in offers]}
    response = make_response(jsonify(body), 200)
    response.headers["Cache-Control"] = ("private, no-store, max-age=0" if preview_theme
                                         else "public, max-age=60")
    return response


def register_storefront_api(app) -> None:
    from .public_brand import register as _register_public_brand

    _register_public_brand(storefront_bp)
    app.register_blueprint(storefront_bp)
    app.before_request(check_csrf)
    app.after_request(_issue_csrf_cookie)
    current = get_settings()
    log.info("API storefront montat (postgres_mode=%s)", postgres_mode())
    app.logger.info("rute noi: /api/cart*, /api/account/register|verify-email|logout "
                    "(storage_backend=%s)", current.storage_backend)


# ─────────────────────────── plată online (Stripe) ──────────────────────────
#
# Cardul nu atinge niciodată serverul nostru: clientul e trimis pe pagina Stripe
# Checkout. Rezultatul îl aflăm din webhook (`/api/payments/stripe/webhook`), nu din
# redirect — redirect-ul poate fi închis sau falsificat, webhook-ul se reîncearcă.

def _public_base() -> str:
    return (os.environ.get("PUBLIC_BASE_URL") or "https://cesiro.com").rstrip("/")


@storefront_bp.post("/api/payments/stripe/session")
def create_stripe_session():
    """Creează (sau refoloseşte) sesiunea de plată pentru o comandă cu cardul.

    Comanda se creează ÎNAINTE, prin `/api/orders`, cu status `pending_payment`: dacă
    plata eşuează sau clientul renunţă, rămâne o comandă pe care o poate relua 24 h.

    Acces: aceeaşi regulă ca pagina de confirmare — clientul logat (comanda lui) sau
    vizitatorul cu cookie-ul SEMNAT pus la plasare. Fără ea, oricine ar putea încerca
    numere de comandă şi ar vedea pe pagina Stripe produsele şi adresa altcuiva.

    Erori: 404 `order_not_found`, 409 `already_paid`, 409 `order_cancelled`,
    409 `payment_not_card`, 502 `payment_provider_error` (cu `detail`), 503
    `payments_unavailable`.
    """
    from ..payments import service as payments_service
    from ..payments.stripe_gateway import (StripeError, checkout_session_payload,
                                           create_checkout_session, expire_session,
                                           line_items_total_minor, expected_amount_minor,
                                           load_config, retrieve_session)

    config = load_config()
    if not config.usable:
        return _error("payments_unavailable", 503)
    body = _body()
    order_number = str(body.get("order_number") or body.get("id") or "").strip()
    if not order_number:
        return _error("missing_order", 400)

    order = order_for_confirmation(order_number)
    if order is None:
        return _error("order_not_found", 404)
    if str(order.get("payment_status") or "") == "paid":
        return _error("already_paid", 409)
    if str(order.get("status") or "") == "cancelled":
        return _error("order_cancelled", 409)
    if str(order.get("payment_method") or "") != "card":
        return _error("payment_not_card", 409)

    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        # accesul a fost dovedit mai sus (`order_for_confirmation`); RLS-ul vizitatorului
        # cere acelaşi parametru ca pagina de confirmare
        from ..db import set_session_context

        set_session_context(ctx.session, order_number=order_number)
        row = ctx.session.execute(
            text("SELECT id, created_at FROM sales.orders"
                 " WHERE tenant_id = CAST(:t AS uuid) AND order_number = :num"),
            {"t": ctx.tenant_id, "num": order_number},
        ).first()
        if row is None:
            return _error("order_not_found", 404)
        order_id = str(row.id)

        # ── fereastra de plată: CARD_PAYMENT_TIMEOUT_SECONDS de la plasare ──
        # După ea comanda e eşuată (browserul cheamă /payment-timeout, serverul prinde
        # restul). O sesiune nouă cerută după fereastră nu se mai deschide: comanda se
        # închide acum, cu aceeaşi regulă (întâi Stripe, apoi anulare tăcută).
        from ..payments import expiry

        now = int(time.time())
        created = int(row.created_at.timestamp()) if row.created_at else now
        if now - created > expiry.timeout_seconds():
            verdict = expiry.settle_or_cancel(
                ctx.session, ctx.tenant_id, order_number, config=config,
                finalize=_finalize_callback(ctx))
            if verdict == "paid":
                return _error("already_paid", 409)
            return _error("order_cancelled" if verdict == "payment_failed"
                          else "payment_window_closed", 409)
        # Stripe cere minimum 30 de minute de valabilitate; sesiunea se închide oricum
        # explicit (`expire`) la timeout, ca tabul rămas deschis să nu mai poată plăti.
        expires_at = now + 31 * 60

        # ── o sesiune încă deschisă se refoloseşte ──────────────────────────
        # Altfel fiecare reîncărcare a paginii de plată ar deschide o sesiune nouă,
        # iar clientul ar putea plăti de două ori aceeaşi comandă.
        for open_row in payments_service.open_sessions(ctx.session, order_id):
            try:
                existing = retrieve_session(config, open_row.session_id)
            except StripeError:
                continue
            if existing.get("status") == "open" and existing.get("url"):
                return jsonify({"status": "ok", "url": existing.get("url"),
                                "session_id": existing.get("id"), "reused": True,
                                "payment_timeout_seconds": expiry.timeout_seconds(),
                                "payment_deadline": _iso_utc(created + expiry.timeout_seconds())})
            if existing.get("status") == "complete":
                # plătită, dar webhook-ul încă n-a ajuns — nu deschidem alta
                return _error("payment_processing", 409)
            payments_service.mark_session_expired(ctx.session, open_row.id)


        try:
            payload = checkout_session_payload(
                order={**order, "order_id": order_id},
                customer_email=str((order.get("customer") or {}).get("email") or ""),
                success_url=f"{_public_base()}/checkout/confirmare/"
                            f"{quote(order_number)}?paid=1",
                cancel_url=f"{_public_base()}/checkout/plata/{quote(order_number)}",
                locale=str(order.get("locale") or "ro"),
                expires_at=expires_at,
                # textul de sub butonul „Plătește": limita, în limba comenzii
                timeout_seconds=expiry.timeout_seconds(),
            )
        except StripeError as exc:
            log.warning("comanda %s nu are linii de plată: %s", order_number, exc.code)
            return _error("payment_provider_error", 502, detail=exc.code)
        # Suma liniilor TREBUIE să fie totalul comenzii, altfel webhook-ul ar refuza
        # plata („sumă nepotrivită") după ce banii au fost deja luaţi.
        charged = line_items_total_minor(payload)
        expected = expected_amount_minor(order)
        if abs(charged - expected) > 1:
            log.error("comanda %s: liniile Stripe (%s) ≠ total (%s)", order_number,
                      charged, expected)
            return _error("payment_provider_error", 502, detail="amount_mismatch")

        payment_timeout = expiry.timeout_seconds()
        payment_deadline = _iso_utc(created + payment_timeout)
        attempt = payments_service.attempts_for(ctx.session, order_id)
        try:
            session_obj = create_checkout_session(
                config, payload,
                # aceeaşi încercare → aceeaşi sesiune, oricâte clicuri; o reluare după
                # expirare are alt număr, deci o sesiune nouă, nu cea expirată
                idempotency_key=f"order-{order_number}-{attempt}-{charged}",
            )
        except StripeError as exc:
            log.warning("sesiunea Stripe nu a putut fi creată: %s", exc.code)
            return _error("payment_provider_error", 502, detail=exc.code)

        payments_service.record_session(
            ctx.session, tenant_id=ctx.tenant_id, order_id=order_id,
            order_number=order_number,
            session_id=str(session_obj.get("id") or ""),
            amount=charged / 100.0, currency="RON",
            payment_intent=str(session_obj.get("payment_intent") or ""),
            expires_at=int(session_obj.get("expires_at") or expires_at),
        )
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "url": session_obj.get("url"),
                    "session_id": session_obj.get("id"),
                    "payment_timeout_seconds": payment_timeout,
                    "payment_deadline": payment_deadline})




@storefront_bp.post("/api/payments/stripe/webhook")
def stripe_webhook():
    """Evenimentele Stripe. Semnătura se verifică ÎNAINTE de orice altceva.

    Se răspunde 200 şi la evenimentele ignorate: altfel Stripe le retrimite la
    nesfârşit. Se răspunde 400 DOAR la o semnătură invalidă — acolo chiar vrem să se
    oprească.
    """
    from ..payments import service as payments_service
    from ..payments.stripe_gateway import StripeError, load_config, verify_signature

    config = load_config()
    if not config.configured:
        return _error("payments_unavailable", 503)
    raw = request.get_data() or b""
    signature = request.headers.get("Stripe-Signature", "")
    try:
        event = verify_signature(raw, signature, config.webhook_secret)
    except StripeError as exc:
        log.warning("webhook Stripe respins: %s", exc.code)
        return jsonify({"status": "error", "error": exc.code}), 400

    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        # RLS: webhook-ul nu are client autentificat, deci politica `own_orders` nu i-ar
        # arăta nicio comandă („comandă inexistentă" la fiecare plată). Semnătura e deja
        # verificată — evenimentul vine de la Stripe — deci deschidem accesul strict la
        # comanda numită în el, ca pagina de confirmare (migraţia 0017).
        number_hint = payments_service.order_number_of(event)
        if number_hint:
            from ..db import set_session_context

            set_session_context(ctx.session, order_number=number_hint)
        result = payments_service.handle_event(ctx.session, tenant_id=ctx.tenant_id,
                                               event=event)
        number = result.get("order_number") or ""
        if result.get("placed_now"):
            # fluxul nou: comanda devine plasată abia acum → confirmare completă
            _finalize_paid_order(ctx, number)
        elif result.get("paid_on_cancelled"):
            _alert_paid_on_cancelled(ctx, number)
        elif result.get("first_paid"):
            # comenzi cu cardul plasate înainte de 21.09.2026 (deja confirmate)
            _after_payment(ctx, number)
    except Exception:                                 # noqa: BLE001
        log.exception("webhook Stripe: procesarea a eșuat")
        raise
    finally:
        _close_ctx(scope)
    return jsonify({"status": "ok", "handled": result})


def _account_for_paid_order(ctx, row: Any, order: dict[str, Any]) -> tuple[str | None, bool]:
    """Pasul (a) al fluxului card v2: contul clientului, abia după plată.

    Aceleaşi reguli ca fluxul de cont automat de la ramburs:
      * clientul era logat la plasare (`user_id` pe comandă) → nimic nou;
      * adresa are deja cont real → comanda se leagă de el, FĂRĂ cont nou şi FĂRĂ
        sesiune (altfel oricine ar intra în contul altcuiva comandând pe adresa lui);
      * altfel → cont nou (parolă generată, necunoscută nimănui; clientul şi-o alege din
        „Setări cont"), adresa de livrare implicită.
    Apoi comanda se ataşează contului, iar firma şi adresele se salvează în cont.

    Întoarce `(user_id, cont_creat_acum)`. Rulează într-un savepoint: dacă ceva cade,
    plata rămâne înregistrată, iar contul se poate face manual.
    """
    customer = dict(order.get("customer") or {})
    email = normalize_email(customer.get("email"))
    if not email and not row.user_id:
        return None, False
    meta = customer.get("checkout") if isinstance(customer.get("checkout"), dict) else {}
    full_name = str(customer.get("name") or " ".join(
        part for part in (customer.get("first_name"), customer.get("last_name")) if part))
    phone = str(customer.get("phone") or "")
    company = ({"name": customer.get("company_name") or "",
                "vat": customer.get("company_vat") or "",
                "reg": customer.get("company_reg") or ""}
               if customer.get("company_name") else {})
    shipping = dict(order.get("shipping_address") or {})
    billing = dict(order.get("billing_address") or shipping)

    identity = IdentityRepo(ctx.session, ctx.tenant_id)
    from types import SimpleNamespace

    contact = SimpleNamespace(customer=SimpleNamespace(email=email, phone=phone))
    same_billing = bool(meta.get("same_billing", billing == shipping))
    if row.user_id:
        # clientul era logat la plasare: contul există, salvăm doar adresele şi firma
        savepoint = ctx.session.begin_nested()
        try:
            set_session_context_for_user(ctx, str(row.user_id))
            _remember_checkout_details(identity, str(row.user_id), contact, company,
                                       shipping=shipping, billing=billing,
                                       same_billing=same_billing)
            savepoint.commit()
        except Exception:                             # noqa: BLE001
            savepoint.rollback()
            log.exception("adresele comenzii plătite nu au putut fi salvate")
        return str(row.user_id), False

    savepoint = ctx.session.begin_nested()
    try:
        user_id, _new = identity.ensure_guest(
            email=email, full_name=full_name, phone=phone,
            locale=str(order.get("locale") or "ro"), company=company,
            ip=meta.get("ip") or None,
        )
        set_session_context_for_user(ctx, user_id)
        created = False
        if identity.is_guest(user_id):
            identity.promote_guest(
                user_id, secrets.token_urlsafe(24), full_name=full_name, phone=phone,
                ip=meta.get("ip") or None, user_agent=str(meta.get("user_agent") or ""),
                password_set_by_user=False,
            )
            identity.upsert_address(user_id, shipping, make_default=True)
            created = True
        ctx.session.execute(
            text(
                """
                UPDATE sales.orders
                   SET user_id = CAST(:u AS uuid),
                       customer = customer || jsonb_build_object(
                           'account_created_at_payment', CAST(:created AS boolean)),
                       updated_at = now()
                 WHERE id = :oid AND user_id IS NULL
                """
            ),
            {"u": user_id, "created": created, "oid": row.id},
        )
        _remember_checkout_details(identity, user_id, contact, company,
                                   shipping=shipping, billing=billing,
                                   same_billing=same_billing)
        savepoint.commit()
        return user_id, created
    except Exception:                                 # noqa: BLE001
        savepoint.rollback()
        log.exception("contul pentru comanda plătită %s nu a putut fi creat",
                      order.get("order_number"))
        return None, False


def _finalize_paid_order(ctx, order_number: str) -> None:
    """Comanda cu cardul tocmai a fost plătită şi a devenit `placed`.

    Ordinea STRICTĂ cerută de proprietar (flux card v2), o singură dată per comandă —
    `handle_event` întoarce `placed_now` doar pentru evenimentul care a mutat comanda
    din `pending_payment`, iar un eveniment repetat e oprit de `processed_events`:

      (a) contul clientului din datele de pe comandă (sau legarea de contul existent);
      (b) e-mail „Bine ai venit" — doar dacă s-a creat cont acum;
      (c) confirmarea „primită şi plătită";
      (d) copia către magazin;
      (e) WhatsApp;
      (f) Baselinker, cu plata marcată.

    Fiecare pas e izolat: banii sunt încasaţi, iar o notificare care cade nu are voie
    să întoarcă tranzacţia care marchează comanda plătită.
    """
    if not order_number:
        return
    try:
        order = SalesRepo(ctx.session, ctx.tenant_id).get_by_number(order_number)
    except Exception:                                 # noqa: BLE001
        log.exception("comanda plătită %s nu a putut fi citită", order_number)
        return
    if order is None:
        return
    row = ctx.session.execute(
        text("SELECT id, user_id, paid_at, payment_reference, total_ron FROM sales.orders"
             " WHERE tenant_id = CAST(:t AS uuid) AND order_number = :num"),
        {"t": ctx.tenant_id, "num": order_number},
    ).first()
    if row is None:
        return
    customer = dict(order.get("customer") or {})
    customer.setdefault("name", " ".join(
        part for part in (customer.get("first_name"), customer.get("last_name")) if part))
    customer.pop("checkout", None)
    locale = str(order.get("locale") or "ro")

    # (a) contul
    user_id, created = _account_for_paid_order(ctx, row, order)
    from ..mail import notify

    # (b) bun venit — înaintea confirmării, ca clientul să ştie de cont când o citeşte
    if created:
        try:
            # cu telefon: pe WhatsApp pleacă întâi „Bine ai venit", apoi (la pasul e)
            # confirmarea — ordinea e garantată de `clock_timestamp()` din coadă
            notify.account_ready(ctx.session, tenant_id=ctx.tenant_id,
                                 to_email=str(customer.get("email") or ""),
                                 name=str(customer.get("name") or ""), locale=locale,
                                 user_id=user_id, existing=False,
                                 phone=str(customer.get("phone") or ""),
                                 order_id=str(row.id))
        except Exception:                             # noqa: BLE001
            log.exception("e-mailul de bun venit pentru %s nu a putut fi pus în coadă",
                          order_number)
    # (c) confirmare, (d) magazin, (e) WhatsApp — în această ordine, în `order_placed`
    try:
        notify.order_placed(
            ctx.session, tenant_id=ctx.tenant_id, order=order, customer=customer,
            shipping=order.get("shipping_address") or {},
            billing=order.get("billing_address") or None,
            locale=locale, order_id=str(row.id), user_id=user_id, paid=True,
        )
    except Exception:                                 # noqa: BLE001
        log.exception("confirmarea comenzii plătite %s nu a putut fi pusă în coadă",
                      order_number)
    # (f) Baselinker
    _queue_baselinker(
        ctx,
        {**order, "customer": customer, "payment_status": "paid",
         "paid_at": row.paid_at.isoformat() if row.paid_at else None,
         "payment_reference": row.payment_reference or "",
         "payment_amount": float(row.total_ron or 0)},
        str(row.id), shipping=order.get("shipping_address") or {},
        billing=order.get("billing_address") or None,
    )


@storefront_bp.get("/api/orders/<order_number>/status")
def order_payment_status(order_number: str):
    """Starea scurtă a unei comenzi, pentru pagina de confirmare (flux card v2).

    Acces: clientul logat (comanda lui) sau cookie-ul SEMNAT `eva_orders` pus la
    plasare. Altfel 404, fără alte detalii.

    Răspuns: `{order_status, payment_status, payment_method, account_ready,
    account_created, logged_in}`.

    Autologin (sesiune de 30 de zile) pe orice apel, DOAR dacă toate sunt adevărate:
    comanda e `paid`; contul a fost creat chiar de plata ei (nu un cont existent — altfel
    oricine ar intra în contul altcuiva comandând pe adresa lui); cererea vine cu
    cookie-ul semnat al comenzii; nu există deja o sesiune; au trecut cel mult
    `AUTOLOGIN_WINDOW_MINUTES` (30) de la plată. Fără plată, nicio sesiune.
    `account_existing: true` = comanda a fost legată de un cont existent: fără autologin,
    clientul intră cu parola sau cu „Am uitat parola".
    """
    number = str(order_number or "").strip()
    if not number or not postgres_mode():
        return _error("order_not_found", 404)
    mine = order_for_current_user(number)
    has_ticket = number in recent_order_numbers()
    if mine is None and not has_ticket:
        return _error("order_not_found", 404)
    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    session_token = None
    try:
        from ..db import set_session_context

        set_session_context(ctx.session, order_number=number)
        row = ctx.session.execute(
            text(
                """
                SELECT o.id, o.status, o.payment_status, o.payment_method, o.user_id,
                       o.created_at, o.paid_at,
                       coalesce(o.customer ->> 'account_created_at_payment', '') AS created,
                       (o.paid_at IS NOT NULL AND o.paid_at > now()
                            - make_interval(mins => :window)) AS in_window
                  FROM sales.orders o
                 WHERE o.tenant_id = CAST(:t AS uuid) AND o.order_number = :num
                """
            ),
            {"t": ctx.tenant_id, "num": number, "window": _autologin_window_minutes()},
        ).first()
        if row is None:
            return _error("order_not_found", 404)
        paid = row.payment_status == "paid"
        account_ready = bool(paid and row.user_id)
        logged_in = bool(ctx.user_id)
        # Autologin pe ORICE apel de status (nu „o singură dată": primul apel poate veni
        # dintr-un tab care se închide), cât timp: comanda e plătită, contul e cel creat
        # CHIAR de această plată, cererea are cookie-ul semnat al comenzii, nu există
        # sesiune şi suntem în fereastra de `AUTOLOGIN_WINDOW_MINUTES` (30) de la plată.
        # Un cont EXISTENT nu primeşte autologin (altfel oricine ar intra în contul
        # altcuiva comandând pe adresa lui) — clientul foloseşte „Am uitat parola".
        if (account_ready and not logged_in and has_ticket and row.created == "true"
                and row.in_window):
            identity = IdentityRepo(ctx.session, ctx.tenant_id)
            set_session_context_for_user(ctx, str(row.user_id))
            session_token = identity.create_session(
                str(row.user_id), ip=_client_ip(),
                user_agent=request.headers.get("User-Agent", ""))
            ctx.session.execute(
                text("UPDATE sales.orders SET customer = customer || jsonb_build_object("
                     "'autologin_at', now()::text) WHERE id = :oid"),
                {"oid": row.id},
            )
            logged_in = True
        from ..payments import expiry as _expiry

        timeout = _expiry.timeout_seconds()
        payload = {"status": "ok", "order_number": number, "order_status": row.status,
                   "payment_timeout_seconds": timeout,
                   "payment_deadline": (_iso_utc(row.created_at.timestamp() + timeout)
                                        if getattr(row, "created_at", None) else None),
                   "payment_status": row.payment_status,
                   "payment_method": row.payment_method,
                   "account_ready": account_ready,
                   "account_created": bool(paid and row.created == "true"),
                   "account_existing": bool(account_ready and row.created != "true"),
                   "logged_in": logged_in}
    finally:
        _close_ctx(scope)
    response = make_response(jsonify(payload), 200)
    response.headers["Cache-Control"] = "no-store"
    if session_token:
        _with_session_cookie(response, session_token)
    return response


def _iso_utc(epoch: float) -> str:
    from datetime import datetime, timezone

    return datetime.fromtimestamp(epoch, tz=timezone.utc).isoformat()


def _finalize_callback(ctx):
    """Paşii de după plată pentru o sesiune găsită plătită la verificarea de timeout."""
    def finalize(order_number: str, result: dict[str, Any]) -> None:
        if result.get("placed_now"):
            _finalize_paid_order(ctx, order_number)
        elif result.get("paid_on_cancelled"):
            _alert_paid_on_cancelled(ctx, order_number)
    return finalize


@storefront_bp.post("/api/orders/<order_number>/payment-timeout")
def order_payment_timeout(order_number: str):
    """Chemat de pagina de plată/confirmare la expirarea limitei de plată
    (`CARD_PAYMENT_TIMEOUT_SECONDS`, din mediu) fără confirmarea plăţii.

    Acces: clientul logat (comanda lui) sau cookie-ul SEMNAT `eva_orders`; CSRF ca
    restul rutelor de scriere. Regula (vezi `payments/expiry.py`): întâi Stripe — o
    sesiune plătită se aplică şi răspunsul e `paid`; altfel sesiunea se expiră şi
    comanda se anulează TĂCUT. Idempotent.

    200 `{status: "paid" | "payment_failed" | "pending", order_status}`; `pending`
    înseamnă că Stripe nu a putut fi verificat — pagina reîncearcă peste câteva secunde.
    """
    from ..payments import expiry
    from ..payments.stripe_gateway import load_config

    number = str(order_number or "").strip()
    if not number or not postgres_mode():
        return _error("order_not_found", 404)
    if order_for_current_user(number) is None and number not in recent_order_numbers():
        return _error("order_not_found", 404)
    config = load_config()
    try:
        scope, ctx = _open_ctx()
    except LookupError:
        return _error("unknown_tenant", 404)
    try:
        from ..db import set_session_context

        set_session_context(ctx.session, order_number=number)
        verdict = expiry.settle_or_cancel(
            ctx.session, ctx.tenant_id, number,
            config=config if config.configured else None,
            finalize=_finalize_callback(ctx))
        if verdict == "not_found":
            return _error("order_not_found", 404)
        status_row = ctx.session.execute(
            text("SELECT status FROM sales.orders WHERE tenant_id = CAST(:t AS uuid)"
                 " AND order_number = :n"), {"t": ctx.tenant_id, "n": number}).first()
    finally:
        _close_ctx(scope)
    public = {"paid": "paid", "payment_failed": "payment_failed", "retry": "pending"}
    status = public.get(verdict, "paid" if verdict in ("placed", "confirmed", "processing",
                                                      "shipped", "delivered") else verdict)
    response = make_response(jsonify({
        "status": status, "order_number": number,
        "order_status": status_row.status if status_row else None,
    }), 200)
    response.headers["Cache-Control"] = "no-store"
    return response


def _alert_paid_on_cancelled(ctx, order_number: str) -> None:
    """Bani încasaţi pe o comandă deja anulată (timeout de plată depăşit).

    Ales: RAMBURSARE MANUALĂ, nu automată. Plata se marchează `failure_reason =
    'refund_required: …'` (vizibil în panou), magazinul primeşte o alertă, clientul nu
    primeşte nicio confirmare. Motiv: o rambursare automată e ireversibilă, iar
    proprietarul poate prefera să reactiveze livrarea (clientul chiar a plătit).
    """
    try:
        ctx.session.execute(
            text(
                """
                UPDATE sales.payments
                   SET failure_reason = 'refund_required: plată sosită după anularea '
                                        || 'comenzii (timeout) — rambursare manuală în Stripe',
                       updated_at = now()
                 WHERE order_number = :n AND provider = 'stripe' AND status = 'paid'
                """
            ),
            {"n": order_number},
        )
    except Exception:                                 # noqa: BLE001
        log.exception("marcajul de rambursare nu a putut fi scris pe %s", order_number)
    try:
        from ..mail.outbox import enqueue
        from ..mail.sender import resolve_settings

        settings = resolve_settings(ctx.session, ctx.tenant_id)
        if settings.order_notification_email:
            enqueue(ctx.session, tenant_id=ctx.tenant_id, template="paid_on_cancelled",
                    to_email=settings.order_notification_email,
                    subject=f"ATENȚIE: plată încasată pe comanda anulată {order_number}",
                    text_body=(f"Stripe a confirmat plata pentru {order_number}, dar "
                               f"comanda era deja anulată (plata nu a venit în timp).\n"
                               f"Verifică în panou: fie reactivezi manual livrarea, "
                               f"fie rambursezi plata din Stripe."),
                    html_body="", locale="ro")
    except Exception:                                 # noqa: BLE001
        log.exception("alerta de plată pe comandă anulată nu a putut fi trimisă")


def _after_payment(ctx, order_number: str) -> None:
    """E-mail + WhatsApp + Baselinker după o plată confirmată.

    Fiecare pas e izolat: banii sunt deja încasaţi, iar o notificare care cade nu are
    voie să întoarcă tranzacţia şi să lase comanda „neplătită".
    """
    if not order_number:
        return
    row = ctx.session.execute(
        text(
            """
            SELECT id, order_number, locale, customer, total_ron, currency, user_id
              FROM sales.orders
             WHERE tenant_id = CAST(:t AS uuid) AND order_number = :num
            """
        ),
        {"t": ctx.tenant_id, "num": order_number},
    ).first()
    if row is None:
        return
    customer = row.customer if isinstance(row.customer, dict) else {}
    try:
        from ..mail import notify

        notify.order_paid(
            ctx.session, tenant_id=ctx.tenant_id, order_number=row.order_number,
            to_email=str(customer.get("email") or ""),
            name=str(customer.get("name") or ""),
            locale=str(row.locale or "ro"), order_id=str(row.id),
            user_id=str(row.user_id) if row.user_id else None,
            phone=str(customer.get("phone") or ""),
            total=float(row.total_ron or 0), currency=str(row.currency or "RON"),
        )
    except Exception:                                 # noqa: BLE001
        log.exception("notificarea de plată nu a putut fi pusă în coadă")
    try:
        from ..integrations.baselinker import sync as bl_sync

        if hasattr(bl_sync, "push_payment"):
            bl_sync.push_payment(ctx.session, ctx.tenant_id, row.order_number,
                                 float(row.total_ron or 0))
    except Exception:                                 # noqa: BLE001
        log.exception("plata nu a putut fi trimisă în Baselinker")
