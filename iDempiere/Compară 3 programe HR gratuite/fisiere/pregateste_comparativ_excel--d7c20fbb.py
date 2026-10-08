from pathlib import Path
import json,re

BASE=Path(__file__).parent
ROOT=BASE/'Analiza_iDempiere_HR_SSM_SU_2026-10-08'
PAGES=json.loads((ROOT/'01_Raport/continut_structurat.json').read_text(encoding='utf8'))
SOURCES=json.loads((ROOT/'08_Registre_si_verificari/registru_surse.json').read_text(encoding='utf8'))
SD={s['id']:s for s in SOURCES}
PRODUCTS=[]
def prod(id,name,short,kind,version,tech,licence,note,refs,scope):
    PRODUCTS.append(dict(id=id,name=name,short=short,kind=kind,version=version,tech=tech,licence=licence,note=note,refs=refs,scope=scope))

prod('ID','iDempiere standard','iDempiere\n13','ERP de bază','Release 13; commit 0bbc4fa5df2e','Java / OSGi','GPLv2','Funcțiile nucleului. Tabelele HR nu dovedesc singure un motor salarial operațional.',['ID14','ID15B','ID02'],'core')
prod('FR','Frappe HR','Frappe HR\n16.50.0 / 15.64.3','Aplicație HR separată','v16.50.0 și v15.64.3 identificate în pagina release-urilor','Python / JavaScript','GPLv3','Manualul este evolutiv. Se fixează ramura și dependențele compatibile. ERPNext nu este inclus implicit în toate marcajele.',['FR03','FR13','FR01'],'hr')
prod('AX','Axelor HR / Open Suite','Axelor HR\n9.1.9; ghid 8.5','HR în suită ERP','Release v9.1.9; documentație HR inclusiv 8.5; mobil 8.2','Java','AGPLv3, Community','Nu se presupune identitate între ediții sau între ghid și versiune. Payroll este pregătire și export.',['AX04','AX14','AX01','AX13'],'hr')
prod('OF','Apache OFBiz HR','Apache OFBiz\n24.09.07','HR în platformă ERP','24.09.07; manual stable','Java','Apache 2.0','Orele de proiect țin de Project Manager. Nu este confirmată localizarea payroll România.',['OF04','OF06','OF01'],'hr')
prod('SS','SSM.ro','SSM.ro\nSaaS, 08.10.2026','Platformă SSM/SU','SaaS; număr public de versiune neidentificat; ghid la 08.10.2026','SaaS; limbaj neconfirmat','Serviciu comercial','API documentat pentru contacte și raport de nesemnate; nu rezultă un export API integral al tuturor dovezilor.',['SS01','SS05','SS10'],'ssm')
prod('SM','SSMatic','SSMatic\nSaaS, 08.10.2026','Platformă SSM','SaaS; număr public de versiune neidentificat; site la 08.10.2026','SaaS; limbaj neconfirmat','Acces de bază gratuit declarat; semnături plătite','Funcțiile provin din prezentarea furnizorului. Manual tehnic complet și API public neconfirmate.',['SM01','SM02'],'ssm')
prod('SH','SafeHub','SafeHub\nSaaS, 08.10.2026','Platformă SSM/SU','SaaS; număr public de versiune neidentificat; site la 08.10.2026','SaaS; limbaj neconfirmat','Serviciu comercial','Bifele se bazează pe declarațiile furnizorului. Integrarea Microsoft 365 nu dovedește un API general de HR.',['SH01','SH02'],'ssm')
cd=[('CP','Payroll','PL01','Base și DetailNames; exemple pentru Panama. Payroll Contract nu echivalează cu un CIM românesc.'),('CA','Attendance','PL02','Formate TXT/HIKVISION. Compatibilitatea cu terminalul concret se verifică.'),('CT','EmployeeTraining','PL03','Depinde de Payroll. Instruirea generică nu dovedește SSM/SU România.'),('CR','EmployeeRecruitment','PL04','Depinde de Payroll și Training. Descrierea publică este limitată.'),('CC','PayrollReport','PL05','Depinde de Payroll și Attendance.'),('CE','PerformanceEvaluation','PL06','Identificat în catalog; funcții și compatibilitate individuale neconfirmate.')]
for id,name,ref,note in cd:
    verified=id!='CE'
    prod(id,'CDSoftware '+name,'CDS '+name+'\n'+('test iD 10.0.0' if verified else 'versiune NC'),'Plugin iDempiere','Testat pe iDempiere 10.0.0; versiunea pluginului neconfirmată' if verified else 'Versiune și compatibilitate neconfirmate','Java / OSGi' if verified else 'Neconfirmat individual','GPLv2 declarat în catalog' if verified else 'Neconfirmată',note,[ref,'ID10'],'plugin')
