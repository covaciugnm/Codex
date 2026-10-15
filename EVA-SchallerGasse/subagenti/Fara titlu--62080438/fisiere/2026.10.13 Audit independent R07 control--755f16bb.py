import json, hashlib, re
from pathlib import Path
from copy import deepcopy
from decimal import Decimal

HERE = Path(__file__).resolve().parent
R06 = HERE.parent / '2026.10.13 Baza comuna negociere BERGER PECH' / '2026.10.13 R06 propuneri negociere'
inventory_path = HERE/'2026.10.13 Inventar editorial R07.json'
inventory = json.loads(inventory_path.read_text(encoding='utf-8'))
checks = []
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def check(label, actual, expected):
    checks.append({'check':label,'pass':actual==expected,'actual':str(actual),'expected':str(expected)})
def locate(data, pointer):
    nodes=pointer.strip('/').split('/')
    parent=data
    for n in nodes[:-1]: parent=parent[int(n)] if isinstance(parent,list) else parent[n]
    key=int(nodes[-1]) if isinstance(parent,list) else nodes[-1]
    return parent,key
def text_values(x):
    if isinstance(x,str): return [x]
    if isinstance(x,list): return sum((text_values(v) for v in x),[])
    if isinstance(x,dict): return sum((text_values(v) for v in x.values()),[])
    return []
def money(s): return Decimal(s.replace('.','').replace(',','.'))
hashes={}
documents={}
for provider in ['BERGER','PECH']:
    old_path=R06/f'2026.10.13 Werkvertrag {provider} R06 Entwurf.json'
    final_path=HERE/f'2026.10.13 Werkvertrag {provider} R07.json'
    old=json.loads(old_path.read_text(encoding='utf-8'))
    final=json.loads(final_path.read_text(encoding='utf-8'))
    documents[provider]=final
    hashes[provider]={'R06':sha(old_path),'R07':sha(final_path)}
    expected=deepcopy(old)
    replacements=[x for x in inventory['replacements'] if x['provider']==provider]
    for item in replacements:
        parent,key=locate(expected,item['pointer'])
        check(provider+' inventory original exact '+item['id'],parent[key],item['original_R06'])
        parent[key]=item['replacement_DE']
        final_parent,final_key=locate(final,item['pointer'])
        check(provider+' inventory final exact '+item['id'],final_parent[final_key],item['replacement_DE'])
    # Internal provenance and numeric audit metadata are intentionally external.
    expected['sources']=[]
    expected.pop('financial_check',None)
    check(provider+' exact full transformation',expected,final)
    check(provider+' 16 sections',len(final['sections']),16)
    check(provider+' six annexes',len(final['annexes']),6)
    check(provider+' presentation identical',old['presentation'],final['presentation'])
    for n,(a,b) in enumerate(zip(old['annexes'][3]['tables'],final['annexes'][3]['tables']),1):
        check(provider+' financial table rows '+str(n),a['rows'],b['rows'])
        check(provider+' financial table widths '+str(n),a['widths_cm'],b['widths_cm'])
    vals=text_values({k:final[k] for k in ['title','version','preamble','sections','annexes','signatures','presentation']})
    joined='\n'.join(vals)
    forbidden='PECH' if provider=='BERGER' else 'BERGER'
    check(provider+' other-provider token count',len(re.findall(forbidden,joined,re.I)),0)
    check(provider+' negotiation/comparison tokens',len(re.findall(r'verhandl|beide\s+Anbieter|beide\s+AN\b|anbieterabhängig|AG-Verhandlungs|andere\s+Anbieter',joined,re.I)),0)
    original_money=re.findall(r'EUR\s+(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})','\n'.join(text_values(old)))
    final_money=re.findall(r'EUR\s+(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})',joined)
    check(provider+' no new currency values',set(final_money)-set(original_money),set())
    for row in final['annexes'][3]['tables'][3]['rows']:
        n,t,g,r,p=map(money,row[1:])
        check(provider+' VAT '+row[0],t,n*Decimal('.2'))
        check(provider+' gross '+row[0],g,n+t)
        check(provider+' retention '+row[0],r,n*Decimal('.05'))
        check(provider+' payout '+row[0],p,g-r)
    check(provider+' unchanged source after read',sha(old_path),hashes[provider]['R06'])
    check(provider+' unchanged R07 after read',sha(final_path),hashes[provider]['R07'])

B,P=documents['BERGER'],documents['PECH']
for i,(a,b) in enumerate(zip(B['sections'],P['sections'])):
    if i not in [0,10]:check('R07 common section '+str(i+1),a,b)
for i in [0,1,2,5]:check('R07 common annex '+str(i+1),B['annexes'][i],P['annexes'][i])
check('inventory count',len(inventory['replacements']),83)
result={'date':'2026.10.13','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','checks_count':len(checks),'source_hashes':hashes,'editorial_inventory_sha256':sha(inventory_path),'checks':checks,'scope':'Independent exact-delta, public-token and financial preservation checks. Semantic review is in separate TXT. No source edits or PDF generation.'}
(HERE/'2026.10.13 Audit independent R07 control.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ['status','checks_count','source_hashes']},indent=2))
print('FAILURES',json.dumps([x for x in checks if not x['pass']],ensure_ascii=False))
