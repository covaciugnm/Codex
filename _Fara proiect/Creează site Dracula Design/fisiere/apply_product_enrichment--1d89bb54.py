"""Store sourced, multilingual product dossiers in the existing editable CMS fields.

Run in a migrate container with the site root mounted read-only at /import.
Explicit first import replaces the earlier brief descriptions. Subsequent runs
preserve descriptions edited in admin since the last import.
"""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

LABELS = {
 'ro': dict(technical='Fișă tehnică', nutrition='Repere nutriționale', ingredients='Compoziție și alergeni', storage='Păstrare', care='Îngrijire', history='Istorie documentată', story='Povestea Dracula', recipe='Inspirație culinară', styling='Idei de ținute și utilizare', sources='Surse și documentare', portions='Porții', pairing='Asociere', reference='Referință pentru 100 g de ingredient generic; nu reprezintă analiza produsului Dracula Food.', pending='Valori exacte ale produsului: în curs de confirmare.', source='Sursă', basis='Bază de referință', inspiration='Inspirație documentată', recipe_note='Rețetă editorială propusă; adaptare originală pentru această colecție.', occasion='Ocazie'),
 'en': dict(technical='Technical dossier', nutrition='Nutrition references', ingredients='Composition and allergens', storage='Storage', care='Care', history='A documented history', story='The Dracula story', recipe='Culinary inspiration', styling='Styling and use', sources='Sources and research', portions='Servings', pairing='Pairing', reference='Reference for 100 g of a generic ingredient; not an analysis of the Dracula Food product.', pending='Exact product values: awaiting confirmation.', source='Source', basis='Reference basis', inspiration='Documented inspiration', recipe_note='An editorial recipe proposal; an original adaptation for this collection.', occasion='Occasion'),
 'de': dict(technical='Technisches Dossier', nutrition='Nährwertreferenzen', ingredients='Zusammensetzung und Allergene', storage='Aufbewahrung', care='Pflege', history='Dokumentierte Geschichte', story='Die Dracula-Geschichte', recipe='Kulinarische Inspiration', styling='Styling und Verwendung', sources='Quellen und Recherche', portions='Portionen', pairing='Kombination', reference='Referenz für 100 g einer allgemeinen Zutat; keine Analyse des Dracula-Food-Produkts.', pending='Genaue Produktwerte: Bestätigung steht aus.', source='Quelle', basis='Referenzbasis', inspiration='Dokumentierte Inspiration', recipe_note='Ein redaktioneller Rezeptvorschlag; eine eigene Adaption für diese Kollektion.', occasion='Anlass'),
}
NUTRIENTS = {
 'kcal': ('Energie', 'Energy', 'Energie', 'kcal'),
 'energy_kj': ('Energie', 'Energy', 'Energie', 'kJ'),
 'energy_kcal': ('Energie', 'Energy', 'Energie', 'kcal'),
 'protein_g': ('Proteine', 'Protein', 'Eiweiß', 'g'),
 'fat_g': ('Grăsimi', 'Fat', 'Fett', 'g'),
 'saturated_fat_g': ('Grăsimi saturate', 'Saturated fat', 'Gesättigte Fettsäuren', 'g'),
 'saturates_g': ('Grăsimi saturate', 'Saturated fat', 'Gesättigte Fettsäuren', 'g'),
 'carbohydrate_by_difference_g': ('Carbohidrați USDA, inclusiv fibre', 'USDA carbohydrate, including fibre', 'USDA-Kohlenhydrate, einschließlich Ballaststoffen', 'g'),
 'carbohydrate_g': ('Carbohidrați', 'Carbohydrate', 'Kohlenhydrate', 'g'),
 'sugars_g': ('Zaharuri', 'Sugars', 'Zucker', 'g'),
 'fibre_g': ('Fibre', 'Fibre', 'Ballaststoffe', 'g'),
 'sodium_mg': ('Sodiu', 'Sodium', 'Natrium', 'mg'),
 'salt_g': ('Sare', 'Salt', 'Salz', 'g'),
}

