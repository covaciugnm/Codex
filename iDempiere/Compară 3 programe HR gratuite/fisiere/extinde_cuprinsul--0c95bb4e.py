import json,gzip,re
from urllib.parse import urljoin,urlsplit,urldefrag
from bs4 import BeautifulSoup
from colecteaza_documentatia import ROOT,REG,run
reg=json.loads((REG/'registru_surse.json').read_text(encoding='utf-8'))
known={s['url'].rstrip('/') for s in reg}; counts={};extra=[]
for round in range(1,5):
    pending=[]
    for s in reg:
        if not s.get('original'):continue
        if s.get('_scan'):continue
        s['_scan']=True
        if s['grup'] not in ['03_HR/Frappe_HR','03_HR/Axelor','04_SSM_SU/SSM_ro']:continue
        soup=BeautifulSoup(gzip.decompress((ROOT/s['original']).read_bytes()),'html.parser')
        for a in soup.find_all('a',href=True):
            u=urldefrag(urljoin(s.get('url_final',s['url']),a['href']))[0].rstrip('/');p=urlsplit(u)
            if p.query or u in known:continue
            ok=(p.netloc=='docs.frappe.io' and p.path.startswith('/hr/')) or (p.netloc=='ghid.ssm.ro' and p.path.startswith('/docs/')) or (p.netloc=='docs.axelor.com' and p.path.startswith('/aos/en/aos/RH/'))
            if not ok or re.search(r'\.(png|jpg|svg|mp4|gif)$',p.path):continue
            known.add(u);label={'03_HR/Frappe_HR':'FRX','03_HR/Axelor':'AXX','04_SSM_SU/SSM_ro':'SSX'}[s['grup']]
            counts[label]=counts.get(label,0)+1
            pending.append(dict(id=label+str(counts[label]).zfill(3),grup=s['grup'],titlu=a.get_text(' ',strip=True) or p.path.split('/')[-1],url=u,tip='html',nota='Lien interne du manuel'.replace('Lien interne du manuel','Legătură internă a manualului')))
    print('RUNDA',round,'NOI',len(pending),flush=True)
    if not pending:break
    reg+=run(pending)
for s in reg:s.pop('_scan',None);s.pop('_links',None)
(REG/'registru_surse.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2),encoding='utf-8')
print('TOTAL',len(reg))
