import json,re,hashlib,requests,shutil,unicodedata,zipfile,io,html
from pathlib import Path
from urllib.parse import urlparse,urlsplit,urlunsplit,unquote,parse_qs,urljoin
from concurrent.futures import ThreadPoolExecutor,as_completed
from bs4 import BeautifulSoup
from catalogue import BASE,CACHE,ROWS,add,topic_program
OUT=BASE/'F';OUT.mkdir(exist_ok=True)
BIN=BASE/'download_cache';BIN.mkdir(exist_ok=True)
GROUPS={'UE':'01. UE','SEE':'02. SEE Norvegia','CH':'03. Elvetia','ALTE':'04. Alte organisme','ARHIVA':'05. Arhiva'}
def clean(s,n=45):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode();s=re.sub(r'[<>:"/\\|?*\x00-\x1f]',' ',s);s=re.sub(r'\s+',' ',s).strip(' .');return s[:n].rstrip(' .') or 'document'
arch_names=['Dezvoltare locală','Energie','Justiție','Sănătate','Cercetare','Active Citizens Fund','Dezvoltarea afacerilor / SMEs Growth','RO-Cultura','Afaceri interne','Mediu','Educație','Dialog social']
for i,name in enumerate(arch_names,1):
    add('NA'+str(i).zfill(2),'SEE / Norvegia 2014–2021 – '+name,'NARCH_'+str(i),name,'Solicitanți conform fostelor apeluri',group='ARHIVA',mode='Operatorul vechii perioade',status='Arhivă – nu reprezintă apel deschis',note='Perioada 2014–2021; documentație istorică, distinctă de noul ciclu 2021–2028.')
byid={r['id']:r for r in ROWS}
for id,patch in {'EICA':{'deadline':'2026-11-04','status':'Deschis; propunere scurtă și GO înainte de etapa completă'},'INNOWWIDE':{'deadline':'2026-12-01','status':'Deschis de la 01.10.2026','rate':'Maximum 70%; cost eligibil total minimum 86.000 EUR','amount':'60.000 EUR / proiect, grant fix','budget':'4.200.000 EUR – buget apel 5','note':'Firmă înființată de minimum 2 ani la termen; fără finanțare Innowwide anterioară; proiect 6 luni, TRL 4–8 și subcontractor independent pe piața-țintă.'},'ERCST':{'deadline':'2026-10-14','status':'Deschis – ERC-2027-STG'},'ERCCO':{'deadline':'2027-01-12','status':'Deschis – ERC-2027-COG'},'CHC2':{'deadline':'2025-12-17'},'JUHI':{'deadline':'2026-10-08','status':'Apel 13: deschis pentru propuneri scurte'}}.items():byid[id].update(patch)
for r in ROWS:
    prefix='9999. INCHIS' if r['status'].startswith(('Arhivă','Închis','Apel închis')) else r['deadline'].replace('-','.') if r['deadline'] else 'PROGRAM'
    # IDs let the workbook retain full names while keeping Windows paths short.
    folder=clean(prefix+' - '+r['id']+' - '+r['title'],55)
    r['folder']=GROUPS[r['group']]+'/'+folder
    (OUT/r['folder']/'1.DOCUMENTE OFICIALE').mkdir(parents=True,exist_ok=True)
    (OUT/r['folder']/'0.ARHIVA').mkdir(exist_ok=True)
PLAN=[]
official=('europa.eu','eeagrants.org','gov.ro','eurekanetwork.org','snf.ch','eda.admin.ch','cost.eu','elvetiaromania.ro','eib.org','esa.int','sbfi.admin.ch','coe.int','ebrd.com','swiss-contribution.ro','fdsc.ro')
def norm(u):
    u=html.unescape(u).strip().replace('http://','https://',1)
    parts=urlsplit(u)
    if '/document/download/' in parts.path:u=urlunsplit((parts.scheme,parts.netloc,parts.path,'',''))
    return u
def adddoc(id,u,label,source='',archive=False):
    u=norm(u);host=(urlparse(u).hostname or '').lower()
    if not any(host==h or host.endswith('.'+h) for h in official):return
    if not u.startswith('https://'):return
    PLAN.append({'program':id,'url':u,'label':label or unquote(urlparse(u).path.split('/')[-1]),'source':source or byid[id]['source'],'archive':archive})