prod('AM','AMERPSOFT Personnel & Payroll','AMERPSOFT\niD 12 în testare','Plugin iDempiere','README: iDempiere 12, Under Test; manualul modulului exemplifică JAR 11.0.0.202408050959','Java / OSGi','De clarificat','Modele AMN_. Nu combinați implicit cu alt motor salarial. Compatibilitatea cu 13 nu este demonstrată.',['PL07','PL08','PL17'],'plugin')
prod('IP','Ingeint Payroll','Ingeint Payroll\nversiune NC','Plugin iDempiere','Versiune și mentenanță curentă neconfirmate','Neconfirmat din cod recuperat','Neconfirmată','Identificat în catalog. Disponibilitatea actuală a sursei necesită verificare.',['PL10'],'plugin')
prod('IH','Ingeint Human Talent','Ingeint Human Talent\nrepository, versiune NC','Repository de extensie','Repository; release stabil neconfirmat','Java','Neconfirmată','Cod public identificat, fără manual sau release suficient pentru validarea funcțiilor.',['PL11'],'plugin')
prod('LP','Libero Payroll istoric','Libero Payroll\nistoric, neîntreținut','Plugin istoric','Versiune curentă neconfirmată; declarat neîntreținut','Neconfirmat din cod recuperat','Neconfirmată în selecția consultată','Referință istorică; pagina indică înlocuirea cu Ingeint.',['PL12'],'plugin')
prod('TW','iDempiere Taiwan HR mobil','Taiwan HR mobil\nversiune NC','Implementare / ofertă','Versiune, distribuție și licență neconfirmate','Bază iDempiere; client mobil neconfirmat','Neconfirmată','Ofertă HR mobilă. Funcțiile și sursa se cer furnizorului.',['PL18'],'hr')
prod('EX','Exvee ERP / 17tek','Exvee / 17tek\nversiune NC','ERP comercial bazat pe iDempiere','Versiune publică neidentificată','Bază iDempiere / Java','Condiții comerciale de confirmat','HR/payroll declarat. Nu este un plugin gratuit verificat.',['PL19'],'hr')
prod('AD','ADempiere HR/Payroll','ADempiere\n3.9.4 identificat','Produs ERP distinct','Release 3.9.4 identificat în pagina consultată; nu se afirmă că este ultima versiune','Java','De verificat pe release-ul ales','Origine comună cu iDempiere; modulele nu sunt pluginuri compatibile automat.',['PL14'],'hr')
prod('RO','Localization Romania','Localizare România\npagină 2020','Localizare iDempiere','Pagină în progres, actualizare indicată în 2020','Extensie iDempiere; detalii de verificat','Neconfirmată','Traducere și plan de conturi. Nu demonstrează payroll, D112, REGES sau SSM.',['PL13'],'localization')
prod('RE','BX Service iDempiere REST','iDempiere REST\nrepository, versiune NC','Plugin de integrare','Repository și documentație; tag compatibil cu 13 de fixat','Java / OSGi','De verificat pentru tagul ales','Adaugă REST; nu este modul HR. Nu reprezintă conector Frappe gata instalat.',['PL15','PL16'],'integration')
prod('CB','CDSoftware Base','CDS Base\nversiune NC','Dependență tehnică','Versiune și compatibilitate individuale neconfirmate','Neconfirmat individual','Neconfirmată individual','Menționat ca dependență pentru Payroll. Nu i se atribuie funcții HR autonome.',['PL01'],'dependency')
prod('CD','CDSoftware DetailNames','CDS DetailNames\nversiune NC','Dependență tehnică','Versiune și compatibilitate individuale neconfirmate','Neconfirmat individual','Neconfirmată individual','Menționat ca dependență pentru Payroll. Nu i se atribuie funcții HR autonome.',['PL01'],'dependency')
PD={p['id']:p for p in PRODUCTS}
LABEL={'Y':'✓ Da','P':'◐ Parțial','N':'✕ Nu','?':'? Neconfirmat','A':'— N/A'}
ROWS=[]
def row(chapter,feature,note='',scope='all'):
    rid='F'+str(len(ROWS)+1).zfill(3)
    r={'id':rid,'chapter':chapter,'feature':feature,'note':note,'scope':scope,'cells':{}}
    for p in PRODUCTS:
        c='?'
        if scope=='erp' and p['id']!='ID': c='A' if p['scope'] not in ['hr'] or p['id'] in ['FR','TW'] else '?'
        if scope=='hr' and p['scope'] in ['ssm','localization','integration','dependency']:c='A'
        if scope=='ssm' and p['scope'] in ['plugin','localization','integration','dependency']:c='A'
        r['cells'][p['id']]={'status':c,'detail':'Funcția nu este confirmată în sursele consultate pentru acest produs.' if c=='?' else 'În afara scopului acestui modul în comparație; funcțiile platformei de bază nu sunt atribuite extensiei.','refs':p['refs'][:2],'level':'Neconfirmat' if c=='?' else 'Delimitare de scop'}
    ROWS.append(r)
    return r
