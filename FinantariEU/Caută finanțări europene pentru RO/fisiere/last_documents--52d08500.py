import json,re,shutil,hashlib,io,zipfile,requests,unicodedata
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from pypdf import PdfReader
from research import fetch,CACHE,BASE
OUT=BASE/'F';cat=json.loads((BASE/'catalogue.json').read_text(encoding='utf8'));byid={r['id']:r for r in cat}
sources={'CME_2026_Call':'https://culture.ec.europa.eu/culture-moves-europe/call-for-individual-mobility','CME_2026_Doc':'https://culture.ec.europa.eu/resources/document-library/call-document-for-individual-mobility-2026-2027','IF26_SME':'https://climate.ec.europa.eu/areas-action/eu-funding-climate-action/innovation-fund/calls-proposals/if26-sme-call_en','IF26_NZT':'https://climate.ec.europa.eu/areas-action/eu-funding-climate-action/innovation-fund/calls-proposals/if26-nzt-call_en','IF26_Maritime':'https://climate.ec.europa.eu/areas-action/eu-funding-climate-action/innovation-fund/calls-proposals/if26-maritime-call_en','CleanHydrogen_Call':'https://www.clean-hydrogen.europa.eu/apply-funding/call-proposals-0_en','CleanAviation_Ref':'https://www.clean-aviation.eu/about-us/reference-documents','SMP_Official_Docs':'https://commission.europa.eu/publications/single-market-programme-legal-texts-and-factsheets_en'}
with ThreadPoolExecutor(max_workers=4) as pool:
 for f in as_completed([pool.submit(fetch,x) for x in sources.items()]):print('SOURCE',f.result(),flush=True)
plan=[]
for key,id in [('CME_2026_Doc','CME'),('IF26_SME','INNOV'),('IF26_NZT','INNOV'),('IF26_Maritime','INNOV'),('CleanHydrogen_Call','JUHY'),('CleanAviation_Ref','JUCA'),('SMP_Official_Docs','SMP')]:
 d=json.loads((CACHE/(key+'.json')).read_text(encoding='utf8'))
 for a in d.get('documents',[]):
  u=a['url'];label=a['context'] or a['label']
  if not re.search(r'\.(pdf|docx?|xlsx?|zip)(?:[?#]|$)',u,re.I) and '/document/download/' not in u:continue
  if any(x in label.lower() for x in ['privacy','data protection','notice']):continue
  if key in ['CleanHydrogen_Call','CleanAviation_Ref','SMP_Official_Docs'] and not any(x in label+' '+u for x in ['2026','2025','2027']):continue
  if key=='CleanAviation_Ref' and not any(x in (label+' '+u).lower() for x in ['work programme','work-programme','work_programme','2026']):continue
  archive=(key in ['CleanHydrogen_Call','CleanAviation_Ref'] and '2027' not in label+' '+u) or ('2025-2026' in u and id=='CME')
  plan.append({'program':id,'url':u,'label':label,'source':d['url'],'archive':archive})
plan.append({'program':'INNOV','url':'https://climate.ec.europa.eu/document/download/8f9ea27e-38dc-4cb5-a804-252892192b73_en','label':'IF26 SME - prezentare consultare 19 iunie 2026; nu este ghid final','source':sources['IF26_SME'],'archive':False})
def get(d):
 row={**d,'ok':False}
 try:
  r=requests.get(d['url'],timeout=(12,35),headers={'User-Agent':'Mozilla/5.0'});r.raise_for_status();raw=r.content
  assert raw.startswith(b'%PDF-'),'Serverul nu a furnizat PDF original'
  row.update(ok=True,ext='.pdf',bytes=len(raw),pages=len(PdfReader(io.BytesIO(raw)).pages),sha256=hashlib.sha256(raw).hexdigest())
  sub='0.ARHIVA' if d['archive'] else '1.DOCUMENTE OFICIALE';folder=OUT/byid[d['program']]['folder']/sub;folder.mkdir(parents=True,exist_ok=True)
  title=unicodedata.normalize('NFKD',d['label']).encode('ascii','ignore').decode();title=re.sub(r'[<>:"/\\|?*\x00-\x1f]',' ',title);title=re.sub(r'\s+',' ',title).strip(' .');maxlen=max(12,244-len(str(folder))-14)
  target=folder/(title[:min(60,maxlen)].rstrip(' .')+'_'+row['sha256'][:8]+'.pdf');target.write_bytes(raw);row['relative_path']=target.relative_to(OUT).as_posix()
 except Exception as e:row['error']=str(e)[:250]
 return row
m=json.loads((BASE/'manifest.json').read_text(encoding='utf8'));known={(d['program'],d['url']) for d in m};plans={ (d['program'],d['url']):d for d in plan if (d['program'],d['url']) not in known}
print('LAST_DOCUMENTS',len(plans),flush=True)
with ThreadPoolExecutor(max_workers=4) as pool:
 for f in as_completed([pool.submit(get,d) for d in plans.values()]):
  d=f.result();m.append(d);print('DOC',d['ok'],d['url'],d.get('error',''),flush=True)
(BASE/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8')
print('LAST_DOCS_DONE',flush=True)