def sourcedocs(key,ids,predicate=lambda d:True,archive=False):
    p=CACHE/(key+'.json')
    if not p.exists():return
    d=json.loads(p.read_text(encoding='utf8'))
    for doc in d.get('documents',[]):
        if predicate(doc):
            for id in ids:adddoc(id,doc['url'],doc['context'] or doc['label'],d.get('url_final',d['url']),archive)
h=json.loads((CACHE/'Horizon_WP.json').read_text(encoding='utf8'))['documents']
mapping={'General introduction':['EU01'],'MSCA':['MSPF','MSDN','MSSE','MSCF','MSCZ'],'Infrastructures':['HINF'],'Cluster 1':['HCL1'],'Cluster 2':['HCL2'],'Cluster 3':['HCL3'],'Cluster 4':['HCL4'],'Cluster 5':['HCL5'],'Cluster 6':['HCL6'],'European Innovation Ecosystems':['HEIE'],'WIDERA':['HWID'],'EU Missions':['HMIS'],'NEB':['HNEB'],'Horizontal activities':['HHOR'],'General annexes':['EU01']}
for doc in h:
    if '(2026-27)' in doc['context']:
        for token,ids in mapping.items():
            if ' - '+token in doc['context']:
                for id in ids:adddoc(id,doc['url'],doc['context'],byid[id]['source'])
sourcedocs('Horizon_WP',['EU01'],lambda d:'(2025)' in d['context'] and ('General introduction' in d['context'] or 'Annexes' in d['context']),True)
sourcedocs('EIC',['EICA','EICP','EICT','EICS','EICD','EICCH'],lambda d:'march-2026' not in d['url'] and '5-november' not in d['url'] and 'DPN_' not in d['url'])
sourcedocs('EIC_Accelerator',['EICA'],lambda d:'guide' in d['context'].lower() or 'Annexes' in d['context'])
sourcedocs('EIC_STEP',['EICS'],lambda d:'DPN_' not in d['url'])
sourcedocs('EIC_Investment',['EICA','EICS','EICD'])
sourcedocs('EIC_Transition',['EICT'],lambda d:'guide' in d['context'].lower() or 'guidance' in d['context'].lower())
for id in ['ERCST','ERCCO','ERCAD','ERCSY','ERCPO']:
    adddoc(id,'https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/wp-call/2027/wp_horizon-erc-2027_en.pdf','ERC Work Programme 2027',byid[id]['source'])
    adddoc(id,'https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/wp-call/2026/wp_horizon-erc-2026_en.pdf','ERC Work Programme 2026',byid[id]['source'],True)
