from pathlib import Path
import csv, json, re, collections, hashlib, unicodedata
from docx import Document

out=Path(__file__).parent
ev=out/'evidence-v2'; ev.mkdir(exist_ok=True)
d=Document(out/'Audituri/Audit.Claude.V1.0.docx')
items=[]
for t in d.tables:
    for r in t.rows:
        c=r.cells
        if re.fullmatch(r'[OP]\d+\.\d+',c[0].text):
            items.append(dict(id=c[0].text,text=c[1].text,priority=c[2].text))
(ev/'audit-claude.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
src=Path('U:/cesiro1-site/wc-product-export-16-9-2026-1789549595309.csv')
a=list(csv.DictReader(src.open(encoding='utf-8-sig',newline='')))
def fold(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
rules=[('Seturi',r'\b(set|serviciu)\b.*(farfur|masa|vesel|cana|cani|cesti|ceai|boluri)'),('Farfurii',r'farfur'),('Boluri',r'\bbol|salatier'),('Căni și cești',r'\bcana|\bcani|ceasca|cesti|pahar'),('Servire și tacâmuri',r'tacam|lingur|furcul|platou|cutit|cutite'),('Gătit',r'cratita|oala|tigaie|copt|termorez'),('Decor și grădină',r'vaza|ghivec|lumanar|figurina|planter'),('Detergenți',r'detergent|degresant|solutie|dezinfect|domestos'),('Consumabile',r'sac|lavet|buret|manus|consumabil|prosop hartie'),('Alte familii',r'.')]
sample=[]; counts={}
partition={label:[] for label,pat in rules}
for x in a:
    for label,pat in rules:
        if re.search(pat,fold(x['Nume'])):
            partition[label].append(x);break
for label,pat in rules:
    pool=partition[label]
    pool.sort(key=lambda x:hashlib.sha256(x['ID'].encode()).hexdigest())
    counts[label]=len(pool)
    chosen=pool[:5]
    special=next((x for x in pool if x['Tip']=='variable'),None)
    if special is not None and special not in chosen:chosen[-1]=special
    for x in chosen:
        attrs={x.get('Nume atribut '+str(i),''):x.get('Valoare (valori) atribut '+str(i),'') for i in range(1,9) if x.get('Nume atribut '+str(i),'')}
        missing=[k for k in ['SKU','GTIN, UPC, EAN sau ISBN','Descriere','Imagini','Greutate (kg)'] if not x.get(k,'').strip()]
        sample.append(dict(family=label,id=x['ID'],sku=x['SKU'],name=x['Nume'],type=x['Tip'],attributes=attrs,missing=missing))
stats=dict(source=str(src),snapshot='2026-09-16 (data din numele fișierului)',read_date='2026-10-21',sha256=hashlib.sha256(src.read_bytes()).hexdigest(),rows=len(a),unique_ids=len({x['ID'] for x in a}),unique_nonempty_skus=len({x['SKU'] for x in a if x['SKU']}),types=dict(collections.Counter(x['Tip'] for x in a)),published=dict(collections.Counter(x['Publicat'] for x in a)),missing={k:sum(not x.get(k,'').strip() for x in a) for k in ['SKU','GTIN, UPC, EAN sau ISBN','Descriere','Imagini','Greutate (kg)','Stoc','Preț obișnuit']},sample_size=len(sample),sampling_groups=counts,sample_missing=dict(collections.Counter(k for x in sample for k in x['missing'])),samples=sample)
(ev/'catalog-summary.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in stats.items() if k!='samples'},ensure_ascii=False,indent=2))