def setc(r,p,code,detail,refs=None,level=None):
    if isinstance(p,list):
        for id in p:setc(r,id,code,detail,refs,level)
        return
    r['cells'][p]={'status':code,'detail':detail,'refs':refs or PD[p]['refs'][:2],'level':level or ('Neconfirmat' if code=='?' else 'Documentație / cod' if code in ['Y','P'] else 'Delimitare explicită')}
def find(feature):return next(r for r in ROWS if r['feature']==feature)

# Tehnologie, licență și compatibilitate: negativele sunt explicite, nu deduse din lipsa unei pagini.
r=row('01 Tehnologie și acces','Implementare principală în Java')
setc(r,['ID','AX','OF','CP','CA','CT','CR','CC','AM','IH','AD','RE'],'Y','Java sau extensie Java/OSGi identificată în proiect/catalog.')
setc(r,'FR','N','Frappe HR folosește Python și JavaScript; nu este o aplicație Java.',['FR02'])
setc(r,['TW','EX'],'P','Bază iDempiere; stack-ul complet al ofertei nu este confirmat.')
r=row('01 Tehnologie și acces','Cod sursă public identificat')
setc(r,['ID','FR','AX','OF','AM','IH','AD','RE'],'Y','Repository public identificat; existența codului nu stabilește singură licența sau compatibilitatea.')
setc(r,['CP','CA','CT','CR','CC'],'P','Catalogul indică Sources; arhiva sursă și buildul nu au fost recuperate și validate.',['PL01','PL02','PL03','PL04','PL05'],'Catalog')
r=row('01 Tehnologie și acces','Licență software fără taxă pentru utilizare proprie')
setc(r,['ID','FR','AX','OF'],'Y','Licența open source a fost examinată. Găzduirea, adaptarea, integrarea și suportul sunt costuri separate.')
setc(r,['CP','CA','CT','CR','CC'],'Y','GPLv2 indicat în catalog; se verifică și licențele dependențelor.',['PL01','PL02','PL03','PL04','PL05'],'Catalog')
setc(r,'SM','P','Utilizare gratuită de bază declarată; semnăturile sunt contra cost.',['SM02'],'Declarație furnizor')
setc(r,['SS','SH'],'N','Platformă oferită comercial; nu s-a identificat ofertă integrală gratuită. ',None,'Ofertă comercială')
r=row('01 Tehnologie și acces','Instalare și găzduire proprie')
setc(r,['ID','FR','AX','OF'],'Y','Distribuție pentru instalare proprie; condițiile ediției și dependențele rămân aplicabile.')
setc(r,['CP','CA','CT','CR','CC','AM','IH','RE'],'P','Extensie sau cod pentru găzduire în iDempiere; instalarea pe versiunea țintă trebuie probată.')
r=row('01 Tehnologie și acces','Plugin nativ pentru iDempiere')
setc(r,['CP','CA','CT','CR','CC','AM','IH','RE'],'Y','Extensie iDempiere identificată. Aceasta nu confirmă testarea pe release 13.')
setc(r,['ID','CB','CD'],'A','Nucleu sau dependență; nu este o alternativă HR autonomă.')
setc(r,['FR','AX','OF','AD'],'N','Aplicație / produs separat, care necesită integrare sau portare.')
setc(r,['TW','EX'],'P','Implementare bazată pe iDempiere; distribuirea ca plugin reutilizabil nu este confirmată.')
r=row('01 Tehnologie și acces','Compatibilitate a extensiei demonstrată pe iDempiere 13')
for p in PRODUCTS:
    if p['scope'] not in ['plugin','integration','localization','dependency']:setc(r,p['id'],'A','Criteriu aplicabil extensiilor instalabile, nu aplicațiilor separate.')
