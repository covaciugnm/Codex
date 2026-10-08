from pathlib import Path
import requests, json, hashlib, gzip, re, sys, time, html
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit, urldefrag, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).parent/'Analiza_iDempiere_HR_SSM_SU_2026-10-08'
ROOT.mkdir(exist_ok=True)
REG=ROOT/'08_Registre_si_verificari'; REG.mkdir(exist_ok=True)
CSS='body{font:17px/1.55 Arial,sans-serif;max-width:1100px;margin:36px auto;padding:0 24px;color:#172331}table{border-collapse:collapse;width:100%;margin:18px 0}td,th{border:1px solid #d9d9d9;padding:9px;text-align:left;vertical-align:top}th{background:#e9eff5}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f5f7;padding:12px}a{color:#165a87;overflow-wrap:anywhere}h1,h2,h3{color:#000}.meta{font-size:14px;color:#455465}img,svg{display:none}'
S=[]
def add(id,group,title,url,kind='html',note=''):
    S.append(dict(id=id,grup=group,titlu=title,url=url,tip=kind,nota=note))
I='02_iDempiere'; F='03_HR/Frappe_HR'; A='03_HR/Axelor'; O='03_HR/Apache_OFBiz'; R='04_SSM_SU/SSM_ro'; M='04_SSM_SU/SSMatic'; H='04_SSM_SU/SafeHub'; P='05_Extensii_HR_iDempiere'; L='06_Legislatie'
add('ID01',I,'Portal documentație iDempiere','https://docs.idempiere.org/')
add('ID02',I,'Structura funcțională','https://docs.idempiere.org/docs/basic-functional/menue_overview')
add('ID03',I,'Manual de referință','https://wiki.idempiere.org/en/Reference')
add('ID04',I,'Inventar ferestre și procese','https://wiki.idempiere.org/en/Manual')
add('ID05',I,'Cod sursă iDempiere','https://github.com/idempiere/idempiere')
add('ID06',I,'Versiuni și instalatoare','https://wiki.idempiere.org/en/Downloading_Installers')
add('ID07',I,'Fișiere distribuție','https://sourceforge.net/projects/idempiere/files/')
add('ID08',I,'Modificări release 13','https://wiki.idempiere.org/en/ChangeLog_Release_13')
add('ID09',I,'Timp și deconturi','https://wiki.idempiere.org/en/Expense_Report_%28Window_ID-235%29')
add('ID10',I,'Catalog extensii','https://wiki.idempiere.org/en/Category%3AAvailable_Plugins')
add('ID11',I,'Arhitectură și scop','https://idempiere.org/about/')
add('ID12',I,'Funcții ERP','https://idempiere.org/features/')
add('ID13',I,'Comparație versiuni','https://docs.idempiere.org/upgrade/compare')
add('ID14',I,'Cod stabil release 13','https://github.com/idempiere/idempiere/tree/release-13')
add('ID15',I,'Licența iDempiere','https://raw.githubusercontent.com/idempiere/idempiere/release-13/LICENSE','text')
for id,title,url in [
 ('FR01','Manual Frappe HR','https://docs.frappe.io/hr/introduction'),
 ('FR02','Repository Frappe HR','https://github.com/frappe/hrms'),
 ('FR03','Versiuni Frappe HR','https://github.com/frappe/hrms/releases'),
 ('FR04','Dosar angajat','https://docs.frappe.io/hr/employee'),
 ('FR05','Recrutare','https://docs.frappe.io/hr/recruitment'),
 ('FR06','Ture','https://docs.frappe.io/hr/shift-management'),
 ('FR07','Configurare salarizare','https://docs.frappe.io/hr/payroll-setup'),
 ('FR08','Procesare salarizare','https://docs.frappe.io/hr/payroll-entry'),
 ('FR09','Fluturaș salarial','https://docs.frappe.io/hr/salary-slip'),
 ('FR10','API REST','https://docs.frappe.io/framework/user/en/api/rest'),
 ('FR11','Webhooks','https://docs.frappe.io/framework/v14/user/en/guides/integration/webhooks'),
 ('FR12','Program de instruire','https://docs.frappe.io/hr/training-program')]: add(id,F,title,url)
