from pathlib import Path
from copy import deepcopy
import json, hashlib, re, shutil
from collections import Counter

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
DATE='2026.10.13'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def fresh(p,content):assert not p.exists(),p;p.write_text(content,encoding='utf-8')
def locate(data,pointer):
    parts=pointer.lstrip('/').split('/');obj=data
    for part in parts[:-1]:obj=obj[int(part)] if isinstance(obj,list) else obj[part]
    key=int(parts[-1]) if isinstance(obj,list) else parts[-1]
    return obj,key
def rendered_text(data):
    values=[data['title'],data['version'],*data['preamble'],*data['signatures']]
    for kind in ['sections','annexes']:
        for block in data[kind]:
            values.extend([block['title'],*block['paragraphs']])
            for t in block.get('tables',[]):values.extend(t['headers']);values.extend(str(v) for row in t['rows'] for v in row)
    return '\n'.join(values)

inventory_path=OUT/f'{DATE} Inventar editorial R07.json'
assert sha(inventory_path)=='e1bd3564e30cfc0ad020adc8e610b756997c136436220b898bfac8622addc06c'
inventory=read(inventory_path)
records=[];contracts={}
domains={'BERGER':'bmberger.at','PECH':'zt-pech.at'}
offer_dates={'BERGER':'2026.08.17','PECH':'2026.09.17'}
original_hashes={'BERGER':'b9d4297e8e68277cc146d00dc5527711640c0da61f1b32f74cddafa6071fc80b','PECH':'29495a44171efd95e99b68de2b646d6f0eaf3ecf440e89bd00a9adb82cb74ef1'}
for source in inventory['sources']:
    provider=source['provider'];p=ROOT/source['file'];assert sha(p)==source['sha256']
    old=read(p);new=deepcopy(old);changes=[]
    for replacement in inventory['replacements']:
        if replacement['provider']!=provider:continue
        obj,key=locate(new,replacement['pointer']);assert obj[key]==replacement['original_R06'],replacement['id']
        obj[key]=replacement['replacement_DE'];changes.append({'id':replacement['id'],'pointer':replacement['pointer'],'before':replacement['original_R06'],'after':replacement['replacement_DE']})
    # Publish an editable source containing only the contract and presentation.
    # Provenance and comparison records stay in this internal dossier.
    new={k:new[k] for k in ['provider','title','version','date','preamble','sections','annexes','signatures','presentation'] if k in new}
    new['sources']=[]
    assert len(new['sections'])==16 and len(new['annexes'])==6
    assert [len(x['paragraphs']) for x in old['sections']]==[len(x['paragraphs']) for x in new['sections']]
    assert sum(len(x['paragraphs']) for x in new['sections'])==96
    for old_block,new_block in zip(old['sections']+old['annexes'],new['sections']+new['annexes']):
        assert old_block['number']==new_block['number']
        assert len(old_block.get('tables',[]))==len(new_block.get('tables',[]))
        for ot,nt in zip(old_block.get('tables',[]),new_block.get('tables',[])):
            assert len(ot['rows'])==len(nt['rows'])
    # All honorarium rows, allocations, rates, VAT/retention/payment and options
    # are copied byte-for-byte at cell level from the previously audited R06.
    assert [x['rows'] for x in old['annexes'][3]['tables']]==[x['rows'] for x in new['annexes'][3]['tables']]
    assert old['presentation']==new['presentation']
    old_money=Counter(re.findall(r'\bEUR\s+\d[\d.,]*',rendered_text(old)))
    new_money=Counter(re.findall(r'\bEUR\s+\d[\d.,]*',rendered_text(new)))
    assert not new_money-old_money,'A monetary amount was added outside the exact-copy price tables'
    other='PECH' if provider=='BERGER' else 'BERGER'
    visible=rendered_text(new)
    assert other.lower() not in visible.lower()
    assert not re.search(r'verhand|\banbieter\b|für beide AN|beide Auftragnehmer|gemeinsame Verhandlungs|wesentlichen Abweichungen',visible,re.I)
    target=OUT/f'{DATE} Werkvertrag {provider} R07.json'
    fresh(target,json.dumps(new,ensure_ascii=False,indent=2)+'\n')
    folder=ROOT/f'00.Proiect/09. Vertraege/{domains[provider]}/{DATE} Vertragsvorschlag R07'
    folder.mkdir(parents=True,exist_ok=False)
    public_source=folder/target.name;shutil.copy2(target,public_source);assert sha(public_source)==sha(target)
    offer_name=f'{DATE} Anlage 5 Originalangebot {provider} {offer_dates[provider]}.pdf'
    original=ROOT/f'00.Proiect/09. Vertraege/{domains[provider]}/{DATE} Verhandlungsentwurf R06'/offer_name
    assert sha(original)==original_hashes[provider]
    copied_offer=folder/offer_name;shutil.copy2(original,copied_offer);assert sha(copied_offer)==original_hashes[provider]
    contracts[provider]=new
    records.append({'provider':provider,'source_R06':source,'R07':str(target.relative_to(ROOT)),'R07_sha256':sha(target),'public_source':str(public_source.relative_to(ROOT)),'PDF_expected':str((folder/f'{DATE} Werkvertrag {provider} R07.pdf').relative_to(ROOT)),'offer_copy':str(copied_offer.relative_to(ROOT)),'offer_sha256':sha(copied_offer),'applied_editorial_changes':changes,'price_cells_exact_R06':True,'original_offer_unchanged':True,'other_provider_visible':False,'negotiation_visible':False})
for i in [0,1,2,5]:assert contracts['BERGER']['annexes'][i]==contracts['PECH']['annexes'][i]
assert [i+1 for i,(a,b) in enumerate(zip(contracts['BERGER']['sections'],contracts['PECH']['sections'])) if a!=b]==[1,11]
manifest={'data':DATE,'statut':'PROPUNEREA A&C DE CONTRACT; surse noi R07; R06 si ofertele originale nemodificate','inventar_editorial_sha256':sha(inventory_path),'operatiuni':records,'emailuri_trimise':0,'semnaturi':0,'plati':0}
fresh(OUT/f'{DATE} Registru aplicare editoriala R07.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
for source in inventory['sources']:assert sha(ROOT/source['file'])==source['sha256']
print(json.dumps([{'provider':r['provider'],'source_sha256':r['R07_sha256'],'changes':len(r['applied_editorial_changes']),'price_cells_exact':True} for r in records],ensure_ascii=False))
