import json, hashlib
from pathlib import Path
from decimal import Decimal as D

ROOT = Path(__file__).resolve().parent
OUT = ROOT / '2026.10.13 Audit independent R06 control.json'
BASE = ROOT.parent
checks = []
docs = {}
def check(label, value, expected):
    checks.append({'check':label, 'actual':str(value), 'expected':str(expected), 'pass':value == expected})
def money(s):
    return D(s.replace('.', '').replace(',', '.'))
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

for provider, total, originals in [('BERGER',45000,[13000,20000,2000,10000]), ('PECH',69300,[42000,6000,5000,800,14000,1500])]:
    p = ROOT / f'2026.10.13 Werkvertrag {provider} R06 Entwurf.json'
    h = sha(p)
    d = json.loads(p.read_text(encoding='utf-8'))
    docs[provider] = d
    a = d['annexes'][3]['tables']
    check(provider+' sections', [x['number'] for x in d['sections']], list(range(1,17)))
    check(provider+' annexes', [x['number'] for x in d['annexes']], list(range(1,7)))
    check(provider+' original net', [money(x[1]) for x in a[0]['rows'][:-1]], list(map(D,originals)))
    for row in a[0]['rows']:
        n,t,g = map(money,row[1:])
        check(provider+' original VAT '+row[0],t,n*D('.2'))
        check(provider+' original gross '+row[0],g,n+t)
    alloc = a[2]['rows']
    for i,row in enumerate(alloc[:-1]):
        vals = list(map(money,row[1:]))
        check(provider+' allocation row '+row[0],sum(vals[:-1]),vals[-1])
        check(provider+' E-percent '+row[0],vals[-1],D(total)*D([10,20,25,15,10,10,10][i])/100)
        check(provider+' event money '+row[0],money(a[1]['rows'][i][-1]),vals[-1])
    for c,expected in enumerate(originals):
        check(provider+' allocation column '+str(c+1),sum(money(r[c+1]) for r in alloc[:-1]),D(expected))
    for row in a[3]['rows']:
        n,t,g,r,pay = map(money,row[1:])
        check(provider+' billing VAT '+row[0],t,n*D('.2'))
        check(provider+' billing gross '+row[0],g,n+t)
        check(provider+' billing retention '+row[0],r,n*D('.05'))
        check(provider+' billing payout '+row[0],pay,g-r)
    for c in range(1,6):
        check(provider+' billing total '+str(c),sum(money(r[c]) for r in a[3]['rows'][:-1]),money(a[3]['rows'][-1][c]))
    option = D(1000 if provider=='BERGER' else 2700)
    check(provider+' six options net', money(a[-1]['rows'][0][2]),option)
    check(provider+' six options VAT gross',money(a[-1]['rows'][0][3]),option*D('1.2'))
    check(provider+' max conditional package',money(a[-1]['rows'][1][2]),D(total)+option)
    check(provider+' max conditional gross',money(a[-1]['rows'][1][3]),(D(total)+option)*D('1.2'))
    check(provider+' source unchanged after read',sha(p),h)

B,P=docs['BERGER'],docs['PECH']
for i,(b,p) in enumerate(zip(B['sections'],P['sections'])):
    if i==0:
        check('same AG identity',b['paragraphs'][0],p['paragraphs'][0])
        check('same authority rule',b['paragraphs'][2],p['paragraphs'][2])
    elif i==10:
        check('same section 11 apart from amount',b['paragraphs'][1:],p['paragraphs'][1:])
    else:
        check('common section '+str(i+1),b,p)
for i in [0,1,2,5]:
    check('common annex '+str(i+1),B['annexes'][i],P['annexes'][i])
check('same event IDs',[r[0] for r in B['annexes'][3]['tables'][1]['rows']],[r[0] for r in P['annexes'][3]['tables'][1]['rows']])
check('same complete event triggers',[r[1] for r in B['annexes'][3]['tables'][1]['rows']],[r[1] for r in P['annexes'][3]['tables'][1]['rows']])
check('same event percentages',[r[2] for r in B['annexes'][3]['tables'][1]['rows']],[r[2] for r in P['annexes'][3]['tables'][1]['rows']])
matrix = json.loads((BASE/'2026.10.13 Cerinte comune negociere matrice.json').read_text(encoding='utf-8'))
author = json.loads((ROOT/'2026.10.13 R06 Autorenkontrolle und Konkordanz100.json').read_text(encoding='utf-8'))
check('matrix criterion IDs',sorted(x['id'] for x in matrix['matrice']),['N'+str(i).zfill(3) for i in range(1,101)])
check('author references matched by ID, not display order',sorted(x['id'] for x in author['coverage']),['N'+str(i).zfill(3) for i in range(1,101)])
result={'date':'2026.10.13','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','checks_count':len(checks),'checks':checks,'source_hashes':{n:sha(ROOT/f'2026.10.13 Werkvertrag {n} R06 Entwurf.json') for n in docs},'matrix_sha256':sha(BASE/'2026.10.13 Cerinte comune negociere matrice.json'),'scope':'Independent numeric and exact common-text checks; semantic and legal review is recorded separately. No source modifications or PDF generation.'}
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':result['status'],'checks':len(checks),'failures':[x for x in checks if not x['pass']],'source_hashes':result['source_hashes']},ensure_ascii=False,indent=2))
