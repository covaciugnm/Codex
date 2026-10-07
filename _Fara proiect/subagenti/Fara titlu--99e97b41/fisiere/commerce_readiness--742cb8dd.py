"""Fail-closed launch checks. Reports field paths only, never credentials.

This validates technical completeness and explicit merchant confirmation; it does
not certify the accuracy of tax, food labelling, or legal text.
"""
from __future__ import annotations

import math
import os
import re
from collections.abc import Mapping


def _number(value, minimum=0):
    try:
        return not isinstance(value, bool) and math.isfinite(float(value)) and float(value) >= minimum
    except (ValueError, TypeError):
        return False


def _present(value):
    return bool(str(value or '').strip())


def validate_readiness(cfg, products, env=None):
    """Return JSON-safe {ready, missing, ...}; safe to run on every live order."""
    env = os.environ if env is None else env
    missing = []

    def need(ok, field, reason):
        if not ok:
            missing.append({'field': field, 'reason': reason})

    settings = cfg.get('settings') or {}
    approval = settings.get('commerce_approval') or {}
    legal = cfg.get('legal') or {}
    seller = cfg.get('seller') or {}
    shipping = cfg.get('shipping_rules') or {}
    tax = cfg.get('tax') or {}
    for key in ('company_name', 'cui', 'registration', 'address', 'phone', 'email', 'website'):
        need(_present(legal.get(key)), 'legal.' + key, 'required_merchant_data')
    need(bool(re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', str(legal.get('email', '')))), 'legal.email', 'valid_contact_email_required')
    need(_present(seller.get('legal_name')), 'seller.legal_name', 'required_invoice_identity')
    need(seller.get('legal_name') == legal.get('company_name') and bool(legal.get('company_name')), 'seller.legal_name', 'must_match_legal_company_name')
    need(seller.get('address') == legal.get('address') and bool(legal.get('address')), 'seller.address', 'must_match_legal_address')
    need(approval.get('legal_pages_confirmed') is True, 'settings.commerce_approval.legal_pages_confirmed', 'review_all_enabled_languages_and_replace_drafts')
    need(cfg.get('currency') == 'RON', 'currency', 'current_checkout_and_shipping_engine_supports_RON')
    need(settings.get('demo_prices') is False, 'settings.demo_prices', 'disable_demo_prices_only_after_confirmation')
    need(tax.get('requires_review') is False, 'tax.requires_review', 'tax_configuration_requires_merchant_confirmation')
    need(_number(tax.get('vat_rate')) and float(tax.get('vat_rate', 0) or 0) <= 1, 'tax.vat_rate', 'explicit_fraction_between_0_and_1_required')
    need(isinstance(tax.get('prices_include_vat'), bool), 'tax.prices_include_vat', 'explicit_tax_price_policy_required')
    need(approval.get('tax_confirmed') is True, 'settings.commerce_approval.tax_confirmed', 'confirm_applicable_tax_treatment')
    countries = shipping.get('countries') or []
    need(isinstance(countries, list) and bool(countries), 'shipping_rules.countries', 'explicit_delivery_countries_required')
    rules = shipping.get('rules') or []
    for country in countries:
        need(any(r.get('country') in (country, '*') and _number(r.get('price_ron')) for r in rules if isinstance(r, dict)), 'shipping_rules.rules.' + str(country), 'explicit_nonnegative_delivery_rate_required')
    need(bool(shipping.get('delivery_methods')), 'shipping_rules.delivery_methods', 'explicit_delivery_methods_required')
    need(approval.get('shipping_confirmed') is True, 'settings.commerce_approval.shipping_confirmed', 'confirm_countries_rates_delivery_times_and_returns')
    methods = [m.get('code') if isinstance(m, Mapping) else m for m in shipping.get('payment_methods', [])]
    stripe_enabled = str(env.get('STRIPE_ENABLED', '')).lower() in ('true', '1', 'yes', 'on')
    if stripe_enabled and 'card' not in methods:
        methods.append('card')
    need(bool(methods), 'shipping_rules.payment_methods', 'explicit_payment_methods_required')
    need(all(m in ('cash_on_delivery', 'bank_transfer', 'card') for m in methods), 'shipping_rules.payment_methods', 'unsupported_payment_method')
    need(approval.get('payments_confirmed') is True, 'settings.commerce_approval.payments_confirmed', 'merchant_must_confirm_payment_methods')
    if 'bank_transfer' in methods:
        for key in ('iban', 'bank'):
            need(_present(legal.get(key)), 'legal.' + key, 'required_for_bank_transfer')
    if 'card' in methods:
        need(stripe_enabled, 'env.STRIPE_ENABLED', 'card_processor_must_be_enabled')
        for key, prefix in [('STRIPE_SECRET_KEY', 'sk_live_'), ('STRIPE_PUBLISHABLE_KEY', 'pk_live_'), ('STRIPE_WEBHOOK_SECRET', 'whsec_')]:
            need(str(env.get(key, '')).startswith(prefix), 'env.' + key, 'live_processor_configuration_required')
    # Acknowledgement flags alone cannot turn a demo price into a real price.
    reviewed = approval.get('products') or {}
    products = list(products)
    need(bool(products), 'products', 'published_catalog_required')
    for p in products:
        sku = str(p.get('sku') or p.get('external_id') or p.get('id'))
        base = 'products.' + sku
        review = reviewed.get(sku) or {}
        price = p.get('price_ron')
        need(_number(price, 0.01), base + '.price_ron', 'positive_real_price_required')
        need(p.get('needs_price_review') is False, base + '.needs_price_review', 'product_price_requires_confirmation')
        need(_number(review.get('confirmed_price_ron'), 0.01) and _number(price, 0.01) and abs(float(review['confirmed_price_ron']) - float(price)) < 0.005, base + '.confirmed_price_ron', 'confirmation_must_match_current_product_price')
        need(p.get('manage_stock') is True and _number(p.get('stock_quantity')), base + '.stock_quantity', 'managed_nonnegative_stock_required')
        need(review.get('stock_confirmed') is True, base + '.stock_confirmed', 'demo_inventory_requires_confirmation')
        need(review.get('content_confirmed') is True, base + '.content_confirmed', 'confirm_description_images_variants_and_product_information')
        if cfg.get('tenant') == 'dracula-food':
            need(review.get('food_information_confirmed') is True, base + '.food_information_confirmed', 'confirm_ingredients_allergens_quantity_nutrition_origin_and_storage')
    return {'schema_version': 1, 'tenant': cfg.get('tenant'), 'ready': not missing,
            'commerce_mode': env.get('COMMERCE_MODE', 'demo'),
            'activation_requested': env.get('COMMERCE_READY') == 'true',
            'published_product_count': len(products), 'missing': missing,
            'scope': 'merchant_data_and_checkout_configuration; email_and_public_delivery_checked_separately'}


def database_readiness(session, tenant_id, cfg=None, env=None):
    """Use the existing tenant-scoped transaction; no database writes."""
    from sqlalchemy import text
    from .repositories.tenant_repo import get_tenant_settings
    cfg = cfg or get_tenant_settings(session, tenant_id)
    rows = session.execute(text('''SELECT id,external_id,sku,price_ron,stock_quantity,
        manage_stock,needs_price_review FROM catalog.products
        WHERE tenant_id=:t AND status='published' ORDER BY sku'''), {'t': tenant_id}).mappings()
    return validate_readiness(cfg, rows, env)
