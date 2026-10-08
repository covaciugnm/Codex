import json,re,ast,concurrent.futures
from pathlib import Path
import requests
p=Path(__file__).resolve().parent
sources=json.loads((p/'source-checks.json').read_text(encoding='utf-8'))
mods=[('mgmtsystem_quality','O02','Coordonarea sistemului QMS'),('document_page_quality_manual','O03','Șablon de manual'),('mgmtsystem_nonconformity','O04','Neconformități și cauze'),('mgmtsystem_audit','O05','Audituri'),('mgmtsystem_nonconformity_hr','O06','Departament pe neconformitate'),('document_page_approval','O07','Aprobarea paginilor'),('mgmtsystem_action_efficacy','O08','Eficacitatea acțiunilor'),('mgmtsystem_review','O09','Analiza de management'),('mgmtsystem_nonconformity_product','O10','Produs pe neconformitate')]
def fetch(m):
    name,sid,role=m;repo='knowledge' if name=='document_page_approval' else 'management-system'
    url=f'https://raw.githubusercontent.com/OCA/{repo}/18.0/{name}/__manifest__.py'
    try:
        r=requests.get(url,timeout=15);r.raise_for_status();x=ast.literal_eval(r.text)
        return dict(name=name,id=sid,role=role,version=x.get('version','18.0'),license=x.get('license','De verificat'),url=url)
    except Exception:return dict(name=name,id=sid,role=role,version='18.0; patch neconfirmat',license='De verificat',url=url)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: modules=list(pool.map(fetch,mods))
releases={}
for repo in ['frappe/erpnext','frappe/hrms']:
    url=f'https://api.github.com/repos/{repo}/releases/latest'
    try:
        r=requests.get(url,timeout=15);r.raise_for_status();x=r.json();releases[repo]={'version':x['tag_name'],'url':x['html_url']}
    except Exception:releases[repo]={'version':'Versiune exactă neconfirmată','url':f'https://github.com/{repo}/releases'}
text=(p/'report.md').read_text(encoding='utf-8');part=text.split('## 4 Matricea funcțiilor')[1].split('## 5 ')[0]
rows=[];chapter='';k=0
for line in part.splitlines():
    if line.startswith('### '):chapter=line[4:]
    if not line.startswith('|'):continue
    c=[x.strip() for x in line.strip('|').split('|')]
    if len(c)!=6 or c[0]=='Funcție efectivă' or set(c[0])<=set('-: '):continue
    k+=1;oca,erp,book,dms,r=c[1:]
    hr='—';qcc=r;six=r;eva='U';note=''
    f=c[0]
    if 'HR în ecosistem' in f:hr='N';erp='A';note='HR separat: Frappe HR; OCA HR nu înseamnă integrare cu AMN.'
    if 'Evenimente și rezultate de instruire' in f:hr='N';erp='A';note='În ERPNext sunt necesare componentele Frappe HR.'
    if 'API în platformă' in f:hr='N';eva='C';note='API-ul R cere serviciu plumber. REST EVA: versiunea instalată trebuie verificată.'
    if 'Evenimente către' in f:hr='N';note='Webhook-urile nu includ automat maparea și livrarea fiabilă în EVA.'
    if 'Conector AMN' in f or 'Conector complet' in f:hr='U';eva='—';note='Niciun conector extern complet EVA nu este demonstrat.'
    if 'Relație cu persoana' in f:hr='D';eva='N';note='EVA folosește C_BPartner și AMN_Employee; extern trebuie mapare.'
    if 'Dezactivare sincronizată' in f:hr='D';eva='U'
    if 'Competență pentru' in f or 'Păstrarea postului' in f:hr='D';eva='D'
    if 'Gage' in f:qcc='U';six='N';note='Gage R&R confirmat în SixSigma; nu presupus în qcc.'
    if 'Obiective de calitate' in f or 'Analiză înainte' in f:qcc='C';six='C'
    if 'Editare prin browser' in f:eva='C';note='EVA are interfață ZK; editorul QMS complet nu este demonstrat.'
    if 'Dovadă arhivată' in f:eva='N';note='EVA_DocEmis arhivează documentul emis, cu SHA256 și atașament.'
    if 'Aceeași platformă' in f:eva='N';hr='D';note='DMS cere validare pe iDempiere 13; celelalte sunt servicii separate.'
    if 'Respectarea modelului exact' in f:eva='C';hr='D'
    if 'Licență open source' in f:hr='N';eva='U';note='DMS: GPL din catalog; licența întregului repository privat EVA nu a fost auditată.'
    if 'Proceduri și instrucțiuni' in f:eva='D'
    if 'aprobat' in f or 'Aprobare de document' in f or 'Citire nominală' in f:eva='D'
    if 'revizii' in f.lower() and 'documentului' in f:eva='D'
    if 'lot' in f:note=(note+' Legarea rezultatelor la operații și loturi EVA cere dezvoltare.').strip()
    refs={'4.1':'O03 O07 E02 B01 B08 D02 D03 P07','4.2':'O04 O05 O08 O09 E04 E05 R01 R02','4.3':'O06 E07 E08 E09 E10 P03 P04 P05 P06','4.4':'E03 E06 R01 R02 P07','4.5':'O11 O13 E11 E12 B05 B07 R05 I01 P01'}[chapter[:3]]
    rows.append([f'F{k:02}',chapter[4:],f,oca,erp,hr,book,dms,qcc,six,eva,note,refs])
rows.insert(0,['F00','HR și identitate','Fișă de angajat în aplicație','A','A','N','—','—','—','—','N','În EVA: C_BPartner + AMN_Employee. SSO nu este fișă HR.','E07 E08 P03 P04 P05'])
data={'rows':rows,'modules':modules,'releases':releases,'sources':sources}
(p/'excel-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'functions':len(rows),'modules':modules,'releases':releases},ensure_ascii=False))
