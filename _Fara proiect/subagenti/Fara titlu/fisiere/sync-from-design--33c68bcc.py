"""Refresh shared SOURCE code, then apply Food data/branding. No runtime data copied.

Usage: python ops/sync-from-design.py /path/to/dracula-design-office
Never run concurrently with a Food source edit. Does not start containers.
"""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'.env', '.git', 'node_modules', '__pycache__', '.pytest_cache', '.venv', 'venv', 'data', 'backups', 'dist', 'assets', 'test_integration.py', 'test_admin.py'}

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding='utf-8', newline='\n')

def apply(source):
    source = source.resolve()
    if source == ROOT or not (source/'backend/app/dracula.py').is_file():
        raise SystemExit('Specify the Dracula Design source project, never its data directory.')
    for name in ['backend', 'frontend', 'database']:
        shutil.copytree(source/name, ROOT/name, dirs_exist_ok=True,
                        ignore=lambda parent, names: set(names) & EXCLUDED)
    for name in ['docker-compose.yml', 'docker-compose.cloudflare.yml', '.env.example', '.gitignore']:
        shutil.copy2(source/name, ROOT/name)
    for name in ['prepare.py', 'start.sh', 'backup.sh', 'start-cloudflare.sh', 'CLOUDFLARE.md']:
        shutil.copy2(source/'ops'/name, ROOT/'ops'/name)

    # Brand only this shop's copy. Runtime secrets and databases remain independent.
    for path in list((ROOT/'backend').rglob('*.py')) + list((ROOT/'frontend/src').rglob('*.ts')) + list((ROOT/'frontend/src').rglob('*.tsx')) + list((ROOT/'ops').glob('*')) + [ROOT/'docker-compose.yml', ROOT/'docker-compose.cloudflare.yml', ROOT/'.env.example']:
        if not path.is_file() or path.name == Path(__file__).name:
            continue
        value = path.read_text(encoding='utf-8')
        for old, new in [('dracula-design', 'dracula-food'), ('dracula_design', 'dracula_food'), ('owner@dracula.local', 'owner@dracula-food.local'), ('4181', '4183'), ('dracula_admin_rt', 'dracula_food_admin_rt'), ('dracula_cart', 'dracula_food_cart'), ('dracula_session', 'dracula_food_session'), ('dracula_orders', 'dracula_food_orders'), ('dracula_csrf', 'dracula_food_csrf'), ('eva_consent', 'dracula_food_consent'), ('Dracula Design Office', 'Dracula Food'), ('Dracula Design', 'Dracula Food'), ('dracula.admin.', 'dracula.food.admin.')]:
            value = value.replace(old, new)
        write(path, value)

    cloudflare = ROOT/'ops/CLOUDFLARE.md'
    value = cloudflare.read_text(encoding='utf-8')
    value = value.replace('Stack separat de CESIRO și Dracula Food.', 'Stack separat de CESIRO și Dracula Design.')
    value = value.replace('Nu folosi tokenul CESIRO sau Food.', 'Nu folosi tokenul CESIRO sau Design.')
    write(cloudflare, value)

    overlay = json.loads((ROOT/'food/overrides.json').read_text(encoding='utf-8'))
    email_render = ROOT/'backend/app/mail/render.py'
    write(email_render, email_render.read_text(encoding='utf-8').replace('/assets/brand/dracula-food-logo-auriu.jpeg', overlay['brand']['logo']))
    content = json.loads((source/'backend/dracula-content.json').read_text(encoding='utf-8'))
    content['products'] = json.loads((ROOT/'food/catalog.json').read_text(encoding='utf-8'))
    content['categories'] = overlay['categories']
    for product in content['products']:
        required = {'id', 'sku', 'price', 'category', 'image', 'name', 'description', 'details'}
        if required - product.keys():
            raise SystemExit(f"Incomplete food product: missing {required - product.keys()}")
        if product['category'] not in [c[0] for c in overlay['categories']]:
            raise SystemExit('Product must use a configured Food category.')
        for field in ['name', 'description', 'details']:
            if not all(product[field].get(lang) for lang in ['ro','en','de']):
                raise SystemExit('Initial product content must include RO, EN and DE.')
        if not product['image'].startswith('/assets/produse/') or '..' in product['image']:
            raise SystemExit('Food product image must be a local /assets/produse/ path.')
    content['ui'].update(overlay['ui'])
    for page in content['pages']:
        page.update(overlay['pages'].get(page['slug'], {}))
    serialized = json.dumps(content, ensure_ascii=False, indent=2)
    for old,new in [('Dracula Design Office','Dracula Food'),('DRACULA DESIGN OFFICE','DRACULA FOOD'),('Dracula Design','Dracula Food'),('Dracula-Castel (Castelul-Dracula)','Dracula-Farm'),('Dracula-Castel','Dracula-Farm')]:
        serialized=serialized.replace(old,new)
    write(ROOT/'backend/dracula-content.json',serialized+'\n')

    seed = (ROOT/'backend/seed_dracula.py').read_text(encoding='utf-8')
    seed = seed.replace('/assets/brand/dracula-food-logo-auriu.jpeg', overlay['brand']['logo'])
    seed = re.sub(r"'dracula_images':\{[^}]*\}", "'dracula_images':"+repr(overlay.get('images', {'hero':overlay['brand']['logo'],'collection':overlay['brand']['logo'],'scarf':overlay['brand']['logo']})), seed)
    seed = seed.replace('Dracula-Castel (Castelul-Dracula)', 'Dracula-Farm')
    seed = re.sub(r"for n,\(code,names\) in enumerate\(\[.*?\]\):", "for n,(code,names) in enumerate(content['categories']):", seed)
    seed = seed.replace("'/assets/produse/dracula-food-'+p['image']+'.jpeg'", "p['image']")
    seed = seed.replace("print('Dracula seeded: 5 products, 14 pages, RO/EN/DE; existing data preserved.')", "print(f\"Dracula Food seeded: {len(content['products'])} products; existing data preserved.\")")
    write(ROOT/'backend/seed_dracula.py', seed)

    for name in ['shop.js', 'index.html']:
        path = ROOT/'backend/public'/name
        value = path.read_text(encoding='utf-8')
        for old,new in [('Dracula Design Office','Dracula Food'),('Dracula Design','Dracula Food'),('dracula.language','dracula.food.language'),('dracula.cookies','dracula.food.cookies'),('dracula_csrf','dracula_food_csrf'),('/assets/brand/dracula-design-logo-auriu.jpeg',overlay['brand']['logo']), ("['all','business','everyday','women']", "['all','gourmet','pantry','gifts']"), ('D<span>D</span>','D<span>F</span>')]:
            value=value.replace(old,new)
        if name == 'index.html':
            value=value.replace('</head>', '<link rel="stylesheet" href="/assets/brand/food.css"></head>')
        write(path,value)

    path=ROOT/'frontend/index.html'
    write(path,path.read_text(encoding='utf-8').replace('Dracula Design','Dracula Food'))
    for name in ['package.json','package-lock.json']:
        path=ROOT/'frontend'/name
        write(path,path.read_text(encoding='utf-8').replace('dracula-design-admin','dracula-food-admin'))
    logo=ROOT/'food/assets/dracula-food-logo.jpeg'
    if not logo.is_file():
        raise SystemExit('Original Food logo required at food/assets/dracula-food-logo.jpeg')
    (ROOT/'backend/public/assets/brand').mkdir(parents=True,exist_ok=True)
    shutil.copy2(logo,ROOT/'backend/public/assets/brand/dracula-food-logo.jpeg')
    shutil.copy2(ROOT/'food/food.css',ROOT/'backend/public/assets/brand/food.css')
    # Supplied product assets, if any, stay in Food only and are never copied from Design.
    products=ROOT/'food/assets/produse'
    if products.exists():
        shutil.copytree(products,ROOT/'backend/public/assets/produse',dirs_exist_ok=True)
    manifest={'source':'Dracula Design shared engine, source only','logo_sha256':hashlib.sha256(logo.read_bytes()).hexdigest(),'products':len(content['products']),'public_ui_keys':len([k for k in content['ui'] if not k.startswith('admin.')]),'languages':['ro','en','de'],'database':'dracula_food','volume':'dracula_food_pgdata','project':'dracula-food','preview_port':4183}
    write(ROOT/'food/build-manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(manifest,ensure_ascii=False))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    apply(parser.parse_args().source)
