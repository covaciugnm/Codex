import json
from pathlib import Path

root = Path('outputs/dracula-food')
categories = [
    ['stafide-naturale', {'ro': 'Stafide naturale & soiuri', 'en': 'Natural raisins & varieties', 'de': 'Naturrosinen & Sorten'}],
    ['stafide-aromatizate', {'ro': 'Stafide aromatizate & infuzate', 'en': 'Flavoured & infused raisins', 'de': 'Aromatisierte & verfeinerte Rosinen'}],
]
for relative in ('food/overrides.json', 'backend/dracula-content.json'):
    path = root / relative
    data = json.loads(path.read_text(encoding='utf-8'))
    existing = {row[0] for row in data['categories']}
    data['categories'].extend(row for row in categories if row[0] not in existing)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sql_literal(value):
    return "'" + value.replace("'", "''") + "'"

statements = ['BEGIN;']
for position, (code, translations) in enumerate(categories, start=3):
    statements.append(f"INSERT INTO catalog.categories(tenant_id,external_id,position) SELECT id,{sql_literal(code)},{position} FROM core.tenants WHERE slug='dracula-food' ON CONFLICT DO NOTHING;")
    for lang, name in translations.items():
        statements.append(f"INSERT INTO catalog.category_translations(category_id,tenant_id,locale,name,slug) SELECT c.id,c.tenant_id,{sql_literal(lang)},{sql_literal(name)},{sql_literal(code)} FROM catalog.categories c JOIN core.tenants t ON t.id=c.tenant_id WHERE t.slug='dracula-food' AND c.external_id={sql_literal(code)} ON CONFLICT DO NOTHING;")
statements.append('COMMIT;')
(root / 'backend/apply_food_categories.sql').write_text('\n'.join(statements) + '\n', encoding='utf-8')
print('Two categories prepared with RO/EN/DE translations.')
