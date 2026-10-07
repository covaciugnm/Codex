import json,re,shutil
from concurrent.futures import ThreadPoolExecutor,as_completed
from downloads import BASE,OUT,CACHE,download,clean
from research import fetch
cat=json.loads((BASE/'catalogue.json').read_text(encoding='utf8')); byid={r['id']:r for r in cat}
sources={
'EYF_2027':'https://www.coe.int/en/web/kyiv/-/announcing-the-eyf-call-for-proposals-for-international-one-off-youth-co-operation-activities-and-international-long-term-youth-co-operation-projects-with-the-deadline-of-1-october-2026',
'Swiss_ECO_Update':'https://www.swiss-contribution.ro/web/swiss/noutati/-/asset_publisher/31kQDN4YO3VO/content/noutati_20260701',
'Swiss_ECO_Guide':'https://economie.gov.ro/procedura-de-implementare-a-programului-pentru-consolidarea-imm-urilor-prin-acces-imbunatatit-la-finantare-sme-eco-tech-consolidata/',
'Swiss_VET_Operator':'https://www.cndipt.ro/operator-de-program/',
'Swiss_Consultants':'https://roreg.eu/programul-roeea/consultan%C8%9Bi-certifica%C8%9Bi-eea',
'Innowwide_Apply':'https://www.eurekanetwork.org/apply/',
'CEF_Energy_Call':'https://cinea.ec.europa.eu/funding-opportunities/calls-proposals/cef-energy-2025-cross-border-renewable-energy-projects-call-works-studies_en',
'Eurimages':'https://www.coe.int/en/web/eurimages/co-production-funding'}
with ThreadPoolExecutor(max_workers=4) as pool:
 for f in as_completed([pool.submit(fetch,i) for i in sources.items()]): print('PAGE',f.result(),flush=True)
plan=[]
def add(id,url,label,source='',archive=False): plan.append({'program':id,'url':url,'label':label,'source':source or byid[id]['source'],'archive':archive})
for id,slug in {'CH01':'xBGFU4GL3Jfw/dual-vet-programme.pdf','CH02':'oH9pVYsPsmIb/international-research-cooperation-programme.pdf','CH03':'IcTgQUQPuMe8/emissions-research-monitoring-infrastructure-programme.pdf','CH04':'ABn4-RblFWVZ/smes-programme.pdf','CH05':'Mbk3i98hC-pT/internal-affairs-programme.pdf','CH06':'GYL5CfyMeT1M/justice-programme.pdf','CH07':'9AEyDlWxRJeK/energy-efficiency-renewable-energy-programme.pdf','CH08':'yre7-hH9sIz4/metrorex-programme.pdf','CH09':'WJkU1RWmDoMX/health-programme.pdf','CH10':'rIF5WVvYfpvy/social-inclusion-programme.pdf','CH11':'PHSK7tlLVQ7Y/civic-engagement-programme-july-2026.pdf'}.items():
 add(id,'https://www.schweiz-rumaenien.eda.admin.ch/dam/en/eda-cms/'+slug,'FDFA Factsheet '+byid[id]['title'])
solid=json.loads((CACHE/'Solidarity.json').read_text(encoding='utf8'))
for d in solid.get('documents',[]):
 if re.search(r'2026_(en|ro)(?:_\d+)?\.pdf',d['url'],re.I): add('ESC',d['url'],'European Solidarity Corps Guide 2026 '+d['url'].rsplit('/',1)[-1],solid['url'])
for key,id,archive in [('EYF_2027','EYF',False),('Swiss_ECO_Guide','CH04',False),('Swiss_VET_Operator','CH01',True),('Swiss_Consultants','CH07',True),('Innowwide_Apply','INNOWWIDE',False),('CEF_Energy_Call','CEFE',True)]:
 d=json.loads((CACHE/(key+'.json')).read_text(encoding='utf8'))
 for doc in d.get('documents',[]):
  if re.search(r'\.(pdf|docx?|xlsx?|zip)(?:[?#]|$)',doc['url'],re.I) or '/document/download/' in doc['url'] or 'rm.coe.int' in doc['url']: add(id,doc['url'],doc['label'] or doc['context'][:150],d['url'],archive)
for id,url,label in [
 ('EYF','https://rm.coe.int/call-2027-one-off-1-october-2026-2756-4971-9575-v/48802d01da','EYF 2027.C5.A Call overview'),
 ('EYF','https://rm.coe.int/call-2027-long-term-1-october-2026-2772-6033-2311-v-1/48802d0217','EYF 2027.C6.B Call overview'),
 ('EU4H','https://hadea.ec.europa.eu/document/download/f34c373c-a925-407f-b811-396fa4c118da_en','EU4Health FAQ EU4H-2026-SANTE-PJ'),
 ('AGRIP','https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/agrip/wp-call/2026/call-fiche_agrip-multi-2026_en.pdf','AGRIP MULTI 2026 Call fiche'),
 ('EUIPO','https://euipo.europa.eu/tunnel-web/secure/webdav/guest/document_library/contentPdfs/about_euipo/Grants/GR_001_26/gr_001_26_call_notice_en.pdf','SME Fund 2026 Call notice - URL de verificat')]:
 if id in byid:add(id,url,label,archive=id=='AGRIP')
reg=json.loads((CACHE/'Norway_Archive_Docs.json').read_text(encoding='utf8'))
for d in reg.get('documents',[]):
 if any(t in d['url'] for t in ['1041-','1040-','1039-']):
  for id in ['N01','N02','N03','N04','N05','N06','N07','N08','N09']: add(id,d['url'],d['label'] or d['context'],reg['url'])
unique={x['url']:x for x in plan};print('EXTRA_URLS',len(unique),flush=True)
results={}
with ThreadPoolExecutor(max_workers=3) as pool:
 for f in as_completed([pool.submit(download,u,True) for u in unique]):
  d=f.result();results[d['url']]=d;print('EXTRA',d['ok'],d['url'],d.get('error','')[:100],flush=True)
manifest=json.loads((BASE/'manifest.json').read_text(encoding='utf8'));existing={(d['program'],d['url']) for d in manifest}
for item in plan:
 if (item['program'],item['url']) in existing:continue
 existing.add((item['program'],item['url'])); d={**item,**results[item['url']]}
 if d['ok']:
  sub='0.ARHIVA' if d['archive'] else '1.DOCUMENTE OFICIALE'
  if any(x in d['label'].lower() for x in ['annex','application form','budget','anexa']):sub+='/ANEXE'
  folder=OUT/byid[d['program']]['folder']/sub;folder.mkdir(parents=True,exist_ok=True)
  mx=max(12,244-len(str(folder))-10-len(d['ext']))
  dest=folder/(clean(d['label'],min(60,mx))+'_'+d['sha256'][:8]+d['ext']);shutil.copy2(d['file'],dest)
  d['relative_path']=dest.relative_to(OUT).as_posix()
 manifest.append(d)
(BASE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print('EXTRAS_DONE',sum(x['ok'] for x in results.values()),'/',len(results),flush=True)