for p in ['CP','CA','CT','CR','CC']:setc(r,p,'?','Catalogul indică testare pe 10.0.0, fără probă recuperată pentru 13.')
setc(r,'AM','?','README general indică 12 în testare; compatibilitatea cu 13 nu este demonstrată.')
r=row('01 Tehnologie și acces','Manual public detaliat identificat')
setc(r,['ID','FR','AX','OF','SS','AM','RE'],'Y','Manual sau documentație tehnică publică identificată. Ediția exactă este indicată în foaia Produse.')
setc(r,['CP','CA','CT','CR','CC'],'P','Pagini de catalog funcționale; unele descărcări wiki au fost refuzate.')
r=row('01 Tehnologie și acces','Pachet SSM integral gratuit, inclusiv semnături')
for p in PRODUCTS:
    if p['scope']!='ssm':setc(r,p['id'],'A','Criteriu comercial aplicabil platformelor SSM/SU.')
setc(r,['SS','SM','SH'],'N','Nu este oferită gratuitate integrală demonstrată, incluzând semnăturile și serviciile aferente.',['SS10','SM02','SH02'],'Ofertă comercială')

# Funcțiile nucleului iDempiere; scopul altor module nu este extins artificial.
for pi,chapter in [(2,'02 Platformă ERP'),(3,'03 Comercial și logistică'),(4,'04 Finanțe și operațiuni')]:
    for vals in PAGES[pi]['rows']:
        r=row(chapter,vals[0]+' — '+vals[1],vals[-1],scope='erp')
        code='P' if vals[0] in ['Planificare industrială extinsă','Integrare'] else 'Y'
        setc(r,'ID',code,'; '.join(vals[1:]),PAGES[pi]['refs'][:3])

# Transcriere explicită a matricelor HR din raport. D devine Da; dezvoltarea posibilă nu devine automat Parțial.
hr_codes=[
    ['YYYY','PYYY','YYYY','PYYY','?PYP','????','NYYY','NY P?'.replace(' ',''),'NY P?'.replace(' ',''),'PYPP','NYYY'],
    ['NYYY','NYY?','NY??','NP??','PYP?','YPPP','NPY?','YYY?','NYYY','NYYY','NYY?','NYP?'],
    ['YYYP','PYP?','N Y P P'.replace(' ',''),'NY??','NYP?','PYP?','NYYP','????','????','????','????']]