def esc(value):
    return html.escape(str(value if value is not None else ''), quote=True)

def paragraphs(value):
    if isinstance(value, list):
        return '<ul>' + ''.join('<li>'+esc(v)+'</li>' for v in value) + '</ul>'
    return ''.join('<p>'+esc(p)+'</p>' for p in str(value or '').split('\n\n') if p)

def section(title, body):
    return '<section><h3>'+esc(title)+'</h3>'+body+'</section>'

def source_links(ids, sources):
    return '<ul>'+''.join('<li><a href="'+esc(sources[i]['url'])+'">'+esc(sources[i]['title'])+'</a></li>' for i in dict.fromkeys(ids) if i in sources and sources[i]['url'].startswith('https://'))+'</ul>'

def render_product(product, locale, sources):
    content=product['content'][locale]
    labels=LABELS[locale]
    parts=['<!--dracula-dossier-v1-->']
    rows=''.join('<tr><th>'+esc(r['label'])+'</th><td>'+esc(r['value'])+'</td></tr>' for r in content['technical'])
    parts.append(section(labels['technical'],'<table><tbody>'+rows+'</tbody></table>'))
    used=[]
    nutrition=product.get('nutrition')
    if nutrition:
        ref=nutrition.get('reference') or {}
        used.extend([ref['source_id']] if ref.get('source_id') else [])
        index=('ro','en','de').index(locale)
        rows=''
        for key,value in (ref.get('values') or {}).items():
            if value is None: continue
            nutrient=NUTRIENTS.get(key)
            if not nutrient: raise ValueError('Unknown nutrition key: '+key)
            display=str(value).replace('.',',') if locale in ('ro','de') else str(value)
            rows+='<tr><th>'+esc(nutrient[index])+'</th><td>'+esc(display)+' '+nutrient[3]+'</td></tr>'
        body=paragraphs(labels['reference'])+paragraphs(ref.get('food_name',''))
        if rows: body+='<table><tbody>'+rows+'</tbody></table>'
        body+=paragraphs((nutrition.get('note') or {}).get(locale,''))+paragraphs(labels['pending'])
        parts.append(section(labels['nutrition'],body))
    if content.get('ingredients') or content.get('allergens'):
        parts.append(section(labels['ingredients'],paragraphs(content.get('ingredients'))+paragraphs(content.get('allergens'))))
    for key in ('storage','care'):
        if content.get(key): parts.append(section(labels[key],paragraphs(content[key])))
    used.extend(content.get('storage_source_ids') or [])
    history=content.get('history') or {}
    used.extend(history.get('source_ids') or [])
    parts.append(section(labels['history'],paragraphs(history.get('text'))+source_links(history.get('source_ids',[]),sources)))
    parts.append(section(labels['story'],paragraphs(content.get('brand_story'))))
    recipe=content.get('recipe')
    if recipe:
        used.extend(recipe.get('inspiration_source_ids') or [])
        body='<h4>'+esc(recipe['title'])+'</h4>'+paragraphs(labels['recipe_note'])
        body+=paragraphs(labels['portions']+': '+str(recipe.get('servings','')))
        body+='<ul>'+''.join('<li>'+esc(v)+'</li>' for v in recipe['ingredients'])+'</ul>'
        body+='<ol>'+''.join('<li>'+esc(v)+'</li>' for v in recipe['steps'])+'</ol>'
        body+=paragraphs(labels['pairing']+': '+recipe.get('pairing',''))
        body+=paragraphs(recipe.get('allergens',''))+paragraphs(recipe.get('status',''))+paragraphs(recipe.get('inspiration_note',''))
        parts.append(section(labels['recipe'],body))
    if content.get('styling'):
        body=''
        for look in content['styling']:
            body+='<h4>'+esc(look['title'])+'</h4>'+paragraphs(look['pieces'])+paragraphs(labels['occasion']+': '+look['occasion'])+paragraphs(look['instructions'])
        parts.append(section(labels['styling'],body))
    parts.append(section(labels['sources'],source_links(used,sources)))
    return ''.join(parts)