sourcedocs('LIFE_support',['LIFEN','LIFEE','LIFEC','LIFET'])
sourcedocs('CERV',['CERV'],lambda d:('2026' in d['context'] or 'lump sums' in d['context']) and not re.search(r'_(de|fr)\b',d['url']))
sourcedocs('EDF',['EDF'],lambda d:'2026' in d['context'] or 'tutorial' in d['url'].lower())
sourcedocs('EDIP',['EDIP'],lambda d:('2026' in d['context'] or '2027' in d['context'] or 'programme' in d['context'].lower()) and not re.search(r'_(de|fr)\b',d['url']))
for key,ids in [('RFCS',['RFCS']),('I3',['I3']),('EIB_ELENA',['ELENA']),('ELENA_Brochure',['ELENA']),('EYE',['EYE']),('CBE',['JUBB']),('CleanAviation',['JUCA']),('Rail',['JURA']),('Eureka',['EUROSTARS']),('Swiss_RO',['CH01']),('Norway_MoU',['N01','N02','N04','N05']),('Norway_MoU_N',['N03','N06','N07','N08','N09']),('Swiss_MAPS',['CHMAPS']),('ESA_BASS',['ESABASS']),('Antifraud',['ANTIF'])]:sourcedocs(key,ids,lambda d:not d['url'].endswith('.fr.pdf'))
sourcedocs('COST_Docs',['COST'],lambda d: any(t in d['context'].lower() for t in ['open call','proposers','country','annotated rules','submission']))
sourcedocs('Erasmus_Docs',['ERASMUS','EMUNDUS'],lambda d:any('_'+lang+'.pdf' in d['url'] for lang in ['en','ro']))
sourcedocs('Creative_Docs',['CREAC','CREAM','CREAX'])
sourcedocs('Solidarity',['ESC'],lambda d:'2026' in d['url'] and (d['url'].endswith('_en.pdf') or d['url'].endswith('_ro.pdf')))
for n in range(1,8):sourcedocs('CSF_'+str(n),['CSF'+str(n)],lambda d:'Privacy' not in d['context'] and 'privacy' not in d['url'])
for n in [1,2]:sourcedocs('Swiss_Civic_'+str(n),['CHC'+str(n)],archive=True)
sourcedocs('Swiss_Civic_Results',['CHC2'],archive=True)
sourcedocs('Norway_Archive_Docs',['NA01'],archive=True)
# Current programme factsheets have official fallback URLs published by FDFA.
swiss_files={'CH01':'dual-vet-programme.pdf','CH02':'international-research-cooperation-programme.pdf','CH03':'emissions-research-monitoring-infrastructure-programme.pdf','CH04':'smes-programme.pdf','CH05':'internal-affairs-programme.pdf','CH06':'justice-programme.pdf','CH07':'energy-efficiency-renewable-energy-programme.pdf','CH08':'metrorex-programme.pdf','CH09':'health-programme.pdf','CH10':'social-inclusion-programme.pdf','CH11':'civic-engagement-programme-july-2026.pdf'}
for id,fn in swiss_files.items():adddoc(id,'https://www.eda.admin.ch/content/dam/countries/countries-content/romania/en/'+fn,'FDFA Factsheet '+byid[id]['title'], 'https://www.schweiz-rumaenien.eda.admin.ch/en/second-swiss-contribution-projects')
adddoc('CH11','https://www.eda.admin.ch/content/dam/countries/countries-content/romania/en/srcp-factsheet.pdf','FDFA Fișa Programului de cooperare elvețiano-român','https://www.schweiz-rumaenien.eda.admin.ch/en/second-swiss-contribution-projects')
adddoc('CHMAPS','https://www.snf.ch/media/fr/mUNB1vaOQda3tEkI/Call_Document_MAPS.pdf','MAPS Call Document',byid['CHMAPS']['source'],True)
adddoc('EUROSTARS','https://www.eurekanetwork.org/wp-content/uploads/2026/02/eurostars-september-2026.pdf','Eurostars Call 11 – septembrie 2026',byid['EUROSTARS']['source'],True)
dig=json.loads((CACHE/'Digital_WP.json').read_text(encoding='utf8'))
for a in dig['links']:
    if a['label']=='March 2026 amendment (.pdf)':adddoc('DIG',a['url'],'Digital Europe WP – amendament martie 2026',dig['url'])
    if a['label']=='July 2026 amendment':
        # This is a document page; retain source link. Its direct PDF is obtained from portal topic conditions.
        byid['DIGECCC']['note']+=' Documentul ECCC din iulie 2026 este indicat în sursa oficială.'
TOPICS=json.loads((BASE/'portal_all.json').read_text(encoding='utf8'))['results']
for topic in TOPICS:
    m=topic['metadata'];ident=m['identifier'][0];id=topic_program(ident)
    src='https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/'+ident
    for field in ['topicConditions','descriptionByte','supportInfo','additionalInfo']:
        for t in m.get(field,[]):
            for a in BeautifulSoup(t,'html.parser').select('a[href]'):
                u=a['href'].strip()
                if re.search(r'\.(pdf|docx?|xlsx?|zip)(?:[?#]|$)',u,re.I) or '/document/download/' in u:
                    adddoc(id,u,a.get_text(' ',strip=True),src)
    # Authoritative portal data kept separately from original guide files.
    p=OUT/byid[id]['folder']/'2.APELURI PORTAL';p.mkdir(exist_ok=True)
    (p/(clean(ident,80)+'.json')).write_text(json.dumps(topic,ensure_ascii=False,indent=2),encoding='utf8')
unique={}
for d in PLAN:
    k=(d['program'],d['url']);unique.setdefault(k,d)