chapter_names=['05 Personal și recrutare','06 Timp și dezvoltare','07 Salarizare și România']
for k,pi in enumerate([10,11,12]):
    page=PAGES[pi]
    for j,vals in enumerate(page['rows']):
        code=hr_codes[k][j]
        assert len(code)==4,(vals,code)
        r=row(chapter_names[k],vals[0],scope='hr')
        for n,p in enumerate(['ID','FR','AX','OF']):
            detail=vals[n+1]
            if code[n]=='N':detail+='; funcția nu este atribuită nucleului standard, fiind indicată ca extensie sau dezvoltare.'
            if code[n]=='?':detail+='; acoperirea gata de utilizare nu este confirmată.'
            refs=([x for x in page['refs'] if x.startswith({'ID':'ID','FR':'FR','AX':'AX','OF':'OF'}[p])])
            if not refs:refs=PD[p]['refs'][:2]
            setc(r,p,code[n],detail,refs)

# Acoperirea individuală a extensiilor, fără a moșteni automat toate funcțiile ERP-ului.
def addon(p,features,code='Y',note='',refs=None,level=None):
    for f in features:setc(find(f),p,code,note or 'Funcție descrisă pentru acest modul în sursa indicată.',refs,level)
addon('CP',['Identitate angajat','Dosar personal extins','Poziții și atribuiri','Departamente HR','Remunerație de referință','Motor salarial complet','Componente și formule','Procesare colectivă','Contabilizare salarii'],note='Funcție descrisă pentru Payroll. Exemplele de localizare includ Panama; România nu este validată.',level='Catalog')
addon('CP',['Contracte de muncă'],'P','Payroll Contract include frecvențe de salarizare; nu dovedește un flux complet de CIM.',level='Catalog')
addon('CA',['Check-in și prezență','Terminale pontaj','Ture'],note='Import TXT, formate HIKVISION, ture rotative și întârzieri descrise în catalog.',level='Catalog')
addon('CT',['Instruire'],note='Planificare și urmărire instruiri; depinde de Payroll. Nu reprezintă automat instruire SSM/SU românească.',level='Catalog')
addon('CR',['Recrutare'],note='Recrutare și selecție descrise în catalog; depinde de Payroll și Training.',level='Catalog')
addon('CR',['Interviuri și feedback'],'?','Detaliul etapelor și formularelor nu este confirmat din descrierea publică.')
addon('CE',['Evaluarea performanței'],'?','Numele modulului este în catalog; nu se deduce funcționalitatea completă din denumire.')
addon('AM',['Identitate angajat','Departamente HR','Poziții și atribuiri','Remunerație de referință','Componente și formule'],'Y','Descris în documentația Personnel & Payroll. Modelele proprii folosesc prefixul AMN_.')
addon('AM',['Motor salarial complet','Contabilizare salarii','Procesare colectivă'],'P','Motor și procesare documentate; ediția pentru iDempiere 12 este declarată în testare. Localizarea RO este neconfirmată.')
addon('TW',['Portal angajat','Mobil HR'],'Y','Ofertă HR mobilă și acces angajat declarate. Distribuția și versiunea necesită confirmare.',level='Declarație furnizor')
addon('EX',['Dosar personal extins','Motor salarial complet'],'P','HR și payroll declarate la nivel de ofertă, fără demonstrarea fluxului și localizării RO.',level='Declarație furnizor')
addon('AD',['Motor salarial complet'],'P','Familie HR/Payroll într-un produs distinct. Nu dovedește compatibilitate ca plugin iDempiere.',['PL14'])
for p in ['CA','CT','CR','CC','CE','CB','CD','RE','RO']:
    for r in ROWS:
        if r['scope']=='hr' and r['cells'][p]['status']=='?':
            if p in ['CE'] and r['feature']=='Evaluarea performanței':continue
            setc(r,p,'A','Funcția este în afara rolului individual al extensiei sau este furnizată de o dependență; nu este atribuită acestui modul.')