add('FR13',F,'Licență sursă','https://raw.githubusercontent.com/frappe/hrms/develop/license.txt','text')
for id,title,url in [
 ('AX01','Manual HR','https://docs.axelor.com/aos/en/category/rh/'),
 ('AX02','Repository suită','https://github.com/axelor/axelor-open-suite'),
 ('AX03','Cod modul HR','https://github.com/axelor/axelor-open-suite/tree/master/axelor-human-resource'),
 ('AX04','Versiuni','https://github.com/axelor/axelor-open-suite/releases'),
 ('AX05','Aplicație web și build','https://github.com/axelor/open-suite-webapp'),
 ('AX06','Recrutare','https://docs.axelor.com/aos/en/aos/RH/job_offer/'),
 ('AX07','Dosar angajat','https://docs.axelor.com/aos/en/aos/RH/employe_file/'),
 ('AX08','Pregătire salarizare','https://docs.axelor.com/aos/en/aos/RH/tickets/'),
 ('AX09','Instruire și evaluare','https://docs.axelor.com/aos/en/aos/RH/training/'),
 ('AX10','API servicii','https://docs.axelor.com/adk/7.4/dev-guide/web-services/index.html'),
 ('AX11','Ediții și prețuri','https://axelor.com/pricing/'),
 ('AX12','Community și migrare','https://forum.axelor.com/t/clarifcation-on-community-versions/6243'),
 ('AX13','Funcții mobile HR','https://docs.axelor.com/aos/en/8.2/aom/hr/hr_intro/')]: add(id,A,title,url)
add('AX14',A,'Licență','https://raw.githubusercontent.com/axelor/axelor-open-suite/master/LICENSE','text')
add('OF01',O,'Manual utilizator HTML','https://nightlies.apache.org/ofbiz/stable/ofbiz/html5/user-manual.html')
add('OF02',O,'Manual utilizator PDF','https://nightlies.apache.org/ofbiz/stable/ofbiz/pdf/user-manual.pdf','pdf')
add('OF03',O,'Manual dezvoltator PDF','https://nightlies.apache.org/ofbiz/stable/ofbiz/pdf/developer-manual.pdf','pdf')
add('OF04',O,'Descărcări oficiale','https://ofbiz.apache.org/download')
add('OF05',O,'Cod sursă','https://github.com/apache/ofbiz-framework')
add('OF06',O,'Licență','https://raw.githubusercontent.com/apache/ofbiz-framework/trunk/LICENSE','text')
for id,title,url in [
 ('SS01','Ghid SSM.ro','https://ghid.ssm.ro/docs'),
 ('SS02','Primii pași','https://ghid.ssm.ro/docs/02-ghiduri/utilizator/primii-pasi'),
 ('SS03','Generatoare documente','https://ghid.ssm.ro/docs/02-ghiduri/utilizator/generatoare-documente'),
 ('SS04','Date angajați','https://ghid.ssm.ro/docs/02-ghiduri/utilizator/introducere-date-angajati'),
 ('SS05','API','https://ghid.ssm.ro/docs/03-api'),
 ('SS06','Autentificare API','https://ghid.ssm.ro/docs/03-api/autentificare'),
 ('SS07','Rapoarte API','https://ghid.ssm.ro/docs/03-api/rapoarte'),
 ('SS08','Exemplu Node.js','https://ghid.ssm.ro/docs/03-api/exemple-implementare/nodejs'),
 ('SS09','Întrebări frecvente','https://www.ssm.ro/intrebari-frecvente'),
 ('SS10','Oferta','https://www.ssm.ro/oferta')]: add(id,R,title,url)
