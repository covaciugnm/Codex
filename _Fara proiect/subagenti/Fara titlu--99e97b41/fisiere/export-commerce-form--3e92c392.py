#!/usr/bin/env python3
"""Export merchant input blanks without changing the DB or demo configuration."""
import csv
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
is_food = root.name == 'dracula-food'
tenant = 'dracula-food' if is_food else 'dracula-design'
content = json.loads((root / 'backend/dracula-content.json').read_text(encoding='utf-8'))
address = 'Dracula-Farm' if is_food else 'Dracula-Castel (Castelul-Dracula)'
form = {
    'tenant': tenant,
    'instructions': 'Firma si adresa de mai jos sunt deja confirmate de proprietar si se pastreaza. Null/false inseamna informatie inca nefurnizata. Preturile curente sunt demonstrative. Nu introduce parole sau chei in acest formular.',
    'confirmed_identity': {'company_name': 'Dracula-Company', 'address': address},
    'legal_to_complete': {key: None for key in ['cui', 'registration', 'email', 'phone', 'website', 'iban_if_bank_transfer', 'bank_if_bank_transfer']},
    'tax_to_complete': {'vat_rate_fraction': None, 'prices_include_vat': None, 'confirmed': False},
    'shipping_to_complete': {'countries': [], 'rates_ron_by_country': {}, 'delivery_times_by_country': {}, 'returns_instructions': None, 'confirmed': False},
    'payments_to_complete': {'enabled_methods': [], 'card_provider_if_needed': None, 'confirmed': False},
    'legal_pages_reviewed_in_all_enabled_languages': False,
    'products': []
}
for p in content['products']:
    item = {'sku': p['sku'], 'name_ro': p['name']['ro'], 'current_demo_price_ron': p['price'],
            'confirmed_price_ron': None, 'actual_stock_quantity': None, 'stock_confirmed': False,
            'content_confirmed': False}
    if is_food:
        item['food_information_confirmed'] = False
        item['food_information'] = {key: None for key in ['net_quantity', 'ingredients', 'allergens', 'nutrition', 'origin', 'storage', 'shelf_life']}
    else:
        item['product_information'] = {key: None for key in ['materials', 'sizes', 'care', 'variants_stock']}
    form['products'].append(item)
target = root / 'FORMULAR-DATE-COMERCIALE.json'
target.write_text(json.dumps(form, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
with (root / 'FORMULAR-PRETURI-STOCURI.csv').open('w', newline='', encoding='utf-8-sig') as stream:
    writer = csv.writer(stream)
    writer.writerow(['SKU', 'Produs', 'Pret demonstrativ RON', 'Pret real confirmat RON', 'Stoc real', 'Informatii produs confirmate'])
    for p in form['products']:
        writer.writerow([p['sku'], p['name_ro'], p['current_demo_price_ron'], '', '', ''])
print(f'{tenant}: exported {len(form["products"])} products; confirmed identity preserved.')