for f in ['Stat de plată RO','D112','REGES-ONLINE','Conformitate SSM/SU RO','CIM și acte RO']:
    for p in ['ID','FR','AX','OF','CP','AM','IP','IH','LP','TW','EX','AD','RO']:setc(find(f),p,'?','Implementarea completă pentru România nu este confirmată din sursele consultate. Posibilitatea de configurare nu este o funcție livrată.')
for p in ['SS','SM','SH']:setc(find('Conformitate SSM/SU RO'),p,'?','Platformă orientată spre cerințe românești; conformitatea integrală pentru firma concretă nu este demonstrată prin prezentarea produsului.')
r=row('07 Salarizare și România','Împrumuturi angajați și contabilizare',scope='hr')
setc(r,'CP','Y','Împrumuturi către angajați și contabilizarea lor descrise pentru Payroll.',['PL01'],'Catalog')
r=row('07 Salarizare și România','Rapoarte payroll cu coloane multiple și exporturi',scope='hr')
setc(r,'CC','Y','Rapoarte și exporturi configurabile; depinde de Payroll și Attendance.',['PL05'],'Catalog')
setc(r,'FR','Y','Rapoarte payroll și procesare documentate; formatul legal RO nu este implicit.',['FR08','FR09'])
setc(r,'AX','P','Pregătire și export variabile payroll; nu demonstrează calcul net complet.',['AX08'])
r=row('07 Salarizare și România','Traducere română și plan de conturi România')
setc(r,'RO','P','Pagină în progres, actualizare 2020; traducere și plan de conturi, fără validare integrală curentă.',['PL13'],'Catalog')

# Matricele platformelor SSM/SU, cu statutul comercial păstrat în Dovezi.
ssm_codes=[['YYY','Y?Y','YYY','Y?Y','Y?Y','YYY','YYY','Y?Y','YYY','YYY','Y??'],['?P?','??Y','??Y','Y?Y','??Y','Y?Y','Y??','P?Y','???','???','Y??']]
for k,pi in enumerate([15,16]):
    for j,vals in enumerate(PAGES[pi]['rows']):
        name=vals[0]
        if name=='Cod public și self-host complet':continue
        if name=='Manual public detaliat':continue
        r=row('08 SSM/SU instruire' if k==0 else '09 SSM/SU operațiuni',name,scope='ssm')
        for n,p in enumerate(['SS','SM','SH']):
            refs=([x for x in PAGES[pi]['refs'] if x.startswith({'SS':'SS','SM':'SM','SH':'SH'}[p])])
            setc(r,p,ssm_codes[k][j][n],vals[n+1],refs, 'Neconfirmat' if ssm_codes[k][j][n]=='?' else 'Declarație furnizor' if p in ['SM','SH'] else 'Manual / API')
        if name=='Semnare electronică':r['note']='Disponibilitatea tehnică nu certifică singură validitatea circuitului pentru fiecare document.'
        if name=='Microsoft 365':r['note']='SSM.ro: SSO Entra. SafeHub: integrări Microsoft 365 declarate; acoperirile nu sunt identice.'
        if name=='API public':
            setc(r,'ID','P','Servicii și importuri în nucleu; REST extins prin plugin.',['ID02','PL15'])
            setc(r,'FR','Y','REST documentat la nivel Frappe.',['FR10'])
            setc(r,'AX','Y','Servicii web documentate în ADK; versiunea ADK trebuie corelată cu suita.',['AX10'])
            setc(r,'RE','Y','Plugin REST pentru iDempiere.',['PL15','PL16'])
extra_refs=['SSX021','SSX020','SSX023','SSX016','SSX017','SSX018','SSX038']
for j,vals in enumerate(PAGES[17]['rows']):
    name=vals[0]
    if name=='Registru accidente':name='Export registru accidente în Excel'
    r=row('10 Audit, arhivă și acces',name,vals[2],scope='ssm')
    setc(r,'SS','Y',vals[1]+' '+vals[2],[extra_refs[j]],'Manual')
    if name=='SSO':setc(r,'SH','Y','SSO Microsoft 365 declarat; protocolul și configurația se confirmă.',['SH01'],'Declarație furnizor')