add('SM01',M,'Funcții SSMatic','https://www.ssmatic.ro/')
add('SM02',M,'Prețuri SSMatic','https://www.ssmatic.ro/preturi')
add('SH01',H,'Funcții SafeHub','https://safehub.ro/')
add('SH02',H,'Prețuri SafeHub','https://safehub.ro/preturi/')
plugins=[('PL01','CDSoftware Payroll','CDSoftware_Payroll'),('PL02','CDSoftware Attendance','CDSoftware_Attendance'),('PL03','CDSoftware Training','CDSoftware_EmployeeTraining'),('PL04','CDSoftware Recruitment','CDSoftware_EmployeeRecruitment'),('PL05','CDSoftware PayrollReport','CDSoftware_PayrollReport'),('PL06','CDSoftware PerformanceEvaluation','CDSoftware_PerformanceEvaluation'),('PL10','Ingeint Payroll','Ingeint_Payroll'),('PL12','Libero Payroll istoric','Libero_Payroll'),('PL13','Localizare România','Localization_Romania')]
for id,title,path in plugins: add(id,P,title,'https://wiki.idempiere.org/en/Plugin%3A_'+path)
add('PL07',P,'AMERPSOFT repository','https://github.com/luisamesty/Amerpsoft-iDempiere-community')
add('PL08',P,'AMERPSOFT manual modul','https://raw.githubusercontent.com/luisamesty/Amerpsoft-iDempiere-community/master/org.amerpsoft.com.idempiere.personnelpayroll/README.md','text')
add('PL09',P,'AMERPSOFT prezentare istorică PDF','https://wiki.idempiere.org/w-en/images/5/53/PayrollPluginNomina_EN_Luis_Amesty.pdf','pdf','Document istoric 2019; nu confirmă versiunea actuală')
add('PL11',P,'Ingeint Human Talent','https://github.com/ingeint/ingeint-idempiere-humantalent')
add('PL14',P,'ADempiere referință pentru portare','https://github.com/adempiere/adempiere/releases')
add('PL15',P,'iDempiere REST sursă','https://github.com/bxservice/idempiere-rest')
add('PL16',P,'iDempiere REST documentație','https://bxservice.github.io/idempiere-rest-docs/')
add('PL17',P,'AMERPSOFT README PDF','https://raw.githubusercontent.com/luisamesty/Amerpsoft-iDempiere-community/master/README.pdf','pdf')
add('LG01',L,'Legea 319 din 2006','https://legislatie.just.ro/Public/DetaliiDocument/73772')
add('LG02',L,'Ordinul 712 din 2005','https://legislatie.just.ro/Public/DetaliiDocumentAfis/63056')
add('LG03',L,'Ordinul 163 din 2007','https://legislatie.just.ro/Public/DetaliiDocument/80730')
add('LG04',L,'HG 1425 Norme PDF CNPP','https://www.cnpp.ro/documents/10180/13120847/HG-nr.1425-2006-pentru-aprob.-normelor-metodologice-de-aplicare-a-prevederilor-lg.-securitatii-si-sanatatii-in-munca-nr.319-2006?t=1730902121752&version=1.0','pdf','Copie de referință; verificarea formei în vigoare rămâne necesară')

def slug(s): return re.sub('[^a-zA-Z0-9_-]+','_',s).strip('_')[:90]
def norm(u):
    u=urldefrag(u)[0]
    return u.rstrip('/') if urlsplit(u).path!='/' else u