def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--check',action='store_true',help='Validate content without accessing the database.')
    args=parser.parse_args()
    food=(args.root/'food/product-enrichment.json').exists()
    path=args.root/('food/product-enrichment.json' if food else 'design/product-enrichment.json')
    data=json.loads(path.read_text(encoding='utf-8'))
    sources={s['id']:s for s in data['sources']}
    rendered=[(p,loc,render_product(p,loc,sources)) for p in data['products'] for loc in ('ro','en','de')]
    assert len(rendered)==(57 if food else 15)
    if args.check:
        print(json.dumps({'products':len(data['products']),'translations':len(rendered),'sources':len(sources)}));return
    engine=create_engine(os.environ['SUPERUSER_DATABASE_URL'].replace('postgresql://','postgresql+psycopg://'))
    report={'updated_translations':0,'preserved_admin_edits':[]}
    with Session(engine) as session,session.begin():
        tenant=session.execute(text('SELECT id FROM core.tenants WHERE slug=:slug'),{'slug':os.environ['DEFAULT_TENANT']}).scalar_one()
        settings=session.execute(text('SELECT settings FROM core.tenant_settings WHERE tenant_id=:t FOR UPDATE'),{'t':tenant}).scalar_one()
        hashes=dict(settings.get('dossier_import_hashes') or {})
        for product,loc,body in rendered:
            row=session.execute(text('''SELECT tr.product_id,tr.description,tr.short_description FROM catalog.product_translations tr
                JOIN catalog.products p ON p.id=tr.product_id WHERE p.tenant_id=:t AND p.external_id=:ext AND tr.locale=:loc'''),{'t':tenant,'ext':product['id'],'loc':loc}).one()
            key=product['id']+':'+loc
            previous=hashes.get(key)
            edited=(digest(row.description or '')!=previous.get('description') or digest(row.short_description or '')!=previous.get('short_description')) if isinstance(previous,dict) else bool(previous and digest(row.description or '')!=previous)
            if edited:
                report['preserved_admin_edits'].append(key);continue
            session.execute(text('''UPDATE catalog.product_translations SET short_description=:intro,description=:body,
                seo_description=:seo,updated_at=now() WHERE product_id=:pid AND locale=:loc AND tenant_id=:t'''),{'intro':product['content'][loc]['intro'],'body':body,'seo':product['content'][loc]['intro'][:160],'pid':row.product_id,'loc':loc,'t':tenant})
            hashes[key]={'description':digest(body),'short_description':digest(product['content'][loc]['intro'])};report['updated_translations']+=1
        values={'dossier_import_hashes':hashes}
        if food:
            drafts=json.loads((args.root/'food/raisin-drafts.json').read_text(encoding='utf-8'))['products']
            values['dracula_preview_drafts']=all((args.root/'backend/public/assets/produse'/p['image_brief']['proposed_filename']).is_file() for p in drafts)
        session.execute(text('UPDATE core.tenant_settings SET settings=settings||CAST(:v AS jsonb),legal=jsonb_set(legal,\'{website}\',to_jsonb(CAST(:url AS text))),updated_at=now() WHERE tenant_id=:t'),{'v':json.dumps(values),'url':'https://'+('dracula-food.com' if food else 'dracula-design.com'),'t':tenant})
        ui=json.loads((args.root/'backend/stage_ui.json').read_text(encoding='utf-8'))
        for key,value in ui.items():
            params={'t':tenant,'k':key,'v':json.dumps(value)}
            changed=session.execute(text('UPDATE core.ui_translations SET values=CAST(:v AS jsonb),updated_at=now() WHERE tenant_id=:t AND key=:k'),params)
            if not changed.rowcount:
                session.execute(text('INSERT INTO core.ui_translations(tenant_id,key,values) VALUES(:t,:k,CAST(:v AS jsonb)) ON CONFLICT DO NOTHING'),params)
    engine.dispose()
    print(json.dumps(report,ensure_ascii=True))

if __name__=='__main__':main()