# Documente distincte care nu sunt echivalente cu existența unei funcții generice.
docs=[
('Fișă individuală de instruire SSM','SS03','Y?Y'),
('Fișă de instruire SU','SS03','Y?Y'),
('Plan de prevenire și protecție complet','SS03','???'),
('Dosar complet de cercetare accident','SSX021','???'),
('Plan de evacuare / intervenție specific amplasamentului','SS03','???'),
('Arhivă integrală exportabilă cu toate dovezile de semnare','SS05','???')]
for name,ref,codes in docs:
    r=row('11 Documente și conformitate',name,'Se cere documentul real, cu date, versiuni, semnături și dovezi; un generator generic nu dovedește completitudinea.',scope='ssm')
    for i,p in enumerate(['SS','SM','SH']):setc(r,p,codes[i],'Documentare a fișelor de instruire.' if codes[i]=='Y' and p=='SS' else 'Fișe de instruire declarate de furnizor.' if codes[i]=='Y' else 'Documentul complet și circuitul pentru cazul firmei nu sunt confirmate.',[ref] if p=='SS' else PD[p]['refs'][:1], 'Manual' if p=='SS' else 'Declarație furnizor' if codes[i]=='Y' else 'Neconfirmat')
for name in ['Act adițional la CIM în forma utilizată în România','Decizie HR cu istoric și dată efectivă']:
    row('11 Documente și conformitate',name,'Necesită exemplu și validare locală.',scope='hr')
r=row('12 Integrare','Webhooks documentate')
setc(r,'FR','Y','Webhooks documentate la nivel Frappe; evenimentele și permisiunile trebuie configurate.',['FR11'])
r=row('12 Integrare','Conector iDempiere–Frappe gata de utilizare')
for p in PRODUCTS:setc(r,p['id'],'?','În cercetarea efectuată nu a fost demonstrat un conector complet gata de utilizare. API disponibil nu înseamnă integrare implementată.')
r=row('12 Integrare','Sincronizare contacte prin API SSM')
for p in PRODUCTS:
    if p['scope']!='ssm':setc(r,p['id'],'A','Criteriu al platformei SSM; conectorul către HR/ERP se implementează separat.')
setc(r,'SS','Y','Operații pentru contacte documentate în API.',['SS05'],'API')
r=row('12 Integrare','Raport API al documentelor nesemnate')
for p in PRODUCTS:
    if p['scope']!='ssm':setc(r,p['id'],'A','Criteriu al platformei SSM.')
setc(r,'SS','Y','Raport draft_signatures documentat.',['SS05'],'API')
r=row('12 Integrare','Export API complet al documentelor și dovezilor SSM')
for p in PRODUCTS:
    if p['scope']!='ssm':setc(r,p['id'],'A','Criteriu al platformei SSM.')

# Fiecare celulă evaluată are explicație și URL-uri recuperabile; N/A se explică în legendă și catalog.
evidence=[]
for r in ROWS:
    for p in PRODUCTS:
        c=r['cells'][p['id']]
        assert c['status'] in LABEL
        assert all(x in SD for x in c['refs']),(r['id'],p['id'],c['refs'])
        if c['status']=='A':continue
        refs=c['refs'][:3]
        evidence.append([r['id'],r['feature'],p['name'],LABEL[c['status']],c['detail'],c['level'],', '.join(refs),' ; '.join(SD[s]['url'] for s in refs),r['note']])
data={'date':'08.10.2026','products':PRODUCTS,'rows':ROWS,'labels':LABEL,'evidence':evidence,'sources':SD,'chapters':list(dict.fromkeys(r['chapter'] for r in ROWS))}
(BASE/'date_comparativ_excel.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'produse_module':len(PRODUCTS),'functii':len(ROWS),'capitole':len(data['chapters']),'evaluari_documentate':len(evidence)},ensure_ascii=False))