def fetch(s):
    out=dict(s); folder=ROOT/s['grup']; folder.mkdir(parents=True,exist_ok=True)
    stem=s['id']+'_'+slug(s['titlu'])
    out.update(data_recuperare=time.strftime('%Y-%m-%dT%H:%M:%S%z'),stare='NE_DESCARCAT',fisier='',sha256='',octeti=0)
    (folder/(stem+'.url')).write_text('[InternetShortcut]\nURL='+s['url']+'\n',encoding='utf-8')
    try:
        rr=requests.get(s['url'],timeout=(12,45),headers={'User-Agent':'Mozilla/5.0 DocumentationArchive/1.0'},allow_redirects=True)
        out.update(http=rr.status_code,url_final=rr.url)
        if rr.status_code!=200: raise ValueError('HTTP '+str(rr.status_code))
        data=rr.content
        if s['tip']=='pdf':
            if not data.startswith(b'%PDF'): raise ValueError('Răspunsul nu este PDF')
            dest=folder/(stem+'.pdf'); dest.write_bytes(data)
        elif s['tip']=='text':
            if b'<html' in data[:1000].lower(): raise ValueError('HTML în loc de text')
            dest=folder/(stem+'.txt'); dest.write_bytes(data)
        else:
            soup=BeautifulSoup(data,'html.parser')
            title=soup.title.get_text(' ',strip=True) if soup.title else s['titlu']
            if 'Just a moment' in title: raise ValueError('Protecție web; conținut indisponibil')
            out['titlu_pagina']=title
            out['_links']=[urljoin(rr.url,a.get('href')) for a in soup.find_all('a',href=True)]
            main=soup.select_one('article') or soup.select_one('main') or soup.select_one('#mw-content-text') or soup.body or soup
            for tag in list(main.select('script,style,nav,header,footer,button,form,iframe,svg,noscript,video,audio,source,img,link,meta')): tag.decompose()
            for tag in main.find_all(True):
                attrs={}
                if tag.name=='a' and tag.get('href'):
                    u=urljoin(rr.url,tag['href'])
                    if u.startswith(('https://','http://','#')): attrs['href']=u
                if tag.name in ['td','th']:
                    for k in ['colspan','rowspan']:
                        if tag.get(k): attrs[k]=tag[k]
                if tag.get('id'): attrs['id']=tag['id']
                tag.attrs=attrs
            # Captură textuală cu tabele și linkuri; originalul inert păstrează proveniența.
            raw=folder/(stem+'.original.html.gz'); raw.write_bytes(gzip.compress(data))
            out['original']=raw.relative_to(ROOT).as_posix()
            out['sha256_original']=hashlib.sha256(data).hexdigest()
            dest=folder/(stem+'.html')
            doc='<!doctype html><html lang="ro"><meta charset="utf-8"><title>'+html.escape(s['titlu'])+'</title><style>'+CSS+'</style><body><p class="meta">Copie locală pentru documentare • '+html.escape(out['data_recuperare'])+'<br>Sursa: <a href="'+html.escape(rr.url,quote=True)+'">'+html.escape(rr.url)+'</a><br>Conținutul original își păstrează limba și drepturile. Scripturile, meniurile și imaginile externe nu sunt incluse în această versiune offline.</p>'+str(main)+'</body></html>'
            dest.write_text(doc,encoding='utf-8')
        final=dest.read_bytes()
        out.update(stare='DESCARCAT',fisier=dest.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(final).hexdigest(),octeti=len(final))
    except Exception as e:
        out['eroare']=str(e)[:300]
        (folder/(stem+'_INDISPONIBIL.txt')).write_text('Materialul nu a putut fi descărcat.\nSursa: '+s['url']+'\nMotiv: '+out['eroare']+'\nNu se prezintă drept document recuperat.\n',encoding='utf-8')
    return out

def run(items):
    res=[]
    with ThreadPoolExecutor(max_workers=6) as pool:
        for f in as_completed([pool.submit(fetch,s) for s in items]):
            r=f.result(); res.append(r)
            print(r['id'],r['stare'],r.get('http',''),flush=True)
    return res

if __name__=='__main__':
    results=run(S); known={norm(s['url']) for s in S}; discovered=[]
    rules=[(F,'docs.frappe.io','/hr/',220,'FRD'),(R,'ghid.ssm.ro','/docs',120,'SSD'),(A,'docs.axelor.com','/aos/en/aos/RH/',40,'AXD'),(I,'docs.idempiere.org','/docs/basic-functional/',30,'IDD')]
    for group,host,prefix,limit,label in rules:
        candidates=set()
        for r in results:
            if r['grup']==group:
                for u in r.get('_links',[]):
                    parts=urlsplit(u); u=norm(u)
                    if parts.netloc==host and parts.path.startswith(prefix) and not parts.query and u not in known:
                        if not re.search(r'\.(png|jpg|jpeg|svg|zip|mp4)$',parts.path,re.I): candidates.add(u)
        for n,u in enumerate(sorted(candidates)[:limit],1):
            known.add(u); title=unquote(urlsplit(u).path.rstrip('/').split('/')[-1]).replace('-',' ')
            discovered.append(dict(id=label+str(n).zfill(3),grup=group,titlu=title,url=u,tip='html',nota='Page découverte dans les liens du manuel'.replace('Page découverte dans les liens du manuel','Pagină identificată în cuprinsul manualului')))
    print('PAGINI_DESCOPERITE',len(discovered),flush=True)
    results+=run(discovered)
    for r in results: r.pop('_links',None)
    results.sort(key=lambda x:x['id'])
    (REG/'registru_surse.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    (REG/'surse_initiale.json').write_text(json.dumps(S,ensure_ascii=False,indent=2),encoding='utf-8')
    print('FINAL',len(results),sum(x['stare']=='DESCARCAT' for x in results),flush=True)