PLAN=list(unique.values())
(BASE/'download_plan.json').write_text(json.dumps(PLAN,ensure_ascii=False,indent=2),encoding='utf8')
(BASE/'catalogue.json').write_text(json.dumps(ROWS,ensure_ascii=False,indent=2),encoding='utf8')
def download(u,retry=False):
    key=hashlib.sha256(u.encode()).hexdigest();meta=BIN/(key+'.json')
    if meta.exists():
        cached=json.loads(meta.read_text(encoding='utf8'))
        if cached['ok'] or not retry:return cached
    result={'url':u,'ok':False,'file':'','bytes':0}
    try:
        try:
            r=requests.get(u,timeout=(12,50),headers={'User-Agent':'Mozilla/5.0','Referer':'https://'+urlparse(u).netloc+'/'});r.raise_for_status()
            raw=r.content;ct=r.headers.get('Content-Type','').lower();finalurl=r.url
        except requests.exceptions.SSLError:
            import ssl,urllib.request
            req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=45,context=ssl.create_default_context()) as resp:
                raw=resp.read();ct=resp.headers.get('Content-Type','').lower();finalurl=resp.url
        if len(raw)>60*1024*1024:raise ValueError('Document peste 60 MiB; link păstrat')
        ext=''
        if raw[:5]==b'%PDF-':
            ext='.pdf'
            from pypdf import PdfReader
            reader=PdfReader(io.BytesIO(raw));result['pages']=len(reader.pages)
        elif raw[:2]==b'PK':
            z=zipfile.ZipFile(io.BytesIO(raw));names=z.namelist()
            ext='.docx' if any(n.startswith('word/') for n in names) else '.xlsx' if any(n.startswith('xl/') for n in names) else '.pptx' if any(n.startswith('ppt/') for n in names) else '.zip'
            if z.testzip():raise ValueError('Arhivă invalidă')
        elif raw[:8]==bytes.fromhex('D0CF11E0A1B11AE1'):ext='.doc' if '.doc' in u.lower() else '.xls'
        else:raise ValueError('Răspunsul serverului nu este un PDF sau document Office / ZIP (tip: '+ct+')')
        path=BIN/(key+ext);path.write_bytes(raw)
        result.update(ok=True,file=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),ext=ext,url_final=finalurl)
    except Exception as e:result['error']=str(e)[:280]
    meta.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    return result
if __name__=='__main__':
    urls=sorted(set(d['url'] for d in PLAN)); print('PROGRAMS',len(ROWS),'TOPICS',len(TOPICS),'DOWNLOAD_URLS',len(urls),'FOLDER_COPIES',len(PLAN),flush=True)
    results={}
    with ThreadPoolExecutor(max_workers=8) as pool:
        fs={pool.submit(download,u):u for u in urls}
        for i,f in enumerate(as_completed(fs),1):
            res=f.result();results[res['url']]=res
            if i%20==0 or i==len(urls):print('PROGRESS',i,'/',len(urls),'OK',sum(x['ok'] for x in results.values()),flush=True)
    manifest=[]
    for d in PLAN:
        result=results[d['url']];row={**d,**result}
        if result['ok']:
            r=byid[d['program']];sub='0.ARHIVA' if d['archive'] else '1.DOCUMENTE OFICIALE'
            if any(w in d['label'].lower() for w in ['annex','anexa','form','declaration','declarat','bugetul','budget table']):sub+='/ANEXE'
            targetdir=OUT/r['folder']/sub;targetdir.mkdir(exist_ok=True,parents=True)
            # Keep paths under 245 characters in the staging area and shared folder.
            maxlen=max(12,244-len(str(targetdir))-1-len(result['ext'])-9)
            label=clean(re.split(r' Latest version| English Download| Download \(',d['label'])[0],min(60,maxlen))
            fn=label+'_'+result['sha256'][:8]+result['ext'];target=targetdir/fn
            shutil.copy2(result['file'],target);row['relative_path']=str(target.relative_to(OUT)).replace('\\','/')
        manifest.append(row)
    (BASE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    print('FINISHED unique',len(urls),'downloaded',sum(x['ok'] for x in results.values()),'failed',sum(not x['ok'] for x in results.values()),flush=True)
